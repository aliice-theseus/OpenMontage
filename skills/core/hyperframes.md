# HyperFrames 技能（第二层）

本文是 **OpenMontage 专用**的 HyperFrames 指南。它说明了在什么情况下 OpenMontage 流水线应选择 HyperFrames 而非 Remotion，OpenMontage 的工件如何映射到 HyperFrames 项目文件，以及合成阶段如何驱动 HyperFrames CLI。

关于 HyperFrames 原始知识（创作契约、`data-*` 属性、GSAP 时间线规则、CLI 标志、注册表块、网站转视频），请阅读第三层技能：

- `.agents/skills/hyperframes/`——路由到以下专注技能（HF 0.7+ 将单体技能拆分）
- `.agents/skills/hyperframes-core/`——合成契约：`data-*` 时序、轨道、子合成、确定性渲染规则
- `.agents/skills/hyperframes-creative/`——非动画创意指导：调色板、字体、旁白、节奏规划
- `.agents/skills/hyperframes-media/`——TTS/BGM/SFX/转写/字幕/背景移除
- `.agents/skills/hyperframes-animation/`——所有运动知识（规则、蓝图、转场、运行时适配器）
- `.agents/skills/hyperframes-cli/`——init、add、lint、validate、inspect、snapshot、preview、render、benchmark、lambda、doctor（0.7+）
- `.agents/skills/hyperframes-registry/`——`hyperframes add` + 块接线
- `.agents/skills/website-to-video/`——捕获到视频的工作流（0.7 版从 website-to-video 重命名）
- `.agents/skills/music-to-video/`——使用 `hyperframes beats` 的节拍同步音乐驱动视频
- `.agents/skills/motion-graphics/`——简短的设计主导运动图形模式
- `.agents/skills/media-use/`——用于 BGM/SFX/图像/图标的 `resolve` 动词（任何流水线、任何运行时）
- `.agents/skills/remotion-to-hyperframes/`——仅当用户明确要求移植 Remotion 源码时进行迁移

本文件教授两者之间的桥梁。

---

## OpenMontage 何时选择 HyperFrames（对比 Remotion 和 FFmpeg）

OpenMontage 区分两个概念：

- **`renderer_family`**——创作语法（`explainer-data`、`cinematic-trailer`、`product-reveal` 等）。在提案阶段选定。
- **`render_runtime`**——实现该语法的技术引擎（`remotion`、`hyperframes`、`ffmpeg`）。也在提案阶段选定。

两者都在 `proposal_packet.schema.json` 中锁定，并在 `edit_decisions` 中保持不变，除非在 `decision_log` 中记录了 `render_runtime_selection` 决策。静默切换运行时是违反契约的行为。

### 决策矩阵

| 场景 | 优先选择 | 原因 |
|----------|--------|-----|
| 现有讲解视频、React 场景组件栈（text_card、stat_card、图表场景、字幕叠加、TalkingHead、CinematicRenderer） | **Remotion** | 这些合成已存在于 `remotion-composer/`。复用它们是零成本的；在 HTML 中复制它们则不是。 |
| 单词级字幕烧录 / 卡拉 OK 字幕 | **Remotion** | `remotion_caption_burn` 是 Remotion 特有的，在 HyperFrames 上第一天就存在差异。 |
| 虚拟形象 / 唇同步主持人 | **Remotion** | `TalkingHead` 合成存在于 Remotion。HyperFrames 尚无等效实现。 |
| 动态排版、大量文字动画、GSAP 原生动画 | **HyperFrames** | HTML/GSAP 是天然媒介。将其表达为 Remotion 的 `interpolate()` 调用既慢又脆弱。 |
| 产品推广 / 发布预告 / 营销标题卡片 | **HyperFrames** | CSS/GSAP 合成语法与设计师的思维模式一致。模板（`kinetic-type`、`product-promo`、`swiss-grid`）提供了很好的起点。 |
| 网站转视频 / UI 驱动的合成 | **HyperFrames** | `website-to-video` 工作流正是为此而生。 |
| 需要注册表块（数据图表、颗粒叠加、闪光扫过、着色器转场） | **HyperFrames** | 注册表是 HyperFrames 独有的。Remotion 没有 `hyperframes add`。 |
| 合成 UI / 模拟终端 / 模拟浏览器演示 | 两者均可——取决于现有覆盖范围 | OpenMontage 已随附 Remotion `TerminalScene`（参见第三层 `synthetic-screen-recording`）。对于终端以外的 UI 界面，HyperFrames HTML 更简单。 |
| 纯拼接/裁剪源片段，无需合成 | **FFmpeg** | Remotion 和 HyperFrames 在此场景中都没有增加价值。 |
| 本机未安装 Remotion | **HyperFrames**（如果可用）或 **FFmpeg** | 不要静默回退。在降级前告知用户。 |

