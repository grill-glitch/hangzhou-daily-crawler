#!/usr/bin/env python3
"""Prepare GitHub Pages site from crawled data."""

import json
import os
import sys

def main():
    os.makedirs('_site', exist_ok=True)
    
    # Copy data files
    for pattern in ['dskb_*.json', 'summary_*.txt', 'short_news_*.txt']:
        os.system(f'cp {pattern} _site/ 2>/dev/null || true')
    
    os.chdir('_site')
    
    # Convert markdown files to HTML
    for md_file in [f for f in os.listdir('.') if f.startswith('dskb_') and f.endswith('.md')]:
        html_file = md_file.replace('.md', '.html')
        date_str = md_file[5:-3]  # Extract date from dskb_YYYY-MM-DD.md
        
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Create HTML page with markdown rendering
        page_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>都市快报 {date_str}</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
    .container {{ max-width: 900px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }}
    .back {{ display: inline-block; margin-bottom: 20px; color: #ff6b6b; text-decoration: none; font-weight: bold; }}
    .back:hover {{ text-decoration: underline; }}
    h1 {{ color: #333; border-bottom: 3px solid #ff6b6b; padding-bottom: 10px; }}
    h2 {{ color: #555; margin-top: 2em; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
    h3 {{ color: #666; margin-top: 1.5em; }}
    p {{ line-height: 1.8; margin: 1em 0; }}
    a {{ color: #ff6b6b; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    blockquote {{ border-left: 4px solid #ff6b6b; padding-left: 1em; margin: 1em 0; color: #666; font-style: italic; }}
    code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
    pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    pre code {{ background: transparent; padding: 0; }}
    hr {{ border: none; border-top: 1px solid #eee; margin: 2em 0; }}
  </style>
</head>
<body>
  <div class="container">
    <a href="index.html" class="back">← 返回索引</a>
    <div id="content"></div>
  </div>
  <script>
    document.getElementById('content').innerHTML = marked.parse(`{md_content.replace('`', '\\`')}`);
  </script>
</body>
</html>'''
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(page_html)
        print(f"Created {html_file} from {md_file}")
    
    # Build data.json index
    index = {}
    for filename in os.listdir('.'):
        if filename.startswith('dskb_') and filename.endswith('.json'):
            date = filename[5:-5]
            try:
                with open(filename, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                index[date] = {
                    'total_sections': data.get('total_sections', 0),
                    'total_articles': data.get('total_articles', 0),
                    'total_words': sum(a.get('word_count', 0) for a in data.get('articles', [])),
                    'sections': data.get('sections', [])
                }
                html_file = f'dskb_{date}.html'
                if os.path.exists(html_file):
                    index[date]['html'] = True
                if os.path.exists(f'summary_{date}.txt'):
                    index[date]['summary'] = True
                if os.path.exists(f'short_news_{date}.txt'):
                    index[date]['short_news'] = True
            except Exception as e:
                print(f"Skipping {filename}: {e}")
    
    with open('data.json', 'w', encoding='utf-8') as fp:
        json.dump(index, fp, ensure_ascii=False, indent=2)
    print(f"Created data.json for {len(index)} dates")
    
    # Generate index.html
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>都市快报 Digital Archive</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
    .container { max-width: 960px; margin: auto; }
    h1 { color: #333; border-bottom: 3px solid #ff6b6b; padding-bottom: 10px; }
    .card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 10px 0; }
    .stat { text-align: center; padding: 10px; background: #f8f9fa; border-radius: 4px; }
    .stat-value { font-size: 1.5em; font-weight: bold; }
    .stat-label { font-size: 0.85em; color: #666; }
    .btn { display: inline-block; margin: 5px 5px 5px 0; padding: 10px 16px; background: #ff6b6b; color: white; text-decoration: none; border-radius: 4px; }
    .tags { margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px; }
    .tag { background: #e9ecef; padding: 4px 10px; border-radius: 12px; font-size: 0.85em; }
  </style>
</head>
<body>
  <div class="container">
    <h1>📰 都市快报 Digital Archive</h1>
    <div class="card">
      <p>自动爬取《都市快报》数字报，每日更新。</p>
      <p><strong>最新数据：</strong> ''' + os.popen('date +%Y-%m-%d').read().strip() + '''</p>
    </div>
    <div id="app"></div>
    <script>
      fetch('data.json').then(r => r.json()).then(data => {
        const app = document.getElementById('app');
        Object.keys(data).sort().reverse().forEach(date => {
          const d = data[date];
          const card = document.createElement('div');
          card.className = 'card';
          const tags = d.sections ? d.sections.map(s => 
            `<span class="tag" title="${s.name}">${s.code}</span>`
          ).join('') : '';
          card.innerHTML = `
            <h2>${date}</h2>
            <div class="stats">
              <div class="stat"><div class="stat-value">${d.total_sections}</div><div class="stat-label">版块</div></div>
              <div class="stat"><div class="stat-value">${d.total_articles}</div><div class="stat-label">文章</div></div>
              <div class="stat"><div class="stat-value">${(d.total_words/10000).toFixed(1)}万</div><div class="stat-label">字数</div></div>
            </div>
            <div>
              <a class="btn" href="dskb_${date}.json">📄 原始数据</a>
              ${d.html ? '<a class="btn" href="dskb_'+date+'.html">📖 阅读页面</a>' : ''}
              ${d.summary ? '<a class="btn" href="summary_'+date+'.txt">📋 摘要</a>' : ''}
              ${d.short_news ? '<a class="btn" href="short_news_'+date+'.txt">⚡ 短新闻</a>' : ''}
            </div>
            <div class="tags">${tags}</div>
          `;
          app.appendChild(card);
        });
      }).catch(e => {
        document.getElementById('app').innerHTML = '<p>暂无数据</p>';
        console.error(e);
      });
    </script>
  </div>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as fp:
        fp.write(html)

if __name__ == '__main__':
    main()
