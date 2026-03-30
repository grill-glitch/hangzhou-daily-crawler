#!/usr/bin/env python3
import json
import re
from html import unescape

def clean_content(html_content):
    """从HTML中提取纯文本"""
    if not html_content:
        return ""
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', ' ', html_content)
    # 替换空白字符
    text = re.sub(r'\s+', ' ', text)
    # HTML实体转义
    text = unescape(text)
    return text.strip()

def show_short_news(date_str):
    with open(f'dskb_{date_str}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    short_news = [art for art in data['articles'] if '很短很新鲜' in art.get('section_name', '')]
    
    print(f"\n{'='*80}")
    print(f"《都市快报》{date_str} - 很短很新鲜 版面内容")
    print(f"{'='*80}\n")
    print(f"共 {len(short_news)} 篇短新闻\n")
    
    for i, art in enumerate(short_news, 1):
        print(f"{i}. {art['title']}")
        print(f"   [{art['section_code']}] {art['word_count']}字")
        # 清理并显示内容
        content = clean_content(art.get('content', ''))
        print(f"   {content}\n")
        print(f"   【原文】{art['url']}")
        print(f"   {'-'*40}\n")

show_short_news('2026-03-28')
show_short_news('2026-03-29')
