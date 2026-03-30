#!/usr/bin/env python3
import re

html = '<li><a href="article_detail_2_20260329A0119.html" target="_parent">“华人神探”李昌钰逝世</a></li>'

pattern = r'<a href="([^"]+article_detail_[^"]+\.html)[^>]*>([^<]+)</a>'
m = re.search(pattern, html, re.DOTALL)
if m:
    print("Groups:", m.groups())
else:
    print("No match")

# 分解看看
print("\nDirect findall:")
links = re.findall(pattern, html, re.DOTALL)
print(links)

# 尝试更简单
pattern2 = r'href="([^"]+)"[^>]*>([^<]+)</a>'
links2 = re.findall(pattern2, html, re.DOTALL)
print("Pattern2:", links2)