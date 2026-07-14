# 动画运行时选择器

元技能回答两个问题：

1. **这个视频应该使用哪个合成运行时？** — Remotion、HyperFrames 或 FFmpeg。
2. **这个场景应该使用哪个动画库/第 3 层技能？** — Remotion 原语、GSAP 插件、framer-motion、Lottie、Manim、D3。

在编写任何动画组件或合成之前，以及在提案时选择 `render_runtime` 时，请阅读本技能。它会将你引导到正确的第 3 层技能，这样你就不会浪费时间去手工实现一个插件已经解决的问题。

> **创作模式优先。** 在运行时或库之前，首先要决定合成是如何构建的：**模板化**（组装库存 `cut.type` 场景）**vs 工作室**（从头开始手工编写）。英雄作品默认为工作室模式，并遵循 `skills/meta/bespoke-composition.md`。下面的路由在任一模式下都适用——但在工作室模式下，库存场景类型和注册表块是禁止使用的；你要自己编写。"是否有库存 cut-type 适合？"**不是**英雄作品的有效捷径。见 `AGENT_GUIDE.md` → "Composition Authoring Mode"。

## 何时使用本技能

适用于以下情况：
- **提案阶段**需要锁定 `render_runtime`（remotion / hyperframes / ffmpeg）
- 阶段指导（asset、edit、compose）需要编写动画组件
- agent 即将为涉及文字展示、SVG 运动、曲线镜头路径、形状变形或多阶段编排的场景编写 Remotion JSX
- agent 被要求构建 HyperFrames 合成
- agent 不确定是使用 GSAP 插件还是内联 `interpolate()`/`spring()`

## 运行时选择（Remotion vs HyperFrames vs FFmpeg）

OpenMontage 分离创意语法（`renderer_family`）和技术引擎（`render_runtime`）。两者都在提案时锁定，并在 `edit_decisions` 中保持不变。在合成时无声交换运行时是合约违规。

### 硬性规则——呈现两个运行时，不要无声默认

当机器上 Remotion 和 HyperFrames 都可用时（检查 `video_compose.get_info()["render_engines"]`），agent **必须**在锁定 `render_runtime` 之前向用户呈现两个选项。下面的决策矩阵是 agent 对话的输入，**不是**默默选择"默认"条目的许可证。见 `AGENT_GUIDE.md` → "Present Both Composition Runtimes" 了解完整合约。

具体来说，在提案阶段：

1. 查询 `video_compose.get_info()["render_engines"]` 以确定该机器上哪些运行时可用。
2. 如果 Remotion 和 HyperFrames 都可用，向用户呈现两者：一行针对需求定制的描述、一行诚实的权衡、agent 的推荐及理由。
3. 等待用户明确批准。
4. 在 `decision_log` 中记录决策，类别为 `render_runtime_selection`，两个运行时都在 `options_considered` 中。
5. 然后才将 `render_runtime` 写入 `proposal_packet.production_plan`。

当两者都可用时，只考虑了一个选项的 `render_runtime_selection` 决策是审查者的关键发现。

