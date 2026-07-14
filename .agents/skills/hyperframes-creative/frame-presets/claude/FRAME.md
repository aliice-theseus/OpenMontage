---
version: alpha
name: Claude — Frame (video / frame layer)
description: >
  Claude 的 design.md 的视频优先伴侣。单位是帧 (1920×1080)。原子
  相同且神圣 — 暖奶油纸（从不是纯白、从不是冷色）、单一陶土珊瑚
  作为稀缺"电压"、发丝线墨水抬升（无沉重阴影）、EB Garamond 用于所有
  展示 + Inter 正文 + JetBrains Mono 用于暖海军蓝代码表面上的索引/代码声音、
  句子大小写展示和 ✱ 珊瑚尖刺标记。构图 + 帧比例已重写。运动
  不在此范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  ink: "#141413"
  cream: "#FAF9F5"
  tile: "#EFE9DE"
  tile-strong: "#ECE3D4"
  coral: "#CC785C"
  navy: "#181715"
  navy-soft: "#1F1E1B"
  navy-elev: "#252320"

borders: { hairline: "1px solid ink@12%", hairline-strong: "1px solid ink@20%", dark: "1px solid cream@14% (on navy)" }
shadows: { card: "0 1px 3px ink@8%, 0 4px 16px ink@4%", none: "none" }

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Inter", cqw: 1.5, weight: 400, lineHeight: 1.5 }
  lead:    { fontFamily: "Inter", cqw: 2.08, weight: 400, lineHeight: 1.5 }
  card-title:{ fontFamily: "Inter", cqw: 2.3, weight: 500, lineHeight: 1.25, tracking: "-0.005em" }
  button:  { fontFamily: "Inter", cqw: 1.46, weight: 500, lineHeight: 1.0 }
  tag-upper:{ fontFamily: "Inter", cqw: 1.35, weight: 500, tracking: "0.18em", upper: true }
  kicker:  { fontFamily: "JetBrains Mono", px: 28, cqw: 1.46, weight: 500, tracking: "0.16em", upper: true }
  mono-label:{ fontFamily: "JetBrains Mono", px: 26, cqw: 1.35, weight: 500, tracking: "0.02em" }
  code:    { fontFamily: "JetBrains Mono", cqw: 1.67, weight: 400, lineHeight: 1.6 }
  # — display ramp (EB Garamond 400, sentence case, negative tracking. Renderer embeds only 400/700 — author at 400; italic is the synthesized slant) —
  headline:{ fontFamily: "EB Garamond", cqw: 4.6, weight: 400, lineHeight: 1.06, tracking: "-0.018em" }
  quote-pull:{ fontFamily: "EB Garamond", cqw: 5.0, weight: 400, lineHeight: 1.12, tracking: "-0.012em", italic: true }
  display-italic:{ fontFamily: "EB Garamond", cqw: 6.7, weight: 400, lineHeight: 1.05, tracking: "-0.012em", italic: true }
  display:{ fontFamily: "EB Garamond", cqw: 7.3, weight: 400, lineHeight: 1.02, tracking: "-0.022em" }
  number-hero:{ fontFamily: "EB Garamond", cqw: 9.4, weight: 400, lineHeight: 0.95, tracking: "-0.025em" }
  display-cover:{ fontFamily: "EB Garamond", cqw: 9.9, weight: 400, lineHeight: 0.98, tracking: "-0.028em" }
  number-unit:{ fontFamily: "JetBrains Mono", cqw: 2.08, weight: 500, lineHeight: 1.0 }

spacing:
  slide-pad: "4.2cqw"   # ~80px @1920
  gap-md: "1.7cqw"
  hairline: "1px"
  radius-sm: "6px"
  radius-md: "8px"
  radius-lg: "12px"
  radius-pill: "9999px"

