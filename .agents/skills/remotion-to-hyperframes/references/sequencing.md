# 序列翻译：Sequence, Series, Composition 根节点

Remotion 的嵌套 `Sequence` 树如何映射到 HF 平面的 `data-start` / `data-duration` 标记，以及单个暂停的 GSAP 时间线。

## 核心思想

Remotion 的 `<Sequence from={F} durationInFrames={D}>` 是一个坐标变换：它将 `useCurrentFrame()` 偏移 `F`，并将子组件裁剪到窗口 `[F, F+D]`。HF 没有每个元素的"当前帧" — 只有一个合成的 seek 时间，运行时根据元素的 `data-start` / `data-duration` 隐藏/显示元素。

结果：嵌套树展平为同一父级下的同级元素列表，每个元素都有自己的时间窗口。

## `<Composition>` → 根节点 `#stage`

```tsx
<Composition
  id="MyVideo"
  component={MyVideo}
  durationInFrames={300}
  fps={30}
  width={1280}
  height={720}
/>
```

```html
<div
  id="stage"
  data-composition-id="MyVideo"
  data-start="0"
  data-duration="10"      <!-- 300/30 -->
  data-fps="30"
  data-width="1280"
  data-height="720"
>
  <!-- 合成内容 -->
</div>
```

`#stage` 上必须要有 `data-start="0"`（运行时需要它来锚定播放；缺失会触发 lint 警告）。

## `<AbsoluteFill>` → 绝对定位的 div

```tsx
<AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>...children...</AbsoluteFill>
```

```html
<div style="position:absolute;inset:0;background-color:#0a0a0a;">...children...</div>
```

`AbsoluteFill` 在 Remotion 中只是一个带样式的 div。翻译为带有 `position:absolute; inset:0` 的 div，并复制任何其他样式属性。

## `<Sequence>` → 带时间窗口的 div

```tsx
<Sequence from={0} durationInFrames={90}>
  <TitleCard />
</Sequence>
```

```html
<div data-start="0" data-duration="3" data-track-index="0">
  <!-- TitleCard 子元素内联 -->
</div>
```

将帧转换为秒：`from/fps`、`durationInFrames/fps`。每个并行渲染层选择一个 `data-track-index`（背景 = 0、叠加层 = 1、音频 = 2 等）。顺序场景可以共享同一个索引。

## 嵌套的 `<Sequence>` 展平

当序列嵌套时，Remotion 会累加偏移量：

```tsx
<Sequence from={60} durationInFrames={120}>
  <Sequence from={30} durationInFrames={60}>
    <ImageScene />
  </Sequence>
</Sequence>
```

内部序列的有效窗口是 `[60+30, 60+30+60] = [90, 150]`。

翻译时计算总和，生成一个具有解析后窗口的 HF div：

```html
<div data-start="3" data-duration="2" data-track-index="0">
  <!-- ImageScene 子元素 -->
</div>
```

## `<Series>` → 带顺序偏移的同级元素

```tsx
<Series>
  <Series.Sequence durationInFrames={60}>
    <A />
  </Series.Sequence>
  <Series.Sequence durationInFrames={120}>
    <B />
  </Series.Sequence>
  <Series.Sequence durationInFrames={90}>
    <C />
  </Series.Sequence>
</Series>
```

每个 `Sequence.Sequence` 位于下一个时间槽。生成累加 `data-start` 的同级元素：

```html
<div data-start="0" data-duration="2" data-track-index="0">A</div>
<div data-start="2" data-duration="4" data-track-index="0">B</div>
<div data-start="6" data-duration="3" data-track-index="0">C</div>
```

## 场景边界的交叉淡入淡出

Remotion `<Sequence>` 默认在硬边界处显示/隐藏。HF 也是如此 — 但如果你的合成需要在场景之间平滑淡入淡出，你必须使用 GSAP 在边界处显式驱动透明度：

```js
const tl = gsap.timeline({ paused: true });
tl.set(scene1, { opacity: 1 }, 0);
tl.set(scene1, { opacity: 0 }, 2); // 在 2 秒处硬切换
tl.set(scene2, { opacity: 1 }, 2);
```

对于 0.5 秒的交叉淡入淡出：

```js
tl.to(scene1, { opacity: 0, duration: 0.5 }, 1.5);
tl.to(scene2, { opacity: 1, duration: 0.5 }, 1.5);
```

关于 Remotion `<TransitionSeries>` 的翻译，参见 [transitions.md](transitions.md)。

## `<Loop>`

```tsx
<Loop durationInFrames={30}>
  <Spinner />
</Loop>
```

HF 没有 `<Loop>` 原语。翻译为带有 `repeat: -1` 的 GSAP 时间线：

```js
const spinTl = gsap.timeline({ paused: true, repeat: -1, repeatRefresh: false });
spinTl.to(spinner, { rotate: 360, duration: 1.0, ease: "none" });
// 在正确的偏移处嵌入主合成时间线：
mainTl.add(spinTl, 3);
```

这有点脆弱 — Remotion 的 `<Loop>` 在每次迭代时重置内部状态，GSAP 的 repeat 也是如此，但如果循环子元素有自己的动画，你需要小心地根据需要打开或关闭 GSAP 的 `repeatRefresh`。对于大多数简单的"永远旋转"情况，这是可以的。

## `<Freeze>`

```tsx
<Freeze frame={30}>
  <Animated />
</Freeze>
```

丢弃包装器。`<Freeze>` 将子元素的 `useCurrentFrame()` 固定为一个常数值 — 但在 HF 中，子元素的动画已经由显式的 GSAP 补间驱动，因此 freeze 翻译为"不对这个元素做补间"。

## 多个并行轨道

当你有背景视频 + 叠加文本 + 音频同时播放时，使用不同的 `data-track-index` 值：

```html
<div data-track-index="0">背景视频</div>
<div data-track-index="1">叠加文本</div>
<audio data-track-index="2" ...></audio>
```

运行时从索引中确定轨道顺序。参见 [media.md](media.md) 了解媒体特定的轨道约定。
