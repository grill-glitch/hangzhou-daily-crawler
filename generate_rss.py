#!/usr/bin/env python3
"""
生成 RSS feed (atom.xml)
每个daily newspaper一个条目，指向文章列表页
封面图从 A01 版面的 page_view 页面自动爬取
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

import requests

try:
    from feedgen.feed import FeedGenerator
except ImportError:
    print("错误：请安装 feedgen (pip install feedgen)", file=sys.stderr)
    sys.exit(1)

DATA_DIR = "data"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SESSION = requests.Session()
SESSION.headers["User-Agent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def get_all_data_files():
    """获取所有数据文件"""
    files = []
    if not os.path.exists(DATA_DIR):
        return files
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("dskb_") and filename.endswith(".json"):
            date_str = filename[5:-5]  # 提取 YYYY-MM-DD
            files.append((date_str, filename))
    files.sort(reverse=True)
    return files


def fetch_cover_image(data, date_str):
    """从 A01 版面的 page_view 页面提取封面图 URL"""
    sections = data.get("sections", [])
    if not sections:
        print(f"  警告：{date_str} 无版块数据，跳过封面提取", file=sys.stderr)
        return None

    # 找到 A01 版面URL
    page_view_url = None
    for sec in sections:
        code = sec.get("code", "").upper()
        sec_url = sec.get("url", "")
        if code == "A01" and sec_url:
            # 从 page_detail_2_... → page_view_2_...
            page_view_url = sec_url.replace("page_detail", "page_view")
            break

    if not page_view_url:
        print(f"  警告：{date_str} 未找到 A01 版面URL，跳过封面提取", file=sys.stderr)
        return None

    try:
        resp = SESSION.get(page_view_url, timeout=30)
        resp.raise_for_status()
        # 提取 <img src="https://fsnews...">
        match = re.search(r'<img[^>]+src="((?:https?:)?//[^"]+)"', resp.text)
        if match:
            img_url = match.group(1)
            # 转为绝对URL
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            return img_url
        print(f"  警告：{date_str} 未在 page_view 中找到 <img> 标签", file=sys.stderr)
    except Exception as e:
        print(f"  警告：无法获取 {date_str} 封面图: {e}", file=sys.stderr)

    return None


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
        main_url = f"https://mdaily.hangzhou.com.cn/dskb/{year}/{month}/{day}/article_list_{year}{month}{day}.html"

        # 构造 mdaily 链接用于 article_list 页面参考
        mdaily_article_url = main_url

        fe = fg.add_entry()
        fe.id(mdaily_article_url)
        fe.title(f"都市快报 {date_str}")
        fe.link(href=mdaily_article_url, rel="alternate")
        fe.updated(datetime.now(timezone.utc))
        # 发布日期
        try:
            dt = datetime(int(year), int(month), int(day), tzinfo=timezone.utc)
            fe.published(dt)
        except Exception as e:
            fe.published(datetime.now(timezone.utc))

        # 提取封面图
        cover_url = fetch_cover_image(data, date_str)

        # 内容：统计信息 + (可选)封面图 + 文章列表链接
        content_html = f"<p>共 {total_sections} 个版块，{total_articles} 篇文章</p>"
        if cover_url:
            content_html += f'<p><img src="{cover_url}" alt="都市快报 {date_str} 封面" width="1024" height="642" /></p>'
        # 包含 mdaily 链接
        content_html += f'<p><a href="{mdaily_article_url}">查看 {date_str} 报纸</a></p>'
        fe.content(content_html, type='html')

        print(f"  {date_str}: {total_sections} 版块/{total_articles} 篇文章 封面: {'有' if cover_url else '无'}")

    output_path = os.path.join(OUTPUT_DIR, "atom.xml")
    fg.atom_file(output_path, pretty=True)
    print(f"\nRSS feed 已生成: {output_path}")
    print(f"共 {len(files)} 天的数据")

if __name__ == "__main__":
    generate_rss()
