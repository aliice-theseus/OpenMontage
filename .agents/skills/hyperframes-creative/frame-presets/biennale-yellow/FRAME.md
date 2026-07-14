---
version: alpha
name: Biennale Yellow — Frame (video / frame layer)
description: >
  Biennale Yellow 的 design.md 的视频优先伴侣。单位是帧 (1920×1080)。原子
  相同且神圣——暖羊皮纸底色、单一深靛蓝油墨、太阳黄作为
  光晕/面板/瓷砖底色、Instrument Serif 展示 + Archivo 无衬线 + JetBrains Mono 数据、
  1px 发丝线作为唯一边框、氛围深度（无阴影）以及右下角
  页码。构图 + 帧比例已重写。克制是规则；运动不在此范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  paper: "#E9E5DB"
  paper-deep: "#DCD6C4"
  sun: "#F1EE2E"
  sun-soft: "#F8F39B"
  haze: "#F0DA7C"
  ink: "#1B2566"
  ember: "#E26B4A"

typography:
  # — reading + data ramp —
  body:    { fontFamily: "Archivo", cqw: 0.85, weight: 400, lineHeight: 1.5, color: "ink" }
  body-lede:{ fontFamily: "Archivo", cqw: 0.95, weight: 400, lineHeight: 1.55 }
  micro-label:{ fontFamily: "Archivo", px: 13, weight: 600, tracking: "0.18em", upper: true }
  rail-label:{ fontFamily: "Archivo", px: 13, weight: 600, tracking: "0.32em", upper: true }
  mono-data:{ fontFamily: "JetBrains Mono", cqw: 0.73, weight: 400, tracking: "0.04em" }
  pagenum: { fontFamily: "JetBrains Mono", px: 13, weight: 400, tracking: "0.08em", opacity: 0.75 }
  # — display ramp (Instrument Serif 400, tight, negative tracking) —
  ledger-title:{ fontFamily: "Instrument Serif", cqw: 1.55, weight: 400, lineHeight: 1.15 }
  strand-title:{ fontFamily: "Instrument Serif", cqw: 1.7, weight: 400, lineHeight: 1.1 }
  headline-sm:{ fontFamily: "Instrument Serif", cqw: 2.9, weight: 400, lineHeight: 1.0 }
  headline:{ fontFamily: "Instrument Serif", cqw: 4.6, weight: 400, lineHeight: 1.06, tracking: "-0.005em" }
  date-rail:{ fontFamily: "Instrument Serif", cqw: 5.0, weight: 400, lineHeight: 0.96, tracking: "-0.005em" }
  display-it:{ fontFamily: "Instrument Serif", cqw: 7.0, weight: 400, italic: true, lineHeight: 1.04, tracking: "-0.005em" }
  numeral-md:{ fontFamily: "Instrument Serif", cqw: 7.5, weight: 400, lineHeight: 0.92, tracking: "-0.01em" }
  display:{ fontFamily: "Instrument Serif", cqw: 14.6, weight: 400, lineHeight: 0.86, tracking: "-0.018em" }
  numeral-jumbo:{ fontFamily: "Instrument Serif", cqw: 28.0, weight: 400, lineHeight: 0.84, tracking: "-0.04em" }

spacing:
  pad-edge: "4cqw"
  pad-region: "4.2cqw"
  gap-region: "2.5cqw"

components:
  sun-bloom:
    background: "radial gradient {colors.sun} core → {colors.sun-soft} → {colors.haze} → transparent on {colors.paper}"
    size: "42–70% of the frame, off-center or behind the focal element"
    description: "The primary depth layer. One per frame; a flat parchment frame reads as broken."
  ember-bloom:
    background: "radial {colors.ember} at 15–22% opacity"
    placement: "corner opposite the sun-bloom"
    description: "Subordinate counter-temperature balance; never dominant."
  block-tile:
    backgroundColor: "{colors.sun} at 40–70% opacity"
    layout: "rectangles on an 8×4 grid behind cover/colophon"
    description: "A layered poster underprint."
  yellow-panel:
    backgroundColor: "{colors.sun}"
    textColor: "{colors.ink}"
    rounded: "0"
    border: "none (meets paper directly)"
    description: "Full-bleed column/third — the strongest color statement, ink on top."
  hairline-rule:
    rule: "1px solid {colors.ink} (soft variant: {colors.ink} at 18–20%)"
    description: "The ONLY border — header underlines, footer tops, ledger separators. No thicker rule exists."
  strand-row:
    borderBottom: "1px {colors.ink} 18–20%"
    typography: "{typography.strand-title} + {typography.body}"
    description: "Serif numeral + serif title + sans body. Numbered editorial lists."
  ledger-row:
    borderBottom: "1px {colors.ink} 18–20%"
    typography: "{typography.mono-date} · {typography.ledger-title} · {typography.body} · {typography.mono-data}"
    description: "4-col tabular — mono date · serif title · sans venue · mono duration (right)."
  footer-band:
    borderTop: "1px solid {colors.ink} per cell"
    typography: "{typography.micro-label} + {typography.body-sm}"
    description: "4-column metadata strip at the foot of cover/colophon."
  vertical-rail:
    typography: "{typography.rail-label}"
    transform: "rotated up the left edge"
    description: "Section marker on chapter/divider frames."
  pagenum:
    typography: "{typography.pagenum}"
    color: "{colors.ink} at 75%"
    placement: "bottom-right"
    description: "The only persistent chrome."
