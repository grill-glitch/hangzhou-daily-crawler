# 都市快报数字报爬虫

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

专门针对《都市快报》数字报（hzdaily.hangzhou.com.cn）的网络爬虫，支持完整抓取指定日期的所有版块内容，包括文章详情、作者、字数等元数据。

## ✨ 特性

- 🎯 **完整抓取**：自动发现所有版块（A/B版共16个）
- 🔄 **智能解析**：基于iframe的版块结构，稳定可靠
- 📊 **数据丰富**：标题、作者、发布日期、正文、字数统计
- 💾 **多种输出**：JSON汇总 + 单文件存储（可选）
- 🚀 **极简使用**：单命令完成抓取

## 📦 项目结构

```
hangzhou-daily-crawler/
├── dskb_crawler_v2.py   # 主爬虫脚本
├── generate_summary.py  # 内容摘要生成器
├── extract_short_news.py # 提取"很短很新鲜"版面
├── show_short_news*.py  # 短新闻展示工具
├── dskb_YYYY-MM-DD.json # 抓取结果（示例）
└── README.md
```

## 🚀 快速开始

### 安装依赖

```bash
pip install requests
```

### 基本使用

```bash
# 抓取指定日期（只生成汇总JSON）
python3 dskb_crawler_v2.py 2026-03-28

# 抓取并保存单篇文章
python3 dskb_crawler_v2.py 2026-03-28 --individual

# 指定输出目录
python3 dskb_crawler_v2.py 2026-03-28 --output-dir ./output
```

## 📋 输出格式

### 汇总 JSON (`dskb_YYYY-MM-DD.json`)

```json
{
  "date": "2026-03-28",
  "total_sections": 16,
  "total_articles": 59,
  "total_words": 77687,
  "sections": [
    {
      "code": "A01",
      "name": "都市快报",
      "url": "https://hzdaily.hangzhou.com.cn/..."
    }
  ],
  "articles": [
    {
      "section_code": "A01",
      "section_name": "都市快报",
      "title": "文章标题",
      "url": "https://...",
      "author": "记者姓名",
      "publish_date": "2026-03-28",
      "content": "正文内容...",
      "word_count": 1234
    }
  ]
}
```

### 单篇文章文件（可选）

当使用 `--individual` 参数时，会在日期目录下保存每篇文章为独立JSON文件：

```
dskb_2026-03-28/
├── article_A01_001.json
├── article_A02_001.json
└── ...
```

## 🛠️ 辅助工具

### 生成内容摘要

```bash
python3 generate_summary.py 2026-03-28
```

输出统计信息、版块分布、重点新闻、长文章Top5等。

### 提取"很短很新鲜"版面

```bash
python3 extract_short_news.py 2026-03-28
```

列出该版面的所有短新闻标题和预览。

## 🔍 技术细节

### 网站结构

- **版块列表页**: `https://hzdaily.hangzhou.com.cn/dskb/YYYY/MM/DD/page_detail_2_YYYYMMDD[版块].html`
  - 嵌入iframe指向 `article_list_2_YYYYMMDD[版块].html`
- **文章列表页**: `article_list_2_YYYYMMDD[版块].html`
- **文章详情页**: `article_detail_2_YYYYMMDD[版块][序号].html`

### 核心流程

1. 构造所有版块的 `page_detail` URL（A01-A08, B01-B08）
2. 下载页面，提取iframe的 `src`（`article_list`）
3. 解析文章列表页，提取所有文章链接
4. 并发下载文章详情（带延迟避免被封）
5. 提取标题、作者、内容、字数
6. 保存数据

## 📝 注意事项

- ⏱️ **请求延迟**：默认0.5秒间隔，避免对服务器造成压力
- 📈 **User-Agent**：已设置为桌面浏览器标识
- 🔒 **仅用于学习研究**：请遵守网站robots.txt和服务条款
- 📅 **历史数据**：仅能抓取网站还保留数字报的日期

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 数据来源：[杭州日报](https://hzdaily.hangzhou.com.cn)
- 开发工具：Python 3.8+, requests

---

**⚠️ 免责声明**：本工具仅供学习和研究使用。使用者需自行遵守相关法律法规和网站的使用条款。作者不对使用本工具产生的任何后果负责。
