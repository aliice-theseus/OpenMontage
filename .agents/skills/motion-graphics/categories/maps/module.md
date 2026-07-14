# maps — 类别模块

地理动态：高亮区域、连接地点、缩放到某位置。**第一个决策：镜头是否需要真实底图**（卫星/街道/地形图像、地球仪或缩放到真实地址）？这决定了轨道。

## 规划（Director）

首先设置 `content.lane`：

- **矢量**（默认）— 风格化区域形状，无真实图像。在 HF 中原生且实时运行，成本低。`asset_needs: []`。
- **底图** — 需要真实卫星/暗色瓦片、地球仪或缩放到真实地点。`asset_needs: [{ type: "map-bake", … }]`。**在素材来源阶段烘焙图像**：HF 禁止渲染时网络访问并需要确定性，因此实时瓦片（会重新获取且每次渲染都可能变化）不能作为图像层 — 烘焙将其冻结（额外好处是流畅）。参见底图轨道 + 确定性。

`content`：`{ lane, shot: highlight|flow|choropleth|labels|flag|pin-rollout|zoom-to, regions[], points[], basemap: satellite|dark, palette, headline, overlays: [label|pin|callout-card] }`。

`overlays` 与 `shot` 无关，在两个轨道中都有效。**`callout-card`** = 一个固定卡片（标志芯片 + 统计数字 + 进度条）— 即"纪录片弹窗"（热门第13位）；将其组合到任何缩放到/高亮镜头上，而不是作为独立镜头处理。

## 词汇表 / 依赖

**矢量轨道**（D3 + TopoJSON — 复用现有地图系列，不要重复）：

- 复用：`us-map`（+气泡/六边形/流向）、`world-map`、`spain-map`。
- **手动编写**这些（不在目录中 — 按以下特征构建，不要期望有 `add` 命令）：`geo-highlight`（N个国家着色 + 标签 + 边界脉冲）、`geo-flow`（世界弧线/枢纽网络）、`flag-borders`（国旗裁剪到国家）、`pin-rollout`（城市按顺序脉冲 + 计数器）。
- 特征：国家填充交错 · 图钉下落 + 脉冲环 · 弧线 `stroke-dashoffset` 绘制 + 飞行物 · 分色图颜色揭示 · **viewBox** 缩放。

**底图轨道**（MapLibre，在素材来源阶段烘焙 — 已验证的流水线、`bake-basemap.mjs`、完全环境参数化 — 适用于任何国家，不仅限于原型）：

- **烘焙** `bake-basemap.mjs`（puppeteer + MapLibre；环境驱动：`NAME STYLE COUNTRIES CENTER ZSTART ZEND PITCH BEARING FPS DUR`）：驱动摄像机 **缩放→保持**（`easeInOutCubic`）并且**在每帧前 `await map.once('idle')`** 以使每帧都有完整瓦片（Remotion `delayRender` 技术 → 无瓦片弹出）。辅助工具自己解析 Chrome，精确固定依赖，按主题派生海外领地过滤器，并在空闲超时时**大声失败**（可疑帧 → 非零退出）。_外部依赖：固定的 CDN 库（maplibre/topojson/world-atlas）+ Esri/CARTO 瓦片端点是第三方的 — 在任何版本升级时重新验证可用性和服务条款。_ `preserveDrawingBuffer:true`、`fadeDuration:0`。辅助工具然后将帧**编码为全帧内 MP4**（`ffmpeg -framerate FPS -i f%04d.png -c:v libx264 -g 1 -pix_fmt yuv420p`）并将所有内容写入 **`$OUT`（默认为 `cwd`）**，而非技能目录 → `<NAME>.mp4` + `<NAME>-coords.json`。
- **导出地理→屏幕**在保持视图：`map.project()` 每个请求的国家 → `<NAME>-coords.json` = `{ view, countries: [{ name, color, d (SVG 路径), bbox, label }] }`。摄像机在缩放后保持静态，因此这些路径保持像素对齐。`label` 是一个**近似**锚点（本土多边形的顶点平均 — 对于凹形国家按可读性微调）。消费 `coords.countries[i]`；`smooth-frde2`/`smooth-flag` 示例目录早于此辅助工具，使用扁平 `{fr,de,…}` 形状，因此适配它们的接线。
- **构建器**：轨道 0 上的 `<video>` 底图 + 一个 **SVG 覆盖层**，在保持期间动画化国家**边界（`stroke-dashoffset` 绘制）** + **填充（色块揭示）** + 标签/图钉/卡片 — 全部通过 `coords.json` 地理对齐。这复现了 Hera 的"卫星 + 动画彩色边界/标注"外观。
  - 同一投影路径也可作为 SVG **`clipPath`**：将**国旗（或任何纹理）裁剪到真实边界内**用于_边界国旗_ — 比纯色更丰富的填充，在真实地图上下文中（已验证：法国三色旗在暗色底图上，`smooth-flag`）。将特征的屏幕 **bbox** 与其路径一同导出，以便国旗条纹/纹理可以按国家尺寸缩放。
- **扩展/数据空白**（根据需要扩展 `bake-basemap.mjs` — 评估代理做过）：**地球仪介绍**（"从地球仪开始"）= MapLibre `projection:{type:'globe'}` 用于开场阶段，缓动到目标位置的墨卡托（辅助工具默认为墨卡托）。**次国家**区域（州/省）不在 world-atlas 中（仅国家）→ 使用 Natural Earth **admin-1** TopoJSON，或将质心投影为图钉（`pin-rollout`）。