### 硬性规则：当两种运行时都可用时，应同时呈现

上述决策矩阵是供与用户对话时参考的输入，而不是静默选择"默认值"的许可。当本机同时安装了 Remotion 和 HyperFrames 时，提案阶段必须：

1. 向用户同时呈现两者，并附带针对具体需求的优缺点。
2. 推荐其中一个，并提供与 `delivery_promise` 和 `visual_approach` 相关的理由。
3. 等待批准。
4. 在 `render_runtime_selection` 决策的 `options_considered` 中记录两者。

详见 `AGENT_GUIDE.md` → "同时呈现两种合成运行时（硬性规则）"的完整契约，以及 `skills/meta/reviewer.md` 中的 CRITICAL 级别发现强制机制。

### 硬性规则：需要动画的交付物

如果需求的 `delivery_promise.motion_required` 为 `true`（科幻预告片、电影感预告、混剪、任何依赖于真实运动的承诺），则在提案阶段选择的运行时是一个**承诺**，而非提示。合成阶段不得降级到 FFmpeg Ken Burns。如果选定的运行时失败（未安装 Remotion、`npx hyperframes doctor` 报告阻塞），则按照 `AGENT_GUIDE.md` > "明确上报阻塞问题"处理，并在切换运行时之前等待用户批准。

---

## 保持 Remotion 独占的内容（第一阶段）

**不要**在第一天就尝试将这些移植到 HyperFrames。它们需要专门的等效性工作：

- `remotion_caption_burn`（逐字烧录字幕）
- `TalkingHead` 合成（虚拟形象/唇同步主持人）
- 现有的纪录片蒙太奇结尾标签叠加栈（依赖于特定的 Remotion 组件）
- 任何假定资源存放在 `remotion-composer/public/` 下并由现有 React 场景组件消费的内容

对于这些，保持 `render_runtime = "remotion"` 并照常进行。

---

## 项目工作空间布局

HyperFrames 需要自己的项目工作空间。**不要**复用 `remotion-composer/public/`——那是 Remotion 的共享暂存目录，混合运行时会导致跨项目冲突。

```
projects/<项目名称>/
├── artifacts/
├── assets/
│   ├── images/
│   ├── video/
│   ├── audio/
│   └── music/
├── hyperframes/                ← HyperFrames 运行时工作空间（当被选中时）
│   ├── index.html              ← 根合成
│   ├── compositions/           ← 子合成和注册表块
│   │   └── components/         ← 注册表组件（颗粒叠加等）
│   ├── assets/                 ← 项目资源的符号链接或副本
│   ├── hyperframes.json        ← CLI 配置（注册表 URL、安装路径）
│   ├── DESIGN.md               ← 从风格手册派生的视觉需求（可选）
│   └── narration.wav           ← TTS 输出（如适用）
└── renders/
    └── final.mp4
```

工作空间在合成时由 `hyperframes_compose` 根据 `edit_decisions` + `asset_manifest` + 激活的风格手册生成。它是可重新生成的，并与 `projects/` 的其他部分一起被 gitignore 忽略。

