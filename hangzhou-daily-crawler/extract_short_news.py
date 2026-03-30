#!/usr/bin/env python3
"""
提取"很短很新鲜"版面内容
"""

import json
import sys
from datetime import datetime

def load_data(date_str):
    filename = f"dskb_{date_str}.json"
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_short_news(data):
    """提取很短很新鲜版面的文章"""
    articles = []
    
    # A06 和 A07 都是"很短很新鲜"（不同日期版块名可能重复）
    for section in data['sections']:
        if '很短很新鲜' in section['name']:
            code = section['code']
            for art in data['articles']:
                if art['section_code'] == code:
                    articles.append({
                        'title': art['title'],
                        'content': art.get('content', ''),
                        'word_count': art.get('word_count', 0),
                        'section': f"{code} ({section['name']})"
                    })
    
    return articles

def generate_short_news_report(date_str):
    data = load_data(date_str)
    short_news = extract_short_news(data)
    
    print("=" * 80)
    print(f"《都市快报》{date_str} - 很短很新鲜 版面内容汇总")
    print("=" * 80)
    print(f"\n共 {len(short_news)} 篇短新闻\n")
    
    for i, news in enumerate(short_news, 1):
        print(f"{i}. 【{news['section']}】{news['title']}")
        print(f"   ({news['word_count']}字)")
        # 提取前200字预览
        preview = news['content'][:200].replace('\n', ' ').strip()
        if len(news['content']) > 200:
            preview += "..."
        print(f"   {preview}\n")
    
    print("=" * 80)

def main():
    if len(sys.argv) < 2:
        print("用法: python3 extract_short_news.py YYYY-MM-DD")
        sys.exit(1)
    
    date_str = sys.argv[1]
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("错误：日期格式必须是 YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)
    
    generate_short_news_report(date_str)

if __name__ == '__main__':
    main()
