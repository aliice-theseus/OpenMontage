# 规则索引

原子运动配方。每个位于 `rules/<name>.md`。每场景组合 2-4 个，使用单个暂停时间线。

## 文本与排版

<rules>
<hacker-flip-3d path="rules/hacker-flip-3d.md">字符级 3D 旋转，带确定性字形替换（解密）。GSAP `back.out` 缓动 + 逐字形 `onUpdate` 用于闪烁哈希。标签：text, 3d, reveal, decode</hacker-flip-3d>
<vertical-spring-ticker path="rules/vertical-spring-ticker.md">在遮罩列中使用步进 GSAP 补间的老虎机型垂直滚动。标签：text, ticker, scroll, vertical</vertical-spring-ticker>
<counting-dynamic-scale path="rules/counting-dynamic-scale.md">字号随值增长的计数器，递增强调。数字代理上的单个 GSAP 补间。标签：counter, scale, font-size, number, dynamic</counting-dynamic-scale>
<discrete-text-sequence path="rules/discrete-text-sequence.md">在时间阈值处替换整个文本状态，实现非线性打字（输入错误、保持、批量添加、退格）。GSAP onUpdate 驱动的反向搜索。标签：text, typing, discrete, threshold, non-linear</discrete-text-sequence>
<asr-keyword-glow path="rules/asr-keyword-glow.md">以辉光 + 缩放 + 颜色高亮关键词，与 ASR 单词时间戳同步。每个单词两个 GSAP 补间通过攻击-衰减-保持包络驱动 CSS 自定义属性 `--glow`。标签：asr, audio-sync, highlight, glow, keyword, text</asr-keyword-glow>
<3d-text-depth-layers path="rules/3d-text-depth-layers.md">多个偏移文本层（N 个 div 在 `(i*dx, i*dy)` 处递减 alpha）在大号字体上创建堆叠的 3D 挤压幻觉。标签：text, 3d, depth, layers, shadow, typography, stacked</3d-text-depth-layers>
<context-sensitive-cursor path="rules/context-sensitive-cursor.md">打字光标，其 `background-color` 在段边界切换，加上通过 `(tl.time() % cycle) < cycle/2` 的方波闪烁。标签：cursor, color, context, typewriter, styling, segment</context-sensitive-cursor>
<dynamic-content-sequencing path="rules/dynamic-content-sequencing.md">从 `{textMain, textAccent, charSpeed, hold}` 条目的脚本预计算平坦的 `[{startTime, endTime, ...}]` 数组。每个短语窗口 = `chars × charSpeed + hold`。内容驱动时长，无手调偏移。标签：timeline, sequencing, dynamic, duration, script-driven</dynamic-content-sequencing>
<kinetic-beat-slam path="rules/kinetic-beat-slam.md">打击式动感排版 — 简短短语在一个共享节拍数组上猛烈进入，每个短语有**不同**的入场（缩放撞击/侧边快照/上升旋转），可选节奏镀铬（节拍器滴答、节拍条），然后锁定终曲。"有力/节奏"标语的配方。标签：text, kinetic, typography, beat, rhythm, slam, percussive, punchy</kinetic-beat-slam>
</rules>

## 数据与统计

<rules>
<counting-dynamic-scale path="rules/counting-dynamic-scale.md">字号随值增长的计数器；seek 安全 `onUpdate`、`Math.round`、`tabular-nums`、多统计和弦。（也列在文本与排版下。）标签：counter, number, stat, count-up</counting-dynamic-scale>
<stat-bars-and-fills path="rules/stat-bars-and-fills.md">将数字与图形配对的数据可视化原语 — 增长条（CSS `scaleY` 错开）、进度填充（条 `scaleX` 或测量的 SVG 环）和分数星级评分擦拭（`clip-path`）。仅变换，seek 安全。选择单焦点 vs 分屏并保持。标签：data, stats, chart, bars, progress, ring, stars, rating, infographic</stat-bars-and-fills>
</rules>

## 摄像机与视口

