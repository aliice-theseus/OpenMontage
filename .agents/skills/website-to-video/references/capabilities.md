# HyperFrames — 完整能力清单

今天工作区中 HyperFrames 能实现的所有功能，综合了所有 7 个包、16 个技能和完整注册表的直接源码阅读。

> **如何阅读此文件。** 首先扫描下面的**目录**。**不要线性阅读此文件**——它是 700+ 行的清单；每次会话都从头到尾阅读浪费上下文。当故事板或特定节拍需要某种能力（HTML-in-Canvas、着色器过渡、音频响应、动态计数器等）时，直接跳到该章节。

你不局限于从网站捕获的内容。你可以从头创建着色器、搜索并下载注册表块、构建 Three.js 场景、编写自定义 WebGL 效果、使用任何 Web API——浏览器能渲染的任何内容。

关于实现模式（工作代码），参见 `techniques.md`。此文件是 WHAT；techniques.md 是 HOW。

## 基本规则

- **确定性：** 没有 `Math.random()`，没有 `Date.now()`，没有 `requestAnimationFrame`，没有 `repeat: -1`。渲染引擎在精确的时间戳上定位。
- **时间线约定：** `window.__timelines["composition-id"] = tl` 必须同步设置。时间线长度定义作品时长。
- **子作品：** 通过 `data-composition-src` 加载的外部 `.html` 文件。自动嵌套时间线、作用域 CSS、作用域脚本。
- **检查器：** 60+ 条规则。在渲染前运行 `npx hyperframes lint`。捕获缺失时间线、重叠片段、路径损坏、GSAP 错误。

## 目录

| # | 章节 | 内容 |
| --- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | **作品基础** | 数据属性、时间线约定、分辨率预设（1080p、4K、竖屏、方形、自定义） |
| 2 | **动画引擎（6 个适配器）** | GSAP + 15 个插件、Anime.js v4、CSS @keyframes、WAAPI、Lottie（lottie-web + dotlottie）、Three.js（hf-seek 事件） |
| 3 | **着色器过渡（14 个 WebGL）** | domain-warp、ridged-burn、whip-pan、sdf-iris、ripple-waves、gravitational-lens、cinematic-zoom、chromatic-split、swirl-vortex、thermal-distortion、flash-through-white、cross-warp-morph、light-leak、glitch——加上自定义 GLSL |
| 4 | **CSS 场景过渡（30+）** | 推/滑动、缩放/放大、径向/剪辑、3D 翻转、模糊、溶解、覆盖/百叶窗、漏光/烧灼、扭曲/故障、机械/快门、网格溶解、破坏/燃烧、VHS/重力/变形——6 种时序预设 |
| 5 | **视觉效果 + 纹理** | 文本标记（高亮、圆形、爆发、涂鸦、草图轮廓）、颗粒/噪点、漏光、胶片烧灼、暗角、光晕、纸张纹理、闪光扫光 |
| 6 | **字幕技术** | 逐词卡拉 OK、强度层级、5 种退出风格、6 种语调映射、逐词样式触发器、7 种音频源格式、定位辅助 |
| 7 | **音频响应动画** | 贝斯→缩放、中频→形状、高音→光晕；任何 GSAP 属性；频段提取脚本；禁止模式 |
| 8 | **HTML-in-canvas** | 实时 DOM 作为 GPU 纹理（drawElementImage）、Three.js 平面、HTML 上的 WebGL 着色器、7 个 VFX 块（iPhone/MacBook 设备、液体、玻璃、磁性、传送门、粉碎、文本光标） |
| 9 | **Three.js / WebGL 自定义场景** | 完整 3D：AnimationMixer、自定义 GLSL、后处理、GLTF 模型、灯光、相机、材质——所有通过 hf-seek 实现确定性 |
| 10 | **SVG / canvas / 可变字体** | SVG 路径绘制、Canvas 2D 程序化艺术、CSS 3D 卡片、逐词输入、可变字体轴、字符打字、速度匹配切割、MotionPath |
| 11 | **媒体：视频、音频、TTS** | 视频合成 + 帧注入、音频混音器（多轨）、Kokoro TTS（54 个语音、9 种语言）、Whisper/Groq/OpenAI 转录、背景去除（u2net） |
| 12 | **注册表（51 个块 + 4 个组件 + 8 个示例）** | 社交叠加（8）、展示（5）、数据可视化（2）、Logo 品牌（1）、3D/VFX（7）、着色器过渡（14）、过渡画廊（13）、组件（颗粒、闪光、像素化、纹理遮罩）、8 个入门示例 |
| 13 | **CLI（25 个命令）** | init、add、catalog、play、preview、publish、render（MP4/WebM/MOV/PNG、HDR、GPU、并行）、lint、validate、inspect、snapshot、capture、tts、transcribe、remove-background、doctor 等 |
| 14 | **检查器（60+ 条规则）** | 核心、媒体、GSAP、字幕、作品、适配器、纹理、字体——加上异步 URL 检查 |
| 15 | **播放器 Web 组件** | `<hyperframes-player>` 带 seek/play/pause API、11 个事件、媒体镜像、运行时自动注入 |
| 16 | **引擎 + 生成器** | MP4/WebM/MOV/PNG 输出、HDR（PQ/HLG）、透明度（ProRes）、GPU 编码（NVENC/VideoToolbox/VAAPI/QSV）、并行渲染、视频帧注入 |
| 17 | **Studio（浏览器内 NLE）** | 时间线编辑器、拖放/调整片段、资源浏览器、渲染队列、检查模态框、字幕编辑器、元素选择器 |
| 18 | **确定性保证** | 没有 Math.random、没有 Date.now、没有 RAF、没有 repeat:-1、没有回调、同步构建 |
| 19 | **变量 / 参数化** | 类型化运行时变量（string、color、number、boolean、enum）、CLI 覆盖、严格验证 |
| 20 | **子作品** | 外部文件或内联模板、自动嵌套时间线、作用域 CSS、作用域脚本、变量继承 |
| 21 | **全局运行时 API** | 25+ 个 window 全局对象，用于时间线、播放器、变量、适配器、钩子 |
| 22 | **技能（16 个）** | hyperframes、cli、media、registry、contrast、animation-map、website-to-video、remotion、gsap、animejs、css-animations、waapi、lottie、three、tailwind、contribute-catalog |
| 23 | **参考（15 个文档）** | transitions、css-patterns、dynamic-techniques、motion-principles、typography、narration、captions、audio-reactive、transcript-guide、techniques、beat-direction、visual-styles 等 |
| 24 | **文档（27 页）** | 指南 + 包文档涵盖渲染、HDR、html-in-canvas、性能、提示、故障排除等 |

