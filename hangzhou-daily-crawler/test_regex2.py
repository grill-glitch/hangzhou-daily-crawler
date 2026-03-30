#!/usr/bin/env python3
import re

html = '''<li><a href="article_detail_2_20260329A0119.html" target="_parent">“华人神探”李昌钰逝世</a></li>'''

# 试试最简单的
patterns = [
    r'article_detail_[\w\d]+\.html',
    r'<a[^>]*?href="([^"]+)"[^>]*>([^<]+)</a>',
    r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>',
    r'<a[^>]*href="([^"]+)"[^>]*>([\s\S]*?)</a>',
]

for i, pat in enumerate(patterns):
    links = re.findall(pat, html, re.DOTALL)
    print(f"Pattern {i+1}: {links}")