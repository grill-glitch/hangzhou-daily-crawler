#!/usr/bin/env python3
import requests, re

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

# 查找包含 article_detail 的行
lines = html.split('\n')
for i, line in enumerate(lines):
    if 'article_detail' in line:
        print(f"Line {i}: {repr(line)}")
        break

# 直接搜索整个HTML中的 article_detail
matches = re.findall(r'article_detail_[^\s<>\'"]+\.html', html)
print(f"\nTotal article_detail occurrences: {len(matches)}")
print("First few:", matches[:10])
