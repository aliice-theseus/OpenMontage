---
version: alpha
name: Coral — Frame (video / frame layer)
description: >
  Coral 的 design.md 的视频优先伴侣。单位是帧 (1920×1080)，不是
  幻灯片中的一页。原子相同且神圣 — 三表面系统（珊瑚火 /
  墨黑 / 暖奶油）、Bebas Neue 大写追踪 + Inter 正文、45° 对角线阴影、
  装饰性壁纸数字、硬颜色区域分割、零阴影、零圆角（除
  圆形外）。构图、帧比例和宽高比行为已为帧重写。
  运动不在此范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  coral: "#E85D5D"
  coral-dark: "#D44A4A"
  cream: "#F5F0E8"
  cream-dark: "#E8E0D4"
  black: "#1A1A1A"
  gray: "#6B6B6B"
  light-gray: "#B0B0B0"
  white: "#FFFFFF"

typography:
  # — reading ramp (Inter) —
  body:          { fontFamily: "Inter", cqw: 1.0,  weight: 400, lineHeight: 1.7 }
  body-light:    { fontFamily: "Inter", cqw: 1.5,  weight: 300, lineHeight: 1.5, note: "pull-quote voice" }
  section-label: { fontFamily: "Inter", px: 12, weight: 700, tracking: "4px", upper: true }
  item-label:    { fontFamily: "Inter", px: 11, weight: 700, tracking: "3px", upper: true }
  quote-attribution: { fontFamily: "Inter", px: 14, weight: 600, tracking: "3px", upper: true }
  quote-role:    { fontFamily: "Inter", px: 12, weight: 400, tracking: "1px" }
  # — display / hero ramp (Bebas Neue, uppercase, tracked) —
  card-title:    { fontFamily: "Bebas Neue", cqw: 1.9, weight: 400, lineHeight: 1.1, tracking: "1px", upper: true }
  sidebar-value: { fontFamily: "Bebas Neue", cqw: 2.3, weight: 400, lineHeight: 1.0, upper: true }
  bar-title:     { fontFamily: "Bebas Neue", cqw: 2.3, weight: 400, lineHeight: 1.0, tracking: "2px", upper: true }
  card-stat:     { fontFamily: "Bebas Neue", cqw: 2.5, weight: 400, lineHeight: 1.0, upper: true }
  column-title:  { fontFamily: "Bebas Neue", cqw: 3.7, weight: 400, lineHeight: 1.0, tracking: "2px", upper: true }
  section-headline:{ fontFamily: "Bebas Neue", cqw: 4.2, weight: 400, lineHeight: 1.0, tracking: "2px", upper: true }
  stat-numeral:  { fontFamily: "Bebas Neue", cqw: 5.0, weight: 400, lineHeight: 1.0, upper: true }
  hero-title:    { fontFamily: "Bebas Neue", cqw: 6.5, weight: 400, lineHeight: 0.9, tracking: "4px", upper: true }
  jumbo-feature: { fontFamily: "Bebas Neue", cqw: 9.0, weight: 400, lineHeight: 1.0, tracking: "12px", upper: true }
  # — decorative —
  background-numeral: { fontFamily: "Bebas Neue", cqw: 10.0, weight: 400, color: "rgba(0,0,0,0.12)", note: "wallpaper numeral inside a coral region" }
  giant-mark:    { fontFamily: "Bebas Neue", cqw: 14.0, weight: 400, color: "rgba(0,0,0,0.35)", note: "decorative quote mark inside a coral region" }

spacing:
  pad-x: "5cqw"       # standard horizontal frame padding
  pad-y: "4cqw"
  pad-col: "3cqw"
  gap-grid: "1.7cqw"
  card-pad: "2cqw"

