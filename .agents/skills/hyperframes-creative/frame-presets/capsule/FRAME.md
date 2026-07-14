---
version: alpha
name: Capsule — Frame (video / frame layer)
description: >
  Capsule 的 design.md 的视频优先伴侣。单位是帧 (1920×1080)。原子
  相同且神圣 — 药丸几何 (小 9999px / 卡片 2rem) 带 2px 墨水色轮廓在
  所有内容上、日晒奶油画布、九色糖果调色板、Bodoni Moda + Space
  Grotesk、柔和硬偏移阴影 (4/6/8/12px 在 8% 墨水色中)、浮动装饰性药丸壁纸、
  径向强调光晕和颗粒叠加。构图 + 帧比例已重写。运动不在此范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#F5F5F0"
  ink: "#1A1A1A"
  outline: "#1E1E1E"
  white: "#FFFFFF"
  coral: "#E85D4E"
  lime: "#C4D94E"
  lavender: "#C5B5E0"
  sky: "#8BB4F7"
  violet: "#A06CE8"
  yellow: "#F2D160"
  peach: "#F5B895"
  mint: "#A8E6CF"
  shadow: "rgba(26,26,26,0.08)"

typography:
  # — reading ramp (Space Grotesk) —
  body:      { fontFamily: "Space Grotesk", cqw: 0.85, weight: 400, lineHeight: 1.6 }
  subtitle:  { fontFamily: "Space Grotesk", cqw: 0.95, weight: 400, tracking: "0.18em", upper: true }
  pill-text: { fontFamily: "Space Grotesk", cqw: 0.75, weight: 600, tracking: "0.12em", upper: true }
  label:     { fontFamily: "Space Grotesk", px: 14, weight: 500, tracking: "0.1em", upper: true }
  # — display / hero ramp (Bodoni Moda, ink, sentence case) —
  card-headline:{ fontFamily: "Bodoni Moda", cqw: 1.9, weight: 700, lineHeight: 1.1 }
  orbit-numeral:{ fontFamily: "Bodoni Moda", cqw: 2.6, weight: 700, lineHeight: 1.0 }
  quote-display:{ fontFamily: "Bodoni Moda", cqw: 4.2, weight: 600, lineHeight: 1.3, tracking: "-0.01em" }
  stat-number: { fontFamily: "Bodoni Moda", cqw: 3.6, weight: 800, lineHeight: 1.0, tracking: "-0.03em" }
  section-headline:{ fontFamily: "Bodoni Moda", cqw: 4.0, weight: 700, lineHeight: 1.05, tracking: "-0.01em" }
  headline:    { fontFamily: "Bodoni Moda", cqw: 5.0, weight: 700, lineHeight: 1.05, tracking: "-0.02em" }
  closing-display:{ fontFamily: "Bodoni Moda", cqw: 8.5, weight: 800, lineHeight: 0.95, tracking: "-0.03em" }
  display:     { fontFamily: "Bodoni Moda", cqw: 12.0, weight: 800, lineHeight: 0.88, tracking: "-0.03em" }

spacing:
  pad: "5cqw"
  gap-md: "2cqw"
  card-pad: "2cqw 1.6cqw"

