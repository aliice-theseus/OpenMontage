---
version: alpha
name: Creative Mode — Frame (video / frame layer)
description: >
  Creative Mode 的 design.md 的视频优先伴侣。单位是帧 (1920×1080)，
  不是幻灯片中的一页。原子相同且神圣 — 暖奶油画布、4px 墨水色
  边框、硬偏移阴影（无模糊）、Archivo Black 大写 0.92 行高、
  JetBrains Mono 分类、Space Grotesk 正文、四强调色调色板。构图、
  帧比例和宽高比行为已为帧重写。运动不在此范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#EFE9D9"
  cream-2: "#E4DCC4"
  ink: "#0F0F0F"
  ink-2: "#2A2A2A"
  green: "#1F8A4C"
  green-dark: "#136636"
  pink: "#F06CA8"
  pink-dark: "#D14E8B"
  orange: "#E85A1F"
  yellow: "#F5C518"

typography:
  # — reading ramp (px @ 1920, with cqw) —
  body-lg:    { fontFamily: "Space Grotesk", px: 28, cqw: 1.46, weight: 400, lineHeight: 1.4 }
  body-md:    { fontFamily: "Space Grotesk", px: 24, cqw: 1.25, weight: 400, lineHeight: 1.3 }
  mono-label: { fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 400, tracking: "0.06em", upper: true }
  mono-kicker:{ fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 400, tracking: "0.14em", upper: true }
  table-head: { fontFamily: "Archivo Black", px: 28, cqw: 1.46, weight: 400, upper: true }
  # — display / hero ramp (frame-native, cqw-first) —
  step-title: { fontFamily: "Archivo Black", px: 34,  cqw: 1.77, weight: 400, lineHeight: 1.0, upper: true }
  badge-label:{ fontFamily: "Archivo Black", px: 28,  cqw: 1.46, weight: 400, upper: true }
  marker:     { fontFamily: "Archivo Black", cqw: 2.4, weight: 400, lineHeight: 1.0, upper: true }
  stamp-num:  { fontFamily: "Archivo Black", cqw: 2.2, weight: 400, lineHeight: 0.9 }
  stat-num:   { fontFamily: "Archivo Black", cqw: 6.4, weight: 400, lineHeight: 0.88 }
  step-num:   { fontFamily: "Archivo Black", cqw: 7.0, weight: 400, lineHeight: 0.85 }
  display-head: { fontFamily: "Archivo Black", cqw: 4.2, weight: 400, lineHeight: 0.92, tracking: "-0.01em", upper: true }
  display-lg: { fontFamily: "Archivo Black", cqw: 8.0,  weight: 400, lineHeight: 0.9,  tracking: "-0.01em", upper: true }
  display-xl: { fontFamily: "Archivo Black", cqw: 11.0, weight: 400, lineHeight: 0.9,  tracking: "-0.01em", upper: true }
  display-hero:{ fontFamily: "Archivo Black", cqw: 15.5,weight: 400, lineHeight: 0.84, tracking: "-0.02em", upper: true }

spacing:
  frame-pad: "3.3cqw"        # 64px chrome gutter @1920
  content-gutter: "5cqw"     # 96px content gutter @1920
  grid-gap: "1.5cqw"         # 28px
  cell-pad: "1.7cqw"         # 32px

