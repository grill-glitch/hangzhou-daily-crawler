#!/usr/bin/env python3
"""测试清理函数"""
import re
from html import unescape

def clean_article_content(raw_content):
    """清理文章内容，移除导航和多余空白"""
    # 移除 script, style, nav, header, footer
    content = re.sub(r'<script[^>]*>.*?</script>', '', raw_content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<header[^>]*>.*?</header>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # 替换 br 和 p 标签为换行
    content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)
    content = re.sub(r'</p>', '\n', content, flags=re.IGNORECASE)
    content = re.sub(r'<p[^>]*>', '\n', content, flags=re.IGNORECASE)
    content = re.sub(r'<[^>]+>', ' ', content)
    content = unescape(content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    # 新增：按行清理导航文本和空白
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(keyword in stripped for keyword in ['上一篇', '下一篇>>', '返回主页']):
            continue
        if re.fullmatch(r'[-=_=]{2,}', stripped):
            continue
        cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = '\n'.join(line.rstrip() for line in content.split('\n'))
    return content.strip()

# 测试样本（从 JSON 中提取的一段）
sample = """“华人神探”李昌钰逝世_都市快报 
     
       
     
     
     
     
     
	 
	 
     
     
     
     
     
     
     
     
     
      
     
      
     
    
     
    
     
    
     
    
     
    
     
    
     
    
     
 \r\n \r\n     
         
        \t  
        \t  
         
         
             
\t\t         
\t\t          
                   
             
\t\t\t 
\t\t\t     
\t\t\t    \t 下一篇>> 
\t\t\t    \t  返回主页  
\t\t\t     
\t\t\t     
\t\t\t         我一辈子都在做傻瓜 
\t\t\t    \t “华人神探”李昌钰逝世 
\t\t\t          
\t\t\t        \n\n\r\n\t\t\t        \n2026-03-29\n\r\n\t\t\t     
\t\t\t     
\t\t\t       \t\t　　告别新闻  A07"""

cleaned = clean_article_content(sample)
print("原始长度:", len(sample))
print("清理后长度:", len(cleaned))
print("\n清理后内容:")
print(cleaned)
