#!/usr/bin/env python3
import re

html = '''<li><a href="article_detail_2_20260329A0119.html" target="_parent">“华人神探”李昌钰逝世</a></li>
    		<li><a href="article_detail_2_20260329A0120.html" target="_parent">杭州市区天气预报</a></li>'''

patterns = [
    r'<li>\s*<a[^>]*href=["\']([^"\']+article_detail_[^"\']+\.html)["\'][^>]*>([^<]+)</a>\s*</li>',
    r'<a href="([^"]+article_detail_[^"]+\.html)[^>]*>([^<]+)</a>',
    r'href=["\']([^"\']+article_detail_[^"\']+\.html)["\'][^>]*>([^<]+)<',
]

for i, pat in enumerate(patterns):
    links = re.findall(pat, html, re.DOTALL)
    print(f"Pattern {i+1}: {len(links)} links")
    for url, title in links:
        print(f"  {title.strip()}: {url}")