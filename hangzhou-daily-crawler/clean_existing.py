#!/usr/bin/env python3
"""清理现有 JSON 文件中的导航文本"""
import json
import re
from html import unescape

def clean_content(content):
    """清理单篇文章内容"""
    if not content:
        return ""
    # 移除常见导航关键词及其所在行
    lines = content.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(kw in stripped for kw in ['上一篇', '下一篇>>', '返回主页']):
            continue
        if re.fullmatch(r'[-=_=]{2,}', stripped):
            continue
        cleaned.append(line)
    content = '\n'.join(cleaned)
    # 合并连续空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = '\n'.join(l.rstrip() for l in content.split('\n'))
    return content.strip()

# 处理今天的文件（可能已经抓取过）
date_str = '2026-03-29'
filename = f'dskb_{date_str}.json'

with open(filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
for art in data['articles']:
    old = art.get('content', '')
    new = clean_content(old)
    if len(old) != len(new):
        count += 1
    art['content'] = new
    # 更新字数统计
    art['word_count'] = len(new)

# 写回文件
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'已清理 {count} 篇文章的内容，保存到 {filename}')

# 顺便也清理昨天的文件
import os
yesterday = '2026-03-28'
yesterday_file = f'dskb_{yesterday}.json'
if os.path.exists(yesterday_file):
    with open(yesterday_file, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    count2 = 0
    for art in data2['articles']:
        old = art.get('content', '')
        new = clean_content(old)
        if len(old) != len(new):
            count2 += 1
        art['content'] = new
        art['word_count'] = len(new)
    with open(yesterday_file, 'w', encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=2)
    print(f'已清理 {count2} 篇文章的内容，保存到 {yesterday_file}')
