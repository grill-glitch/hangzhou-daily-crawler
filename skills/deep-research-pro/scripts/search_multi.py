#!/usr/bin/env python3
"""
Multi-engine search for Deep Research Pro.
Uses configured search skills: web_search (Brave), multi-search-engine, tavily-search.
"""

import sys
import json
import subprocess
from typing import List, Dict, Any


def search_brave(query: str, max_results: int = 8) -> List[Dict[str, Any]]:
    """Search using Brave Search API via web_search tool."""
    try:
        # In OpenClaw, this would be called as a tool
        # For standalone usage, we'll simulate with a note
        print(f"[Brave Search] Query: {query} (max: {max_results})", file=sys.stderr)
        # TODO: Implement actual tool call when running in agent context
        return []
    except Exception as e:
        print(f"[Brave Search Error] {e}", file=sys.stderr)
        return []


def search_multi_engine(query: str, max_results: int = 8) -> List[Dict[str, Any]]:
    """Search using multiple engines via multi-search-engine skill."""
    try:
        print(f"[Multi-Engine Search] Query: {query} (max: {max_results})", file=sys.stderr)
        # Engines: Baidu, Bing CN/INT, Sogou, 360, Google, DuckDuckGo, Brave, etc.
        # TODO: Implement actual tool call in agent context
        return []
    except Exception as e:
        print(f"[Multi-Engine Error] {e}", file=sys.stderr)
        return []


def search_tavily(query: str, max_results: int = 8) -> List[Dict[str, Any]]:
    """Search using Tavily API via tavily-search skill."""
    try:
        print(f"[Tavily Search] Query: {query} (max: {max_results})", file=sys.stderr)
        # TODO: Implement actual tool call in agent context
        return []
    except Exception as e:
        print(f"[Tavily Error] {e}", file=sys.stderr)
        return []


def combined_search(query: str, max_per_engine: int = 8) -> List[Dict[str, Any]]:
    """Execute search across all available engines and deduplicate."""
    all_results = []
    
    # Brave
    brave_results = search_brave(query, max_per_engine)
    for r in brave_results:
        r['_engine'] = 'Brave'
        all_results.append(r)
    
    # Multi-engine (covers many)
    multi_results = search_multi_engine(query, max_per_engine)
    for r in multi_results:
        r['_engine'] = 'Multi'
        all_results.append(r)
    
    # Tavily
    tavily_results = search_tavily(query, max_per_engine)
    for r in tavily_results:
        r['_engine'] = 'Tavily'
        all_results.append(r)
    
    # Deduplicate by URL
    seen = set()
    unique = []
    for r in all_results:
        url = r.get("href") or r.get("url", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(r)
    
    return unique


if __name__ == "__main__":
    # Simple CLI for standalone testing
    if len(sys.argv) < 2:
        print("Usage: search.py <query> [--max N]")
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = 8
    if "--max" in sys.argv:
        idx = sys.argv.index("--max")
        if idx + 1 < len(sys.argv):
            max_results = int(sys.argv[idx + 1])
    
    results = combined_search(query, max_results)
    print(json.dumps(results, indent=2, ensure_ascii=False))
