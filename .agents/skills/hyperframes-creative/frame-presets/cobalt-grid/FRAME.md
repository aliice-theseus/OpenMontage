---
version: alpha
name: Cobalt Grid — Frame (video / frame layer)
description: >
  Cobalt Grid 的 design.md 的视频优先伴侣。单位是帧 (1920×1080)。原子
  相同且神圣 — 暖奶油纸、电钴蓝墨水（唯一墨水）、永久
  方格纸网格、Newsreader 衬线 400 + Hanken Grotesk + DM Mono、顶部/底部钴蓝
  发丝线和像素故障 + QR 块签名。构图、帧比例和
  宽高比行为已为帧重写。运动不在此范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  paper: "#F0EBDE"
  paper-2: "#E6E0CE"
  ink: "#1F2BE0"
  ink-soft: "#5560E5"
  grid: "rgba(31,43,224,0.10)"
  ink-faint: "rgba(31,43,224,0.18)"

typography:
  # — reading ramp —
  body:        { fontFamily: "Hanken Grotesk", cqw: 0.83, weight: 400, lineHeight: 1.5 }
  body-lede:   { fontFamily: "Hanken Grotesk", cqw: 0.95, weight: 400, lineHeight: 1.5 }
  micro:       { fontFamily: "Hanken Grotesk", px: 13, weight: 600, tracking: "0.16em", upper: true }
  micro-strong:{ fontFamily: "Hanken Grotesk", px: 16, weight: 600, tracking: "0.18em", upper: true }
  mono-tag:    { fontFamily: "DM Mono", cqw: 0.78, weight: 400, tracking: "0.05em" }
  mono-chrome: { fontFamily: "DM Mono", px: 13, weight: 400, tracking: "0.06em" }
  # — display / hero ramp (Newsreader 400, negative tracking) —
  table-name:  { fontFamily: "Newsreader", cqw: 1.5, weight: 400, lineHeight: 1.15 }
  row-headline:{ fontFamily: "Newsreader", cqw: 2.1, weight: 400, lineHeight: 1.05 }
  ed-callout:  { fontFamily: "Newsreader", cqw: 2.6, weight: 400, lineHeight: 1.1, italic: true }
  headline:    { fontFamily: "Newsreader", cqw: 4.6, weight: 400, lineHeight: 0.95 }
  headline-index:{ fontFamily: "Newsreader", cqw: 5.0, weight: 400, lineHeight: 0.95 }
  display-quote:{ fontFamily: "Newsreader", cqw: 5.7, weight: 400, lineHeight: 1.05, tracking: "-0.005em" }
  display-chapter:{ fontFamily: "Newsreader", cqw: 6.8, weight: 400, lineHeight: 1.0, tracking: "-0.005em" }
  display-closing:{ fontFamily: "Newsreader", cqw: 9.4, weight: 400, lineHeight: 0.96, tracking: "-0.005em" }
  display-hero:{ fontFamily: "Newsreader", cqw: 10.4, weight: 400, lineHeight: 0.9, tracking: "-0.008em" }
  vbig-numeral:{ fontFamily: "Newsreader", cqw: 12.5, weight: 400, lineHeight: 0.9, tracking: "-0.015em" }

spacing:
  edge: "4cqw"          # standard frame edge inset (~80px@1920)
  pad-top: "7cqw"
  pad-bottom: "6cqw"
  gap-md: "2cqw"

