#!/usr/bin/env python3
import json

def extract_full_content(date_str):
    with open(f'dskb_{date_str}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 找到"很短很新鲜"版块
    short_news_articles = []
    for art in data['articles']:
        if '很短很新鲜' in art.get('section_name', ''):
            short_news_articles.append(art)
    
    print(f"\n{'='*80}")
    print(f"《都市快报》{date_str} - 很短很新鲜 完整内容")
    print(f"{'='*80}\n")
    
    for i, art in enumerate(short_news_articles, 1):
        print(f"{i}. 【{art['section_code']}】{art['title']}")
        print(f"   作者：{art.get('author', '无')}")
        print(f"   字数：{art.get('word_count', 0)}")
        print(f"\n   {art.get('content', '')[:500].replace(chr(10), ' ')}")
        if len(art.get('content', '')) > 500:
            print("   ...")
        print(f"\n   【原文链接】{art['url']}")
        print(f"\n{'='*80}\n")

# 28日
extract_full_content('2026-03-28')

# 29日
extract_full_content('2026-03-29')
