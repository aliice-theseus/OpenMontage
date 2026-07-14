---
version: alpha
name: Daisy Days — Frame (video / frame layer)
description: >
  Daisy Days 的 design.md 的视频优先伴侣。单位是帧 (1920×1080)。原子
  相同且神圣 — 阳光花园粉彩调色板（奶油 + 蓝绿/粉/黄油/薄荷/
  薰衣草/桃/天蓝 + 珊瑚强调）、炭笔 3px 轮廓、硬偏移阴影（6/4px、无模糊）、
  Fredoka + Quicksand 搭配、大圆角、颜色上的标题文字阴影、点项目符号和
  手绘 SVG 装饰层。构图 + 帧比例已重写。运动不在此范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#F5F0E6"
  turquoise: "#7ECDC0"
  soft-pink: "#F7C8D4"
  butter: "#FDE68A"
  mint: "#A8E6CF"
  lavender: "#D4A5E8"
  peach: "#FFCBA4"
  sky: "#A8D8F0"
  coral: "#F8635F"
  text-dark: "#2D2D2D"
  text-muted: "#6B6B6B"
  white: "#FFFFFF"

borders: { primary: "3px solid text-dark", thin: "2px solid text-dark" }
shadows: { default: "6px 6px 0 text-dark", small: "4px 4px 0 text-dark", text-headline: "3px 3px 0 text-dark", text-headline-soft: "3px 3px 0 rgba(0,0,0,0.2)" }

typography:
  # — reading ramp (Quicksand) —
  body:    { fontFamily: "Quicksand", cqw: 0.95, weight: 500, lineHeight: 1.6 }
  body-strong:{ fontFamily: "Quicksand", cqw: 0.95, weight: 600, lineHeight: 1.5 }
  meta:    { fontFamily: "Quicksand", cqw: 0.78, weight: 600, lineHeight: 1.45 }
  # — display ramp (Fredoka One / Fredoka 600 — single weight, never italic) —
  badge:   { fontFamily: "Fredoka One", cqw: 0.9, tracking: "0.02em" }
  label-display:{ fontFamily: "Fredoka One", cqw: 1.3, lineHeight: 1.3, tracking: "0.02em" }
  subtitle:{ fontFamily: "Fredoka One", cqw: 1.8, lineHeight: 1.2, tracking: "0.02em" }
  quote:   { fontFamily: "Fredoka One", cqw: 2.6, lineHeight: 1.35 }
  title:   { fontFamily: "Fredoka One", cqw: 3.0, lineHeight: 1.15, tracking: "0.02em" }
  headline:{ fontFamily: "Fredoka One", cqw: 4.5, lineHeight: 1.1, tracking: "0.02em" }
  display: { fontFamily: "Fredoka One", cqw: 6.5, lineHeight: 1.1, tracking: "0.02em" }

spacing:
  pad-slide: "3cqw"
  radius: "20px"
  radius-lg: "28px"
  radius-pill: "50px"
  radius-round: "50%"