components:
  graph-grid:
    backgroundImage: "linear-gradient grid, ~2cqw cells, 10% {colors.ink} ({colors.grid})"
    placement: "behind EVERY frame on the ground"
    description: "永久方格纸网格——从不禁用；画布基调。"
  hairlines:
    rule: "0.12cqw solid {colors.ink}"
    placement: "≈3cqw from top + bottom, inset {spacing.edge}"
    description: "两条持久的钴蓝规则线框定每个构图。"
  page-chrome:
    typography: "{typography.pagenum}"
    color: "{colors.ink}"
    placement: "page number bottom-right, nav/meta hint bottom-left, above the bottom hairline"
    description: "唯一持久的装饰性元素。"
  pixel-glitch:
    backgroundColor: "{colors.paper}"
    fill: "repeating-linear-gradient(90deg, {colors.ink} 0 2px, transparent 2px 8px)"
    size: "14–30cqw wide, full height, stair-stepped"
    placement: "right on cover/data, left on chapter/colophon; z above grid, below headline"
    description: "阶梯式扫描线列。装饰性。"
  qr-block:
    backgroundColor: "{colors.paper}"
    cells: "8×8, {colors.ink} on / {colors.grid} off"
    size: "3–9cqw square"
    shadow: "0 0 0 0.12cqw {colors.paper} (anti-shadow for readability, not elevation)"
    description: "QR 马赛克补丁——角落标点。"
  topbar-rule:
    typography: "{typography.headline-index} + {typography.mono-tag}"
    borderBottom: "0.12cqw solid {colors.ink}"
    description: "索引/数据/表格帧的章节头部。"
  ledger-row:
    layout: "grid: mono num · Newsreader name · Hanken desc · mono delta"
    borderBottom: "0.06cqw solid {colors.ink-faint} (header 0.12cqw solid {colors.ink})"
    typography: "{typography.mono-tag} + {typography.table-name} + {typography.body}"
    description: "密集矩阵行，带 ↑/↓/— 变化量。"
  pixel-stack-bar:
    cells: "column-reverse, {colors.grid} off / {colors.ink} on"
    baseline: "0.12cqw solid {colors.ink} + {typography.mono-tick} ticks"
    description: "数据以网格单元单元格形式呈现；呼应故障效果。"
  vstack-label:
    typography: "{typography.mono-tick}"
    transform: "writing-mode: vertical-rl"
    description: "沿帧边缘的目录装饰性元素。"
---

# Cobalt Grid — 帧（视频 / 帧层）

## 概述

帧尺度下的 Cobalt Grid 是一个**双色 risograph 趋势报告** — 暖奶油纸、电钴蓝墨水和每帧背后的**永久方格纸网格**。钴蓝是_唯一_墨水：标题、正文、规则、网格、像素故障装饰、QR 补丁。没有强调色和第二表面。

声音是三种字体的对话：**Newsreader** 衬线字重 400（层级通过大小而非字重实现）承载所有展示和标题；**Hanken Grotesk** 承载正文和大写追踪标签；**DM Mono** 承载所有装饰性元素——页码、标签、刻度线、垂直堆叠。每帧由顶部 + 底部钴蓝发丝线框定；声明式帧带有**像素故障列**和 **QR 块**补丁。

**帧尺度的关键特征：**

- **严格双色** — 奶油纸 + 钴蓝墨水；无强调色、无第二表面。
- **永久 ~2cqw 方格纸网格**（10% 钴蓝）位于每帧背后；不可禁用。
- **顶部 + 底部 1.5px 钴蓝发丝线**框定每个构图，由 `edge` 内缩。
- **Newsreader 400** 用于所有展示（负追踪）；**Hanken 600** 大写 0.16em 标签；**DM Mono** 装饰。
- **像素故障列 + QR 块**作为声明式帧的标志性装饰补丁。
- **像素堆叠条**将数据渲染为网格单元单元格（钴蓝开 / 10% 关）。

## 帧

### 帧工艺条

三条目测检查在任何结构检查之前把关每一帧：

- **眯眼测试** — 一个 Newsreader 元素以 **3–6 倍于其最近邻**为主导（`display-hero`/`vbig-numeral`）；层级通过大小而非字重实现。
- **静谧测试** — 声明式帧（封面、章节、引用、版权页）有 **45-60% 的空白**，网格可见；**索引账页和数据帧是唯一的密集例外**（密度通过安静的重复而非丰富性实现）。
- **克制测试** — **仅双色**（奶油色 + 钴蓝，绝不使用第二种色调）；每个声明式帧一个像素故障列和最多一个 QR 块。
- **参考测试** — 瞄准**WIRED Japan / Shift 双色 risograph 专著**；失败看起来像**带有第二种强调色调的彩色仪表板**。

