#!/usr/bin/env python3
import requests, re

BASE_URL = "https://hzdaily.hangzhou.com.cn"
date_str = "2026-03-29"
section_url = f"{BASE_URL}/dskb/{date_str.replace('-', '/')}/article_list_2_20260329A01.html"

headers = {'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw-Crawler/1.0)'}
resp = requests.get(section_url, headers=headers, timeout=30)
resp.encoding = 'utf-8'
html = resp.text

# 找到包含 article_detail 的部分
start = html.find('article_detail')
if start != -1:
    snippet = html[start-100:start+200]
    print("Snippet around article_detail:")
    print(repr(snippet))

pattern = r'<a href="([^"]+article_detail_[^"]+\.html)[^>]*>([^<]+)</a>'
links = re.findall(pattern, html, re.DOTALL)
print(f"\nPattern result: {len(links)} links")
for url, title in links:
    print(f"  {title.strip()}: {url}")