components:
  card-hairline:
    backgroundColor: "{colors.cream} or {colors.tile}"
    border: "1px solid {colors.ink}@12%"
    rounded: "{spacing.radius-lg}"
    shadow: "{shadows.card}"
    typography: "{typography.card-title} + {typography.body}"
    description: "编辑内容卡片。抬升来自发丝线 + 一个柔和温暖阴影——绝不使用沉重投影、光晕或渐变。"
  kicker-spike:
    typography: "{typography.kicker}"
    mark: "✱ coral spike prefix"
    description: "眉标——JetBrains Mono 大写、索引性（2-5 词）、前缀为珊瑚 ✱。绝不是纯文本、绝不是句子。"
  coral-callout:
    backgroundColor: "{colors.coral} (full-bleed) or {colors.cream} with a coral edge"
    textColor: "{colors.cream} on coral"
    rounded: "{spacing.radius-md}"
    typography: "{typography.button} / {typography.h2}"
    description: "每帧唯一的电压时刻——CTA、单个内联链接或全出血带。一帧内绝不出现两个珊瑚色。"
  number-lockup:
    typography: "{typography.number-hero} figure + {typography.number-unit} unit"
    description: "英雄统计——EB Garamond 数字搭配 JetBrains Mono 单位（200K, +1,204, −318, 17 files）。数字是衬线；单位始终是等宽，绝不是衬线。"
  pull-quote:
    typography: "{typography.quote-pull} (EB Garamond italic) + {typography.tag-upper} cite"
    description: "提交信息、审阅者行或主题论点。EB Garamond 斜体，下方小号 Inter 大写引用来源。"
  section-rule:
    rule: "1px solid {colors.ink}@12% (or {colors.cream}@14% on navy)"
    description: "唯一的分隔符。珊瑚色 1px 规则线可绘制引入一个部分。绝不 2px+，绝不用作粗分隔线。"
  code-surface:
    backgroundColor: "{colors.navy} body / {colors.navy-elev} title bar + status strip"
    textColor: "{colors.cream} (JetBrains Mono); syntax in coral (keywords) / teal #5DB8A6 (strings) / amber #E8A55A (numbers)"
    border: "1px solid {colors.cream}@14%"
    rounded: "{spacing.radius-md}"
    description: "暖海军蓝代码/终端表面。代码本身由 code-* 注册块（code-diff / code-typing / code-snippet-*）渲染；此预设拥有周围表面、标题栏、状态条和等宽装饰——而非代码渲染本身。"
  spike-mark:
    glyph: "✱ (U+2731), always {colors.coral}"
    description: "品牌标记。在单个强调节拍上淡出 + 缩放 0.92→1；从不旋转。"
---

# Claude — 帧（视频 / 帧层）

## 概述

帧尺度下的 Claude 是一个**活起来的温暖编辑品牌书** — 文学印记或研究笔记的语域。主题是三种颜色：**奶油色是底色、墨水色是声音、珊瑚色是电压** — 第四种（暖海军蓝）仅在代码出现的地方。每个表面是**暖奶油色**（从不是纯白、从不是冷灰）；内容聚集在**瓷砖**表面上，深半步 — 分界是半步，从不是硬对比。抬升是**1px 发丝线**墨水色边框低 alpha，加上，罕见地，一个柔和温暖阴影。没有沉重投影、没有光晕、内容上没有渐变。

三种编辑声音，每种使用自己的字体：**EB Garamond** 承载每个展示时刻——封面、标题、拉取引用、大号统计数字——以大字展示尺寸配合柔和负追踪；其**斜体**是表达性语域。**Inter** 承载正文、导语、卡片标题、按钮和 UI 装饰。**JetBrains Mono** 承载索引层——眉标、技术标签、代码窗口、状态条。切换某声音的字体即折叠该语域：无衬线标题或衬线标签读起来像不同的品牌。

**帧尺度的关键特征：**