---

# Biennale Yellow — 帧（视频 / 帧层）

## 概述

帧尺度的 Biennale Yellow 是一个**文学编辑系统**，风格如艺术双年展目录：暖羊皮纸、单一深靛蓝油墨、太阳黄作为氛围。没有卡片、没有按钮、没有阴影、没有圆角——结构词汇只是**纸、墨和黄色。** 深度由柔和径向**太阳光晕**传达，而非抬升。

声音是三个严格角色的面孔：**Instrument Serif**（字重 400，紧行高，负字距）承载所有展示、数字和引用（40px 到 720px+）；**Archivo** 承载正文和大写追踪的微标签；**JetBrains Mono** 承载所有日期、数字和页码。文字**始终是墨水色**——对比来自大小和字重，而非颜色。情绪介于折页博物馆手册和慢读文学季刊之间：自信、氛围感、深度克制。

**帧尺度的关键特征：**

- **暖羊皮纸底色**在每一帧上；从不白色，从不灰色。
- **单一墨水色**（`{colors.ink}`）用于所有文字和所有标尺；**太阳黄**作为光晕/面板/瓷砖。
- **Instrument Serif 400** 展示（紧，负字距）；**Archivo** 正文 + 微标签；**JetBrains Mono** 数据。
- **1px 发丝线**是唯一边框——不存在更粗的字重；**无阴影，无圆角**。
- **太阳光晕**是每帧的主要深度层；余烬反向光晕增加了暖冷张力。
- **编辑克制**——稀疏读起来优雅；拥挤破坏目录感。

## 帧

### 帧工艺检查

三个目测测试在任何结构检查之前检查每一帧：

- **眯眼** — 一个 Instrument Serif 元素以 3-6 倍于其邻居的效果主导；太阳光晕聚焦视线。
- **静默** — 帧读起来 **55-60% 为空**；**分类账是唯一密集例外**（通过安静发丝线重复实现密度，而非丰富性）。
- **克制** — **一种墨水色**用于所有文字和标尺；每帧**一个太阳光晕**（+ 可选从属余烬）；绝不自相矛盾（没有墨水色上的黄色文字）。
- **参考** — 目标是**艺术双年展目录 / 慢展览海报 / 文学季刊**；失败看起来像**平面 CMS 模板**（无光晕）或**带边框的卡片组**。

- **主要：** 1920×1080 (16:9)。展示尺寸以 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖版：** 1080×1920 (9:16)。**方形：** 1080×1080 (1:1)。
- **安全区域：** `pad-edge` 4cqw（等效 40-76px）——优雅依赖于边缘负空间；只有光晕、瓷砖和面板可出血。

**容器定律（承重）。** 每个帧底色设置 `container-type: size`；所有
帧相对单位都是针对它的 `cqw`/`cqh`——从不用 `vw`。发丝线保持 1px；光晕大小以帧的 `%` 缩放。

## 颜色

令牌与源相同。`{colors.paper}` 是通用底色；`{colors.ink}`（深
靛蓝海军蓝）是**每一行文字和每一条标尺**——没有次要文字颜色。
`{colors.sun}` 有三种部署方式：**光晕**（径向氛围）、**黄面板**
（全出血海报填充，墨水色在顶部）和 **block-tile** 底色。`{colors.sun-soft}`/`haze`
是光晕中间/外部梯度。`{colors.ember}` **仅**作为 15-22% 的反向光晕出现——从不是
填充，从不是文字。**系统从不自相矛盾**——太阳上的墨水色是正确的；黄色文字在墨水色上不存在。

## 排版

两个坡道。**阅读/数据坡道**（Archivo 正文 0.85cqw 墨水色，微标签用 px，JetBrains Mono
数据）承载文案 + 铬色；**展示坡道**（Instrument Serif `ledger-title` 1.55cqw →
`numeral-jumbo` 28cqw）承载所有标题、数字和引用。