components:
  card:
    backgroundColor: "{colors.white}"
    border: "3px solid {colors.text-dark}"
    rounded: "{spacing.radius} (28px featured)"
    shadow: "6px 6px 0 {colors.text-dark}"
    description: "The universal container; white-on-pastel is standard."
  framed-header:
    backgroundColor: "pastel cap + {colors.white} body"
    border: "3px solid {colors.text-dark} (one continuous)"
    rounded: "{spacing.radius-lg}"
    shadow: "6px 6px 0 {colors.text-dark}"
    description: "Pastel header strip flush above a white body — one unit, one shadow."
  badge-pill:
    backgroundColor: "{colors.butter}"
    border: "3px solid {colors.text-dark}"
    rounded: "{spacing.radius-pill}"
    typography: "{typography.badge}"
    shadow: "4px 4px 0 {colors.text-dark}"
    description: "Section tag. white-space:nowrap."
  circle-marker:
    backgroundColor: "any pastel"
    textColor: "{colors.white} (dark on butter)"
    border: "3px solid {colors.text-dark}"
    rounded: "50%"
    size: "bullet 20 / icon 44 / dot 48 / step 90"
    typography: "Fredoka numeral"
    description: "Steps carry a small shadow."
  bullet-dot:
    backgroundColor: "{colors.butter}"
    border: "2px solid {colors.text-dark}"
    rounded: "50%"
    size: "20px (::before, 4px from line top)"
    description: "Lists never use glyph bullets."
  ornament:
    type: "hand-drawn SVG (daisy, star, sun, cloud, rainbow)"
    stroke: "2.1px {colors.text-dark}"
    placement: "z-index:1 behind content (z-index:2), cropping past the frame edge"
    description: "3–7 per frame, clustered at corners/edges."
  quote-mark:
    typography: "oversized Fredoka quote glyph"
    color: "{colors.soft-pink} (charcoal stroke)"
    description: "Above a quote body."
  text-headline-shadow:
    shadow: "3px 3px 0 {colors.text-dark} (soft 20% variant on pink/mint)"
    appliesTo: "Fredoka headlines on saturated surfaces (cream headlines sit flat)"
    description: "Makes the headline read 'outlined' like the shapes."
---

# Daisy Days — 帧（视频 / 帧层）

## 概述

帧尺度下的 Daisy Days 是一个**快乐、童真的系统** — 图画书插画遇上贴纸 kawaii。每个形状都带有**3px 炭笔轮廓**、每个抬升元素都带有**实色硬偏移阴影**（无模糊）、每个表面都是阳光花园粉彩。声音是一个搭配：**Fredoka One**（粗圆、单一字重）用于每个标题、**Quicksand** 用于每个正文和元行。标志是**手绘 SVG 装饰层** — 雏菊、星星、太阳、云、彩虹聚集在角落并裁剪出边缘。

The palette is **multi-pastel with one warm pop**: cream canvas, seven pastel surfaces, and
`{colors.coral}` reserved for small high-attention markers only. Headlines on a saturated surface
get a 3px charcoal text-shadow (so they read "outlined" like the shapes) and switch to white;
headlines on cream sit flat in charcoal. Depth is 2D and graphic — thick outline + hard offset =
sticker-on-paper.

**帧尺度的关键特征：**

- **奶油默认 + 旋转粉彩表面**；`{colors.coral}` 是标记强调色，从不作为表面。
- **Fredoka One** 标题 + **Quicksand 500/600** 正文 — 严格按角色，从不混用。
- **3px 炭笔轮廓 + 硬偏移阴影**（6/4px，零模糊）在每个抬升形状上。
- **大方的圆角** — 20px 卡片、28px 特色、药丸徽章、圆形标记；无方角。
- **饱和表面上的标题文字阴影**（白色文字）；奶油上平贴炭笔色。
- **圆点项目符号**（描边奶油圆盘，从不使用字符）+ 每帧一个 **3–7 个装饰花环**。

## 帧

### 帧工艺条

三项目测检查在任何结构检查前把关每帧：

- **眯眼测试** — 一个 Fredoka 标题或内容卡片以 3–6 倍于其邻元素占主导。
- **留白测试** — **每帧一个内容容器**，被装饰花环包围；**信息卡片网格是唯一密集的例外**。空角落看起来不完整。
- **克制测试** — 奶油或**一种**粉彩表面；coral 是小标记强调色（从不作为表面）；仅炭笔边框 + 硬偏移阴影；无第九种颜色。
- **参照测试** — 瞄准**儿童画本 / 贴纸 kawaii 杂志**；失败看起来像**平面、方角、模糊阴影的企业幻灯片**。

- **主尺寸：** 1920×1080 (16:9)。展示以 **`cqw`** 为单位编写（`px ÷ 1920 × 100 = cqw`）。
- **竖版：** 1080×1920 (9:16)。**方版：** 1080×1080 (1:1)。
- **安全区域：** `pad-slide` ~3cqw；装饰元素故意出血边缘。