components:
  pill:
    rounded: "9999px (small) / 2rem (cards)"
    border: "0.2cqw solid {colors.outline}"
    backgroundColor: "any candy or {colors.white}"
    description: "通用容器——每个芯片/按钮/标签/统计块/节点/条。不存在无描边的药丸。"
  pill-card:
    backgroundColor: "{colors.white}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "2rem"
    shadow: "0.4cqw 0.4cqw 0 {colors.shadow}"
    typography: "{typography.card-headline} + {typography.body}"
    description: "容纳圆形卡片图标、Bodoni 标题、Space Grotesk 正文。"
  stat-pill:
    backgroundColor: "{colors.white}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "2rem"
    shadow: "0.3cqw 0.3cqw 0 {colors.shadow}"
    typography: "{typography.stat-number} (COLORED) + {typography.pill-text}"
    description: "颜色接触数字的唯一位置；+ 40px 强调条。"
  title-pill:
    backgroundColor: "{colors.yellow}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    shadow: "0.3cqw 0.3cqw 0 {colors.shadow}"
    typography: "{typography.pill-text}"
    description: "位于封面/结束页的展示标题上方。"
  card-icon:
    backgroundColor: "any candy"
    border: "0.2cqw solid {colors.outline}"
    rounded: "50%"
    size: "60px"
    typography: "Bodoni numeral/letter in {colors.ink}"
    description: "卡片标记。"
  floating-pill:
    backgroundColor: "any candy"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px / 50%"
    transform: "rotate(−20°..+25°)"
    shadow: "none"
    typography: "{typography.pill-text}"
    description: "装饰性壁纸彩纸，每个声明式帧 5-8 个。平面——无阴影。"
  quote-highlight:
    backgroundColor: "{colors.lime} / {colors.sky}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    description: "内联糖果药丸包裹 Bodoni 引用中的短语——强调机制，替代粗体/斜体。"
  bar-track:
    backgroundColor: "{colors.cream}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    fill: "child candy pill, value at right edge"
    description: "36px 药丸图表轨道。"
  accent-line:
    backgroundColor: "{colors.coral}"
    rounded: "9999px"
    size: "60×4 (80×4 closing)"
    description: "珊瑚色药丸规则线。"
  atmosphere:
    background: "1–3 radial candy glows (6–15% opacity) over {colors.cream} + 4% grain overlay"
    description: "每帧的基线画布层。从不缺席。"
---

# Capsule — 帧（视频 / 帧层）

## 概述

帧尺度下的 Capsule 是一个**俏皮编辑系统，每个容器都是一个药丸。** `border-radius: 9999px`（小）/ `2rem`（卡片）规则加上 2px 墨水色轮廓包裹每个芯片、卡片、图标、条和节点——膨胀、友好、图形独特。画布是日晒奶油色，由柔和径向糖果光晕和永久 4% 颗粒叠加温暖。

声音是双面对话：**Bodoni Moda**（didone 衬线、字重 700-800、始终墨水色、始终句子大小写）承载每个标题、统计和引用；**Space Grotesk** 承载正文和所有大写追踪的药丸/标签文字。九种糖果强调色可互换填充药丸，无语义含义。深度是**柔和硬偏移阴影**（4/6/8/12px 在 8% 墨水色中）——抬升而非印章——保留给承载内容的容器；装饰性浮动药丸是平的。

**帧尺度的关键特征：**

- **药丸几何无处不在** — 小 9999px、卡片 2rem — 每个包裹在 2px `{colors.outline}` 描边中。
- **Bodoni Moda** 展示（墨水色、句子大小写）+ **Space Grotesk** 正文/药丸（大写、追踪）。
- **九种糖果强调色**、可互换；颜色接触统计数字 + 药丸填充、从不标题。
- **柔和偏移阴影**（4/6/8/12px、8% 墨水色）仅在内容容器上；浮动药丸是平的。
- **浮动装饰性药丸壁纸**（5-8 个、倾斜）+ 径向光晕 + 4% 颗粒在声明帧上。
- **奶油画布**由氛围温暖——裸露角落读起来像破损。

## 帧

### 帧工艺条

三条目测检查在任何结构检查之前把关每一帧：

- **眯眼测试** — 一个 Bodoni 标题或统计数据以 **3–6 倍于其最近邻**为主导。
- **静谧测试** — 声明式帧承载**氛围而非杂乱**（药丸作为壁纸而非内容）；**支柱卡片和统计网格是密集的例外**。
- **克制测试** — 每个药丸都有 2px 轮廓；颜色仅接触**填充 + 统计数字**（从不触及标题）；仅承载内容的药丸有柔和阴影（浮动药丸是平的）；无第十种强调色。
- **参考测试** — 瞄准**孟菲斯 / 冰淇淋店编辑版面**；失败看起来像**扁平、无贴纸的 SaaS 卡片网格**。