<rules>
<coordinate-target-zoom path="rules/coordinate-target-zoom.md">通过缩放（外部包裹容器）+ 反向平移（内部包裹容器）缩放到非居中元素。标签：camera, zoom, scale, translate</coordinate-target-zoom>
<camera-cursor-tracking path="rules/camera-cursor-tracking.md">双阶段虚拟摄像机，将视口锁定到移动焦点（打字光标）— 静态初始构图然后焦点锁定跟踪。在 `document.fonts.ready` 后使用浏览器原生 `getBoundingClientRect()` / `ctx.measureText()`。标签：camera, tracking, viewport, two-phase, typing</camera-cursor-tracking>
<multi-phase-camera path="rules/multi-phase-camera.md">顺序摄像机缩放系统（拉回/聚焦/推进）加连续微漂移。标签：camera, zoom, phase, drift, scale, cinematic</multi-phase-camera>
<viewport-change path="rules/viewport-change.md">虚拟摄像机 — 通过变换包含所有场景内容的单个 `.world` 包裹容器模拟缩放/平移/焦点锁定。单元素复合变换 `translate(x,y) scale(S)`；反向平移数学为 `T = -offset × S`（不同于 coordinate-target-zoom 的 `T = -offset`）。标签：viewport, camera, zoom, pan, focus-lock</viewport-change>
<depth-of-field-blur path="rules/depth-of-field-blur.md">选择性焦距拉动 — 通过 `--dof` 变量在脱焦层上 GSAP 补间 `filter: blur()`（+轻微不透明度变暗），同时聚焦元素保持清晰；单次拉动、双平面切换、或推进时模糊集群。有限、确定性、seek 安全。标签：blur, depth-of-field, focus, rack-focus, dim, spotlight</depth-of-field-blur>
</rules>

## 布局与网络

<rules>
<avatar-cloud-network path="rules/avatar-cloud-network.md">椭圆环上的头像，带 SVG 连接到中心点的线，错开进入。云中心坐标必须与中心件元素精确匹配。标签：avatar, cloud, network, social-proof, stagger</avatar-cloud-network>
<3d-page-scroll path="rules/3d-page-scroll.md">完整网页渲染为倾斜的 3D 卡片，其内部内容滚动以揭示特定部分。与 asr-keyword-glow 配合作页面关键词高亮。标签：3d, page, scroll, webpage, tilt, perspective, product-demo</3d-page-scroll>
<center-outward-expansion path="rules/center-outward-expansion.md">元素从屏幕中心聚集开始扩展到最终位置。每个元素通过 CSS 获得其目标位置一次；GSAP 补间变换 `x` / `y` 与共享驱动器步调一致偏移到 0。标签：expansion, scatter, center, reveal, layout, sync</center-outward-expansion>
<split-tilt-cards path="rules/split-tilt-cards.md">两张卡片并排，相反 rotationY 倾斜（+/- 基础倾斜）并从各自侧边滑入。连续浮动以相位相反运行（`Math.PI` 偏移）。标签：3d, cards, split, tilt, comparison, symmetric</split-tilt-cards>
<orbit-3d-entry path="rules/orbit-3d-entry.md">元素从 3D 空间翻转入场（`rotateX` + `rotateY` + `translateZ`）然后稳定到连续椭圆轨道。**关键**：入场必须在轨道起始位置原位翻转（`gsap.set` 在阶段 1**之前**），而非场景中心。标签：orbit, 3d, flip, ellipse, circular, icon, entry, continuous</orbit-3d-entry>
<ai-tracking-box path="rules/ai-tracking-box.md">AI 检测叠加 — 黄色 `#facc15` L 形支架角 + 置信度标签（波动 95-99%）在正弦弧路径上跟随目标。框位置每帧从目标位置重新计算（从不单独补间）。标签：ai, tracking, bounding-box, detection, corner, ml</ai-tracking-box>
<depth-scatter-assemble path="rules/depth-scatter-assemble.md">N 个元素散开进入/从旋转的 3D 深度云重新组装 — 每个从确定性的索引派生的 3D 偏移（translateZ + rotateX/Y + 散开）开始并稳定到干净的平面布局；翻滚交换和径向爆炸变体。preserve-3d + perspective，仅变换，seek 安全。标签：3d, scatter, assemble, tumble, depth, perspective, glyphs</depth-scatter-assemble>
</rules>

## SVG 与图标

<rules>
<svg-icon-enrichment path="rules/svg-icon-enrichment.md">动画化内部 SVG 元素（旋转指针、振荡刀片、脉冲点、虚线流线）使图标感觉生动。**关键**：使用 SVG `setAttribute('transform', 'rotate(deg cx cy)')` 用于显式中心 — CSS `transform-origin` + `transform-box: fill-box` 在 bbox 局部坐标中解释原点（对于细线条偏离中心）。标签：svtg, icon, animation, micro-animation, rotation, pulse</svg-icon-enrichment>
<svg-path-draw path="rules/svg-path-draw.md">SVG 轮廓逐笔绘制自身，通过 `stroke-dasharray` / `stroke-dashoffset`。在组合设置时使用 `getTotalLength()` 测量，设置初始 dashoffset = 长度，GSAP 补间到 0。对于环形进度环，将描画旋转 `-90deg`，使绘制从 12 点钟开始。标签：svg, stroke, draw, vector, path, dasharray</svg-path-draw>
</rules>

## 空闲与环境