**容器法则（承重规则）。** 每个帧背景设置 `container-type: size`；所有帧相对单位都是 `cqw`/`cqh` 以它为基准 — 从不用 `vw`。边框保持 3px/2px；圆角保持 20/28/50px；阴影偏移量以 `cqw` 为单位从而保持贴纸偏移的比例。

## 颜色

色值令牌与源文件一致。默认背景 `{colors.cream}`；旋转饱和粉彩（蓝绿 / 柔粉 / 奶油 / 薄荷 / 紫芙 / 桃 / 天蓝）获取色调情感。**卡片在任何表面上都是白色**。**边框 + 阴影始终是 `{colors.text-dark}` 炭笔色** — 从不彩色、从不模糊、从不用 `rgba`（除了柔和文字阴影变体）。`{colors.coral}` 是唯一的高饱和强调色 — 仅用于小标记（步骤圆圈、圆点、标题），从不作为表面。正文为炭笔色/低饱和；粉彩色承载**无语义含义**。无第九种颜色。

## 排版

两个阶梯。**阅读阶梯**（Quicksand 500 正文 0.95cqw、600 强调、元数据）承载文案；**展示阶梯**（Fredoka One `label-display` 1.3cqw → `display` 6.5cqw，单一字重）承载每个标题、标题、引用和标记数字。

- **可读性底线：** 任何承重行 ≥ **1.4cqw**；元数据仅为铬色。
- **按篇幅调整：** 根据标题的长度调整字号。将标题块限制在 **≤ 78cqw**；≤3 词 → `display`；4–6 → `headline`；7+ → `title`。
- **Fredoka One 用于所有展示，Quicksand 用于所有正文 — 从不混用。** Fredoka 是单一字重（无斜体、无下划线、无替代字重）；Quicksand 保持 500/600/700。Fredoka 字距 0.02em；Quicksand 正文从不大写。

## 深度与表面

2D 图形深度 — 硬偏移阴影、实心炭笔色、零模糊、右下角：

- **`shadows.default` 6px** 卡片、框架、徽章、图表容器。
- **`shadows.small` 4px** 小卡片、步骤圆圈、头像。
- **文字标题阴影** — 饱和表面上的 Fredoka 标题上 3px 炭笔阴影（20% 柔和变体在粉色/薄荷上）；奶油标题平贴。
- **轮廓 + 偏移** 共同构成贴纸在纸上的标志性效果。

**天花板规则：** 无模糊阴影、无 `rgba`（除了柔和文字阴影）、无渐变、无发光；元素要么投射硬炭笔偏移，要么无阴影。

## 形状

- **20px** 卡片、**28px** 特色、**50px** 药丸（徽章、计数器）、**50%** 所有圆形、**4px** 图例色块。零方角 — 每个区域都是圆角的。

## 组件

- **card / framed-header** — 白色填充的带边框容器（一个阴影）。**badge-pill** — 奶油色节目标签。
- **circle-marker** 家族（bullet 20 / icon 44 / dot 48 / step 90）+ **bullet-dot** — 描边粉彩圆盘，Fredoka 数字。
- **ornament** — 手绘 SVG 贴纸层（3–7 个每帧）。**quote-mark** — 柔粉色 Fredoka 锚点。**text-headline-shadow** — 在色标题处理。

## 帧处理方案

> 配方：背景 · 容器 · 组成 · 焦点 · 铬色 · 强调 · 留白 · 固定/自由 · 密度。
> 每帧一个内容容器 + 3–7 个装饰花环；空角落视为不完整。

### 1 · 封面（标识 · 动势：装饰花环 · 饱和 · 居中）

**背景** 饱和粉彩（如 `{colors.turquoise}`）。**组成** badge-pill、display、body sub、3–7 ornaments、counter。**焦点** 1–2 行 Fredoka `display`，**白色带 3px 炭笔文字阴影**，居中，在奶油 badge-pill 之下。**铬色** counter 药丸。**强调** 装饰花环（角落的雏菊 + 星星，裁剪出边缘）。**留白** 内容居中；装饰元素填满边缘。**固定** 饱和上文字阴影、3px 轮廓、炭笔阴影。**自由** 表面颜色、装饰元素组合/位置、文案。**密度** 丰满但不拥挤。

