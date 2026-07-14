---
name: hyperframes-css-animations
description: CSS 动画适配器模式，用于 HyperFrames。在编写 CSS 关键帧、基于 animation-delay 的时间控制、animation-fill-mode、animation-play-state 或纯 CSS 动效（HyperFrames 必须在预览和渲染期间确定性定位）时使用。
---

# CSS 动画用于 HyperFrames

HyperFrames 可以通过其 `css` 运行时适配器定位 CSS 关键帧动画。用于简单的重复主题、背景运动、闪烁、辉光、遮罩和非序列化的装饰。

对于场景编排，GSAP 通常更清晰。CSS 动画在动效属于单个元素且具有固定时长时效果最佳。

## 约定

- 在运行时初始化完成之前将动画元素放入 DOM。
- 为时间化元素指定 `data-start` 值，使本地动画时间与剪辑匹配。
- 使用有限的 `animation-duration` 和 `animation-iteration-count`，因为负延迟回退无法在没有 WAAPI 支持的 CSS 动画环境中表示无界时长。
- 优先使用 `animation-fill-mode: both`，使定位状态在活跃动效前后都能保持。
- 避免使用挂钟 JavaScript、悬停触发的状态以及依赖用户事件的类切换。

适配器发现具有计算后 `animation-name` 的元素，在可用时定位其浏览器的 `Animation` 句柄，并回退到使用负 `animation-delay` 暂停。

## 基本模式

```html
<div
  id="pulse-ring"
  class="clip pulse-ring"
  data-start="0"
  data-duration="4"
  data-track-index="2"
></div>

<style>
  .pulse-ring {
    width: 280px;
    height: 280px;
    border: 4px solid rgba(255, 255, 255, 0.7);
    border-radius: 50%;
    animation-name: pulse-ring;
    animation-duration: 1200ms;
    animation-timing-function: cubic-bezier(0.2, 0, 0, 1);
    animation-iteration-count: 3;
    animation-fill-mode: both;
  }

  @keyframes pulse-ring {
    from {
      opacity: 0;
      transform: scale(0.82);
    }
    35% {
      opacity: 1;
    }
    to {
      opacity: 0;
      transform: scale(1.18);
    }
  }
</style>
```

## 错开（Stagger）模式

使用 CSS 自定义属性以避免重复关键帧：

```html
<div class="clip dots" data-start="1" data-duration="3" data-track-index="3">
  <span style="--i: 0"></span>
  <span style="--i: 1"></span>
  <span style="--i: 2"></span>
</div>

<style>
  .dots span {
    display: inline-block;
    width: 18px;
    height: 18px;
    margin-right: 10px;
    border-radius: 50%;
    background: currentColor;
    animation: dot-pop 900ms ease-out both;
    animation-delay: calc(var(--i) * 120ms);
  }

  @keyframes dot-pop {
    from {
      opacity: 0;
      transform: translateY(18px) scale(0.75);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }
</style>
```

## 适用场景

- 具有已知重复次数的装饰性循环。
- 遮罩、辉光、闪烁、颗粒感和微妙的视差层。
- 简单的单元素入场，完整 JS 时间线会显得过度。

## 避免

- 无限的 CSS 动画，除非已验证浏览器暴露了可定位的 WAAPI 支持 CSS 动画句柄。优先使用覆盖可见时长的有限迭代次数。
- 在 transforms 可以工作时动画化布局属性如 `top`、`left`、`width` 或 `height`。
- 依赖悬停、焦点、滚动或媒体查询来触发渲染关键的运动。
- 启动后更改动画类，除非另一个确定性时间线控制该更改。

## 验证

编辑 CSS 动画组合后：

```bash
npx hyperframes lint
npx hyperframes validate
```

## 参考与致谢

- HyperFrames 适配器源码：`packages/core/src/runtime/adapters/css.ts`。
- MDN CSS 动画文档：https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation
- MDN `animation-fill-mode`：https://developer.mozilla.org/en-US/docs/Web/CSS/animation-fill-mode
