#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step3 提示词逆向：DeepSeek 按《视频提示词写法规范》10段式输出
输出：①整片10段式总纲 ②逐镜头可执行提示词（每镜头一个）
key：env LLM_API_KEY（或 DEEPSEEK_API_KEY）
用法：python3 step3_reverse.py <parse.json> <vision.json> [输出目录]
"""
import json, os, sys, urllib.request

DEEPSEEK_BASE = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

def get_key():
    return os.environ.get("LLM_API_KEY", "")


# 《视频提示词写法规范》10 段式（源自 evolink 135 案例精华，output/图文成片镜头配方卡/）
TEN_PART = """① FORMAT 格式锁定（时长/画幅/设备感）
② REFERENCES 参考图逐项描述（@image1 人物属性清单/@image2 产品属性清单）
③ CAMERA LOCK 机位规则（哪些机位可能/不可能）
④ TIMELINE 时间轴分段（每段=场景+动作+情绪，标确切秒数）
⑤ SPEECH 台词剧本（带秒+情绪+走位，每句台词必须绑定可见动作——唇形同步锚点）
⑥ CONTINUITY 一致性锁定（房间/服装/配饰/人物属性，开头锁定一次后续不丢主体）
⑦ PHYSICS 物理细节（真实性来源：衣物随动作滑落/头发滞后一帧/床单褶皱）
⑧ LIGHTING 灯光方案（每镜头主光/补光）
⑨ AUDIO 声音设计（环境声清单/对话语气/音乐开关）
⑩ LOCKS 风格锁（4K/颗粒/色温/快门）+ STRICTLY AVOID 排除项（No morphing/No flicker/No warped hands/No duplicated limbs/No identity drift/No text drift）"""

PROMPT_TMPL = """你是资深视频提示词逆向工程师。基于以下视频分析素材，逆向输出该视频的完整提示词资产。

【分析素材】
- 视频时长：{duration}s，镜头数：{scenes}
- 完整口播转写：{transcript}
- 逐镜头视觉分析：{vision}

【输出要求】
第一部分：整片 10 段式提示词总纲（严格按以下结构）：
{TEN_PART}

第二部分：逐镜头提示词（每个镜头一段，格式：`[镜号] 时间轴 景别+主体+动作+环境+光线+运镜+时长+排除项`，时间轴格式 `0:00-0:03 (3s)`，中英双语，可直接粘贴到 AI 视频生成工具）。

【铁律】
1. 行业基准：原视频所属行业就是基准，复刻内容禁止跨越其他行业（术语/语境/受众对齐）
2. 数据真实：所有内容必须来自上述分析素材，禁止编造画面
3. 台词逐字对齐转写稿，不增删
4. 产品与人物分离锁定（电商关键）：人物=身份属性，产品=物理属性，防止变形
5. 输出 JSON：{{"overview": "10段式总纲全文", "industry": "判断的行业", "shots": [{{"idx": 1, "time": "0:00-0:03", "prompt_cn": "中文提示词", "prompt_en": "英文提示词"}}]}}"""

def call_deepseek(prompt, key):
    body = json.dumps({
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 6000,
    }).encode()
    req = urllib.request.Request(
        DEEPSEEK_BASE + "/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def main():
    parse_path, vision_path = sys.argv[1], sys.argv[2]
    outdir = sys.argv[3] if len(sys.argv) > 3 else os.path.dirname(parse_path)
    parse = json.load(open(parse_path, encoding="utf-8"))
    vision = json.load(open(vision_path, encoding="utf-8"))
    key = get_key()
    if not key:
        print("❌ LLM_API_KEY 未配置"); sys.exit(1)

    prompt = PROMPT_TMPL.format(
        duration=parse["duration"],
        scenes=parse["scene_count"],
        transcript=parse.get("transcript", "")[:3000] or "（无口播或转写失败）",
        vision=json.dumps([{"idx": v["idx"], "analysis": v.get("analysis", {})} for v in vision], ensure_ascii=False)[:5000],
        TEN_PART=TEN_PART,
    )
    print("⏳ DeepSeek 逆向生成中（10段式总纲 + 逐镜头提示词）…")
    content = call_deepseek(prompt, key)
    try:
        result = json.loads(content)
    except Exception:
        # 容错：剥离 markdown 代码块
        import re
        m = re.search(r"\{.*\}", content, re.S)
        result = json.loads(m.group(0)) if m else {"overview": content, "industry": "未知", "shots": []}
    result["_meta"] = {"duration": parse["duration"], "scene_count": parse["scene_count"]}
    with open(os.path.join(outdir, "reverse.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"✅ Step3 完成：行业={result.get('industry')} / {len(result.get('shots', []))} 镜头提示词")
    print(f"   输出：{outdir}/reverse.json")

if __name__ == "__main__":
    main()
