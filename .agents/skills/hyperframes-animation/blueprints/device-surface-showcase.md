# device-surface-showcase — 设备 / 表面展示

**意图**：一个产品表面——一个设备模拟或浮动浏览器/应用窗口——是画面中保持的主角，其屏幕经历真实流程循环，由覆盖从静态保持到连续 3D 推进范围的摄像机动作展示。

**服务角色**

- Key_Feature（来自 key-feature-device-screen-tour、key-feature-floating-window-scroll、key-feature-3d-device-hand-demo）：展示在其实**际界面**内**体验的一个功能——表面容纳动作，其屏幕推进通过一个流程，而非列举方块或追逐光标穿过工作流。（注意：所有三个草稿都是 Key_Feature；此蓝图角色窄但机制丰富——变体按**机制**区分，而非角色。）
- Key_Feature（来自 demo-page-scroll-spotlight）：浮动窗口推进滚动变体，带到聚光灯高潮——一个真实的网页渲染为倾斜 3D 卡片，平稳滑入（power2，像举起的手机——无弹簧），头部关键词在 VO 命名时以卡拉 OK 辉光闪光，页面滚动到演示部分，一个元素在径向聚光灯下**抬起**离开表面（translateZ + 缩放），聚光灯使其余部分变暗。

**时长**：5–9.6 秒（page-scroll-spotlight 5–9 秒 · floating-window 7.8 秒 · 3d-hand 7.9 秒 · device-tour 9.6 秒）

**镜头结构**
一个产品表面 — `[device mockup]` 或 `[floating browser/app window]` — 是 `[styled backdrop: gradient / radial / stylized 3D void]` 上的持久主角；其 `[screens/sections]` 通过真实 `[product flow]` 循环，同时展示摄像机（静态保持、推进→拉远、或一次连续推进）呈现它。每个屏幕状态保持 ~1.0–1.5 秒。

- 场景 1（0.0–~1.5 秒）：表面**建立** — 它 `[从边缘滑入 / 从倾斜漂移进入 / 从全帧标题卡片溶解]` 并稳定，一个 `[accent shape or backdrop]` 在其后解析；第一个 `[screen]` 可见。展示摄像机开始（参见变体）。
- 场景 2（~1.5–~Xs）：表面在其自身面上被**操作** — 一个 `[tap/select/scroll]` 触发第一个屏幕前进：旧内容 `[推出 / 向上滚动]`，新 `[screen/section]` `[从侧边拉上 / 推入]`；同时一个 `[label / header word / side headline]` 更新。摄像机继续其移动。
- 场景 3+（~Xs–结束，对 `[2–4 个屏幕节拍]` 重复）：表面推进通过连续的 `[screens/sections]`，每个是离散交换或滚动，与表面的流程同步，同时辅助文案 `[换出向上 / 向上进入]` 或保持标记以维持阅读位置。在最终 `[screen]` 上**保持**（或对于一种变体，绽放退出 — 参见变体）。