components:
  frame-chrome:
    typography: "{typography.mono-label}"
    placement: "topbar 2.5cqw from top, meta 2.5cqw from bottom, both inset {spacing.frame-pad}"
    rounded: "0"
    shadow: "none"
    description: "Mono topbar (section label left + 999px ink-stroked pill right) + meta footer (descriptor left + NN • NN counter right, 0.5cqw ink dot divider). Present on most frames."
  stat-cell:
    backgroundColor: "{colors.green} · {colors.pink} · {colors.orange} · {colors.cream}"
    textColor: "{colors.cream} on accent · {colors.ink} on cream"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    padding: "{spacing.cell-pad}"
    typography: "{typography.stat-num} + {typography.mono-label}"
    shadow: "none"
    description: "Flat accent/cream stat tile, square corners, no shadow."
  step-card:
    backgroundColor: "{colors.cream} · {colors.pink} · {colors.yellow} · {colors.green}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    padding: "{spacing.cell-pad}"
    typography: "{typography.step-num} + {typography.step-title} + {typography.body-md}"
    shadow: "none"
    description: "Ink-bordered card; giant step-num top. Sequence alternates cream with accents and ENDS on green."
  marker-block:
    backgroundColor: "{colors.pink}"
    textColor: "{colors.ink}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    typography: "{typography.marker}"
    shadow: "1.25cqw 1.25cqw 0 {colors.orange}, 1.25cqw 1.25cqw 0 0.2cqw {colors.ink}"
    description: "The one hard-offset featured callout per frame."
  kicker-block:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    typography: "{typography.mono-kicker}"
    padding: "0.5cqw 1cqw"
    rounded: "0"
    description: "Inverted eyebrow chip."
  badge-rotated:
    backgroundColor: "{colors.yellow}"
    border: "0.4cqw solid {colors.ink}"
    typography: "{typography.badge-label}"
    rounded: "0"
    transform: "rotate(-4deg)"
    description: "Deliberate-imperfection annotation."
  pill-badge:
    backgroundColor: "{colors.cream}"
    border: "0.2cqw solid {colors.ink}"
    rounded: "999px"
    typography: "{typography.mono-label}"
    description: "The ONLY rounded element; reads as a chip, not a card."
  stamp:
    backgroundColor: "{colors.pink}"
    border: "0.4cqw solid {colors.cream}"
    size: "~18cqw square"
    rounded: "0"
    transform: "rotate(-6deg)"
    typography: "{typography.stamp-num}"
    description: "Closing seal with a cream circular inner ring."
  comparison-table:
    backgroundColor: "{colors.cream-2}"
    border: "0.4cqw solid {colors.ink}"
    rule: "0.3cqw solid {colors.ink}"
    rounded: "0"
    typography: "{typography.table-head} + {typography.body-md}"
    shadow: "none"
    description: "Ink head row with cream Archivo labels; pink/green column-fill variants."
  decorative-circle:
    backgroundColor: "{colors.yellow}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "50%"
    description: "Decorative figure; pairs with a green panel for shape contrast."
---

# Creative Mode — 帧（视频 / 帧层）

## 概述

帧尺度下的 Creative Mode 是一个**新粗野主义编辑海报披着运动的外衣** — 暖奶油纸、近黑墨水色和四种全饱和碰撞的强调色。每帧是一个平面色块构图：无渐变、无模糊阴影、无圆角卡片（除了一个药丸碎片）。深度是**硬偏移阴影**（实色同向复制）或**色块对比**，从不是光线。

The display voice is **Archivo Black in strict uppercase at 0.92 line-height** — letters overlap
their own cap height; that tightness is the brand. **JetBrains Mono** carries every label, kicker,
counter, and axis as a "technical artifact" register. **Space Grotesk** carries the few body lines.
The frame is loud by construction and calm by restraint: two or three accents per frame, the green
ground reserved for a single closing plate, the hard shadow spent on one featured element only.

**帧尺度的关键特征：**

- **奶油背景**（`{colors.cream}`）在几乎每帧上；`{colors.green}` 专用于结束板。
- **0.4cqw (4px @1920) 墨水色边框** 在每个结构元素上；0.3cqw 内部规则线。
- **硬偏移阴影**（≈1.25cqw，橙色+墨水）在每帧一个特色块上 — 从不模糊。
- **Archivo Black 大写**，始终 0.92 行高；不存在句首大写的 Archivo Black。
- **每帧两到三个强调色**，从不全四种；碰撞即是设计。
- **每帧一个药丸芯片**（999px）作为唯一圆角元素。

### 帧工艺条

三项目测检查在任何结构检查前把关每帧：

- **眯眼测试** — 恰好一个元素占主导，以 **3–6 倍于最近邻元素**（深渊，而非阶梯）：`display-hero`/`display-xl` 声明或 `stat-num` 数字，绝不两个竞争的标题。
- **留白测试** — 稀疏帧（封面、声明、结束板）呈现 **45–60% 空白**；**统计网格和对比账簍是唯一密集的例外**。绝不填充稀疏帧以看起来完整。
- **克制测试** — 稀缺的手法每帧只用一次：最多一个硬偏移阴影，两到三个强调色（从不全四种），绿色背景专用于单一结束板。
- **参照测试** — 瞄准**Risograph 编辑海报 / 扮酷杂志张页**（平面墨边块、一个大声明、广阔奶油）；失败看起来像**圆角、柔和阴影的 SaaS 功能网格**。

