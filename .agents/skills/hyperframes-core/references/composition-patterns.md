# 合成模式

如何架构一个项目 — 何时将所有内容内联到一个 HTML 中，何时拆分为子合成，`index.html` 协调器在规模下是什么样子，以及实际项目中常见的子合成原型。与 `minimal-composition.md`（单文件形状）和 `sub-compositions.md`（子合成文件的机制）配合使用。

## 两种架构

|                    | 整体式（单文件）                                          | 模块化（子合成）                                                                    |
| ----------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 项目布局           | 仅 `index.html`                                          | `index.html` + 每个场景一个 `compositions/<scene>.html`                           |
| 场景位置           | 根下内联 `<section class="clip">` 同级元素                | 每个场景是包装在 `<template>` 中的单独文件                                         |
| 时间线注册         | 一个以根 `data-composition-id` 为键的时间线               | 根时间线（通常近乎为空）+ 每个子合成一个时间线，每个以其 `id` 为键                   |
| 路由入口           | `references/minimal-composition.md`                     | `references/sub-compositions.md`                                                  |

两种架构使用相同的运行时契约 — `data-*` 属性 + `window.__timelines[id]`。选择是结构性的，而非行为性的。

### 何时选择整体式

- 整个视频是一个连续场景，没有硬切。
- 场景共享重型状态（一个 Canvas/WebGL 上下文贯穿整个视频，一个 SVG 跨所有节拍变形）。
- 总体范围较小（约 200–400 行 HTML + 脚本）。
- 没有场景在项目间复用。

### 何时选择模块化

- 视频有明显场景切换——每个场景是时间线的独立段落。
- 某些场景较大（超过 100 行 HTML 或大量脚本动画）。
- 场景可复用（动感开场、片尾标志组合、转场）。
- 视频有跨多个视觉段落的连续音轨。音频保持在根层级，视觉段落作为子合成。
- 希望隔离创作/迭代场景（直接预览单个子合成文件）。

### 两者间的重构

转换是机械且可逆的。将整体式场景提升为子合成：将场景的标记 + 作用域 CSS + 父时间线片段包裹到一个 `<template>` 中，保存为 `compositions/<scene>.html`，将 `index.html` 中的内联内容替换为一个插槽 `<div data-composition-src="compositions/<scene>.html">`，并在 `window.__timelines["<scene>"]` 注册子合成自己的时间线。父时间线相应缩小。

如果整体式项目接近三个或更多场景切换，建议在添加下一个场景**之前**进行模块化。混合项目（部分场景内联、同级在 `compositions/` 中）最难维护。

## 模块化编排模式

