---
name: hyperframes-gsap-adapter
description: HyperFrames 的 GSAP 动画 API 参考。在编写 HyperFrames 组合中可定位的 GSAP 时间线时使用，包括 gsap.to()、from()、fromTo()、set()、时间线位置参数、标签、缓动、错开、有限重复和变换性能。
---

# HyperFrames GSAP

GSAP 用法限定在 HyperFrames 的 seek 驱动渲染模型范围内。此技能是受 HyperFrames **约束**的 GSAP 参考——关于框架更广泛的组合约定，请参见 `hyperframes-core`。

## HyperFrames 约定

HyperFrames 通过其 `gsap` 运行时适配器控制 GSAP。同步创建暂停的时间线，在 `window.__timelines` 上使用确切的 `data-composition-id` 注册，让 HyperFrames 定位它。

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  tl.from(".title", { y: 48, opacity: 0, duration: 0.6, ease: "power3.out" }, 0);
  tl.to(".accent", { scaleX: 1, duration: 0.5, ease: "power2.out" }, 0.25);

  window.__timelines["main"] = tl; // key 必须等于组合根元素的 data-composition-id
</script>
```

- 注册键必须匹配组合根元素的 `data-composition-id`。
- 括号和点语法均可注册：`window.__timelines["main"] = tl` 和 `window.__timelines.main = tl` 等价（linter 都识别）。括号形式在 id 不是有效标识符时（例如包含 `-`）是必需的。
- 不要为渲染关键运动调用 `tl.play()`。
- 不要在异步代码、定时器或事件处理程序中构建时间线。
- 保持循环有限。HyperFrames 渲染有限的视频时长。
- **渲染时长来自组合根元素上的 `data-duration`，而非 GSAP 时间线长度。** 不要用空补间如 `tl.set({}, {}, 283)` 填充时间线来"延长"它。（某些外部文档展示了这种技巧；在 HyperFrames 中它与 seek 驱动的时长模型冲突——请改用 `data-duration`。）

## 核心补间方法

- **gsap.to(targets, vars)** — 从当前状态动画到 `vars`。最常用。
- **gsap.from(targets, vars)** — 从 `vars` 动画到当前状态（入场）。
- **gsap.fromTo(targets, fromVars, toVars)** — 显式指定开始和结束。
- **gsap.set(targets, vars)** — 立即应用（时长为 0）。

始终使用**驼峰命名**的属性名称（例如 `backgroundColor`、`rotationX`）。

## 常用 vars（速查表）

- **duration** — 秒（默认 0.5）。
- **delay** — 开始前的秒数。
- **ease** — `"power1.out"`（默认）、`"power3.inOut"`、`"back.out(1.7)"`、`"elastic.out(1, 0.3)"`、`"none"`。参见 `./gsap-easing-and-stagger.md`。
- **stagger** — 数字或对象。参见 `./gsap-easing-and-stagger.md`。
- **repeat** — 有限的数字；在 HyperFrames 中不要使用 `-1`。从可见时长计算重复次数。
- **yoyo** — 与 repeat 配合交替方向。
- **overwrite** — `false`（默认）、`true` 或 `"auto"`。
- **immediateRender** — 对于 from()/fromTo() 默认为 `true`。在目标相同属性和元素的后续补间上设置为 `false`。
- **onComplete**、**onStart**、**onUpdate** — 回调函数。

关于 transforms、autoAlpha、clearProps 和 SVG 细节，参见 `./gsap-transforms-and-perf.md`。

## 动画属性允许列表

HyperFrames 比原始 GSAP 更严格。仅可动画化：

- **合成器低成本**：`opacity`、`x`、`y`、`scale`、`scaleX`、`scaleY`、`rotation`、`rotationX`、`rotationY`、`skewX`、`skewY`、`transformOrigin`
- **视觉填充**：`color`、`backgroundColor`、`borderColor`、`borderRadius`
- **CSS 变量**：`"--hue": 180` 等。
- **媒体 `volume`**（在 `<audio>` / `<video>` 上）：用于淡入淡出/闪避的动画，例如 `tl.to("#bgm", { volume: 0, duration: 1 }, "outro")`。运行时从时间线探测这些关键帧并在预览和渲染中同时驱动（两者匹配）。这设置了**作者**音量；当没有补间触及该元素时，`data-volume` 是静态基线。
- **DOM 文本 `innerText`**（用于数字计数器）：直接补间，例如 `tl.to(el, { innerText: 100, snap: { innerText: 1 } })`——`snap` 保持整数；GSAP 检查器识别为计数器。等同于 `../rules/counting-dynamic-scale.md` 中的 `onUpdate` proxy 形式；当必须在同一补间中同时驱动字号、区域格式（`toLocaleString`）或后缀时，优先使用那种 proxy 形式。

**避免**（改用变换别名）：

- `width` / `height` / `top` / `left` / `right` / `bottom` / `margin*` / `padding*` — 触发布局回流。使用 `scaleX/Y`（配合 `transformOrigin`）或 `x` / `y`。

**禁止**（破坏渲染器或剪辑生命周期）：

- `display`、`visibility` — 永远不要直接补间这些。使用 `autoAlpha`（在端点同时设置 opacity 和 visibility，但不补间断续属性）。
- 任何由 `Math.random()`、`Date.now()`、`performance.now()` 或事件驱动的内容——动画状态必须仅从时间可确定性决定。

> **注意**：`docs/guides/gsap-animation.mdx` 在其"支持的属性"中列出了 `width`/`height`/`visibility`——该列表对于 HyperFrames 组合规则来说过于宽松。本允许列表是权威版本。关于完整确定性渲染约定，请参见 `hyperframes-core/references/determinism-rules.md`。

## 参考

- `./gsap-timeline-and-labels.md` — 时间线创建、位置参数（`+=`、`<`、`>`）、标签、嵌套、子组合 `fromTo` 优先、播放控制。
- `./gsap-easing-and-stagger.md` — 缓动族、stagger 对象、基于函数的值、`gsap.matchMedia()`、`gsap.defaults()`。
- `./gsap-transforms-and-perf.md` — 变换别名、autoAlpha、`quickTo`、`will-change`、性能规则。
- `../rules/gsap-effects.md` — 即用配方：打字机效果（带光标/退格/单词旋转）+ 音频可视化器（使用 `skills/hyperframes-creative/scripts/extract-audio-data.py`）。

## 最佳实践

- 使用驼峰命名属性名；优先使用变换别名和 autoAlpha。
- 优先使用时间线而非带延迟的链式补间；使用位置参数。
- 使用 `addLabel()` 添加标签以实现可读的排序。
- 将默认值传入时间线构造函数。
- 在控制播放时存储补间/时间线的返回值。

## 禁止

- 在 transforms 足够时动画化布局属性（`width`/`height`/`top`/`left`）。
- 在同一 SVG 元素上同时使用 `svgOrigin` 和 `transformOrigin`。
- 时间线可以排序时使用 `delay` 链式动画。
- 在 DOM 存在之前创建补间。
- 在 HyperFrames 组合中使用无限 `repeat: -1`——使用从可见时长计算的有限重复次数。

## 参考与致谢

- HyperFrames 适配器源码：`packages/core/src/runtime/adapters/gsap.ts`。
- GSAP 文档：https://gsap.com/docs/v3/
- GSAP 时间线 pause 和 seek 行为：https://gsap.com/docs/v3/GSAP/Timeline/pause%28%29/
