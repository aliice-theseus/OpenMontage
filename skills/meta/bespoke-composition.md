# 定制合成（工作室模式）

用于**从头开始手工编写合成**而非组装库存场景类型的元技能。这是"每次都手工缝制"的路径：对于英雄作品，每个像素的外观都是全新编写的，这样没有两个视频会共享视觉语言。

当你为一篇作品选择了**工作室模式**时阅读本技能（见"何时使用"）。它不会为你提供组件——而是引导你需要掌握的*原则、引擎机制和工具接线*，以便你构建的内容正确且独特。

> 支配以下所有内容的唯一规则是：**重用引擎知识，绝不重用创意组件。** Remotion 如何解析资产是引擎知识——可以自由重用。以前的视频看起来如何是创意决策——绝不重用。

## 何时使用本技能（创作模式是提案决策）

OpenMontage 分离三个正交轴，全部在提案时锁定：

- `renderer_family` — 创意语法
- `render_runtime` — 技术引擎（remotion / hyperframes / ffmpeg）
- **`composition_mode`** — **模板化**（组装库存 `cut.type` 场景）**vs. 工作室**（手工编写）

默认情况下为以下场景选择**工作室**模式：营销、发布、必须令人印象深刻的解说、品牌作品、任何单个交付物且质量是重点的场景。选择**模板化**模式用于：批量输出、本地化变体、快速草稿、低风险内部片段——这些地方可靠的重复性没问题，定制成本不合理。在提案时向用户呈现选择，并在 `decision_log` 中记录（`category: "composition_mode"`），方式与呈现运行时相同。

### 工作室模式与两个运行时

两个运行时对待"定制"的方式不同——在假设原则以相同方式映射到两者之前，请先阅读以下内容：

- **Remotion** 附带一个 `cut.type` 注册表，包含库存场景（`text_card`、`stat_card`、`bar_chart`……），由 `Explainer`/`CinematicRenderer` 合成分发。这是模板化默认值。**工作室模式是逃生口**——`composition_mode: "atelier"` 将渲染路由到 `_render_via_atelier` 并完全绕过注册表，因此 agent 在 `projects/<slug>/` 下手写自己的 React 合成。
- **HyperFrames 本质上是工作室模式。** HF 中没有剪辑 schema——每个合成都是手工编写的 `index.html`，带有 `data-*` 时间属性和你编写的 GSAP 时间线。注册表（`hyperframes add`）是一个*块*注册表（纹理叠加、过渡）——它是你合成的可选输入，而不是分发整个渲染的场景目录。**当选择了 `render_runtime: "hyperframes"` 时，作品已经是工作室风格；`composition_mode: "atelier"` 是隐含的。** 本技能中的原则（艺术指导、场景独特性、无英雄组件脊柱、独特性审查）同样适用。通过 `hyperframes_compose` 渲染（或对手工编写的合成使用 `npx hyperframes render`——见第 5 节）。

因此：如果 `render_runtime == "remotion"` 且作品是英雄作品，记录一个 `composition_mode: "atelier"` 决策。如果 `render_runtime == "hyperframes"`，工作室是默认行为，你不需要为此争论；本技能仍然会在你编写合成之前通过相同的原则引导你。

如果工作室模式生效（任一运行时），库存 Remotion `cut.type` 目录、作为场景使用的 `hyperframes-registry` 成品块（相对于作为原始输入）、fixtures 以及任何预先烘焙的创意组件都是**禁止使用的**——它们是冻结的外观并重新引入重复性。

## 构建路线

按此顺序编写。每个步骤都会引导你到现有知识——不要跳过第一步。

### 1. 为此主题*确定艺术指导*——分化引擎
在编写任何组件之前，决定一种适合**这个**主题且与其他主题不同的视觉语言。使用 **`visual-style`** 第 3 层技能（CREATE 模式）锁定：调色板、字体的个性、动态特征、布局系统，以及一个**签名装置**，独特于这篇作品。视频之间的差异在这里得到保证——不是通过扣留组件，而是通过每次强制采用全新的方向。将其写下来（项目中的一个简短 `art-direction.md`），并按照它构建。

问问自己：*有什么视觉隐喻属于这个主题而我以前从未使用过？* 如果答案与过去的作品相似，你还没有找到方向。

### 1.5 将每个场景规划为独立的合成——无英雄组件脊柱
最隐蔽的模板化形式在*场景*级别悄然回归：选择一个引人注目的视觉元素（一支蜡烛、一个浏览器框架、一个评分环），然后在每个场景中重复使用它，只更换下面的文字。作品感觉是定制的，因为英雄元素是定制的——但每个场景在机械上是相同的合成。那是品牌化的幻灯片，不是电影。**不要这样做。**

