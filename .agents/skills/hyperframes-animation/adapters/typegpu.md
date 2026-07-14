---
name: hyperframes-typegpu
description: TypeGPU 和原生 WebGPU 适配器模式，用于 HyperFrames。在使用 TypeGPU、原生 WebGPU、WGSL 片段着色器、计算管线、液态玻璃特效、粒子系统或任何由 navigator.gpu 驱动且响应 HyperFrames hf-seek 事件的 canvas 图层时使用。
---

# TypeGPU / WebGPU 用于 HyperFrames

HyperFrames 通过其 `typegpu` 运行时适配器支持 TypeGPU 和原生 WebGPU。适配器不管理你的管线。它发布 HyperFrames 时间并派发一个 seek 事件，让你的组合能够渲染确切的 GPU 帧。

## 渲染环境前提条件（WebGPU + html-in-canvas）

渲染引擎自动将 `--enable-unsafe-webgpu` 和 `--enable-features=CanvasDrawElement` 传递给其 Chrome 启动参数。标准 Chromium 和捆绑的 headless-shell **不支持** WebGPU 与 `drawElementImage` 的组合——这是液态玻璃块（`ios26-liquid-glass`、`macos-tahoe-liquid-glass`、`liquid-glass-*`、`vfx-liquid-glass`）所需的组合。对于这些块，通过设置 `PRODUCER_HEADLESS_SHELL_PATH` 环境变量指向浏览器可执行文件，将引擎指向 Brave（或 Chrome canary），然后再运行 `npx hyperframes render` / `preview`。没有 HTML 作为纹理的纯 TypeGPU 图层在 headless-shell 中工作——只有 html-in-canvas 与 WebGPU 组合需要覆盖设置。

## 约定

- **异步**初始化 WebGPU（`await navigator.gpu.requestAdapter()`），但所有 GSAP 补间必须**同步**注册——在任何 `await` 之前。HyperFrames 播放器在页面加载时立即读取时间线。
- 从 HyperFrames 时间渲染，而非 `performance.now()`。
- 监听 `hf-seek` 事件并在确切时间重新渲染。
- 对 WebGPU 不可用的环境进行防护——适配器不会为你检查。
- 对于视频渲染，在提交 GPU 工作后调用 `await device.queue.onSubmittedWorkDone()`，以确保 canvas 在帧被捕获前已刷新。

适配器设置 `window.__hfTypegpuTime` 并在每次 seek 时派发 `new CustomEvent("hf-seek", { detail: { time } })`。

## 基本模式

```html
<canvas id="gpu-layer"></canvas>
<script>
  (async () => {
    if (!navigator.gpu) return;
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) return;
    const device = await adapter.requestDevice();
    const canvas = document.getElementById("gpu-layer");
    canvas.width = 1920;
    canvas.height = 1080;
    const ctx = canvas.getContext("webgpu");
    const fmt = navigator.gpu.getPreferredCanvasFormat();
    ctx.configure({ device, format: fmt, alphaMode: "opaque" });

    // 构建你的管线、缓冲区、绑定组...
    const timeUniform = new Float32Array([0]);
    const timeBuf = device.createBuffer({
      size: 16,
      usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST,
    });

    function render(t) {
      timeUniform[0] = t;
      device.queue.writeBuffer(timeBuf, 0, timeUniform);
      const enc = device.createCommandEncoder();
      const pass = enc.beginRenderPass({
        colorAttachments: [
          {
            view: ctx.getCurrentTexture().createView(),
            loadOp: "clear",
            clearValue: { r: 0, g: 0, b: 0, a: 1 },
            storeOp: "store",
          },
        ],
      });
      pass.setPipeline(pipeline);
      pass.setBindGroup(0, bindGroup);
      pass.draw(3);
      pass.end();
      device.queue.submit([enc.finish()]);
    }

    render(0);
    window.addEventListener("hf-seek", (e) => render(e.detail.time));
  })();
</script>
```

## 时间线注册

驱动文本、字幕或 HTML 元素的 GSAP 补间必须**同步**注册——在任何 `await` 之前：

