# visual-style.md 格式规范

**版本：** 1.0
**状态：** 草案

## 概述

`visual-style.md` 文件是一个带有 YAML 前置元数据的 Markdown 文档，用于定义完整的视觉设计系统。该格式的设计目标：

- **人类可读** — 在任何文本编辑器中都能理解
- **AI 可消费** — 每个字段都可以直接被 AI 模型使用
- **可移植** — 可在任何支持该格式的工具之间通用

## 文件结构

```
---
[YAML 前置元数据]
---

[Markdown 正文部分]
```

## 必填字段

| 字段 | 类型 | 描述 |
|------|------|------|
| `name` | string | 风格的显示名称 |
| `version` | string | 规范版本（当前为 `1.0`） |
| `style_prompt_short` | string | 1-2 句电梯游说 |
| `style_prompt_full` | string | 完整的自然语言生成提示 — **最重要的字段** |
| `colors.primary` | array | 至少 2 种颜色，每种包含 `name`、`hex`、`role` |

## 可选字段

### 元数据

| 字段 | 类型 | 描述 |
|------|------|------|
| `tags` | array | 分类标签（例如 "iconic design"、"retro tech"） |
| `author` | string | 风格作者署名 |
| `source_url` | string | 提取此风格的来源 URL |
| `created` | string | ISO 日期 (YYYY-MM-DD) |

### 颜色

| 字段 | 类型 | 描述 |
|------|------|------|
| `colors.accent` | array | 强调色，含 name/hex/role |
| `colors.neutral` | array | 中性色，含 name/hex/role |

**颜色对象结构：**
```yaml
- name: "描述性名称"
  hex: "#RRGGBB"
  role: "此颜色在系统中的使用方式"
```

### 排版

| 字段 | 类型 | 描述 |
|------|------|------|
| `typography.display` | object | 展示/标题排版 |
| `typography.body` | object | 正文排版 |
| `typography.caption` | object | 说明文字/标签排版 |
| `typography.rules` | array | 排版规则和约束 |

**排版对象结构：**
```yaml
display:
  family: "字体族名称"
  weight: "bold"
  style: "uppercase, tight tracking"
```

### 布局

| 字段 | 类型 | 描述 |
|------|------|------|
| `layout.grid` | string | 网格系统描述 |
| `layout.alignment` | string | 对齐方式 |
| `layout.aspect_ratio` | string | 默认宽高比（如 "16:9"） |
| `layout.notes` | array | 额外布局指南 |

### 动效

| 字段 | 类型 | 描述 |
|------|------|------|
| `motion.transitions` | array | 使用的过渡类型 |
| `motion.animation_style` | string | 整体动画方式 |
| `motion.pacing` | string | 节奏/韵律描述 |
| `motion.audio_cues` | array | 声音设计说明 |

### 氛围

| 字段 | 类型 | 描述 |
|------|------|------|
| `mood.keywords` | array | 氛围/感受关键词 |
| `mood.era` | string | 时代参考 |
| `mood.cultural_reference` | string | 文化/历史背景 |
| `mood.avoid` | array | **反模式** — 需明确避免的内容 |

### 资源

| 字段 | 类型 | 描述 |
|------|------|------|
| `assets.reference_images` | array | 参考图片 URL |
| `assets.gsep_elements` | array | 叠加/图形元素 URL |
| `assets.html_snippets` | array | HTML 组件示例 URL |
| `assets.color_palette_image` | object | 调色板可视化图片 URL |

**重要提示：** 资源始终使用 URL，绝不嵌入二进制数据。

### 扩展

| 字段 | 类型 | 描述 |
|------|------|------|
| `x_*` | object | 命名空间化的工具特定扩展 |

示例：
```yaml
x_heygen:
  video_id: "abc123"
  orientation: "landscape"

x_figma:
  library_id: "xyz789"
```

## Markdown 正文部分

在 YAML 前置元数据之后，可包含以下可选的 Markdown 部分：

### `## Connectors`（连接器）

工具特定的转换说明：

```markdown
## Connectors

### HeyGen Video Agent
将 `style_prompt_full` 作为视觉风格块输入。使用 `motion.transitions`
进行场景切换。方向：横屏。

### HTML Slides
将颜色映射到 CSS 变量。使用 `typography.display` 为 h1-h3 设置样式。
```

### `## Design Principles`（设计原则）

自由形式的设计理念：

```markdown
## Design Principles

排版驱动层级。颜色使用克制且有目的性。
每个元素都对齐基线网格。留白是一种特色。
```

### `## Extraction Notes`（提取说明）

来源文档（提取时使用）：