- **主画幅：** 1920×1080 (16:9)。展示使用 **`cqw`** (`px ÷ 1920 × 100 = cqw`) 编写。
- **竖版画幅：** 1080×1920 (9:16)。**方形画幅：** 1080×1080 (1:1)。
- **安全区域：** `pad` (5cqw)；浮动药丸可作为壁纸溢出边缘。

**容器法则（承重）。** 每个帧底设置 `container-type: size` 并承载径向光晕 + 颗粒氛围；所有帧相对单位均使用 `cqw`/`cqh` 相对于它——绝不使用 `vw`。药丸圆角保持 `9999px`/`2rem`（形状而非缩放）；阴影偏移以 `cqw` 缩放。

## 色彩

令牌与源文件一致。`{colors.cream}` 是底色；`{colors.ink}`/`{colors.outline}` 是字体 + 通用 2px 描边；九种糖果强调色填充药丸，**无语义映射**——搭配暖色（珊瑚/黄/桃）与冷色（天蓝/薰衣草/紫罗兰/薄荷）再与中性亮色（青柠）；永远不将两个同色系相邻放置。颜色出现在**统计数字和药丸填充上**——从不出现在 Bodoni 标题上。阴影始终是 `{colors.shadow}`（8% 墨水色）。无第十种颜色。

## 字体排印

两个斜坡。**阅读斜坡**（Space Grotesk 正文 0.85cqw，大写追踪的药丸/标签文字）承载文案 + 芯片；**展示斜坡**（Bodoni `card-headline` 1.9cqw → `display` 12cqw，全部 700-800）承载每个标题、统计和引用。

- **可读性底线：** 任何承重行 ≥ **1.4cqw**；px 标签仅为装饰性。
- **按文量体：** 根据长度调整标题大小。将块限制在 **≤ 78cqw**；≤3 词 → `display`/`closing-display`；4-6 词 → `headline`；7+ 词 → `section-headline`。
- **Bodoni 700+ 墨水色、句子大小写**（斜体仅通过 `<em>`，允许对斜体关键词使用糖果色）；**Space Grotesk 药丸/标签大写、0.08em+ 追踪**；负追踪 Bodoni 展示。

## 深度与表面

柔和硬偏移阴影是唯一的深度，使用 `{colors.shadow}`（8% 墨水色），右下方向：

- **0.2cqw (4px)** 小节点；**0.3cqw (6px)** 统计药丸、轨道药丸、图表节点；**0.4cqw (8px)** 支柱卡片；**0.6cqw (12px)** 视觉帧。
- **2px 轮廓**在奶油色上完成大部分抬升；阴影增添了悬浮感。
- **装饰性浮动药丸不投射阴影**——这使内容与氛围一目了然地区分开。

**天花板：** 无模糊阴影、无重新着色阴影、无渐变深度。

## 形状

- **9999px** — 所有小药丸（芯片、按钮、条、节点、浮动药丸、引用高亮、强调线）。
- **2rem** — 较大卡片（支柱卡片、统计药丸、图表容器、视觉帧）。
- **50%** — 圆形药丸（卡片图标 60px、步骤节点 56px、轨道中心 160px、导航点）。
- **0** — 仅颗粒叠加和视觉帧内的渐变区域。不存在尖角文本容器。

## 组件

- **pill** — 通用 2px 描边容器。**pill-card / stat-pill / title-pill** — 带有柔和阴影的白色/黄色内容药丸。
- **card-icon** — 圆形糖果标记；**floating-pill** — 扁平倾斜壁纸彩纸；**quote-highlight** — 内联糖果强调药丸。
- **bar-track** — 药丸形状的图表条；**accent-line** — 珊瑚色药丸规则线；**atmosphere** — 每帧的基线光晕 + 颗粒。

