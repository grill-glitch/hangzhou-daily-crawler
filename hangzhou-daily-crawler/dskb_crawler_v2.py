#!/usr/bin/env python3
"""
都市快报数字版爬虫（纯文本版）
基于 page_detail + article_list iframe 结构

用法：
    python3 dskb_crawler_v2.py 2026-03-29 [--individual] [--output-dir DIR]

输出：
    dskb_YYYY-MM-DD.json - 所有文章结构化数据
    dskb_YYYY-MM-DD/    - 单篇文章文件（可选）
"""

import requests
import re
import json
import sys
import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import urllib.parse

# 配置
BASE_URL = "https://hzdaily.hangzhou.com.cn"
USER_AGENT = "Mozilla/5.0 (compatible; OpenClaw-Crawler/1.0)"
DELAY = 1  # 请求间隔（秒）


def fetch_page(url: str) -> Optional[str]:
    """抓取页面HTML"""
    try:
        headers = {'User-Agent': USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        return resp.text
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def get_page_sections(date_str: str) -> List[Dict[str, str]]:
    """
    从 page_list_YYYYMMDD.html 获取所有版块信息
    
    实际HTML结构：
        <a href="page_detail_2_YYYYMMDDA01.html" title="都市快报">第A01版：都市快报</a>
    """
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    date_no_dash = dt.strftime('%Y%m%d')
    
    list_url = f"{BASE_URL}/dskb/{date_str.replace('-', '/')}/page_list_{date_no_dash}.html"
    html = fetch_page(list_url)
    if not html:
        print(f"无法获取版块列表: {list_url}", file=sys.stderr)
        return []
    
    # 提取版块链接 - 匹配 <a href="page_detail_2_...html" title="...">第A01版：名称</a>
    pattern = r'<a[^>]*href=["\']([^"\']+\.html)["\'][^>]*title=["\'][^"\']+["\'][^>]*>第([A-Z0-9]+)版：([^<]+)</a>'
    links = re.findall(pattern, html, re.DOTALL)
    
    sections = []
    for href, code, name in links:
        # 只处理主版块（排除重复的）
        if code in [s['code'] for s in sections]:
            continue
        full_url = urllib.parse.urljoin(f"{BASE_URL}/dskb/{date_str.replace('-', '/')}/", href)
        sections.append({
            'code': code,
            'name': name.strip(),
            'url': full_url,
            'href': href
        })
    
    return sections


def get_articles_from_section(section_url: str) -> List[Dict[str, str]]:
    """
    从版块的文章列表 iframe 页面提取文章
    
    页面地址格式：article_list_2_YYYYMMDDAXX.html
    实际HTML结构：
        <li><a href="article_detail_2_YYYYMMDSAXX123.html" target="_parent">文章标题</a></li>
    """
    html = fetch_page(section_url)
    if not html:
        return []
    
    # 提取所有 <a href="...">标题</a> 链接
    link_pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
    all_links = re.findall(link_pattern, html, re.DOTALL)
    
    # 过滤只保留文章详情链接
    articles = []
    for rel_url, title in all_links:
        if not rel_url.startswith('article_detail_'):
            continue  # 跳过PDF下载、翻页等非文章链接
        
        title = title.strip()
        if not title:
            continue
        
        full_url = urllib.parse.urljoin(os.path.dirname(section_url) + '/', rel_url)
        articles.append({
            'title': title,
            'url': full_url,
            'relative_url': rel_url
        })
    
    return articles


def extract_text_from_body(html: str) -> str:
    """从HTML的body中提取清理后的文本"""
    from html import unescape
    
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    if not body_match:
        return ""
    
    content = body_match.group(1)
    
    # 移除不需要的标签
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<header[^>]*>.*?</header>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # 转换为文本
    content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)
    content = re.sub(r'</p>', '\n', content, flags=re.IGNORECASE)
    content = re.sub(r'<p[^>]*>', '\n', content, flags=re.IGNORECASE)
    content = re.sub(r'<[^>]+>', ' ', content)
    content = unescape(content)
    
    # 空白字符处理
    content = content.replace('\u3000', ' ')
    content = content.replace('\t', ' ')
    
    # 按行清理
    lines = content.split('\n')
    cleaned_lines = []
    prev_blank = False
    
    for line in lines:
        stripped = line.strip()
        
        # 跳过导航行
        if any(keyword in stripped for keyword in ['上一篇', '下一篇>>', '返回主页']):
            continue
        
        # 跳过纯分隔线
        if re.fullmatch(r'[-=_=]{2,}', stripped):
            continue
        
        if not stripped:
            if not prev_blank:
                cleaned_lines.append('')
                prev_blank = True
        else:
            cleaned_lines.append(stripped)
            prev_blank = False
    
    content = '\n'.join(cleaned_lines)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()


