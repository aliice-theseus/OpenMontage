---
name: hyperframes-core
description: HyperFrames 合成契约 — 构建一个可渲染的项目。用于合成结构、`data-*` 时间属性、`class="clip"`、轨道、子合成、变量、框架拥有的媒体播放、确定性渲染规则和验证。在编写合成 HTML 之前阅读。
---

# HyperFrames 核心

HyperFrames 从 HTML 渲染视频。合成是一个 HTML 文件，其 DOM 使用 `data-*` 属性声明时间，其动画运行时是可定位的，其媒体播放由框架拥有。

此技能是**技术契约** — 如何构建一个 hyperframes 项目。以下正文是构建指南；每个主题的细节在 `references/` 中（索引如下），按需阅读。其他关注点在同级领域技能中 — `hyperframes-animation`、`hyperframes-creative`、`hyperframes-media`、`hyperframes-cli`、`hyperframes-registry`。`/hyperframes` 中的能力映射说明了每个技能涵盖的内容。

## 参考

| 文件                                  | 阅读以…                                                                                   |
| ------------------------------------ | ----------------------------------------------------------------------------------------- |
| `references/minimal-composition.md`  | 从最小的可渲染合成骨架开始                                                                  |
| `references/composition-patterns.md` | 选择整体式与模块化；组织模块化 `index.html`；选择子合成原型                                  |
| `references/data-attributes.md`      | 查找任何 `data-*`（根/剪辑/子合成宿主/旧别名）；使用 `class="clip"`                         |
| `references/tracks-and-clips.md`     | 选择 `data-track-index`，处理同轨道重叠/z-index，相对于另一个剪辑计时                        |
| `references/sub-compositions.md`     | 连接子合成（宿主属性、`<template>`、实例变量）并在其中执行动画                               |
| `references/variables-and-media.md`  | 声明变量；放置 `<video>`/`<audio>`、设置音量、修剪                                          |
| `references/determinism-rules.md`    | 构建可定位的时间线；确定性禁止规则；可动画属性白名单；布局/文本适配                           |
| `references/full-screen-motion.md`   | 使用共享背景创作全帧动画                                                                    |
| `references/storyboard-format.md`    | 创作 `STORYBOARD.md` 计划（+ 解析后的清单）                                                 |
| `references/script-format.md`        | 创作可选的 `SCRIPT.md` 锁定旁白                                                            |
| `references/subagent-dispatch.md`    | 将子代理调度动词（并行展开/后台/等待）映射到你的框架                                         |
| `references/tailwind.md`             | 在 Tailwind v4 项目中工作（`init --tailwind`；与 Studio 的 v3 运行时契约不同）               |

关于动画运行时细节（GSAP API、Lottie、Three.js 等），请查看 `hyperframes-animation` → `adapters/<runtime>.md`。

## 构建合成

### 两种根形式（不可互换）

- **独立**（顶层 `index.html`）— 根 `<div data-composition-id="…">` 直接放在 `<body>` 中，**无 `<template>` 包装器**（包装它会隐藏所有内容并破坏渲染）。
- **子合成**（通过 `data-composition-src` 加载）— 根**必须**包装在 `<template>` 中。

> ⚠ 传输规则：运行时**仅克隆 `<template>` 内容**；外部的一切（包括 `<head>` 样式/脚本）都被丢弃 — 将 `<style>`/`<script>` 放在模板**内部**。
> ⚠ 宿主 ID 规则：宿主插槽的 `data-composition-id` 必须**完全等于**内部模板的 `data-composition-id` **以及** `window.__timelines["<id>"]` 键 — 不允许有 `-mount`/`-slot`/`-host` 后缀。

文件形状、宿主连接和渲染前检查清单 → `references/sub-compositions.md`。

### 根必须有尺寸（静默布局错误）

独立根需要一个显式的**尺寸框**（`width`/`height` 以像素为单位），并且到 `height:100%` 元素的每个祖先都必须有解析的高度 — 否则 flex/`100%` 子元素会塌缩到 ~0，内容堆积到左上角。`lint`/`validate`/`inspect` 不会捕获此问题。骨架 → `references/minimal-composition.md`。

### 一个暂停的时间线

每个合成在 `window.__timelines["<id>"]`（键 = 根 `data-composition-id`）处注册**恰好一个** `gsap.timeline({ paused: true })`，在页面加载时**同步**构建。渲染时长 = 根 `data-duration`，而非时间线长度。不要手动将子时间线嵌套到宿主中。完整契约（包括非 GSAP 运行时）→ `references/determinism-rules.md` + `hyperframes-animation/adapters/`。

### 不可协商的规则（`lint`/`validate`/`inspect` 不会捕获的静默错误）

在此列出；完整原理在链接的参考中。不要违反：

- 无运行时时钟 / 未播种的 `Math.random` / 网络 / 输入状态；无 `repeat: -1`（使用有限计数）。→ `determinism-rules.md`
- 仅动画化视觉属性白名单；永远不要 `display`/`visibility`；不在后期场景剪辑上使用 `gsap.set`。→ `determinism-rules.md`
- 正文中没有 `<br>`；变换后的元素必须是块级+有尺寸；脉冲式绝对定位装饰元素需要峰值间距。→ `determinism-rules.md`
- `<video>`/`<audio>` 必须是宿主根的**直接子元素**（决不能放在子合成 `<template>`/包装器内部）；框架拥有播放控制。→ `variables-and-media.md`
- 每个 `id` 必须在**组装后的**页面中唯一；在子合成内部，使用合成 ID 作为 id 前缀（`#<id>-hero`）。重复的 `<video>`/`<img>` id 会渲染为**空白** — 生产者通过 `getElementById` 注入帧，跨文件重复会绕过 `lint`。→ `composition-patterns.md`
- 全屏场景填充应放在全出血的**子元素**上（`position:absolute; inset:0`），决不能放在合成本身上 — 生产者的帧合成可能会丢弃根元素自身的 `background`（帧渲染为**黑色**），即使预览/`snapshot` 显示正确。→ `composition-patterns.md`

## 编辑现有合成

- 先阅读文件。保留不相关的时间、轨道、ID、变量、媒体路径。
- 匹配现有的合成 ID 和时间线键。
- 添加剪辑：选择不重叠的 `data-track-index` 或有意识地调整周围时间。
- 添加子合成：在连接宿主之前验证其内部 `data-composition-id`。

## 验证

使用 `hyperframes-cli` 获取命令详情

- [ ] `npx hyperframes lint` 通过（0 错误）
- [ ] `npx hyperframes validate` 通过（0 控制台错误）
- [ ] `npx hyperframes inspect` 通过（0 错误）
- [ ] 带子合成的项目：`npx hyperframes snapshot --at <midpoints>` 并目视检查每个帧
- [ ] `npx hyperframes preview` 用于审查（用户可以在 Studio 的时间线中编辑任何内容）
- [ ] 仅当用户批准后运行 `npx hyperframes render`