---

## 1. 作品基础

### 运行时识别的数据属性

- **根作品：** `data-composition-id`、`data-start`、`data-duration`、`data-width`、`data-height`、`data-composition-src`（外部子作品）、`data-composition-duration`、`data-composition-variables`（JSON）、`data-variable-values`（覆盖）
- **每个片段：** `id`、`data-start`、`data-duration`、`data-track-index`、`class="clip"`、可选的 `data-media-start`、`data-volume`、`data-playback-start`
- **子作品宿主：** `data-composition-id`、`data-composition-src` 或内联 `<template id="${compId}-template">`
- **解析器也读取：** `data-type`（composition|text）、`data-end`、`data-keyframes`（JSON）、`data-x|y|scale|opacity`、`data-color|font-size|font-weight|font-family|text-shadow|outline|highlight*`、`data-layer`（z-index，已弃用，但用于音频混音器层）、`data-resolution`、`data-composition-width|height`

### 时间线约定

- `gsap.timeline({ paused: true })` 注册在 `window.__timelines["<composition-id>"]`
- 主时钟（TransportClock + WebAudioTransport）通过 `tl.totalTime(t, false)` 或 `tl.seek(t, false)` 驱动时间线
- 框架自动嵌套子作品时间线
- 时长来自根上的 `data-duration`，而不是 GSAP 长度
- 需要同步时间线构建（没有 async/await/setTimeout）
- 循环由 `<hyperframes-player>` 处理，不是 GSAP `repeat: -1`

### 分辨率预设

VALID_CANVAS_RESOLUTIONS：1920×1080 默认、1080×1920 竖屏、1080×1080 方形、4K、1440×2560，加上 `normalizeResolutionFlag` 用于 `--resolution` CLI 标志。

---

## 2. 动画引擎（6 个确定性帧适配器）

运行时按顺序注册这些适配器；每个实现 `discover()` / `seek({time})` / `pause` / `play?` / `revert`：

| 适配器 | 驱动什么 | 如何加载 | 注意事项 |
| ---------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| GSAP（createGsapAdapter） | 主时间线 + 注册在 `window.__timelines[<id>]` 上的所有动画 | CDN `https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js` | 插件通过标准 GSAP 注册；HyperFrames 不会修补 THREE.Clock（改用 `__hfThreeTime`） |
| Anime.js v4（createAnimeJsAdapter） | 推送到 `window.__hfAnime` 的 Anime 实例 | CDN `animejs@4.0.2/lib/anime.iife.min.js` 或 ESM | 适配器将作品秒数乘以 1000 转换为毫秒 |
| CSS 动画（createCssAdapter） | 任何具有计算后 `animation-name` 的元素 | 声明式 `@keyframes` | 当 WAAPI 不可用时回退到负 `animation-delay` |
| WAAPI（createWaapiAdapter） | document 上的所有 Animation 对象 | `element.animate()` | 使用 `document.getAnimations()` |
| Lottie（createLottieAdapter） | `window.__hfLottie` 数组；支持 lottie-web + dotlottie-web | CDN `lottie.min.js` + `@lottiefiles/dotlottie-web` | `goToAndStop(time*1000)` 或 `setCurrentRawFrameValue` / `seek(%)` |
| Three.js（createThreeAdapter） | `window.__hfThreeTime` + 分派 `CustomEvent("hf-seek", {detail:{time}})` | ESM CDN `three@0.181.2/+esm` | 作品的渲染循环监听 `hf-seek`；模式：`mixer.setTime(time)` |

