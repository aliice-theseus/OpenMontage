---
version: alpha
name: Cartesian — Frame (video / frame layer)
description: >
  Cartesian 的 design.md 的视频优先伴侣。单位是帧 (1920×1080)。原子
  相同且神圣 — 五色调暖石调色板、Playfair Display 400 + Inter、
  通用 1px 灰褐发丝线作为唯一结构设备、圆规绘制的几何环、
  以及零阴影/零填充。构图、帧比例和宽高比行为已为帧
  重写。克制是规则；运动不在此范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  bg-primary: "#EDE8E0"
  bg-secondary: "#E2DBD1"
  text-primary: "#1A1A1A"
  text-secondary: "#5A5A5A"
  accent: "#8A8178"
  line: "#B8B0A4"
  white-overlay: "rgba(255,255,255,0.3)"

typography:
  # — reading ramp (Inter) —
  body:        { fontFamily: "Inter", cqw: 1.0,  weight: 400, lineHeight: 1.6, color: "text-secondary" }
  body-sm:     { fontFamily: "Inter", cqw: 0.85, weight: 400, lineHeight: 1.6 }
  subtitle:    { fontFamily: "Inter", cqw: 1.3,  weight: 400, lineHeight: 1.5 }
  label:       { fontFamily: "Inter", px: 14, weight: 500, tracking: "3px", upper: true, color: "accent" }
  attribution: { fontFamily: "Inter", px: 15, weight: 400, tracking: "2px", upper: true, color: "accent" }
  micro:       { fontFamily: "Inter", px: 12, weight: 400, tracking: "2px", upper: true, color: "accent" }
  # — display / hero ramp (Playfair Display 400, sentence case) —
  h3:          { fontFamily: "Playfair Display", cqw: 1.8, weight: 400, lineHeight: 1.1 }
  timeline-headline:{ fontFamily: "Playfair Display", cqw: 1.9, weight: 400, lineHeight: 1.1 }
  card-headline:{ fontFamily: "Playfair Display", cqw: 2.0, weight: 400, lineHeight: 1.15 }
  stat-figure: { fontFamily: "Playfair Display", cqw: 3.0, weight: 400, lineHeight: 1.0 }
  quote-mark:  { fontFamily: "Playfair Display", cqw: 9.0, weight: 400, lineHeight: 0.5, color: "line" }
  h2:          { fontFamily: "Playfair Display", cqw: 4.0, weight: 400, lineHeight: 1.1 }
  h1:          { fontFamily: "Playfair Display", cqw: 6.2, weight: 400, lineHeight: 1.06 }
  display:     { fontFamily: "Playfair Display", cqw: 8.0, weight: 400, lineHeight: 1.04 }

spacing:
  pad-x: "7cqw"
  pad-y: "5cqw"
  gap-xl: "6cqw"
  gap-lg: "5cqw"

