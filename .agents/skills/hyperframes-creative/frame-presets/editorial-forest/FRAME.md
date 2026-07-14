---
version: alpha
name: Editorial Forest — Frame (video / frame layer)
description: >
  Editorial Forest 的 design.md 的视频优先伴侣。单位是帧 (1920×1080)。原子
  相同且神圣 — 绿/粉/奶油编辑三元组、Source Serif 4 字重 500
  (光学尺寸轴) 用于所有展示 + JetBrains Mono 500 大写铬色、平面纸张深度（无
  阴影）、2px 发丝线规则、6/8px 卡片圆角和字母组合圆形印章。构图 + 帧
  比例已重写。运动不在此范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  green: "#2e4a2a"
  green-deep: "#243a21"
  green-lite: "#3a5a36"
  pink: "#e89cb1"
  pink-deep: "#d27e96"
  cream: "#efe7d4"
  cream-2: "#e6dcc4"
  ink: "#1a1a17"

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Source Serif 4", cqw: 1.56, weight: 400, lineHeight: 1.38 }
  body-card:{ fontFamily: "Source Serif 4", cqw: 1.35, weight: 400, lineHeight: 1.34 }
  label:   { fontFamily: "JetBrains Mono", px: 26, cqw: 1.35, weight: 500, tracking: "0.18em", upper: true }
  caption-mono:{ fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 500, tracking: "0.14em", upper: true }
  # — display ramp (Source Serif 4 weight 500, opsz, negative tracking) —
  title-card-sm:{ fontFamily: "Source Serif 4", cqw: 2.9, weight: 500, lineHeight: 0.98, tracking: "-0.01em" }
  title-card:{ fontFamily: "Source Serif 4", cqw: 3.5, weight: 500, lineHeight: 0.96, tracking: "-0.01em" }
  headline:{ fontFamily: "Source Serif 4", cqw: 4.4, weight: 500, lineHeight: 1.0, tracking: "-0.02em" }
  headline-xl:{ fontFamily: "Source Serif 4", cqw: 5.0, weight: 500, lineHeight: 0.96, tracking: "-0.02em" }
  display:{ fontFamily: "Source Serif 4", cqw: 7.3, weight: 500, lineHeight: 1.02, tracking: "-0.02em" }
  display-hero:{ fontFamily: "Source Serif 4", cqw: 11.5, weight: 500, lineHeight: 0.92, tracking: "-0.02em" }
  stat-figure:{ fontFamily: "Source Serif 4", cqw: 11.5, weight: 500, lineHeight: 0.92, tracking: "-0.03em" }
  stat-figure-unit:{ fontFamily: "Source Serif 4", cqw: 5.7, weight: 500, lineHeight: 0.92 }
  name:    { fontFamily: "Source Serif 4", cqw: 2.3, weight: 600, lineHeight: 1.0 }

spacing:
  slide-pad: "5cqw"
  rule: "2px"
  rule-card: "2.5px"
  radius-card: "6px"
  radius-step: "8px"

components:
  topbar:
    typography: "{typography.label} (JetBrains Mono) + monogram-circle or counter"
    placement: "top edge, label left, mark right"
    description: "On EVERY frame — the system's spine; a frame without it reads untreated."
  footline:
    typography: "{typography.caption-mono} ×2, space-between"
    placement: "absolute bottom edge"
    description: "On cover/data/summary frames."
  monogram-circle:
    border: "2px solid {colors.pink}"
    rounded: "50%"
    size: "130px"
    typography: "mono monogram"
    description: "The identity stamp. Cover/summary only."
  topic-tile:
    backgroundColor: "{colors.green} (pink text) / {colors.pink} (green-deep) / {colors.green-lite} (pink) / {colors.cream-2} + 2px {colors.green} border (green)"
    rounded: "{spacing.radius-card}"
    shadow: "none"
    typography: "{typography.caption-mono} ordinal + {typography.title-card-sm} + mono foot"
    description: "Fills rotate; never repeat one across a grid."
  step-tile:
    backgroundColor: "{colors.cream} + green border / {colors.green} / {colors.pink}"
    border: "2.5px solid"
    rounded: "{spacing.radius-step}"
    typography: "mono ordinal + {typography.title-card} + {typography.body-card} + mono marker over a top rule"
    description: "Framework/process card."
  kpi-block:
    typography: "{typography.caption-mono} tag → {typography.stat-figure} (+{typography.stat-figure-unit}) → {typography.body}"
    rule: "2px accent rule above"
    description: "Oversized serif figure."
  meta-dl:
    borderTop: "2px solid {colors.green}"
    typography: "{typography.caption-mono} dt + {typography.meta-value} dd"
    description: "3-column dt/dd grid."
  bar:
    backgroundColor: "{colors.pink} / {colors.cream} / {colors.green}"
    rounded: "3px 3px 0 0"
    size: "56px wide"
    typography: "mono value above"
    description: "Vertical chart bar."
  rule-thin:
    rule: "2px solid (green on cream / pink on green / green-deep on pink)"
    description: "The only separator. Never 1px, never 3px+."