<rules>
<sine-wave-loop path="rules/sine-wave-loop.md">连续呼吸/空闲环境运动。两种形式：GSAP `sine.inOut` yoyo 有限重复（独立时首选）或读取 `tl.time()` 的 onUpdate（乘到另一个实时值上时首选）。标签：idle, loop, breathing, sine, ambient</sine-wave-loop>
<ambient-glow-bloom path="rules/ambient-glow-bloom.md">无触发柔和径向辉光，在主角元素后绽放并保持带有限空闲呼吸，或一次穿过表面的单次移动光泽。无点击、无单词同步；峰值不透明度 ≤ ~0.45，有限/确定性。标签：glow, bloom, ambient, radial, sheen, hero</ambient-glow-bloom>
</rules>

## 过渡与运动

<rules>
<reactive-displacement path="rules/reactive-displacement.md">物理碰撞过渡，进入元素的 GSAP 补间驱动退出元素的位移。在相同时间线位置的三个并发补间，受害者时长为侵入者的 40-50%。标签：transition, physics, collision, displacement, push</reactive-displacement>
<press-release-spring path="rules/press-release-spring.md">触觉按钮按下：线性压缩然后弹簧恢复，通过相同属性上的两个相邻 GSAP 补间。变体：颜色过渡、通过 CSS 变量的阴影深度、释放爆发、背景辉光。标签：spring, press, button, interaction, physics, glow, burst</press-release-spring>
<physics-press-reaction path="rules/physics-press-reaction.md">物理点击模拟 — 两个顺序 GSAP 缩放补间（降到 0.9，升到 1.0）近似带过冲的弹簧。传递单个目标数组 `["#cta", "#cursor"]` 同时压缩两者以获得触觉接触感。标签：spring, click, physics, press, interaction, cursor</physics-press-reaction>
<cursor-click-ripple path="rules/cursor-click-ripple.md">动画光标移动到目标，在点击时同时下压光标 + 目标，发出带攻击-衰减不透明度包络的扩展涟漪。元素从 t=0 在 DOM 中存在，带 `opacity: 0`（无条件渲染）。标签：cursor, click, ripple, interaction, mouse, button, keyframes</cursor-click-ripple>
<scale-swap-transition path="rules/scale-swap-transition.md">两个 DOM 元素在同一屏幕中心的协调变形。退出集群缩小 + 淡出；进入以 `back.out(2)` 过冲弹入。标签：transition, morph, scale, swap</scale-swap-transition>
<card-morph-anchor path="rules/card-morph-anchor.md">容器在两种镜头之间变形表观尺寸 + 圆角半径 + 表面处理，然后淡出以揭示其下真实目标。HyperFrames 用均匀 `scale` 替代禁止的 `width`/`height` 补间，加上仅绘制的 `borderRadius`/`background`/`boxShadow`。标签：morph, anchor, transition, border-radius, container, shape, handoff</card-morph-anchor>
<spring-pop-entrance path="rules/spring-pop-entrance.md">规范的入场弹出 — 元素（或错开组）通过 `back.out` 过冲 `scale: 0 → 1` 弹簧进入，`fromTo` 使其在 seek 下 t=0 时正确。单主角、错开组（≤500ms 上限）、过冲按个性调谐。与 `press-release-spring`（点击/按下反应）不同。标签：spring, entrance, pop, scale-in, overshoot, stagger, arrival</spring-pop-entrance>
<motion-blur-streak path="rules/motion-blur-streak.md">快速入场/摄像机推进穿过的伪造方向速度模糊 — 模糊在最大速度时达到峰值，在稳定时解析为 0。两条路径：运动轴上的 SVG `feGaussianBlur` stdDeviation（通过代理补间），或塌缩到前导的确定性回声/鬼影轨迹。仅入场/镜头中段。标签：motion-blur, streak, velocity, ghost, echo, fast</motion-blur-streak>
</rules>

## 特效配方（从 hyperframes-creative 迁移）

<rules>
<gsap-effects path="rules/gsap-effects.md">即用 GSAP 时间线模式 — 打字机、音频可视化器和其他可重用的编排块。标签：gsap, recipe, drop-in, typewriter, audio-visualizer</gsap-effects>
<css-marker-patterns path="rules/css-marker-patterns.md">标记高亮绘制模式的纯 CSS + GSAP 实现 — 高亮（黄色扫过）、圆圈（手绘椭圆）、爆发（辐射线）、涂鸦（混乱）、素描（粗糙矩形轮廓）。标签：css, marker, highlight, text, emphasis</css-marker-patterns>
</rules>

## 参见

- `blueprints-index.md` — 场景形状模板（此技能的"蓝图"），将规则组合成完整镜头
- `techniques.md` — 更广泛的动效设计技巧（SVG 路径绘制、Canvas 2D、CSS 3D、动感排版、可变字体、合成）；几个规则引用它
- `transitions/` — 场景过渡目录（共享技能；故事拥有 `transition_in`，线束注入它）
