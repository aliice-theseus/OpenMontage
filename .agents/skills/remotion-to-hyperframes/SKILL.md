---
name: remotion-to-hyperframes
description: '将现有的 Remotion (React) 合成移植到 HyperFrames HTML。仅在用户明确要求移植/转换/迁移/翻译 Remotion 源码时使用。不要用于：(a) 编写新的 HyperFrames 合成；(b) 顺带提及 Remotion；(c) 仅作为参考分享的 Remotion 代码；(d) "和我 Remotion 一样的视频"但没有明确要求迁移源码 — 视为新建。有疑问 → `/general-video`。单向，仅 Remotion：不支持反向导出（HyperFrames→Remotion 或任何其他框架），非 Remotion 源码（After Effects, Framer Motion, 纯 React/CSS）→ 超出范围，通过 `/general-video` 重建。标记不支持的模式（useState, useEffect, async calculateMetadata, 第三方 React 库, `@remotion/lambda`）并推荐运行时互操作而非有损翻译。不确定是移植还是新建，或只是顺带提及 Remotion？→ /hyperframes。'
---

# Remotion 到 HyperFrames

> **在开始构建之前确认路线。** 仅使用此技能将现有的 **Remotion** (React) 合成源码移植到 HyperFrames。编写 **新** 合成（即使灵感来自 Remotion 视频）→ 使用创作工作流 `/general-video`。**超出范围**（单向，仅 Remotion）：不支持反向导出（HyperFrames → Remotion 或任何其他框架），且 **非 Remotion** 源码（After Effects, Framer Motion, 纯 React/CSS）没有可翻译的 Remotion 源码 → 通过 `/general-video` 重建。不确定，或只是顺带提及 Remotion？**先阅读 `/hyperframes`。**

## 概述

