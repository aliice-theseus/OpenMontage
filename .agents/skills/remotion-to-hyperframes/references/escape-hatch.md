# 何时退出：运行时互操作模式

有些 Remotion 合成无法被干净翻译。该技能应提前识别它们，并推荐来自 [PR #214](https://github.com/heygen-com/hyperframes/pull/214) 的**运行时互操作模式**，而不是生成有问题的 HTML。

## 何时推荐互操作

首先运行 `scripts/lint_source.py`。如果它返回任何阻断器，推荐互操作。阻断器包括：

| 规则                           | 捕获内容                                                       |
| ------------------------------ | -------------------------------------------------------------- |
| `r2hf/use-state`               | useState 驱动动画                                               |
| `r2hf/use-reducer`             | useReducer 驱动动画                                             |
| `r2hf/use-effect-deps`         | 带非空依赖的 useEffect/useLayoutEffect（副作用）                 |
| `r2hf/async-metadata`          | calculateMetadata 返回 Promise                                  |
| `r2hf/third-party-react-ui`    | 从 MUI、Chakra、Mantine、antd、shadcn、Radix、NextUI 导入       |

这些都会破坏 HF 依赖的 seek 驱动、确定性帧模型。翻译它们会产生静默错误的输出。

## 互操作模式的实际作用

根据 [PR #214](https://github.com/heygen-com/hyperframes/pull/214)，运行时适配器：

1. 通过 esbuild 将用户的 Remotion 代码与 React + `@remotion/player` 打包。
2. 在 HF 合成的 HTML 内部挂载一个 Remotion `<Player>`。
3. 在挂载时暂停播放器。
4. 在 `window.__hfRemotion` 上注册播放器，包含 `seekTo(frame)`、`pause()`、`durationInFrames`、`fps`。
5. HF 的渲染循环通过 `seekTo(frame)` 逐帧定位播放器。

结果：Remotion 的 React 树在 HF 的确定性帧节拍下渲染。自定义 hooks、useState、useEffect、MUI 组件 — 一切正常，因为 Remotion 的 React 协调器在执行渲染。

## 建议消息

当技能检测到阻断器时，输出类似以下内容：

> Remotion 源码使用了 `useState`（及其他），这无法翻译为 HF 的 seek 驱动 HTML 模型。推荐路径是 **运行时互操作模式**：将你的 Remotion 代码与 `@remotion/player` 打包，让 HF 逐帧驱动它。
>
> 参见 https://github.com/heygen-com/hyperframes/pull/214 了解完整实现。快速摘要：
>
> 1. 使用 esbuild 打包 `entry.tsx`：`npx esbuild entry.tsx --bundle --outfile=dist/bundle.js --format=iife --jsx=automatic`
> 2. 挂载 Player 并在 `window.__hfRemotion` 上注册：
>
>    ```tsx
>    const playerRef = useRef<PlayerRef>(null);
>    useEffect(() => {
>      playerRef.current?.pause();
>      window.__hfRemotion = window.__hfRemotion || [];
>      window.__hfRemotion.push({
>        seekTo: (f) => playerRef.current?.seekTo(f),
>        pause: () => playerRef.current?.pause(),
>        durationInFrames,
>        fps,
>      });
>    }, []);
>    ```
>
> 3. 从你的 HF `index.html` 引用该 bundle 并正常渲染：`<script src="dist/bundle.js"></script>`

## lint 输出已包含建议

`lint_source.py` 为每个发现发出 `recommendation` 字段。逐字呈现它们 — 它们针对每个阻断器规则进行了调优：

```json
{
  "rule": "r2hf/use-state",
  "message": "检测到 useState — 通过 React 状态驱动动画的 Remotion 合成在 HyperFrames 中不是确定性帧捕获目标",
  "recommendation": "使用 PR #214 中的运行时互操作模式，而不是尝试翻译"
}
```

## 何时不退出：仅警告

有些模式产生的是警告而非阻断器 — 丢弃包装器后进行翻译：

| 规则                        | 操作                                                              |
| --------------------------- | ----------------------------------------------------------------- |
| `r2hf/lambda-import`        | 丢弃 `@remotion/lambda` 配置；HF 单机运行，记录差距                |
| `r2hf/delay-render`         | 丢弃调用；HF 处理资源就绪                                           |
| `r2hf/use-callback`         | 丢弃包装器，内联函数                                               |
| `r2hf/use-memo`             | 丢弃包装器，直接计算                                               |
| `r2hf/custom-hook`（纯函数）| 如果是 `useCurrentFrame` 的推导，内联 hook 体                       |
| `r2hf/static-file`          | 将 `staticFile("x")` 替换为 `"assets/x"`                          |
| `r2hf/interpolate-colors`   | 翻译为 GSAP 颜色补间（参见 [timing.md](timing.md)）                |

这些在 T4 案例 05–07 中有文档记录。

`r2hf/lambda-import` 是警告而非阻断器 — 因为 Lambda 配置与合成本身是正交的。翻译一个其他方面都干净的 Remotion 合成不应仅仅因为作者还配置了 AWS Lambda 用于分布式渲染而失败。该技能在步骤 3（生成）中丢弃 `@remotion/lambda` 导入和 `renderMediaOnLambda(...)` 调用，并写入 `TRANSLATION_NOTES.md` 条目，以便用户知道需要单独设置 HF 渲染。

## 当源码同时包含阻断器和警告

退出。单个阻断器的存在意味着技能不应尝试翻译 — 即使合成的其余部分是干净的。用户应该对整个内容使用互操作，或者先从 Remotion 源码中重构掉阻断器模式。