### 为什么每个项目需要独立的工作空间

- HyperFrames 相对于项目根目录解析 `data-composition-src`、`src=` 和注册表块。共享工作空间会破坏这一点。
- `npx hyperframes lint | validate | render` 都基于项目目录操作。它们不像 Remotion 那样接受抽象的合成 ID。
- 资源与引用它们的 HTML 相邻存放，这与 `website-to-video` 的参考工作流一致。

---

## 工件到 HyperFrames 的映射

当 `render_runtime = "hyperframes"` 时，合成阶段将 OpenMontage 工件转换为 HyperFrames 项目文件：

| OpenMontage 工件字段 | HyperFrames 目标 |
|---|---|
| `edit_decisions.cuts[]`（场景序列） | `index.html` 时间线，每个剪辑一个 `<div data-composition-id data-composition-src>` |
| `edit_decisions.cuts[i].in_seconds / out_seconds` | 剪辑元素上的 `data-start` / `data-duration` |
| `edit_decisions.cuts[i].type`（场景类型） | 通过 `hyperframes add` 安装的注册表块，或手写的子合成模板 |
| `asset_manifest.assets[]` 路径 | 复制或符号链接到 `projects/<p>/hyperframes/assets/` 中，并使用相对路径 `src=` 引用 |
| `audio.narration.segments[]` | 带匹配 `data-start` / `data-duration` 的 `<audio>` 元素 |
| `audio.music` | 第二个 `<audio>` 元素，较低 `data-volume` |
| `subtitles`（启用 + 来源） | 注册表的 `captions` 块或手写的逐词跨度——**不是** `remotion_caption_burn` |
| 选定的风格手册（`flat-motion-graphics`、`clean-professional` 等） | `:root` CSS 自定义属性 + `DESIGN.md`。参见 `lib/hyperframes_style_bridge.py`。 |
| `renderer_family` | 控制使用哪个顶层 HTML 模板以及预安装哪些注册表块 |

具体的渲染过程是：`hyperframes_compose` 将文件写入工作空间，运行 `lint → validate → render`，然后返回包含生成 MP4 路径的 `render_report`。参见 `tools/video/hyperframes_compose.py`。

### 工作空间本地的创作工件

上游的 `website-to-video` 技能使用 `DESIGN.md`、`SCRIPT.md` 和 `STORYBOARD.md` 作为逐步工作空间文件。OpenMontage **不会**用这些文件替换其规范工件契约——`brief`、`script`、`scene_plan`、`edit_decisions` 等仍然是 `projects/<p>/artifacts/` 下的真实数据源。将上游文件视为写入 HyperFrames 工作空间的**便利副本**，使运行时工作流感觉自然：

- `DESIGN.md`——从选定的风格手册派生，由 `hyperframes_compose` 或 `lib/hyperframes_style_bridge.py` 写入。可安全地用作工作空间中的工作需求文档。
- `SCRIPT.md`——可选的旁白副本，供人工审核。规范脚本保留在 `artifacts/script.json` 中。
- `STORYBOARD.md`——可选的逐节奏创意指导。规范场景计划保留在 `artifacts/scene_plan.json` 中。

如果工作空间本地文件与规范工件不一致，以规范工件为准。

---

## 运行时选择规则

1. **提案阶段**选择 `render_runtime` 并在 `decision_log` 中以 `render_runtime_selection` 类别记录该决策。它必须考虑上述决策矩阵以及每个运行时的实际可用性。
2. **预检阶段**报告哪些运行时可用（见下文）。不可用的运行时不是有效的提案选择，除非用户明确批准安装它。
3. **剪辑阶段**将 `render_runtime` 保持不变地传递。
4. **合成阶段**读取 `edit_decisions.render_runtime` 并通过 `video_compose` 路由到 `hyperframes_compose`（对于 HyperFrames）或现有的 Remotion 路径（对于 Remotion）。未经新的 `render_runtime_selection` 决策，合成阶段不得切换运行时。
5. **最终审核**记录 `render_runtime_used`，如果与提案阶段不同，则将 `runtime_swap_detected` 设置为 `true`。

