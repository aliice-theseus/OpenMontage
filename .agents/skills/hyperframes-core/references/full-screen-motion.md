# 全屏运动模式

对于全帧运动（连续背景、颜色渲染、跨越多个片段的满版视觉状态），优先使用**共享背景层 + 透明计时内容层**，而不是堆叠的不透明场景背景。

## 原因

堆叠不透明场景 div 意味着每次场景变化都必须重新绘制整个帧，每次跨场景视觉连续性都必须伪造，并且每个"全局"状态（色调偏移、暗角、胶片颗粒）都必须在每个场景上重复。由可查找时间线驱动的共享背景层为您提供一个连续的视觉表面，并使场景本身变得轻量和透明。

## 模式

```html
<div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="20">
  <!-- 共享背景 — 不是 clip。始终可见。由时间线驱动。 -->
  <div id="bg" class="full-bleed"></div>

  <!-- 计时内容层 — 透明背景。 -->
  <section
    id="scene1"
    class="clip transparent"
    data-start="0"
    data-duration="6"
    data-track-index="1"
  >
    <!-- 内容 -->
  </section>
  <section
    id="scene2"
    class="clip transparent"
    data-start="6"
    data-duration="14"
    data-track-index="1"
  >
    <!-- 内容 -->
  </section>
</div>

<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 从可查找时间线驱动共享背景。
  tl.to("#bg", { backgroundColor: "#0a1530", duration: 6, ease: "sine.inOut" }, 0);
  tl.to("#bg", { backgroundColor: "#1a0a30", duration: 14, ease: "sine.inOut" }, 6);

  // 场景本地动画保持在顶部透明层。
  tl.from("#scene1 h1", { y: 48, opacity: 0, duration: 0.6 }, 0.2);

  window.__timelines["main"] = tl;
</script>
```

## 规则

- **背景不是 clip。** 没有 `data-start` / `data-duration` / `data-track-index`。它存在于整个合成中。
- **内容场景具有透明背景。** 你在共享 `#bg` 中放置的任何内容都会透显出来。
- **从共享层驱动全局状态。** 色调偏移、暗角、颗粒、胶片效果滤镜 — 在共享层上一次完成动画，而不是逐场景进行。
- **不要在 `.clip` 元素上动画 visibility。** HyperFrames 已经基于 `data-start` 和 `data-duration` 显示/隐藏 clip。在 clip 本身上动画 `display` / `visibility` 会与框架自身的显示/隐藏产生竞争。改为在 clip 内部动画一个_子包装器_。
- **通过快照验证有意溢出。** 在添加 `data-layout-allow-overflow` 以消除检查警告之前，运行 `npx hyperframes snapshot` 并确认溢出是你想要的效果。

## 何时不使用此模式

如果场景确实是视觉不连续的——不同色彩世界之间的硬切，没有连续性——那么堆叠不透明模式是可以的。共享背景模式适用于背景**是运动语言的一部分**的合成，而不仅仅是背景幕。