## 帧

- **主尺寸：** 1920×1080 (16:9)。所有展示尺寸以 **`cqw`** 为单位编写（`px ÷ 1920 × 100 = cqw`）。
- **竖版：** 1080×1920 (9:16)。**方版：** 1080×1080 (1:1)。
- **安全区域：** 铬色为 `3.3cqw` (64px) 内缩进；内容为 `5cqw` (96px) 沟槽。无承重元素跨越 `3.3cqw` 线。

**容器法则（承重规则）。** 每个帧背景设置 `container-type: size`。所有帧相对单位都是 `cqw`/`cqh`（1cqw = 帧宽度的 1%），以那个背景为基准解析 — **绝不用 `vw`。** `vw` 测量页面视口，因此帧在非全屏渲染时会膨胀；`cqw` 在任何渲染尺寸下都相对于帧解析。这就是为什么展示阶梯中的所有尺寸都是 `cqw`。

## 颜色

色值令牌与源文件一致。在帧尺度下：`{colors.cream}` 是**背景**，`{colors.ink}`
是边框 + 字体，四种强调色（`green` / `pink` / `orange` / `yellow`）是**每帧配给两到三种的平面填充**。`{colors.orange}` 也是硬阴影颜色。`{colors.green}`
兼作单一结束板背景 — 其稀有性即是冲击力。绝不引入第五种强调色；绝不使用纯白色；绝不使用渐变。

## 排版

两个阶梯。**阅读阶梯**（正文、单位标签、表格标题）使用 px+cqw 用于铬色和文案。**展示/英雄阶梯** 是帧原生的，以 `cqw` 为单位编写 — 从 `display-head` (4.2cqw) 到 `display-hero` (15.5cqw)，用于品牌字标封面。

- **可读性底线：** 任何承重行 ≥ **1.4cqw (≈27px@1920)**。单位铬色在 1.15cqw 仅为版权信息。
- **按篇幅调整：** 标题的字号跟踪其行长。将标题块限制在 **≤ 78cqw**，绝不触及安全边距。≤3 词 → `display-hero`/`display-xl`；4–6 词 → `display-lg`；7+ 词 → `display-head`。短行用大字；长行降级。
- **所有 Archivo Black 始终大写 + 0.92 行高**。单位字体使用 0.06–0.14em 字距。绝不将 Archivo Black 字距超过编码的 −0.01em；绝不将正文居中设置。

## 深度与表面

零模糊。仅两种深度手法：

- **硬偏移阴影** — 在 X 和 Y 方向上约 1.25cqw 的实色复制偏移（`box-shadow: 1.25cqw 1.25cqw 0 {colors.orange}, 1.25cqw 1.25cqw 0 0.2cqw {colors.ink}`）。**每帧一个特色块**（marker、stamp）。图解堆叠可使用 0.95cqw 纯墨水偏移。
- **色块对比** — 奶油在 cream-2 上，墨水在奶油上，强调色在奶油上。当对比足以承载时无需阴影。

**天花板规则：** 无模糊阴影、无渐变、无发光，任何地方都不得使用。

## 形状

- 每个结构元素 **0 圆角** — 统计单元、步骤卡片、表格单元、标记、面板。
- **50%** 在装饰圆圈、印章内环、元数据圆点上。
- **999px** 仅在顶部栏药丸芯片上 — 唯一圆角例外。
- **旋转** 仅在固定品牌角度上：badge −4°，stamp −6°。

## 组件

- **frame-chrome** — 单位顶部栏 + 元数据底部栏。几乎每帧都有；仅当纯全出血品牌字标节拍与之竞争时才省略。
- **stat-cell / step-card** — 墨边平面填充块；步骤序列以绿色结束。
- **marker-block** — 每帧一个硬阴影特色引出块。
- **kicker-block** — 反色墨水眉标芯片；**badge-rotated** — −4° 黄色注释；**pill-badge** — 唯一圆角芯片。
- **stamp** — −6° 结束封印。**comparison-table** — cream-2 账簍，带墨色标题行。
- **decorative-circle** — 黄色圆盘，用于与绿色面板形成形状对比。