你的艺术指导中命名的签名装置应该出现在**一个或最多两个节拍中**——通常是高潮时刻——而不是作为每个场景的视觉支架。它通过稀缺性来赢得其分量。

对于计划中的每个场景，在编写代码之前*具体地*回答：

- **这个场景的主要视觉主体是什么？** 它必须*不同于*前一个场景的。一个角色。一个图表。一个证据。一个风景。一个排版时刻。签名装置。一个虚空。每个场景的主要主体就是它的工作。
- **这个节拍为什么存在？** 它做了其他节拍无法为故事做的什么？如果你可以将两个场景合并为一个而不损失意义，你应该这样做。
- **它在视觉上如何与前后场景不同？** 不同的构图（三分法 vs 居中 vs 分割）。不同的尺度（亲密特写 vs 广阔场景）。不同的动态模式（静态 vs 繁忙）。不同的调色板强调。不同的文字处理。
- **如果从这个场景中移除签名装置，场景还能工作吗？** 如果能，签名装置可能不属于这个场景——它是作为填充物存在的。砍掉它。

审查者将其作为"scene_distinctness"检查强制执行（见 `skills/meta/reviewer.md` → Composition Authoring Mode Review）：一个记录的清单，包含每个场景的主要主体 + 第一帧，以及对"是否有任何两个场景共享其主要视觉主体？"的明确回答。是 ⇒ 关键 ⇒ 重新规划。

推论：每个场景的计划是一个*一等工件*，而非隐含的。在编写 `Composition.tsx` 之前将其写下来（在 `art-direction.md` 或同级文件 `scenes.md` 中）。

### 2. 确定动态语言——原则而非预设
使用**原则性**技能，永远不要使用完成的动画：
- **`framer-motion`** 和 **`lottie-bodymovin`** ——迪士尼的 12 个原则（预备动作、 staging、跟随动作、慢入慢出、弧线、时间、夸张、吸引力）。与运行时无关；在你自己编写的 Remotion `spring()`/`interpolate()` 代码中应用这些*原则*。
- HyperFrames 的 `references/motion-principles.md` ——缓动作为情感，时间作为重量。

### 3. 仅在概念需要时才使用更丰富的词汇

**在 Remotion 上**——大多数场景使用 Remotion 原语。仅在*创意*需要时才升级，而不是默认：`gsap-*`（通过 SplitText 的动态排版，通过 MorphSVG 的形状变形，通过 MotionPath 的曲线运动，通过 DrawSVG 的线条绘制，自定义缓动），`threejs-*`（3D），`d3-viz`（数据驱动自定义图表——手工构建图表；**不要**使用库存的 `bar_chart`/`line_chart`），`manim-*`（数学），`canvas-procedural-animation`（粒子/天气）。

**在 HyperFrames 上**——词汇表在 `/hyperframes-animation` 中：36+ 个原子运动**规则**（`kinetic-beat-slam`、`3d-text-depth-layers`、`motion-blur-streak`、`physics-press-reaction`、`multi-phase-camera`、`depth-of-field-blur`……），15+ 个场景**蓝图**（`kinetic-type-beats`、`comparison-split`、`dataviz-countup`、`constellation-hub`、`ticker-takeover`、`device-surface-showcase`……），16 个**过渡**系列（`css-distortion`、`css-destruction`、`css-radial`、`css-light`、`css-mechanical`……），以及**7 个运行时适配器**，都在一个合成下：GSAP 默认，加上 Lottie、Three.js、Anime.js、CSS keyframes、WAAPI 和 TypeGPU（GPU 计算）。旗舰能力是 `adapters/html-in-canvas-patterns.md`——将实时 HTML/CSS 捕获为 GPU 纹理，并通过 WebGL/Three.js 渲染以实现电影级辉光、破碎、液体、传送门效果。每部视频只用于 1-3 个英雄节拍，而不是每个节拍。**每个节拍组合使用 2-4 个不同的原子规则**，并在整部作品中**使用至少 3 种不同的缓动**——这是动画技能中内置的原则，不是可选的优化。

对于 HF 创意方向（调色板/字体/旁白/节拍规划），阅读 `/hyperframes-creative`。对于 HF 资产（TTS/BGM/SFX/转录/背景移除），阅读 `/hyperframes-media` 或 `/media-use`。对于 HF CLI 工作流（init/lint/validate/inspect/snapshot/beats/render），阅读 `/hyperframes-cli`。`/hyperframes` 路由器技能映射所有这些。

### 4. 正确掌握引擎机制——陷阱代码库
这是你唯一"重用"的地方：引擎已解决的问题。这些是关于框架如何工作的事实，而不是外观。

