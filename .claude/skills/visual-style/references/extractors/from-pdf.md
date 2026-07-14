# 从 PDF / 品牌指南提取

从 PDF 品牌指南或风格文档生成 `visual-style.md`。

## 工作流程

1. **接收 PDF** — 用户上传品牌指南、风格指南或设计文档
2. **解析章节** — 识别颜色、排版、布局和指南章节
3. **映射到字段** — 将品牌指南规范转换为 visual-style.md 字段
4. **填补空缺** — 从结构化数据生成 `style_prompt_full`
5. **输出** — 完整的 `visual-style.md`
6. **验证** — 确保所有必填字段齐全

## 常见品牌指南章节

| 品牌指南章节 | 映射到 |
|-------------|--------|
| 品牌概述/使命 | `style_prompt_short`, `mood.keywords` |
| 调色板 | `colors.*` |
| 主色 | `colors.primary` |
| 次要/强调色 | `colors.accent` |
| 排版 | `typography.*` |
| 标题 | `typography.display` |
| 正文 | `typography.body` |
| 网格系统 | `layout.grid` |
| 间距 | `layout.notes` |
| 应与不应 | `typography.rules`, `mood.avoid` |
| 语气与口吻 | `mood.keywords`, `style_prompt_full` |
| 摄影风格 | `mood.keywords`, `mood.avoid` |
| 图标设计 | `style_prompt_full` |

## 提取提示

解析品牌指南 PDF 时使用此提示：

```
Parse this brand guide PDF and generate a visual-style.md.

Map the brand guide sections to visual-style.md fields:

REQUIRED:
- name: Brand name + "Brand Style"
- version: "1.0"
- style_prompt_short: Synthesize from brand overview/mission
- style_prompt_full: Combine ALL visual specifications into a coherent
  generation prompt. Include specific hex codes, font names, spacing
  values, and design principles.
- colors.primary: From "Primary Colors" section

FROM COLOR SECTIONS:
- colors.primary: Primary palette (convert all color specs to hex)
- colors.accent: Secondary/accent colors
- colors.neutral: Grays, backgrounds, supporting colors

FROM TYPOGRAPHY SECTIONS:
- typography.display: Headline font specs
- typography.body: Body copy font specs
- typography.caption: Caption/label specs (if defined)
- typography.rules: Any typography guidelines or restrictions

FROM LAYOUT SECTIONS:
- layout.grid: Grid system specifications
- layout.alignment: Alignment rules
- layout.notes: Spacing, margins, padding guidelines

FROM GUIDELINES SECTIONS:
- mood.keywords: Extract from voice/tone/personality sections
- mood.avoid: Extract from "Don't" lists, incorrect usage examples

Be precise:
- Convert all color specifications to hex (RGB, CMYK, Pantone → hex)
- Use exact font family names as specified
- Include specific measurements where given
- Preserve the brand's stated values in style_prompt_full

Output format:
Complete YAML frontmatter between --- delimiters
Plus Markdown body sections (## Design Principles from brand philosophy)
```

## 颜色转换参考

品牌指南通常以多种格式指定颜色：

| 格式 | 示例 | 十六进制转换 |
|------|------|-------------|
| Hex | #FF5500 | 直接使用 |
| RGB | 255, 85, 0 | → #FF5500 |
| CMYK | 0, 67, 100, 0 | 近似到十六进制 |
| Pantone | PMS 021 C | 查找十六进制等价 |
| HSL | 20°, 100%, 50% | 转换为十六进制 |

对于 Pantone 颜色，使用官方的 Pantone 到十六进制映射，或在 `role` 字段中注明 Pantone 代码。

## 示例输出

给定企业品牌指南 PDF：

