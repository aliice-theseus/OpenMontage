---
name: transitions
description: 使用 TransitionSeries 为 Remotion 添加场景转场和叠加效果
metadata:
  tags: transitions, overlays, fade, slide, wipe, scenes
---

## TransitionSeries

`<TransitionSeries>` 编排场景，并支持两种方式增强场景切换点：

- **转场**（`<TransitionSeries.Transition>`）— 在两个场景间执行淡入淡出、滑动、擦除等效果。会缩短时间线，因为转场期间两个场景同时播放。
- **叠加层**（`<TransitionSeries.Overlay>`）— 在切换点上渲染效果（如漏光），不缩短时间线。

子元素为绝对定位。

## 前置条件

```bash
npx remotion add @remotion/transitions
```

## 转场示例

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>;
```

## 叠加层示例

任何 React 组件都可以用作叠加层。有关现成效果，请参阅 **light-leaks** 规则。

```tsx
import { TransitionSeries } from "@remotion/transitions";
import { LightLeak } from "@remotion/light-leaks";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Overlay durationInFrames={20}>
    <LightLeak />
  </TransitionSeries.Overlay>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>;
```

## 混合转场和叠加层

转场和叠加层可以在同一个 `<TransitionSeries>` 中共存，但叠加层不能与转场或其他叠加层相邻。

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { LightLeak } from "@remotion/light-leaks";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Overlay durationInFrames={30}>
    <LightLeak />
  </TransitionSeries.Overlay>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneC />
  </TransitionSeries.Sequence>
</TransitionSeries>;
```

## 转场属性

`<TransitionSeries.Transition>` 需要：

- `presentation` — 视觉效果（例如 `fade()`、`slide()`、`wipe()`）
- `timing` — 控制速度和缓动（例如 `linearTiming()`、`springTiming()`）

## 叠加层属性

`<TransitionSeries.Overlay>` 接受：

- `durationInFrames` — 叠加层可见时长（正整数）
- `offset?` — 相对于切换点中心的偏移。正值 = 更晚，负值 = 更早。默认值：`0`

## 可用的转场类型

从各自的模块导入转场：

```tsx
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { flip } from "@remotion/transitions/flip";
import { clockWipe } from "@remotion/transitions/clock-wipe";
```

## 带方向的滑动转场

```tsx
import { slide } from "@remotion/transitions/slide";

<TransitionSeries.Transition
  presentation={slide({ direction: "from-left" })}
  timing={linearTiming({ durationInFrames: 20 })}
/>;
```

方向：`"from-left"`、`"from-right"`、`"from-top"`、`"from-bottom"`

## 时间控制选项

```tsx
import { linearTiming, springTiming } from "@remotion/transitions";

// 线性时间控制 - 恒定速度
linearTiming({ durationInFrames: 20 });

// 弹簧时间控制 - 有机运动
springTiming({ config: { damping: 200 }, durationInFrames: 25 });
```

## 时长计算

转场会使相邻场景重叠，因此总合成长度**小于**所有序列时长的总和。叠加层**不会**影响总时长。

例如，两个 60 帧序列和一个 15 帧转场：

- 无转场：`60 + 60 = 120` 帧
- 有转场：`60 + 60 - 15 = 105` 帧

在另外两个序列之间添加叠加层不会改变总时长。

### 获取转场时长

在时间控制对象上使用 `getDurationInFrames()` 方法：

```tsx
import { linearTiming, springTiming } from "@remotion/transitions";

const linearDuration = linearTiming({
  durationInFrames: 20,
}).getDurationInFrames({ fps: 30 });
// 返回 20

const springDuration = springTiming({
  config: { damping: 200 },
}).getDurationInFrames({ fps: 30 });
// 返回基于弹簧物理计算的时长
```

对于没有显式 `durationInFrames` 的 `springTiming`，时长取决于 `fps`，因为它计算弹簧动画稳定所需的时间。

### 计算合成总时长

```tsx
import { linearTiming } from "@remotion/transitions";

const scene1Duration = 60;
const scene2Duration = 60;
const scene3Duration = 60;

const timing1 = linearTiming({ durationInFrames: 15 });
const timing2 = linearTiming({ durationInFrames: 20 });

const transition1Duration = timing1.getDurationInFrames({ fps: 30 });
const transition2Duration = timing2.getDurationInFrames({ fps: 30 });

const totalDuration =
  scene1Duration +
  scene2Duration +
  scene3Duration -
  transition1Duration -
  transition2Duration;
// 60 + 60 + 60 - 15 - 20 = 145 帧
```
