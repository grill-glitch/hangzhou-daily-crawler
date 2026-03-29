---
name: deep-research-pro
version: 1.0.0
description: "Multi-source deep research agent. Searches the web using multiple engines, synthesizes findings, and delivers cited reports."
homepage: https://github.com/paragshah/deep-research-pro
metadata: {"clawdbot":{"emoji":"🔬","category":"research"}}
---

# Deep Research Pro 🔬

A powerful deep research skill that produces thorough, cited reports from multiple web sources using **multi-engine search** (17 engines via multi-search-engine skill). **Always searches in both Chinese and English** regardless of query language.

## How It Works

When the user asks for research on any topic, follow this workflow:

### Step 1: Understand the Goal (30 seconds)

Ask 1-2 quick clarifying questions:
- "What's your goal — learning, making a decision, or writing something?"
- "Any specific angle or depth you want?"

If the user says "just research it" — skip ahead with reasonable defaults.

### Step 2: Plan the Research (think before searching)

Break the topic into 3-5 research sub-questions. For example:
- Topic: "Impact of AI on healthcare"
  - What are the main AI applications in healthcare today?
  - What clinical outcomes have been measured?
  - What are the regulatory challenges?
  - What companies are leading this space?
  - What's the market size and growth trajectory?

### Step 3: Bilingual Search Strategy (CRITICAL)

**For EVERY sub-question, generate and search BOTH Chinese and English keywords.**

#### Why Bilingual?
- **Chinese engines** (Baidu, Sogou, 360, etc.) index CN-content that global engines miss
- **English engines** (Google, Bing, DuckDuckGo) cover international sources
- Ensures comprehensive coverage for topics involving China or Chinese-language content
- Even if the user asks in English, Chinese sources may have unique insights
- Even if the user asks in Chinese, English sources provide global perspective

#### How to Generate Keywords

