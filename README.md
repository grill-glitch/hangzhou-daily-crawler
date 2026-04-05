# 都市快报 RSS 订阅服务 (neo 分支)

## 项目理念

本项目的核心目标是：

1. **版权保护** - 不全文展示，仅提供标题、摘要和原文链接，引导用户访问官方来源
2. **RSS 订阅** - 类似 RSSHub，为都市快报提供稳定可靠的 RSS 订阅服务
3. **日期导航** - 点击任意日期报纸，显示该日期的文章列表页
4. **简洁高效** - 使用 Python FastAPI，无需静态站点构建，快速响应

## 架构设计

- **数据层**：爬虫抓取 → JSON 格式存储（`data/dskb_*.json`）
- **服务层**：FastAPI 提供：
  - 首页 `/` - 所有可用日期列表
  - 每日页面 `/daily/YYYY-MM-DD` - 该日文章列表
  - RSS 订阅 `/rss?date=YYYY-MM-DD` - RSS 2.0 feed
- **视图层**：Jinja2 模板渲染简洁 HTML 页面

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行爬虫抓取数据

```bash
python3 dskb_crawler_v2.py 2026-04-04
```

数据将保存在 `data/dskb_YYYY-MM-DD.json`

### 启动 Web 服务

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

访问：
- 首页：http://localhost:8000/
- 2026-04-04 文章列表：http://localhost:8000/daily/2026-04-04
- RSS 订阅：http://localhost:8000/rss?date=2026-04-04

## 页面示例

**首页**（所有日期）：
```
https://mdaily.hangzhou.com.cn/
    ├── 2026-04-04
    ├── 2026-04-03
    └── ...
```

**每日页面**（类似 mdaily.hangzhou.com.cn 结构）：
```
https://mdaily.hangzhou.com.cn/dskb/2026/04/04/article_list_20260404.html
    - 显示该日所有文章标题、作者、版块、摘要
    - 点击标题跳转至原文链接
```

## API 接口

- `GET /api/dates` - 获取所有有数据的日期列表
- `GET /api/articles/{date_str}` - 获取指定日期的文章数据（JSON）

## 部署建议

- **Vercel / Railway / Heroku** - 一键部署，自动 HTTPS
- **自托管** - 使用 systemd 或 docker-compose
- **GitHub Pages** - 不适用（需要动态服务端渲染）

## 注意事项

- ⚠️ **版权说明**：本服务仅提供元数据和链接，不展示全文，请用户访问官方来源阅读完整内容
- 📅 **数据更新**：建议配合 GitHub Actions 每日自动抓取并部署
- 🔗 **原文链接**：所有文章链接指向 hzdaily.hangzhou.com.cn 官方来源

## 技术栈

- Python 3.11+
- FastAPI - Web 框架
- Jinja2 - 模板引擎
- Feedgen - RSS 生成
- Uvicorn - ASGI 服务器

## License

MIT