## 帧处理方案

> 配方：底色 · 容器 · 组成 · 焦点 · 装饰 · 强调 · 静谧 · 固定/自由 · 密度。
> 每帧都有氛围（光晕 + 颗粒）；声明式帧带有浮动药丸壁纸。

### 1 · 封面（标识 · 动态：标题药丸 + 展示 · 居中）

**底色** 奶油色 + 氛围，浮动药丸壁纸。**组成** title-pill、display、accent-line、floating-pills（5-8 个）。**焦点** 一行或两行 Bodoni `display` 标题（墨水色，斜体关键词使用糖果色），居中，位于黄色 title-pill 下方；下方为 coral accent-line。**装饰** 大写 Space Grotesk 副标题。**强调** 斜体词 + 糖果浮动药丸。**静谧** 内容居中；药丸填充边缘。**固定** 药丸轮廓、Bodoni 墨水色、扁平浮动药丸。**自由** 标题、使用哪种糖果色、药丸文字/位置。**密度** 中等氛围感。

### 2 · 支柱卡片（目录 · 动态：3 列网格 · 左对齐——密集帧）

**底色** 奶油色 + 氛围。**组成** title-pill（薰衣草色）、section-headline、3× pill-card。**焦点** 三个白色 2rem pill-card（圆形糖果 card-icon、Bodoni card-headline、Space Grotesk 正文），带有 0.4cqw 阴影，位于 Bodoni section-headline 下方。**装饰** 薰衣草色头部标签药丸。**强调** 三个 card-icon 填充（珊瑚/天蓝/青柠序列）。**静谧** 紧凑——密度例外（此处无浮动药丸）。**固定** 2px 轮廓、柔和阴影、墨水色标题。**自由** 卡片内容、图标颜色。**密度** 密集例外。

### 3 · 统计网格（数据 · 动态：统计药丸 · 居中标题）

**底色** 奶油色 + 氛围。**组成** section-headline、3-4× stat-pill。**焦点** 一行白色 stat-pill，每个包含彩色 Bodoni 统计数字 + 大写标签 + 强调条。**强调** 彩色数字 + 条（颜色接触字体的唯一位置）。**静谧** 适中。**固定** 2rem 药丸、仅彩色数字、柔和阴影。**自由** 数字（来自脚本）、颜色。**密度** 标准。

### 4 · 拉取引用（引用 · 动态：高亮药丸 · 左对齐）

**底色** 奶油色 + 氛围，少量浮动药丸。**组成** quote-display、quote-highlight、accent-line。**焦点** 一个 Bodoni 引用（墨水色），其中一个短语包裹在青柠/天蓝色 `quote-highlight` 药丸中（强调机制——从不使用粗体）。**装饰** 大写署名。**强调** 高亮药丸。**静谧** 约 50%。**固定** Bodoni 600、高亮药丸强调。**自由** 引用、高亮色/短语。**密度** 稀疏。

### 5 · 轨道（概念 · 动态：引力药丸 · 居中）

**底色** 奶油色 + 氛围。**组成** orbit-center（160px 青柠色圆形、Bodoni 序号）、4-6 个 orbit-pill 卫星（糖果色、倾斜、柔和阴影）。**焦点** 青柠色中心被轨道糖果药丸环绕。**强调** 卫星颜色。**静谧** 适中。**固定** 圆形中心、带阴影的轮廓卫星。**自由** 序号、卫星文字/位置。**密度** 中等。

### 6 · 结束页（结尾 · 动态：标题药丸 + 展示 · 居中）

**底色** 奶油色 + 氛围，浮动药丸壁纸。**组成** title-pill（黄色）、closing-display、accent-line、floating-pills。**焦点** 一个 Bodoni `closing-display` 签名（墨水色，斜体词为紫罗兰/糖果色），居中。**强调** 斜体词 + 药丸。**静谧** 内容居中。**固定** Bodoni 墨水色、扁平药丸。**自由** 签名、药丸文字。**密度** 中等氛围感。