- **奶油色 / 墨水色 / 珊瑚色三位一体** + 暖海军蓝代码表面；奶油色是默认底色，墨水色是声音，珊瑚色是稀缺电压。
- **EB Garamond**（句子大小写、负追踪）用于所有展示；**Inter** 正文/装饰；**JetBrains Mono** 索引 + 代码。
- **发丝线抬升** — 1px 低 alpha 墨水色边框 + 最多一个柔和温暖阴影。无沉重投影、光晕或渐变。
- **珊瑚色是配给的** — 每帧最多一个珊瑚色时刻（CTA、内联链接或全出血带）；珊瑚色从不设置标题或正文段落。
- **密度自由** — 按内容意愿填充帧；一帧可以仅靠一个焦点或承载密集分层构图。
- **✱ 珊瑚尖刺**开启眉标；暖海军蓝保留给代码/终端表面。

## 帧

### 帧工艺条

目测检查在任何结构检查之前把关每一帧：

- **眯眼测试** — 一个 EB Garamond 展示时刻以 3-6 倍于其邻居的规模主导。
- **三位一体** — 奶油色/瓷砖底色、墨水色文本、珊瑚色恰好**一次**；暖海军蓝仅在代码表面；无冷灰/纯白/第四色调。
- **字体** — EB Garamond 句子大小写展示（负追踪）；Inter 400 正文；JetBrains Mono 眉标（大写 0.16em，珊瑚 ✱）+ 代码。

- **主画幅：** 1920×1080 (16:9)。展示使用 **`cqw`** (`px ÷ 1920 × 100 = cqw`) 编写。
- **竖版画幅：** 1080×1920 (9:16)。**方形画幅：** 1080×1080 (1:1)。
- **安全区域：** `slide-pad` 约 4.2cqw；眉标/等宽装饰位于其内。

**容器法则（承重）。** 每个帧底设置 `container-type: size`；所有帧相对单位均使用 `cqw`/`cqh` 相对于它——绝不使用 `vw`。发丝线保持 1px；卡片圆角保持 6/8/12px；暖纸阅读体验必须在每个比例下保持。

## 色彩

令牌与源文件一致。默认底色 `{colors.cream}`；内容聚集在 `{colors.tile}` / `{colors.tile-strong}` 上（半步暖色递进，从不是硬对比）。**标题和正文：** `{colors.ink}` 在奶油色/瓷砖上；`{colors.cream}` 在海军蓝上。**珊瑚色**（`{colors.coral}`）是稀缺电压——每帧一个时刻（CTA、内联链接或全出血带），绝不是正文，绝不是卡片填充。**暖海军蓝**（`{colors.navy}` / `navy-soft` / `navy-elev`）是代码/终端/暗色卡片表面——结构锚点，而非第四品牌色调。**无冷灰、无纯白、无纯黑。**

**固定语法颜色（装饰，不可混入的品牌色调）。** 当代码行是手动设置而非由 `code-*` 块渲染时，关键词为珊瑚色，字符串为**茶色 `#5DB8A6`**，数字为**琥珀色 `#E8A55A`**；状态读取成功 `#5DB872` / 警告 `#C64545`。这些追踪代码表面，而非品牌三位一体——将它们排除在品牌调色板之外。

## 字体排印

两个斜坡。**阅读/装饰斜坡**（Inter `body` 1.5cqw / `lead` 2.08cqw 字重 400；JetBrains Mono `kicker`/`mono-label` 以 px 为单位）承载文案 + 装饰；**展示斜坡**（EB Garamond `headline` 4.6cqw → `display-cover` 9.9cqw，字重 400，负追踪）承载每个标题 + 统计。

- **可读性底线：** 任何承重行 ≥ **1.4cqw**；等宽 px 标签仅为装饰性。
- **按文量体：** 根据长度调整标题大小。将块限制在 **≤ 78cqw**；≤3 词 → `display-cover`；4-6 词 → `display`；7+ 词 → `headline`。保留 7.3-9.9cqw 等级用于封面/声明/统计。
- **EB Garamond 展示为句子大小写**（非标题大小写、非全大写），字重 400，负追踪（−0.012..−0.028em）；当行文是立场或定义时使用**斜体**。**Inter 正文**句子大小写字重 400。**JetBrains Mono** 眉标全大写 0.16em 带珊瑚 ✱。无大写衬线、无无衬线标题、无衬线标签。

