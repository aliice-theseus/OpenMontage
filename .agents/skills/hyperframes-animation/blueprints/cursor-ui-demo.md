# cursor-ui-demo — 光标驱动的 UI 演示

**意图**：一个可见的自定义光标通过点击/悬停/拖拽驱动一个真实的（重建的）应用 UI，使屏幕状态逐镜头变化，同时摄像机追逐每次交互 — 产品表面是主体，光标是演员。

**服务角色**

- Product_Intro（来自 `product-intro-cursor-ui-demo` / #14 Product_Intro_02、#15 Product_Intro_2、#17 Product_Intro_04）：产品表面的第一印象 — 光标扫过/悬停以**介绍**应用并揭示它是什么，着陆在一个悬停的主角元素或刚弹出的结果上。轻量、探索性；背景在其进展中逐步换色。
- Key_Feature（来自 `key-feature-cursor-ui-demo` / #23 Key_Feature_2、#24 Key_Feature_03、#27 Key_Feature_06）：一个特定的多步骤工作流**端到端**演示（跨 2–4 个离散节拍的编辑/配置/选择），每个节拍是 UI 实时响应的真实编辑，锁定在主操作按钮或产生的结果上。
- Key_Feature（来自 `workflow-approve-press`）：一个审批/确认工作流，由 3D 倾斜侧翼的驾驶舱框架 — 步骤列表滴答待处理 → 活跃 → 完成（快照状态机，CSS 响应 `[data-state]`），一个侧翼按钮在回报时接受**按下**（颜色切换到成功，勾选标记盖章）。点击是高潮，而非经过的手势。

**时长**：4.0–9.3 秒（Key_Feature 4.0–7.3 秒和 Product_Intro 6.1–9.3 秒的并集）

**镜头结构**（一个 `[product UI surface]` — 固定应用窗口、仪表板/编辑器、视差 `[content card]` 堆栈、或 `[container object/icon]` — 居中在 `[bg color/gradient]` 上，显示为 `[flat]` 或 `[3D-isometric]`；一个自定义 `[brand-colored cursor with icon]` 是主角，摄像机伺服到它触碰的任何东西；UI **实时**响应并与每个光标动作同步。两个角色调整的节奏折叠其中 — Product_Intro **扫过以介绍**，Key_Feature **执行工作流**。）

- **场景 1（0.0–~Xs）——表面建立 + 首次触碰。** `[product UI surface]` 居中到达在 `[bg color/gradient]` 上 — 要么它简单存在（固定窗口/仪表板/编辑器），一个 3D 视差 `[content cards]` 堆栈，或一个 `[container object/icon]` 以 3D 翻滚**飞入**并稳定。自定义 `[cursor]` 进入。光标在 `[cursor target 1]` 上执行**第一个**动作，UI 在同一节拍中实时响应。摄像机保持或开始向被操作区域缓慢推进。
  - _变体 — Product_Intro_：低承诺首次触碰 — 光标**悬停**/扫过一个控件或**扫过高亮**一个字段到 `[accent color]`，或 `[container]` 扇开。一个可选标签/标题淡入/变形到表面上。关键是**显示表面存在**且可触摸。
  - _变体 — Key_Feature_：一个具体编辑 — 光标**拖拽**滚动条 / **输入**到字段 / **拖拽**手柄，UI 实质响应（`[scroll]` / 值攀升 / 区域调整大小）。如果表面以 `[3D-isometric]` 打开，它可能在此快照透视**展平**以读取工作流。

- **场景 2（~Xs–~Ys）——摄像机追逐到下一个交互（引擎）。** 摄像机**移动**到下一个目标 — 推进 + 平移 / 甩切 / 下移到 `[cursor target k]` — 光标执行动作 k，UI 实时更新。每个节拍是一个离散交互，由快速摄像机移动连接；表面的内部内容每次交互**交换**。
  - _变体 — Product_Intro_：导航是探索性的 — 跨视差 `[content card]` 堆栈的缓慢摄像机平移 + 景深**焦距拉动**，或 `[container]` 扇成 `[N option/content cards]` 弹簧到位置。内容交换时，支持背景**步进**其颜色（`[bg step 1]` → step 2 → …）。通常一或两个这样的移动。
  - _变体 — Key_Feature_：对 `[2–4 节拍总计]` 重复，每个是 UI 响应的不同操作 — 计数器**计数递增**，`[pill/swatch]` **选择**，一个模态**滑入**并**输入** — 由甩切/渐进缩放连接。工作流明显向结果前进。

- **场景 3（~Ys–结束）——回报状态，摄像机稳定，**保持**。光标落在其最终目标上，屏幕达到回报状态；摄像机静止并保持。
  - _变体 — Product_Intro_：光标**悬停**主角元素 — 一个 `[content card]` 在悬停时**放大**，一个节点获得一个 `[Available]` 风格胶囊，或一个 `[result card]` **弹出**/弹簧进入 — "这就是产品"的回报。稳定静态，保持。
  - _变体 — Key_Feature_：锁定特写结果上 — 光标落在 `[primary action button: Export / Save / Reimburse]` 上，一个 `[hover backdrop / highlight]` **弹簧弹出**（高潮是操作按钮/产生的结果）。保持。