- **可读性下限：** 任何承重行 ≥ **1.4cqw**；px 单位的等宽/标签仅为铬色。
- **适应测量：** 根据标题长度调整大小。将块限制在 **≤ 78cqw**；≤3 词 → `display`；4-6 → `headline`；7+ → `headline-sm`。巨型数字是分隔的全部意义——不要缩小它。
- **Instrument Serif 仅为字重 400**（其对比度就是字重信号），紧行高（0.84-1.06），负字距；**微标签大写 Archivo 600，≥0.16em**；**所有数字/日期用等宽**。无粗体衬线，无第二文字颜色，正文/展示中无等宽。

## 深度与表面

氛围式，而非结构式。深度来自：

- **太阳光晕** — 主层：分层径向（太阳 70-95% 核心 → sun-soft → haze 18-22% → paper 0%），帧的 42-70%。每帧一个。
- **余烬光晕** — 对面角落的 15-22% 桃色反向光晕；始终从属。
- **Block-tile 底色** — 8×4 网格上的半透明黄色矩形（封面/版权页）。
- **黄面板** — 唯一"硬"颜色声明：充满的列/三分之一，墨水色在顶部。
- **发丝线标尺** — 1px 墨水色用于结构分隔（密集行的柔和 18-20% 变体）。

**上限：** 零 box-shadow，零 text-shadow，零圆角，无边框粗于 1px。

## 形状

- **所有内容 0 圆角** — 严格矩形。光晕无边缘（它们淡入纸张）。

## 组件

- **sun-bloom / ember-bloom / block-tile** — 氛围深度集。**yellow-panel** — 海报填充声明。
- **hairline-rule** — 唯一边框（1px 墨水色；密集行的柔和变体）。
- **strand-row / ledger-row / footer-band** — 编辑列表、表格日历和元数据条。
- **vertical-rail** — 旋转的章节标记。**pagenum** — 右下角等宽铬色。

## 帧处理

> 配方：背景 · 容器 · 组成 · 焦点 · 铬色 · 强调 · 静默 · 固定/自由 · 密度。
> 每帧一个太阳光晕 + 右下角页码；稀疏是默认设置。

### 1 · 封面（标识 · 动作：展示 + 太阳光晕 · 左）

**背景** 纸 + 一个大太阳光晕（中心偏左）+ 一个余烬反向光晕（对角）。
**组成** 微标签、展示、日期轨、页脚带、页码。**焦点** 墨水色中 2 行 Instrument
Serif `display`（斜体关键词），左对齐，在微标签下方。**铬色** 右上角衬线日期轨；
底部 4 列页脚带。**强调** 太阳光晕 + 黄色。**静默** 光晕占据空白空间。**固定** 墨水色文字、一个光晕、1px 页脚规则、无阴影。**自由**
标题、日期、页脚单元格。**密度** 低。

### 2 · 章节分隔（章节 · 动作：巨型数字 · 垂直轨）

**背景** 纸 + 角落锚定的太阳光晕。**组成** 垂直轨、巨型数字、
特小标题。**焦点** 单个巨大的 Instrument Serif `numeral-jumbo`（≈28cqw）主导，下方带有
衬线标题。**铬色** 沿左边缘旋转的垂直轨标签；页码。**强调**
数字背后的光晕。**静默** ~60%。**固定** 衬线 400、巨型数字、轨标签。
**自由** 序数、标题、轨文字。**密度** 低。

### 3 · 分类账（目录 · 动作：发丝线表格行 · 密集帧）

**背景** 纸（光晕可选，微妙）。**组成** 特小标题 + 微标签顶部栏、分类账行。
**焦点** 一个 4 列表格日历 — 等宽日期 · 衬线标题 · 无衬场地 · 等宽时长 —
由发丝线柔和规则分隔，上方为 1px 墨水色标题规则。**铬色** 页码。**强调** 无 —
通过安静重复实现密度，而非颜色。**静默** 紧 — 密度例外（通过
重复实现，而非丰富性）。**固定** 发丝线规则、等宽日期、衬线标题。**自由** 行、场地。
**密度** 密集例外。

### 4 · 宣言/引用（引用 · 动作：斜体衬线 · 居中光晕）

**背景** 纸 + 居中太阳光晕。**组成** 大号数字引用标记、展示斜体、署名。
**焦点** 墨水色中 2 行 Instrument Serif **斜体** `display-it` 引用，居中，位于
超大衬线引用标记下方。**铬色** 微标签署名。**强调** 居中光晕。
**静默** ~60% — 故意开放。**固定** 斜体衬线、一个光晕、墨水色。**自由** 引用、
署名。**密度** 低。

### 5 · 海报面板（声明 · 动作：黄色面板 · 分割）

**背景** 纸，带全出血 `{colors.sun}` `yellow-panel`（列或三分之一）。**组成**
黄色面板、微标签、标题。**焦点** Instrument Serif `headline` 墨水色放置在**太阳面板上**
（墨水色在黄色上 — 标志性）。**铬色** 微标签；页码。**强调** 面板
本身。**静默** 纸张侧保持开放。**固定** 墨水色在太阳上、面板直接接触纸（无
边框）、无阴影。**自由** 标题、面板侧/宽度。**密度** 低。