### GSAP 插件（有文档的模式）

- **TextPlugin**——`tl.call` 中的文本变异（skills/gsap/references/effects.md）
- **MotionPathPlugin**——曲线约束动画（skills/hyperframes/references/techniques.md）
- **CustomEase**——从 Remotion 风格时序导入的贝塞尔缓动
- **ScrollTrigger / Flip / SplitText / Draggable / Inertia / Observer / ScrambleText / CustomWiggle / CustomBounce / ScrollSmoother / GSDevTools**——如果加载且动画在注册的暂停时间线上，则可原生工作，但没有特殊的 HyperFrames 适配器
- 生成器在需要时自动注入 ScrollTrigger CDN（packages/producer/src/services/htmlCompiler.ts）

---

## 3. 着色器过渡——@hyperframes/shader-transitions

14 个命名的 WebGL 片段着色器。所有着色器共享相同的 uniforms：`u_from`、`u_to`、`u_progress`、`u_resolution`、`u_accent`、`u_accent_dark`、`u_accent_bright`。

### 14 个着色器

| 名称 | 视觉效果 | 说明 |
| ------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| domain-warp | 多倍频 FBM 反向扭曲两个场景；有机溶解边缘带强调闪光 | 使用 NQ 噪点 |
| ridged-burn | 脊状多重分形遮罩揭示 B；强调 → 亮 → 白色燃烧渐变；火花 | NQ |
| whip-pan | 10 样本水平运动模糊 + 横向交叉淡入淡出 | 无噪点 |
| sdf-iris | 矫正宽高比的圆形 SDF 扩展 + 强调色调光晕环 | — |
| ripple-waves | 径向驻波 UV 位移 + 色调交叉淡入淡出 | — |
| gravitational-lens | 向中心拉拽 + R/B 色差分离 | — |
| cinematic-zoom | 12 RGB 偏移径向缩放模糊样本（色差缩放条纹） | — |
| chromatic-split | R/B 径向通道向外/向内移位；G 固定 | 不同于 CSS 色差 |
| swirl-vortex | 逆时针漩涡带 FBM 噪点；进入时反向 | NQ |
| thermal-distortion | 垂直 sin + FBM 水平位移；暖雾 | NQ |
| flash-through-white | 通过白色中点淡入淡出——场景之间可见的白色闪光 | 不使用强调色。仅当品牌特别要求白色闪光节拍边界时使用；这不是中性的「默认」过渡。 |
| cross-warp-morph | FBM 向量场位移两个场景；第三个 FBM 偏置不规则擦除 | NQ |
| light-leak | 固定的画外漏光带指数衰减 + 强调暖色调 + 脊状光晕 | 硬编码漏光锚点 |
| glitch | 行位移 + RGB 横向分割 + 扫描调制 + 调色板化 + 闪烁 | 确定性 |

### 公共 API

```js
HyperShader.init({
  bgColor: "#0b0f14",
  accentColor: "#f59e42",
  scenes: ["scene1", "scene2"],
  transitions: [{ time: 3, shader: "sdf-iris", duration: 0.65, ease: "power2.inOut" }],
  timeline: gsap.timeline({ paused: true }),
  compositionId: "main",
  previewCaptureFps: 30,
});
```

- 能力检测：`isHtmlInCanvasCaptureSupported()`（Chrome layoutSubtree/drawElementImage）
- 调优：`?__hf_shader_capture_scale=`（0.25–1）、`?__hf_shader_loading=`（internal|player|none）
- 缓存：PNG 快照的 IndexedDB；最多同时激活 2 个纹理过渡
- 回退（`applyFallbackTransition`）：当 capture / texImage2D 失败时的 smoothstep 不透明度动画
- 引擎模式在设置 `window.__HF_VIRTUAL_TIME__` 时跳过 GL/capture（生成器使用元数据）

你也可以**从头编写自定义 GLSL 着色器**——任何片段着色器都可以使用标准 uniforms 工作。

---

## 4. CSS 场景过渡（30+ 个命名模式）

记录在 skills/hyperframes/references/transitions/ 下的 14 个分类文件中。全部由 GSAP 驱动，不能在同一作品中的着色器过渡混用。

### 按分类