components:
  hairline:
    rule: "0.07cqw solid {colors.line}"
    description: "通用结构设备——每个分隔符（议程规则线、时间线连接器、卡片边框、统计顶部）都是这条 1px 灰褐线。不存在粗边框。"
  card:
    backgroundColor: "{colors.white-overlay}"
    border: "0.07cqw solid {colors.line}"
    rounded: "0"
    shadow: "none"
    description: "微弱的白色叠加填充（画布透出）使卡片区别于裸区域。"
  card-icon:
    border: "0.07cqw solid {colors.line}"
    rounded: "50%"
    size: "40px circle"
    textColor: "{colors.accent}"
    typography: "Playfair numeral/letter"
    description: "环状圆形标记。"
  agenda-row:
    borderBottom: "0.07cqw solid {colors.line}"
    typography: "{typography.h3} (numeral {colors.accent}, label {colors.text-primary})"
    description: "左侧数字、右侧标签，位于灰褐规则线上。"
  timeline:
    borderTop: "0.07cqw solid {colors.line}"
    typography: "{typography.timeline-headline} + {typography.body-sm}"
    description: "跨项目的单一灰褐顶部规则线——无节点、无圆点。"
  stats-cluster:
    borderTop: "0.07cqw solid {colors.line}"
    typography: "{typography.stat-figure} + uppercase {colors.accent} labels"
    description: "内联适度的统计数字（无英雄数字）。"
  geo-ring:
    border: "1px solid {colors.line} (inner dashed ::before ~70–80%)"
    rounded: "50%"
    size: "10–50cqw"
    opacity: "0.2–0.5"
    description: "内容背后的圆规构图环。每帧 1-2 个，从不超过。"
  horizontal-accent:
    backgroundColor: "{colors.text-primary}"
    size: "~18cqw × 1px"
    description: "系统唯一的墨水黑色规则线——在封面/结束页上作为强烈的终端强调，稀疏使用。"
  vertical-line:
    backgroundColor: "{colors.line}"
    size: "1px × full height, ~5cqw from edge"
    opacity: "0.3–0.4"
    description: "绘图纸对齐参考线。可选。"
  image-placeholder:
    backgroundColor: "{colors.bg-secondary}"
    mark: "crossed +30°/−30° 1px taupe diagonals (an X)"
    typography: "small uppercase {typography.micro}"
    description: "标志性的图像未连接标记。"
  team-photo:
    backgroundColor: "{colors.bg-secondary}"
    border: "0.07cqw solid {colors.line}"
    rounded: "50%"
    typography: "Playfair initial in {colors.accent}"
    description: "圆形肖像框。"
---

# Cartesian — 帧（视频 / 帧层）

## 概述

帧尺度下的 Cartesian 是一个**安静的博物馆目录编辑系统** — 通过 1px 线条实现克制。每个结构分隔符都是一个 1px 灰褐发丝线；没有粗边框、没有填充（除了微弱的白色叠加卡片）、没有阴影、没有圆角矩形。层级来自**字体对比和负空间**，氛围来自**圆规绘制的几何环**在内容后漂移。

声音是一个文学搭配：**Playfair Display** 字重 400（细笔画 didone、从不粗体、始终句子大小写）承载每个标题、数字和引用标记为墨水色；**Inter** 承载暖灰色正文和灰褐色大写标签，2-3px 字距。调色板是五块暖石加墨水色 — 不存在民粹强调色。正确的密度是**稀疏和呼吸感的**：一个清晰的想法、良好构图、在石纸上。

**帧尺度的关键特征：**

- **1px 灰褐发丝线**作为通用结构设备 — 每个分隔符都是这一条线。
- **Playfair Display 400**（墨水色、句子大小写）用于展示；**Inter** 正文（灰色）+ 标签（灰褐、追踪）。
- **五块暖石 + 墨水色** — 无红/蓝/绿；唯一"颜色"是字体对比。
- **圆规绘制的几何环**（实线 + 虚线、20-50% 不透明度）在内容后营造情绪。
- **平面** — 零阴影、零圆角矩形（仅圆形）；唯一的墨水色线条是 `horizontal-accent`。
- **稀疏且呼吸感** — 慷慨的负空间；拥挤读起来像破损。

## 帧

### 帧工艺条

三条目测检查在任何结构检查之前把关每一帧：

- **眯眼测试** — 一个 Playfair 元素以 **3–6 倍于其最近邻**为主导；衬线/无衬线 + 大小对比承载层级，而非字重。
- **静谧测试** — 声明式帧读起来有 **55-60% 的空白**；Cartesian **没有密集帧**——即使是议程/索引也保持呼吸（拥挤时系统崩溃）。
- **克制测试** — 每帧**最多两个几何环**；唯一的墨水黑色 `horizontal-accent` 规则线稀疏使用；绝不使用民粹强调色。
- **参考测试** — 瞄准**Vignelli 编辑手册 / Cooper Hewitt 目录 / 铅笔和描图纸平面**；失败看起来像**带有阴影和圆角卡片的 SaaS 画板**。