components:
  diagonal-hatch:
    backgroundImage: "repeating-linear-gradient(45deg, transparent 0 20px, rgba(0,0,0,.06) 20px 40px)"
    placement: "::before overlay on {colors.coral} regions"
    description: "Signature 45° hatch (6% ink). Variants −45° 30/60px, 90° vertical 60/62px 10% ink. Texture, never depth."
  region-split:
    layout: "two/three solid surfaces meeting at a hard edge; ratios 38/62 rows, 40/60 cols, 50/50"
    rounded: "0"
    description: "The primary layout device — no gradient, no rounded junction; the boundary is the layout."
  card:
    backgroundColor: "{colors.white}"
    borderTop: "0.26cqw solid {colors.coral}"
    rounded: "0"
    shadow: "none"
    typography: "{typography.card-title} + {typography.body}"
    description: "5px coral TOP border is the only chrome; holds a card-icon, title, body, coral card-stat."
  sidebar-item:
    backgroundColor: "{colors.white}"
    borderLeft: "0.2cqw solid {colors.coral}"
    rounded: "0"
    typography: "{typography.sidebar-value} + {typography.section-label}"
    description: "4px coral LEFT border is the only chrome."
  card-icon:
    backgroundColor: "{colors.coral}"
    textColor: "{colors.white}"
    size: "2.5cqw square"
    rounded: "0"
    description: "The card mark — one white Bebas glyph centered."
  accent-line:
    backgroundColor: "{colors.coral}"
    size: "4cqw × 0.25cqw (60×4 closing variant)"
    rounded: "0"
    description: "Sub-headline accent rule."
  background-numeral:
    typography: "{typography.background-numeral}"
    color: "rgba(0,0,0,0.12)"
    placement: "behind a {colors.coral} region's title"
    description: "The wallpaper-numeral signature (12% ink)."
  giant-mark:
    typography: "{typography.giant-mark}"
    color: "rgba(0,0,0,0.35)"
    placement: "inside a {colors.coral} region"
    description: "Oversized quote mark / character, half-decorative."
  timeline:
    line: "0.2cqw solid {colors.black} (gradient-dashed ::after)"
    node: "{colors.coral} circle, {colors.cream} halo, 50% radius"
    description: "Ink line with coral nodes + cream halos."
  info-bar:
    backgroundColor: "{colors.cream-dark}"
    typography: "{typography.bar-title} + uppercase {typography.section-label}"
    rounded: "0"
    shadow: "none"
    description: "Footer band beneath a feature region — Bebas title left, Inter meta right."
---

# Coral — 帧（视频 / 帧层）

## 概述

帧尺度下的 Coral 是一个**大胆的杂志海报**，由三个实色表面构建 — 珊瑚火、墨黑、暖奶油 — 在**硬颜色边缘**交汇。区域边界就是布局：帧分割为珊瑚平面 + 奶油平面，或珊瑚面板 + 墨水面板，每个容纳一个独立构图。无渐变过渡、无圆角连接、无投影。

语气是一个双面层级：**Bebas Neue**（高窄大写字母，始终大写，始终带字距 1–12px）承载每个标题、统计数字、标题和元数据图形；**Inter**（字重 300–700）承载每行正文、标签和署名。Bebas 宣告；Inter 解释。标志性的氛围是珊瑚区域上的 **45° 对角线阴影**（6% 墨水）和区域标题背后的 **超大壁纸数字**（12% 墨水）。

**帧尺度的关键特征：**

- **三表面，硬边缘** — `{colors.coral}` / `{colors.black}` / `{colors.cream}` 作为实色区域。
- **Bebas 大写 + 字距** 在每个展示元素上；**Inter** 在每个正文/标签上。
- **45° 阴影**（6% 墨水）在珊瑚区域；**壁纸数字**（12%）和**巨型标记**（35%）在内容背后。
- **墨上火** — 珊瑚上的 Bebas 始终用墨水色，从不白色。眉标在奶油/墨水上为珊瑚色，在珊瑚上为墨水色。
- **扁平** — 无阴影，无层级；仅圆形有圆角（导航点、时间线节点）。
- **珊瑚既是强调色也是环境色** — 4–5px 珊瑚边框、48px 珊瑚图标方块和完整珊瑚区域。

### 帧工艺条

三项目测检查在任何结构检查前把关每帧：

- **眯眼测试** — 一个元素以 **3–6 倍于最近邻元素**占主导：`hero-title`/`jumbo-feature` 或区域标题后的壁纸数字，绝不允许两个竞争的标题。
- **留白测试** — 珊瑚/奶油/墨水区域呈现 **40–55% 空白**；**三列目录是唯一密集的例外**。填充不足的珊瑚区域应添加壁纸数字，而非更多内容。
- **克制测试** — 珊瑚作为**每帧要么是强调色要么是一个完整区域**（不可同时全强度使用）；每段引用一个巨型标记；墨上火（珊瑚上从不白色）。
- **参照测试** — 瞄准**体育杂志封面 / Saul Bass 旅行海报**（硬边缘上的实色平面，紧凑大写字母作为架构）；失败看起来像**柔和的投影卡片组**。

