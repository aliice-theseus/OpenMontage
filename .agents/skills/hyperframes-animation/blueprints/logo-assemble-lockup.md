# logo-assemble-lockup — Logo 组装 → 组合

**意图**：一个品牌标记/wordmark 由部件自建（元素组装或轨道进入、字母级联、轮廓描画、或摄像机穿过负空间推进）并解析为一个居中的 logo 组合——可选扩展为最终 URL / CTA。

**服务角色**

- Product_Intro（来自 product-intro-logo-system-assemble）：一个无言的、高级品牌**开场**——一个抽象的系统元素脉冲/生长/轨道运行并围绕一个**固定的**中心 logo 组装，由一次电影级摄像机倾斜承载；无文案，无 UI。
- CTA（来自 cta-camera-push-lockup）：logo 构建是最终请求的**引导**——一个 3D 标记组装 + wordmark 级联，然后快速摄像机**推进穿过**标记的负空间，巨大 CTA 字母飞过镜头，解析在一个 `[url]` / `[CTA verb]` 组合上。
- CTA（来自 cta-button-wordmark-build）："绘制自身轮廓 → wordmark 逐字母构建"子形态——一个 `[CTA button]` 胶囊描画其自身发光边框，一个对角带**擦除**翻转画面，`[wordmark]` 在斜线旁边输入以着陆组合。摄像机静止。
- Brand_Outro（来自 brand-outro-assemble-logo-lockup）：结束标记——一个 `[feature pills / UI elements]` 的编队从所有四边**清空**舞台，然后在空白画面上，`[logo mark]` 逐笔画绘制自身，`[wordmark]` 揭示以完成组合，然后淡出。
- Product_Intro（来自 brand-reveal-assemble-zoom）：一个上下文然后聚焦的揭示——一个配套标语**输入**以设置上下文，主角标记在其旁边弹出，然后配套退出，布局重新居中，摄像机**推进**到标记的特写保持（宽构图缩小到紧密聚焦）。

**时长**：~4.6–11.0 秒（Brand_Outro ~4.6 秒 · brand-reveal ~5 秒 · Product_Intro ~7 秒 · CTA 5.4–11.0 秒）

**镜头结构**（一个统一的时间编码模板；`[slots]` 与产品无关）

- 场景 1 — 清空 / 点燃（0.0–~1.0 秒）：舞台为标记构建做好准备。
  - _变体 — Product_Intro_：在干净的 `[light bg]` 上打开，带有微弱的同心引导环，在平坦俯视图下；环**脉冲**并从中心扩展；节拍中途背景交叉淡入 `[light]→[dark gradient: hero→secondary]`，微小种子点沿环出现，中心 `[logo mark]` 的辉光**点燃**（标记从 t=0 就存在，固定，正面朝向）。
  - _变体 — CTA push_：在 `[bg gradient]` 上，`[logo mark]` 在对象空间中稳定（一个 3D 标记，带细线框边缘引导 + 中心背后的微弱括号主题）；非常缓慢的连续摄像机推进可能已经在爬行。
  - _变体 — CTA button-build_：在 `[dark grid bg]` 上，一个圆角 `[CTA button "label"]` 胶囊上升/缩放到中心（之前的标题从顶部清空）；其细边框作为动画发光轮廓**描画**绘制，左侧边缘有一个小 `[accent]` 彗星/火花图标。
  - _变体 — Brand_Outro_：一个预排列的 `[feature pills / element grid]` 编队（每个 `[icon]`+`[label]`）**散开**——元素从其布局位置向外滑动，飞出所有四个画面边缘（边缘清除漂移，非中心原点爆发），将画面清空到干净的 `[bg]` 上。

- 场景 2 — 组装标记（~1.0–~Ys）：标记由部件自建。
  - _变体 — Product_Intro_：种子点**放大**为在环上排列的平面 `[accent]` 形状；同心带向外波动（隧道感），形状开始围绕静止固定的中心**轨道运行**/漂移。
  - _变体 — CTA push_：`[wordmark]` 从标记后面**级联**出来（字母从左到右带过冲）成为完整的 `[brand lockup]`；3D 标记可以分节拍组装（一个终端分离并作为弹簧点弹出，一个部件铰链打开并弹性咬合关闭）。可选节拍：一个 `[cursor]` 弧线进入并"点击"wordmark，或一个磨砂玻璃胶囊持有中间 `[CTA line]` 弹簧进入，同时分层标记壳扇向边缘。
  - _变体 — CTA button-build_：一个图形**擦除**将画面翻转到 `[contrast bg]`——一条细 `[accent]` 对角线扫入，膨胀为全画面对角**带**，然后塌缩为一个小 `[accent]` 斜线。
  - _变体 — Brand_Outro_：在现在干净的画面上，`[logo mark]` 通过描画**绘制**（逐弧/逐段构建）。