| 需求特征 | `render_runtime` | 阅读 |
|---|---|---|
| 现有 React 场景栈（text_card、stat_card、chart、caption overlay、TalkingHead、CinematicRenderer） | **remotion** | `skills/core/remotion.md` |
| 逐词字幕烧录 / 卡拉 OK 字幕 | **remotion** | `skills/core/remotion.md` |
| 虚拟形象 / 唇形同步 / 主持人 | **remotion** | `skills/core/remotion.md` |
| 动态排版、HTML/GSAP 原生运动、产品推广、发布短片 | **hyperframes** | `skills/core/hyperframes.md` + `.agents/skills/hyperframes/SKILL.md`（路由器）→ `hyperframes-core`（合约）、`hyperframes-creative`（调色板/字体）、`hyperframes-animation`（运动） |
| 网站 → 视频、UI 驱动的合成 | **hyperframes** | `.agents/skills/website-to-video/SKILL.md`（0.7 版本从 website-to-hyperframes 重命名） |
| 需要注册表块（数据图表、纹理叠加、着色器过渡等） | **hyperframes** | `.agents/skills/hyperframes-registry/SKILL.md` |
| 节拍同步音乐视频（音频驱动场景时间） | **hyperframes** | `.agents/skills/music-to-video/SKILL.md` — 使用 `hyperframes beats` 检测节奏点，在节拍网格上布局帧 |
| 将现有 Remotion 合成移植到 HyperFrames | **hyperframes** | `.agents/skills/remotion-to-hyperframes/SKILL.md` — 迁移指南，仅针对明确的移植请求 |
| BGM / SFX / 图像 / 图标解析（任何流水线、任何运行时） | 不适用 | `.agents/skills/media-use/SKILL.md` — 针对项目缓存 + 全局缓存 + HeyGen 目录执行 `resolve` 动词 |
| 短篇设计主导的动态图形（下三分之一、统计数据展示、标志 sting、标题） | **hyperframes** | `.agents/skills/motion-graphics/SKILL.md` |
| 纯拼接/裁剪源剪辑，无需合成 | **ffmpeg** | `skills/core/ffmpeg.md` |
| 所选运行时不可用 | **上报** — 不要无声替换 | `AGENT_GUIDE.md` → Escalate Blockers |

阅读 `skills/core/hyperframes.md` 了解完整的 Remotion-vs-HyperFrames 决策矩阵以及第 1 阶段保持 Remotion 独占的功能列表。

## 动画库决策矩阵

| 动画需求 | 推荐运行时 | 首先阅读 |
|---|---|---|
| 简单淡入淡出 / 滑动 / 缩放 / 弹簧 | Remotion 原语（无需插件） | `.agents/skills/remotion` |
| 带物理效果的双状态弹簧 | Remotion `spring()` | `.agents/skills/remotion` |
| 带偏移的多步序列 | Remotion `Sequence` + `interpolate()` **或** GSAP 时间线 | `.agents/skills/remotion` + 可选的 `.agents/skills/gsap-timeline` |
| 与旁白同步的逐词文字展示 | Remotion `interpolate` 由逐词字幕驱动（现有 `CaptionOverlay` 模式） | `.agents/skills/remotion` |
| 逐字符动态排版（SplitText 风格） | Remotion 内的 GSAP SplitText | `.agents/skills/gsap-plugins` (SplitText)、`.agents/skills/gsap-react` |
| 两条路径之间的 SVG 形状变形 | Remotion 内的 GSAP MorphSVG | `.agents/skills/gsap-plugins` (MorphSVG) |
| 沿自定义路径的曲线镜头/物体运动 | Remotion 内的 GSAP MotionPath | `.agents/skills/gsap-plugins` (MotionPath) |
| SVG 线条绘制 / 描边展示 | GSAP DrawSVG | `.agents/skills/gsap-plugins` (DrawSVG) |
| 定制贝塞尔 / 弹性 / 卡顿缓动 | GSAP CustomEase / EasePack / CustomWiggle | `.agents/skills/gsap-plugins` |
| 布局到布局过渡（FLIP） | Remotion 内的 GSAP Flip | `.agents/skills/gsap-plugins` (Flip) |
| 迪士尼 12 个动画原则用于 UI 运动 | framer-motion + Lottie | `.agents/skills/framer-motion`、`.agents/skills/lottie-bodymovin` |
| 从 After Effects / Figma 导出 Lottie | Lottie | `.agents/skills/lottie-bodymovin` |
| 合成终端 / CLI 演示 | Remotion TerminalScene | `.agents/skills/synthetic-screen-recording` |
| 数学 / 科学可视化 | Manim | `.agents/skills/manim-composer`、`.agents/skills/manimce-best-practices` |
| D3 数据驱动可视化 | D3 | `.agents/skills/d3-viz` |
| 数据图表（柱状/折线/饼图/KPI） | Remotion 内置图表组件 | `remotion-composer/SCENE_TYPES.md` |
| HyperFrames 合成——动画知识（规则、蓝图、过渡、运行时适配器） | HyperFrames + GSAP 默认 | `.agents/skills/hyperframes-animation`（整合的运动技能）+ `.agents/skills/gsap-core`、`.agents/skills/gsap-timeline` |
| HyperFrames 合成结构（data-* 时间、轨道、子合成） | HyperFrames | `.agents/skills/hyperframes-core` |
| HyperFrames 创意方向（调色板、字体、旁白、节拍规划） | HyperFrames | `.agents/skills/hyperframes-creative` |
| HyperFrames 音频/媒体（TTS、BGM、SFX、转录、字幕、背景移除） | HyperFrames | `.agents/skills/hyperframes-media` |
| HyperFrames 合成 CLI 工作（lint/validate/inspect/snapshot/benchmark/render/lambda） | HyperFrames CLI 0.7+ | `.agents/skills/hyperframes-cli` |
| HyperFrames 注册表块安装（`hyperframes add ...`） | HyperFrames 注册表 | `.agents/skills/hyperframes-registry` |

