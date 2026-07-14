# 翻译限制

此技能明确无法翻译的内容，与阻断器列表（由 `lint_source.py` 强制执行）分开。这些是_已知_差距 — 在翻译周围合成时，将它们作为翻译说明告知用户。

## 技能拒绝的 React 模式

参见 [escape-hatch.md](escape-hatch.md)。以下任一情况都会触发退出：

- `useState`、`useReducer` 驱动动画
- 带非空依赖的 `useEffect` / `useLayoutEffect`（副作用）
- 异步 `calculateMetadata`
- 第三方 React UI 库（MUI、Chakra、Mantine、antd、shadcn、Radix、NextUI）

`@remotion/lambda` 不再在此列表中 — 它是警告而非阻断器，因为 Lambda 配置与合成渲染是正交的。该技能会丢弃 imports 和 `renderMediaOnLambda(...)` 调用，并写入 `TRANSLATION_NOTES.md` 条目。参见 [escape-hatch.md](escape-hatch.md)。

## 有注意事项的模式

### `<Audio>` 上的音量渐变

Remotion 接受 `volume` 的函数形式：

```tsx
<Audio src={...} volume={(f) => interpolate(f, [0, 30], [0, 1])} />
```

HF 仅支持静态 `data-volume`。翻译：在翻译时使用 `ffmpeg afade` 将渐变烘焙到音频文件中，或者丢弃渐变并附带说明。丢弃渐变的方式会产生听觉上不同的输出，但视频视觉上相同，因此 SSIM 可以通过 — 只需标记它即可。

### 带有状态子元素的 `<Loop>`

```tsx
<Loop durationInFrames={30}>
  <CounterThatIncrementsViaUseRef />
</Loop>
```

使用 `repeat: -1` 的循环适用于_视觉_重复。如果循环的子元素有跨迭代状态（计数器、随机种子），HF 不会在每次迭代中完全相同地重现它。除非子元素每次迭代完全确定，否则退出。

### Remotion 带有 crossOrigin 的 `<Img>`

```tsx
<Img src="https://other-domain.com/x.png" crossOrigin="anonymous" />
```

HF 的渲染器不像 Remotion 那样强制执行 CORS。大多数公共图片可以工作；带有认证头的私有图片则不行。如果源码使用 `crossOrigin="use-credentials"`，则需要在翻译时下载资源并将其内联。

### `<TransitionSeries>` 中的自定义 `presentation`

```tsx
const customPresentation: PresentationComponent = ({ children, presentationProgress }) => {
  return <div style={{ filter: `blur(${(1 - presentationProgress) * 20}px)` }}>{children}</div>;
};
```

纯粹的 presentations（从进度计算变换/滤镜/透明度）可以干净地翻译为 GSAP 补间。在内部读取 `useCurrentFrame()` 或具有状态子元素的 presentations 则不行 — 退出。

### 代码分割组件（`React.lazy`）

```tsx
const HeavyChart = React.lazy(() => import("./HeavyChart"));
```

`React.lazy` 是异步的，不适用于确定性渲染模型。翻译为常规 import；生成的 HF 合成将直接包含所有代码。

## 始终有效的模式

- `<AbsoluteFill>` 和 `<Sequence>`（任意嵌套）
- `useCurrentFrame()` 推导：`interpolate`、`spring`、`Easing`、`interpolateColors`、手动计算
- 带简单属性的 `<Audio>`、`<Video>`、`<Img>`、`<IFrame>`
- `staticFile()` 引用
- 作为属性的纯函数的自定义 React 子组件
- 作为 `useCurrentFrame` 的纯推导的自定义 hooks
- `@remotion/lottie`（翻译为 HF 的 Lottie 适配器）
- `@remotion/google-fonts/<Family>`（翻译为 `<link>` 或 `@font-face`）
- 同步 `calculateMetadata`（在翻译时解析）
- 带内置 presentations 的 `<TransitionSeries>`（`fade`、`slide`、`wipe`、`clockWipe`、`flip`、`iris`）

## 技能从不尝试翻译的内容

这些是设计上超出范围的：

- **HDR 渲染** — HF 支持 HDR，但 Remotion 不支持，因此没有什么可翻译的。
- **可变帧率** — 两个工具都假设恒定的 fps。
- **多合成 `<Composition>` 列表** — 一次翻译一个。技能会提示用户选择哪个合成。
- **Remotion Studio 属性面板** — HF Studio 中的可视化属性编辑需要不同的基础设施；超出范围。

## 向用户报告差距

当翻译产生了_某些东西_但结果存在差距时，在输出旁边写入 `TRANSLATION_NOTES.md`：

```markdown
# 翻译说明

以下 Remotion 模式在翻译时存在注意事项：

- `<Audio volume={(f) => ...}>`（第 15 行）：音量渐变已丢弃 — 添加了静态 `data-volume="0.5"`。要保留渐变，请运行 `ffmpeg -i music.wav -af "afade=t=in:st=0:d=1" music.faded.wav` 并替换源文件。
- `<HeavyChart>`（第 30 行）：以内联 HTML 翻译。原始的 React.lazy 边界已被丢弃 — 包大小不变，因为 HF 提供单个 HTML 文件。

如果这些注意事项中的任何一个很重要，可以考虑改用运行时互操作模式。
```

此文件由技能在 HF 输出旁生成，而不是保存在语料库中。