使用子合成时，`index.html` 应该**很薄**。它的工作是声明插槽、在时间上布局、挂载音轨，并注册一个（通常为空的）根时间线。所有场景动画位于子合成内部。

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {
        margin: 0;
        background: #000;
      }
      #root {
        position: relative;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
      }
      /* Sub-comp slots stretch to fill the root. */
      [data-composition-id="root"] > div[data-composition-src] {
        position: absolute;
        inset: 0;
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="root"
      data-width="1920"
      data-height="1080"
      data-duration="30"
    >
      <!-- Sequential scenes — each one a sub-composition slot. -->
      <div
        id="el-intro"
        data-composition-id="intro"
        data-composition-src="compositions/intro.html"
        data-start="0"
        data-duration="6"
        data-track-index="1"
      ></div>

      <div
        id="el-body"
        data-composition-id="body"
        data-composition-src="compositions/body.html"
        data-start="6"
        data-duration="18"
        data-track-index="1"
      ></div>

      <div
        id="el-outro"
        data-composition-id="outro"
        data-composition-src="compositions/outro.html"
        data-start="24"
        data-duration="6"
        data-track-index="1"
      ></div>

      <!-- Continuous audio at the root — survives scene cuts. -->
      <audio
        id="el-bgm"
        src="assets/bgm.mp3"
        data-start="0"
        data-duration="30"
        data-track-index="10"
        data-volume="0.6"
      ></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["root"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
```

此布局的关键属性：

- **同一 `data-track-index` 上的视觉场景**（例如 `1`）。顺序排列——它们在同一轨道上不能重叠。如需两个场景间的交叉淡入淡出，将一个放在更高轨道上，以淡入淡出时长重叠它们的时间。
- **音频在独立、更高的轨道索引上**（例如 `10`）。保持检查器的重叠规则远离任何视觉冲突。
- **根时间线近乎为空。** 所有动画位于子合成中。最后在根层级淡出到黑色是可以的；不要在根层级设置并行动画轨道。
- **宿主插槽 ID** 使用 `el-<name>` 或 `<scene-id>`。插槽的 `data-composition-id` 必须仍等于子合成的内部 ID（参见 `sub-compositions.md`）。

## 子合成原型

### A. 内容场景（默认）

子合成包含场景的完整 DOM、作用域 CSS 和时间线。这是 `sub-compositions.md` 中的标准模式——大多数场景属于此类。

### B. 宿主媒体 + 主时间线驱动（任何 `<video>`/`<audio>` 必需）

媒体播放仅在 `<video>`/`<audio>` 是**宿主根的直接子元素**时有效——绝不能在子合成 `<template>` 内部（会渲染为空白/黑色）。这不是可选的，也不仅限于"跨场景的媒体"；它适用于每个片段，包括场景特定的片段。场景的子合成保留框架/外壳；媒体是位于其上方的宿主同级元素。

子合成时间线**不能**驱动宿主元素（全局选择器或 `document.querySelector` 无法跨越边界解析）。因此，在 `index.html` 的**主时间线**上以**全局时间**（= 场景本地时间 + 场景插槽的 `data-start`）编写媒体的每场景动效（缩放/透明度/变形/倾斜/呼吸）。

```html
<!-- index.html (host) -->
<div
  id="el-final"
  data-composition-id="final-anim"
  data-composition-src="compositions/final-anim.html"
  data-start="20"
  data-duration="6"
  data-track-index="1"
></div>

<!-- media is a DIRECT root child; sits over the sub-comp's frame -->
<video
  id="final-video"
  class="clip"
  src="assets/final.mp4"
  data-start="20"
  data-duration="6"
  data-track-index="2"
  muted
  playsinline
  style="position:absolute; left:360px; top:100px; width:1200px; height:680px; object-fit:cover; border-radius:24px;"
></video>

<script>
  // MAIN timeline drives the host video. Global time: scene starts at 20.
  window.__timelines = window.__timelines || {};
  const main = window.__timelines["main"];
  main.fromTo(
    "#final-video",
    { scale: 1.4, filter: "blur(14px)" },
    { scale: 1.0, filter: "blur(0px)", duration: 0.9, ease: "power3.out" },
    20,
  ); // = slot data-start (+ any scene-local offset)
</script>

<!-- compositions/final-anim.html — frame/shell only, no <video>, no host-element animation -->
<template>
  <div
    data-composition-id="final-anim"
    data-width="1920"
    data-height="1080"
    data-duration="6"
    style="position:absolute; inset:0; pointer-events:none;"
  >
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      // animate ONLY this sub-comp's own elements here (labels, frame, overlays)
      window.__timelines["final-anim"] = tl;
    </script>
  </div>
</template>
```

注意事项：

- 宿主媒体必须是根的直接子元素，并存在于 DOM 中（在 `index.html` 中静态声明）——它始终如此。
- 片段生命周期管理媒体元素在其 `[data-start, data-start+data-duration]` 窗口内的可见性。主时间线的不透明度/缩放补间与其配合良好；对于不透明度揭示/交叉淡入淡出，建议使用宿主**包装器**，以避免与媒体元素本身的生命周期冲突。
- 两个共享相同 `src` + `data-start` 的媒体元素会触发 `duplicate_media_discovery_risk`（良性——两者仍可渲染）。

### C. 多场景合并

当多个节拍级场景共享连续状态时——增长的聊天线程、跨切换携带的持久标题词、具有内部阶段变化的单个 Canvas——将它们合并到一个子合成中，使用**内部阶段 div** 而不是多个子合成插槽。

```html
<!-- compositions/act2-merged.html -->
<template>
  <div data-composition-id="act2-merged" data-width="1920" data-height="1080" data-duration="9">
    <style>
      [data-composition-id="act2-merged"] .phase {
        position: absolute;
        inset: 0;
        opacity: 0;
      }
    </style>
    <div class="phase" id="phase-a">…</div>
    <div class="phase" id="phase-b">…</div>
    <div class="phase" id="phase-c">…</div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      tl.set("#phase-a", { opacity: 1 }, 0);
      tl.to("#phase-a", { opacity: 0, duration: 0.4 }, 3.0);
      tl.set("#phase-b", { opacity: 1 }, 3.0);
      // …
      window.__timelines["act2-merged"] = tl;
    </script>
  </div>
</template>
```

在场景共享 DOM、共享 Canvas 或需要带有持久元素（跨阶段切换保留的标题）的交叉淡入淡出时，优先使用此模式而非多个顺序插槽。每个阶段只是同一子合成内的一个 div——父时间线无需了解内部阶段的边界。

### D. 音频在根层级，响应式视觉在内部

音频始终位于宿主（`index.html`），作为根级 `<audio>`，因此播放能在场景切换中持续。可视化音频的子合成应在初始化时读取**预烘焙**的频率曲线，然后从其时间线中采样烘焙曲线——视觉仍然必须是 `tl.time()` 的确定性函数，而不是 `audio.currentTime`。参见 `determinism-rules.md` 和 `hyperframes-creative` 了解创作模式。

## 命名约定

| 内容                               | 约定                                      | 示例                                    |
| ----------------------------------- | ------------------------------------------- | ------------------------------------------ |
| 子合成文件                       | `compositions/<scene-id>.html`              | `compositions/act0-intro-bell.html`        |
| 子合成 `<template>` id（可选） | `<scene-id>-template`                       | `<template id="act0-intro-bell-template">` |
| 子合成根 `data-composition-id` | `<scene-id>`（必须匹配宿主插槽）         | `data-composition-id="act0-intro-bell"`    |
| 时间线注册键               | 匹配 `data-composition-id`               | `window.__timelines["act0-intro-bell"]`    |
| 宿主插槽 `id`                      | `el-<short>` 或 `<scene-id>`                | `id="el-intro"`、`id="act0"`               |
| 子合成内部元素 ID       | 使用场景 ID 作为前缀                    | `#act0-bell`、`#b1-tape`                   |
| 根层级音频                       | `data-track-index` 远高于视觉轨道 | `10`，视觉轨道使用 `1`                 |

`<template>` 上的 `-template` 后缀是约定而非强制——运行时会从 `<body>` 中的任意 `<template>` 提取内容，无论 ID 如何。内部元素 ID 的前缀是当多个子合成同时挂载到同一宿主页面时防止 ID 冲突的唯一保障。

## 编辑现有项目

在添加或修改场景之前，识别当前使用的架构：

```bash
ls compositions/ 2>/dev/null && echo "modular" || echo "monolithic"
```

- 在**整体式**项目中，将新场景添加为内联 `<section class="clip">` 元素，使用不重叠的 `data-start` 和合理的 `data-track-index`，并扩展现有的单条时间线。
- 在**模块化**项目中，匹配模式：在 `compositions/` 下添加新文件，在 `index.html` 中添加插槽，保持根时间线精简。**不要**在同级场景是子合成时将新场景内联到 `index.html` 中——这种不一致性是最糟糕的两种世界结合。
- 如果整体式项目需要第三或第四个场景切换，在添加更多场景之前将每个场景提升为子合成。转换是机械性的（参见上面的"两者间的重构"）。

选择插槽的 `data-start`/`data-duration` 时，建议延续现有的时序约定（相邻起始、有意重叠用于交叉淡入淡出）。除非确实需要并行的视觉图层，否则不要引入新的轨道索引——大多数顺序场景项目正好使用一个视觉轨道。
