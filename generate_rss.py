#!/usr/bin/env python3
"""
生成 RSS feed (atom.xml)
每个daily newspaper一个条目，指向文章列表页
"""

import json
import os
import sys
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

DATA_DIR = "data"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 静态封面图（例子）
COVER_IMAGE_URL = "https://fsnews.hangzhou.com.cn/group1/M00/7D/02/rB4AiWnSzVGAbsw7AAenFDNIqi8079.jpg?1024*642"

def get_all_data_files():
    """获取所有数据文件"""
    files = []
    if not os.path.exists(DATA_DIR):
        return files
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("dskb_") and filename.endswith(".json"):
            date_str = filename[5:-5]  # 提取 YYYY-MM-DD
            files.append((date_str, filename))
    # 按日期降序排序
    files.sort(reverse=True)
    return files

def generate_rss():
    fg = FeedGenerator()
    fg.title("都市快报 RSS - 每日报纸主页")
    fg.id("https://grill-glitch.github.io/hangzhou-daily-crawler/atom.xml")
    fg.link(href="https://grill-glitch.github.io/hangzhou-daily-crawler/", rel="alternate")
    fg.description("都市快报每日报纸主页链接 RSS 订阅，包含最新一天的报纸入口。")
    fg.language("zh-CN")
    fg.lastBuildDate(datetime.now(timezone.utc))

    files = get_all_data_files()
    if not files:
        print("错误：未找到数据文件", file=sys.stderr)
        sys.exit(1)

    for date_str, filename in files:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        total_articles = data.get("total_articles", 0)
        total_sections = data.get("total_sections", 0)

        # 构造主页链接
        year, month, day = date_str.split('-')
        # 目标链接格式: https://mdaily.hangzhou.com.cn/dskb/YYYY/MM/DD/article_list_YYYYMMDD.html
        main_url = f"https://mdaily.hangzhou.com.cn/dskb/{year}/{month}/{day}/article_list_{year}{month}{day}.html"

        fe = fg.add_entry()
        fe.id(main_url)
        fe.title(f"都市快报 {date_str}")
        fe.link(href=main_url)
        # 发布日期（设置为当天的凌晨 UTC）
        try:
            dt = datetime(int(year), int(month), int(day), tzinfo=timezone.utc)
            fe.published(dt)
        except Exception as e:
            fe.published(datetime.now(timezone.utc))

        # 内容：包含统计信息和封面图
        content_html = f"<p>共 {total_sections} 个版块，{total_articles} 篇文章</p>"
        content_html += f'<img src="{COVER_IMAGE_URL}" alt="都市快报 {date_str} 封面" width="1024" height="642" />'
        fe.content(content_html, type='html')

    output_path = os.path.join(OUTPUT_DIR, "atom.xml")
    fg.atom_file(output_path, pretty=True)
    print(f"RSS feed 已生成: {output_path}")
    print(f"共 {len(files)} 天的数据")

if __name__ == "__main__":
    generate_rss()