def parse_article_detail(html: str) -> Dict[str, Any]:
    """解析文章详情页（纯文本版）"""
    from html import unescape
    
    # 提取标题
    title_match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    title = unescape(title_match.group(1).strip()) if title_match else ""
    title = title.replace('都市快报-', '').strip()
    
    # 从 body 提取文本
    content = extract_text_from_body(html)
    word_count = len(content)
    
    # 提取作者和日期
    author_match = re.search(r'记者\s+([^\s\n]+)', content)
    author = author_match.group(1) if author_match else ""
    
    date_match = re.search(r'(\d{4})[-年](\d{1,2})[-月](\d{1,2})日?', content)
    if date_match:
        publish_date = f"{date_match.group(1)}-{int(date_match.group(2)):02d}-{int(date_match.group(3)):02d}"
    else:
        publish_date = ""
    
    # 移除正文开头的重复标题
    if title and title.strip():
        title_clean = title.strip()
        content_stripped = content.lstrip()
        if content_stripped.startswith(title_clean):
            content = content[content.find(title_clean) + len(title_clean):].lstrip()
            word_count = len(content)
    
    return {
        'title': title,
        'author': author,
        'publish_date': publish_date,
        'content': content,
        'word_count': word_count
    }


def crawl_newspaper(date_str: str, save_individual: bool = False) -> Dict[str, Any]:
    """
    爬取指定日期的完整报纸
    
    步骤：
    1. 从 page_list_YYYYMMDD.html 获取所有版块
    2. 对每个版块，抓取 article_list_2_YYYYMMDDAXX.html 获取文章列表
    3. 批量抓取文章详情
    """
    print(f"开始爬取《都市快报》{date_str} ...")
    
    # 步骤 1: 获取所有版块
    sections = get_page_sections(date_str)
    if not sections:
        print("未找到任何版块", file=sys.stderr)
        return {'error': 'No sections found'}
    
    print(f"发现 {len(sections)} 个版块:")
    for s in sections:
        print(f"  {s['code']}: {s['name']}")
    
    # 创建输出目录
    output_dir = None
    if save_individual:
        output_dir = f"dskb_{date_str}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    # 步骤 2 & 3: 遍历版块，抓取文章
    all_articles = []
    total_count = 0
    
    for section_idx, section in enumerate(sections, 1):
        print(f"\n[{section_idx}/{len(sections)}] 版块 {section['code']}: {section['name']}")
        
        # 获取该版块的文章列表 (将 page_detail 转换为 article_list)
        article_list_url = section['url'].replace('page_detail_2_', 'article_list_2_')
        articles = get_articles_from_section(article_list_url)
        print(f"  发现 {len(articles)} 篇文章")
        
        for art_idx, article in enumerate(articles, 1):
            print(f"  [{art_idx}/{len(articles)}] 抓取: {article['title'][:50]}...")
            
            detail_html = fetch_page(article['url'])
            if detail_html:
                detail_data = parse_article_detail(detail_html)
                article.update(detail_data)
            else:
                article['content'] = ""
                article['author'] = ""
                article['publish_date'] = ""
                article['word_count'] = 0
            
            article['section_code'] = section['code']
            article['section_name'] = section['name']
            article['date'] = date_str
            
            # 保存单篇文章
            if output_dir:
                safe_title = re.sub(r'[^\w\-_.]', '_', article['title'])[:100]
                filename = f"{section['code']}_{safe_title}.json"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(article, f, ensure_ascii=False, indent=2)
            
            all_articles.append(article)
            total_count += 1
            time.sleep(DELAY)
    
    # 构建结果
    result = {
        'date': date_str,
        'total_sections': len(sections),
        'total_articles': total_count,
        'sections': sections,
        'articles': all_articles
    }
    
    # 保存汇总 JSON
    json_file = f"dskb_{date_str}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成！共抓取 {len(sections)} 个版块、{total_count} 篇文章")
    print(f"数据已保存到 {json_file}")
    if output_dir:
        print(f"单篇文章已保存到 {output_dir}/ 目录")
    
    # 统计
    section_counts = {}
    for art in all_articles:
        sec = art['section_code']
        section_counts[sec] = section_counts.get(sec, 0) + 1
    
    print("\n按版块统计:")
    for sec, count in sorted(section_counts.items()):
        sec_name = next((s['name'] for s in sections if s['code'] == sec), '')
        print(f"  {sec} ({sec_name}): {count}篇")
    
    total_words = sum(art.get('word_count', 0) for art in all_articles)
    print(f"总字数: {total_words:,}")
    
    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python3 dskb_crawler_v2.py 2026-03-29 [--individual] [--output-dir DIR]")
        sys.exit(1)
    
    date_str = sys.argv[1]
    save_individual = '--individual' in sys.argv or '--output-dir' in sys.argv
    output_dir = None
    
    # 解析可选参数
    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == '--individual':
            save_individual = True
        elif arg == '--output-dir' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("错误：日期格式必须是 YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)
    
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    result = crawl_newspaper(date_str, save_individual)
    if 'error' in result:
        print(f"爬取失败: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