- **主画幅：** 1920×1080 (16:9)。展示使用 **`cqw`** (`px ÷ 1920 × 100 = cqw`) 编写。
- **竖版画幅：** 1080×1920 (9:16)。**方形画幅：** 1080×1080 (1:1)。
- **安全区域：** `edge` (4cqw) 内缩；发丝线 + 页码位于安全线上。

**容器法则（承重）。** 每个帧底设置 `container-type: size` 并承载方格纸 `background-image`；所有帧相对单位均使用 `cqw`/`cqh` 相对于它——绝不使用 `vw`。网格 `background-size` 为 `~2cqw 2cqw`，使单元格密度在任何渲染尺寸下保持。

## 色彩

令牌与源文件一致。`{colors.paper}` 是底色；`{colors.ink}` 钴蓝是唯一的墨水（字体、规则、网格线、故障、QR）。`{colors.ink-soft}` 是仅用于编辑副标题的次要钴蓝；`{colors.grid}` (10%) 是永久网格 + 图表"关"单元格；`{colors.ink-faint}` (18%) 是微弱的行分隔线。**绝不使用第二种色调**——强调来自大小、从 Hanken 切换到 Newsreader、来自等宽变化量箭头或来自不透明度，从不来自颜色。

## 字体排印

两个斜坡。**阅读斜坡**（Hanken 正文 0.83cqw，等宽装饰以 px 为单位）承载文案 + 标签；**展示/英雄斜坡**（Newsreader `headline` 4.6cqw → `vbig-numeral` 12.5cqw）承载每个陈述和数字。

- **可读性底线：** 任何承重行 ≥ **1.4cqw**；等宽装饰（px）仅用于版权页。
- **按文量体：** 根据行长调整标题大小。将块限制在 **≤ 78cqw**；≤3 词 → `display-hero`/`vbig-numeral`；4-6 词 → `display-chapter`；7+ 词 → `headline`。
- **Newsreader 仅字重 400**，钴蓝色，负追踪（hero −0.008em，数字 −0.015em）。**Hanken 标签大写、0.16-0.18em。** **DM Mono 0.04-0.08em。** 无粗体衬线。

## 深度与表面

扁平。深度仅为结构性：

- **1.5px 钴蓝规则线** — 幻灯片发丝线、顶栏规则、图表基线。
- **1px 墨水淡分隔线** — 密集列表 / 账页行。
- **方格纸网格** — 一切背后的测量平面基调。
- **像素故障 + QR** — 纹理和图形标点，无 Z 轴。

**天花板：** 无投影阴影（QR 的 1.5px 纸张外扩是为可读性而设的反阴影，非抬升）、无渐变、无圆角、无第二种颜色。

## 形状

- **处处 0 圆角** — 帧、账页行、QR 单元格、故障块、图表。零圆形元素；这种方正感是身份的一部分。

## 组件

- **graph-grid / hairlines / page-chrome** — 永久帧家具，每个构图继承。
- **pixel-glitch**（边缘列）+ **qr-block**（角落补丁）— 声明式帧的标志性装饰。
- **topbar-rule** — 索引/数据/表格章节头部。**ledger-row** — 带变化量箭头的密集矩阵行。
- **pixel-stack-bar** — 数据以网格单元单元格形式呈现。**vstack-label** — 垂直等宽目录装饰。

## 帧处理方案

> 配方：底色 · 容器 · 组成 · 焦点 · 装饰 · 强调 · 静谧 · 固定/自由 · 密度。
> 网格 + 发丝线存在于每帧上。按类型选择密度：声明式 = 稀疏，索引/数据 = 密集。

### 1 · 英雄封面（标识 · 动态：衬线 + 故障 · 左对齐）

