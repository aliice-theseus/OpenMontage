---
name: hyperframes-animejs
description: Anime.js 适配器模式，用于 HyperFrames。在 HyperFrames 组合中编写 Anime.js 动画或时间线、在 window.__hfAnime 上注册动画、使 Anime.js 可 seek 驱动且确定性、或将 Anime.js 示例转换为可安全渲染的 HyperFrames HTML 时使用。
---

# Anime.js 用于 HyperFrames

HyperFrames 可以通过其 `animejs` 运行时适配器定位 Anime.js 实例。组合拥有动画对象；HyperFrames 拥有时钟。

## 约定

- 在组合初始化期间**同步**创建动画或时间线。
- 设置 `autoplay: false` 使 Anime.js 不按其自己的时钟推进。
- 在 `window.__hfAnime` 上注册每个返回的动画或时间线。
- 使用有限的时长和循环次数。
- 避免基于挂钟时间、网络状态或非种子化随机性改变 DOM 的回调。

适配器使用 `instance.seek(timeMs)` 定位每个注册的实例，其中 `timeMs` 是以毫秒为单位的 HyperFrames 时间。

## 基本模式

```html
<script src="https://cdn.jsdelivr.net/npm/animejs@4.0.2/lib/anime.iife.min.js"></script>
<script>
  const anim = anime({
    targets: ".mark",
    translateX: 280,
    rotate: "1turn",
    opacity: [0, 1],
    duration: 1200,
    easing: "easeOutExpo",
    autoplay: false,
  });

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(anim);
</script>
```

## 时间线模式

```html
<script>
  const tl = anime.timeline({
    autoplay: false,
    easing: "easeOutCubic",
  });

  tl.add({
    targets: ".title",
    translateY: [40, 0],
    opacity: [0, 1],
    duration: 650,
  }).add(
    {
      targets: ".accent",
      scaleX: [0, 1],
      duration: 450,
    },
    250,
  );

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(tl);
</script>
```

## 模块构建

如果你使用 ES 模块构建，适配器不关心实例是如何创建的。它只需要返回的对象暴露 `seek()`、`pause()` 和（可选）`play()`：

```html
<script type="module">
  import { animate } from "https://cdn.jsdelivr.net/npm/animejs/+esm";

  const anim = animate(".chip", {
    x: "18rem",
    duration: 900,
    autoplay: false,
  });

  window.__hfAnime = window.__hfAnime || [];
  window.__hfAnime.push(anim);
</script>
```

## 适用场景

- 小型 SVG 和 DOM 点缀，Anime.js 语法更简洁。
- 可以改为 seek 驱动的导入的 Anime.js 示例。
- 推入同一注册表的多个独立微动画。

除非用户特别要求 Anime.js，否则复杂场景排序请使用 GSAP。GSAP 仍然是 HyperFrames 主要的创作路径。

## 避免

- 将 `autoplay` 保留为 Anime.js 默认值。
- 依赖 `anime.running` 自动发现而非显式的 `window.__hfAnime.push(...)`。
- 无限循环。从组合时长计算有限的重复次数。
- 在定时器、Promise、事件处理程序或异步资源加载后构建动画。

## 验证

编辑使用 Anime.js 的组合后：

```bash
npx hyperframes lint
npx hyperframes validate
```

## 参考与致谢

- HyperFrames 适配器源码：`packages/core/src/runtime/adapters/animejs.ts`。
- Anime.js 关于 `autoplay`、`pause()` 和 `seek()` 的文档：https://animejs.com/documentation/
