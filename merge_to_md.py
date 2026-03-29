#!/usr/bin/env python3
"""
将指定日期的所有文章合并为单个 Markdown 文件

用法：
    python3 merge_to_md.py 2026-03-29 [--output DIR] [--title "标题"]
    
输出：
    output/dskb_2026-03-29.md - 合并后的 Markdown 文件
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def load_data(date_str):
    """加载指定日期的 JSON 数据"""
    filename = f"dskb_{date_str}.json"
    if not os.path.exists(filename):
        print(f"错误：文件 {filename} 不存在", file=sys.stderr)
        print("请先运行 dskb_crawler_v2.py 抓取数据", file=sys.stderr)
        sys.exit(1)
    
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def escape_markdown(text):
    """转义 Markdown 特殊字符（在代码块内不需要，但为了安全起见）"""
    # 在正文中，我们保留原始格式，只在标题等地方做必要处理
    return text

def slugify(text):
    """生成 Markdown 锚点友好的 slug"""
    # 移除特殊字符，保留中文、英文、数字
    import re
    # 将中文、英文、数字转换为连字符分隔的小写形式
    text = text.lower()
    text = re.sub(r'[^\w\u4e00-\u9fff\-]+', '-', text)  # 保留中文、字母、数字、连字符
    text = re.sub(r'-+', '-', text)  # 合并多个连字符
    text = text.strip('-')
    return text

def generate_markdown(data, title_prefix=None):
    """生成 Markdown 内容"""
    date_str = data['date']
    total_articles = data['total_articles']
    total_sections = data['total_sections']
    
    if title_prefix:
        md_title = f"# {title_prefix} - {date_str}"
    else:
        md_title = f"# 都市快报 {date_str} 全部文章"
    
    # 按版块分组并收集信息用于生成目录
    articles_by_section = {}
    for art in data['articles']:
        section_code = art['section_code']
        if section_code not in articles_by_section:
            articles_by_section[section_code] = {
                'name': art['section_name'],
                'articles': []
            }
        articles_by_section[section_code]['articles'].append(art)
    
    # 生成目录
    toc_lines = [
        "## 📋 目录",
        "",
        "### 版块"
    ]
    
    for section_code in sorted(articles_by_section.keys()):
        section = articles_by_section[section_code]
        section_slug = f"#{section_code}-{slugify(section['name'])}"
        toc_lines.append(f"- [{section_code} {section['name']}]({section_slug}) ({len(section['articles'])} 篇)")
    
    toc_lines.append("")
    
    # 生成文章详细目录（可选，根据文章数量决定是否生成）
    total_articles_count = len(data['articles'])
    if total_articles_count <= 200:  # 如果文章不多，列出所有文章
        toc_lines.append("### 文章列表")
        toc_lines.append("")
        
        for section_code in sorted(articles_by_section.keys()):
            section = articles_by_section[section_code]
            section_slug = f"#{section_code}-{slugify(section['name'])}"
            toc_lines.append(f"- **{section_code} {section['name']}**")
            
            for idx, art in enumerate(section['articles'], 1):
                title = art['title']
                # 限制标题长度
                display_title = title if len(title) <= 30 else f"{title[:27]}..."
                article_slug = f"#{section_code}-{idx:02d}-{slugify(title)}"
                toc_lines.append(f"  - [{idx:02d}. {display_title}]({article_slug})")
            toc_lines.append("")
    
    toc_lines.append("---")
    toc_lines.append("")
    
    # 开始正文内容
    lines = [
        md_title,
        "",
        f"> 共 {total_sections} 个版块，{total_articles} 篇文章",
        ""
    ]
    
    # 插入目录
    lines.extend(toc_lines)
    
    # 按版块顺序输出（按版块代码排序）
    for section_code in sorted(articles_by_section.keys()):
        section = articles_by_section[section_code]
        # 使用锚点ID
        section_id = f"{section_code}-{slugify(section['name'])}"
        lines.extend([
            f"## {section_code} {section['name']}",
            "",
            f'<a id="{section_id}"></a>',
            ""
        ])
        
        for idx, art in enumerate(section['articles'], 1):
            # 文章标题（带锚点）
            article_id = f"{section_code}-{idx:02d}-{slugify(art['title'])}"
            lines.append(f'<a id="{article_id}"></a>')
            lines.append(f"### {idx}. {art['title']}")
            lines.append("")
            
            # 元信息
            meta_parts = []
            if art.get('author'):
                meta_parts.append(f"**作者**: {art['author']}")
            meta_parts.append(f"**日期**: {art.get('publish_date', date_str)}")
            meta_parts.append(f"**字数**: {art.get('word_count', 0)} 字")
            lines.append(f"> {' | '.join(meta_parts)}")
            lines.append("")
            
            # 正文内容
            content = art.get('content', '').strip()
            if content:
                lines.append(content)
                lines.append("")
            
            # 原文链接
            if art.get('url'):
                lines.append(f"[原文链接]({art['url']})")
            
            lines.extend([
                "",
                "---",
                ""
            ])
    
    return '\n'.join(lines)

def main():
    if len(sys.argv) < 2:
        print("用法: python3 merge_to_md.py YYYY-MM-DD [--output DIR] [--title \"标题\"]")
        sys.exit(1)
    
    date_str = sys.argv[1]
    
    # 验证日期格式
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("错误：日期格式必须是 YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)
    
    # 解析可选参数
    output_dir = "output"
    title_prefix = None
    
    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
        elif arg == '--title' and i + 1 < len(sys.argv):
            title_prefix = sys.argv[i + 1]
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 加载数据
    data = load_data(date_str)
    
    # 生成 Markdown
    md_content = generate_markdown(data, title_prefix)
    
    # 输出文件
    output_file = os.path.join(output_dir, f"dskb_{date_str}.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ 已生成: {output_file}")
    print(f"   包含 {data['total_articles']} 篇文章，{len(md_content)} 字符")

if __name__ == '__main__':
    main()