- **主画幅：** 1920×1080 (16:9)。展示使用 **`cqw`** (`px ÷ 1920 × 100 = cqw`) 编写。
- **竖版画幅：** 1080×1920 (9:16)。**方形画幅：** 1080×1080 (1:1)。
- **安全区域：** `pad-x` (7cqw) 宽敞的间距；几何图形可溢出边缘。

**容器法则（承重）。** 每个帧底设置 `container-type: size`；所有帧相对单位均使用 `cqw`/`cqh` 相对于它——绝不使用 `vw`。1px 发丝线和几何环在任何渲染尺寸下都保持相对于帧的比例。

## 色彩

令牌与源文件一致。`{colors.bg-primary}` 是底色；`{colors.text-primary}` 墨水色是标题和唯一的黑色强调规则线；`{colors.text-secondary}` 灰色是正文；`{colors.accent}` 灰褐是标签、数字、小文字；`{colors.line}` 灰褐是每条 1px 结构边框。`{colors.bg-secondary}` 是唯一的次要填充（占位符、相框）。**无民粹强调色**——当需要强调时，放大字体、从无衬线切换到衬线、或添加一条 `horizontal-accent` 墨水线。标题从不是灰褐色；小文字从不是墨水色。

## 字体排印

两个斜坡。**阅读斜坡**（Inter 正文 1.0cqw 灰色，px 标签为灰褐）承载文案 + 装饰；**展示斜坡**（Playfair `h3` 1.8cqw → `display` 8.0cqw，全部字重 400）承载每个标题。

- **可读性底线：** 任何承重行 ≥ **1.4cqw**；px 标签仅为装饰性。
- **按文量体：** 根据长度调整标题大小。将块限制在 **≤ 78cqw**；≤3 词 → `display`/`h1`；4-6 词 → `h2`；7+ 词 → `h3`。Cartesian 没有英雄统计数字——统计保持适度（`stat-figure` 3cqw）。
- **Playfair 字重 400、墨水色、句子大小写** — 从不粗体、从不全大写、从不灰褐。**Inter 标签全大写、2-3px 追踪、灰褐。** 斜体仅在强调时使用 Playfair 斜体。

## 深度与表面

平面是唯一的技术。层级来自：

- **字体对比** — Playfair 衬线 vs Inter 无衬线；8cqw→0.7cqw 的尺度跨度。
- **1px 灰褐发丝线** — 每个分隔线、卡片轮廓、时间线规则、照片环。
- **色调** — 墨水色 vs 灰色 vs 灰褐。
- **负空间** — 宽裕的内边距。
- **几何氛围** — 暗示深度而不创造深度的圆规环。

**天花板：** 无 `box-shadow`、无抬高卡片、无渐变、无圆角矩形。唯一的墨水线（`horizontal-accent`）是唯一的非灰褐规则线。

## 形状

- **50%（圆形）** — card-icon、team-photo、nav-dot、每个几何环。
- **0** — 其他所有形状；软圆角不存在。

## 组件

- **hairline** — 通用 1px 灰褐分隔符（身份特征）。
- **card**（1px 灰褐 + 白色叠加）/ **card-icon**（环状圆形）/ **agenda-row** / **timeline**（线，无节点）/ **stats-cluster** — 全部构建在发丝线上。
- **geo-ring** — 圆规装饰（实线 + 虚线），每帧 1-2 个。**horizontal-accent** — 唯一墨水线，稀疏使用。**vertical-line** — 绘图参考线。
- **image-placeholder**（交叉 X）/ **team-photo**（环状首字母）— 石材填充占位符。

## 帧处理方案

> 配方：底色 · 容器 · 组成 · 焦点 · 装饰 · 强调 · 静谧 · 固定/自由 · 密度。
> 每帧都稀疏且呼吸感；最多 1-2 个几何装饰。

