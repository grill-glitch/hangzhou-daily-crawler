# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Web Search

### Primary: Tavily Search
- **Skill:** `openclaw-tavily-search` (installed, configured with TAVILY_API_KEY in `~/.openclaw/.env`)
- **Usage:** Use `web_search` tool - it will automatically use Tavily instead of Brave.
- **Alternative:** Run the script directly:
  ```bash
  python3 skills/openclaw-tavily-search/scripts/tavily_search.py --query "..." --max-results 5 --format md
  ```
- **Note:** Keep `max-results` small (3–5) to reduce token usage.

### Secondary: Multi Search Engine (no API keys)
- **Skill:** `multi-search-engine` (installed)
- **Description:** 17 search engines (8 CN + 9 Global) via direct URL construction. No API keys required.
- **Usage:** Use `web_fetch` with constructed URLs:
  ```bash
  # Domestic engines
  web_fetch({"url": "https://www.baidu.com/s?wd={keyword}"})
  web_fetch({"url": "https://cn.bing.com/search?q={keyword}&ensearch=0"}) # Bing CN
  web_fetch({"url": "https://cn.bing.com/search?q={keyword}&ensearch=1"}) # Bing INT
  web_fetch({"url": "https://www.so.com/s?q={keyword}"}) # 360
  web_fetch({"url": "https://sogou.com/web?query={keyword}"}) # Sogou
  
  # International engines
  web_fetch({"url": "https://www.google.com/search?q={keyword}"})
  web_fetch({"url": "https://duckduckgo.com/html/?q={keyword}"})
  web_fetch({"url": "https://search.brave.com/search?q={keyword}"})
  ```
- **Advanced operators:** `site:`, `filetype:`, `""` (exact), `-` (exclude), `OR`
- **Time filters:** `tbs=qdr:h/d/w/m/y` (hour/day/week/month/year)
- **DuckDuckGo bangs:** `!gh` (GitHub), `!so` (Stack Overflow), `!w` (Wikipedia), etc.
- **WolframAlpha:** `https://www.wolframalpha.com/input?i={query}` for knowledge/math/conversions
- **See also:** `skills/multi-search-engine/references/` for detailed guides.

Add whatever helps you do your job. This is your cheat sheet.

---

## Self-Improvement

- **Skill:** `self-improving-agent` (installed)
- **Purpose:** Log learnings, errors, and corrections to enable continuous improvement. When something fails or you discover a better approach, record it.
- **Logs:** Stored in `.learnings/`:
  - `LEARNINGS.md` - Corrections, knowledge gaps, best practices
  - `ERRORS.md` - Command failures, exceptions
  - `FEATURE_REQUESTS.md` - Requested capabilities
- **When to use:**
  - Command/operation fails unexpectedly
  - User corrects you
  - You discover your knowledge is outdated
  - You find a better approach for recurring tasks
  - An external API/tool fails
- **Promotion:** Valuable learnings can be promoted to `SOUL.md` (behavior), `AGENTS.md` (workflow), or `TOOLS.md` (tool gotchas).
- **Format:** Use structured entries with ID, priority, area, summary, details, suggested action, and metadata.
- **Review:** Check `.learnings/` before major tasks and periodically to resolve/promote entries.

## Blog Configuration

- **Skill:** `blog-config-tips` (custom, created 2026-03-21)
- **Purpose:** Hexo 博客配置技巧、性能优化、主题定制、Nginx 配置、SEO、评论系统、图片优化、安全加固
- **Main script:** `skills/blog-config-tips/blog-config-tips.py`
- **Usage:**
  ```bash
  BLOG_DIR=/var/www/myblog python3 skills/blog-config-tips/blog-config-tips.py check_performance
  BLOG_DIR=/var/www/myblog python3 skills/blog-config-tips/blog-config-tips.py nginx_optimize
  BLOG_DIR=/var/www/myblog python3 skills/blog-config-tips/blog-config-tips.py backup
  ```
- **Triggers (natural language):**
  - "博客配置技巧"
  - "Hexo 优化"
  - "博客性能"
  - "Nginx 配置"
  - "主题定制"
  - "SEO 设置"
  - "评论系统"
  - "图片优化"
  - "博客安全"
- **Checklist:** Review before major deployment, after theme changes, or when performance degrades.
- **Reference docs:** `skills/blog-config-tips/references/CONFIG_TIPS.md`

## Internet Archive

- **Skill:** `internet-archive` (custom, created 2026-03-29)
- **Purpose:** 与 Internet Archive (archive.org) 交互 - 搜索、下载、上传和管理存档内容
- **Main script:** `skills/internet-archive/internet-archive.py`
- **Usage:**
  ```bash
  # 检查工具状态
  python3 skills/internet-archive/internet-archive.py check
  
  # 搜索存档
  python3 skills/internet-archive/internet-archive.py search "collection:nasa mediatype:image" --itemlist
  
  # 下载项目
  python3 skills/internet-archive/internet-archive.py download <identifier> --glob="*.pdf"
  
  # 上传文件（需要认证）
  python3 skills/internet-archive/internet-archive.py upload <id> file.txt \
    --metadata="mediatype:texts" \
    --metadata="title:My File"
  
  # 查看/修改元数据
  python3 skills/internet-archive/internet-archive.py metadata <identifier> --formats
  
  # 列出文件
  python3 skills/internet-archive/internet-archive.py list <identifier> --location
  ```
