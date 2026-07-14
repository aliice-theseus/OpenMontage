---
name: timing
description: Remotion 中的插值曲线 - 线性、缓动、弹性动画
metadata:
  tags: spring, bounce, easing, interpolation
---

使用 `interpolate` 函数进行简单的线性插值。

```ts title="在 100 帧内从 0 到 1"
import { interpolate } from "remotion";

const opacity = interpolate(frame, [0, 100], [0, 1]);
```

默认情况下，值不会被钳制，因此值可能超出 [0, 1] 范围。  
以下是钳制方法：

```ts title="在 100 帧内从 0 到 1，带外推控制"
const opacity = interpolate(frame, [0, 100], [0, 1], {
  extrapolateRight: "clamp",
  extrapolateLeft: "clamp",
});
```

## 弹性动画

弹性动画具有更自然的运动感。  
它们随时间从 0 到 1 变化。

```ts title="在 100 帧内从 0 到 1 的弹性动画"
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({
  frame,
  fps,
});
```

### 物理属性

默认配置为：`mass: 1, damping: 10, stiffness: 100`。  
这导致动画在稳定前会有一些弹跳。

可以这样覆盖配置：

```ts
const scale = spring({
  frame,
  fps,
  config: { damping: 200 },
});
```

无弹跳的自然运动推荐配置为：`{ damping: 200 }`。

以下是一些常见配置：

```tsx
const smooth = { damping: 200 }; // 平滑，无弹跳（微妙的揭示效果）
const snappy = { damping: 20, stiffness: 200 }; // 干脆，最小弹跳（UI 元素）
const bouncy = { damping: 8 }; // 弹跳入场（俏皮动画）
const heavy = { damping: 15, stiffness: 80, mass: 2 }; // 沉重，缓慢，小弹跳
```

### 延迟

默认情况下动画立即开始。  
使用 `delay` 参数将动画延迟一定数量的帧。

```tsx
const entrance = spring({
  frame: frame - ENTRANCE_DELAY,
  fps,
  delay: 20,
});
```

### 时长

`spring()` 有基于物理属性的自然时长。  
要将动画拉伸到特定时长，请使用 `durationInFrames` 参数。

```tsx
const spring = spring({
  frame,
  fps,
  durationInFrames: 40,
});
```

### 组合 spring() 与 interpolate()

将弹性输出（0-1）映射到自定义范围：

```tsx
const springProgress = spring({
  frame,
  fps,
});

// 映射到旋转
const rotation = interpolate(springProgress, [0, 1], [0, 360]);

<div style={{ rotate: rotation + "deg" }} />;
```

### 弹性值相加

弹性函数只返回数字，因此可以进行数学运算：

```tsx
const frame = useCurrentFrame();
const { fps, durationInFrames } = useVideoConfig();

const inAnimation = spring({
  frame,
  fps,
});
const outAnimation = spring({
  frame,
  fps,
  durationInFrames: 1 * fps,
  delay: durationInFrames - 1 * fps,
});

const scale = inAnimation - outAnimation;
```

## 缓动

可以将缓动添加到 `interpolate` 函数：

```ts
import { interpolate, Easing } from "remotion";

const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

默认缓动为 `Easing.linear`。  
还有其他各种凸性：

- `Easing.in` 缓慢开始并加速
- `Easing.out` 快速开始并减速
- `Easing.inOut`

和曲线（从最线性到最弯曲排序）：

- `Easing.quad`
- `Easing.sin`
- `Easing.exp`
- `Easing.circle`

凸性和曲线需要组合以形成缓动函数：

```ts
const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

也支持三次贝塞尔曲线：

```ts
const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.bezier(0.8, 0.22, 0.96, 0.65),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```