## 深度与表面

发丝线抬升：

- **1px 发丝线**墨水色边框约 12% alpha 是主要抬升（海军蓝上为 cream@14%）。
- **一个柔和温暖阴影**（`0 1px 3px ink@8%, 0 4px 16px ink@4%`）——罕见使用，绝不沉重。
- **半步表面** — 奶油色上的 `{colors.tile}` 块通过暖色阶梯而非通过投影阴影读起来有抬升感。

**天花板：** 无沉重投影阴影、无光晕、内容上无渐变、无倾斜。系统没有光要发出；它通过温暖和发丝线来阅读。

## 形状

- **6px** 小装饰，**8px** 卡片/代码表面，**12px** 大卡片/引用框，**9999px** 仅限于真正药丸。无方形角，无沉重圆角；编辑语域是柔和圆润，从不生硬。

## 组件

- **card-hairline** — 编辑内容卡片（发丝线 + 一个柔和阴影）。**section-rule** — 唯一分隔符（1px，珊瑚色可绘制引入）。
- **kicker-spike** — ✱ 珊瑚色眉标。**coral-callout** — 唯一的电压时刻（CTA / 内联链接 / 全出血带）。
- **number-lockup** — EB Garamond 数字 + 等宽单位（PR `+N / −M`，`200K`，文件计数）。**pull-quote** — EB Garamond 斜体 + 引用来源（提交信息 / 审阅者行）。
- **code-surface** — 暖海军蓝代码/终端表面；代码本身来自 **`code-*` 注册块**，此预设拥有表面 + 等宽装饰。
- **spike-mark** — ✱ 品牌字形，始终珊瑚色。

## 帧处理方案

> 配方：底色 · 容器 · 组成 · 焦点 · 装饰 · 强调 · 固定/自由 · 密度。
> 每帧一个珊瑚色时刻；以 kicker-spike 开启。

### 1 · 封面（标识 · 动态：超大 EB Garamond · 奶油色）

**底色** `{colors.cream}`，`slide-pad`。**组成** kicker-spike、display-cover、lead、mono-label index。**焦点** 2-3 行 EB Garamond `display-cover`（句子大小写，墨水色）位于珊瑚 ✱ 眉标下方。**装饰** 等宽索引条（仓库 · 分支）。**强调** 单个珊瑚 ✱。**固定** EB Garamond 400 句子大小写、发丝线、奶油色底色。**自由** 标题、等宽索引、布局 + 帧的行进程度。**密度** 自由。

### 2 · 声明（声明 · 动态：单行 EB Garamond · 奶油色或海军蓝）

**底色** `{colors.cream}`（或 `{colors.navy}` 用于庄重感）。**组成** kicker-spike、display、可选 lead。**焦点** 一行 2 行 EB Garamond `display` 以句子形式承载变化——如果是立场则使用**斜体**。**装饰** 等宽眉标。**强调** 无——衬线承载一切（或一个珊瑚色词）。**固定** 句子大小写衬线。**自由** 行文、底色、布局 + 密度。**密度** 自由。

### 3 · 代码表面（代码 · 动态：暖海军蓝代码窗口 · PR 关键帧）

**底色** `{colors.cream}` 框定 `{colors.navy}` **code-surface**（8px，cream@14% 发丝线，`navy-elev` 标题栏 + 文件名为等宽）。**组成** mono-label 文件名、**`code-*` 块**（code-diff / code-typing / code-snippet-*）、可选 `section-rule`。**焦点** 代码面板——差异 / 之前→之后 / 打字片段。**装饰** 等宽文件名 + 状态条。**强调** 面板内语法珊瑚/茶色/琥珀色；面板外一个珊瑚色标记（如 `+`/`−` 装订线提示）。**固定** 暖海军蓝表面、等宽代码、发丝线。**自由** 使用哪个 code-* 块、代码（来自差异）、面板大小。**密度** 密集。