---

## 预检——HyperFrames 可用性

在预检阶段，提供商菜单报告 HyperFrames 的可用性。`hyperframes_compose` 工具的 `get_info()` 返回：

```json
{
  "runtime_available": true | false,
  "node_major": 22,
  "ffmpeg_available": true,
  "doctor_ok": true,
  "install_instructions": "…"
}
```

最低要求（所有条件必须满足才能 `runtime_available: true`）：

- Node.js 主版本 ≥ 22
- `ffmpeg` 二进制文件在 PATH 中
- `npx` 在 PATH 中（随 Node.js 一起提供）
- `npx hyperframes doctor` 退出码为 0，或通过轻量级等效检查

**不需要** `bun`——HyperFrames 可通过 `npx hyperframes` 使用（发布的 npm 包名称为 `hyperframes`；monorepo 内部使用的 `@hyperframes/cli` 名称不在公共 npm 注册表中，会返回 404）。

当 `runtime_available: false` 时，预检必须说明原因并提供安装说明。按照 `AGENT_GUIDE.md` 的设置提供协议，按工作量对修复进行分组：

- 缺少 Node 22 → 5 分钟安装，说明它能解锁什么
- 缺少 FFmpeg → macOS/Linux 上 1 分钟安装，Windows 上稍长
- `doctor` 报告问题 → 逐字显示 doctor 输出

---

## 验证协议

HyperFrames 配备了一整套验证工具。在宣布渲染完成之前，请**全部**运行：

1. **`npx hyperframes lint`**——静态契约检查（重复 ID、重叠轨道、缺少 `data-composition-id`、未注册的时间线）。必须在渲染前通过。
2. **`npx hyperframes validate`**——基于浏览器的运行时检查：定位到暂停的合成中、截图、采样像素、计算 WCAG 对比度、验证 `window.__timelines` 注册和定时元素上的 `class="clip"`。必须在渲染前通过（对比度检查在迭代期间可以使用 `--no-contrast` 推迟，但最终版本不可以）。
3. **`npx hyperframes render --quality standard`**——生成 MP4。
4. **渲染后最终审核**——用 ffprobe 探测、采样帧、转写音频、与脚本比对。与 Remotion 路径的契约相同。参见 `final_review.schema.json`。

如果 lint 或 validate 失败，**不要**渲染。修复合成并重新运行。从失败的合成进行静默渲染是违反契约的行为——HyperFrames 的全部意义就在于 validate 能捕获 FFmpeg 或 Remotion 无法发现的问题。

---

## 样式桥接（风格手册 → CSS）

OpenMontage 风格手册目前会转换为 Remotion 的 `themeConfig` 对象。对于 HyperFrames，等效转换会生成：

- 在 `:root` 上的一组 CSS 自定义属性（`--color-bg`、`--color-fg`、`--color-accent`、`--font-heading`、`--font-body`、`--ease-primary`、`--duration-primary` 等）。
- 一份简短的 `DESIGN.md`，用通俗语言解释视觉系统。
- 可选的字体 `@import` 语句（仅限 HyperFrames 字体编译器支持的字体）。

参见 `lib/hyperframes_style_bridge.py`。风格手册不需要分叉——现有的风格手册模式携带了足够的信息来驱动 Remotion 和 HyperFrames 的输出。

---

## 成本模型

HyperFrames 渲染是本地进行的：API 成本为 $0，但属于 CPU 密集型（无头 Chrome + FFmpeg）。通过 `cost_tracker` 追踪：

- `estimate`——基于合成时长 × 分辨率 × `--workers`
- `reserve`——0（无 API 支出）
- `reconcile`——壁钟渲染时间

与 Remotion 相同的模式。

---

## 实践中的陷阱（来之不易的经验）

上游文档没有警告但会让你花 60 分钟渲染来发现的问题。在创作时修复，而不是在渲染时修复。