| 分类 | 模式 |
| -------------------------------- | ------------------------------------------------------------------------------------------------ |
| 推/滑动（css-push.md） | 推滑、垂直推、弹性推、挤压 |
| 缩放/放大（css-scale.md） | 缩放穿透、缩放退出、缩放交换 |
| 径向/剪辑（css-radial.md） | 圆形虹膜、菱形虹膜、对角线分割 |
| 3D（css-3d.md） | 3D 卡片翻转、铰链门 |
| 模糊（css-blur.md） | 交叉淡入淡出、模糊交叉淡入淡出、焦距拉远 |
| 溶解（css-dissolve.md） | 颜色浸入（间隙到黑色）、交错颜色块（2 块、5 块） |
| 覆盖（css-cover.md） | 水平百叶窗、垂直百叶窗（可变条数：6 / 12 / 20） |
| 光效（css-light.md） | 漏光叠加、过曝烧灼、胶片烧灼 |
| 扭曲（css-distortion.md） | 故障（CSS——RGB 层抖动）、色差、涟漪 |
| 机械（css-mechanical.md） | 快门（两半）、时钟擦除（9 点旋转楔形） |
| 网格（css-grid.md） | 网格溶解（12 或 120 个单元格）、网格像素化擦除 |
| 破坏（css-destruction.md） | 页面烧灼（SVG clip-path + canvas 字符边缘） |
| 其他（css-other.md） | VHS 磁带（基于条纹的种子抖动）、重力下落、变形圆、模糊穿透、定向模糊 |
| 已拒绝 | 星形虹膜、移轴、镜头光晕（不要使用——非 CSS 现实） |

### 时序预设

| 预设 | duration | ease |
| -------- | -------- | ---------------------- |
| snappy | 0.2s | power4.inOut |
| smooth | 0.4s | power2.inOut |
| gentle | 0.6s | sine.inOut |
| dramatic | 0.5s | power3.in → power3.out |
| instant | 0.15s | expo.inOut |
| luxe | 0.7s | power1.inOut |

---

## 5. 视觉效果 + 纹理

### 标记/强调模式（css-patterns.md）

| 模式 | 作用 | 实现 |
| --------- | --------------------------------- | ----------------------------------------- |
| highlight | 黄色条在文本后面擦除 | CSS 条 + GSAP scaleX 0→1 |
| circle | 手绘红色环形围绕词语 | CSS 边框椭圆 + back.out 缩放 |
| burst | 从词语中心发出 12 条径向射线 | DOM 线阵，--len/--angle 变量 |
| scribble | 随时间绘制的波浪下划线 | SVG `<path>` 二次曲线 + stroke-dash GSAP |
| sketchout | 在文本上的交叉阴影 x-out | 两条 2px 旋转线 |

### 颗粒/噪点

- **grain-overlay**（注册表组件）：SVG feTurbulence data-URL + CSS 关键帧抖动、`steps(1)`、默认不透明度 0.15
- **分层径向渐变颗粒**（首选模式）：无 SVG，无 canvas 污染，各处速度快

### 光效/胶片

- 漏光过渡（CSS + 着色器变体）
- 过曝烧灼——`brightness()` 渐变 + 闪光叠加
- 胶片烧灼——多层琥珀/橙/红径向
- 暗角——径向渐变叠加
- 纸张纹理（在 registry/examples/warm-grain/ 中）

### 光晕

- 字幕文本光晕：textShadow 半径键控到高音频段（始终仅在活跃词上，从不父元素）
- 径向光晕背景：CSS 渐变 / 模糊斑点

---

## 6. 字幕技术

### 动画风格

- 基线：逐词卡拉 OK 高亮（每个能量级别）
- 强度层级：强调 + 光晕 + 15% 缩放（高能量）→ 3% 缩放（低能量）
- 按能量退出（dynamic-techniques.md）：散射、下落、折叠、淡出+滑动、淡出
- 语调映射（captions.md）：缩放弹出 `back.out(1.7)`、淡出+滑动 `power3.out`、打字机、弹跳、`elastic.out`、逐词

### 逐词样式触发器

- 品牌/产品名称
- 全大写
- 数字 / 统计
- 情感关键词
- CTA
- 标记高亮模式（上面列出的 5 种）

### 字幕时序的音频源

| 源 | 格式 | 粒度 |
| ------------------------------------------ | -------- | ----------------- |
| hyperframes transcribe（本地 whisper.cpp） | JSON | 词语级 |
| OpenAI verbose_json | JSON | 词语级 |
| Groq verbose_json | JSON | 词语级 |
| 手动编写 | JSON | 词语级 |
| SRT | text | 仅短语级 |
| VTT | text | 仅短语级 |
| hyperframes tts → transcribe 链 | wav→json | 词语级 |

### 定位辅助

- 横屏：底部 80–120px 居中
- 竖屏：距底部约 600–700px
- `window.__hyperframes.fitTextFontSize(text, {maxWidth, fontFamily, fontWeight})` 用于动态大小调整

---

## 7. 音频响应动画

### 数据格式

```js
window.AUDIO_DATA = {
  fps: 30,
  totalFrames: 900,
  frames: [{ bands: [0.42, 0.18, ...] }]  // 各频段在整轨上归一化 0–1
};
```

索引 0 = 贝斯，越高 = 高音。频段范围 0–1，在完整轨长上归一化。

### 有文档的映射

| 频段 | 属性 |
| --------------------- | ---------------------------- |
| 贝斯（bands[0–1]） | 缩放（脉冲） |
| 中频（bands[4–8]） | borderRadius、width |
| 高音（bands[12–14]） | textShadow、boxShadow（光晕） |
| 总振幅 | opacity、y、backgroundColor |

