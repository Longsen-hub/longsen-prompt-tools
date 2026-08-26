# 隆森 Prompt 工坊（Longsen Prompt Tools）

> 视频 → 提示词 → 分镜脚本 ｜ 图片提示词模板库 —— 图+视频双提示词能力开源包
> MIT License · 由 隆森AI 开源

---

## 🎬 这是什么

**两个 AI 提示词工程技能，开源给你免费试用：**

| 技能 | 能力 | 效果 |
|:--|:--|:--|
| **video-prompt-reverse** | 视频逆向拆解 | 一段视频 → 10段式提示词总纲 + 每镜头提示词 + 12字段分镜表 |
| **image-prompt-hub** | 图片提示词检索 | 一句话需求 → 匹配最佳提示词模板（8 场景分类） |

## ✨ 为什么值得试

- **方法源于实战**：10 段式提示词结构提炼自顶级 AI 视频案例库（135 个真实案例）
- **工具链完整**：不是纸面方法论——PySceneDetect 镜头切分 + 本地转写 + 多模态视觉 + LLM 逆向，一条命令跑完
- **免费通道**：视觉理解走 GLM-4V-Flash（免费注册 bigmodel.cn），本地转写零成本
- **责任护栏**：内置 deepfake 防护（拒绝克隆真实人物冒充）

## 🚀 快速开始

```bash
# 视频提示词逆向（见 video-prompt-reverse/SKILL.md）
cd video-prompt-reverse/scripts
export ZHIPU_API_KEY="你的智谱key"   # 免费：bigmodel.cn 注册
export LLM_API_KEY="你的LLM key"
./run_all.sh /path/to/video.mp4 /tmp/vpr_out

# 图片提示词检索（示例数据，见 image-prompt-hub/SKILL.md）
cd image-prompt-hub/scripts
python3 search_demo.py "小红书 护肤 极简"
```

## 📦 目录结构

```
longsen-prompt-tools/
├── video-prompt-reverse/
│   ├── SKILL.md              # 技能文档（方法论+工作流）
│   ├── references/           # 分镜表模板 / 失败模式清单 / 底座索引
│   ├── scripts/              # 4 步工具链 + 一键入口
│   └── examples/             # 示例输出
├── image-prompt-hub/
│   ├── SKILL.md              # 技能文档（分类体系+检索）
│   ├── scripts/              # 检索 demo
│   └── examples/             # 示例提示词
└── LICENSE                   # MIT
```

## 🧠 方法论文档

- `video-prompt-reverse/references/ai-storyboard-template.md` —— AI 生成向分镜表模板（12 字段）
- `video-prompt-reverse/references/失败模式清单.md` —— 视频生成失败模式 12 项 + 修复动作
- 10 段式输出规范见各 SKILL.md

## 🔒 完整版入口（数据底座）

开源版提供**方法 + 示例数据**。完整版包含：

- **21,719 条图片提示词数据底座**（14 个数据源，8 场景分类）
- **135 条行业视频案例库**（完整 prompt + 元数据）
- **7 个精选包**（小红书/抖音/淘宝/海报/人像写真/3D手作/手绘风格，各 200 条+）
- **工作台模块**（检索/解锁/出图引导，私有化部署）

> 获取完整版：关注隆森AI · 工作台接入 / 精选包购买（39.9 单包 / 59.9 全库买断+更新）

## 📄 许可证

MIT —— 可商用、可修改、可再分发（保留版权声明）。
方法论继承的各底座项目版权归原作者所有（见 video-prompt-reverse/references/底座索引.md）。

## 📮 联系

- GitHub Issues 提交反馈
- 商务合作 / 完整版授权：隆森AI

---

**隆森AI · 让 AI 提示词成为可复用资产**