**对于 Remotion**，学习 `.agents/skills/remotion-best-practices`（19 个规则文件：时间、过渡、文字动画、透明视频、字体、音频、排序、文字测量）。你也可以阅读 `remotion-composer/src/components/` 中的库存组件**作为机制代码库——学习习语，永远不要导入或模仿外观。**

**对于 HyperFrames**，合成合约在 `/hyperframes-core` 中（`data-*` 时间属性——`data-start`、`data-duration`、`data-track-index`——加上强制性的 `class="clip"`、`data-composition-id`、`window.__timelines` 注册、子合成挂载）。每次更改后运行 `npx hyperframes lint && npx hyperframes validate`——它们在渲染前捕获缺失的根属性、缺失的剪辑 ID、未解析的 GSAP 目标、重叠的补间和对比度失败。使用 `npx hyperframes snapshot . --at <times>` 在提交完整渲染前视觉抽查节拍。

如果你不了解，反复出现的机制问题：
- **确定性**：每帧不要使用 `Math.random()` / `Date.now()`——使用 Remotion `random(seed)` 或种子辅助函数，否则粒子/缓动会在渲染中闪烁。
- **每个场景的时长**：`useVideoConfig().durationInFrames` 返回的是*合成*长度，而不是你的场景的长度。从传入的 `durationInFrames`/`Sequence` 驱动场景局部时间，而不是全局值。
- **资产路径**：URL 和 `staticFile()`（public/）到处可用；**`<Audio>` 拒绝 `file://`**（只有 `<OffthreadVideo>`/`<Img>` 接受绝对路径 `file://`）。将音频/视频放在项目的 public 目录中，通过 `staticFile` 引用。镜像 `resolveAsset` 辅助函数。
- **Remotion 中的 GSAP**：使用 `paused` 时间线和 `.seek(frame/fps)`——永远不要使用 `requestAnimationFrame`——这样帧才能确定性地渲染。
- **字体（Remotion）**：在模块范围内，从 `@remotion/google-fonts/<Name>` 调用 `loadFont()`，仅一次。
- **HF data-* 合约**：每个定时元素需要 `data-start`、`data-duration`、`data-track-index`**和** `class="clip"`——没有 `clip`，框架不会管理可见性，你的元素将在整个时间线上可见。根 `<body>` 需要 `data-composition-id`、`data-start="0"`、`data-duration`、`data-width`、`data-height`。每个时间线必须是 `gsap.timeline({ paused: true })` 并注册为 `window.__timelines["<composition-id>"]`。在剪辑和 GSAP 目标上使用稳定的 `id` 属性——`nth-of-type` 选择器在验证时不稳定。
- **字幕 vs 屏幕文字——选择一个角色，永远不要对相同内容同时使用两者。** 在创作之前，每部作品决定一次：字幕是在增加口头词汇无法承载的意义（数字、名字、翻译、引用出处），还是它们是重复旁白的辅助功能字幕？如果你的场景已经显示了一个逐字朗读脚本的 SerifLine，**不要**也输出一个带有相同文本的自动字幕——即使场景的其他部分很漂亮，重复的短语看起来也很业余。在 props 中使用空 `captions: []`，或者将字幕仅限定在屏幕文字与所说内容不同的场景中。

### 5. 通过运行时合适的定制路径进行渲染
定制合成是**一次性且项目本地的**——它们从不进入任何共享注册表。

#### Remotion 工作室路径
- 在 `projects/<slug>/` 下编写（gitignore）。渲染工具通过 mtime-skip 复制将你的 `.tsx`/`.ts` 源文件自动暂存到 `remotion-composer/projects/<slug>/`，以便 webpack 可以解析 `node_modules`——你的真相源头保持在 `projects/` 下。
- 使用 `python scripts/scaffold_atelier_project.py <slug>` 搭建脚手架——仅发出引擎管道（entry / Root / 空白的 `Composition.tsx` / `art-direction.md` / props 模板 / README）。零创意内容；占位符是一个故意丑陋的黑屏，这样渲染后审查会正确地拒绝交付未创作的脚手架。
- 将媒体文件放在 `projects/<slug>/public/` 中，并将其作为 `bespoke.public_dir` 传递。
- 通过 `video_compose` `operation="render"` 渲染：

```json
edit_decisions = {
  "render_runtime": "remotion",
  "composition_mode": "atelier",
  "bespoke": {
    "entry": "projects/<slug>/index.tsx",
    "composition_id": "<id registered in that entry's Root>",
    "props_path": "<absolute path to artifacts/props.json>",
    "public_dir": "<absolute path to projects/<slug>/public/>",
    "art_direction": "<short note or path to art-direction.md — REQUIRED>",
    "scale": 0.5,          // 0.5 用于快速草稿；最终 1080p 去掉此项
    "crf": 18,             // 清晰的最终输出
    "concurrency": 8
  }
}
```

