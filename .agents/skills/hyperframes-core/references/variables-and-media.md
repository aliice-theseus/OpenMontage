# 变量与媒体

两个独立关注点，因为都控制"从 HTML 外部流入的内容"而组合在一起：运行时参数（变量）和外部媒体文件（视频/音频）。

## 变量

在 `<html>` 元素上使用 `data-composition-variables` 声明变量。每个声明需要 `id`、`type`、`label` 和 `default`：

```html
<html
  data-composition-variables='[
    {"id":"title","type":"string","label":"Title","default":"Hello"},
    {"id":"accent","type":"color","label":"Accent","default":"#66d9ef"}
  ]'
></html>
```

在初始化期间一次性读取解析后的值：

```js
const { title, accent } = window.__hyperframes.getVariables();
document.getElementById("title").textContent = title;
document.documentElement.style.setProperty("--accent", accent);
```

### 变量规则

- 支持的类型及其额外选项（供 Studio 编辑 UI 使用）：
  - `string` — 可选 `placeholder`、`maxLength`
  - `number` — 可选 `min`、`max`、`step`、`unit`
  - `color` — 无
  - `boolean` — 无
  - `enum` — **必需** `options: [{ "value": "...", "label": "..." }, ...]`
- 始终提供有用的 `default` 值，以便预览无需 CLI 覆盖即可工作。
- 在子合成宿主上使用 `data-variable-values='{"title":"Pro"}'` 实现按实例覆盖。
- 使用 `npx hyperframes render --variables '{"title":"Q4 Report"}'` 或 `--variables-file` 实现渲染时覆盖。
- 在 CI 中添加 `--strict-variables`：将未声明的键、类型不匹配和不在 `options` 中的枚举值转换为错误而非警告。
- 在初始化期间一次性读取值，而不是在每个动画帧上读取——变量在渲染过程中不会变化。
- 媒体调色可以在 `data-color-grading` JSON 内部使用精确的变量引用。使用 `$gradingPreset` 或 `${gradingIntensity}` 作为整个字段值；运行时会先解析当前合成的变量，再应用着色器调色。

### 两种 JSON 形态（容易混淆）

- `data-composition-variables` 是一个**声明数组**（模式定义）：`[{id, type, label, default}, ...]`
- `--variables` 和 `data-variable-values` 是**以 id 为键的对象**（实际值）：`{ title: "Q4", accent: "#fff" }`

## 媒体

**不可协商：`<video>`/`<audio>` 必须是宿主合成根（`index.html`）的直接子元素。** 运行时仅注册和驱动作为根直接子元素的媒体。放置在子合成 `<template>` 内部或包裹在任何中间 `<div>` 中的媒体，永远不会被 seek/解码 → 渲染为空白或黑色。`lint`/`validate`/`inspect` 不会捕获此问题；逐帧 `snapshot` 会显示空白面板。

后果：

- 场景特定的片段仍然存在于宿主根中，而不是场景的子合成中。子合成只保留框架/外壳；媒体是位于其上方的宿主同级元素。
- 子合成**无法触及或驱动宿主元素**——`document.querySelector("#host-id")` 和 gsap 选择器字符串（`tl.to("#host-id", …)）都无法跨越边界解析；子合成时间线仅驱动其自身的子树。因此，**宿主媒体上的所有每场景动效（缩放/透明度/变形/倾斜/呼吸）必须在 `index.html` 的主时间线上以全局时间编写**（场景本地时间 + 场景插槽的 `data-start`）。对于没有透视父元素的 3D 倾斜，请对元素使用 gsap `transformPerspective`。参见 `composition-patterns.md` 原型 B。

视频元素必须设置为 muted（静音）和 inline（内联）。音频必须是一个独立的 `<audio>` 元素，即使它使用与视频相同的源文件。

```html
<video
  id="a-roll"
  class="clip"
  src="assets/demo.mp4"
  data-start="0"
  data-duration="12"
  data-track-index="0"
  muted
  playsinline
></video>

<audio
  id="a-roll-audio"
  src="assets/demo.mp4"
  data-start="0"
  data-duration="12"
  data-track-index="10"
  data-volume="1"
></audio>
```

### 媒体规则

- **不要**在合成代码中调用 `video.play()`、`audio.play()`、暂停或 seek。HyperFrames 拥有播放控制权。
- **不要**将媒体放置在子合成 `<template>` 或任何包装 `<div>` 内部——只能是宿主的直接子元素（见上文），否则永远不会解码。
- **不要**从子合成时间线驱动宿主媒体——这不起作用。应从主时间线以全局时间驱动。
- **不要**对计时媒体元素尺寸做动画；应改为对非计时包装器做动画。
- **不要**将视频嵌套在计时包装器内。将时间设置在媒体元素上，或保持包装器无计时。
- 对于需要画布捕获或像素检查的外部媒体，添加 `crossorigin="anonymous"`。
- 音频始终位于独立的 `<audio>` 元素上——即使其源文件与 `<video>` 相同。`<video>` 是静音的；`<audio>` 承载声音。
- 对于音量淡入淡出/闪避，在时间线上对 `volume` 做动画（`tl.to("#bgm", { volume: 0, duration: 1 }, "outro")`），而不是交换 `data-volume`。运行时会探查时间线的音量关键帧，并在预览和渲染中一致地应用它们；`data-volume` 是没有补间触及的元素的静态基线。

关于媒体时长：如果已知媒体的固有长度且希望使用完整片段，`<video>` 和 `<audio>` 可以省略 `data-duration`。否则请显式提供 `data-duration`。