**动词语汇**：光标驱动点击/悬停/扫过高亮/拖拽/输入；每次交互实时 UI 响应（滚动、值攀升、区域调整大小、内容交换）；摄像机推进 + 平移/甩切/下移伺服到每个目标；坐标缩放到被操作区域；按下并涟漪在被点击控件上；按钮按下压缩；屏幕状态逐镜头交换；卡片扇出到角落（弹簧）；3D 容器飞入和翻滚稳定；透视展平（3D→2D 快照）；分页/步进背景颜色前进；跨视差卡片堆栈的景深焦距拉动；计数器计数递增；胶囊/色样选择；模态滑入 + 打字；状态之间标签/标题变形；UI 关键词高亮辉光；终端悬停缩放或结果卡片弹出；最终操作按钮上的弹簧悬停背景。

**规则映射**

- 视口跟随光标 / 摄像机伺服到其触碰的任何东西（主要）→ `camera-cursor-tracking`
- 光标移动到目标、按下、发出涟漪（点击本身 — 主要交互原语）→ `cursor-click-ripple`
- 状态之间屏幕交换逐镜头（表面内部内容在节拍之间变化）→ `scale-swap-transition`
- 摄像机推进 + 平移/甩切/下移到下一个目标 → `viewport-change`（跨 UI 的平移/缩放）
- 将追逐排序为离散交互节拍 → `multi-phase-camera`
- 缩放到特定的被操作 UI 区域 → `coordinate-target-zoom`
- 光标图标/状态随上下文变化（例如在可拖拽手柄上指针↔抓取）→ `context-sensitive-cursor`
- 每节拍哪些内容出现 / 逐步 UI 状态推进 / 每次交互交换 → `dynamic-content-sequencing`
- 扫过高亮字段，高亮 UI 关键词到 `[accent color]` → `asr-keyword-glow`（触碰元素上的关键词辉光）
- 点击按钮在按下时压缩，释放时弹回 → `press-release-spring`
- 在更重按下时光标 + 按钮一起压缩 → `physics-press-reaction`
- 面板/卡片在两个状态之间变形（例如卡片 → 展开卡片，表面状态 A → B）→ `card-morph-anchor`
- 终端悬停缩放、`[result card]` 弹出、最终操作按钮上的弹簧悬停背景 → `spring-pop-entrance`
- 卡片扇出到角落 / 选项卡片弹簧到位置 → `split-tilt-cards`（扇出/展开到倾斜位置）+ `spring-pop-entrance`（弹簧稳定）
- 作为表面的 3D 视差内容卡片堆栈；UI 显示为 3D 等角 → `3d-page-scroll`（UI 作为倾斜滚动/视差卡片）
- 节点获得 `[Available]` 风格胶囊 / 元素上出现跟踪徽章 → `ai-tracking-box`
- UI 响应的计数器/值计数递增 → `counting-dynamic-scale`
- 作为工作流结果的结果条/数字**填充** → `stat-bars-and-fills`
- 用作表面的实时 `[video]` 屏幕捕获剪辑 → 技术：视频合成
- 透视展平（3D 等角 → 平面 2D 快照）和 3D 等角倾斜本身 → 技术：CSS-3D（无专用规则；倾斜/展平变换是 CSS-3D 原语）
- 摄像机在回报上稳定静态并**保持** →（回报元素上 `spring-pop-entrance` 的稳定阶段；静态保持本身无需规则）
- 3D 容器/对象飞入和翻滚稳定 → `depth-scatter-assemble`（自由翻滚 3D 对象/容器进入，飞入并翻滚稳定；`orbit-3d-entry` 仅将平面元素轨道到位置）
- 跨视差卡片堆栈的景深焦距拉动 → `depth-of-field-blur`（近远卡片之间的机架对焦/景深模糊过渡；`3d-page-scroll` 提供倾斜视差堆栈，`viewport-change` 提供平移）
- 分页/步进背景颜色前进与交互同步（`[bg step 1]`→step 2→…）→ `discrete-text-sequence`（离散状态步进，此处应用于背景颜色状态而非文本）
- 模态滑入 + 模内打字作为一个组合节拍 → `card-morph-anchor` / `scale-swap-transition`（面板滑入）+ `discrete-text-sequence`（模内打字文本）

**摄像机修饰**：定义性运动是摄像机**追逐** — 视口通过 `camera-cursor-tracking`（主要）跟随光标从目标到目标，由 `viewport-change` 下的具体推进+平移/甩切/下移动作实现，由 `multi-phase-camera` 排序为离散交互节拍，每个节拍的目的地通过 `coordinate-target-zoom`（缩放到被操作区域）瞄准。Product_Intro 偏向于扫过表面的缓慢、探索性平移 + 焦距拉动；Key_Feature 偏向于更快的甩切/渐进缩放，穿过工作流行进并锁定在操作按钮上。这种摄像机伺服到光标的方式将此蓝图与无需操作的摄像机滚动（dataviz-scroll-reveal）和静态设备/窗口巡览区分开。