```markdown
## Extraction Notes

提取自 https://example.com，日期 2026-03-12。
主色采样自主视觉区域。
排版通过浏览器开发者工具识别。
```

## 完整示例

```yaml
---
name: "Josef Müller-Brockmann Swiss International Style"
version: "1.0"
tags:
  - iconic design
  - sleek minimal
author: "Bin"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  Grid-locked Swiss precision. Black and white base with electric blue
  accent. Helvetica only. Data visualizations as hero elements.

style_prompt_full: >
  Josef Müller-Brockmann Swiss International Style. Grid-locked layouts
  with mathematical precision. Black and white base with ONE accent color
  (electric blue #0066FF). Strong diagonal compositions. Helvetica
  typography only. Data visualizations are the hero — animated charts,
  counters, grids. Every frame snaps to a grid. Transitions are horizontal
  grid wipes. No organic shapes. No gradients. No stock photography.
  Everything is geometric, systematic, precise.

colors:
  primary:
    - name: "Pure Black"
      hex: "#000000"
      role: "dominant ground, text, structural elements"
    - name: "Pure White"
      hex: "#FFFFFF"
      role: "background fields, negative space"
  accent:
    - name: "Electric Blue"
      hex: "#0066FF"
      role: "the ONE accent — data highlights, key emphasis"
  neutral:
    - name: "Grid Gray"
      hex: "#CCCCCC"
      role: "grid lines, secondary structure"

typography:
  display:
    family: "Helvetica"
    weight: "bold"
    style: "uppercase or sentence case, tight tracking"
  body:
    family: "Helvetica"
    weight: "regular"
    style: "flush left, ragged right, generous leading"
  caption:
    family: "Helvetica"
    weight: "light"
    style: "small, uppercase, wide tracking"
  rules:
    - "Helvetica ONLY — no other typeface"
    - "Type sizes follow a mathematical scale"
    - "Always flush left — never centered"

layout:
  grid: "Strict modular grid — 12 columns"
  alignment: "Flush left, grid-snapped"
  aspect_ratio: "16:9"
  notes:
    - "Every element locked to the grid"
    - "Data visualizations are the hero elements"

motion:
  transitions:
    - "horizontal grid wipes"
    - "elements snapping to grid positions"
    - "clean hard cuts"
  animation_style: >
    Geometric precision. Elements snap to grid positions.
    Charts animate systematically. Nothing bounces.
  pacing: "Measured, confident, unhurried"

mood:
  keywords:
    - "precise"
    - "systematic"
    - "authoritative"
    - "geometric"
  era: "1950s–1970s (timeless)"
  cultural_reference: "Müller-Brockmann, Grid Systems in Graphic Design"
  avoid:
    - "organic or curved shapes"
    - "gradients"
    - "stock photography"
    - "centered text"
    - "decorative elements"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""
---

## Design Principles

Typography and the grid are the only design elements needed.
Mathematical relationships create visual harmony.
Restraint is the ultimate sophistication.

## Connectors

### HeyGen Video Agent
Use `style_prompt_full` verbatim. No avatar, no b-roll — pure motion graphics.
Hard cuts between scenes.

### HTML Slides
Map to CSS: `--color-bg: #000`, `--color-text: #FFF`, `--color-accent: #0066FF`.
Use Helvetica via system fonts or Google Fonts equivalent.
```

## 验证

一个有效的 `visual-style.md` 必须满足：

1. 在 `---` 分隔符之间有有效的 YAML 前置元数据
2. 包含所有必填字段
3. `colors.primary` 至少包含 2 个颜色对象
4. 每个颜色对象包含 `name`、`hex` 和 `role`
5. `version` 设置为 `1.0`

## 版本管理

`version` 字段指的是规范版本，而非风格版本。当规范发生变化时：

- **小版本变更**（新增可选字段）：版本保持 `1.0`
- **破坏性变更**（必填字段变更）：版本升至 `2.0`

## 设计决策

### 为什么 `style_prompt_full` 是必填项

许多 AI 工具只接受文本提示。通过要求提供完整的自然语言风格描述，我们确保每个 `visual-style.md` 文件可以立即被任何工具使用——即使是那些不解析结构化字段的工具。

### 为什么不嵌入二进制数据

URL 使文件保持小巧、可版本化且可移植。二进制资源应托管在外部并通过 URL 引用。

### 为什么用 `x_*` 命名空间

不同工具有不同的能力。`x_` 前缀允许工具特定配置而不污染核心模式。示例：`x_heygen`、`x_figma`、`x_paper`。

### 为什么有 `mood.avoid`

负面约束与正面约束同等重要。告诉 AI 什么**不要**做往往比告诉它做什么更有效。
