#!/usr/bin/env python3
import json
import re
import sys

def clean_content(content):
    """清理单篇文章内容，保留段落换行"""
    if not content:
        return ""
    lines = content.split('\n')
    cleaned_lines = []
    prev_blank = False  # 追踪前一行是否为空
    
    for line in lines:
        stripped = line.strip()
        
        # 跳过导航行
        if any(keyword in stripped for keyword in ['上一篇', '下一篇>>', '返回主页']):
            continue
        
        # 跳过纯分隔线
        if re.fullmatch(r'[-=_=]{2,}', stripped):
            continue
        
        # 处理空行：只保留一个连续的空白行
        if not stripped:
            if not prev_blank:
                cleaned_lines.append(line)  # 保留第一个空行
                prev_blank = True
            # 如果前一行已经是空行，则跳过（避免连续多个空行）
        else:
            cleaned_lines.append(line)
            prev_blank = False
    
    content = '\n'.join(cleaned_lines)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

# 读取原始JSON数据
with open('dskb_2026-03-29.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 清理每篇文章
for art in data['articles']:
    if 'content' in art:
        old = art['content']
        new = clean_content(old)
        art['content'] = new
        art['word_count'] = len(new)

# 写回文件
with open('dskb_2026-03-29.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'已清理 {len(data["articles"])} 篇文章')
