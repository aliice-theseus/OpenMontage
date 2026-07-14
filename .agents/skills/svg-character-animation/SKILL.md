---
name: svg-character-animation
description: 使用 GSAP、CSS 变换、Remotion 帧控制和 HyperFrames 兼容的浏览器预览来动画 SVG 角色绑定。
license: MIT
---

# SVG 角色动画

在动画由 SVG 部件组成的角色绑定时使用此技能。

## 运行时规则

- 动画变换（`x`、`y`、`scale`、`rotation`）而非布局。
- 对多部件表演节拍使用时间线。
- 对于 SVG 元素，使用稳定的枢轴点（`svgOrigin` 或正确作用域的变换原点）。
- 在 Remotion 中，不要让 GSAP 通过 `requestAnimationFrame` 推进；从当前帧驱动暂停的时间线。

## 浏览器模式

```js
gsap.set("#arm_right", { svgOrigin: "390 310" });
const tl = gsap.timeline({ defaults: { ease: "power2.inOut" } });
tl.to("#head", { rotation: -8, duration: 0.2 })
  .to("#arm_right", { rotation: 35, duration: 0.4 }, "<");
```

## Remotion 模式

```tsx
const frame = useCurrentFrame();
const progress = frame / durationInFrames;
timeline.progress(progress);
```

## HyperFrames 模式

使用具有确定性时间线的 HTML/SVG/GSAP 组件，并通过 HyperFrames CLI 在最终渲染前进行验证。

## 质量检查清单

- 部件在运动期间在枢轴点保持连接。
- 眨眼、视线和嘴型足够分离以便阅读。
- 姿态停顿足够长以传达情感。
- 帧采样显示有意义的增量，而非冻结的动画。

## 参考资料

- GSAP 核心变换属性和 SVG 处理：
  https://gsap.com/docs/v3/GSAP/CorePlugins/CSS/
- GSAP 时间线和排序：
  https://gsap.com/docs/v3/GSAP/Timeline/
- Remotion `useCurrentFrame`：
  https://www.remotion.dev/docs/use-current-frame