- 变体 — 静态巡览（key-feature-device-screen-tour，9.6 秒）：一个 `[device mockup]` 从屏幕外滑入并稳定（缓出）；一个 `[accent-color shape]` 在其后放大（弹簧过冲）。摄像机在整个剪辑中**保持静态** — 所有运动是元素/UI 级别的：一个点击**压缩**按钮（95%→100%），UI 滚动/过渡到下一个视图（旧推出，新拉上），一个 `[side headline]` 在设备旁边**交换**（旧上滑 + 淡出，新上滑 + 淡入）每屏。在最终屏幕上保持。无摄像机移动，无光标。
- 变体 — 浮动窗口（key-feature-floating-window-scroll，7.8 秒）：开在满帧 `[title card]` 上（一个小 `[icon]` 在中心绘制，`[feature name]` 在其下；保持 ~2 秒），它**溶解**到一个浮动在 `[vivid gradient]` 上的 `[macOS-style browser/app window]`（交通灯 + `[URL pill]` + 标签；左导航，中央内容，右侧 `[sidebar]`）。摄像机**推进**到 `[target region/sidebar]`（活动项高亮 `[accent]`，一个光标在列表中向下漂移），然后**拉远**重新构图整个窗口，同时内容**滚动**通过 `[sections]`；`[highlighted item]` 保持标记。一次推入→拉远弧线，由标题卡片开篇控制。
- 变体 — 3D 手（key-feature-3d-device-hand-demo，7.9 秒）：完全 3D — 一个 `[3D device]` 漂移进 `[stylized 3D void / bloom + particles]`，打开时倾斜并自旋转到几乎面向镜头，同时**一次连续向前摄像机推进**开始（无切）。一个光泽 `[3D hand]` 从底部前景升起并用**手势驱动**表面：它滑动以滚动 `[picker/sidebar panel]` 的 `[option cards]`，并点击 `[option]`（同时一个 `[header word]` 在原位字母翻转）；选择**应用** — 一个 `[new layout]` 从中心生长填满设备面，导航翻转，一个 `[marquee]` 水平滚动；手再次滑动以向上滚动页面通过 `[sections]`，然后漂离。摄像机从未停止推进；明亮的设备面不断向镜头生长，直到它**绽放**成 `[light]` 冲刷——一个缩放通过"门户"退出，填满画面。

**动词语汇**
表面建立（边缘滑入 + 稳定 / 倾斜漂移进入 + 自旋转面向摄像机 / 标题卡片溶解）；重音形状在表面后弹簧；元素级别屏幕循环（滚动交换、从侧边推入、缩放交换）；按钮点击压缩；错开侧标题揭示 + 文案交换（上出 / 上入）；原位头部词语字母翻转；浮动浏览器窗口-在渐变上空闲浮动；全帧标题卡片开场（图标绘制 + 标签）；摄像机推入到区域；摄像机拉远重新构图；内容滚动通过；一次连续 3D 摄像机跟随推进（无切）；3D 设备漂移 + 自旋转；风格化环境绽放/粒子；3D 手进入 + 滑动滚动 + 点击（手势驱动）；选择器面板滑入；模板应用从中心生长；水平游走字幕滚动；手势驱动页面滚动；缩放通过绽放/门户退出；静态保持（无摄像机）作为摄像机范围的基底。

**规则映射**（每个动作动词 → 支持规则，或标记特殊）

