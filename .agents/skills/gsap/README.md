# OpenMontage 中的 GSAP 技能

> **范围：** 此目录没有 `SKILL.md` — 它**不是**一个可加载的技能。此文件是八个可加载的 `gsap-*` 技能的导航地图，这些技能位于同级目录中（`gsap-core`、`gsap-timeline` 等）。阅读它以找到正确的 `gsap-*` 技能；代理加载的是那些技能，而非此 README。

八个第 3 层技能，教导代理正确使用 GSAP（GreenSock 动画平台）。来源于 [greensock/gsap-skills](https://github.com/greensock/gsap-skills)，MIT 许可。

## 为什么 GSAP 在这个仓库中

OpenMontage 目前不直接使用 GSAP — Remotion 合成由 `useCurrentFrame()` + `interpolate()` + `spring()` 驱动。GSAP 在以下两个具体场景中变得相关：

1. **Remotion 组件内的高级文本 / SVG / 运动路径动画。** GSAP 的插件家族（SplitText、MorphSVG、DrawSVG、MotionPath、CustomEase）解决了使用原始 `interpolate()` 调用手工实现时很麻烦的问题。当你需要逐字揭示、SVG 上的弯曲相机路径或两个任意形状之间的变形时 — 使用 GSAP。
2. **HyperFrames 合成。** HyperFrames 是 OpenMontage 中的一个生产合成运行时（通过 `hyperframes_compose` 渲染；参见 `skills/core/hyperframes.md` 和 `AGENT_GUIDE.md`）。GSAP 通过 Frame Adapter 模式成为其原生动画运行时 — 时间线被暂停并注册在 `window.__timelines` 上，引擎逐帧寻找它们。GSAP 时间线创作是 HyperFrames 场景的基础技能。

## 何时阅读哪个

| 你正在做… | 首先阅读 |
|---|---|
| 任何 GSAP 动画，从零开始 | [`gsap-core`](../gsap-core/SKILL.md) |
| 多步骤序列或编排 | [`gsap-timeline`](../gsap-timeline/SKILL.md) |
| 逐词或逐字文本动画 | [`gsap-plugins`](../gsap-plugins/SKILL.md)（SplitText 部分） |
| SVG 形状变形 | [`gsap-plugins`](../gsap-plugins/SKILL.md)（MorphSVG 部分） |
| 对象沿曲线路径运动 | [`gsap-plugins`](../gsap-plugins/SKILL.md)（MotionPath 部分） |
| 自定义贝塞尔缓动 | [`gsap-plugins`](../gsap-plugins/SKILL.md)（CustomEase 部分） |
| React 组件内的 GSAP（Remotion） | [`gsap-react`](../gsap-react/SKILL.md) |
| 数学工具（clamp、mapRange、interpolate、random） | [`gsap-utils`](../gsap-utils/SKILL.md) |
| 调试慢动画 | [`gsap-performance`](../gsap-performance/SKILL.md) |
| 滚动驱动动画（仅 Web 预览，非视频渲染） | [`gsap-scrolltrigger`](../gsap-scrolltrigger/SKILL.md) |
| Vue / Svelte / 非 React 宿主 | [`gsap-frameworks`](../gsap-frameworks/SKILL.md) |

## 如何从第 2 层发现这些

这些技能不会自动触发。触发点：

- **`skills/meta/animation-runtime-selector.md`** — 调度元技能。在创作任何动画场景时，先阅读此文件；它会根据你需要的运动类型将你路由到正确的第 3 层技能。
- **管线资源导演技能** — `animated-explainer`、`animation` 和 `cinematic` 管线在适用时引用这些技能（文本用 SplitText、标志用 MorphSVG、相机运动用 MotionPath）。
- **`hyperframes_compose` 工具** — 声明 `agent_skills: ["gsap-timeline", "gsap-core"]`，以便代理在创作 HyperFrames 合成之前自动阅读它们。

## 在 Remotion 内确定性运行 GSAP

标准 GSAP 通过 `requestAnimationFrame` 驱动动画 — 非确定性，不兼容 Remotion。要在 Remotion 组件中使用 GSAP：

- **在创建时暂停时间线**：`const tl = gsap.timeline({ paused: true })`
- **通过 `useCurrentFrame()` 驱动进度**：`tl.progress(frame / durationInFrames)`
- 或**按时间寻找**：`tl.seek(frame / fps)` 到特定点
- 或**仅将 GSAP 用作值计算器** — 通过 `gsap.parseEase(...)` 和 `gsap.utils.interpolate(...)` 调用补间数学，无需运行实际动画循环

这是 HyperFrames 内部使用的模式。在 Remotion 内部，简单情况优先使用原生 `interpolate()`；在特别需要 SplitText / MorphSVG / MotionPath / CustomEase 时使用 GSAP。

## 归属

来源：https://github.com/greensock/gsap-skills
许可：MIT
复制日期：2026-04-16（提交 `{{source_commit}}` — 查看上游获取最新版本）