- 场景 3 — 解析为组合（~Ys–结束）：组合完成并保持（Product_Intro / Brand_Outro）或飞入/扩展到 CTA（CTA 变体）。
  - _变体 — Product_Intro（**那一个**摄像机动作）_：整个系统从平坦俯视图平滑**倾斜**到倾斜的等角透视（缓入缓出），略微缩小——平面形状变为发光 3D 形态，带变为发光轨道线，而中心 `[logo mark]` 不倾斜（保持 2D，正面朝向，固定）。摄像机缓停；元素保持连续轨道/漂移（内部比外部快）；标记保持稳定辉光。最终稳定画面。
  - _变体 — CTA push（标志性动作）_：一次快速摄像机**推进穿过**标记的负空间/穿过玻璃胶囊——重水平运动模糊，巨大 `[CTA]` 字母划过镜头（光标退出）。解析为饱和 `[bg]` 上的最终组合：一个 `[url badge]` / `[CTA line]` 由左→右**擦除**揭示，带有 `[accent]` 前导边缘（或干净淡入），实体标记形状在背后视差滑入。稳定到完全静止保持（缓慢缩小/稳定）。
  - _变体 — CTA button-build_：`[wordmark]` 在斜线右侧**逐字母构建**，着陆在新背景上的最终 "`[slash] [WORDMARK]`" 组合。缓慢稳定到静止。
  - _变体 — Brand_Outro_：`[wordmark]` 在绘制的标记旁边揭示（滑动/淡入）以完成 `[lockup]`；组合保持，然后淡出到 `[black / bg]`。

**动词语汇**：环脉冲/扩展；背景交叉淡入（亮→暗）；辉光点燃；种子点放大；连续轨道/漂移（内部比外部快）；单次 3D 透视倾斜（平坦→等角）+ 围绕固定 2D 锚点的略微缩小；3D logo 组装（部件分离 + 弹簧点，铰链打开/咬合，壳扇出）；wordmark 级联带过冲（字母从左到右）；按钮胶囊上升/缩放进入；动画描画轮廓**绘制** + 辉光（按钮边框和 logo 标记）；彗星/火花重音；对角带擦除（扫过 → 膨胀 → 塌缩为斜线）；逐字母 wordmark 构建；预成型网格从所有四边**散开**；logo 标记描画绘制（顺序弧/段）；快速摄像机**推进穿过**带运动模糊（CTA 脊线）；连续缓慢推进/拉出；光标弧线进入 + 点击；视差形状滑入；左→右 URL/徽章擦除带发光前导边缘；静态/淡出结束组合保持；可选标记上的空闲呼吸。

**规则映射**（每个动作动词 → `rules/<id>.md`）

