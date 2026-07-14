---
name: sequencing
description: Remotion 的序列编排模式 - 延迟、裁剪、限制项目时长
metadata:
  tags: sequence, series, timing, delay, trim
---

使用 `<Sequence>` 来延迟元素在时间线中出现的时间。

```tsx
import { Sequence } from "remotion";

const {fps} = useVideoConfig();

<Sequence from={1 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Title />
</Sequence>
<Sequence from={2 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Subtitle />
</Sequence>
```

默认情况下，这会将组件包裹在一个绝对填充元素中。  
如果项目不应被包裹，请使用 `layout` 属性：

```tsx
<Sequence layout="none">
  <Title />
</Sequence>
```

## 预挂载

这会在组件实际播放之前在时间线中加载它。  
始终预挂载任何 `<Sequence>`！

```tsx
<Sequence premountFor={1 * fps}>
  <Title />
</Sequence>
```

## 系列

当元素应按顺序播放而不重叠时，使用 `<Series>`。

```tsx
import { Series } from "remotion";

<Series>
  <Series.Sequence durationInFrames={45}>
    <Intro />
  </Series.Sequence>
  <Series.Sequence durationInFrames={60}>
    <MainContent />
  </Series.Sequence>
  <Series.Sequence durationInFrames={30}>
    <Outro />
  </Series.Sequence>
</Series>;
```

与 `<Sequence>` 相同，使用 `<Series.Sequence>` 时，默认情况下项目会被包裹在绝对填充元素中，除非 `layout` 属性设置为 `none`。

### 重叠的系列

使用负偏移量实现重叠序列：

```tsx
<Series>
  <Series.Sequence durationInFrames={60}>
    <SceneA />
  </Series.Sequence>
  <Series.Sequence offset={-15} durationInFrames={60}>
    {/* 在 SceneA 结束前 15 帧开始 */}
    <SceneB />
  </Series.Sequence>
</Series>
```

## 序列内部的帧引用

在 Sequence 内部，`useCurrentFrame()` 返回局部帧（从 0 开始）：

```tsx
<Sequence from={60} durationInFrames={30}>
  <MyComponent />
  {/* 在 MyComponent 内部，useCurrentFrame() 返回 0-29，而不是 60-89 */}
</Sequence>
```

## 嵌套序列

序列可以嵌套以实现复杂的时间控制：

```tsx
<Sequence from={0} durationInFrames={120}>
  <Background />
  <Sequence from={15} durationInFrames={90} layout="none">
    <Title />
  </Sequence>
  <Sequence from={45} durationInFrames={60} layout="none">
    <Subtitle />
  </Sequence>
</Sequence>
```

## 在一个合成中嵌套另一个合成

要在另一个合成中添加合成，可以使用带有 `width` 和 `height` 属性的 `<Sequence>` 组件来指定合成的尺寸。

```tsx
<AbsoluteFill>
  <Sequence width={COMPOSITION_WIDTH} height={COMPOSITION_HEIGHT}>
    <CompositionComponent />
  </Sequence>
</AbsoluteFill>
```