---

# Editorial Forest — 帧（视频 / 帧层）

## 概述

帧尺度下的 Editorial Forest 是一个**衬线主导的文学编辑系统** — Penguin 经典或安静年报的语域。一个自信的声音，**Source Serif 4 字重 500**（光学尺寸轴启用）承载每个标题和统计高达 ~12cqw；**JetBrains Mono** 字重 500 大写是编辑铬色（标签、说明文字、轴刻度、页脚行）。三个表面 — 森林绿、灰粉、燕麦奶油 — 别无其他。深度是**平面且基于纸张的**：无阴影、无渐变；抬升是色块对比 + 2px 发丝线 + 边框对比填充。

令人无法错认的标志是**字重 500**（从不用 400 展示，从不用 700）和**单位/衬线角色倒置**（单位字用于铬色，衬线字用于正文和展示）。正文降为衬线字重 400 — 这个 500→400 阶梯即是阅读节奏。每帧都带有单位顶部栏；字母组合圆圈是身份印章。

**帧尺度的关键特征：**

- **绿 / 粉 / 奶油 三元组** — 每帧两种表面色调是典型的，三种则太吵闹。
- **Source Serif 4 字重 500**（opsz，负字距）用于所有展示；**衬线字 400** 正文；**JetBrains Mono 500** 大写铬色。
- **平面 — 无阴影、无渐变**；抬升是色块 + 2px 发丝线 + 边框与填充对比。
- **2px 发丝线规则** 是唯一的分隔符（2.5px 在步骤磁贴上）；6/8px 卡片圆角；字母组合圆圈是唯一的完整圆形。
- **每帧都有顶部栏**（单位标签 + 字母组合/计数器）；数据/封面帧有底部行。
- **宽敞且专注** — 每帧一个主题在深度负空间中；元素较少，尺寸较大。

## 帧

### 帧工艺条

三项目测检查在任何结构检查前把关每帧：

- **眯眼测试** — 一个 Source Serif 4 瞬间以 3–6 倍于其邻元素占主导；表面块使视线聚集中心。
- **留白测试** — 每帧一个主题在深度负空间中；**topic-tile 和 step 网格是唯一密集的例外**。
- **克制测试** — 每帧**最多两种表面色调**（三种太吵闹）；衬线字 **字重 500** 展示 / **400** 正文；绿色背景专用于重磅瞬间。
- **参照测试** — 瞄准**Penguin 经典 / 安静年报 / 艺术书刊**；失败看起来像**带阴影多色的网页仪表盘**。

- **主尺寸：** 1920×1080 (16:9)。展示以 **`cqw`** 为单位编写（`px ÷ 1920 × 100 = cqw`）。
- **竖版：** 1080×1920 (9:16)。**方版：** 1080×1080 (1:1)。
- **安全区域：** `slide-pad` 5cqw（源文件宽敞的 96–140px）；顶部栏/底部行位于其内。

**容器法则（承重规则）。** 每个帧背景设置 `container-type: size`；所有帧相对单位都是 `cqw`/`cqh` 以它为基准 — 从不用 `vw`（源文件是固定 1920 画布，所以其像素可清晰映射：`px ÷ 1920 × 100`）。发丝线保持 2px；卡片圆角保持 6/8px。

## 颜色

色值令牌与源文件一致。默认背景 `{colors.cream}` 用于内容；`{colors.green}` 用于封面/声明/摘要重磅瞬间。**标题：** 奶油上绿色，绿色上奶油色（或英雄尺度上的粉色），粉色上深绿色。**正文：** 奶油上墨水色，绿色上奶油色，粉色上深绿色。标签/规则线采用区域的强调色（绿色上粉色，奶油上绿色，粉色上深绿色）。磁贴填充旋转绿色 / 粉色 / 浅绿 / 带绿边的 cream-2。**无第四种颜色家族** — 三元组 + 接近的重复是整个调色板；绝不在表面上使用 `rgba` 透明度。

## 排版

两个阶梯。**阅读/铬色阶梯**（Source Serif 4 **400** 正文 1.56cqw；JetBrains Mono 标签以 px 为单位）承载文案 + 铬色；**展示阶梯**（Source Serif 4 **500** `title-card-sm` 2.9cqw → `display-hero`/`stat-figure` 11.5cqw，opsz，负字距）承载每个标题 + 图表。

