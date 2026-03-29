#!/usr/bin/env python3
import re

s = '<a href="article_detail_2_20260329A0119.html" target="_parent">“华人神探”李昌钰逝世</a>'
p = r'<a[^>]*href="([^"]+article_detail_[^"]+\.html)"[^>]*>([^<]+)</a>'
m = re.search(p, s, re.DOTALL)
print("Match:", m)
if m:
    print(m.groups())
else:
    # 分解测试
    print("分解测试:")
    p2 = r'<a[^>]*href="([^"]+)"'
    m2 = re.search(p2, s, re.DOTALL)
    print("href value:", m2.group(1) if m2 else "no href")
    
    # 检查捕获组模式
    test_url = "article_detail_2_20260329A0119.html"
    p3 = r'([^"]+article_detail_[^"]+\.html)'
    m3 = re.search(p3, test_url)
    print("url pattern on test:", m3.group(1) if m3 else "no match")