## 帧处理方案

> 每块板的配方：背景 · 容器 · 组成 · 焦点 · 铬色 · 强调 · 留白 · 固定/自由 · 密度。
> 在 1920×1080 下编写。偏向居中；变化锚点；每帧一个想法。

### 1 · 品牌字标封面（标识 · 动势：全帧锁定 · 居中）

**背景** `{colors.cream}`，`frame-pad`。**容器** 网格，铬色顶部/底部，焦点居中。**组成** frame-chrome、品牌字标。**焦点** `display-hero`(15.5cqw)的两行品牌字标，居中，第二行为强调色（`{colors.pink}`/`orange`）。**铬色** 单位顶部栏（节目标签 + 药丸）和元数据底部栏（描述符 + 01•NN）。**强调** 仅第二行颜色；可选一个角落装饰圆出血边缘。**留白** ~55% 空白奶油。**固定** Archivo Black 大写 0.84 lh，品牌字标上一个强调色，方角。**自由** 哪种强调色、换行、圆是否出血角落。**密度** 稀疏。

### 2 · 大声明（超大声明 · 动势：比例 · 左对齐）

**背景** 全出血强调色（`{colors.pink}`/`green`/`orange`），`content-gutter`。**容器** flex，声明左锚定且垂直居中。**组成** kicker-block、声明。**焦点** `display-xl`/`display-lg` 的 2–3 行声明，强调色上的墨水色（火上墨 — 从不白色）。**铬色** 声明上方的小墨色 kicker-block；单位元数据底部栏。**强调** 背景本身就是强调色；无第二个强调色竞争。**留白** ~45% 的有色区域空白。**固定** 强调色上的墨水字体、按篇幅调整尺寸、字体无阴影。**自由** 声明、哪种强调色背景、哪些换行。**密度** 稀疏 — 一个想法。

### 3 · 统计网格（目录 · 动势：密度 — 唯一密集帧 · 居中）

**背景** `{colors.cream}`，`content-gutter`。**容器** 网格：居中的 `display-head` 上方有一行 3 列统计单元。**组成** frame-chrome、3× stat-cell。**焦点** 三个墨边单元的行（绿色 / 粉色 / 橙色），每个包含 `stat-num` + 单位标签。**铬色** 单位顶部栏 + 元数据。**强调** 三个单元填充（名义密集例外 — 此处允许三个强调色）。**留白** ~25% — 设计上紧凑。**固定** 0.4cqw 边框、方角、无单单元阴影、单位标签。**自由** 三个数字+标签、标题文案、哪三种强调色。**密度** 密集例外。

### 4 · 结束板（收尾 · 动势：背景交换 · 居中）

**背景** `{colors.green}`（整套帧中唯一的绿色帧），`frame-pad`。**焦点** `{colors.cream}` 中的 `display-lg` 两行结尾语，居中。**组成** frame-chrome（奶油变体）、stamp。**铬色** 奶油色单位顶部栏 + 元数据。**强调** 一个在角落旋转 −6° 的 `{colors.pink}` stamp，奶油环 + stamp-num。**留白** ~55% 空白绿色。**固定** 绿色背景专用于此节拍，奶油色在绿上字体，一个stamp。**自由** 结尾语文案、stamp文字、stamp角落。**密度** 稀疏。

### 5 · 特色标记（呼出 · 动势：硬阴影焦点 · 左对齐/非对称）

**背景** `{colors.cream}`。**组成** frame-chrome、marker-block、可选 body-md 支撑行。**焦点** 粉色 marker-block，带有标志性的橙色+墨水硬偏移阴影，非对称设置。**强调** 粉色块 + 橙色阴影（两个强调色）。**留白** ~50%。**固定** 每帧恰好一个硬阴影，0.4cqw 边框。**自由** marker 文案、块位置、可选支撑行。**密度** 稀疏。

### 6 · 对比账簍（数据 · 动势：矩阵 · 左对齐）