工作室模式不需要 `asset_manifest` 或 `cuts`——合成拥有自己的资产。工具的 `_run_atelier_checks` 会在任何源文件从库存注册表（`src/components`、`src/Explainer` 等）导入时使渲染失败，并在 `art_direction` 缺失时发出警告。

#### HyperFrames 路径
- 使用 `npx hyperframes init <slug>` 搭建脚手架（从 `projects/` 运行）。HF init 生成 `index.html`、`meta.json`、`package.json` 和一个项目特定的 `CLAUDE.md`，它会自动将 agent 路由到 `/hyperframes`——这样下一个会话就知道要加载哪些子技能。
- 手工编写 `index.html`。每个剪辑需要 `class="clip"` + 三个 `data-*` 时间属性 + 一个稳定的 `id`。当一个文件上的时间线增长超过 4 个剪辑时，通过 `data-composition-src` 挂载子合成（lint 会检查密度）。
- 对于音乐驱动的作品，在将曲目放入 `assets/` 后运行 `npx hyperframes beats .`——它会生成 `beats/<audio>.json`，包含每个节拍的 `{time, strength}`，这样 agent 可以将场景落在真实的节奏点上（而不是猜测）。
- 渲染前验证：`npx hyperframes lint . && npx hyperframes validate . && npx hyperframes snapshot . --at <times>`。Snapshot 是 HF 的原生视觉抽查（所选时间戳处 PNG 帧的联系表）——用法与工作室模式的 `final_review.visual_spotcheck` 相同。
- **渲染**：`npx hyperframes render . --output renders/<name>.mp4`。
  > 已知差距（F13）：`hyperframes_compose.render` 目前需要来自模板化路径的 `edit_decisions.cuts[]`。对于手工编写的 HF 合成，它会报错；在工具增长出定制分支之前，直接调用 `npx`。

## 防止反作用的防护措施

- **独特性审查（取代一致性审查）。** 在最终渲染之前，问：*这可能是任何其他产品的视频吗？它是否重复了我以前做过外观？* 如果是，艺术指导失败——返回第 1 步。这是"是否与参考匹配"的逆运算。
- **不要无声回退到库存。** "保持简单"适用于*机制*（10 行的 spring 没问题），从不适用于*设计*（简单 ≠ 使用 `text_card`）。如果你发现自己在英雄作品中添加库存 `cut.type`，停下来。
- **成本诚实。** 工作室模式比模板化消耗更多的 agent token 和迭代。在提案时就说清楚，让用户知情选择。没有库存基准，质量变化更大——通过强大的原则技能（如上）和独特性审查来缓解，而不是通过重新引入重用。
- **检查点节奏。** 遵循 `skills/meta/checkpoint-protocol.md`：在生成资产前提交脚本 + 场景计划供批准，然后是一个素材/资产检查点，然后是首次渲染检查点。不要在获得签署前批量生成。

## 工作先例（用于*工作流*，而非外观）

两个参考作品——每个运行时一个——用于研究**过程**，而不是视觉语言：

- **Remotion 工作室** — Phantom Reach 解说（`projects/phantom-reach-explainer/`）：Playwright 捕获的应用素材，带 PII 模糊层 → 逐句 TTS 拼接，带静音节拍 → 免费 Pixabay 音乐 → 手工编写的 Remotion 场景（自定义开场、评分环、agent 流程、CTA），使用一次性紫罗兰主题。Compound Snowball（`projects/compound-snowball/`）和 Library of Alexandria（`projects/alexandria-fire/`）是两个更多例子——三个 Remotion 工作室作品，三种完全不同的视觉语言。

- **HyperFrames** — `in-a-hurry`（`projects/in-a-hurry/`）：一个音乐驱动的动态排版作品，使用新的 HF 0.7 `beats` 命令将场景时间锁定到真实节奏点。练习了 **5 个类别**的 `/hyperframes-animation`：`kinetic-beat-slam`、`3d-text-depth-layers`（堆叠挤压）、`motion-blur-streak`（回声鬼影轨迹）、`transitions/css-distortion`（色差 RGB 分离）和 `adapters/html-in-canvas-patterns`（Three.js + UnrealBloom 在英雄点睛之笔上）。每个节拍使用不同的缓动（`expo.out`、`back.out(2)`、`circ.out`、`sine.inOut`）。

**不要复制它们中的任何视觉语言**——下一篇作品必须与它们中的任何一个看起来都不同。这就是全部的意义。只研究*过程*（决策、顺序、门控、验证）。

另见：`skills/meta/animation-runtime-selector.md`（运行时 + 库路由）、`AGENT_GUIDE.md` → "Composition Authoring Mode"、`/hyperframes`（HF 路由器和能力地图）。
