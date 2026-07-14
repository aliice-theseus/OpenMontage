# 数据属性参考

每个 HyperFrames 合成都使用 `data-*` 属性向框架声明时间和结构。这是完整的属性表 — 配合 `tracks-and-clips.md` 了解 `data-track-index` 背后的规则。

## 合成根

每个可渲染的合成需要一个根元素：

| 属性                          | 必需 | 含义                                                                              |
| ---------------------------- | ---- | --------------------------------------------------------------------------------- |
| `data-composition-id`        | 是   | 唯一 ID。必须匹配 `window.__timelines` 上的动画注册键。                            |
| `data-width` / `data-height` | 是   | 像素帧尺寸。常见值：`1920x1080`、`1080x1920`、`1080x1080`。                       |
| `data-duration`              | 是   | 持续秒数。这是渲染时长，不是 GSAP 时间线长度。                                     |
| `data-fps`                   | 否   | 可选的帧率提示。CLI 渲染标志可以覆盖输出 fps。                                     |
| `data-composition-variables` | 否   | 变量声明的 JSON 数组（在 `<html>` 上）。参见 `variables-and-media.md`。             |

根元素应该是 `position: relative`，具有显式像素尺寸，并隐藏溢出，除非有意在帧外构图。

## 剪辑属性

定时子元素是剪辑。**可见定时元素需要 `class="clip"`**（`<div>`、`<img>` 等）— 没有它，运行时会保持元素在整个合成中可见，忽略 `data-start` / `data-duration`。在 `<video>`（框架直接管理可见性）和 `<audio>`（无视觉）上省略。

**剪辑必须是合成根的直接子元素。** 嵌套在包装器 `<div>` 内的剪辑不会被注册 — 最明显的是，包装器内的 `<video>` 永远不会被定位/解码，会渲染为黑色。要包装/变换剪辑，将包装器放在剪辑_内部_，或动画化剪辑元素本身；不要包装剪辑。（另外，`<video>`/`<audio>` 必须位于**宿主**根，绝不能放在子合成 `<template>` 中 — 参见 `variables-and-media.md`。）

| 属性                | 必需                                              | 含义                                                                                                     |
| ------------------ | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `id`               | 是                                                | 用于 lint 检查、时间线目标和调试的稳定 DOM ID。                                                           |
| `data-start`       | 是                                                | 以秒为单位的开始时间，或支持的剪辑时间引用。                                                              |
| `data-duration`    | `div`、`img` 和子合成必需                           | 持续秒数。视频/音频在已知时长时可以使用媒体时长作为默认值。                                                |
| `data-track-index` | 是                                                | 时间线轨道。同一轨道上的剪辑不得重叠。                                                                    |
| `data-media-start` | 否                                                | 进入媒体源的偏移量，以秒为单位。                                                                          |
| `data-volume`      | 否                                                | 静态音频音量，`0` 到 `1`，默认为 `1`。对于淡入淡出，在时间线上动画化 `volume`（参见 `variables-and-media.md`）。 |
| `data-has-audio`   | 否（仅 `<video>`）                                 | 当自动检测会遗漏时，声明视频带有音轨的 `"true"`。                                                         |

**可见窗口包含两端。** 当 `start ≤ t ≤ start + duration` 时剪辑可见 — 它在 `t = start + duration` 时仍然渲染，因此最后一帧保持动画的解析结束状态（运行时不会提前一帧隐藏它）。因此，在 `data-duration` 时完成的揭示/进入效果在最后一帧可见；你不需要仅仅为了确保结束状态渲染而在 `data-duration` _之前_完成它。（`/hyperframes-animation` 中的高潮停留指导是关于节奏的，而非此边界。）

## Sub-Composition Host Attributes

When a clip is a sub-composition host (loads another composition file):

| 属性                          | 必需 | 含义                                                                |
| ---------------------------- | -------- | ---------------------------------------------------------------------- |
| `data-composition-id`        | 是      | 加载文件的内部合成 ID。                        |
| `data-composition-src`       | 是      | 子合成 HTML 文件的路径。                                 |
| `data-width` / `data-height` | 是      | 子合成实例的渲染尺寸。                    |
| `data-variable-values`       | 否       | 按实例的变量覆盖，JSON 格式。参见 `variables-and-media.md`。 |

完整的接线模式请参见 `sub-compositions.md`。

## 创作提示

- `id="root"` — 脚手架和转场目录使用的模板约定，使 CSS 可以用 `#root` 而非 `[data-composition-id="main"]` 定位合成根。运行时不要求，但与生态系统其他部分保持一致。
- `class="clip"` — 可见计时元素（`<div>`、`<img>` 等）上必需的运行时可见性标记。参见上面的片段属性。
- `data-layout-allow-overflow` — 告知 `hyperframes inspect` 此元素（或其后代）上的溢出是有意的。注意事项：
  - `inspect` 在采样的时间戳上测量 `getBoundingClientRect`，而非渲染像素——`overflow: hidden` 剪辑了视觉效果，但**不会**抑制 `inspect` 的溢出发现。此属性是逃生口；CSS overflow 不是。
  - 可以在合成**根**以及任何子元素上设置。当引用的违规者是 `div.<comp>-root inside div.<comp>-root`（根报告其自身子元素的联合体溢出）时，修复应放在根上，而不是单个文本后代上——缩小字体大小无法收敛。
  - 在多场景 `group_wN.html`（连续运行）中，每个场景本地元素在其它场景的时间窗口期间仍保留在 DOM 中；布局框联合体在变形接缝处几乎总是溢出画布。请在**构建时**（而非 `inspect` 标记后）使用此属性标记根和每个场景本地的首要/辅助元素。
  - **爆炸半径——它不仅抑制 `inspect`。** 该属性沿子树向下继承（感知探针会遍历祖先），因此它也会对每个后代抑制渲染感知检查 `text-clipping`、`content-cramped-container` 和 `foreground-over-panel`。将其放在同时承载真实前景内容的持久面板上，会在面板的整个生命周期中禁用该内容上的碰撞检查。建议选择最窄的选择退出方式：将其范围限定在最小的装饰包装器上，或对一次有意的首要文本裁剪使用逐元素 `data-layout-bleed="true"`。两个画布/边缘检查 `primary-offscreen` 和 `foreground-over-panel` 即使**在** `allow-overflow` 下也会继续运行，因此它无法隐藏被画框切割的文字商标或渗入面板边缘的文本。
- `data-layout-ignore` — 完全从布局审核中排除此元素。

## 旧版/已移除属性

以下名称出现在旧项目和示例中。创作或编辑时请使用当前名称：

| 旧名称       | 改用              |
| ------------ | ------------------ |
| `data-layer` | `data-track-index` |
| `data-end`   | `data-duration`    |