## 构图规则

### 必须

- 让每个文本容器成为**药丸**（9999px / 2rem）并带有 **2px 墨水色轮廓**。
- 设置 **Bodoni 标题为墨水色、句子大小写**；颜色存在于统计数字 + 药丸填充上。
- 在内容容器上使用**柔和偏移阴影**（4/6/8/12px、8% 墨水色）；保持浮动药丸扁平。
- 在声明式帧上浮动 **5-8 个糖果药丸** + 径向光晕 + 颗粒；裸露的角落读起来像破损。
- 将内联强调包裹在**糖果引用高亮药丸**中，绝不使用粗体/单独斜体。
- 搭配暖色+冷色+中性亮色强调；封面/结束页偏向居中，卡片/引用偏向左。

### 禁止

- 无尖角文本容器；无无描边的药丸。
- 无彩色 Bodoni 标题；无大写 Bodoni。
- 无模糊或重新着色的阴影；无第十种强调色。
- 装饰性浮动药丸上无阴影。
- 不要将标题撑到边缘到边缘——按文量体。

## 宽高比行为

| 处理方案       | 16:9                         | 9:16                           | 1:1                     |
| ------------- | ---------------------------- | ------------------------------ | ----------------------- |
| 封面          | display 居中，药丸环绕         | display 顶部，药丸带           | 居中，药丸更少           |
| 支柱卡片      | 标题 + 3 列                  | 标题 + 3 行堆叠                | 标题 + 2+1              |
| 统计网格      | 3-4 个横向                    | 2×2                            | 2×2                     |
| 拉取引用      | 引用左对齐                     | 引用顶部，高亮内联             | 居中                     |
| 轨道          | 中心 + 4-6 个卫星              | 中心 + 3 个卫星                | 中心 + 4 个              |
| 结束页        | 居中 + 药丸                    | 居中，药丸带                   | 居中                     |

`pad` 在短边上保持；重新调整 display 使其高于 1.4cqw 底线。在较紧凑的宽高比上减少浮动药丸数量，使其保持为壁纸而非杂乱。

## 批准的实体

源文件中未定义真实客户、徽标或供应商——将任何此类标记渲染为占位符。浮动药丸文字为中性氛围词（"VISION"、"FUTURE"、"NEXT"），从不涉及特定内容。

## 数字与声明（硬性规则）

绝不在帧尺度上编造数字、统计数据或计数。将插槽渲染为 `— figure —`、`{metric}`、`N%`。统计药丸数字和条形轨道宽度在脚本提供值之前使用占位符。

## 预渲染自审

- **眯眼测试** — 一个 Bodoni 元素以 3-5 倍于其邻居的规模主导。
- **静谧测试** — 声明式帧承载氛围而非杂乱；仅支柱/统计网格密集运行。
- **药丸** — 每个容器都是一个带有 2px 轮廓的药丸；无尖锐文本容器。
- **颜色** — 糖果色用于填充 + 统计数字；标题为墨水色；无第十种色调。
- **深度** — 仅内容上有柔和偏移阴影；浮动药丸扁平；无模糊。
- **字体** — Bodoni 墨水色句子大小写、按文量体；药丸大写追踪；≥1.4cqw 底线。
- **锚定** — 封面/结束页/轨道居中，卡片/引用左对齐；不连续三个相同。
- **编造** — 每个数字追溯到脚本，否则为占位符。

## 已知差距

- **运动有意不在此范围内。** frame.md 仅指定构图；源文件中的 0.6s 淡入淡出是画板机制。
- **Bodoni Moda + Space Grotesk 通过 Google Fonts 加载。** 中日韩配对（ZCOOL XiaoWei / Yozai）从源文件延续。
- **9:16 / 1:1 为指导**；验证底线和浮动药丸数量的比例缩放。
- 颗粒叠加、径向光晕、浮动药丸和条形填充仅使用 CSS；无需外部图像。