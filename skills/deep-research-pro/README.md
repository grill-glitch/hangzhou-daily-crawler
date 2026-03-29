# Deep Research Pro 🔬

A powerful, self-contained deep research skill for [OpenClaw](https://github.com/openclaw/openclaw) / Clawdbot agents. Produces thorough, cited reports from multiple web sources using **multi-engine search with mandatory bilingual (Chinese + English) coverage**.

**No paid APIs required** — uses 17 search engines via multi-search-engine skill.

## Features

- 🔍 **Bilingual multi-engine search**: Always searches in both Chinese and English
- 🌏 **17 search engines**: Google, Bing, Baidu, Sogou, DuckDuckGo, Brave, Yahoo, Startpage, Ecosia, Qwant, 360, etc.
- 📄 Full-page content fetching for deep reads
- 📊 Automatic deduplication across queries and engines
- 📝 Structured reports with citations and CN/EN source breakdown
- 💾 Save to file (Markdown or JSON)
- 🆓 Completely free (no API keys)

## Installation

```bash
clawhub install deep-research-pro
```

## Usage

### As an Agent Skill

Just ask your agent to research something:
```
"Research the current state of nuclear fusion energy"
"Deep dive into Rust vs Go for backend services"
"LLM在医疗诊断中的应用现状"
"中国半导体行业的最新进展"
```

The agent will follow the bilingual workflow in `SKILL.md` to produce a comprehensive report using multiple search engines in both Chinese and English.

### CLI Tool

The `scripts/research` tool can also be used standalone:

```bash
# Basic multi-engine search (single language)
./scripts/research "query 1" "query 2" "query 3"

# Full bilingual research mode (requires both CN and EN keywords)
./scripts/research --full --lang-cn "中文关键词" --lang-en "english keywords"

# Save to file
./scripts/research --full --lang-cn "AI 医疗" --lang-en "AI healthcare" --output results.md

# JSON output
./scripts/research "topic" --json
```

### Options

| Flag | Description |
|------|-------------|
| `--full` | Enable multi-engine + fetch top pages |
| `--lang-cn` | Chinese keywords (required for bilingual mode) |
| `--lang-en` | English keywords (required for bilingual mode) |
| `--max N` | Max results per query per engine (default 8) |
| `--fetch-top N` | Fetch full text of top N results (default 3 in --full mode) |
| `--output FILE` | Save results to file |
| `--json` | Output as JSON |

## How It Works

1. **Plan** — Break topic into 3-5 sub-questions
2. **Bilingual keyword generation** — Create both Chinese and English keyword sets
3. **Search** — Run queries across 17 engines, using appropriate language engines
4. **Deduplicate** — Remove duplicate sources across engines and languages
5. **Deep Read** — Fetch full content from key sources (balanced CN/EN)
6. **Synthesize** — Write structured report with citations, noting CN/EN split
7. **Report** — Include methodology summary with source counts by language

## Report Structure

```markdown
# Topic: Deep Research Report

## Executive Summary
## 1. First Major Theme
## 2. Second Major Theme
## Key Takeaways
## Sources (with links)
## Methodology
  - Searched N queries in Chinese and English
  - Engines: 17 total (Google, Bing, Baidu, etc.)
  - Sources: Total M (CN: X, EN: Y)
```

## Bilingual Search Strategy

**CRITICAL: Always use both Chinese and English keywords, regardless of user's query language.**

- If user asks in **Chinese**: Generate 3-5 English keyword variations
- If user asks in **English**: Generate 3-5 Chinese keyword variations
- If user asks in **mixed** or other language: Generate both Chinese and English sets

**Engine assignment:**
- Chinese keywords → Baidu, Sogou, 360, Bing CN
- English keywords → Google, Bing INT, DuckDuckGo, Brave, Yahoo, Startpage, Qwant, Ecosia

This ensures comprehensive coverage of both CN and global sources.

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (auto-installs dependencies)
- Search skill installed: `multi-search-engine` (no setup needed)
- `web_fetch` tool for page content extraction
- Optional: `tavily-search` (if TAVILY_API_KEY set)
- No external paid APIs needed

## Search Engine Coverage (17 Engines)

### Domestic (8 CN engines)
Baidu, Bing CN, Bing INT, 360, Sogou, WeChat, Toutiao, Jisilu

### International (9 global engines)
Google, Google HK, DuckDuckGo, Yahoo, Startpage, Brave, Ecosia, Qwant, WolframAlpha

## License

MIT

## Author

Built by [AstralSage](https://moltbook.com/u/AstralSage) 🦞
