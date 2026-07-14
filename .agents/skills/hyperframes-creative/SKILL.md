---
name: hyperframes-creative
description: HyperFrames 视频的非动画创意方向。用于设计规范（frame.md / design.md）处理、调色板、排版、旁白、节拍规划、音频响应式视觉效果、构图模式以及品牌/风格决策。对于原子化运动模式和场景蓝图，请使用 `hyperframes-animation`。
---

# HyperFrames Creative

品牌、节奏、风格、旁白和构图方向。在 `hyperframes-core` 的技术合约就绪后使用。

对于运动模式、场景蓝图、过渡和 CSS 标记效果，请使用 `hyperframes-animation` — 此技能特意不涉及动画。

> **对于任何非平凡的合成，请先阅读以下两篇——它们会覆盖网页本能：**
>
> - `references/house-style.md` — "解释提示，生成真实内容"，惰性默认列表，以及前景/背景分层方案。这是将字面意义的样式重写转变为 _概念_ 的关键。
> - `references/video-composition.md` — 视频媒介密度、缩放、前景元数据（"制作而非生成"的细节：数据条、注册标记、等宽读数、每场景 8-10 个元素）。
>
> 跳过这两篇是产生通用、网页风格输出的最大原因。它们在下方的路由表中不是可选项——对于任何超过单行编辑的内容，在选择颜色或编写 HTML 之前，请先打开这两篇。

## 工作流程

1. 如果项目有设计规范，**先阅读它**，并将其 frontmatter 标记视为品牌真理（颜色、字体、间距、语气、约束）。要读取哪个文件（优先级 `frame.md` → `design.md` → `DESIGN.md`）以及如何解析（frontmatter = 规范性，prose = 上下文）在 [`references/design-spec.md`](references/design-spec.md) 中定义 — 按照该文档解析和加载。
2. 如果没有设计规范且用户要求视觉方向，选择一个路径：
   - 现成的帧预设（可选）→ `frame-presets/`（将 `FRAME.md` 作为 `frame.md` 采用；参见 `references/design-spec.md`）
   - 命名风格或情绪 → `references/visual-styles.md`
   - 快速默认 → `references/house-style.md`
   - 交互式选择 → `references/design-picker.md`
3. 对于多场景工作，在编写 HTML 之前规划节拍和节奏 → `references/beat-direction.md`。对于场景过渡，跳转到 `hyperframes-animation/transitions/`。
4. 对于运动密集型工作，阅读 `references/motion-principles.md`（高层护栏规则），然后转到 `hyperframes-animation` 获取原子化规则。

## 路由表

| 主题                                                                      | 阅读文件                                        |
| ------------------------------------------------------------------------ | ---------------------------------------------- |
| 采用现成的帧预设作为 `frame.md`（可选）                                   | `frame-presets/` · `references/design-spec.md` |
| 默认调色板、运动、排版、惰性默认值提问                                    | `references/house-style.md`                    |
| 命名风格预设、情绪到风格的路由                                            | `references/visual-styles.md`                  |
| 特定调色板的颜色标记                                                      | `palettes/*.md`                                |
| 构图模式 — 画中画、文字在主体后、标题卡、幻灯片                           | `references/composition-patterns.md`           |
| 统计数据/信息图展示                                                       | `references/data-in-motion.md`                 |
| 开放式提示的结构化扩展                                                    | `references/prompt-expansion.md`               |
| 视频媒介密度、缩放、颜色、画面构图                                        | `references/video-composition.md`              |
| 逐节拍方向、节奏规划、过渡时间                                            | `references/beat-direction.md`                 |
| 创作后规范验证（颜色、字体、圆角、间距、深度）                            | `references/design-adherence.md`               |
| 高层运动护栏规则和 GSAP 质量规则                                          | `references/motion-principles.md`              |
| 字体选择、搭配、渲染视频类型护栏规则                                      | `references/typography.md`                     |
| 脚本节奏、语气、开场、数字发音                                            | `references/narration.md`                      |
| 预计算的音频频段映射到运动                                                | `references/audio-reactive.md`                 |

## 脚本

- `scripts/contrast-report.mjs` — 检查渲染帧的对比度警告。
- `scripts/extract-audio-data.py` — 预提取音频频段，用于音频响应式合成。
- `scripts/package-loader.mjs` — 捆绑创意工具的支持脚本。

从仓库根目录使用显式路径运行，例如：

```bash
python skills/hyperframes-creative/scripts/extract-audio-data.py <audio-file>
```

动画分析（`animation-map.mjs`）位于 `hyperframes-animation/scripts/`。

## 边界

- 不要覆盖 `hyperframes-core` 的技术规则。
- 不要为最小技术合成要求设计系统。
- 除非请求需要或你先提出扩展，否则不要添加额外场景、旁白、音乐、字幕或过渡。
- 保持配方引用针对具体任务；不要为简单编辑阅读所有引用。
