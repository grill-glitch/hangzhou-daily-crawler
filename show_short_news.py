#!/usr/bin/env python3
import json

def show_short_news(date_str):
    with open(f'dskb_{date_str}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 筛选"很短很新鲜"版块
    short_news = [art for art in data['articles'] if '很短很新鲜' in art.get('section_name', '')]
    
    print(f"\n{'='*80}")
    print(f"《都市快报》{date_str} - 很短很新鲜 版面内容")
    print(f"{'='*80}\n")
    print(f"共 {len(short_news)} 篇\n")
    
    for i, art in enumerate(short_news, 1):
        print(f"{i}. {art['title']}")
        print(f"   【{art['section_code']}】{art['section_name']} | {art['word_count']}字")
        # 清理内容：去掉HTML whitespace
        content = art.get('content', '').replace('\r', '').replace('\t', '').strip()
        # 取前300字预览
        if len(content) > 300:
            preview = content[:300] + "..."
        else:
            preview = content
        print(f"   {preview}\n")
        print(f"   ---\n")

# 显示两天
show_short_news('2026-03-28')
show_short_news('2026-03-29')