**底色** paper + grid，hairlines。**组成** pixel-glitch（右侧，~26cqw）、qr-block（右上角）、display-hero、ed-callout。**焦点** 1-2 行 `display-hero` Newsreader 标题（钴蓝色），左锚定，带斜体 `ed-callout` 副标题（`{colors.ink-soft}`）。**装饰** Hanken 眉标；顶部等宽元数据 + 页码。**强调** 无（钴蓝是唯一的墨水）。**静谧** 约 45% 纸张。**固定** Newsreader 400、故障 + QR 存在、网格 + 发丝线。**自由** 标题、故障阶梯图案、QR 位置。**密度** 稀疏。

### 2 · 索引账页（目录 · 动态：密集矩阵 · 左对齐——密集帧）

**底色** paper + grid，hairlines，`pad-top`/`pad-bottom`。**组成** topbar-rule、ledger-rows。**焦点** 顶栏（`headline-index` + 等宽实验室标签，1.5px 规则线）位于 4-6 行账页行（等宽数字 · Newsreader 名称 · Hanken 描述）之上，墨水淡分隔线。**装饰** 页码。**强调** 等宽变化量箭头。**静谧** 紧凑——密度例外（网格想要被填充）。**固定** 1.5px 顶栏规则、1px 墨水淡分隔线、Newsreader 名称。**自由** 行、实验室标签、变化量。**密度** 密集例外。

### 3 · 章节开页（章节 · 动态：缩放 · 稀疏 · 左对齐）

**底色** paper + grid，hairlines。**组成** pixel-glitch（左侧，~14cqw，低不透明度）、mono index、display-chapter、body-lede。**焦点** `display-chapter` Newsreader 标题，上方为小号等宽 `CHAPTER NN` 索引，下方为可选 Hanken 导语 ≤42cqw。**强调** 无。**静谧** 约 60%——让网格呼吸。**固定** Newsreader 400、故障低不透明度、网格可见。**自由** 标题、导语、故障侧。**密度** 稀疏。

### 4 · 数据帧（图表 · 动态：像素堆叠 · 左对齐）

**底色** paper + grid，hairlines，`pad-top`。**组成** topbar-rule、pixel-stack-bar row。**焦点** 一行 6-8 个像素堆叠条（钴蓝开 / 10% 关）位于 1.5px 钴蓝基线上，带等宽刻度线。**装饰** 顶栏标题 + 等宽数字标签；页码。**强调** 无——数据即钴蓝单元格。**静谧** 适中。**固定** 网格单元单元格、钴蓝基线、等宽刻度线。**自由** 条值（来自脚本）、刻度标签。**密度** 标准/密集。

### 5 · 宣言 / 引用（引用 · 动态：居中陈述 · 稀疏）

**底色** paper + grid，hairlines。**组成** display-quote（或 display-manifesto）、attribution rule、可选紧凑 glitch。**焦点** 2-3 行 Newsreader 拉取（钴蓝色），上方为 Hanken 眉标，下方为 1px 钴蓝署名规则线 + 等宽作者行。**强调** 无。**静谧** 约 55%——故意开放。**固定** Newsreader 400、署名规则线、网格可见。**自由** 引用、作者行。**密度** 稀疏。

### 6 · 版权页（结尾 · 动态：右对齐结束 · 稀疏）

**底色** paper + grid，hairlines。**组成** pixel-glitch（左侧边缘，镜像封面）、display-closing、mono credit columns。**焦点** 右对齐 `display-closing` Newsreader 标题，上方为 Hanken 眉标。**装饰** 底部 3-4 列等宽致谢网格；页码。**强调** 无。**静谧** 约 50%。**固定** 左侧故障、Newsreader 400。**自由** 结束语、致谢。**密度** 稀疏。

## 构图规则

### 必须

