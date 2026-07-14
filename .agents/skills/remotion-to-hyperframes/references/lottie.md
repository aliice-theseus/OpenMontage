# Lottie 翻译：@remotion/lottie → HF lottie 适配器

Lottie 动画是一个干净的翻译案例 — HF 有一个内置的 [Lottie 适配器](https://github.com/heygen-com/hyperframes/blob/main/packages/core/src/runtime/adapters/lottie.ts)，同时支持 `lottie-web` 和 `@lottiefiles/dotlottie-web`。适配器自动发现注册在 `window.__hfLottie` 上的动画，并通过 `goToAndStop` 逐帧定位。

## 模式

```tsx
import { Lottie } from "@remotion/lottie";
import animationData from "./hello.json";

export const MyComp = () => (
  <AbsoluteFill>
    <Lottie animationData={animationData} loop={false} />
  </AbsoluteFill>
);
```

翻译为：

```html
<div id="stage" ...>
  <div id="lottie-anim" style="width:100%;height:100%"></div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
  <script>
    const anim = lottie.loadAnimation({
      container: document.getElementById("lottie-anim"),
      renderer: "svg",
      loop: false,
      autoplay: false,
      path: "assets/hello.json",
    });
    window.__hfLottie = window.__hfLottie || [];
    window.__hfLottie.push(anim);
  </script>
</div>
```

与典型 Lottie 嵌入的关键区别：

- `autoplay: false` — HF 通过定位来驱动播放
- `loop: false` 通常如此（除非 Remotion 的 `loop={true}`）
- `window.__hfLottie.push(anim)` 是将动画钩入 HF 逐帧定位的机制

## 资源处理

Remotion 通过 webpack 导入打包动画 JSON。HF 需要 JSON 在磁盘上的 `assets/` 目录下，并通过路径引用：

1. 将 `hello.json` 从 Remotion 项目复制到 `hf-src/assets/`。
2. 在 `loadAnimation` 中引用为 `path: "assets/hello.json"`。

对于 dotlottie（二进制）格式，替换为 `@lottiefiles/dotlottie-web`：

```html
<script src="https://unpkg.com/@lottiefiles/dotlottie-web"></script>
<canvas id="anim" style="width:100%;height:100%"></canvas>
<script>
  const player = new DotLottie({
    canvas: document.getElementById("anim"),
    src: "assets/hello.lottie",
    autoplay: false,
  });
  window.__hfLottie = window.__hfLottie || [];
  window.__hfLottie.push(player);
</script>
```

HF 适配器处理两种播放器 API（它通过鸭子类型识别 `goToAndStop` 与 `setCurrentRawFrameValue` / `seek`）。

## 多个 Lottie 动画

一个合成中的多个 `<Lottie>` 实例可以工作 — 将每个实例推送到 `window.__hfLottie`，适配器将同步定位所有实例：

```js
window.__hfLottie.push(anim1);
window.__hfLottie.push(anim2);
window.__hfLottie.push(anim3);
```

## Lottie 源实际上不是翻译阻塞

Lottie 动画编码了它们自己确定性的时间线。它们是 Remotion 合成中最_容易_翻译的部分，因为动画逻辑已经是自包含的 — Remotion 和 HF 都不"动画化"它们，两者都只是定位它们。翻译成本接近于零。

## After Effects → Lottie 限制

Lottie 支持 After Effects 功能的一个子集。表达式、大多数效果（投影、颜色叠加）、Normal/Add/Multiply 之外的所有混合模式、亮度蒙版和大多数 3D 参数都不支持。如果 Remotion 合成使用了依赖这些功能的 Lottie 文件，动画在 Remotion 和 HF 中都会出现问题 — 这不是翻译问题，而是 Lottie 的限制。参见 [airbnb/lottie/after-effects.md](https://github.com/airbnb/lottie/blob/master/after-effects.md) 了解完整的功能支持列表。

## 循环行为

Remotion 的 `loop={true}` 会连续播放动画。只有在检查生成的帧之后，才将其翻译为播放器选项。HF 适配器定位绝对合成时间；它不会在播放器之上添加模运算循环或播放速率缩放。对于精确的重复循环或非默认播放速率，将时间烘焙到 Lottie 资源中，或围绕 Lottie 层编写显式的时间线，并验证渲染输出。

## 性能说明

根据 [Lottie 适配器](https://github.com/heygen-com/hyperframes/blob/main/packages/core/src/runtime/adapters/lottie.ts) 文档：lottie-web 的 `goToAndStop(time, isFrame=false)` 接受以毫秒为单位的时间；适配器传递 `time * 1000` 以确保精度。这比传递帧号更精确（特别是对于内部 fps 与 HF 渲染 fps 不匹配的动画）。
