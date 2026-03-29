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

# 保存原始HTML用于调试
with open('list_page_raw.txt', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML length:", len(html))
print("First 2000 chars:")
print(html[:2000])

# 测试正则
section_pattern = r'第([A-Z0-9]+)版：([^\n]+)\n{2,}(.+?)(?=第[A-Z0-9]+版|$)'
sections = re.findall(section_pattern, html, re.DOTALL)
print(f"\nFound {len(sections)} sections")
for sec in sections[:3]:
    print(f"Section: {sec[0]} - {sec[1]}, content length: {len(sec[2])}")
    print("Content preview:", sec[2][:200])
