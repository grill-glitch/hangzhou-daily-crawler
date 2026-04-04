#!/usr/bin/env python3
"""
都市快报数字版爬虫
完整抓取指定日期的所有文章内容和元数据

用法：
    python3 dskb_crawler.py 2026-03-29

输出：
    dskb_YYYY-MM-DD.json - 所有文章的结构化数据
    dskb_YYYY-MM-DD/ - 单篇文章文件（可选）
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
BASE_URL = "https://mdaily.hangzhou.com.cn"
USER_AGENT = "Mozilla/5.0 (compatible; OpenClaw-Crawler/1.0)"
DELAY = 1  # 请求间隔（秒），避免给服务器造成压力


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


def parse_article_list(html: str, date_str: str) -> List[Dict[str, Any]]:
    """
    解析文章列表页，提取所有文章信息
    
    参数：
        html: 列表页HTML
        date_str: 日期字符串 YYYY-MM-DD
    
    返回：
        文章列表，每个文章包含 section, title, url, date 等字段
    """
    import urllib.parse
    
    articles = []
    
    # 计算日期路径
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    date_path = dt.strftime('%Y/%m/%d')
    
    # 提取所有链接和文本 - 处理换行和空格
    link_pattern = r'href=["\']([^"\'\s>]+?\.html)["\'][^>]*>([^<]+)<'
    links = re.findall(link_pattern, html, re.DOTALL)
    
    # 版块名称映射
    section_names = {
        'A01': '都市快报',
        'A02': '中国新闻',
        'A03': '杭州新闻',
        'A04': '热线新闻',
        'A05': '快报为你寄思念',
        'A06': '很短很新鲜',
        'A07': '告别新闻',
        'A08': '天气与生活',
        'B01': '杭州Discovery',
        'B02': '杭州Discovery',
        'B03': '狮子少年',
        'B04': '狮子少年',
        'B05': '狮子少年',
        'B06': '财经新闻',
        'B07': '大家健康',
        'B08': '橙柿家',
    }
    
    for rel_url, title in links:
        # 只处理文章详情链接
        if not rel_url.startswith('article_detail_'):
            continue
        
        # 从URL提取版块代码，例如 article_detail_2_20260329A0119.html -> A01
        section_match = re.search(r'article_detail_\d+_\d{8}([A-Z0-9]+)', rel_url)
        if not section_match:
            continue
            
        section_code = section_match.group(1)
        section_name = section_names.get(section_code, f'第{section_code}版')
        
        # 构造完整URL
        full_url = f"{BASE_URL}/dskb/{date_path}/{rel_url}"
        articles.append({
            'section': section_code,
            'section_name': section_name,
            'title': title.strip(),
            'url': full_url,
            'date': date_str,
            'relative_url': rel_url
        })
    
    return articles


def parse_article_detail(html: str) -> Dict[str, Any]:
    """解析文章详情页，提取正文内容"""
    from html import unescape
    
    # 提取标题
    title_match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    title = unescape(title_match.group(1).strip()) if title_match else ""
    title = title.replace('都市快报-', '').strip()
    
    # 提取正文 - 移除HTML标签
    content = html
    
    # 移除脚本、样式
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<header[^>]*>.*?</header>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # 保留换行
    content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)
    content = re.sub(r'</p>', '\n', content, flags=re.IGNORECASE)
    content = re.sub(r'<p[^>]*>', '\n', content, flags=re.IGNORECASE)
    
    # 移除所有剩余HTML标签
    content = re.sub(r'<[^>]+>', ' ', content)
    
    # HTML实体转义
    content = unescape(content)
    
    # 清理空白
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    # 提取作者
    author_match = re.search(r'记者\s+([^\s\n]+)', content)
    author = author_match.group(1) if author_match else ""
    
    # 提取日期
    date_match = re.search(r'(\d{4})[-年](\d{1,2})[-月](\d{1,2})日?', content)
    if date_match:
        publish_date = f"{date_match.group(1)}-{int(date_match.group(2)):02d}-{int(date_match.group(3)):02d}"
    else:
        publish_date = ""
    
    return {
        'title': title,
        'author': author,
        'publish_date': publish_date,
        'content': content,
        'word_count': len(content)
    }


def crawl_newspaper(date_str: str, save_individual: bool = False) -> Dict[str, Any]:
    """
    爬取指定日期的完整报纸
    
    参数：
        date_str: 日期字符串，格式 YYYY-MM-DD
        save_individual: 是否保存单篇文章为单独文件
    
    返回：
        包含所有文章数据的字典
    """
    print(f"开始爬取《都市快报》{date_str} ...")
    
    # 构建列表页URL
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    date_no_dash = dt.strftime('%Y%m%d')
    date_path = dt.strftime('%Y/%m/%d')
    
    list_url = f"{BASE_URL}/dskb/{date_path}/article_list_{date_no_dash}.html"
    print(f"列表页: {list_url}")
    
    html = fetch_page(list_url)
    if not html:
        print("无法获取列表页", file=sys.stderr)
        return {'error': 'Failed to fetch list page'}
    
    articles = parse_article_list(html, date_str)
    print(f"发现 {len(articles)} 篇文章")
    
    # 创建输出目录
    output_dir = None
    if save_individual:
        output_dir = f"dskb_{date_str}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    # 抓取每篇文章详情
    all_data = {
        'date': date_str,
        'list_url': list_url,
        'total_articles': len(articles),
        'articles': []
    }
    
    for idx, article in enumerate(articles, 1):
        print(f"[{idx}/{len(articles)}] 抓取: {article['title'][:50]}...")
        
        detail_html = fetch_page(article['url'])
        if detail_html:
            detail_data = parse_article_detail(detail_html)
            article.update(detail_data)
        else:
            article['content'] = ""
            article['author'] = ""
            article['publish_date'] = ""
            article['word_count'] = 0
        
        # 保存单篇文章（可选）
        if output_dir:
            safe_title = re.sub(r'[^\w\-_.]', '_', article['title'])[:100]
            filename = f"{article['section']}_{safe_title}.json"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(article, f, ensure_ascii=False, indent=2)
        
        all_data['articles'].append(article)
        time.sleep(DELAY)  # 礼貌延迟
    
    # 保存完整JSON
    json_file = f"dskb_{date_str}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成！数据已保存到 {json_file}")
    if output_dir:
        print(f"单篇文章已保存到 {output_dir}/ 目录")
    
    # 统计
    sections = {}
    for art in all_data['articles']:
        sec = art['section']
        sections[sec] = sections.get(sec, 0) + 1
    
    print("\n按版块统计:")
    for sec, count in sorted(sections.items()):
        print(f"  {sec}: {count}篇")
    
    total_words = sum(art.get('word_count', 0) for art in all_data['articles'])
    print(f"总字数: {total_words:,}")
    
    return all_data


def main():
    if len(sys.argv) < 2:
        print("用法: python3 dskb_crawler.py YYYY-MM-DD [--individual]")
        print("示例: python3 dskb_crawler.py 2026-03-29 --individual")
        sys.exit(1)
    
    date_str = sys.argv[1]
    save_individual = '--individual' in sys.argv
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("错误：日期格式必须是 YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)
    
    crawl_newspaper(date_str, save_individual)


if __name__ == '__main__':
    main()
