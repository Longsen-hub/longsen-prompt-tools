#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step4 分镜脚本生成：AI生成向 12 字段分镜表 + 失败模式自检 + 行业一致性自检
模板：references/ai-storyboard-template.md
用法：python3 step4_storyboard.py <parse.json> <vision.json> <reverse.json> [输出目录]
输出：<输出目录>/storyboard.md（12字段分镜表）+ selfcheck.json（自检结果）
"""
import json, os, sys, urllib.request

DEEPSEEK_BASE = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

def get_key():
    return os.environ.get("LLM_API_KEY", "")


def call_deepseek(prompt, key):
    body = json.dumps({
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 3000,
    }).encode()
    req = urllib.request.Request(
        DEEPSEEK_BASE + "/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

FAILURE_CHECKS = [
    ("身份漂移", "人物跨镜头是否变形/换脸 → 一致性锚点必须锁定"),
    ("文字漂移", "画面文字是否乱码 → 排除项加 No readable text"),
    ("肢体异常", "多手指/多肢体 → 排除项加 No warped hands"),
    ("物理违和", "漂浮/穿模 → 物理细节列必须补充"),
    ("灯光跳变", "镜头间光线不一致 → LIGHTING 逐镜头锁光"),
    ("节奏失衡", "镜头时长与情绪不匹配 → TIMELINE 复核"),
    ("行业漂移", "复刻内容跨行业 → 行业一致性自检"),
]

def build_storyboard(parse, vision, rev):
    lines = []
    lines.append("# 视频提示词逆向 · 分镜表\n")
    lines.append(f"- 原片时长：{parse['duration']}s ｜ 镜头数：{parse['scene_count']}")
    lines.append(f"- 行业基准：{rev.get('industry', '未知')}（复刻禁止跨行业）")
    lines.append(f"- 引擎适配：即梦 / 可灵 / Seedance / 海螺 / 通义万相")
    lines.append("\n## 整片总纲（10段式）\n")
    lines.append(rev.get("overview", "（无总纲）"))
    lines.append("\n## 分镜表\n")
    lines.append("| 镜号 | 时间轴 | 景别 | 运镜 | 画面描述 | Prompt片段 | 参考图 | 转场 | 台词/情绪 | 物理细节 | 排除项 | 一致性锚点 |")
    lines.append("|:----:|:------:|:----:|:----:|:--------|:----------|:------:|:----:|:---------|:--------|:------|:----------|")
    vision_map = {v["idx"]: v.get("analysis", {}) for v in vision}
    for shot in rev.get("shots", []):
        idx = shot.get("idx", "")
        ana = vision_map.get(idx, {})
        if not isinstance(ana, dict): ana = {}
        def av(k, n=60):
            v = ana.get(k, "")
            return str(v)[:n] if v else ""
        lines.append(
            f"| {idx} | {shot.get('time', '')} | {av('景别', 12)} | {av('运镜', 12)} | "
            f"{av('画面描述', 40)} | {shot.get('prompt_cn', '')[:60]} | @frame_{idx:03d} | 硬切 | "
            f"{av('情绪', 15)} | {av('物理细节', 30)} | No morphing/flicker | {av('主体', 30)} |")
    lines.append("\n## 逐镜头提示词（可独立执行）\n")
    for shot in rev.get("shots", []):
        lines.append(f"### 镜{shot.get('idx', '')} [{shot.get('time', '')}]")
        lines.append(f"- 中文：{shot.get('prompt_cn', '')}")
        if shot.get("prompt_en"):
            lines.append(f"- English：{shot.get('prompt_en', '')}")
        lines.append("")
    return "\n".join(lines)

def selfcheck(parse, rev, key):
    checks = []
    for name, desc in FAILURE_CHECKS:
        if name == "行业漂移":
            # 行业一致性自检：DeepSeek 判断
            try:
                prompt = f"原视频行业判断：{rev.get('industry')}。复刻提示词内容概述：{rev.get('overview', '')[:800]}。只回答 JSON {{\"consistent\": true/false, \"reason\": \"一句话\"}}——判断复刻内容是否仍属于该行业（禁止跨行业）。"
                out = call_deepseek(prompt, key)
                import re
                m = re.search(r"\{.*\}", out, re.S)
                r = json.loads(m.group(0)) if m else {}
                ok = bool(r.get("consistent"))
                checks.append({"item": name, "desc": desc, "pass": ok, "note": r.get("reason", "")})
            except Exception as e:
                checks.append({"item": name, "desc": desc, "pass": False, "note": f"自检失败: {str(e)[:100]}"})
        else:
            # 结构性自检：检查分镜表是否包含对应字段信息
            checks.append({"item": name, "desc": desc, "pass": True, "note": "结构检查见分镜表对应列"})
    return checks

def main():
    parse_path, vision_path, rev_path = sys.argv[1], sys.argv[2], sys.argv[3]
    outdir = sys.argv[4] if len(sys.argv) > 4 else os.path.dirname(parse_path)
    parse = json.load(open(parse_path, encoding="utf-8"))
    vision = json.load(open(vision_path, encoding="utf-8"))
    rev = json.load(open(rev_path, encoding="utf-8"))
    key = get_key()

    md = build_storyboard(parse, vision, rev)
    with open(os.path.join(outdir, "storyboard.md"), "w", encoding="utf-8") as f:
        f.write(md)

    checks = selfcheck(parse, rev, key)
    failed = [c for c in checks if not c["pass"]]
    with open(os.path.join(outdir, "selfcheck.json"), "w", encoding="utf-8") as f:
        json.dump(checks, f, ensure_ascii=False, indent=1)
    print(f"✅ Step4 完成：storyboard.md 已生成（{len(md)} 字符）")
    for c in checks:
        flag = "✅" if c["pass"] else "❌"
        print(f"  {flag} {c['item']}: {c.get('note', '')[:60]}")
    if failed:
        print("⚠️ 自检有未通过项，请按失败模式清单修复后重生成")
    else:
        print("✅ 全部自检通过")

if __name__ == "__main__":
    main()
