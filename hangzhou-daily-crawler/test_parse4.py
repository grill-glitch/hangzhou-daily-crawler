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

# 更宽松的正则
link_pattern = r'href=["\']([^"\']+article_detail_[^"\']+\.html)["\'][^>]*>([^<]+)<'
links = re.findall(link_pattern, html, re.DOTALL)
print(f"Found {len(links)} links")
for url, title in links[:10]:
    print(f"  {title.strip()}: {url}")
