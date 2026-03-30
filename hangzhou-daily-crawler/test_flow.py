#!/usr/bin/env python3
import requests, re
from datetime import datetime

BASE_URL = "https://hzdaily.hangzhou.com.cn"
date_str = "2026-03-29"

# 模拟 get_page_sections
date_no_dash = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y%m%d')
list_url = f"{BASE_URL}/dskb/{date_str.replace('-', '/')}/page_list_{date_no_dash}.html"
print("List URL:", list_url)

headers = {'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw-Crawler/1.0)'}
resp = requests.get(list_url, headers=headers, timeout=30)
resp.encoding = 'utf-8'
html = resp.text

# 提取版块
pattern = r'<a[^>]*href=["\']([^"\']+\.html)["\'][^>]*title=["\'][^"\']+["\'][^>]*>第([A-Z0-9]+)版：([^<]+)</a>'
links = re.findall(pattern, html, re.DOTALL)
print(f"Found {len(links)} sections")

if links:
    href, code, name = links[0]
    print(f"First section: {code} - {name}, href: {href}")
    
    # 构造 article_list URL
    section_url = f"{BASE_URL}/dskb/{date_str.replace('-', '/')}/{href}"
    print(f"Section URL (page_detail): {section_url}")
    
    # 提取 A01 -> article_list_2_20260329A01.html
    # 实际上应该是 page_detail_2_20260329A01.html
    # 我们希望 article_list_2_20260329A01.html
    
    article_list_url = section_url.replace('page_detail_2_', 'article_list_2_')
    print("Article list URL:", article_list_url)
    
    # 抓取 article_list
    resp2 = requests.get(article_list_url, headers=headers, timeout=30)
    resp2.encoding = 'utf-8'
    html2 = resp2.text
    print("HTML2 length:", len(html2))
    
    # 提取文章
    link_pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
    all_links = re.findall(link_pattern, html2, re.DOTALL)
    print(f"Total <a> links: {len(all_links)}")
    
    article_links = [(url, title) for url, title in all_links if url.startswith('article_detail_')]
    print(f"Article links: {len(article_links)}")
    for url, title in article_links[:3]:
        print(f"  {title.strip()}: {url}")