#!/usr/bin/env python3
import requests, re

BASE_URL = "https://hzdaily.hangzhou.com.cn"
date_str = "2026-03-29"
section_url = f"{BASE_URL}/dskb/{date_str.replace('-', '/')}/article_list_2_20260329A01.html"

headers = {'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw-Crawler/1.0)'}
resp = requests.get(section_url, headers=headers, timeout=30)
resp.encoding = 'utf-8'
html = resp.text

print("HTML length:", len(html))

# 测试不同的pattern
patterns = [
    r'<a href="([^"]+article_detail_[^"]+\.html)"[^>]*>([^<]+)</a>',
    r'<a[^>]*href="([^"]+article_detail_[^"]+\.html)"[^>]*>([^<]+)</a>',
    r'href="([^"]+article_detail_[^"]+\.html)"[^>]*>([^<]+)</a>',
    r'<a[^>]*?href="([^"]+)"[^>]*>([^<]+)</a>',
]

for i, pat in enumerate(patterns):
    links = re.findall(pat, html, re.DOTALL)
    print(f"\nPattern {i+1}: {len(links)} links")
    for url, title in links[:3]:
        print(f"  {title.strip()}: {url}")