#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step2 视觉理解：智谱 GLM-4V-Flash 逐镜头分析（免费通道）
底座：image-read/scripts/analyze_image.py（zhipuai 库 + glm-4v）
用法：python3 step2_vision.py <parse.json路径> [输出目录]
输出：<输出目录>/vision.json [{idx, frame, analysis:{景别,运镜,主体,光线,情绪,物理细节,画面描述}}]
零成本：智谱免费 API（bigmodel.cn 注册即得）
"""
import base64, json, os, sys

def get_zhipu_key():
    k = os.environ.get("ZHIPU_API_KEY", "")
    if k: return k
    return ""

PROMPT = """你是专业视频分镜分析师。分析这张视频关键帧，输出 JSON：
{"景别":"(ECU大特写/CU特写/MCU中近景/MS中景/MLS中全景/WS全景/VWS远景/EWS大远景，对齐分镜表模板8级)", "运镜":"(固定/手持/推/拉/摇/移/升降/环绕，依据画面推断)", "主体":"(画面主体是什么，属性清单)", "光线":"(主光方向/光源类型/色调)", "情绪":"(画面传达的情绪)", "物理细节":"(可见的真实性锚点：材质/反光/纹理/动态模糊)", "画面描述":"(构图+背景，供分镜表引用)"}
只输出 JSON，不要其他文字。"""

def analyze_frame(frame_path, api_key):
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key=api_key)
    with open(frame_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    data_url = f"data:image/jpeg;base64,{b64}"
    resp = client.chat.completions.create(
        model="glm-4v-flash",
        messages=[{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": data_url}},
            {"type": "text", "text": PROMPT},
        ]}],
    )
    return resp.choices[0].message.content

def main():
    parse_path = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(parse_path)
    parse = json.load(open(parse_path, encoding="utf-8"))
    api_key = get_zhipu_key()
    if not api_key:
        print("⚠️ ZHIPU_API_KEY 未配置（bigmodel.cn 免费注册），降级为跳过视觉分析")
        with open(os.path.join(outdir, "vision.json"), "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)
        sys.exit(0)

    results = []
    for sc in parse["scenes"]:
        frame = sc.get("frame", "")
        if not frame or not os.path.exists(frame):
            results.append({"idx": sc["idx"], "analysis": {"景别": "未知", "画面描述": "无关键帧"}})
            continue
        try:
            content = analyze_frame(frame, api_key)
            try:
                analysis = json.loads(content)
            except Exception:
                import re
                m = re.search(r"\{.*\}", content, re.S)
                analysis = json.loads(m.group(0)) if m else {"原始输出": content[:300]}
            results.append({"idx": sc["idx"], "frame": frame, "analysis": analysis})
            print(f"  镜头{sc['idx']}: {str(analysis.get('景别',''))} / {str(analysis.get('主体',''))[:30]}")
        except Exception as e:
            results.append({"idx": sc["idx"], "frame": frame, "analysis": {"error": str(e)[:200]}})
            print(f"  ⚠️ 镜头{sc['idx']} 分析失败: {str(e)[:100]}")

    with open(os.path.join(outdir, "vision.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(f"✅ Step2 完成：{len(results)} 镜头视觉分析 → {outdir}/vision.json")

if __name__ == "__main__":
    main()
