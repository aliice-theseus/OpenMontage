---
name: camera-cursor-tracking
description: 双阶段虚拟摄像机，将视口锁定到移动的焦点，可配置初始定位。
metadata:
  tags: camera, tracking, viewport, two-phase, spring
---

# 双阶段摄像机光标跟踪

通过在两个摄像机模式之间切换，保持水平增长的元素（例如带打字文本的搜索栏、动画中的长 URL）可见。

## 工作原理

分离**世界空间**（带有所有内容的完整目标元素）与**屏幕空间**（视口）。两个阶段：

- **阶段 1（静态）** — 世界容器位于固定初始偏移。摄像机不移动。这在跟踪开始前将观看者眼睛锚定到构图。
- **阶段 2（跟踪）** — 当焦点（光标、高亮、最后键入的字形）超过目标屏幕位置（例如从左侧到视口宽度的可配置分数 `CURSOR_TARGET_FRACTION`）时激活。世界容器向左平移（`x: -<delta>`），将焦点固定在该屏幕位置。

## HTML、CSS 和 GSAP 时间线

（保持原有代码块，注释已中文化。）

## 关键原则

- **使用 `getBoundingClientRect()` / 探针节点测量**，而非字符数 × 字号。比例字体有可变字形宽度。
- **世界上设置 `white-space: nowrap`** — 文本必须保持在一行，摄像机数学才能工作
- **通过设置 `maxWidth` 为完整目标宽度预分配世界宽度** — 防止补间中段布局偏移
- **缓动摄像机（`power2.inOut` / `power3.inOut`），非线性** — 自然平移感
- **通过缓动近似弹簧**，非刚度/阻尼参数

## 关键约束

- **同步构建时间线，无 fonts.ready 门控** — HF 在并行工作线程中渲染帧，每个线程是新鲜浏览器。如果你将时间线构建包装在 `document.fonts.ready.then(...)` 中，某些工作线程会在 Promise 解析之前定位帧，找不到注册的时间线 → 那些帧以 CSS 初始状态渲染，其他工作线程正确渲染 → 空和填满之间的可见闪烁。在脚本解析时注册 `window.__timelines[id] = tl`，即使字体尚未加载 — 摄像机数学可以容忍来自回退字体测量的百分之几宽度误差，但工作线程竞态闪烁是不可接受的。
- **如果精确的后字体测量重要**，在补间的 `onUpdate` 中重新测量（仍确定性每帧定位），而非通过 Promise 门控。或在 `@font-face` 上设置 `font-display: block` 强制浏览器在绘制任何文本前等待字体。
- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **阶段边界处的连续数学**：世界在跟踪开始时刻的 `x` 必须等于静态阶段偏移。`Math.min(INITIAL_OFFSET, trackingOffset)` 公式保证这一点；不要切换到硬 `if (typingProgress > threshold)` 分支，否则摄像机会明显跳跃。
- **内联光标，非绝对定位**：光标应是文本的兄弟（inline-block），使其自然跟随文本流
- **`.viewport` 上设置 `overflow: hidden`**：随着世界向左平移出屏幕，裁剪其左边缘
- **光标闪烁通过 GSAP，而非 CSS `@keyframes ... infinite`** — HF 通过定位暂停时间线渲染；CSS 动画时钟不与定位同步，因此任何 CSS 驱动的闪烁会跨帧非确定性闪烁。始终将闪烁驱动为暂停 GSAP 时间线上的有限 yoyo 补间（从场景长度计算重复次数）。