1. **Start from the original sub-question** (in user's language)
2. **Create English version** (if original is Chinese) or **Chinese version** (if original is English)
3. **Add keyword variations** (2-3 per language):
   - Synonyms
   - Alternative phrasings
   - Technical vs. layman terms
   - Include year for current topics (e.g., "2026")

**Example (user asks in Chinese):**
- Original: "大语言模型在医疗领域的应用"
- English variations:
  - "LLM applications in healthcare"
  - "large language models medical use cases"
  - "AI translation in clinical settings"

**Example (user asks in English):**
- Original: "Rust vs Go for backend services"
- Chinese variations:
  - "Rust 与 Go 后端服务对比"
  - "Rust Go 后端开发 选择"
  - "后端语言 Rust Go 性能对比"

### Step 4: Execute Multi-Engine Search

**For each keyword (both languages), search across multiple engines:**

Use `web_fetch` with URLs constructed for different search engines:

```bash
# For EACH keyword (both CN and EN):

# Google (English/global)
web_fetch({"url": "https://www.google.com/search?q=<encoded-query>", "extractMode": "markdown", "maxChars": 2000})

# Bing International
web_fetch({"url": "https://cn.bing.com/search?q=<encoded-query>&ensearch=1", "extractMode": "markdown", "maxChars": 2000})

# Baidu (Chinese)
web_fetch({"url": "https://www.baidu.com/s?wd=<encoded-query>", "extractMode": "markdown", "maxChars": 2000})

# Sogou (Chinese)
web_fetch({"url": "https://sogou.com/web?query=<encoded-query>", "extractMode": "markdown", "maxChars": 2000})

# 360 (Chinese)
web_fetch({"url": "https://www.so.com/s?q=<encoded-query>", "extractMode": "markdown", "maxChars": 2000})

# DuckDuckGo (global, privacy-focused)
web_fetch({"url": "https://duckduckgo.com/html/?q=<encoded-query>", "extractMode": "markdown", "maxChars": 2000})

# Brave (global)
web_fetch({"url": "https://search.brave.com/search?q=<encoded-query>", "extractMode": "markdown", "maxChars": 2000})
```

**Search strategy:**
- For each sub-question, aim for 6-10 total keyword queries (3-5 EN + 3-5 CN)
- Distribute across engines:
  - **English keywords** → Google, Bing INT, DuckDuckGo, Brave, Yahoo, Startpage, Qwant, Ecosia
  - **Chinese keywords** → Baidu, Sogou, 360, Bing CN
- Use time filters for current topics: add `&tbs=qdr:m` (past month) or `&tbs=qdr:w` (past week)
- Use site-specific searches when appropriate: `site:arxiv.org <query>` or `site:github.com <query>` or `site:csdn.net <query>`
- Aim for 40-60 unique sources total across all sub-questions and languages
- Limit extraction to ~2000 chars per result to manage token usage

**Optional: Tavily enhancement**
If TAVILY_API_KEY is configured, you can optionally add Tavily results (it handles both languages well). However, ensure the workflow works 100% without it.

### Step 5: Deep-Read Key Sources

For the most promising URLs (top 3-5 per major theme), fetch full content:

```bash
web_fetch({"url": "<url>", "extractMode": "markdown", "maxChars": 8000})
```

Tips:
- Balance between Chinese and English sources in your reading
- Focus on sources with comprehensive coverage
- Extract main content, ignore navigation/ads
- Keep snippets for citation (store title, URL, excerpt)

### Step 6: Synthesize & Write Report

Structure the report as:

```markdown
# [Topic]: Deep Research Report
*Generated: [date] | Sources: [N] | Confidence: [High/Medium/Low]*

## Executive Summary
[3-5 sentence overview of key findings, mentioning both CN and EN insights if relevant]

## 1. [First Major Theme]
[Findings with inline citations]
- Key point ([Source Name](url))
- Supporting data ([Source Name](url))

## 2. [Second Major Theme]
...

## 3. [Third Major Theme]
...

## Key Takeaways
- [Actionable insight 1]
- [Actionable insight 2]
- [Actionable insight 3]

## Sources
1. [Title](url) — [one-line summary]
2. ...

## Methodology
Searched [N] queries across 17 search engines in both Chinese and English.
Sub-questions investigated: [list]
Engines: Google, Bing (INT/CN), Baidu, Sogou, 360, DuckDuckGo, Yahoo, Startpage, Brave, Ecosia, Qwant, WolframAlpha.
Total unique sources: [M] (CN: X, EN: Y)
```

### Step 7: Save & Deliver

Save the full report:
```bash
mkdir -p ~/clawd/research/[topic-slug]
# Write report to ~/clawd/research/[topic-slug]/report.md
```

Then deliver based on length:
- **Short topics** (<1000 words): Post full report in chat
- **Long reports**: Post executive summary + key takeaways, offer full report as file attachment

## Quality Rules

1. **Every claim needs a source.** No unsourced assertions. Link citations inline.
2. **Cross-reference.** If only one source says it, flag as unverified or emerging.
3. **Recency matters.** Prefer sources from last 12 months for fast-moving topics.
4. **Language diversity.** Ensure sources include both Chinese and English perspectives when relevant.
5. **Engine diversity.** Sources should span multiple search engines to reduce bias.
6. **Acknowledge gaps.** If you couldn't find good info on a sub-question in one language, note that.
7. **No hallucination.** If you don't know, say "insufficient data found" — don't invent.
8. **Academic rigor.** For technical/scientific topics, prioritize peer-reviewed papers and official documentation.

## Examples

```
"Research the current state of nuclear fusion energy"
"Deep dive into Rust vs Go for backend services"
"Research the best strategies for bootstrapping a SaaS business"
"What's happening with the US housing market right now?"
"Compare transformer vs Mamba architecture for NLP"
"LLM在医疗诊断中的应用现状"
"中国半导体行业的最新进展"
```

## For Sub-Agent Usage

When spawning as a sub-agent, include the full research request and bilingual requirement:

```python
sessions_spawn(
  task=f"""Run deep research on {topic}. Follow the deep-research-pro SKILL.md workflow.
Goal: {goal}
Specific angles: {angles}

CRITICAL: Use BILINGUAL search strategy:
- For each sub-question, generate 3-5 Chinese keywords AND 3-5 English keywords
- Search Chinese keywords on: Baidu, Sogou, 360, Bing CN
- Search English keywords on: Google, Bing INT, DuckDuckGo, Brave, Yahoo, Startpage, Qwant, Ecosia
- Use site: operators and time filters as needed
- Aim for balanced CN/EN source coverage

Fetch full content from top 3-5 sources per theme (maxChars=8000).
Save report to ~/clawd/research/{slug}/report.md
Include in methodology: counts of CN vs EN sources.
When done, wake the main session with key findings.""",
  label=f"research-{slug}",
  thinking="high",
  model="openrouter/anthropic/claude-3-7-sonnet"
)
```

## Requirements

- **Search skill installed:** `multi-search-engine` (no setup needed, 17 engines)
- `web_fetch` tool for page content extraction
- Optional: `tavily-search` (if TAVILY_API_KEY set)
- No external paid APIs needed

## Notes

- This skill uses **multi-search-engine** exclusively (17 search engines across CN and global)
- **Bilingual search is mandatory** — always produce both Chinese and English keyword sets
- Using multiple engines mitigates individual engine biases and gaps
- For best results, combine breadth (many engines + both languages) with depth (full-page reads)
- When topic is China-specific, prioritize Chinese engines; when global, still include both for completeness