```yaml
---
name: "Acme Corp Brand Style"
version: "1.0"
tags:
  - corporate
  - technology
author: "Extracted from Acme Brand Guidelines v2.3"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  Professional tech brand with bold blue accents.
  Clean, trustworthy, forward-thinking.

style_prompt_full: >
  Acme Corp brand style. Professional technology company aesthetic.
  Primary blue (#0052CC) for brand elements, CTAs, and emphasis.
  Navy (#172B4D) for headings and high-contrast text. Clean white
  (#FFFFFF) backgrounds with generous whitespace. Neutral grays
  for supporting content. Typography uses Roboto for digital
  and Avenir for print — clean, geometric sans-serifs that convey
  precision. 8-point spacing grid. Rounded corners (4px) on
  interactive elements. Photography should be authentic, diverse,
  and optimistic — no stock photo clichés. Iconography is outlined,
  2px stroke, rounded caps. Professional but approachable. Never
  corporate-stuffy or overly playful.

colors:
  primary:
    - name: "Acme Blue"
      hex: "#0052CC"
      role: "primary brand color, CTAs, links"
    - name: "Navy"
      hex: "#172B4D"
      role: "headings, high-contrast text"
  accent:
    - name: "Success Green"
      hex: "#36B37E"
      role: "positive states, confirmations"
    - name: "Warning Yellow"
      hex: "#FFAB00"
      role: "warnings, attention"
    - name: "Error Red"
      hex: "#DE350B"
      role: "errors, destructive actions"
  neutral:
    - name: "White"
      hex: "#FFFFFF"
      role: "primary background"
    - name: "Light Gray"
      hex: "#F4F5F7"
      role: "secondary backgrounds, cards"
    - name: "Mid Gray"
      hex: "#6B778C"
      role: "secondary text, placeholders"
    - name: "Dark Gray"
      hex: "#42526E"
      role: "body text"

typography:
  display:
    family: "Roboto"
    weight: "700"
    style: "sentence case, -0.02em tracking"
  body:
    family: "Roboto"
    weight: "400"
    style: "16px base, 1.5 line height"
  caption:
    family: "Roboto"
    weight: "500"
    style: "12px, uppercase for labels"
  rules:
    - "Roboto for all digital applications"
    - "Avenir for print materials"
    - "Minimum body text size: 14px"
    - "Maximum line length: 75 characters"
    - "Use Medium (500) weight for emphasis, not bold"

layout:
  grid: "8-point grid, 12 columns"
  alignment: "Left-aligned text, center-aligned hero content"
  aspect_ratio: "16:9 for presentations"
  notes:
    - "Minimum margin: 24px (mobile), 48px (desktop)"
    - "Standard spacing: 8, 16, 24, 32, 48, 64px"
    - "Card border-radius: 4px"
    - "Button border-radius: 4px"

motion:
  transitions:
    - "ease-out, 200ms for micro-interactions"
    - "ease-in-out, 300ms for page transitions"
  animation_style: "Subtle, purposeful. Animation should clarify, not decorate."
  pacing: "Quick, responsive feedback"

mood:
  keywords:
    - "professional"
    - "trustworthy"
    - "innovative"
    - "approachable"
    - "precise"
  era: "Contemporary tech (2020s)"
  cultural_reference: "Enterprise SaaS, developer tools"
  avoid:
    - "overly playful or casual tone"
    - "generic stock photography"
    - "gradients on brand elements"
    - "more than 3 colors in one composition"
    - "centered body text"
    - "all-caps body text"
    - "drop shadows deeper than 2px"

assets:
  reference_images: []
  color_palette_image:
    url: ""
---

## Design Principles

From Acme Brand Guidelines:

1. **Clarity over cleverness** — Communication should be immediately understood
2. **Consistency builds trust** — Every touchpoint reinforces the brand
3. **Purposeful restraint** — Add only what adds value
4. **Accessible by default** — Design for everyone

## Extraction Notes

Extracted from "Acme Brand Guidelines v2.3" (PDF, 48 pages).
Color values converted from Pantone specifications.
Typography mapped from "Digital Standards" section.
Do's and Don'ts synthesized into mood.avoid list.
```

## 提示

- **优先精确性** — 品牌指南是精确的；保留确切的值
- **不要编造** — 如果 PDF 中没有该章节，保持字段为空
- **综合 style_prompt_full** — 这应该读起来像你给设计师的简报
- **捕捉"不应"** — `mood.avoid` 通常在品牌指南中明确说明
- **记录来源** — 在提取说明中包含页码或章节名称