## 帧

- **主尺寸：** 1920×1080 (16:9)。展示尺寸以 **`cqw`** 为单位编写（`px ÷ 1920 × 100 = cqw`）。
- **竖版：** 1080×1920 (9:16)。**方版：** 1080×1080 (1:1)。
- **安全区域：** `5cqw`（pad-x）标准帧内边距；区域边缘可全幅出血。

**容器法则（承重规则）。** 每个帧容器设置 `container-type: size`；所有帧相对单位都是以它为基准的 `cqw`/`cqh` — **绝不用 `vw`**。使用 `vw` 尺寸的帧在非全屏渲染时会膨胀；`cqw` 在任何渲染尺寸下都相对于帧解析。

## 颜色

色值令牌与源文件一致。在帧尺度下，三个表面根据构图混合使用 — 珊瑚/奶油、珊瑚/墨水、墨水/奶油或单表面。`{colors.coral}` 既作强调色（边框、图标方块、时间线节点、奶油/墨水上的眉标）也作环境色（完整区域）。标题：奶油/珊瑚上墨水色，墨水上奶油色 — **绝不用灰色，绝不用白字在珊瑚上。** 眉标：奶油/墨水上珊瑚色，珊瑚上墨水色 — 不存在珊瑚上珊瑚。唯一允许的渐变是罕见的 135° 珊瑚深→珊瑚特色区域；其他一切均为纯色。

## 排版

两个阶梯。**阅读阶梯**（Inter 正文 1.0cqw，正文浅色 1.5cqw，标签以 px 为单位）承载文案和眉标；**展示/英雄阶梯**（Bebas，`card-title` 1.9cqw 到 `jumbo-feature` 9.0cqw，加上装饰性的 `background-numeral` 10cqw 和 `giant-mark` 14cqw）承载所有标题和统计数据。

- **可读性底线：** 任何承重行 ≥ **1.4cqw**；px 标签仅为铬色装饰。
- **按篇幅调整：** 根据标题的行长调整字号。将标题块限制在 **≤ 78cqw**；≤3 词 → `hero-title`/`jumbo-feature`；4–6 → `section-headline`；7+ → `column-title`。
- **每个 Bebas 元素均为大写且字距 ≥1px**（标准 2px，英雄 4px，超大 12px）。**每个 Inter 标签均为大写，字距 1–4px。** 无斜体、无下划线、无句首大写的 Bebas。

## 深度与表面

扁平，带有硬色边缘。深度信号仅：

- **硬区域边界** — 主要结构手段。
- **强调边框** — 5px 珊瑚顶部（卡片）、4px 珊瑚左侧（侧边栏磁贴）、4px 墨水色（时间线）。
- **45° 阴影** — 珊瑚区域上的 6% 墨水纹理（不产生深度感）。
- **壁纸排版** — 12% 的数字、35% 的巨型标记，分层在内容背后。

**天花板规则：** 无盒阴影、无抬升卡片、无柔和渐变（除了一处 135° 珊瑚特色）、无圆角矩形。

## 形状

- 每个矩形 **0 圆角** — 区域、卡片、侧边栏磁贴、图标方块、信息栏、强调线。
- 仅圆形 **50%** — 导航点（10px）、导航箭头（44px）、时间线节点（20px）。

## 组件

- **region-split** — 布局手段；表面在硬边缘处交汇。
- **card**（5px 珊瑚顶部）/ **sidebar-item**（4px 珊瑚左侧）/ **card-icon**（48px 珊瑚方块）— 每个元素上唯一的铬色装饰就是其单一的珊瑚边框。
- **diagonal-hatch** / **background-numeral** / **giant-mark** — 珊瑚区域上的氛围加壁纸签名元素。
- **accent-line** — 珊瑚色副标题线。**timeline** — 墨水色线、珊瑚节点、奶油色光晕。**info-bar** — 深奶油色底部栏。

## 帧处理方案

> 每块板的配方：背景 · 容器 · 组成 · 焦点 · 铬色 · 强调 · 留白 · 固定/自由 · 密度
> 在动势允许时偏向居中；变化锚点；每区域一个想法。

### 1 · 区域分割封面（标识 · 动势：硬区域边缘 · 左对齐）

