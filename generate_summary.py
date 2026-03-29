#!/usr/bin/env python3
"""
都市快报内容摘要生成器
"""

import json
import sys
from datetime import datetime
from collections import defaultdict

def load_data(date_str):
    """加载指定日期的数据"""
    filename = f"dskb_{date_str}.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found", file=sys.stderr)
        return None

def generate_summary(data):
    """生成内容摘要"""
    date_str = data['date']
    total_sections = data['total_sections']
    total_articles = data['total_articles']
    
    # 按版块分组
    sections_dict = {s['code']: s for s in data['sections']}
    articles_by_section = defaultdict(list)
    for art in data['articles']:
        articles_by_section[art['section_code']].append(art)
    
    print("=" * 80)
    print(f"《都市快报》{date_str} 内容摘要")
    print("=" * 80)
    
    print(f"\n📊 总体统计:")
    print(f"  版块数: {total_sections}")
    print(f"  文章数: {total_articles}")
    total_words = sum(art.get('word_count', 0) for art in data['articles'])
    print(f"  总字数: {total_words:,}")
    
    print(f"\n📰 版块分布:")
    for code in sorted(articles_by_section.keys()):
        count = len(articles_by_section[code])
        section_name = sections_dict.get(code, {}).get('name', code)
        print(f"  {code} ({section_name}): {count}篇")
    
    # 热点新闻（按字数或位置）
    print(f"\n🔥 重点新闻 (A01-A08版):")
    
    # A01 头版
    if 'A01' in articles_by_section:
        print(f"\n【头版 A01】{sections_dict.get('A01', {}).get('name', '都市快报')}")
        for art in articles_by_section['A01'][:3]:
            print(f"  • {art['title']}")
    
    # A02 中国新闻
    if 'A02' in articles_by_section:
        print(f"\n【中国新闻 A02】")
        for art in articles_by_section['A02'][:5]:
            print(f"  • {art['title']}")
    
    # A03 杭州新闻
    if 'A03' in articles_by_section:
        print(f"\n【杭州新闻 A03】")
        for art in articles_by_section['A03'][:4]:
            print(f"  • {art['title']}")
    
    # A06 很短很新鲜
    if 'A06' in articles_by_section:
        print(f"\n【很短很新鲜 A06】")
        for art in articles_by_section['A06'][:8]:
            print(f"  • {art['title']}")
    
    # 本地新闻 (A04, A05)
    if 'A04' in articles_by_section:
        print(f"\n【热线新闻 A04】")
        for art in articles_by_section['A04'][:3]:
            print(f"  • {art['title']}")
    
    if 'A05' in articles_by_section:
        print(f"\n【浙江新闻 A05】")
        for art in articles_by_section['A05'][:3]:
            print(f"  • {art['title']}")
    
    # B版精彩内容
    if any(code.startswith('B') for code in articles_by_section):
        print(f"\n🌟 专刊/副刊 (B版):")
        for code in sorted([c for c in articles_by_section.keys() if c.startswith('B')]):
            section_name = sections_dict.get(code, {}).get('name', code)
            print(f"\n【{section_name} {code}】")
            for art in articles_by_section[code][:2]:
                print(f"  • {art['title']}")
    
    # 字数最多的文章
    print(f"\n📖 长文章 Top 5:")
    long_articles = sorted(data['articles'], key=lambda x: x.get('word_count', 0), reverse=True)[:5]
    for i, art in enumerate(long_articles, 1):
        print(f"  {i}. {art['title']} ({art['word_count']:,}字) [{art['section_code']}]")
    
    # 作者统计
    authors = defaultdict(int)
    for art in data['articles']:
        if art.get('author'):
            authors[art['author']] += 1
    
    if authors:
        print(f"\n✍️  活跃作者 Top 5:")
        for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {author}: {count}篇")
    
    print("\n" + "=" * 80)
    print(f"数据来源：都市快报 {date_str}")
    print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

def main():
    if len(sys.argv) < 2:
        print("用法: python3 generate_summary.py YYYY-MM-DD")
        sys.exit(1)
    
    date_str = sys.argv[1]
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("错误：日期格式必须是 YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)
    
    data = load_data(date_str)
    if data:
        generate_summary(data)

if __name__ == '__main__':
    main()