任何 GSAP 可动画属性都是公平的游戏——包括 clipPath、filter、SVG 属性、CSS 变量。

### 提取

```bash
python3 .../extract-audio-data.py audio.mp3 --fps 30 --bands 8
```

仅预先提取——渲染时无 Web Audio。

### 音频响应中禁止的

EQ 条、频谱 UI、通用波形、音符剪贴画、通用粒子、彩虹循环、节拍上的白色频闪、抽象脉冲球体。

---

## 8. HTML-in-canvas

记录在 skills/hyperframes/references/html-in-canvas-patterns.md（504 行）。

### 能力

- Chrome 的实验性 `layoutSubtree` + `drawElementImage` 将实时 DOM 栅格化到 canvas
- 特征检测：`isHtmlInCanvasCaptureSupported()`
- 着色器过渡用于场景纹理
- 结合 Three.js：`CanvasTexture` + 后处理

### 可用模式

- Three.js 平面上的 HTML（位移、扭曲、液体模拟）
- 着色器中的 HTML（VFX 的纹理采样）
- 递归 HTML-in-canvas-in-shader-in-HTML

### 使用此功能的实验性 VFX 块

- `vfx-iphone-device`（GLTF iPhone + MacBook、HTML 屏幕）
- `vfx-liquid-background`（液体模拟位移 HTML）
- `vfx-liquid-glass`
- `vfx-magnetic`
- `vfx-portal`
- `vfx-shatter`
- `vfx-text-cursor`（色差边缘、canvas 后处理）

---

## 9. Three.js / WebGL 自定义场景

### 集成模式

```js
window.addEventListener("hf-seek", (e) => {
  const time = e.detail.time;
  mixer.setTime(time);
  shaderUniforms.u_time.value = time;
  renderer.render(scene, camera);
});
```

- 加载：`import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm"`
- 确定性：每一帧必须从 `time` 派生，永远不使用 `requestAnimationFrame` / `Date.now()`
- 包括：AnimationMixer、自定义 GLSL 着色器、后处理、GLTF 模型、灯光、相机、材质

---

## 10. SVG / canvas / 可变字体（其他创作技术）

（来自 skills/hyperframes/references/techniques.md）

| 技术 | 机制 |
| ------------------------ | ------------------------------------------------------------------------------------ |
| SVG 路径绘制 | `strokeDasharray` + `getTotalLength()` + GSAP stroke 偏移 |
| Canvas 2D 程序化艺术 | 种子哈希函数 + `tl.to` 代理 `{time}` onUpdate |
| CSS 3D 卡片 | GSAP `rotationY` + `perspective: 900` |
| 逐词动态排版 | GSAP 时序数组、滑动衰减 |
| 可变字体轴 | 动画化 CSS 变量 → `font-variation-settings: "opsz" var(--opsz), "wght" var(--wght)` |
| 字符打字 | `tl.call` 文本变异 + `steps(1)` 光标闪烁 |
| 速度匹配切割 | 匹配退出的模糊/平移速度到进入，实现无缝节拍 |
| MotionPathPlugin | `gsap.registerPlugin(MotionPathPlugin)` + 路径字符串 |

---

## 11. 媒体：视频、音频、TTS

### 视频合成

- `<video muted playsinline data-start="..." data-duration="..." data-track-index="..." src="...">`
- HyperFrames 在渲染时通过 videoFrameInjector 提取帧（避免不可靠的无头 `<video>` 播放）
- 检查器禁止 `<video>` 同时带有音频——拆分为单独的 `<video muted>` + `<audio>`
- 视频帧提取使用 FFmpeg
- HDR 视频：PQ 或 HLG 传输检测 + 带母版元数据的 x265

### 音频混音器

- `<audio id="..." data-start="..." data-duration="..." data-volume="0.8" data-track-index="2" src="...">`
- 多轨混合使用 `amix normalize=0` + 每轨 adelay + 音量
- 来自 EngineConfig 的主音频增益
- 输出：AAC 192kbps

### TTS（Kokoro-82M，本地）

- 54 个捆绑语音，带前缀：`a` 美式英语、`b` 英式英语、`e` 西班牙语、`f` 法语、`h` 印地语、`i` 意大利语、`j` 日语、`p` 巴西葡萄牙语、`z` 普通话
- 默认语音：`af_heart`
- 速度：0.1–3.0（默认 1.0）
- 语言：en-us、en-gb、es、fr-fr、hi、it、pt-br、ja、zh（非英语需要系统 espeak-ng）
- 输出：WAV；没有音高/音量 CLI 标志
- 无需 API 密钥

### 转录

- Whisper.cpp 模型：tiny、base、small、medium、large-v3、small.en、medium.en（默认 small）
- Groq API：whisper-large-v3 带词语粒度
- OpenAI API：whisper-1 verbose_json
- 导入：SRT、VTT、JSON 格式
- 质量门控：音乐标记检测、垃圾清理、medium.en 重试

