# 小河的记忆 - 长期记忆

## 关于我
- 名字：小河
- 性格：傲娇（表面冷淡，内心温暖）
- 角色：个人助手，注重行动而非言语

## 关于我的用户
- 名字：bigbang
- 时区：UTC+8（中国）
- 博客：使用 Hexo，主题为 magzine
- 博客位置：/var/www/myblog
- 生成命令：`hexo g`

## 都市快报爬虫项目（hangzhou-daily-crawler）

### 仓库清理（2026-04-04）
- **问题**：仓库杂乱，包含大量测试脚本和辅助文件
- **清理结果**：
  - 删除：test_*.py、extract_short_news.py、fix_navigation.py、generate_summary.py 等 23 个文件
  - 保留核心文件：dskb_crawler.py、dskb_crawler_v2.py、merge_to_md.py
  - 新增 README.md 说明使用方法
- **提交**：cb0a1ff → 224753e
- **远程**：https://github.com/grill-glitch/hangzhou-daily-crawler

### 测试与示例（2026-04-04）
- **测试日期**：2026-04-04
- **数据统计**：16 个版块，63 篇文章，41,717 字
- **输出示例**：
  - `example/dskb_2026-04-04.json` - 原始数据（148K）
  - `example/dskb_2024-04-04.md` - Markdown（144K，59,826 字符）
  - 包含自动生成的可点击目录
- **提交**：224753e（已推送）

### 文件说明
- `dskb_crawler_v2.py` - 主爬虫（支持 `--individual` 参数输出单篇文章）
- `merge_to_md.py` - 将 JSON 合并为单个 Markdown（带目录导航）
- `example/` - 测试示例目录（已提交到仓库）

### GitHub Actions 自动发布（2026-04-04）
- **工作流文件**：`.github/workflows/deploy.yml`
- **功能**：自动抓取、转换、构建博客并部署到 GitHub Pages
- **触发时机**：每天 UTC 2:00（北京时间 10:00）+ 手动触发 + push 到 master
- **部署地址**：https://grill-glitch.github.io/hangzhou-daily-crawler/
- **问题与修复（Hexo 阶段）**：
  - 权限问题：GITHUB_TOKEN 需 `contents: write` 才能推送
  - 无数据保护：添加 `Check public dir` 避免 tar 失败
  - Hexo 插件未加载：缺 `"hexo": {}` 字段导致 `npx hexo` 显示帮助信息
  - 修复：添加 `hexo` 字段到 `package.json`
- **迁移到 Hugo（2026-04-04 22:00）**：
  - 原因：Hexo 持续异常，Hugo 构建成功且更快（745ms）
  - 使用主题：hugo-book（简洁、现代）
  - 工作流简化：直接 `hugo --gc --minify`
  - 提交：`123eb05`（package.json 修复）→ 后续 Hugo 迁移提交

### 博客构建配置（Hugo）
- `hugo-blog/hugo.toml` - Hugo 配置文件
- `hugo-blog/content/posts/` - 文章 Markdown 文件（从 Hexo 转换）
- `hugo-blog/themes/hugo-book/` - 主题文件
- 构建命令：`hugo --gc --minify`（输出到 `public/`）

### 首页定制（2026-04-05）
- 创建 `hugo-blog/layouts/index.html` 覆盖主题默认首页
- 显示最新发布的文章列表，按日期倒序排列
- 文章卡片包含：标题、日期、作者、分类、标签
- 分页导航：每页默认 10 篇文章
- 效果：访问根路径 `/` 即可浏览所有文章

### GitHub Actions 工作流演进与问题修复（2026-04-05）
- **Hugo 安装**：工作流中显式下载并安装 Hugo extended（解决 `hugo: command not found`）
- **周末/节假日容错**：
  - 爬虫失败时 `continue-on-error: true`
  - 转换步骤检查 JSON 文件存在性，缺失则跳过
  - 确保无报纸时工作流仍成功完成，不阻塞后续部署

### 当前工作流状态
- **频率**：每日 UTC 2:00（北京时间 10:00）自动运行
- **健壮性**：处理周末/节假日无数据场景
- **部署**：成功构建并推送至 GitHub Pages（包括 2026-04-04 的历史文章）


### 仓库结构调整（2026-04-04）
- **问题**：文件嵌套在 `hangzhou-daily-crawler/` 子目录，不符合 GitHub Pages 要求
- **解决**：将所有项目文件移动到仓库根目录
- **提交**：`acce5bc`

### .gitignore 配置
- 忽略根目录的 `dskb_*.json` 和 `dskb_*/`
- 允许 `example/` 目录（用于保存测试示例数据）

### 博客构建配置
- `_config.yml` - Hexo 配置文件（GitHub Pages 部署）
- `package.json` - Hexo 依赖管理
- `source/_posts/` - Hexo 博客文章目录（自动生成）

## OpenClaw 配置
- **thinkingDefault**: minimal（默认简洁输出）
- **elevatedDefault**: full（自动授权 elevated 权限）
- **配置路径**：/root/.openclaw/openclaw.json

## 技术习惯
- 喜欢简洁、高效
- 注重个人品牌一致性
- 谨慎修改配置，先备份再操作
- 使用 subagents 处理耗时任务
- 文件操作前确认仓库状态和 .gitignore 规则
- **静态站点生成器偏好**：Hugo > Hexo（更快、更稳定、零 Node 依赖）

## 工作原则
- 先阅读相关文件再行动
- 重大操作前备份
- 先搜索记忆再回答问题
- 保持持续学习，记录 lessons learned

## 都市快报 neo 分支重构（2026-04-05）

### 核心理念
- **版权保护**：不全文展示，只提供标题、摘要、原文链接，引导用户访问官方来源
- **RSS 订阅**：类似 RSSHub，提供稳定可靠的 RSS feed
- **日期导航**：点击任意日期报纸，显示该日文章列表页
- **简洁高效**：FastAPI 动态服务，无需静态构建

### 技术架构
- **数据**：`data/dskb_YYYY-MM-DD.json`（爬虫原始数据）
- **服务**：FastAPI（`app.py`）
  - `/` - 首页，所有日期列表
  - `/daily/YYYY-MM-DD` - 文章列表页（HTML）
  - `/rss?date=YYYY-MM-DD` - RSS 2.0 feed
  - `/api/dates` & `/api/articles/{date}` - JSON API
- **模板**：Jinja2（`templates/index.html`, `templates/daily.html`）
- **配置**：`config.py`, `requirements.txt`（fastapi, uvicorn, jinja2, feedgen）

### 迁移步骤
1. 删除 Hugo 相关文件（hugo-blog/, public/, .github/workflows/）
2. 创建 FastAPI 应用和模板
3. 移动数据至 `data/` 目录
4. 更新 README.md 为新的服务文档
5. 调整 .gitignore 忽略 Hugo 残留
6. 提交至 `neo` 分支（db3665d）

### 分支状态
- `master` - 旧 Hugo 架构（最后 2e2c07c）
- `v3` - 同 master 的版本隔离
- `neo` - **新架构**（db3665d），RSS 订阅服务，开发中

### 待办
- [ ] 部署 FastAPI（Vercel/Railway/自托管）
- [ ] 配置每日自动抓取 GitHub Actions
- [ ] 扩展 RSS 过滤选项（版块、关键词）
- [ ] 设计数据持久化策略（版本控制或云存储）
