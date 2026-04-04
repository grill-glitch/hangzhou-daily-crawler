# 杭州都市快报爬虫

抓取杭州都市快报数字版每日新闻内容，生成结构化 JSON 和 Markdown 数据。

## 文件说明

- `dskb_crawler.py` - 原始版本爬虫
- `dskb_crawler_v2.py` - 主版本爬虫（推荐使用）
- `merge_to_md.py` - 将某天所有文章合并为单个 Markdown 文件（带可点击目录）

## 使用方法

### 抓取指定日期数据

```bash
cd hangzhou-daily-crawler
python3 dskb_crawler_v2.py 2026-03-29
```

输出：
- `dskb_YYYY-MM-DD.json` - 所有文章的结构化数据
- `dskb_YYYY-MM-DD/` 目录 - 单篇文章 JSON 文件（可选）

### 生成 Markdown（带自动目录）

```bash
python3 merge_to_md.py 2026-03-29 [--output docs] [--title "标题"]
```

输出：
- `output/dskb_YYYY-MM-DD.md` - 合并后的 Markdown 文件
- 按版块分组，包含标题、作者、字数、正文和原文链接
- 自动生成可点击目录（版块列表 + 详细文章列表）

### 清理已有数据中的导航文本

```bash
python3 fix_navigation.py
```

## 输出格式

JSON 数据结构包含以下字段：
- `title`: 文章标题
- `author`: 作者
- `publish_date`: 发布日期
- `content`: 正文内容（已清理导航文本）
- `word_count`: 字数统计
- `section`: 所属版块
- `original_url`: 原文链接

## 依赖

- Python 3.x
- requests

## 注意事项

- 请求间隔 1 秒，避免对服务器造成压力
- 数据来源：hzdaily.hangzhou.com.cn
- 请遵守robots.txt并尊重版权

## License

MIT