将 Remotion（基于 React）视频合成分解为 HyperFrames（HTML + GSAP）合成。大多数 Remotion 惯用用法都有直接的 HyperFrames 对应物 — 对于约 80% 的典型合成，翻译是机械性的。此技能编码了映射关系，并通过拒绝翻译不适合 HF 基于 seek 模型的模式，以及推荐来自 [PR #214](https://github.com/heygen-com/hyperframes/pull/214) 的运行时互操作模式，来防范那 20% 的有损部分。

该技能附带一个 **分层测试语料库**（T1–T4，共 4 个测试用例），根据测量的 SSIM 阈值对翻译进行评分。不要在不运行评估的情况下进行翻译 — 一个"看起来正确"但渲染结果比已验证基线低 0.05 SSIM 的翻译是静默错误的。

## 何时使用

**仅在用户明确要求从 Remotion 迁移时使用此技能。** 示例触发短语：

- "将我的 Remotion 项目移植到 HyperFrames"
- "将此 Remotion 代码转换为 HyperFrames"
- "从 Remotion 迁移"
- "翻译此 Remotion 合成"
- "将其重写为 HyperFrames HTML"

**在以下情况下不要使用此技能：**

- (a) 用户正在编写一个 **新** 的 HyperFrames 合成，即使他们有或正在 A/B 测试类似的 Remotion 视频。
- (b) 用户顺带提及 Remotion 而没有要求迁移。
- (c) 用户分享 Remotion 代码作为参考材料，而不是要求翻译。
- (d) 用户要求"和我 Remotion 一样的视频"但没有明确要求迁移源码 — 视为新的 HyperFrames 构建。

**不支持（拒绝 — 这不是此技能的职责）：**

- **反向方向。** 将 HyperFrames 合成导出回 _到_ Remotion（或任何其他框架）不是一个工作流 — 翻译只能是 Remotion → HyperFrames。直说即可。
- **非 Remotion 源码。** After Effects 项目（`.aep`）、Framer Motion / 纯 React / CSS 动画或任何其他工具的源码不是 Remotion 合成 — 没有可翻译的 Remotion 源码。通过 `/general-video` 原生重建，如果 HyperFrames 无法表示则拒绝。

如有疑问，默认使用 `/general-video`（通用 HyperFrames 创作流程）编写原生 HyperFrames 合成。

## 工作流

### 步骤 1：检查源码

对 Remotion 源码目录运行 [`scripts/lint_source.py`](scripts/lint_source.py)。该检查工具检测无法干净翻译的模式：

- **阻断器**（拒绝 + 推荐互操作）：`useState`、`useReducer`、带非空依赖的 `useEffect`/`useLayoutEffect`、异步 `calculateMetadata`、第三方 React UI 库（MUI、Chakra、Mantine、antd、shadcn、Radix、NextUI）。
- **警告**（丢弃结构后翻译）：`@remotion/lambda` 配置、`delayRender`、`useCallback`、`useMemo`、自定义 hooks。
- **信息**（带注释翻译）：`staticFile`、`interpolateColors`。

如果触发了任何阻断器，**停止**。阅读 [`references/escape-hatch.md`](references/escape-hatch.md) 并提供建议消息。警告不会停止翻译 — 在步骤 3 中丢弃有问题的结构并在 `TRANSLATION_NOTES.md` 中记录差距。`@remotion/lambda` 配置是典型的警告案例：该技能丢弃 import + `renderMediaOnLambda(...)` 调用，但翻译合成的其余部分。

### 步骤 2：规划翻译

阅读 [`references/api-map.md`](references/api-map.md) — 每个 Remotion API 及其 HF 等价物或按主题分类的参考索引。根据源码使用的内容确定需要哪些主题参考：

| 源码包含                                                               | 加载参考                                    |
| ------------------------------------------------------------------------- | --------------------------------------------- |
| `Composition`、`defaultProps`、`schema`、`calculateMetadata`              | [`parameters.md`](references/parameters.md)   |
| `Sequence`、`Series`、`Loop`、`AbsoluteFill`、`Freeze`                    | [`sequencing.md`](references/sequencing.md)   |
| `useCurrentFrame`、`interpolate`、`spring`、`Easing`、`interpolateColors` | [`timing.md`](references/timing.md)           |
| `Audio`、`Video`、`Img`、`IFrame`、`staticFile`、`delayRender`            | [`media.md`](references/media.md)             |
| `TransitionSeries`、`@remotion/transitions`                               | [`transitions.md`](references/transitions.md) |
| `@remotion/lottie`                                                        | [`lottie.md`](references/lottie.md)           |
| `@remotion/google-fonts/<Family>`、`Font.loadFont`、`@font-face`          | [`fonts.md`](references/fonts.md)             |

不要全部加载 — 只加载特定源码需要的内容。

### 步骤 3：生成 HF 合成

生成 `index.html`，包含：

- 根 `<div id="stage">`，带上合成的 `data-composition-id`、`data-start="0"`、`data-duration`（秒）、`data-fps`、`data-width`、`data-height`，每个标量 prop 对应一个 `data-*`。
- 场景 div 的平面列表，带有 `data-start` / `data-duration` / `data-track-index`。
- 内联 `<style>` 用于布局；CSS 设置每个动画属性的 `from` 状态。
- 底部的一个 `<script>` 标签，包含一个暂停的 `gsap.timeline({paused: true})`。每个 Remotion `useCurrentFrame()` 推导都成为此时间线上正确偏移处的补间动画。
- `window.__timelines["<composition-id>"] = tl;` 将时间线注册到 HF 的运行时。

自定义 React 子组件作为重复 HTML 内联，使用 prop 接口作为模板（参见 [`parameters.md`](references/parameters.md) 了解每个实例的 `data-*` 模式）。

### 步骤 4：验证

运行评估框架 — 完整指南见 [`references/eval.md`](references/eval.md)。快速路径：

```bash
# 渲染 Remotion 基线（在测试用例中运行 npm install 后）
cd remotion-src && npx remotion render <CompositionId> out/baseline.mp4

# 渲染 HF 翻译
cd ../hf-src && npx hyperframes render --skill=remotion-to-hyperframes --output ../hf.mp4

# SSIM 差异比较
../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```

阈值：约低于源码复杂度层级 `p05` 的 ~0.02（参见 `eval.md` 的已验证阈值表）。如果差异比较失败，运行 [`scripts/frame_strip.sh`](scripts/frame_strip.sh) 查看 _哪些_ 帧产生了差异，然后重新阅读相关的时间/序列/媒体参考。

**关键**：两个渲染必须使用匹配的像素格式。在 Remotion 源码的 `remotion.config.ts` 中设置 `Config.setVideoImageFormat("png")` + `Config.setColorSpace("bt709")` — 否则差异比较会测量编码器差异（约 0.05 SSIM 损失），而非翻译保真度。

### 步骤 5：记录差距

任何未能干净翻译的内容（音量渐变被丢弃、自定义演示被近似、字体被替换）都会在 HF 输出旁边生成 `TRANSLATION_NOTES.md`。格式参见 [`references/limitations.md`](references/limitations.md)。

## 此技能明确不做的事

- **翻译 React 状态机。** 通过 `useState` + `useEffect` 驱动动画的合成在 HyperFrames 基于 seek 的模型中不是确定性的帧捕获目标。建议使用运行时互操作模式。
- **在 HyperFrames 旁边运行 Remotion 的渲染管线。** 这是来自 [PR #214](https://github.com/heygen-com/hyperframes/pull/214) 的运行时互操作模式 — 一个针对未通过此技能检查的合成的单独解决方案。

（`@remotion/lambda` _不是_ 阻断器 — Lambda 配置是部署，不是动画。该技能将其作为警告丢弃并翻译其余部分。参见 [`references/escape-hatch.md`](references/escape-hatch.md)。）

## 如何评估自己的翻译

运行测试语料库协调器：

```bash
./assets/test-corpus/run.sh
```

它运行 T1、T2、T3（渲染 + 差异比较）和 T4（检查验证），打印每层级的通过/失败表格，并输出聚合 JSON 报告。使用此方法验证技能在干净检出时是否端到端正常工作 — 以及在编辑任何参考后作为回归检查。

已验证基线（截至 2026-04-27）：

| 层级 | 合成形状                               | 平均 SSIM | 阈值    |
| ---- | ------------------------------------------- | --------- | --------- |
| T1   | 单元素淡入                                  | 0.974     | 0.95      |
| T2   | 多场景 + spring + 音频 + 图片               | 0.985     | 0.95      |
| T3   | 数据驱动、自定义子组件、计数动画              | 0.953     | 0.90      |
| T4   | 逃生舱（8 个检查用例）                      | 8/8 通过  | 不适用    |
