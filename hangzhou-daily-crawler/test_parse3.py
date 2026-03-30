#!/usr/bin/env python3
import requests, re, urllib.parse

BASE_URL = "https://mdaily.hangzhou.com.cn"
date_str = "2026-03-29"
dt = __import__('datetime').datetime.strptime(date_str, '%Y-%m-%d')
date_no_dash = dt.strftime('%Y%m%d')
date_path = dt.strftime('%Y/%m/%d')
list_url = f"{BASE_URL}/dskb/{date_path}/article_list_{date_no_dash}.html"

headers = {'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw-Crawler/1.0)'}
resp = requests.get(list_url, headers=headers, timeout=30)
resp.encoding = 'utf-8'
html = resp.text

# 测试不同正则
patterns = [
    r'<a[^>]*href=["\']([^"\']+article_detail_[^"\']+\.html)["\'][^>]*>([^<]+)</a>',
    r'<a[^>]*?href=["\']?([^"\'<>]+article_detail_[^"\'<>]+\.html)["\']?[^>]*>([^<]+)<',
    r'href=["\']([^"\']+article_detail_[^"\']+\.html)["\'][^>]*>([^<]+)<',
]

for i, pat in enumerate(patterns):
    links = re.findall(pat, html)
    print(f"Pattern {i+1}: {len(links)} links")
    for url, title in links[:5]:
        print(f"  {title.strip()}: {url}")
    print()

# 检查href中的特殊字符处理
print("Sample of HTML around first article link:")
first_article_pos = html.find('article_detail_2_20260329')
if first_article_pos != -1:
    snippet = html[first_article_pos-100:first_article_pos+150]
    print(snippet)
