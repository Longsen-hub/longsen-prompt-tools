#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""image-prompt-hub 示例检索 demo（开源版）
用法：python3 search_demo.py "小红书 护肤 极简"
      python3 search_demo.py --scene 电商
"""
import json, os, sys

EXAMPLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "examples", "sample_prompts.json")

def load():
    with open(EXAMPLES, encoding="utf-8") as f:
        return json.load(f)

def main():
    args = sys.argv[1:]
    q = ""
    scene = ""
    for i, a in enumerate(args):
        if a == "--scene" and i + 1 < len(args):
            scene = args[i + 1]
        elif not a.startswith("--"):
            q = a
    items = load()
    results = []
    for it in items:
        text = f"{it.get('title','')} {it.get('scene','')} {' '.join(it.get('tags',[]))}".lower()
        if scene and scene.lower() not in it.get("scene", "").lower():
            continue
        if q:
            if q.lower() not in text and q.lower() not in it.get("prompt", "")[:200].lower():
                continue
        results.append(it)
    print(f"🔍 检索: {'全部' if not q else q} | 命中 {len(results)} 条（示例数据，完整版 21,719 条见 README）\n")
    for r in results[:8]:
        print(f"■ {r.get('title','')} [{r.get('scene','')} · {r.get('style','')} · {r.get('model','')}]")
        print(f"  {r.get('prompt','')[:120]}…\n")

if __name__ == "__main__":
    main()