### 背景去除

- u2net ONNX 模型
- 设备：auto / cpu / coreml / cuda
- 质量预设：fast / balanced / best
- 输出：透明 WebM、ProRes MOV、PNG 序列
- 可选双输出（前景 + 提取的背景）

---

## 12. 注册表——51 个块 + 4 个组件 + 8 个示例

### 块按分类

**社交叠加（8）：** instagram-follow、tiktok-follow、yt-lower-third、x-post、reddit-post、spotify-card、macos-notification、blue-sweater-intro-video

**展示（5）：** app-showcase（3D 手机）、north-korea-locked-down（地图 + 标注）、apple-money-count（计数器 + SFX）、vpn-youtube-spot（应用商店滚动）、nyc-paris-flight（地图 + 飞机路径）

**数据可视化（2）：** data-chart（动画柱状+折线，NYT 风格）、flowchart + flowchart-vertical（决策树带 SVG 连接器、打字修正）

**Logo / 品牌（1）：** logo-outro（构建 + 光晕 + 标语 + URL 药丸）

**3D / 实验性 VFX（8）：** ui-3d-reveal、vfx-iphone-device（GLTF）、vfx-liquid-background、vfx-liquid-glass、vfx-magnetic、vfx-portal、vfx-shatter、vfx-text-cursor

**单着色器过渡（14）：** 每个命名的着色器一个块——domain-warp-dissolve、ridged-burn、whip-pan、sdf-iris、ripple-waves、gravitational-lens、cinematic-zoom、chromatic-radial-split、glitch、swirl-vortex、thermal-distortion、flash-through-white、cross-warp-morph、light-leak

**过渡画廊（13 个展示作品）：** transitions-3d、transitions-blur、transitions-cover、transitions-destruction、transitions-dissolve、transitions-distortion、transitions-grid、transitions-light、transitions-mechanical、transitions-other、transitions-push、transitions-radial、transitions-scale

### 组件（4 个可重用代码片段）

- **grain-overlay**——SVG feTurbulence + CSS 关键帧
- **shimmer-sweep**——文本上的光扫渐变遮罩
- **grid-pixelate-wipe**——网格方块交错淡出场景擦除
- **texture-mask-text**——亮度遮罩字母形状，带 66 个遮罩 PNG（砖石、石头、地面/道路、木材、金属、有机/软纹理类别）

### 示例（8 个入门项目）

warm-grain、play-mode、swiss-grid、vignelli、decision-tree、kinetic-type、product-promo、nyt-graph

安装：`npx hyperframes add <name>` 用于块/组件，`hyperframes init <dir> --example <name>` 用于示例。

---

## 13. CLI——25 个命令

| 命令 | 用途 |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| init | 从模板/示例搭建项目（交互式或 --non-interactive） |
| add | 安装注册表块/组件 |
| catalog | 浏览注册表块/组件（--type、--tag、--json、--human-friendly 选择器） |
| play | 轻量级浏览器播放器（默认端口 3003） |
| preview | Studio 开发服务器（端口 3002；--force-new、--list、--kill-all） |
| publish | 压缩 + 上传 + 返回 hyperframes.dev URL |
| render | 渲染为 MP4 / WebM / MOV / PNG 序列——标志：--fps 24/30/60、--quality draft/standard/high、--workers、--docker、--hdr/--sdr、--crf、--video-bitrate、--gpu、--browser-gpu auto/software/hardware、--max-concurrent-renders 1-10、--variables JSON、--variables-file PATH、--strict-variables、--resolution preset |
| lint | 静态检查（--json、--verbose） |
| validate | 打包 + 无头 Chrome + 控制台 + 对比度（--contrast default true、--timeout 3000） |
| inspect / layout | 视觉布局审计（在 N 个时间戳检测溢出；--samples 9、--at、--tolerance 2、--max-issues 80） |
| info | 打印项目元数据 |
| compositions | 列出作品（根 + 子作品） |
| benchmark | 5 个预设配置 × N 次运行（--runs 3） |
| browser | 管理 Chrome（ensure/path/clear） |
| remove-background | u2net + FFmpeg → 透明视频 |
| transcribe | whisper.cpp 或导入 SRT/VTT/JSON |
| tts | Kokoro-82M（--voice、--speed、--lang、--list） |
| docs | 打印捆绑的 markdown 主题（data-attributes、examples、rendering、gsap、troubleshooting、compositions） |
| doctor | 环境清单（Node、CPU、内存、磁盘、FFmpeg、FFprobe、Chrome、Docker） |
| upgrade | npm 更新检查 + 可选全局安装 |
| skills | 运行 `npx skills add heygen-com/hyperframes --all` |
| telemetry | enable/disable/status |
| snapshot | 时间线时间戳的 PNG 截图 |
| capture | 捕获 URL → 网站资源 + 截图 + 设计令牌（使用 Puppeteer + 可选 Gemini 视觉） |

