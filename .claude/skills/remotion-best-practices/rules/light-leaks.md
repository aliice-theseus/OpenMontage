---
name: light-leaks
description: 使用 @remotion/light-leaks 为 Remotion 添加漏光叠加效果
metadata:
  tags: light-leaks, overlays, effects, transitions
---

## 漏光效果

此功能仅适用于 Remotion 4.0.415 及以上版本。使用 `npx remotion versions` 检查 Remotion 版本，使用 `npx remotion upgrade` 升级 Remotion 版本。

`@remotion/light-leaks` 中的 `<LightLeak>` 渲染基于 WebGL 的漏光效果。它在持续时间的前半段逐渐显现，在后半段逐渐消失。

通常用于 `<TransitionSeries.Overlay>` 内部，在两个场景的切换点播放。请参阅 **transitions** 规则了解 `<TransitionSeries>` 和叠加层的用法。

## 前置条件

```bash
npx remotion add @remotion/light-leaks
```

## TransitionSeries 基本用法

```tsx
import { TransitionSeries } from "@remotion/transitions";
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
</TransitionSeries>;
```

## 属性

- `durationInFrames?` — 默认为父序列/合成的持续时间。效果在前半段显现，后半段消失。
- `seed?` — 决定漏光图案的形状。不同的种子值产生不同的图案。默认值：`0`。
- `hueShift?` — 以度数为单位旋转色相（`0`–`360`）。默认值：`0`（黄色到橙色）。`120` = 绿色，`240` = 蓝色。

## 自定义外观

```tsx
import { LightLeak } from "@remotion/light-leaks";

// 蓝色调的漏光，不同图案
<LightLeak seed={5} hueShift={240} />;

// 绿色调的漏光
<LightLeak seed={2} hueShift={120} />;
```

## 独立使用

`<LightLeak>` 也可以在 `<TransitionSeries>` 之外使用，例如作为任何合成中的装饰性叠加层：

```tsx
import { AbsoluteFill } from "remotion";
import { LightLeak } from "@remotion/light-leaks";

const MyComp: React.FC = () => (
  <AbsoluteFill>
    <MyContent />
    <LightLeak durationInFrames={60} seed={3} />
  </AbsoluteFill>
);
```
