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

# 找 <div class="news-list"> 或类似容器
list_match = re.search(r'<div[^>]*class=["\'][^"\']*news-list[^"\']*["\'][^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
if not list_match:
    # 尝试其他容器
    list_match = re.search(r'<div[^>]*id=["\']news-list["\'][^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
if not list_match:
    # 任何包含大量 ul 或 li 的 div
    list_match = re.search(r'<div[^>]*>.*?<ul>.*?</ul>.*?</div>', html, re.DOTALL | re.IGNORECASE)

if list_match:
    content = list_match.group(1)
    print("Found list container, length:", len(content))
    # 提取所有链接
    link_pattern = r'<a[^>]*href=["\']([^"\']+\.html)["\'][^>]*>([^<]+)</a>'
    links = re.findall(link_pattern, content)
    print(f"Found {len(links)} links")
    for url, title in links[:10]:
        print(f"- {title.strip()}: {url}")
else:
    print("No list container found")
    # 直接在整个页面中搜索文章链接
    link_pattern = r'<a[^>]*href=["\']([^"\']+\.html)["\'][^>]*>([^<]+)</a>'
    links = re.findall(link_pattern, html)
    print(f"Direct search found {len(links)} links")
    for url, title in links[:10]:
        print(f"- {title.strip()}: {url}")