### 2 · 信息卡片（目录 · 动势：3列白卡 · 奶油 · 密集帧）

**背景** `{colors.cream}`，`pad-slide`。**组成** headline（平贴炭笔色）、3× card（圆形图标 + Fredoka 标题 + Quicksand 正文），几个装饰元素。**焦点** 三个白色 3px 边框卡片，带 6px 阴影。**铬色** 平贴标题。**强调** 粉彩圆形图标（旋转蓝绿/coral/紫芙）。**留白** 紧凑 — 密度例外（此处装饰元素较少）。**固定** 白色卡片、3px + 6px、20px 圆角。**自由** 卡片内容、图标色调。**密度** 密集例外。

### 3 · 流程步骤（序列 · 动势：旋转圆形标记 · 桃色 · 居中）

**背景** `{colors.peach}`（或其他粉彩）。**组成** headline（白色 + 文字阴影）、3–4 个步骤圆圈 + `→` 箭头、装饰元素。**焦点** 一行 90px 描边步骤圆圈，填充**旋转 coral → mint → sky → lavender**，Fredoka 白色数字，由 Fredoka 箭头连接。**铬色** 白色标题带文字阴影。**强调** 旋转圆圈填充。**留白** 适中。**固定** 3px 圆圈 + 小阴影、旋转填充、箭头字形。**自由** 步骤数、标签。**密度** 标准。

### 4 · 引用（引用 · 动势：引用标记锚点 · 柔粉 · 居中）

**背景** `{colors.soft-pink}`。**组成** 白色引用卡片（28px 圆角、6px 阴影）、quote-mark、Fredoka 引用、Quicksand 署名、装饰元素。**焦点** 白色卡片内的 Fredoka `quote` 炭笔色，在超大柔粉 quote-mark 之下。**铬色** Quicksand 700 署名。**强调** quote-mark + 一两颗星星。**留白** 卡片居中，装饰元素在角落。**固定** quote-mark 锚点、白色卡片。**自由** 引用、署名。**密度** 适中。

### 5 · 框架节（特色 · 动势：帽体+正文卡片 · 奶油）

**背景** `{colors.cream}`。**组成** framed-header（粉彩帽体 + 白色正文）、bullet-dot 列表、装饰元素。**焦点** 框架标题 — 粉彩帽体条（Fredoka 标题，可选文字阴影）在白色正文之上，带奶油点项目符号列表。**强调** 帽体颜色 + bullet dots。**留白** 适中。**固定** 一个连续 3px 边框 + 一个阴影、奶油点项目符号。**自由** 帽体颜色、列表。**密度** 标准。

### 6 · 结束（收尾 · 动势：装饰花环 · 饱和 · 居中）

**背景** 饱和粉彩（如 `{colors.lavender}`）。**组成** badge-pill、display（白色 + 文字阴影）、3–7 个装饰元素。**焦点** 白色 Fredoka `display` 结尾语，带炭笔文字阴影，居中。**强调** 装饰花环。**留白** 内容居中。**固定** 饱和上文字阴影，装饰元素填满角落。**自由** 结尾语、表面、装饰元素。**密度** 丰满。

## 构图规则

### 应做

- 严格按角色搭配 **Fredoka One 标题 + Quicksand 正文**。
- 每个形状描边 **3px 炭笔 + 硬偏移阴影**（6/4px，无模糊）；白色卡片在任何表面上填充。
- 给饱和表面上的 Fredoka 标题加上 **3px 炭笔文字阴影 + 白色文字**；奶油上平贴炭笔色。
- 使用 **描边奶油圆盘项目符号**（从不使用字符）；每帧聚集 **3–7 个手绘装饰元素**（角落，裁剪出边缘）。
- 保持 **每帧一个内容容器**；旋转标记颜色（coral → mint → sky → lavender → butter）；coral 仅用于小标记。
- 大部分帧居中；内容密集帧偏向奶油，封面/结束/引用偏向饱和。