### 网站捕获（`hyperframes capture <url>`）

检测捕获网站上的这些库（用于上下文标记）：GSAP / ScrollTrigger、Three.js、Lottie、Anime.js、PixiJS、Babylon.js、Rive、Matter.js、Lenis、Framer Motion、Tailwind CSS、WebGL（着色器指纹识别）。捕获的输出供给 website-to-video 技能工作流。

---

## 14. 检查器——60+ 条规则

分布在 packages/core/src/lint/rules/ 的 8 个文件中：

| 规则文件 | 捕获 |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| core | 缺少 composition-id、缺少尺寸、缺少时间线注册、注册表不匹配、无效脚本语法、作用域 CSS 问题、非确定性代码 |
| media | 重复的媒体 id、视频缺少 muted、视频嵌套在定时元素中、占位符 URL、禁止 base64、缺少 src/start/id、命令式 play()/pause()/seek() |
| gsap | 重叠动画、退出缺少硬清除、GSAP 动画化 .clip 元素、无作用域选择器、CSS transform 冲突、缺少 GSAP 脚本、无限重复（repeat: -1）、重复 ceil 过冲、场景层可见性清除、音频响应每组的单一动画 |
| captions | 字幕退出缺少清除、文本溢出风险、转录未内联、解析错误、容器位置、缩放不匹配、父容器上的 textShadow |
| composition | 文件太大、密集轨道、缺少 class="clip"、已弃用的 data-layer/data-end、分割属性选择器、外部脚本依赖、作品中的 RAF、无效变量 JSON |
| adapters | 缺少 Lottie 脚本、缺少 Three 脚本 |
| textures | 文本上的阴影、缺少 base 的类、文本缺少遮罩、未知纹理类 |
| fonts | Google Fonts 导入（使用 @font-face）、font-family 没有 @font-face |

加上异步 URL 检查（`lintMediaUrls`、`lintScriptUrls`——HEAD 探测）。

`validateCompositionGsap` 还禁止：`Math.random`、`Date.now`、`new Date`、`setTimeout`、`setInterval`、`requestAnimationFrame`、`repeat: -1`。

**注意：** `onUpdate` 回调、`tl.call()` 和 GSAP 事件回调（`onComplete`、`onStart` 等）**不**被检查器禁止——它们是 canvas/WebGL 渲染和逐字打字模式所必需的。检查器只捕获上面列出的确定性违规。

---

## 15. 播放器——`<hyperframes-player>` Web 组件

### 属性

`src`、`srcdoc`、`width`、`height`、`controls`、`muted`、`volume`、`poster`、`playback-rate`、`audio-src`、`shader-capture-scale`、`shader-loading`（internal|player|none）、`loop`、`autoplay`、`speed-presets`

### 公共 API

`seek(t)`（同源时同步——直接使用 `iframe.contentWindow.__player.seek`）、`play()`、`pause()`、`currentTime`、`duration`、`paused`、`ready`、`playbackRate`、`iframeElement`

### 事件

`ready`、`timeupdate`、`play`、`pause`、`ended`、`volumechange`、`ratechange`、`shadertransitionstate`、`playbackerror`、`error`、`audioownershipchange`

### 媒体镜像

具有 `data-start` 的父级音频/视频元素被代理；`_mirrorParentMediaTime` 校正漂移；`_audioOwner` 在自动播放被阻止时提升到父级。

### 运行时自动注入

如果缺少 `__hf`/`__player` 但存在时间线，则加载 `RUNTIME_CDN_URL`（`@hyperframes/core/dist/hyperframe.runtime.iife.js`）。

---

## 16. 引擎 + 生成器——渲染管线

### 输出格式

mp4、webm、mov、png-sequence——带 HDR（PQ / HLG / SDR / 自动检测）、透明度（ProRes MOV / WebM / PNG）或标准 8-bit SDR

### 编码控制

- `--fps`：24 / 30 / 60
- `--quality`：draft / standard / high
- `--crf`：整数（与 `--video-bitrate` 互斥）
- `--video-bitrate`：例如 `8M`
- `--gpu`：NVENC、VideoToolbox、VAAPI、QSV
- `--browser-gpu`：auto / software / hardware
- `--workers`：并行渲染工作进程
- `--max-concurrent-renders`：1–10（设置 `PRODUCER_MAX_CONCURRENT_RENDERS`）
- `--resolution`：预设（1080p、4k、竖屏等）
- `--docker`：在 Dockerfile.test 镜像内渲染（可重现性）
- `--hdr` / `--sdr`：强制 HDR 或 SDR 管线

### 引擎子系统