### 1 · 封面（标识 · 动态：衬线 + 圆规环 · 左对齐）

**底色** `{colors.bg-primary}`，`pad-x`。**组成** geo-ring（右侧，~34cqw，实线+虚线）、vertical-line（左侧）、label、display/h1。**焦点** 2-3 行 Playfair `display`/`h1` 标题（墨水色，关键词斜体），左锚定，上方为灰褐 `label`，下方为 Inter 副标题。**装饰** 可选的底部元数据行（Playfair 值 + 灰褐标签）。**强调** 几何环；可选一条 `horizontal-accent` 墨水线（如果与元数据不冲突）。**静谧** 约 55% 空白。**固定** Playfair 400 墨水色句子大小写，≤2 个几何元素，1px 线条。**自由** 标题、环位置、元数据。**密度** 稀疏。

### 2 · 议程 / 索引（索引 · 动态：发丝线列表 · 左对齐）

**底色** `{colors.bg-primary}`，`pad-x`。**组成** label、h2、agenda-rows。**焦点** Playfair `h2` 下方 4-6 个议程行（Playfair 数字为灰褐 + Playfair 标签为墨水色），每行位于 1px 灰褐规则线上。**装饰** 灰褐 `label` 眉标。**强调** 无——灰褐数字承载一切。**静谧** 适中；行间距宽裕。**固定** 1px 灰褐规则线，Playfair 400。**自由** 项目、数量。**密度** 标准（稀疏行）。

### 3 · 拉取引用（引用 · 动态：居中陈述 · 圆规环）

**底色** `{colors.bg-primary}`，居中。**组成** geo-ring（居中虚线，~26cqw）、quote-mark、h2/display-quote、attribution。**焦点** 2 行 Playfair 引用（墨水色），居中，位于 50% 灰褐 Playfair quote-mark 下方；下方为灰褐大写署名。**强调** 微弱的居中环。**静谧** 约 60%——故意开放。**固定** Playfair 400，一个环，居中。**自由** 引用、署名。**密度** 稀疏。

### 4 · 结束页（结尾 · 动态：居中环 · 居中）

**底色** `{colors.bg-primary}`，居中。**组成** geo-ring（居中，~40cqw，实线+虚线）、label、h1/display、horizontal-accent。**焦点** 1-2 行 Playfair 签名（墨水色，斜体关键词），居中对齐在最大的圆规环内；下方为一条短的墨水色 `horizontal-accent`。**强调** 环 + 唯一墨水线。**静谧** 约 60%。**固定** Playfair 400，居中，≤2 个几何元素。**自由** 签名、环的尺寸。**密度** 稀疏。

### 5 · 双栏编辑（内容 · 动态：不对称分割 · 左对齐）

**底色** `{colors.bg-primary}`，`pad-x`，两列带 `gap-xl`。**组成** label、h2、body、image-placeholder（交叉 X）或 card。**焦点** 文本列中的 Playfair `h2` + Inter 正文；另一列为 image-placeholder 或 card。**强调** 无。**静谧** 宽敞间距。**固定** 1px 灰褐卡片/占位符边框、白色叠加填充。**自由** 哪一侧为文本、正文内容。**密度** 标准。

### 6 · 统计 / 时间线（数据 · 动态：发丝线轨道 · 左对齐）

**底色** `{colors.bg-primary}`，`pad-x`。**组成** label、h3、stats-cluster 或 timeline。**焦点** 适度的 Playfair 统计行（或 1px 规则线时间线，包含年份 + 标题 + 正文，无节点），由 1px 灰褐顶部规则线框定。**强调** 无。**静谧** 适中。**固定** 适度的统计尺度、发丝线规则、无节点。**自由** 数字、阶段。**密度** 标准。

## 构图规则

### 必须