### 全帧背景视频：源分辨率陷阱（不是框架错误）

症状：背景视频渲染为居中的小黑框，周围是黑色区域，即使你已经告诉 HyperFrames 该片段是 1920×1080。六次渲染的调试发现，这**几乎始终是源质量问题，而非 HyperFrames 的框架错误。** 修复输入，而不是 CSS。

根本原因（在 Pexels + Pixabay 素材上观察到）：许多免费素材片段即使你要求"大"尺寸级别，也以 640×360 或 960×540 提供。如果你的预处理使用 `scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:...`，你会得到一个 1920×1080 的文件，但其可见内容是一个居中的 640×360 矩形，带有黑色填充。HyperFrames 会忠实播放该片段——你看到的黑框中微小视频实际上是正确渲染的带黑边的输入。

诊断方法：在归咎 CSS 之前，先对源片段和预处理后的片段运行 `ffprobe -v error -select_streams v -show_entries stream=width,height`。如果预处理后的片段在 1920×1080 的填充内已经显示 640×360 的有效区域，那么问题出在上游。

修复预处理，使用缩放覆盖（scale-to-COVER）并裁剪，而不是缩放适应（scale-to-FIT）并填充：

```
-vf "scale=1920:1080:force_original_aspect_ratio=increase,\
     crop=1920:1080,unsharp=3:3:0.6"
```

这将小片段放大到至少覆盖 1920×1080，裁剪溢出部分，并锐化（unsharp）以补偿可见的柔化。输出是全幅的，HyperFrames 将边到边渲染。

规范的包裹层 div 模式（`patterns.md`）仍然是背景的正确 HTML 结构：

```html
<div style="position:absolute;top:0;left:0;width:1920px;height:1080px;overflow:hidden;">
  <video
    data-start="0" data-duration="60" data-track-index="0"
    src="..." muted playsinline
    style="width:100%;height:100%;object-fit:cover;"
  ></video>
</div>
```

使用它是因为当视频宽高比与 16:9 略有差异时，包裹层上的 `overflow: hidden` 可以优雅地裁剪，并且内部的 `<video>` 上的 `object-fit: cover` 处理了（罕见的）源宽高比不是 16:9 的情况。它**不是**框架布局问题的变通方法——如果源文件的内容填满了整个帧，框架也会正确调整 `<video class="clip">` 的大小。

在包裹层或作用域选择器（如 `.bg-slot video { filter: ... }`）上应用视觉效果（`filter`、`border-radius` 等）。

隐形与明显的失败模式：当你叠加暗色调滤镜（`brightness(0.25–0.35)`）或全幅文字时，这个陷阱会隐藏起来——黑边部分会被解读为"氛围感黑暗"。当你开始使用画面优先的风格（亮度 > 0.5、底部三分之一文字）时，它就变得明显了。如果你从一开始就计划使用画面优先的风格，请在资源阶段探测源分辨率。

当你确实无法获取高清片段时，请切换流水线：使用 FFmpeg 混合合成（在外部 B 卷中缩放覆盖 + 裁剪 + 锐化，然后通过色度键叠加 HyperFrames 文字）。这就是 `projects/quantum-willow-multiverse/` 在经过六次使用 640×360 Pexels 源的 HyperFrames 渲染后最终采用的模式。

### 在渲染前始终预览浏览画面优先的场景

60 分钟的渲染成本很高。在提交完整渲染之前，打开 Launch 预览面板（或 `npx hyperframes preview`）并浏览到每个章节中至少一个 B 卷应占主导的场景。微小视频错误——以及类似的布局问题，如"底部三分之一文字在 1080p 下显示在屏幕外"——在预览时是 2 秒的视觉检查，在渲染时是 60 分钟的回归代价。

### 提升素材可读性，而非降低不透明度

当在 B 卷上叠加文字时，不要仅仅降低视频不透明度——那样两个图层都会变得浑浊。相反：