### 4 · 数字 / 影响（数据 · 动态：超大数字 · 奶油色）

**底色** `{colors.cream}`，`slide-pad`。**组成** kicker-spike、number-lockup、lead/caption、可选 `section-rule`。**焦点** EB Garamond `number-hero` 数字带等宽单位，位于 1px 规则线上——PR 影响（`+1,204 / −318`，`17 files`，`2.1× faster`）。**装饰** 等宽标签。**强调** 墨水色数字；最多一个珊瑚色单位。**固定** 衬线数字 + 等宽单位、发丝线规则。**自由** 数字（来自脚本）、标签、布局 + 密度。**密度** 自由。

### 5 · 拉取引用（引用 · 动态：EB Garamond 斜体 · 奶油色）

**底色** `{colors.cream}`。**组成** kicker-spike、pull-quote、tag-upper cite。**焦点** EB Garamond **斜体** `quote-pull`——提交信息、审阅者行或主题论点——下方小号 Inter 大写引用来源（作者 · 角色）。**装饰** 等宽眉标。**强调** 无，或一个珊瑚色标记。**固定** EB Garamond 斜体引用 + 大写引用来源。**自由** 引用、署名、布局 + 密度。**密度** 自由。

### 6 · 结束 / CTA（结尾 · 动态：珊瑚色电压 · 奶油色或海军蓝）

**底色** `{colors.cream}`（或 `{colors.navy}`）。**组成** display 签名、coral-callout、可选贡献者行（`assets/<login>.png` 头像 + 等宽名称）。**焦点** 简短 EB Garamond 签名配合唯一的 **coral-callout**（CTA 或全出血带），以及对于"发货者"结束页，一排发丝线环状头像芯片。**装饰** 等宽索引。**强调** 单个珊瑚色电压。**固定** 一个珊瑚色时刻、发丝线头像环、句子大小写衬线。**自由** 签名、谁发货、布局 + 密度。**密度** 自由。

## 构图规则

### 必须

- 将每帧立于**暖奶油色底色**之上；将内容聚集在**半步瓷砖**表面上。
- 所有展示使用 **EB Garamond、句子大小写**、负追踪；**Inter 400** 正文；**JetBrains Mono** 眉标（大写、0.16em、珊瑚 ✱）+ 代码。
- 配给**珊瑚色至每帧一个时刻**——CTA、内联链接或全出血带。
- 使用 **1px 发丝线** + 最多一个柔和温暖阴影抬升；将**暖海军蓝**保留给代码/终端表面。
- 以**一个清晰焦点**引领；以 **kicker-spike** 开启区域。按内容意愿填充帧。
- 为每个统计配对 EB Garamond 数字与**等宽单位**；在海军蓝表面上通过 **`code-*` 块**渲染代码。

### 禁止

- 无纯白、无冷灰、无纯黑；无第四品牌色调（海军蓝是结构性的，语法颜色是装饰）。
- 无沉重投影阴影、光晕、内容上的渐变或倾斜——仅发丝线抬升。
- 无大写或标题大小写的 EB Garamond 展示；无无衬线标题；无衬线标签；无衬线设置的数字单位。
- 一帧内无两个珊瑚色时刻；珊瑚色从不设置标题或正文段落。
- 不要将标题撑到超过度量——按级降档。

## 宽高比行为

| 处理方案        | 16:9                     | 9:16                         | 1:1                     |
| -------------- | ------------------------ | ---------------------------- | ----------------------- |
| 封面           | display 左对齐，索引顶部  | display 顶部，索引下方       | display，索引角位       |
| 声明           | 行左对齐/居中             | 行堆叠                       | 居中                    |
| 代码表面       | 面板在奶油色中框定        | 面板更高，行数更少           | 面板居中，方形          |
| 数字/影响      | 数字左对齐                | 数字居中，更高               | 居中                    |
| 拉取引用       | 引用左对齐                | 引用堆叠                     | 居中                    |
| 结束/CTA       | 签名 + 头像行             | 签名顶部，头像下方           | 居中，头像环绕          |