- 帧捕获：Linux headless-shell 上的 BeginFrame（快速，无 alpha）或 `Page.captureScreenshot`（alpha + 超采样）
- 视频帧注入器：预先提取视频到图像，在捕获期间将 `<video>` 替换为 `<img>`（LRU 缓存，按路径 + 字节预算）
- 音频混音器：基于 FFmpeg；每轨延迟、音量、主增益、AAC 192k 输出
- 块编码器：H.264 / H.265 / VP9 / ProRes 预设，可选 GPU
- 流式编码器：`streamingEncodeMaxDurationSeconds` 用于长渲染
- HDR 合成：`rgba16float` WebGPU 回读（有头 Chrome）、PQ OETF 辅助
- 图层合成器：按 z-order 分组 DOM；将 HDR 元素分割到单独的层
- Alpha blit：matrix3d 仿射提取、`blitRgba8OverRgb48le`、`blitRgb48leAffine`
- 并行协调器：并发、coresPerWorker、minParallelFrames、largeRenderThreshold
- 浏览器池：可选，带超时配置

### 仅生成器

- `RenderConfig` 带 `hdrMode`（auto / force-hdr / force-sdr）、`outputResolution` 映射到 `deviceScaleFactor`
- 文件服务器注入 `HF_EARLY_STUB`、`HF_BRIDGE_SCRIPT`、虚拟时间，使 `window.__hf` 桥接 `window.__player.renderSeek`
- HDR 感知的着色器过渡合成，通过 `window.__hf.transitions` 元数据

---

## 17. Studio——浏览器内 NLE

packages/studio/ 中的完整编辑器：

- **NLELayout**：NLE 预览 + 时间线 + 控制
- **Timeline**：片段渲染、拖拽移动（`data-start`）、调整大小（`data-duration`）、`data-track-index` 重新分配、资源拖放、文件拖放
- **PlayerControls**：擦除、播放、暂停、帧步进（`stepFrameTime`）、`STUDIO_PREVIEW_FPS`
- **useTimelinePlayer**：解析 `__player` / `__timeline` / `__timelines`
- **LeftSidebar**：作品列表、资源浏览器
- **RenderQueue + useRenderQueue**：排队多个渲染
- **LintModal**：应用内检查输出
- **MediaPreview + AudioWaveform**：波形渲染
- **CaptionOverlay、CaptionTimeline、CaptionPropertyPanel**：字幕编辑器
- **useCaptionSync**：词语级同步
- **useElementPicker**：点击检查选择器模式
- 使用 Tailwind v3 构建（与作品使用的 Tailwind v4 浏览器运行时分开）。

---

## 18. 确定性保证

- 没有 `Math.random()`（使用种子 PRNG；mulberry32 是技能中的模式）
- 没有 `Date.now()` / `new Date()`
- 时间线构建中没有 `setTimeout` / `setInterval`
- 没有 `requestAnimationFrame`（时间线驱动；引擎逐帧定位）
- 没有 `repeat: -1`（计算精确重复次数：`Math.ceil(duration / cycleDuration) - 1`）
- 没有 `onComplete`/`onStart`/`onRepeat` 回调（引擎不触发它们）。**例外：** `onUpdate` 和 `tl.call()` **被**支持——它们是 canvas/WebGL 渲染、逐字打字和计数器模式所必需的。参见 §10（Canvas 2D 程序化艺术）了解有文档的模式。
- 没有对来自后续场景的片段使用 `gsap.set`（使用 `tl.set(selector, vars, position)`）
- 同步时间线构建（没有 async）
- 主时钟可以在作品结束时钳制

---

## 19. 变量 / 参数化

作品支持类型化运行时变量：

```html
<html
  data-composition-variables='[
  {"name":"brand","type":"string","default":"Stripe"},
  {"name":"primary","type":"color","default":"#635BFF"},
  {"name":"duration","type":"number","default":15},
  {"name":"darkMode","type":"boolean","default":false},
  {"name":"layout","type":"enum","options":["hero","split","stacked"]}
]'
></html>
```

通过 `window.__hyperframes.getVariables()` 访问。在渲染时覆盖：

```bash
npx hyperframes render --variables '{"brand":"Linear","primary":"#5E6AD2"}'
npx hyperframes render --variables-file vars.json
npx hyperframes render --strict-variables  # 如果存在未使用/不匹配的变量则报错
```

`validateVariables()` 在 CLI/工具边界检查值是否符合声明。

---

## 20. 子作品

两种加载机制：

- **外部文件：** `data-composition-src="compositions/act-1.html"`——在运行时获取
- **内联模板：** `<template id="<id>-template">`——由 `loadInlineTemplateCompositions` 提取

每个子作品：

- 有自己的 `data-composition-id`
- 有自己的 `window.__timelines[<id>]`
- 自动嵌套到根时间线
- 通过 `scopeCssToComposition` 作用域 CSS（`[data-composition-id="<id>"]` 选择器）
- 通过 `wrapScopedCompositionScript` 包装脚本
- 从 `data-variable-values` 读取，与自己的默认值合并到 `window.__hfVariablesByComp[<id>]`
- 外部脚本加载带 `EXTERNAL_SCRIPT_LOAD_TIMEOUT_MS` 超时。加载失败会发出 `external_composition_load_failed` / `external_composition_script_load_issue` 诊断

---

## 21. 全局运行时 API（`window.*`）

（文件太长，已截断）
