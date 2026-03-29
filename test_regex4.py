#!/usr/bin/env python3
import re

s = '<a href="article_detail_2_20260329A0119.html" target="_parent">“华人神探”李昌钰逝世</a>'

# 我的原始pattern
p1 = r'<a href="([^"]+article_detail_[^"]+\.html)[^>]*>([^<]+)</a>'
m1 = re.search(p1, s, re.DOTALL)
print("Pattern 1:", m1.group(1,2) if m1 else "No match")

# 简化pattern：提取所有href="..." 和 >...<
p2 = r'href="([^"]+)"[^>]*>([^<]+)</a>'
m2 = re.search(p2, s, re.DOTALL)
print("Pattern 2:", m2.group(1,2) if m2 else "No match")

# 再简化：直接匹配 article_detail
p3 = r'"(article_detail_[^"]+\.html)"[^>]*>([^<]+)</a>'
m3 = re.search(p3, s, re.DOTALL)
print("Pattern 3:", m3.group(1,2) if m3 else "No match")

# 试试 findall
print("\nfindall tests:")
print("p1:", re.findall(p1, s, re.DOTALL))
print("p2:", re.findall(p2, s, re.DOTALL))
print("p3:", re.findall(p3, s, re.DOTALL))