### 6 · 串行列表（节目 · 动作：编号编辑行 · 左）

**背景** 纸 + 微妙太阳光晕。**组成** 微标签、特小标题、串行行。**焦点**
编号列表 — 衬线数字 + 衬线标题 + 无衬正文、发丝线柔和分隔符。**铬色**
微标签；页码。**强调** 光晕。**静默** 中等；行有呼吸空间。**固定** 衬线
数字、发丝线柔和规则。**自由** 项目、文案。**密度** 标准。

## 构图规则

### 该做

- 从**暖羊皮纸**开始；添加**一个太阳光晕**（可选余烬反向光晕）— 氛围即深度。
- 每一行使用**墨水色**；展示使用 **Instrument Serif 400**（紧、负字距），**Archivo** 正文，所有数字/日期使用 **JetBrains Mono**。
- 每个分隔符使用 **1px 墨水色发丝线**（密集行用柔和变体）；海报时刻使用**黄色面板**（墨水色在上）。
- 微标签保持**大写 Archivo 600, 0.16–0.32em**；**页码**固定在右下角。
- 倾向稀疏；封面/章节/列表左对齐/不对称，宣言居中。

### 不该做

- 无投影、无圆角、无带边框卡片、无边框粗于 1px。
- 无第二种文字颜色；无粗体 Instrument Serif；无反转墨水色背景。
- 正文/展示无等宽；无字体替代。
- 不要拥挤画布 — 稀疏读起来优雅；不要省略光晕（平面羊皮纸读起来像 CMS 模板）。
- 不要将标题扩展到边缘 — 降低坡道等级。

## 宽高比行为

| 处理            | 16:9                                         | 9:16                      | 1:1                       |
| --------------- | -------------------------------------------- | ------------------------- | ------------------------- |
| 封面            | 展示左、日期轨右上、页脚底部                    | 展示顶、页脚堆叠            | 展示上、页脚底部           |
| 章节分隔        | 巨型数字、轨左                                | 数字居中、轨顶             | 数字居中                  |
| 分类账          | 4 列行                                       | 丢弃场地列→3列            | 3列                       |
| 宣言            | 居中斜体                                      | 居中、更高                | 居中                      |
| 海报面板        | 侧面板 + 纸                                   | 顶/底面板带               | 面板三分之一               |
| 串行列表        | 编号行                                        | 行（更紧）                | 行                        |

`pad-edge` 在短边上保持；展示钳制使用较短的轴，因此竖屏不会使标题过度膨胀。保持承重行 ≥ 1.4cqw。分类账/串行固定的首列在 9:16 上可能会收紧。

## 已批准实体

源中未定义真实客户、标识或供应商 — 将任何此类标记渲染为占位符。节目名称、场地和日期是内容；系统提供纸、墨水、黄色。

## 数字与声明（硬性规则）

在帧尺度上永远不要发明数字、日期、时长或计数。将插槽渲染为 `— figure —`、`{metric}`、`NN JUN`、`N m`。分类账日期/时长和图表值尤其带有占位符，直到脚本提供它们。章节序数（01, 02…）是装饰性的。

## 渲染前自查

- **眯眼** — 一个衬线展示时刻主导；光晕聚焦视线。
- **静默** — 稀疏帧 55-60% 开放；只有分类账运行密集（通过重复，而非丰富性）。
- **一种颜色** — 墨水色用于所有文字 + 规则；太阳用于光晕/面板/瓷砖；仅余烬反向光晕；无反色。
- **类型** — Instrument Serif 400 紧负字距、适应测量；微标签大写 0.16em+；等宽数字；≥1.4cqw 下限。
- **深度** — 0 阴影、0 圆角、仅 1px 发丝线；存在一个太阳光晕。
- **锚定** — 封面/章节/列表左对齐、宣言居中；页码右下角。
- **制作** — 每个数字/日期追踪到脚本，否则为占位符。

## 已知差距

- **运动有意不在此范围。** frame.md 仅指定构图；源的 280ms 交叉淡入淡出是幻灯片机制。
- **Instrument Serif + Archivo + JetBrains Mono 通过 Google Fonts。** CJK：Smiley Sans（展示）/ Noto Serif SC（正文）/ Noto Sans SC（标签）；斜体衬线和等宽表格数字没有精确的汉字对应 — 保持分类账日期为拉丁文。
- **9:16 / 1:1 为指导性**；`min(vw,vh)` 钳制模式防止展示过度膨胀 — 按比例验证。
- 太阳/余烬光晕、block 瓷砖、黄色面板和发丝线规则仅 CSS；无需外部图片。
