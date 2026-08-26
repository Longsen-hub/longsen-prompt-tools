---
name: video-prompt-reverse
description: >
  视频提示词逆向师（开源版）——把一段视频逆向拆解为：①整片10段式提示词总纲
  （FORMAT/REFERENCES/CAMERA LOCK/TIMELINE/SPEECH/CONTINUITY/PHYSICS/LIGHTING/AUDIO/LOCKS）
  ②每镜头独立可执行提示词 ③AI生成向分镜表（12字段）。工程化底座：PySceneDetect/ffmpeg镜头切分+
  本地whisper转写+多模态视觉理解（GLM-4V-Flash免费）+LLM逆向生成。
  方法论继承：video-prompt-reverse(23★) + video-spec-builder(925★) + Seedance2-Storyboard-Generator(2192★)。
  触发词：反推这段视频、视频提示词、逆向提示词、视频拆解成提示词、分镜脚本。
version: 1.0.0
license: MIT
metadata:
  tags: [video-prompt, reverse, storyboard]
---

# video-prompt-reverse · 视频提示词逆向师（开源版）

> 隆森AI 开源技能包 · MIT 许可
> 业务闭环：**视频 → 提示词 → 分镜头脚本**（可复用创作资产）
> 完整版（含行业案例库与数据服务）见 README 引流入口

---

## 1. 是什么

上传一个视频 → 输出三份交付物：

1. **整片 10 段式提示词总纲**：可直接整体喂 AI 视频模型（即梦/可灵/Seedance/海螺等）
2. **逐镜头提示词**：每镜头一个可独立执行的提示词
3. **AI 生成向分镜表**：12 字段逐镜头表（镜号/时间轴/景别/运镜/画面/prompt片段/参考图/转场/台词情绪/物理细节/排除项/一致性锚点）

## 2. 方法论文档继承（开源声明）

| 底座 | 继承内容 |
|:--|:--|
| luozhilzh/video-prompt-reverse (23★ MIT) | 9 步反推工作流 / 运动设计一等维度 / 视频专属负向词库 / 一致性锚点 / deepfake 责任护栏 |
| feicaiclub/video-spec-builder (925★ MIT) | 分镜规格化 / 追问深挖 / 场景拆解 |
| liangdabiao/Seedance2-Storyboard-Generator (2192★) | 时间轴分镜格式 / 素材编号体系 / 四幕结构 |
| raojiacui/prompt-lens (502★ MIT) | 反推 + 音频台词提取一体化思路 |
| Breakthrough/PySceneDetect (5122★ BSD-3) | 镜头/场景切分工程底座 |

## 3. 核心工作流（4 步工具链）

```
视频上传
  ↓ Step1 解析      PySceneDetect 镜头切分 → ffmpeg 按镜头抽帧 → faster-whisper 完整转写
  ↓ Step2 视觉理解   GLM-4V-Flash（免费通道）逐镜头分析：景别/运镜/主体/光线/情绪
  ↓ Step3 提示词逆向 LLM 按 10 段式输出整片总纲 + 逐镜头提示词
  ↓ Step4 分镜脚本   AI生成向 12 字段分镜表 + 失败模式自检 + 行业一致性自检
  ↓
交付：10段式总纲 + 每镜头提示词 + 分镜表
```

## 4. 快速开始

```bash
# 依赖：python3 + ffmpeg + PySceneDetect + faster-whisper（本地）+ 智谱 GLM-4V key（免费注册 bigmodel.cn）+ LLM API key
export ZHIPU_API_KEY="你的智谱key"      # 免费通道 bigmodel.cn
export LLM_API_KEY="你的LLM key"

cd video-prompt-reverse/scripts
./run_all.sh /path/to/video.mp4 /tmp/vpr_out
# 输出：parse.json / vision.json / reverse.json / storyboard.md / selfcheck.json
```

示例：`examples/` 目录含 5 条示例提示词（示例数据，完整版见 README 入口）

## 5. 10 段式输出规范（核心方法论）

```
① FORMAT        格式锁定（时长/画幅/设备感）
② REFERENCES    参考图逐项描述（@image1 人物属性 / @image2 产品属性）
③ CAMERA LOCK   机位规则（哪些机位可能/不可能）
④ TIMELINE      时间轴分段（每段=场景+动作+情绪，标确切秒数）
⑤ SPEECH        台词剧本（带秒+情绪+走位，每句台词绑定可见动作——唇形同步锚点）
⑥ CONTINUITY    一致性锁定（房间/服装/配饰/人物属性，开头锁定后续不丢主体）
⑦ PHYSICS       物理细节（真实性来源：衣物随动作滑落/头发滞后一帧/床单褶皱）
⑧ LIGHTING      灯光方案（每镜头主光/补光）
⑨ AUDIO         声音设计（环境声清单/对话语气/音乐开关）
⑩ LOCKS         风格锁 + STRICTLY AVOID 排除项（No morphing/No flicker/No warped hands/No identity drift）
```

## 6. 责任护栏

- 拒绝协助"克隆可识别真实人物容貌以冒充本人"（deepfake）
- 视频含可识别真实人物（本人以外者）：不得显式锁定其容貌身份用于冒充；自有肖像权除外
- 检测到未成年人出镜：身份复刻降权/拒绝
- 合理用途正常服务：复刻自己、虚构角色、风格/运镜/场景模仿

## 7. 许可证与声明

- 本开源版：MIT（保留底座项目各自版权声明）
- 完整版（含 135 行业案例库 / 21,719 条图片提示词数据底座 / 工作台模块）：见 README 入口

## 8. 版本历史

| 版本 | 日期 | 变更 |
|:--|:--|:--|
| 1.0.0 | 2026-08-27 | 开源首版：方法论 + 工具链 + 示例数据（脱敏） |