- 在视频上保持 `filter: brightness(0.55) saturate(0.85)`（可见但变暗）。
- 在特定文字后面添加局部 CSS 遮罩（`radial-gradient` 或 `linear-gradient`，使用 `rgba(7,7,12,0.5)`），大小与文字块一致。
- 在文字本身使用 `text-shadow: 0 2px 24px rgba(0,0,0,0.8)`，独立于背景提供局部光晕。

这使素材保持生动感，同时确保字幕和标题在任何帧上仍然可读。

### 素材片段在渲染前需要密集关键帧

当素材片段的关键帧间隔 > 5 秒时，渲染会失败并显示 `video_heavy_parallel_timeout` 或产生帧冻结。在将下载的素材放入工作空间之前，务必通过 `ffmpeg ... -c:v libx264 -r 30 -g 30 -keyint_min 30 -sc_threshold 0 -movflags +faststart` 重新编码。参见 `hyperframes_compose` 现有的工作空间准备——它目前还不会自动执行此操作。

### 视频密集型合成使用 `--workers 1` 进行渲染

当多个视频同时加载时，默认的并行捕获会使无头 Chrome 不堪重负。对于包含超过 5 个背景视频元素的任何合成，始终向 `hyperframes render` 传递 `--workers 1`。

### 使用 Outfit / Inter / JetBrains Mono，而非 Space Grotesk

HyperFrames 的确定性字体编译器只会内联它有映射的字体。即使通过 Google Fonts 加载，`Space Grotesk` 也会渲染为回退字体（通常是 Arial）。请检查编译器的警告输出或 `deterministicFonts.ts` 映射表。安全的选择：`Outfit`、`Montserrat`、`Inter`、`JetBrains Mono`、`Poppins`、`Playfair Display`。

## 反模式

- ❌ 在当前模式已经包含颜色、字体和运动信息的情况下，为 HyperFrames 分叉风格手册数据。
- ❌ 编写引用 `remotion-composer/public/` 的 HyperFrames 合成——HyperFrames 工作空间是独立且自包含的。
- ❌ 从 OpenMontage 编排器运行 `hyperframes init`。`init` 会创建自己的项目语义并安装 agent 技能——它适用于人类引导项目，不适用于流水线。`hyperframes_compose` 直接生成项目文件。
- ❌ 将 HyperFrames 用作"没有 Remotion 的 React"。HyperFrames 是 HTML 优先 + GSAP。如果你的场景是以 React JSX 编写的，它属于 Remotion。
- ❌ 在 HyperFrames 内部的 GSAP 中使用 `repeat: -1`。无限补间会破坏确定性寻道和捕获渲染。始终使用有界重复。
- ❌ 在时间线构建期间从 `async` 上下文、`setTimeout` 或 Promise 进行动画。`window.__timelines` 必须在页面加载后同步完全填充。

---

## 采用 HyperFrames 的流水线

| 流水线 | 状态 |
|----------|--------|
| `animation` | 第一波——对于运动图形密集的需求，HyperFrames 是一等选项 |
| `animated-explainer` | 第一波——当概念是 HTML/GSAP 原生时，HyperFrames 可行；数据图表密集的讲解视频仍以 Remotion 为默认 |
| `screen-demo` | 第一波——HyperFrames 适用于合成产品 UI；`TerminalScene`（Remotion）在终端特定演示中仍然更优 |
| `cinematic` | 第二波 |
| `hybrid` | 第二波 |
| `documentary-montage` | 第二波 |
| `talking-head` | 推迟——依赖于 TalkingHead 的等效性 |
| `avatar-spokesperson` | 推迟——依赖于 TalkingHead 的等效性 |
| `clip-factory`、`podcast-repurpose`、`localization-dub` | 推迟——当前合成路径依赖于 Remotion 字幕烧录 |
| `framework-smoke` | 不适用（测试流水线） |

已采纳流水线的提案和合成指导文档明确描述运行时选择——参见每个流水线的 `proposal-director.md` 和 `compose-director.md`。
