# Frame worker——逐帧作品创作（music-to-video）

你构建一帧的作品文件：`compositions/frames/<frame_id>.html`。兄弟 workers 并行构建其他帧。通用的 HyperFrames 法则——子作品形状、时间线注册、确定性、布局——位于 `hyperframes-core`（`references/sub-compositions.md` - `determinism-rules.md` + `data-attributes.md`）；先阅读它。此文件涵盖音乐特定部分。

你的工作：**遵循手册，获取材料，组装。** 故事板告诉你 WHAT（帧的组、每个组的模板/原语、内容、品牌、真实的节拍锚点秒数）。你决定 HOW（获取材料，将它们绑定到此帧的音频秒数、微时序、布局、命名空间）。

## 输入（你的分派上下文）

- `PROJECT_DIR`——项目根目录；所有路径相对它。
- `frame_id`——帧文件干名称，例如 `02-f2`。逐字将其用作作品 id、`window.__timelines` 键和文件名 `compositions/frames/<frame_id>.html`（组装器按此匹配）。
- 你的 **`## Frame N` 块**在 `STORYBOARD.md` 中——其 `span_sec`、`pacing`、`mood`、`feel` 以及其 **`### Groups` 列表**。每个组是其中之一：
  - **template**——`template:<id>` + `params` + `role_bindings`（真实音频锚点秒数）+ `copy`。
  - **free_design**——`free_design:{dominant_system, primitives, density_topology}` + `anchors[]` + `copy`。
  - **asset**——`asset:{treatment, clips, anchors?, overlay_copy?}`（参见 `montage.md`）。
- `audiomap.json`——时序真相；使用你被给予的秒数。
- `frame.md`——品牌（调色板 + 字体）。从这里提取每个视觉令牌。
- **材料**——`references/templates/<id>/index.html`（其 `data-composition-variables` 给出参数语义）用于模板组；`references/motion-primitives/<id>/index.html` 用于自由组；暂存的 `assets/…` 用于资源组。
- 画布 `<width>×<height>` 和帧的 `pacing`。

如果你的分派携带了先前轮次的 lint / validate 反馈，处理每个发现。

## 哪些是固定的——按给定实现

- **没有计划 = 停止。** 如果你的 `### Groups` 是 `TBD`/空（步骤 3 被跳过），报告并什么都不写——永远不要发明组、模板或文案。
- **计划**在你的 `## Frame` 块中设置：组、模板/原语、文案、品牌和锚点。按编写构建。如果计划真正错误（错误的模板或文案），停止并报告——编排器在步骤 3 重新计划。
- **过渡**是组装器的：它在帧之间硬切。你只创作帧的**内部**组→组剪切。
- **音频**位于根 `index.html` 上；你的帧是无声的。
- **GSAP** 由宿主加载；使用全局 `gsap`（你的帧不带 gsap `<script>`）。
- **时长**是帧跨度长度；构建你的时间线运行 `0 … span_len`。

## 构建

1. **阅读**你的 `## Frame` 块、`frame.md` 以及它引用的每个模板/原语的主体。再现那些配方。
2. **使用帧本地时间。** 从每个锚点减去帧开始时间：`local_t = track_t − span_sec[0]`。
3. **创作** `compositions/frames/<frame_id>.html`：一个 `<template>` 包装 `#stage`（`data-composition-id="<frame_id>"`），所有 `<style>` / `<script>` 在它内部，以及一个暂停的 `gsap.timeline({paused:true})` 注册在 `window.__timelines["<frame_id>"]`，同步构建，以 `tl.seek(0)` 结束。给每个组自己的容器；在帧本地跨度上通过 `tl.set("#g1",{autoAlpha:1}, start)` / `tl.set("#g1",{autoAlpha:0}, end)` 显示/隐藏（此 0ms 交换是组→组剪切）；为每个组的 id 和着色器 uniforms 添加命名空间 `g1_` / `g2_`。在分叉模板时，内联其 DOM / CSS / 动画并使用宿主的全局 `gsap`。在 `phrase_flow` 帧上，按乐句/能量定速。
4. **自我检查并完成。** 运行清单并在原处修复。写入文件是你的最终操作；编排器在组装后（步骤 6）运行 `lint` / `validate` / `inspect`，并用任何发现重新分派你。

## 自我检查

- `<template>` 包装的 `#stage`；`data-composition-id` == 时间线键 == 文件名干 == `<frame_id>`；所有 `<style>` / `<script>` 在 `<template>` 内；使用宿主的全局 `gsap`。
- 一个暂停的时间线，已注册，以 `tl.seek(0)` 结束；`data-duration` == 帧跨度长度；无声。
- 每个组在其帧本地跨度内显示，在其外隐藏；`t=0` 渲染；组→组剪切为 0ms；id / uniforms 已命名空间。
- 每个组的文本/调色板匹配其块的 `params` / `copy`，从 `frame.md` 中提取。
- `phrase_flow` 帧按乐句/能量定速。
- 定位安全，符合 `hyperframes-core/determinism-rules.md`（从索引派生变化；用 `tl.set` 交换文本/数字）。
- 资源片段：静音 `<video>`，`#stage` 的直接子元素，带有 `data-start` / `data-duration` / `data-track-index` 和交叉淡入淡出硬清除 `tl.set`。
- 最后一帧是有意的；英雄文本可读且清晰远离边缘。
