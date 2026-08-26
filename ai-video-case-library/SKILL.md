---
name: ai-video-case-library
description: >
  AI 视频案例库（开源版）——135 个真实 AI 视频案例中精选 7 大分类 14 条脱敏示例，
  含完整可复用 prompt 与元数据（分类/时长/热度），支持关键词检索与分类筛选。
  案例 prompt 提炼自真实 Seedance 2.5 生成视频，10 段式结构可直接复用于 AI 视频生成。
  触发词：AI视频案例、视频案例库、案例库、prompt 案例、分镜参考、爆款视频提示词。
version: 1.0.0
license: MIT
metadata:
  tags: [ai-video, case-library, prompt]
---

# ai-video-case-library · AI 视频案例库（开源版）

> 隆森AI 开源技能包 · MIT 许可
> 完整版（135 条案例全量 + 电商广告子集 28 条 / 工作台模块）见 README 入口

---

## 1. 是什么

**从真实 AI 视频案例里找可复用的提示词**：135 个真实 AI 生成视频（Seedance 2.5）案例中，精选 7 大分类共 14 条脱敏示例，每条含**完整 prompt + 分类 + 时长 + 热度数据**。输入需求 → 检索匹配案例 → 复制 prompt 去生成你自己的 AI 视频。

## 2. 分类体系（7 大类）

| 分类 | 覆盖 | 示例条数（开源版） |
|:--|:--|:--:|
| UGC & Vlog | 自拍感/生活记录/旅拍/日常 vlog | 2 |
| Product Ads & Brand | 产品开箱/品牌广告/商业片 | 2 |
| Character & Product Consistency | 人物/产品一致性锁定 | 2 |
| Dialogue & Native Audio | 对话/原生配音/口播 | 2 |
| 30s Stories & One Take | 30 秒故事/一镜到底 | 2 |
| Action & Anime | 动作场面/动漫风 | 2 |
| More Styles & Techniques | 风格化/转场/特效技巧 | 2 |

## 3. Prompt 结构（10 段式，与 video-prompt-reverse 同源）

案例 prompt 遵循可复现的 10 段式结构，含以下关键信息：

- **FORMAT**：时长/画幅/风格基调
- **TIMELINE**：分段时间轴 + 每段画面
- **SPEECH / AUDIO**：台词、配音、音效
- **LOCKS**：一致性锚点（人物/产品/服装/环境）
- **PHYSICS / LIGHTING**：物理规律、光照

> 逆向拆解任意视频 → 用 `video-prompt-reverse`；正向生成视频提示词 → 参考本库案例结构。

## 4. 快速开始（检索示例数据）

```bash
# 关键词检索
python3 scripts/search_cases.py "vlog 东京"

# 按分类筛选
python3 scripts/search_cases.py --category "UGC & Vlog"
```

输出：匹配案例的标题、分类、时长、热度 + 完整 prompt。

## 5. 责任护栏

- 案例 prompt 内如涉及真实人物，禁止用于克隆/冒充真人（deepfake 防护）
- 示例数据已脱敏（不含内部来源/内部字段），商用请自行评估素材合规
- 完整案例库（135 条全量 + 电商广告子集）为付费资产，见 README 引流入口

## 6. 许可证与声明

- MIT License；示例数据提炼自公开 AI 视频案例站（prompt 文本），仅作学习参考
- 与 `video-prompt-reverse`（视频逆向拆解）、`image-prompt-hub`（图片提示词库）构成图+视频三件套
