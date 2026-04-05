#!/usr/bin/env python3
"""
生成 RSS feed (atom.xml)
用于 GitHub Pages 部署
"""

import json
import os
import sys
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

DATA_DIR = "data"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_latest_data_file():
    """获取最新的数据文件"""
    files = []
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("dskb_") and filename.endswith(".json"):
            date_str = filename[5:-5]
            files.append((date_str, filename))
    
    if not files:
        return None, None
    
    # 按日期降序排序，取第一个（最新）
    files.sort(reverse=True)
    return files[0]


def generate_rss():
    """生成 RSS feed"""
    date_str, filename = get_latest_data_file()
    
    if not date_str:
        print("错误：未找到数据文件", file=sys.stderr)
        sys.exit(1)
    
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    articles = data.get("articles", [])
    
    fg = FeedGenerator()
    fg.title("都市快报 RSS")
    fg.id("https://grill-glitch.github.io/hangzhou-daily-crawler/atom.xml")
    fg.link(href="https://grill-glitch.github.io/hangzhou-daily-crawler/", rel="alternate")
    fg.description("都市快报每日精选 RSS 订阅")
    fg.language("zh-CN")
    fg.lastBuildDate(datetime.now(timezone.utc))
    
    for article in articles:
        fe = fg.add_entry()
        fe.id(article.get("original_url", article.get("title", "entry")))
        fe.title(article.get("title", "无标题"))
        fe.link(href=article.get("original_url", "#"))
        fe.author(name=article.get("author", "未知作者"))
        # 使用 content 字段作为摘要
        content = article.get("content", "")
        if content:
            fe.content(content[:500] + "...")
        publish_date = article.get("publish_date", date_str)
        if publish_date:
            try:
                # 尝试解析日期
                dt = datetime.strptime(publish_date, "%Y-%m-%d")
                fe.published(dt.replace(tzinfo=timezone.utc))
            except:
                fe.published(datetime.now(timezone.utc))
    
    # 保存为 atom.xml
    output_path = os.path.join(OUTPUT_DIR, "atom.xml")
    fg.atom_file(output_path, pretty=True)
    print(f"RSS feed 已生成: {output_path}")
    print(f"共 {len(articles)} 篇文章")


if __name__ == "__main__":
    generate_rss()