### 避免

- 无方角；无模糊或 `rgba` 阴影（除柔和文字阴影外）。
- 无彩色边框（仅炭笔色）；无 coral 表面；无第九种颜色。
- 无第三种字体；无 Quicksand 标题或 Fredoka 正文；无斜体/下划线 Fredoka；无大写 Quicksand 正文。
- 无字符项目符号；无空角落（装饰元素填充它们）；无两个竞争的内容面板。
- 不要让标题撑满到边缘 — 按篇幅调整。

## 宽高比行为

| 处理方案      | 16:9                       | 9:16                             | 1:1        |
| -------------- | -------------------------- | -------------------------------- | ---------- |
| 封面          | 居中，角落装饰 | 居中加高，更多装饰 | 居中   |
| 信息卡片     | 3 列并排                   | 堆叠                          | 2+1        |
| 流程步骤  | 水平 + 箭头        | 垂直，箭头旋转向下     | 2×2        |
| 引用          | 居中卡片              | 居中加高                 | 居中   |
| 框架节 | 帽体 + 正文                 | 帽体 + 正文加高                | 帽体 + 正文 |
| 结束        | 居中，花环           | 居中，花环                 | 居中   |

`pad-slide` 在短边上保持；将展示字号调整在 1.4cqw 底线之上。在更紧凑的比例下，保持装饰元素数量较高（5–7），以便角落从不看起来空白。

## 批准的真实实体

源文件中未定义真实客户、标志或供应商 — 任何此类标记均渲染为占位符。装饰元素和粉彩色与内容无关；计数器/徽章承载每套占卡的文本。

## 数字与断言（硬性规则）

绝不在帧尺度上编造数字、日期或计数。将插槽渲染为 `— figure —`、`{metric}`、`N`。步骤号和图表值均使用占位符，直到脚本提供；幻灯片计数器是装饰性铬色。

## 渲染前自查

- **眯眼测试** — 每帧一个 Fredoka 标题或内容卡片占主导。
- **留白测试** — 每帧一个容器，被装饰花环包围；仅信息卡片网格运行密集。
- **颜色** — 奶油或一种粉彩表面；coral 标记仅用；炭笔边框/阴影；无第九色调。
- **字体** — Fredoka 标题（饱和上文字阴影 + 白色，奶油上平贴炭笔色），Quicksand 正文；≥1.4cqw 底线。
- **深度** — 3px 轮廓 + 硬偏移（无模糊，无 rgba 除柔和文字阴影）；仅圆角。
- **装饰元素** — 3–7 个每帧，裁剪出边缘；无空角落。**项目符号** — 描边圆盘，从不使用字符。
- **虚构** — 每个数字来源于脚本，否则为占位符。

## 已知差距

- **运动设计有意不在范围之内。** frame.md 仅指定构图；源文件使用 scroll-snap 导航，无过渡规范。
- **字体：** 源文件命名为 _Fredoka One_；Google 现在提供 **Fredoka** 变量家族 — 请求 `Fredoka:wght@500;600;700` 并设置展示字重为 600（视觉上等同于 Fredoka One），`Fredoka One` 保持在堆栈的第一位以兼容仍提供它的环境。Quicksand 正常加载。CJK：ZCOOL XiaoWei（展示）/ Yozai（正文）。
- **9:16 / 1:1 为指导性**；保持装饰元素数量较高以便角落按比例始终被填满。
- 装饰元素（雏菊/星星/太阳/云/彩虹）、标记和框架标题为纯 CSS/SVG；重新上色 SVG 装饰元素需要编辑其描边值。
- **对比度：** 保持 `{colors.text-muted}` 不要出现在粉彩表面上（仅奶油/白色卡片）；饱和背景上的小字应为炭笔色或白色。