## 构建（优先复用）

矢量：`npx hyperframes add <block>` → 原地编辑区域/数据/调色板。底图：烘焙的 `map.mp4` 作为轨道-0 `<video>`，将覆盖层绑定到锚点。

**克制（不要俗气 — 这是自动构建地图出错的第1号原因）：** 每个动画元素必须服务于信息 — 区域、连接器、标签、图钉、摄像机。**无装饰性环境辉光、背景光斑、浮动粒子、镜头光晕或多余的泛光。** 动画 = 持续的摄像机运动（viewBox 推进/缩放）+ 有目的的重叠元素揭示 — 不是灯光秀。调色板：颜色必须**承载意义** — 数据刻度（分色图）、区分区域的分类型填充（政治地图）、或1–2个强调色用于主体（高亮国家/路径）在其余中性背景上。不要为了**装饰**而添加颜色（国家为对比而设为琥珀色、为"能量"而设辉光）。画面应像干净的广播地图，而不是屏保。

**可读性（硬性规则）：** 将标签从高亮形状和彼此之间偏移；钳制到安全区域；标注药丸不得放置在另一个标签或边界上（评估曾出现 DE/PL "奥得–尼斯"药丸重叠 POLAND 标签的情况）。关键元素保持可读至少约0.3秒。

**署名（硬性规则）：** 真实底图图像带有使用条款 — 每当底图显示在屏幕上时，将信用元素烘焙到合成中（Esri 卫星 → "Esri, Maxar, Earthstar Geographics"；CARTO → "© CARTO, © OpenStreetMap"）。小角落标签（参见 `smooth-jp`）。对于任何发布内容，不可协商。

**确定性（硬性规则 — 每个都在原型中给我们带来过麻烦）：**

- 一切由 seek 时钟驱动；**绝不用 `tl.call`** 进行有状态更新（计数器、文字）→ 代理补间 + `onUpdate`（tl.call 在 HF seek 下冻结时间线）。
- SVG 缩放 = 动画化 **viewBox**（不要手动计算组变换原点）。
- 居中的覆盖层（使用 `transform: translate(-50%,…)` 居中的卡片/标签）：仅动画化 **opacity**，或包裹在外部居中 div 中 — GSAP 动画化 `y`/`scale` 会覆盖整个 transform 并破坏居中。
- 国家几何：过滤到主体周围**经纬度框**内的多边形 — world-atlas 包含了使 bbox 爆炸的海外领地（法国 + 圭亚那）。保留附近岛屿（科西嘉、西西里），丢弃远距离岛屿。（`bake-basemap.mjs` 锚定在顶点最丰富的多边形 ± `KEEPMARGIN` — 无大洲特定常量。）
- **瓦片世界比例**：MapLibre 的内部世界宽度为 `512·2^zoom`，无论栅格 `tileSize` 如何。Esri/CARTO 栅格 → `tileSize:256`（正确）；512px/@2x/retina/矢量源需要 `tileSize:512`，否则每个缩放级别都会偏移一（这曾静默地使一次烘焙过度缩放 — 法国从顶部到底部溢出画面）。
- **反子午线**：跨越 ±180° 的特征（俄罗斯、斐济、新西兰）在逐顶点 `map.project()` 下会涂抹。`bake-basemap.mjs` 在投影前**将经度展开到以摄像机中心为参考**，这处理了此问题；它仍然在特征即使展开后仍跨越 >180° 时发出警告。
- **流畅度 = 每帧完整瓦片 + 缓动摄像机。** 在烘焙中，每帧截图前 `await map.once('idle')`（= Remotion `delayRender`）并使用 `easeInOutCubic` 缓动摄像机（= 插值+Easing）。`preserveDrawingBuffer:true`、`fadeDuration:0`、大 `maxTileCacheSize`。
- **覆盖层对齐**：在**保持**的摄像机下投影特征边界，并且仅在保持期间动画化覆盖层 — 移动的摄像机会导致固定的投影路径漂移分离。
- **保持前隐藏状态**：在_保持_时揭示的覆盖层必须在构建时 `gsap.set` 为其隐藏状态（`scaleX:0`、完整 `stroke-dashoffset`、`opacity:0`）— 裸 `fromTo` **不会**在补间开始前应用其"从"状态，因此元素在缩放期间会以其自然（可见、错位）状态显示。
- **为什么一定要烘焙**（真正的原因 — 不仅仅是流畅度）：烘焙将图像冻结为**确定性**像素。实时栅格瓦片每次渲染都会重新获取且可能变化，且渲染时网络被禁止。MapLibre _确实_可以在 HF 中实时渲染（只是不稳定：瓦片弹出、深度缩放超出加载速度）；暴露引擎的每帧 `onBeforeCapture` 钩子（它存在 — `frameCapture.ts:~1250`）会使实时渲染**流畅** — 但**不会**消除为**确定性和离线可复现性**冻结瓦片的需求。因此 `onBeforeCapture` 将取代烘焙的_流畅度_角色，而不是_冻结_角色。

## 范围外

3D 逼真地标（Cesium 领域）· 每个国家/每个模板的块（应参数化）· 图表（→ `charts`）。（引擎内_实时_ MapLibre 是可能的但今天不稳定 — 改为烘焙；如果引擎获得每帧就绪钩子则重新评估。）

## 注册

`director.md` 分类行（轨道分支）+ `catalog-map.md` `maps/geo` 行（添加底图轨道）。阶段流水线不变。