**背景** 38/62 分割 — `{colors.coral}` 顶部带（阴影 + 壁纸数字）在 `{colors.cream}` 之上。**容器** 网格行；品牌 + 元数据在珊瑚带中，英雄标题在奶油区域中。**组成** region-split、diagonal-hatch、background-numeral、hero-title。**焦点** 墨水色的两行 `hero-title`，第二行为 `{colors.coral}`，左对齐锚定在奶油区域中。**铬色** 珊瑚带左侧的 Bebas 品牌 — 右侧的 Bebas 元数据。**强调** 珊瑚带 + 珊瑚第二行。**留白** 奶油区域约 45% 空白。**固定** 带中墨水上火、珊瑚上阴影、硬边缘。**自由** 标题文案、哪行是珊瑚色、元数据。**密度** 稀疏。

### 2 · 特色统计（锚点 · 动势：比例 · 珊瑚环境 · 左对齐）

**背景** 全 `{colors.coral}` 带阴影。**组成** diagonal-hatch、background-numeral、section-label、stat headline、body-light。**焦点** 墨水色的 `stat-numeral`/`jumbo-feature` 数字或两行标题，背后有 `background-numeral`（12% 墨水）作为壁纸。**铬色** 墨水色的 `section-label` 眉标；可选 Inter-300 支撑行 ≤44cqw。**强调** 珊瑚背景本身就是环境色；墨水色字体，无白色。**留白** 珊瑚区域约 40% 空白。**固定** 墨水色在珊瑚上、有阴影、背后有壁纸数字。**自由** 数字、标题、支撑文案。**密度** 稀疏。

### 3 · 引用布局（引用 · 动势：面板分割 · 巨型标记）

**背景** 40/60 分割 — `{colors.coral}` 左侧面板（阴影 + giant-mark）+ `{colors.black}` 右侧面板。**组成** region-split、giant-mark、body-light、accent-line、quote-attribution。**焦点** 墨水面板上的 `{colors.cream}` Inter **字重 300** 的 2–3 行拉引文。**铬色** 珊瑚面板上的 `giant-mark`（35% 墨水）；署名上方的 `60×4` 珊瑚强调线。**强调** 珊瑚面板 + 珊瑚强调线。**留白** 珊瑚面板大部分是标记。**固定** Inter-300 引用、墨水面板、珊瑚上墨水标记。**自由** 引用、署名、标记字形。**密度** 稀疏。

### 4 · 结束板（收尾 · 动势：奶油区域 + 珊瑚带 · 居中）

**背景** `{colors.cream}` 区域，底部有 `{colors.coral}` 带（阴影）。**组成** section-label、section-headline/hero-title、accent-line、info-bar。**焦点** 墨水色的两行结尾语，居中，下方有一条珊瑚 `accent-line`。**铬色** 上方的墨水色眉标；珊瑚带底部栏承载 Bebas 结尾语 + 年份。**强调** 珊瑚带 + 珊瑚强调线。**留白** 约 55% 空白奶油。**固定** 居中、墨水色字体、一条珊瑚带。**自由** 结尾语文案、带内容。**密度** 稀疏。

### 5 · 三列目录（目录 · 动势：密度 — 密集帧 · 居中标题）

**背景** `{colors.cream}`（或 `{colors.black}`），`pad-x`。**组成** section-headline、3× card。**焦点** 三个白色 `card` 上方居中的 `section-headline`（5px 珊瑚顶部、48px 图标方块、Bebas 标题、Inter 正文、珊瑚统计）。**强调** 三个珊瑚顶部边框 + 图标方块。**留白** 紧凑 — 密度例外。**固定** 5px 珊瑚顶部为唯一铬色，无阴影/圆角。**自由** 三张卡片的内容。**密度** 密集例外。

### 6 · 时间线（流程 · 动势：水平轨道 · 左对齐）

**背景** `{colors.cream}`，`pad-x`。**组成** section-headline、timeline。**焦点** 墨水色时间线，带有 4–5 个珊瑚节点（奶油色光晕）和 Bebas 标签。**强调** 珊瑚节点。**留白** 适中。**固定** 墨水色线、珊瑚节点、奶油色光晕。**自由** 节点数量、标签。**密度** 标准。

## 构图规则

### 应做