- 屏幕循环 — UI 在表面内滚动/部分滚动（设备巡览、浮动窗口滚动、3D 手页面滚动）→ `3d-page-scroll`（网页/应用作为倾斜卡片，其内容 `translateY` 滚动到各部分；表面屏幕流的主要机制）
- 浮动窗口建立 + 表面呈现为倾斜/浮动 UI 卡片 → `3d-page-scroll`（倾斜/透视框架）+ `css-3d-transforms`（perspective/`translateZ` 深度）
- 屏幕/侧文案状态交换（离散屏幕状态；侧标题内容每节拍交换）→ `discrete-text-sequence`
- 侧标题揭示（错开淡入 + 上滑）→ `discrete-text-sequence`
- 原位头部词语字母翻转（3d-hand）→ `hacker-flip-3d`
- 作为两个屏幕状态之间协调缩出/弹出的屏幕交换 → `scale-swap-transition`
- 模板应用"新布局从中心生长填满面"（3d-hand）→ `center-outward-expansion`（集中在中心 → 扩展到填满）
- 状态之间表面变形 / 标题卡片→窗口溶解作为眼锚过渡 → `card-morph-anchor`
- 按钮点击压缩（95%→100% 按下反馈）→ `press-release-spring`（或 `physics-press-reaction` 用于更重的按下）
- 浮动窗口光标点击高亮列表项 → `cursor-click-ripple`
- 活动侧边栏/列表项上的重音高亮弹出 → `asr-keyword-glow`（聚焦项上的重音辉光）
- 在侧边栏列表中漂移的光标（浮动窗口）→ `camera-cursor-tracking`（平面光标漂移；与推进配对）
- 浮动浏览器窗口空闲浮动 / 3D 设备漂移呼吸 → `sine-wave-loop`
- 3D 设备漂移 + 自旋转面向镜头 + 透视深度（3d-hand）→ `css-3d-transforms`（CSS-3D）**或** `3d.md` 技术（真正的 Three.js/R3F 设备）；参见摄像机修饰
- 水平 `[marquee]` 滚动（3d-hand）→ `viewport-change`（游走字幕条上的 PAN 模式）— _薄匹配；字面 CSS 游走字幕/translateX 循环更接近 `gsap-effects`/CSS 配方，而非命名的动效规则_
- 3D 手进入 + 滑动 + 点击作为交互**驱动**（手势输入，滚动/选择）→ **标记为特殊 — 需要超出规则库的更重能力（R3F/Three.js + WebGL），非动效形状规则。** 3D 手模型 + WebGL 绽放有_技术_支持（`3d.md` — R3F、`useGLTF` HandModel、用于着色器/绽放的 `--gl=swiftshader`），但没有任何动效形状规则将 3D 手建模为滑动到滚动 / 点击到选择的手势协议。`context-sensitive-cursor` / `camera-cursor-tracking` 仅建模平面打字/指针光标，非 3D 做手势的手。
- 缩放通过绽放/门户退出（3d-hand）→ **标记为特殊 — 需要超出规则库的更重能力（WebGL），非命名的过渡规则。** 能力是 `techniques.md` → WebGL 着色器（通过 `3d.md` headless WebGL：`--gl=swiftshader --concurrency=1`），但没有命名的过渡规则覆盖绽放/门户飞越。

**摄像机修饰**：展示摄像机跨越一个按变体关键的范围，都在单个内容包裹虚拟摄像机上（`viewport-change`）：

- 静态巡览 → 无摄像机移动（`viewport-change` 保持在缩放 1，或省略）；所有运动是元素级别。这是范围的基底，也是区分设备巡览与其他变体的关键。
- 浮动窗口 → 一个两阶段推进 → 拉远弧线 → `multi-phase-camera`（例如 1.1→1.0→0.95 感的戏剧性揭示）：通过 `coordinate-target-zoom`（偏离中心目标 = 缩放 + 反向平移）推进到 `[sidebar/region]`，然后 `multi-phase-camera` 拉远重新构图整个窗口，同时内容滚动。
- 3D 手 → 一次连续向前推进（无切）→ `multi-phase-camera` 在稳定推进模式（1.0→1.03→1.06… 加上其正弦微漂移）叠加在 `css-3d-transforms`/`3d.md` 上，使设备在推进期间自旋转面向镜头；推进不间断地运行到绽放/门户退出（退出本身是上面标记为特殊的 WebGL 着色器特殊）。
  在所有三种中：`viewport-change` 是基础虚拟摄像机原语；`multi-phase-camera` 排序推进/缩放阶段（并提供始终开启的微漂移，即使"静态"巡览也不感觉死板）；`coordinate-target-zoom` 将推进瞄准偏离中心屏幕细节。

**溢出（平移/滚动表面 — 对干净的 `inspect` 必需）：** 平移或滚动的表面有意将内容移动到其框架卡片的**边缘之外**。在卡片处裁剪它（在卡片/窗口上设置 `overflow: hidden`）并标记移动的内层（`.world` / 持有截图的表面包裹 + 任何标记/标签）为 `data-layout-allow-overflow` — 否则 `inspect` 会为滚动出画面的部分（例如，标记标签从左边缘平移出去）报告 `text_box_overflow` / `container_overflow` **错误**。卡片在视觉上裁剪它们；属性告诉 `inspect` 这是有意的，而非布局错误。
