"""
都市快报 RSS 订阅服务
FastAPI 主应用
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RSSResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, date
import json
import os
from typing import List, Dict
import feedgen
from feedgen.feed import FeedGenerator
from config import DATA_DIR

app = FastAPI(title="都市快报 RSS 订阅服务", version="1.0.0")
templates = Jinja2Templates(directory="templates")


def get_available_dates() -> List[str]:
    """获取所有有数据的日期"""
    dates = []
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("dskb_") and filename.endswith(".json"):
            date_str = filename[5:-5]  # 提取日期部分
            dates.append(date_str)
    dates.sort(reverse=True)
    return dates


def load_data_for_date(date_str: str) -> Dict:
    """加载指定日期的数据"""
    json_file = os.path.join(DATA_DIR, f"dskb_{date_str}.json")
    if not os.path.exists(json_file):
        raise HTTPException(status_code=404, detail=f"未找到 {date_str} 的数据")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """首页 - 显示所有可用日期"""
    dates = get_available_dates()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "dates": dates,
            "title": "都市快报 RSS 订阅服务"
        }
    )


@app.get("/daily/{date_str}", response_class=HTMLResponse)
async def daily_page(request: Request, date_str: str):
    """指定日期的文章列表页"""
    try:
        data = load_data_for_date(date_str)
    except HTTPException:
        # 如果该日期没有数据，返回空白页
        articles = []
    else:
        articles = data.get("articles", [])
    
    return templates.TemplateResponse(
        "daily.html",
        {
            "request": request,
            "date": date_str,
            "articles": articles,
            "title": f"都市快报 {date_str} 文章列表"
        }
    )


@app.get("/rss")
async def rss_feed(date_str: str = None):
    """RSS feed"""
    fg = FeedGenerator()
    fg.title("都市快报 RSS")
    fg.link(href="https://rss.daily.hangzhou.com.cn", rel="alternate")
    fg.description("都市快报每日精选 RSS 订阅")
    fg.language("zh-CN")
    
    if date_str:
        # 特定日期的 feed
        try:
            data = load_data_for_date(date_str)
        except HTTPException:
            raise HTTPException(status_code=404, detail=f"未找到 {date_str} 的数据")
        fg.title(f"都市快报 {date_str} RSS")
        fg.link(href=f"https://rss.daily.hangzhou.com.cn/rss?date={date_str}", rel="self")
        articles = data.get("articles", [])
    else:
        # 最新日期的 feed
        dates = get_available_dates()
        if not dates:
            raise HTTPException(status_code=404, detail="暂无数据")
        latest_date = dates[0]
        data = load_data_for_date(latest_date)
        fg.title(f"都市快报 最新文章 RSS")
        fg.link(href="https://rss.daily.hangzhou.com.cn/rss", rel="self")
        articles = data.get("articles", [])
    
    for article in articles:
        fe = fg.add_entry()
        fe.title(article.get("title", "无标题"))
        fe.link(href=article.get("original_url", "#"))
        fe.author(author=article.get("author", "未知作者"))
        # 使用 content 字段作为摘要
        content = article.get("content", "")
        if content:
            fe.content(content[:500] + "...")
        fe.pubDate(article.get("publish_date", datetime.now().strftime("%Y-%m-%d")))
    
    return RSSResponse(fg.rss_str(pretty=True))


@app.get("/api/dates")
async def api_dates():
    """API: 获取所有日期"""
    return {"dates": get_available_dates()}


@app.get("/api/articles/{date_str}")
async def api_articles(date_str: str):
    """API: 获取指定日期的文章"""
    try:
        data = load_data_for_date(date_str)
    except HTTPException:
        raise HTTPException(status_code=404, detail=f"未找到 {date_str} 的数据")
    
    # 精简返回，适合 API 使用
    articles = []
    for a in data.get("articles", []):
        articles.append({
            "title": a.get("title"),
            "author": a.get("author"),
            "section": a.get("section_name"),
            "original_url": a.get("original_url"),
            "word_count": a.get("word_count"),
            "publish_date": a.get("publish_date")
        })
    
    return {
        "date": date_str,
        "total": len(articles),
        "articles": articles
    }