```js
const tl = gsap.timeline({ paused: true });

// 字幕补间：同步添加，在 WebGPU 初始化之前
gsap.set(".cap", { opacity: 0 });
tl.to("#cap-1", { opacity: 1, duration: 0.3 }, 1.0);
tl.to("#cap-1", { opacity: 0, duration: 0.2 }, 3.5);

window.__timelines["my-comp"] = tl;

// GPU 相关的补间可以放在异步 IIFE 内部
(async () => {
  // ... WebGPU 初始化 ...
  const proxy = { value: 0 };
  tl.to(proxy, { value: 1, duration: 2, onUpdate: render }, 0.5);
})();
```

## 视频支持的特效（液态玻璃、扭曲）

要将 `<video>` 作为 GPU 输入纹理使用：

```js
const videoEl = document.getElementById("aroll");

// 等待视频元数据后再创建纹理
await new Promise((r) => {
  if (videoEl.readyState >= 1) r();
  else videoEl.addEventListener("loadedmetadata", r, { once: true });
});

// 以视频的原始分辨率创建纹理
const vw = videoEl.videoWidth,
  vh = videoEl.videoHeight;
const bgTex = device.createTexture({
  size: [vw, vh],
  format: "rgba8unorm",
  usage:
    GPUTextureUsage.COPY_DST | GPUTextureUsage.TEXTURE_BINDING | GPUTextureUsage.RENDER_ATTACHMENT,
});

function render(t) {
  try {
    device.queue.copyExternalImageToTexture({ source: videoEl }, { texture: bgTex }, [vw, vh]);
  } catch (_) {
    /* 帧尚未解码 */
  }
  // ... 绘制 ...
}
```

**渲染模式注意：** headless Chrome 可能对 video 元素执行 `copyExternalImageToTexture` 失败。对于生产环境渲染，预先通过 FFmpeg 将关键帧提取为 PNG 并作为图像纹理加载。

## 通过降采样实现的毛玻璃模糊

单通道的高斯核对于玻璃般的毛玻璃效果太弱。使用两遍方法：

1. **通道 1 — 降采样：** 将全分辨率纹理渲染到小纹理（1/6 分辨率）。降采样过程中的双线性滤波自然地对像素进行平均。
2. **通道 2 — 玻璃合成：** 对小纹理采样用于毛玻璃内部（双线性放大 = 重度平滑模糊），对全分辨率纹理采样用于清晰区域和色差折射。

这匹配了 TypeGPU 的 `textureSampleBias` mip 级别方法，而无需生成 mipmap。

## 透明 vs 不透明 Canvas

- **`alphaMode: 'opaque'`** — GPU canvas 渲染完整帧（视频 + 特效）。当 GPU 管线处理所有视觉内容时使用。
- **`alphaMode: 'premultiplied'`** — GPU canvas 在 alpha = 0 处透明，让下方的 HTML 元素透出。用于在常规 `<video>` 元素之上的叠加层（粒子、路径动画）。

## WGSL 全屏三角形

用于全屏效果的标准顶点着色器（无需顶点缓冲区）：

```wgsl
struct Vo { @builtin(position) pos: vec4f, @location(0) uv: vec2f }

@vertex fn vs(@builtin(vertex_index) vi: u32) -> Vo {
  let ps = array<vec2f, 3>(vec2f(-1., -1.), vec2f(3., -1.), vec2f(-1., 3.));
  let ts = array<vec2f, 3>(vec2f(0., 1.), vec2f(2., 1.), vec2f(0., -1.));
  return Vo(vec4f(ps[vi], 0., 1.), ts[vi]);
}
```

使用 `pass.draw(3)` 绘制——一个覆盖视口的三角形。

## 圆角矩形 SDF（液态玻璃圆角）

```wgsl
fn sdf_box(p: vec2f, half_size: vec2f, corner_radius: f32) -> f32 {
  let d = abs(p) - half_size + vec2f(corner_radius);
  return length(max(d, vec2f(0.))) + min(max(d.x, d.y), 0.) - corner_radius;
}
```

使用此函数定义玻璃效果的内部/环形/外部区域。负值表示在形状内部。

## 确定性渲染

- 不要使用 `Math.random()`——使用种子化的 PRNG。
- 渲染循环不要使用 `requestAnimationFrame`——仅响应 `hf-seek` 进行渲染。
- 动画时间不要使用 `performance.now()`——读取 `window.__hfTypegpuTime` 或 `e.detail.time`。
- GPU 提交后，调用 `await device.queue.onSubmittedWorkDone()` 以进行渲染模式帧捕获。