- 环脉冲/从中心扩展 → `center-outward-expansion`（从共享中心辐射；复用 0→1 进度驱动）
- 背景交叉淡入（亮→暗渐变）→ 通过 `gsap-effects` 的普通不透明度/背景补间（无需专用规则）
- 标记上的辉光点燃 → `asr-keyword-glow`（品牌元素上的包络驱动辉光）
- 种子点放大为形状 → `spring-pop-entrance`（缩放弹出；如果点变形为形状则备选 `scale-swap-transition`）
- 围绕固定中心的连续轨道/漂移 → `orbit-3d-entry`（翻转入场然后连续椭圆轨道；中心标签 = 固定标记）
- 单次 3D 透视倾斜（平坦→等角）+ 略微缩小 → `multi-phase-camera`（场景包裹摄像机的脚本化缩放阶段，用于缩小）— 参见摄像机修饰；整个舞台的平坦→等角平面倾斜是一个 CSS-3D 透视动作（`techniques.md` CSS-3D，动画化舞台的 `rotateX`）— 没有确切的摄像机规则用于平面倾斜，近似通过 CSS-3D（最接近参考是 `orbit-3d-entry` 的"倾斜轨道平面"变体随时间动画化）
- 移动宇宙中的固定 2D 锚点 logo → 无需动效规则（静态锚点；有意为之——这是没有运动，宇宙围绕它移动）
- 3D logo 组装 — 部件分离 + 弹簧点 → `spring-pop-entrance`（弹簧弹出，`back.out` 过冲）
- 3D logo 组装 — 铰链打开/关闭（铰链板）→ `hacker-flip-3d`（3D 旋转轴）+ `techniques.md` CSS-3D（弹性打开和咬合关闭铰链是 3D 旋转的改编）
- 3D logo 组装 — 壳扇出到边缘 → `center-outward-expansion`（从标记中心向外运行）
- wordmark 级联带过冲（字母从左到右）→ 配方 `gsap-effects`（逐元素错开滑动）+ `spring-pop-entrance`（每个字母的 `back.out` 过冲）
- 按钮胶囊上升/缩放进入 → `spring-pop-entrance`（缩放进入；备选 `scale-swap-transition`）
- 动画描画轮廓绘制 + 辉光（按钮边框）→ `svg-path-draw`（stroke-dashoffset 绘制）+ `asr-keyword-glow`（绘制描画上的辉光）
- 按钮上的彗星/火花重音 → `asr-keyword-glow`（小辉光重音）；通过 `techniques.md` GSAP MotionPathPlugin 的运动路径（#9）
- 对角带擦除（扫过 → 膨胀 → 塌缩为斜线）→ `techniques.md` clip-path 揭示（#12，动画化画面上的对角线 `polygon(...)`；膨胀然后塌缩为斜线是通过增长→缩小关键帧驱动的相同 clip-path 揭示）
- 逐字母 wordmark 构建 → `discrete-text-sequence`（平滑切片/逐状态构建）；配方 `gsap-effects`（打字机/追加单词）
- 预成型网格从所有四边散开 → 不是规则缺口：飞出画面的编队是**退出**，且管线禁止视频中途退出——过渡线束就是退出（只有最终画面可以退出舞台）。将其视为过渡处理/仅最终画面而非场景内动效规则。（如果作为揭示标记的清除在场景内上演，它重用运行**向外**的 `center-outward-expansion`——中心→目标机制插值编队→屏幕外目标，出缓动。）
- logo 标记描画绘制（顺序弧/段）→ `svg-path-draw`（规范的多段错开绘制）
- wordmark 滑动/淡入在绘制的标记旁边揭示 → `svg-path-draw`（其"品牌线在描画后淡入"尾部）；通过 `spring-pop-entrance` 滑动
- 快速摄像机推进穿过带运动模糊 → `multi-phase-camera`（一个硬推进阶段）— 参见摄像机修饰；重运动模糊条纹本身 → `motion-blur-streak`（快速推进穿过上的方向速度模糊）
- 连续缓慢推进/拉出 → `multi-phase-camera`（阶段缩放 + 漂移）
- 光标弧线进入 + 点击 wordmark → `cursor-click-ripple`（移动 → 点击 → 涟漪）；通过 `techniques.md` MotionPathPlugin 的弧线路径（#9）
- 组合背后视差形状滑入 → `depth-scatter-assemble`（不同深度的形状的视差深度滑入；与 `3d-text-depth-layers` 配合用于深度排序）
- 左→右 URL/徽章擦除带发光前导边缘 → `techniques.md` clip-path 揭示（#12，动画化 `inset()` 从左到右）；发光前导边缘 → `asr-keyword-glow`
- 静态/淡出结束组合保持 → 无需动效规则（终端保持/不透明度淡出；有意为之）
- 保持标记上的空闲呼吸（可选）→ `sine-wave-loop`（稳定后呼吸）

**摄像机修饰**（推进/倾斜）

- **CTA 推进穿过**（CTA 脊线）：场景包裹摄像机上的脚本化硬缩放阶段 → `multi-phase-camera`（"稳定推进"/"书挡拉出"模式；推进阶段 = 高潮）。当标记**偏离中心**且摄像机必须飞过特定负空间点时，与 `coordinate-target-zoom` 组合（外部缩放，内部反向平移，使目标负空间点在缩放增加时落在视口中心；在设置时测量偏移）。标志性重水平**运动模糊**在条纹上 → `motion-blur-streak`（推进上的方向速度模糊）；在推进窗口期间通过摄像机上的 CSS `filter: blur()` / 复制条纹层实现。
- **Product_Intro 倾斜**（那一个电影级动作）：平坦→等角透视倾斜 + 略微缩小是单个脚本化摄像机节拍 → `multi-phase-camera`（用于缩小的缩放阶段 + "针对偏离中心元素的目标缩放"/漂移机制）。`multi-phase-camera` 仅为缩放+平移+漂移，因此整个舞台的透视平面 rotateX（平坦俯视图 → 倾斜等角）是上面提到的 CSS-3D 动作——近似通过 `techniques.md` CSS-3D，动画化舞台的 `rotateX`（最接近参考是 `orbit-3d-entry` 的"倾斜轨道平面"变体随时间动画化）。