**背景** `{colors.cream}`，`content-gutter`。**组成** frame-chrome、comparison-table。**焦点** cream-2 表格，带墨色标题行；一列填充（粉色或绿色）标记胜出者。**强调** 单列填充。**留白** 紧凑 — 第二个密集例外。**固定** cream-2 填充、0.3cqw 内部规则线、墨色标题行带奶油 Archivo 标签。**自由** 行、哪列填充、文案。**密度** 密集例外。

## 构图规则

### 应做

- 构图围绕**每帧一个想法**，焦点元素 **3–5 倍于其邻元素**（眯眼测试）。
- **偏向居中** — 封面、声明、统计网格和结束板均居中其焦点元素；左对齐/非对称留给 marker 和 ledger。
- 保持稀疏帧 **45–60% 空白**；仅统计网格和 ledger 运行密集。
- 使用**每帧两到三个强调色**；将 `{colors.green}` 背景专用于结束板。
- 将硬偏移阴影用于**每帧一个特色块**。
- 标题尺寸 **按篇幅调整**；Archivo Black 大写且 0.92 lh。

### 应做n't

- Don't round corners (except the pill chip); don't gradient, blur, or glow.
- Don't set Archivo Black in sentence case or letter-space it beyond −0.01em.
- Don't use all four accents on one frame, a fifth accent, or pure white.
- Don't center body copy or set labels in anything but JetBrains Mono.
- Don't blow a headline edge-to-edge — step the ramp down for long lines.
- Don't put two hard shadows on one frame.

## 宽高比行为

| 处理方案         | 16:9                            | 9:16                         | 1:1                      |
| ----------------- | ------------------------------- | ---------------------------- | ------------------------ |
| 品牌字标封面    | 两行居中              | 堆叠加高，圆圈顶部   | 居中更紧凑        |
| 大声明         | 声明左对齐，全强调         | 声明顶部，强调满幅       | 声明居中           |
| 统计网格         | 标题在上 3列行              | 标题顶部，3列堆叠          | 标题顶部，2×2（第4单元） |
| 结束板     | 结尾语居中，stamp角落 | 堆叠，stamp在下方         | 居中，stamp角落   |
| 特色标记   | marker 非对称               | marker 居中，阴影向下 | marker 居中          |
| 对比账簍 | 全宽表格                | 表格滚动到更少列  | 2列表格              |

安全区域在每种比例的短边上保持 `3.3cqw` 铬色内缩进；根据比例调整展示字号阶梯，确保承重行不低于 1.4cqw 底线。

## 批准的实体

源文件中未定义真实客户、标志或供应商 — 任何此类标记均渲染为占位符。产品/节目与内容无关；系统提供几何结构，而非品牌。

## 数字与断言（硬性规则）

绝不在帧尺度上编造数字、百分比、计数或日期。将数据槽位渲染为 `— figure —`、`{metric}`、`N×`。真实数字仅当脚本提供时才出现 — 统计网格和 ledger 尤其使用占位符，而非虚构值。

## 渲染前自查

- **眯眼测试** — 一个元素以 3–5 倍于其邻元素占主导，否则重新调整尺寸。
- **留白测试** — 稀疏帧 45–60% 空白；仅统计网格 / ledger 运行密集。
- **强调色** — 每帧两到三个，从不全四种；绿色背景仅在结束板上。
- **深度** — 0 模糊；最多一个硬偏移阴影；否则使用色块对比。
- **几何** — 方角（除药丸外）；旋转仅在 −4/−6°。
- **字体** — Archivo Black 大写 0.92 lh，按篇幅调整，承重行 ≥1.4cqw。
- **锚点** — 默认居中；左对齐/非对称仅用于 marker + ledger；无连续 3 帧共享同一锚点。
- **虚构** — 每个数字来源于脚本，否则为占位符。

## 已知差距

- **运动设计有意不在范围之内。** frame.md 仅指定构图；时间和过渡是后续阶段。结束绿被描述为一块“板”，而非一个过渡。
- **Archivo Black 需要 Google Fonts**；备用为 `sans-serif`。CJK 配对（Noto Serif SC 900 / NSC 400）继承自源文件的 CJK 部分。
- **9:16 / 1:1 为指导性**，非像素锁定；验证每种比例下的可读性底线。
- 装饰性几何图形（圆圈、印章、堆叠块）为纯 CSS；无需外部图像。
