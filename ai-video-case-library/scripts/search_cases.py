#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-video-case-library 示例检索 demo（开源版）
用法：python3 search_cases.py "vlog 东京"
      python3 search_cases.py --category "UGC & Vlog"
"""
import json
import os
import sys

EXAMPLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "examples", "sample_video_cases.json")


def load():
    with open(EXAMPLES, encoding="utf-8") as f:
        return json.load(f)


def main():
    args = sys.argv[1:]
    q = ""
    category = ""
    for i, a in enumerate(args):
        if a == "--category" and i + 1 < len(args):
            category = args[i + 1]
        elif not a.startswith("--"):
            q = a
    items = load()
    results = []
    for it in items:
        text = f"{it.get('title','')} {it.get('category','')} {it.get('prompt','')}".lower()
        if category and category.lower() not in it.get("category", "").lower():
            continue
        if q:
            if q.lower() not in text:
                continue
        results.append(it)
    print(f"🎬 检索: {'全部' if not q else q}{(' / ' + category) if category else ''} | 命中 {len(results)} 条（示例 14 条，完整 135 条见 README）\n")
    for r in results[:8]:
        print(f"■ {r.get('title','')} [{r.get('category','')} · {r.get('duration','')} · ⭐{r.get('saves',0)}]")
        print(f"  {r.get('prompt','')[:150]}…\n")


if __name__ == "__main__":
    main()
