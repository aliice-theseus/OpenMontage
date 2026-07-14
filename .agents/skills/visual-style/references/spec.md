# visual-style.md 格式规范

**版本：** 1.0
**状态：** 草案

## 概述

`visual-style.md` 文件是一个带有 YAML 前置元数据的 Markdown 文档，定义完整的视觉设计系统。该格式设计为：

- **人类可读** — 在任何文本编辑器中都可理解
- **AI 可消费** — 每个字段都可供 AI 模型直接使用
- **可移植** — 可在任何读取该格式的工具中使用

## 文件结构

```
---
[YAML 前置元数据]
---

[Markdown 正文章节]
```

## 必填字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `name` | string | 风格的显示名称 |
| `version` | string | 规范版本（当前为 `1.0`）|
| `style_prompt_short` | string | 1-2 句电梯演讲 |
| `style_prompt_full` | string | 完整的自然语言生成提示 — **最重要的字段** |
| `colors.primary` | array | 至少 2 种颜色，各有 `name`、`hex`、`role` |

## 可选字段

### 元数据

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `tags` | array | 分类标签（例如 "传奇设计"、"复古科技"）|
| `author` | string | 风格创作者的致谢 |
| `source_url` | string | 提取此风格的 URL |
| `created` | string | ISO 日期（YYYY-MM-DD）|

### 颜色

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `colors.accent` | array | 强调色，含 name/hex/role |
| `colors.neutral` | array | 中性色，含 name/hex/role |

**颜色对象模式：**
```yaml
- name: "描述性名称"
  hex: "#RRGGBB"
  role: "该颜色在系统中的使用方式"
```

### 排版

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `typography.display` | object | 展示/标题排版 |
| `typography.body` | object | 正文排版 |
| `typography.caption` | object | 说明文字/标签排版 |
| `typography.rules` | array | 排版规则和约束 |

**排版对象模式：**
```yaml
display:
  family: "字体族名称"
  weight: "bold"
  style: "uppercase, tight tracking"
```

### 布局

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `layout.grid` | string | 网格系统描述 |
| `layout.alignment` | string | 对齐方式 |
| `layout.aspect_ratio` | string | 默认宽高比（例如 "16:9"）|
| `layout.notes` | array | 额外布局指南 |

### 动效

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `motion.transitions` | array | 使用的过渡类型 |
| `motion.animation_style` | string | 整体动画方式 |
| `motion.pacing` | string | 时间/节奏描述 |
| `motion.audio_cues` | array | 声音设计说明 |

### 氛围

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `mood.keywords` | array | 氛围/感觉关键词 |
| `mood.era` | string | 时代参考 |
| `mood.cultural_reference` | string | 文化/历史背景 |
| `mood.avoid` | array | **反模式** — 明确避免的内容 |

### 资产

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `assets.reference_images` | array | 参考图片的 URL |
| `assets.gsep_elements` | array | 覆盖层/图形元素的 URL |
| `assets.html_snippets` | array | HTML 组件示例的 URL |
| `assets.color_palette_image` | object | 调色板可视化的 URL |

**重要：** 资产始终使用 URL，绝不嵌入二进制数据。

### 扩展

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `x_*` | object | 命名空间化的工具特定扩展 |

示例：
```yaml
x_heygen:
  video_id: "abc123"
  orientation: "landscape"

x_figma:
  library_id: "xyz789"
```

## Markdown 正文章节

在 YAML 前置元数据之后，包括以下可选的 Markdown 章节：

### `## Connectors`

工具特定的转换说明：

```markdown
## Connectors

### HeyGen Video Agent
将 `style_prompt_full` 作为视觉风格块输入。使用 `motion.transitions`
进行场景切换。方向：横向。

### HTML Slides
将颜色映射到 CSS 变量。对 h1-h3 使用 `typography.display`。
```

### `## Design Principles`

自由形式的设计哲学：

```markdown
## Design Principles

排版驱动层级。颜色使用克制且有意图。
每个元素都对齐基线网格。留白是一种特色。
```

### `## Extraction Notes`

来源文档（提取时）：

```markdown
## Extraction Notes

于 2026-03-12 从 https://example.com 提取。
主色从英雄区域采样。
通过浏览器开发工具识别排版。
```

## 完整示例