- **Triggers (natural language):**
  - "搜索 Internet Archive"
  - "从 archive.org 下载"
  - "上传到 Internet Archive"
  - "管理存档元数据"
  - "检查 ia 工具"
  - "安装 internetarchive 包"
  - "archive.org 相关"
- **Intents:**
  - `check` - 检查 ia CLI 是否安装和配置
  - `install` - 自动安装 internetarchive 包
  - `search` - 搜索存档目录（支持 Lucene 语法、全文搜索）
  - `download` - 下载项目文件（支持通配符、格式过滤）
  - `upload` - 上传文件（需认证）
  - `metadata` - 查看/修改元数据
  - `list` - 列出项目文件
  - `archive` - **查找 Wayback Machine 存档**（需 URL）
    - 当网站抓取失败时可用作回退
    - 自动显示存档时间戳
    - 支持 `--fetch` 直接获取存档内容
    - 支持 `--from`/`--to` 年份过滤，`--limit` 数量限制
- **Configuration:** 首次使用前需要：
  1. 注册 Internet Archive 账户：https://archive.org/account/signup
  2. 获取 S3 API 密钥：https://archive.org/account/s3.php
  3. 运行 `ia configure` 配置（或在 `~/.config/ia.ini` 中手动配置）
- **Notes:**
  - 下载公开内容无需认证
  - 上传和元数据修改需要有效的 API 密钥
  - 项目标识符一旦创建不可更改
  - 使用 `test_collection` 测试上传（30 天后自动删除）
  - 遵循 Internet Archive 使用条款
- **Fallback usage:** 当 `web_fetch` 遇到 404/5xx 等错误时，可调用此技能的 `archive` intent 自动尝试获取 Wayback Machine 存档。输出中会突出显示存档时间。
- **Reference docs:** `skills/internet-archive/references/QUICK_REFERENCE.md`

## Hangzhou Daily Crawler (都市快报抓取工具)

- **Location:** `hangzhou-daily-crawler/`
- **Purpose:** 抓取杭州都市快报数字版每日新闻内容，生成结构化 JSON 数据
- **Main script:** `hangzhou-daily-crawler/dskb_crawler_v2.py`
- **Usage:**
  ```bash
  # 抓取指定日期数据
  cd hangzhou-daily-crawler
  python3 dskb_crawler_v2.py 2026-03-29
  
  # 可选：保存单篇文章文件（默认不保存）
  python3 dskb_crawler_v2.py 2026-03-29 --individual
  ```
- **Output:**
  - `dskb_YYYY-MM-DD.json` - 所有文章结构化数据（包含 title, author, publish_date, content, word_count 等字段）
  - `dskb_YYYY-MM-DD/` - 单篇文章 JSON 文件（可选，使用 `--individual` 生成）
- **Recent fix (2026-03-30):** 
  - 修复了 `content` 字段中混入导航文本的问题
  - 新增清理逻辑：自动移除 "上一篇", "下一篇>>", "返回主页" 等导航链接
  - 压缩连续空白行，清理行尾空格
  - 辅助脚本 `fix_navigation.py` 用于清理已有 JSON 文件
  - **应用修复**：运行 `python3 dskb_crawler_v2.py 2026-03-29` 重新抓取，或运行 `python3 fix_navigation.py` 清理现有数据
- **Notes:**
  - 请求间隔 1 秒，避免对服务器造成压力
  - 数据来源：hzdaily.hangzhou.com.cn
  - 结构基于 page_list + iframe (article_list) 的双层结构
- **Related scripts:**
  - `extract_short_news.py` - 提取"很短很新鲜"版面内容
  - `show_short_news.py` / `show_short_news_clean.py` / `show_short_news_full.py` - 显示短新闻的不同格式
  - `generate_summary.py` - 生成摘要
  - `merge_to_md.py` - **将某天所有文章合并为单个 Markdown 文件（带可点击目录）**
    ```bash
    cd hangzhou-daily-crawler
    # 先清理数据（可选但推荐）
    python3 fix_navigation.py
    
    # 生成 Markdown（带自动目录）
    python3 merge_to_md.py 2026-03-29
    python3 merge_to_md.py 2026-03-29 --output docs --title "都市快报精选"
    ```
    输出格式：
      - `output/dskb_YYYY-MM-DD.md` (默认输出到 `output/` 目录)
      - 按版块分组，包含标题、作者、日期、字数、正文、原文链接
      - 正文保留段落换行，已移除导航文本和多余空白
      - **自动生成可点击目录**：
        - 版块列表（含文章数统计）
        - 详细文章列表（200篇以内显示全部，自动截断长标题）
        - 每个版块和文章都有唯一锚点，支持快速跳转
      - 目录使用 `slugify` 生成锚点，兼容中文、英文、数字