- **可读性底线：** 任何承重行 ≥ **1.4cqw**；单位 px 标签仅为铬色。
- **按篇幅调整：** 根据标题的长度调整字号。将标题块限制在 **≤ 78cqw**；≤3 词 → `display-hero`；4–6 → `headline-xl`；7+ → `headline`。将 7.3–11.5cqw 级别留给声明/统计/封面。
- **衬线字展示用字重 500，正文用 400**（节奏），600 仅用于署名。负字距（−0.01..−0.03em），紧凑行高（0.92–1.02）。**单位字大写，0.08–0.18em。** 无斜体、无下划线、无第三种字体、无字重 500 的衬线正文。

## 深度与表面

平面，基于纸张。抬升来自：

- **色块对比** — 奶油上的绿色磁贴通过墨色块分隔产生抬升感。
- **2px 发丝线规则** — 区域强调色中的节分隔符。
- **边框与填充对比** — cream-2 磁贴 + 2px 绿色边框产生与实心磁贴不同的抬升感。

**天花板规则：** 零阴影（无任何阴影 — 添加 `box-shadow` 会破坏纸张感觉），无渐变，无发光；表面是实心墨水在纸上。

## 形状

- **6px** 主题磁贴、**8px** 步骤磁贴、**2px** 图例色块、**3px 3px 0 0** 条形图顶部、**50%** 字母组合圆圈。无方角，无过重圆角。

## 组件

- **topbar**（脊柱）+ **footline** + **monogram-circle**（身份印章）— 铬色集合。
- **topic-tile**（6px，旋转填充）/ **step-tile**（8px，2.5px 边框）— 目录 + 框架模式。
- **kpi-block**（超大衬线数字）/ **meta-dl**（3列，2px 规则）/ **bar** / **rule-thin** — 数据 + 结构。

## 帧处理方案

> 配方：背景 · 容器 · 组成 · 焦点 · 铬色 · 强调 · 留白 · 固定/自由 · 密度。
> 每帧都有顶部栏；每帧一个主题在深度负空间中。

### 1 · 封面（标识 · 动势：超大衬线字 · 绿色 · 左对齐）

**背景** `{colors.green}`，`slide-pad`。**组成** topbar（单位标签 + monogram-circle）、display-hero、body lede、footline。**焦点** 粉色的 2 行 Source Serif 4 `display-hero`（一个词为奶油色），左对齐。**铬色** 单位顶部栏；单位底部行。**强调** 粉色展示 + monogram circle。**留白** ~50%。**固定** serif 500、平面、monogram 2px 粉色。**自由** 标题、哪个词为奶油色。**密度** 低。

### 2 · 主题磁贴（目录 · 动势：旋转填充网格 · 奶油 · 密集帧）

**背景** `{colors.cream}`，`slide-pad`。**组成** topbar、headline-xl、3–4× topic-tile。**焦点** 一行 6px 磁贴，填充旋转绿色 / 粉色 / 带绿边 cream-2，每个包含单位序数 + 衬线标题。**铬色** 单位顶部栏。**强调** 磁贴填充（4 种中混合 3 种，从不重复）。**留白** 紧凑 — 密度例外。**固定** 6px 圆角、旋转填充、无阴影。**自由** 磁贴标题、哪些填充。**密度** 密集例外。

### 3 · KPI 统计（数据 · 动势：超大数字 · 绿色）

**背景** `{colors.green}`，`slide-pad`。**组成** topbar、kpi-block（单位标签 + 220px stat-figure + 衬线描述）、footline。**焦点** Source Serif 4 `stat-figure`（~11.5cqw，+单位）粉色，在 2px 粉色规则线之上。**铬色** 单位顶部栏 + footline。**强调** 粉色数字。**留白** ~55%。**固定** serif 500 数字、2px 强调规则线、平面。**自由** 数字（来自脚本）、标签、描述。**密度** 低。

### 4 · 声明（引用 · 动势：展示衬线字 · 奶油 · 左对齐）

**背景** `{colors.cream}`，宽敞内边距。**组成** topbar、display、name (600)、caption-mono 职位。**焦点** 绿色的 2 行 Source Serif 4 `display`（~7.3cqw）；下方有字重 600 的署名 + 单位职位。**铬色** 单位顶部栏。**强调** 无 — 衬线字本身承载。**留白** ~55%。**固定** serif 500 展示 + 600 名称仅用，无斜体。**自由** 引用、名称、职位。**密度** 低。

### 5 · 步骤框架（流程 · 动势：8px 步骤磁贴 · 奶油/绿色）

**背景** `{colors.cream}`（或绿色），`slide-pad`。**组成** topbar、headline、3–4× step-tile。**焦点** 一行 8px 步骤磁贴（2.5px 边框）— 单位序数 + serif 68px 标题 + 正文 + 顶部规则线上的单位标记；填充旋转带绿边的奶油 / 绿色 / 粉色。**强调** 磁贴填充。**留白** 适中。**固定** 8px 圆角、2.5px 边框、单位标记。**自由** 步骤、填充。**密度** 标准。

