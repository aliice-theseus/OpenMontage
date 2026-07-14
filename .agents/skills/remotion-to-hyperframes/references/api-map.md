# Remotion → HyperFrames API 映射

权威翻译对照表。开始翻译时加载此参考以了解高层映射；对于较为脆弱的细节（时间、过渡等），加载按主题分类的参考。

## 阅读此表

- **`drop`** = 从输出中完全移除。HF 运行时会处理。
- **`see references/X.md`** = 映射非平凡；阅读链接的文件。
- **`refuse + interop`** = 技能退出并推荐来自 [PR #214](https://github.com/heygen-com/hyperframes/pull/214) 的运行时适配器模式。

## 合成根节点

| Remotion                                             | HyperFrames                                                                                                                   |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `<Composition id durationInFrames fps width height>` | 根 `<div id="stage" data-composition-id data-start="0" data-duration="<dur/fps>" data-fps data-width data-height>`            |
| `defaultProps={...}`                                 | `#stage` 上的 `data-*` 属性（每个标量 prop 一个）。嵌套对象/数组 — 参见 [parameters.md](parameters.md)                            |
| `schema={z.object(...)}`                             | 不在 HTML 中表示；schema 仅存在于代理的翻译步骤中                                                                              |
| `calculateMetadata`（同步）                           | 在翻译时解析，将具体值写入 `data-*`                                                                                            |
| `calculateMetadata`（异步）                           | **拒绝 + 互操作** — 参见 [escape-hatch.md](escape-hatch.md)                                                                   |
| `registerRoot(RemotionRoot)`                         | drop                                                                                                                          |
| `<AbsoluteFill style>`                               | `<div style="position:absolute;inset:0;{style}">`                                                                             |

## 序列

有关嵌套和交错详情，参见 [sequencing.md](sequencing.md)。

| Remotion                                   | HyperFrames                                                                                              |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `<Sequence from={F} durationInFrames={D}>` | `<div data-start="<F/fps>" data-duration="<D/fps>" data-track-index="N">`                                |
| `<Series>` + `<Series.Sequence>`           | 具有顺序 `data-start` 值的同级元素                                                                        |
| `<Loop durationInFrames={D}>`              | 非原语 — 生成自定义 GSAP `repeat: -1` 循环，带手动偏移计算                                                |
| `<Freeze frame={F}>`                       | 丢弃包装器；HF 在 seek 驱动的时间线之外没有运行中的动画，因此 freeze 是无操作                              |

## 时间

参见 [timing.md](timing.md) — 这是最高杠杆率的部分。

| Remotion                                                   | HyperFrames                                                                                                                  |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `useCurrentFrame()`                                        | drop — HF 定位时间线。从 `frame` 派生出的数学计算成为暂停 GSAP 补间的可动画属性。                                              |
| `useVideoConfig()` 获取 `fps` / `durationInFrames`          | drop — 从 `#stage` 上的 `data-fps` / `data-duration` 读取                                                                    |
| `interpolate(frame, [a,b], [x,y])`（线性）                   | `gsap.fromTo(t, {p:x}, {p:y, duration:(b-a)/fps, ease:"none"})` 在偏移 `a/fps` 处                                            |
| `interpolate(frame, [a,b,c,d], [x,y,y,z])`（多段）          | 在偏移 `a/fps`、`b/fps`、`c/fps` 处的三个 `gsap.to` 调用                                                                     |
| `interpolate(..., {easing: Easing.bezier})`                | GSAP `CustomEase.create("c", "M0,0 C${a},${b} ${c},${d} 1,1")`                                                               |
| `spring({frame, fps, config: {damping, stiffness, mass}})` | GSAP `back.out(N)` — 参见 [timing.md](timing.md) 了解阻尼 → 过冲对照表                                                       |
| `interpolateColors(frame, range, colors)`                  | `gsap.to({...}, { backgroundColor, color, duration, ease })` — GSAP 原生处理颜色补间                                          |
| `Easing.in / .out / .inOut(power)`                         | GSAP `power<N>.in` / `power<N>.out` / `power<N>.inOut`                                                                       |

## 媒体

修剪、音量渐变和编解码器说明参见 [media.md](media.md)。

| Remotion                               | HyperFrames                                                                            |
| -------------------------------------- | -------------------------------------------------------------------------------------- |
| `<Audio src volume>`                   | `<audio data-start data-duration data-track-index data-volume src>`                    |
| `<Audio playbackRate startFrom endAt>` | `data-playback-rate`、`data-trim-start`、`data-trim-end`                              |
| `<Video src>`                          | `<video muted playsinline data-start data-duration data-track-index src>`              |
| `<OffthreadVideo>`                     | `<video>` — HF 不需要离线程变体（使用无头 Chrome）                                      |
| `<Img src>`                            | `<img>`                                                                                |
| `<IFrame src>`                         | `<iframe>` — HF 自动回退到嵌套 iframe 的截图模式                                        |
| `staticFile("x.png")`                  | `"assets/x.png"` — 将文件复制到 `hf-src/assets/`，与 `index.html` 同级                 |
| `delayRender()` / `continueRender()`   | drop — HF 通过 Frame Adapter 模式等待资源就绪                                            |

## 过渡

参见 [transitions.md](transitions.md)。

| Remotion                                                                       | HyperFrames                                                                                                |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| `<TransitionSeries>` + `<TransitionSeries.Transition presentation={fade()} />` | 在边界处手动 `gsap.to(scene, {opacity: 0/1, duration})` 交叉淡入淡出                                       |
| `slide()`、`wipe()`、`clockWipe()`、`fade()`                                   | HF [着色器过渡](https://hyperframes.heygen.com/catalog/blocks) 包预设 — 选择最接近的                       |
| `linearTiming({durationInFrames})`                                             | 持续时间为秒（`/fps`）                                                                                     |
| `springTiming({config})`                                                       | 持续时间为秒，缓动 `back.out` — 参见 [timing.md](timing.md)                                                |

## Lottie

参见 [lottie.md](lottie.md)。

| Remotion                        | HyperFrames                                                                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `<Lottie animationData={data}>` | `<div id="lottie-N">` + `<script>const anim = lottie.loadAnimation({...}); window.__hfLottie.push(anim)</script>`        |
| `loop` / `playbackRate` props   | 仅在检查播放器定位行为后翻译；HF 适配器通过 `goToAndStop` 定位绝对时间                                                    |
| `@remotion/lottie` runtime      | 来自 CDN 的 `lottie-web` — 丢弃 React 包装器                                                                              |

## 字体

参见 [fonts.md](fonts.md)。

| Remotion                                            | HyperFrames                                                                                            |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `loadFont()` 来自 `@remotion/google-fonts/<Family>` | 引用 Google Fonts CSS 的 `@font-face` 规则，或在 `<head>` 中指向 Google Fonts 的 `<link>`              |
| 通过 `@font-face` 的本地字体                         | 相同 — 将规则粘贴到 `<style>` 中                                                                        |
| 系统字体回退                                        | 记录字体回退差异成本（参见 [eval.md](eval.md)）                                                        |

## 参数

参见 [parameters.md](parameters.md)。

| Remotion                      | HyperFrames                                                                                    |
| ----------------------------- | ---------------------------------------------------------------------------------------------- |
| `z.object({foo: z.string()})` | `#stage` 上的 `data-foo`（schema 隐式包含在 HTML 结构中）                                       |
| 嵌套数组属性（`stats[]`）      | 带每个实例 `data-*` 属性的重复 HTML 标记                                                         |
| Zod 默认值                    | 将默认值直接烘焙到 HTML 中                                                                       |
| Zod 运行时验证                 | 不表示；如果需要验证，在生成 HTML 之前的翻译步骤中进行验证                                        |

## React 模式

| Remotion                                           | HyperFrames                                                           |
| -------------------------------------------------- | --------------------------------------------------------------------- |
| 自定义 React 子组件（纯函数，属性驱动）              | 使用 prop 接口作为模板，内联为重复 HTML                                |
| `useState` 驱动动画                                | **拒绝 + 互操作**                                                     |
| `useReducer` 驱动动画                              | **拒绝 + 互操作**                                                     |
| `useEffect(fn, [deps])`（非空依赖）                 | **拒绝 + 互操作**                                                     |
| `useEffect(fn, [])`（仅挂载一次的副作用）            | 丢弃 effect；如果需要启动工作，使用 `queueMicrotask`                   |
| `useCallback`、`useMemo`                           | 丢弃包装器 — 装饰性                                                   |
| 自定义 hook（`useCurrentFrame` 的纯推导）            | 内联函数体                                                            |
| 带有状态/效果的自定义 hook                          | 拒绝 + 互操作                                                         |

## 分布式渲染

`@remotion/lambda` 和 `@remotion/cloudrun` 是部署配置 — 与合成本身正交。技能将其作为**警告**（而非阻断器）发出，在步骤 3（生成）中丢弃它们，并在 `TRANSLATION_NOTES.md` 中附注说明。HF 目前是单机运行；记录此差距。

| Remotion                   | HyperFrames                                            |
| -------------------------- | ------------------------------------------------------ |
| `@remotion/lambda` 导入    | 丢弃导入（警告 `r2hf/lambda-import`）                   |
| `renderMediaOnLambda(...)` | 丢弃调用；在 `TRANSLATION_NOTES.md` 中注明              |
| `@remotion/cloudrun`       | 丢弃导入 + 调用；在 `TRANSLATION_NOTES.md` 中注明       |

## 何时完全退出

如果存在任何阻断器模式，推荐来自 [PR #214](https://github.com/heygen-com/hyperframes/pull/214) 的运行时互操作模式，而不是尝试翻译。参见 [escape-hatch.md](escape-hatch.md)。

阻断器在 [`scripts/lint_source.py`](../scripts/lint_source.py) 中有文档记录，并由 [tier-4-escape-hatch](../assets/test-corpus/tier-4-escape-hatch/) 测试。
