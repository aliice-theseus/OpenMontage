---
name: hyperframes-animation
description: "HyperFrames 的所有动画知识 — 原子运动规则、多阶段场景蓝图、场景过渡、更广泛的动效设计技巧，以及七个运行时适配器（GSAP 默认，外加 Lottie、Three.js、Anime.js、CSS 关键帧、Web Animations API、TypeGPU）。用于任何运动或动画任务：选择 2-4 条规则并组合，或加载蓝图，或查阅运行时特定 API（例如 GSAP 缓动 / Lottie 播放器 / Three.js mixer）。HyperFrames 原生：单个暂停时间线、seek 安全、确定性。"
---

# HyperFrames 动画

所有运动知识在一个技能中：**规则**（原子配方）、**蓝图**（多阶段场景模板）、**过渡**（场景到场景）、**技巧**（更广泛的动效设计模式）和**适配器**（每个运行时的 API）。

关于组合约定（数据属性、子组合、确定性），参见 `hyperframes-core`。

## 默认：组合原子规则

从 `rules-index.md` 中选择 2-4 条规则，用单个暂停的 GSAP 时间线将它们粘合在一起，完成。这比从蓝图开始更快，产生更少的代码。

## 何时加载蓝图

- 场景匹配现有的预设计多阶段模板（品牌揭示、社交证明等），重用其阶段管线可节省实际创作时间
- 你需要复杂 4-5 阶段编排的可运行真实代码

蓝图位于 `blueprints-index.md`。每个条目指向 `blueprints/<id>.md`（配方）。不要投机性读取；在你已决定需要场景级编排时加载。

## 路由

| 你想…                                                                          | 读取                                                |
| ------------------------------------------------------------------------------ | --------------------------------------------------- |
| 按触发方式/标签选择原子运动模式                                                | `rules-index.md`                                    |
| 读取某个规则的完整 HTML / CSS / GSAP 配方                                      | `rules/<name>.md`                                   |
| 选择多阶段场景模板                                                            | `blueprints-index.md`                               |
| 读取某个蓝图的完整配方                                                        | `blueprints/<id>.md`                                |
| 编写场景过渡（CSS 驱动，在两个剪辑之间）                                      | `transitions/overview.md`、`transitions/catalog.md` |
| 查阅更广泛的动效设计技巧                                                      | `techniques.md`                                     |
| 分析现有组合的动画映射                                                        | `scripts/animation-map.mjs`                         |
| GSAP API — 时间线 / 补间 / 位置参数                                           | `adapters/gsap.md`                                  |
| GSAP — 即用特效配方                                                           | `rules/gsap-effects.md`                             |
| GSAP — 变换 / 性能                                                           | `adapters/gsap-transforms-and-perf.md`              |
| GSAP — 缓动 / 错开                                                           | `adapters/gsap-easing-and-stagger.md`               |
| GSAP — 时间线 / 标签                                                         | `adapters/gsap-timeline-and-labels.md`              |
| Lottie / dotLottie（After Effects 导出、`window.__hfLottie`）                 | `adapters/lottie.md`                                |
| Three.js / WebGL（3D 场景、`AnimationMixer`、`hf-seek`）                      | `adapters/three.md`                                 |
| Anime.js（`window.__hfAnime`）                                                | `adapters/animejs.md`                               |
| CSS 关键帧（`animation-delay` / `play-state` / `fill-mode`）                  | `adapters/css-animations.md`                        |
| Web Animations API（`element.animate()`、`currentTime` 定位）                 | `adapters/waapi.md`                                 |
| TypeGPU / WebGPU（`navigator.gpu`、WGSL、计算管线）                           | `adapters/typegpu.md`                               |
| HTML 作为纹理 + WebGL/GLSL 后处理（通过 `drawElementImage` 捕获实时 DOM）     | `adapters/html-in-canvas-patterns.md`               |
| 命名文本动画特效（24 个 ID，通过外部 `animate-text` 技能）                    | `adapters/animate-text.md`                          |

## 选择运行时

- **GSAP** 是 95% 运动工作的默认选择 — 涵盖时间线编排、变换、缓动、错开。本技能中的所有原子规则都基于 GSAP。
- **Lottie** 当资源有自己预烘焙的时间线时（通常是 After Effects 导出）。
- **Three.js** 用于 3D 场景、摄像机运动、着色器驱动的视觉效果。
- **Anime.js** 用于 GSAP 过于重量级时的轻量补间。
- **CSS** 用于简单重复主题、装饰、闪烁 — 无 JavaScript 动画成本。
- **WAAPI** 用于无需 GSAP 依赖的原生浏览器关键帧。
- **TypeGPU / WebGPU** 用于 GPU 渲染的 canvas（粒子、液态玻璃、自定义着色器）。

多个运行时可以在一个组合中共存。每个在运行时特定的全局对象上注册其实例，使 HyperFrames 能一次性定位所有。

## 关键约束

**先决条件：`hyperframes-core` → 不可协商规则**（单个暂停时间线、`data-duration` 控制长度、无 `Math.random` / `Date.now` / `performance.now`、无 `repeat: -1`、无 `gsap.set` 在后续场景剪辑上、无 `display` / `visibility` 动画、不在 `async` / `setTimeout` / `Promise` 内构建时间线）。此处不重复这些。

核心约定之上的动画技艺补充：

- **预计算的布局常量** — 绝不在补间时间从 `getBoundingClientRect()` 派生位置。补间时 DOM 测量会不同步，因为渲染器并行采样；在组合设置时计算一次坐标并复用。
- **空间运动仅使用 GSAP 变换别名**（`x`、`y`、`scale`、`rotation`）。核心的允许列表也允许非空间属性补间的 `opacity` / `color` / `backgroundColor` / `borderRadius` — 但布局变化绝不用 `width` / `height` / `top` / `left`。

## 脚本

```bash
node skills/hyperframes-animation/scripts/animation-map.mjs <composition-dir> \
  --out <composition-dir>/.hyperframes/anim-map
```

读取在 `window.__timelines` 上注册的每个 GSAP 时间线，枚举补间，采样边界框，计算标志，输出 `animation-map.json`。在创作后用于审计编排（死区、错开一致性、生命周期警告）。

## 参见

- `hyperframes-core` — 组合结构、数据属性、子组合、确定性渲染约定
- `hyperframes-creative` — 调色板、排版、旁白、节拍规划（非动画创意指导）
- `hyperframes-cli` — `npx hyperframes lint / validate / inspect / preview / render`