- 在每帧上保持**方格纸网格 + 顶部/底部发丝线**——它们是系统本身。
- 设置 **Newsreader 字重 400 钴蓝色**；通过大小而非字重制造层级；展示使用负追踪。
- **Hanken 标签大写 0.16em** 追踪；**DM Mono 装饰 0.04-0.08em** 追踪。
- 将数据渲染为**像素堆叠单元格**（钴蓝开 / 10% 关）；呼应故障语言。
- 在声明式帧（封面、章节、引用、版权页）上使用**像素故障列 + QR 补丁**。
- 倾向：声明式帧稀疏且呼吸感；索引/数据密集。变化锚定（索引/章节左对齐，引用/结束页居中）。

### 禁止

- 不要引入第二种墨水颜色——仅奶油色 + 钴蓝。
- 不要加粗 Newsreader、不要圆角任何角落、不要添加投影阴影（QR 外扩仅为反阴影）。
- 不要禁用网格或隐藏发丝线。
- 不要拥挤章节 / 引用 / 版权页——这些让网格展示。
- 不要将衬线标题撑到边缘到边缘——按文量体。

## 宽高比行为

| 处理方案          | 16:9                         | 9:16                                  | 1:1                           |
| ---------------- | ---------------------------- | ------------------------------------- | ----------------------------- |
| 英雄封面         | 标题左对齐，故障在右侧       | 标题顶部，故障全宽带                  | 标题偏上，故障偏下            |
| 索引账页         | 顶栏 + 行                    | 顶栏 + 较少行                         | 2 列压缩为 1 列              |
| 章节开页         | 标题左对齐，故障在左侧       | 标题顶部，故障在侧面                  | 标题居中                      |
| 数据帧           | 6-8 条                       | 4-5 条更高                            | 方形图表                      |
| 宣言 / 引用      | 居中拉取                     | 居中，更高                            | 居中                          |
| 版权页           | 右对齐，故障在左侧           | 堆叠，故障在顶部                      | 居中结束                      |

网格 + 发丝线在每个宽高比的短边上保持；重新调整 display 使承重行不低于 1.4cqw。等宽装饰仅保持拉丁/数字字符。

## 批准的实体

源文件中未定义真实客户、徽标或供应商——将任何此类标记渲染为占位符。趋势名称、信号和数字是内容；系统提供网格和装饰。

## 数字与声明（硬性规则）

绝不在帧尺度上编造数字、变化量、日期或信号计数。将插槽渲染为 `— figure —`、`{metric}`、`↑ —`。像素堆叠条高度和账页变化量尤其应在脚本提供值之前使用占位符。等宽目录序号（001, 002…）是装饰性的，可顺序使用。

## 预渲染自审

- **眯眼测试** — 一个 Newsreader 元素以 3-5 倍于其邻居的规模主导。
- **静谧测试** — 声明式帧 45-60% 空白；仅索引/数据运行密集。
- **双色** — 仅奶油色 + 钴蓝；任何地方无第二种色调。
- **家具** — 网格存在、顶部/底部发丝线存在、发丝线上方为页码装饰。
- **字体** — Newsreader 400 负追踪、按文量体；Hanken 标签 0.16em；≥1.4cqw 底线。
- **深度** — 0 阴影（QR 外扩除外）、0 圆角。
- **锚定** — 索引/章节/封面左对齐，引用/结束页居中；不连续三个帧共享一个锚定。
- **编造** — 每个数字/变化量追溯到脚本，否则为占位符。

## 已知差距

- **运动有意不在此范围内。** frame.md 仅指定构图；源文件中的 280ms 交叉淡入淡出是画板机制。
- **像素故障在 CSS 中渲染**（堆叠扫描线块），而非源文件的内联 SVG，以保持展示 SVG 纯净；保真度得到保留。
- **三个 Google Fonts**（Newsreader、Hanken Grotesk、DM Mono）；中日韩配对（Noto Serif SC 700/400）从源文件延续。
- **9:16 / 1:1 为指导**；验证每个宽高比的可读性底线和网格密度。
- QR 马赛克和故障阶梯图案是手动编写的；没有生成层。