- 构图为**多表面区域分割** — 珊瑚 / 墨水 / 奶油在硬边缘交汇；边界即布局。
- 设置每个 Bebas 元素为**大写 + 字距**（标准 2px、英雄 4px、超大 12px）；每个 Inter 标签大写，字距 1–4px。
- 眉标渲染为**奶油/墨水上珊瑚色、珊瑚上墨水色**；标题在奶油/珊瑚上用墨水色，墨水上用奶油色。
- 在珊瑚区域应用 **45° 阴影**（6% 墨水）；用 **12% 壁纸数字** 填充不足的珊瑚区域。
- 在这些元素上使用 **5px 珊瑚顶部**（卡片）/ **4px 珊瑚左侧**（磁贴）作为唯一铬色。
- 封面结尾语和目录标题偏向居中；特色和引用偏向左侧/面板分割。

### 避免

- 不要使用句首大写或无字距的 Bebas；不要搭配非 Inter 的正文字体。
- 不要添加第四表面、投影、层级或圆角矩形。
- 不要在珊瑚上使用白色标题（始终用墨水色）或任何地方使用灰色标题（灰色用于正文/元数据）。
- 不要用渐变柔化区域边界（罕见的 135° 珊瑚特色除外）。
- 不要用零散片段填充珊瑚区域 — 要么完全填充，要么添加壁纸数字/巨型标记。
- 不要让标题撑满到边缘 — 长行应降低字号阶梯。

## 宽高比行为

| 处理方案            | 16:9                       | 9:16                                 | 1:1                  |
| -------------------- | -------------------------- | ------------------------------------ | -------------------- |
| 区域分割封面   | 38/62 行，标题左对齐     | 珊瑚带加高，标题在下方       | 40/60，标题靠下   |
| 特色统计         | 数字左，数值右 | 数字顶部，数值在后           | 居中数字      |
| 引用布局         | 40/60 珊瑚+墨水            | 堆叠：珊瑚标记顶部，引用在下方 | 堆叠              |
| 结束板        | 奶油+底部珊瑚带  | 奶油+加高带                  | 居中，带在下方 |
| 三列目录 | 标题在上 3列             | 标题顶部，3列堆叠                  | 标题顶部，2+1        |
| 时间线             | 水平轨道            | 垂直轨道                        | 紧凑水平   |

安全区域在短边上保持 `5cqw` 内边距；根据比例调整展示字号阶梯，确保承重行不低于 1.4cqw 底线。Bebas 在 CJK 中约宽 20% — 根据比例调整换行。

## 批准的实体

源文件中未定义真实客户、标志或供应商 — 任何此类标记均渲染为占位符。系统提供表面和几何结构，而非品牌。

## 数字与断言（硬性规则）

绝不在帧尺度上编造数字、统计数据、日期或计数。将插槽渲染为 `— figure —`、`{metric}`、`N×`。真实数字仅当脚本提供时才出现 — 特色统计、目录和时间线尤其使用占位符，而非虚构值。壁纸数字（01，02…）为装饰性的，可以是序数。

## 渲染前自查

- **眯眼测试** — 每区域一个焦点元素以 3–5 倍于邻元素占主导。
- **留白测试** — 稀疏帧 40–55% 空白；仅目录运行密集。
- **表面** — 珊瑚/墨水/奶油中的两个或三个，在硬边缘交汇；无第四表面。
- **字体** — Bebas 大写 + 字距，按篇幅调整；珊瑚上墨水色；眉标颜色与表面匹配；≥1.4cqw 底线。
- **深度** — 0 阴影、0 圆角矩形；阴影加壁纸承载纹理。
- **锚点** — 结尾语/标题居中，特色/引用面板/左对齐；无连续 3 帧共享同一锚点。
- **虚构** — 每个数字来源于脚本，否则为占位符。

## 已知差距

- **运动设计有意不在范围之内。** frame.md 仅指定构图；时间和过渡是后续阶段。源文件中的 0.6s 透明度淡入淡出是幻灯片机制，而非帧规范。
- **Bebas Neue + Inter 通过 Google Fonts。** CJK 配对（ZCOOL XiaoWei / Yozai）继承自源文件的 CJK 部分；Bebas 在 CJK 中约宽 20%。
- **9:16 / 1:1 为指导性**，非像素锁定；验证每种比例下的可读性底线。
- 45° 阴影、壁纸数字、巨型标记和时间线虚线均为纯 CSS；无需外部图像。