- 为每个分隔符使用**一条 1px 灰褐线**——发丝线就是身份特征。
- 设置每个 **Playfair 标题为字重 400、墨水色、句子大小写**；标签渲染为灰褐、大写、2-3px 追踪。
- 在内容后叠加 **一或两个圆规环**（实线 + 虚线，20-50% 不透明度）营造氛围。
- 让帧**呼吸**——稀疏、宽敞的负空间；声明式帧 55-60% 空白。
- 引用/结束页偏向居中；封面/议程/编辑页偏向不对称/左对齐。占位符填充使用 `bg-secondary`。

### 禁止

- 不要引入民粹强调色——仅石材和墨水色。
- 不要加粗 Playfair、不要将标题渲染为灰褐、不要使用粗（2px+）边框。
- 不要添加阴影、抬高卡片或圆角矩形（仅允许圆形）。
- 不要让帧拥挤——紧凑的布局读起来像破损。
- 每帧不得超过两个几何装饰；不要将标题撑到边缘到边缘。

## 宽高比行为

| 处理方案           | 16:9                       | 9:16                                 | 1:1                          |
| ----------------- | -------------------------- | ------------------------------------ | ---------------------------- |
| 封面              | 标题左对齐，环在右侧       | 标题顶部，环在下方                   | 标题偏上，环在背后           |
| 议程 / 索引       | h2 + 行                    | h2 + 行（更紧凑）                    | h2 + 行                      |
| 拉取引用          | 居中，环在背后             | 居中，更高                           | 居中                         |
| 结束页            | 环内居中                   | 居中，环缩放                         | 居中                         |
| 双栏编辑          | 文本 + 视觉并排            | 堆叠（折叠）                         | 堆叠                         |
| 统计 / 时间线     | 水平轨道                   | 垂直堆叠（取消时间线规则）           | 紧凑                         |

宽敞的 `pad-x` 在短边上保持；根据宽高比重新调整 display 使其高于 1.4cqw 底线。在 9:16 上，时间线规则在堆叠时失去意义——切换到垂直列表（按源文件）。

## 批准的实体

源文件中未定义真实客户、徽标或供应商——将任何此类标记渲染为占位符（交叉 X 图像占位符，或肖像的环状首字母）。

## 数字与声明（硬性规则）

绝不在帧尺度上编造数字、日期或计数。将插槽渲染为 `— figure —`、`{metric}`。统计和时间线年份在脚本提供之前使用占位符。议程序号（01, 02…）是装饰性的，可顺序使用。

## 预渲染自审

- **眯眼测试** — 一个 Playfair 元素主导；衬线/无衬线对比承载层级。
- **静谧测试** — 声明式帧 55-60% 空白；没有任何内容拥挤。
- **调色板** — 仅五块石头 + 墨水色；无民粹强调色；标题墨水色、标签灰褐。
- **线条** — 每个分隔符都是 1px 灰褐发丝线；唯一的墨水线是 `horizontal-accent`。
- **字体** — Playfair 400 句子大小写、按文量体；标签大写 2-3px；≥1.4cqw 底线。
- **深度** — 0 阴影、0 圆角矩形；每帧 ≤2 个几何环。
- **锚定** — 引用/结束页居中，封面/议程/编辑页左对齐/不对称；不连续三个相同。
- **编造** — 每个数字追溯到脚本，否则为占位符。

## 已知差距

- **运动有意不在此范围内。** frame.md 仅指定构图；源文件中的 0.6s 淡入淡出是画板机制。
- **Playfair Display + Inter 通过 Google Fonts。** 中日韩配对（Noto Serif SC 700/400）延续；Playfair 没有汉字斜体——使用字重变化/灰褐作为强调替代。
- **9:16 / 1:1 为指导**；验证可读性底线以及时间线是否折叠为垂直列表。
- 几何环、交叉 X 占位符和虚线内环仅使用 CSS；无需外部图像。