`slide-pad` 在短边上保持；重新调整 display 使其高于 1.4cqw 底线。代码表面在每个宽高比下保持其发丝线 + 等宽装饰；头像行环绕而非缩小至不可读。

## 批准的实体

源文件中未定义真实客户、徽标或供应商——将任何此类标记渲染为占位符。贡献者头像来自项目的 `assets/<login>.png`（从 PR 的人员图中暂存）；✱ 尖刺、发丝线和代码表面仅使用 CSS，无需外部图像。

## 数字与声明（硬性规则）

绝不在帧尺度上编造数字、统计数据、差异或计数。将插槽渲染为 `— figure —`、`{metric}`、`+N / −M`。数字组合、代码面板和影响统计在脚本（来自 PR 摄入）提供真实值之前使用占位符。分支名称、文件计数和 `+/−` 总计追踪到差异；提交/问题编号是装饰性元素。

## 预渲染自审

- **眯眼测试** — 一个 EB Garamond 展示时刻主导。
- **三位一体** — 奶油色底色 + 瓷砖阶梯 + 墨水色声音；珊瑚色恰好出现一次；暖海军蓝仅在代码表面；无冷灰/纯白/第四色调。
- **字体** — EB Garamond 句子大小写展示（负追踪）；Inter 400 正文；JetBrains Mono 眉标（大写 0.16em，珊瑚 ✱）+ 代码；≥1.4cqw 底线。
- **深度** — 1px 发丝线 + 最多一个柔和温暖阴影；无沉重投影/光晕/渐变/倾斜；6/8/12px 圆角。
- **代码** — 代码由 `code-*` 块在暖海军蓝表面上渲染；语法珊瑚/茶色/琥珀色；数字配等宽单位。
- **编造** — 每个数字/差异追溯到 PR，否则为占位符。

## 已知差距

- **运动有意不在此范围内。** frame.md 仅指定构图。Claude 的运动语域——短交叉淡入淡出、无过冲/弹跳/弹性、珊瑚色是唯一的"绘制入"、数字计数、代码逐行打字——存在于工作流的 `motion-language.md` + `hyperframes-animation` 中，不在此处。
- **EB Garamond + Inter + JetBrains Mono 均已捆绑在 HyperFrames 渲染器中（`@fontsource` 嵌入数据）——它们通过名称离线解析，无 Google Fonts 依赖。** 这是故意的：此处每种字体都在干净的机器或 AWS Lambda 上确定性地渲染，因此帧不需要捕获的 `.woff2` 或 `@font-face` 来加载这三种字体。嵌入集提供**仅字重 400 + 700 且无真正斜体**——因此请以**字重 400** 编写展示（700 读作沉重粗体，偏离语域），并将斜体视为浏览器合成的倾斜（可接受用于拉取引用语域；如果项目重度依赖斜体，则提供真正的 EB Garamond 斜体 `.woff2` + `@font-face`）。EB Garamond 是一种温暖旧式衬线（低对比度、人文主义）；如果加载失败，回退到 Georgia 或其他旧式衬线——绝不回退到无衬线。中日韩：Noto Serif SC（展示）/ Noto Sans SC（正文）/ Noto Sans Mono CJK（代码）；当衬线缺失时，句子大小写的温暖感得以延续。
- **语法颜色（茶色 `#5DB8A6` / 琥珀色 `#E8A55A` / 状态）是固定装饰**，在 §色彩 中声明——它们不在可混入的 `colors:` 块中，因此品牌混入绝不会重绘它们。
- **代码本身是 `code-*` 注册块**，而非此预设——此预设仅拥有周围的暖海军蓝表面 + 等宽装饰。
- **9:16 / 1:1 为指导**；验证可读性底线以及奶油色/瓷砖温暖感 + 单珊瑚色纪律在每个比例下是否保持。