```yaml
---
name: "Josef Müller-Brockmann 瑞士国际风格"
version: "1.0"
tags:
  - 标志性设计
  - 极简风格
author: "Bin"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  网格锁定的瑞士精度。黑白基调配电光蓝
  强调色。仅 Helvetica。数据可视化作为主角元素。

style_prompt_full: >
  Josef Müller-Brockmann 瑞士国际风格。网格锁定的布局
  具有数学精度。黑白基调配一种强调色
  （电光蓝 #0066FF）。强烈的对角线构图。仅 Helvetica
  排版。数据可视化是主角 — 动画图表、
  计数器、网格。每一帧都对齐网格。过渡是水平
  网格擦拭。无有机形状。无渐变。无图库摄影。
  一切都是几何的、系统的、精确的。

colors:
  primary:
    - name: "纯黑"
      hex: "#000000"
      role: "主导底色、文字、结构元素"
    - name: "纯白"
      hex: "#FFFFFF"
      role: "背景区域、留白空间"
  accent:
    - name: "电光蓝"
      hex: "#0066FF"
      role: "唯一强调色 — 数据高亮、关键强调"
  neutral:
    - name: "网格灰"
      hex: "#CCCCCC"
      role: "网格线、次级结构"

typography:
  display:
    family: "Helvetica"
    weight: "bold"
    style: "大写或句首大写，紧凑字距"
  body:
    family: "Helvetica"
    weight: "regular"
    style: "左对齐，右侧参差，宽松行距"
  caption:
    family: "Helvetica"
    weight: "light"
    style: "小号，大写，宽字距"
  rules:
    - "仅 Helvetica — 无其他字体"
    - "字号遵循数学比例"
    - "始终左对齐 — 绝不居中"

layout:
  grid: "严格的模块化网格 — 12 列"
  alignment: "左对齐，对齐到网格"
  aspect_ratio: "16:9"
  notes:
    - "每个元素锁定到网格"
    - "数据可视化是主角元素"

motion:
  transitions:
    - "水平网格擦拭"
    - "元素对齐到网格位置"
    - "干净硬切"
  animation_style: >
    几何精度。元素对齐到网格位置。
    图表系统化地动画。没有什么会弹跳。
  pacing: "沉稳、自信、不慌不忙"

mood:
  keywords:
    - "精确"
    - "系统化"
    - "权威"
    - "几何"
  era: "1950–1970 年代（永恒）"
  cultural_reference: "Müller-Brockmann，《平面设计中的网格系统》"
  avoid:
    - "有机或曲线形状"
    - "渐变"
    - "图库摄影"
    - "居中文字"
    - "装饰元素"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""
---

## Design Principles

排版和网格是唯一需要的设计元素。
数学关系创造视觉和谐。
克制是终极的优雅。

## Connectors

### HeyGen Video Agent
逐字使用 `style_prompt_full`。无虚拟角色，无 B 卷 — 纯动态图形。
场景之间硬切。

### HTML Slides
映射到 CSS：`--color-bg: #000`、`--color-text: #FFF`、`--color-accent: #0066FF`。
通过系统字体或等效的 Google Fonts 使用 Helvetica。
```

## 验证

有效的 `visual-style.md` 必须有：

1. `---` 分隔符之间的有效 YAML 前置元数据
2. 所有必填字段存在
3. `colors.primary` 至少有 2 个颜色对象
4. 每个颜色对象都有 `name`、`hex` 和 `role`
5. `version` 设置为 `1.0`

## 版本管理

`version` 字段指规范版本，而非样式版本。当规范更改时：

- **小改**（新增可选字段）：版本保持 `1.0`
- **大改**（必填字段更改）：版本升至 `2.0`

## 设计决策

### 为什么 `style_prompt_full` 是必填的

许多 AI 工具只接受文本提示。通过要求完整的自然语言风格描述，我们确保每个 `visual-style.md` 文件立即可供任何工具使用 — 即使它们不解析结构化字段。

### 为什么没有嵌入二进制数据

URL 使文件保持小巧、可版本化和可移植。二进制资产应外部托管并通过 URL 引用。

### 为什么使用 `x_*` 命名空间

不同工具有不同的能力。`x_` 前缀允许工具特定配置而不污染核心模式。示例：`x_heygen`、`x_figma`、`x_paper`。

### 为什么有 `mood.avoid`

负面约束与正面约束同等重要。告诉 AI 不要做什么通常比告诉它要做什么更有效。