### 6 · 图表（数据 · 动势：条形图 + 元数据 · 绿色）

**背景** `{colors.green}`，`slide-pad`。**组成** topbar、headline、bars + 2px 轴线规则、meta-dl。**焦点** 内边缘 2px 规则线上的 56px 粉/奶油/绿条形图，带单位刻度；下方可选 3列 meta-dl。**铬色** 单位顶部栏。**强调** 条形图填充。**留白** 适中。**固定** 56px 条形图、3px 顶部、2px 轴线、单位刻度。**自由** 值（来自脚本）、标签。**密度** 标准。

## 构图规则

### 应做

- 所有展示使用 **Source Serif 4 字重 500**，opsz，负字距，紧凑行高；**正文为 400**。
- 所有标签/说明文字/轴/底部行设为 **JetBrains Mono 500 大写，0.08–0.18em**。
- 每帧都给予一个 **topbar**（单位标签 + 字母组合或计数器）；数据/封面帧加 footline。
- 选择**每帧一个主导表面**（最多两种色调）；**旋转磁贴填充**，在一个网格中从不重复。
- 使用区域强调色中的 **2px 发丝线** 分隔节；将 monogram circle 留给封面/摘要。
- 展示尺寸大胆扩展（7.3–11.5cqw）用于声明/统计/封面；偏向左对齐/编辑风格，每帧一个主题。

### 避免

- 无 box-shadow、渐变或发光 — 仅平面、基于纸张的深度。
- 无第三种字体；无斜体/下划线；无字重 500 的衬线正文；无单位字在标题尺度。
- 无第四种颜色家族；无 `rgba` 表面；无 1px 或 4px+ 规则（仅 2px / 2.5px）。
- 无两个竞争的内容块；不要省略 topbar。
- 不要让标题撑满到边缘 — 降低字号阶梯。

## 宽高比行为

| 处理方案      | 16:9                             | 9:16                        | 1:1                      |
| -------------- | -------------------------------- | --------------------------- | ------------------------ |
| 封面          | display 左对齐，monogram 右上角 | display 顶部，monogram 下方 | display，monogram 角落 |
| 主题磁贴    | 3–4 列并排                       | 堆叠                     | 2×2                      |
| KPI 统计       | 数字左对齐                      | 数字居中加高     | 居中                 |
| 声明      | 引用左对齐                       | 引用堆叠               | 居中                 |
| 步骤框架 | 3–4 列并排                       | 堆叠                     | 2×2                      |
| 图表          | bars + meta                      | bars 加高，meta 堆叠    | 方形图表             |

`slide-pad` 在短边上保持；将展示字号调整在 1.4cqw 底线之上。顶部栏在每种比例下核跨顶部；monogram 可降低到角落。

## 批准的真实实体

源文件中未定义真实客户、标志或供应商 — 任何此类标记均渲染为占位符。monogram、footline 字符串和磁贴计数器承载每套占卡的身份；图表数值是内容。

## 数字与断言（硬性规则）

绝不在帧尺度上编造数字、KPI、日期或计数。将插槽渲染为 `— figure —`、`{metric}`、`— %`。KPI 块、条形图和元数据值尤其使用占位符，直到脚本提供。期号/计数器是装饰性铬色。

## 渲染前自查

- **眯眼测试** — 一个衬线字瞬间占主导；表面块使视线聚集中心。
- **留白测试** — 每帧一个主题在深度负空间中；仅 topic-tile/step 网格运行密集。
- **三元组** — 最多两种表面色调；标题/正文/标签使用正确的每表面颜色；无第四家族。
- **字体** — Source Serif 4 **500** 展示（opsz，负字距）/ **400** 正文；单位大写 0.08–0.18em；≥1.4cqw 底线。
- **深度** — 0 阴影，0 渐变；2px 发丝线；6/8px 圆角；monogram 是唯一完整圆形。
- **铬色** — 每帧都有 topbar；数据/封面帧加 footline。
- **虚构** — 每个数字来源于脚本，否则为占位符。

## 已知差距

- **运动设计有意不在范围之内。** frame.md 仅指定构图；源文件依赖 `deck-stage.js` 进行缩放/导航，无过渡规范。
- **Source Serif 4 (opsz 8..60) + JetBrains Mono 通过 Google Fonts** — 光学尺寸轴至关重要；非 opsz 备用方案会彼视尺寸敏感的字形。CJK：LXGW WenKai（展示）/ Noto Serif SC（正文）/ Noto Sans Mono CJK（铬色）。
- **9:16 / 1:1 为指导性**；验证底线和两色调纪律在每种比例下的保持。
- 条形图、发丝线、磁贴和 monogram circle 为纯 CSS；无需外部图像。
- **对比度：** 绿上粉 / 粉上绿仅在展示尺度（84px+）下使用；保持小字为奶油上绿或墨水上奶油。