## "保持简单"的偏向

在使用 GSAP 之前，先问：**Remotion 的原生 API 能否在 ≤ 20 行内解决这个问题？**

- 淡入淡出/滑动/缩放/旋转 → `interpolate(frame, [inFrame, outFrame], [from, to])`
- 自然的"弹跳"运动 → `spring({ frame, fps, config: { damping, stiffness } })`
- 逐词字幕高亮 → 遍历 transcript，按 `frame / fps` 过滤

如果能，使用 Remotion 原语。如果不能，那就是你升级到 GSAP 插件的信号。

GSAP 是一个强大的逃生口，而不是默认选择。每个插件都会增加包体积、注册样板代码和另一个需要阅读的技能。

## 在 Remotion 内确定性运行 GSAP

标准 GSAP 在 `requestAnimationFrame` 上运行——不是确定性的，不能直接与 Remotion 兼容。以下是三种**确实** Remotion 安全的模式：

```jsx
// 模式 1：暂停的时间线，按进度 seek
const tl = useRef(gsap.timeline({ paused: true })).current;
useEffect(() => {
  tl.to('.x', { x: 500 }).to('.y', { opacity: 0 });
}, []);
tl.progress(frame / durationInFrames);

// 模式 2：暂停的时间线，按时间 seek
tl.seek(frame / fps);

// 模式 3：仅将 GSAP 作为值计算器
const easeFn = gsap.parseEase('power2.out');
const t = frame / durationInFrames;
const easedValue = easeFn(t);
```

完整说明请阅读 `.agents/skills/gsap-react/SKILL.md`。

## 对照流水线的阶段指导进行检查

每个流水线的资产指导都有动画特定的指南。如果你在：
- **animated-explainer** → 阅读 `skills/pipelines/explainer/asset-director.md`——它引用了用于动态排版的文字/SVG 选项
- **animation** → 阅读 `skills/pipelines/animation/asset-director.md`——它引用了用于标志/动态图形工作的 MorphSVG 和 MotionPath
- **cinematic** → 阅读 `skills/pipelines/cinematic/asset-director.md`——它引用了用于电影级镜头运动的 MotionPath

资产指导告诉你*在这个流水线上下文中*构建什么。本选择器告诉你*如何*构建。

## 绝对不要做

- ❌ 在只需要淡入淡出/滑动的场景中使用 GSAP ——使用 Remotion 原语。
- ❌ 在 Remotion 内使用带 `requestAnimationFrame` 的 GSAP ——渲染将是非确定性的。
- ❌ 当指示使用插件时跳过阅读匹配的第 3 层技能——每个插件的提示指导都很重要。
- ❌ 在组件体内注册 GSAP 插件——在模块范围或应用入口处注册一次。
