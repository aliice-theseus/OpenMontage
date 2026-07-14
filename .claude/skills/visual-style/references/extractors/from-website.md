# 从网站提取

从网站 URL 生成 `visual-style.md`。

## 工作流程

1. **接收 URL** — 用户提供网站 URL
2. **获取页面** — 使用网页抓取获取 HTML/CSS
3. **截取屏幕截图** — 如果可能，捕获页面的视觉效果
4. **分析** — 识别颜色、排版、布局、动效、氛围
5. **生成** — 输出完整的 `visual-style.md`
6. **验证** — 确保所有必填字段齐全

## 提取提示

分析网站时使用此提示模板：

```
Analyze this website and extract a visual-style.md following the spec.

URL: [URL]

Identify and output these fields:

REQUIRED:
- name: A descriptive name for this style (e.g., "[Brand] Web Style")
- version: "1.0"
- style_prompt_short: 1-2 sentence hook capturing the visual essence
- style_prompt_full: Detailed generation prompt with specific:
  - Hex color codes (use exact values, don't guess)
  - Font family names (check the CSS)
  - Layout structure (grid system, spacing patterns)
  - Motion patterns (animations, transitions)
  - Overall mood and feel
- colors.primary: At least 2 colors with name, hex, role

RECOMMENDED:
- colors.accent: Accent colors with name, hex, role
- colors.neutral: Neutral/gray colors with name, hex, role
- typography.display: Heading font family, weight, style
- typography.body: Body font family, weight, style
- typography.caption: Caption/label font family, weight, style
- typography.rules: Typography constraints and patterns
- layout.grid: Grid system description
- layout.alignment: Alignment patterns
- layout.notes: Additional layout observations
- motion.transitions: Transition types used
- motion.animation_style: Overall animation approach
- mood.keywords: 4-6 mood/feeling words
- mood.era: Design era reference
- mood.avoid: Anti-patterns to avoid

Be specific:
- Use exact hex values from the CSS, not approximations
- Name every color descriptively (not "Blue 1", but "Ocean Blue")
- Describe the role of each color in the system
- Note any custom fonts and their fallbacks

Output format:
Complete YAML frontmatter between --- delimiters
Plus Markdown body sections (## Design Principles, ## Extraction Notes)
```

## 分析检查清单

提取时，注意查找：

### 颜色
- [ ] 背景色（主要表面）
- [ ] 文字颜色（标题 vs 正文）
- [ ] 强调色/CTA 按钮颜色
- [ ] 链接颜色（默认、悬停、已访问）
- [ ] 边框/分割线颜色
- [ ] 渐变使用（如有）

### 排版
- [ ] 标题字体族
- [ ] 正文字体族
- [ ] 使用的字重（light、regular、bold 等）
- [ ] 文字大小（标题比例）
- [ ] 行高
- [ ] 字间距模式
- [ ] 文字变换（大写、小写）

### 布局
- [ ] 最大内容宽度
- [ ] 网格列数（如可见）
- [ ] 间距节奏（一致的间隙）
- [ ] 对齐模式（左、中、混合）
- [ ] 卡片/组件模式
- [ ] 负空间使用

### 动效
- [ ] 页面过渡
- [ ] 悬停效果
- [ ] 滚动动画
- [ ] 加载状态
- [ ] 微交互

### 氛围
- [ ] 整体感觉（专业、趣味、简约、大胆）
- [ ] 设计时代（现代、复古、永恒）
- [ ] 品牌个性（严肃、友好、技术感）
- [ ] 他们明确避免什么

## 示例输出

给定 URL `https://stripe.com`：

```yaml
---
name: "Stripe Web Style"
version: "1.0"
tags:
  - fintech
  - sleek minimal
author: "Extracted"
source_url: "https://stripe.com"
created: "2026-03-12"

style_prompt_short: >
  Clean fintech minimalism with deep purple accents on white.
  Generous whitespace, clear typography, subtle gradients.

style_prompt_full: >
  Modern fintech design inspired by Stripe. Clean white backgrounds
  with generous whitespace. Deep purple (#635BFF) as the primary
  accent color. Typography uses a custom geometric sans-serif
  (similar to Inter or Söhne) with clear hierarchy. Subtle mesh
  gradients in backgrounds. Rounded corners on cards and buttons.
  Smooth, subtle animations on scroll. Professional, trustworthy,
  approachable. No harsh colors, no busy patterns, no stock photos.

colors:
  primary:
    - name: "Pure White"
      hex: "#FFFFFF"
      role: "primary background, negative space"
    - name: "Slate Dark"
      hex: "#0A2540"
      role: "primary text, headings"
  accent:
    - name: "Stripe Purple"
      hex: "#635BFF"
      role: "CTAs, links, brand accent"
    - name: "Cyan Accent"
      hex: "#00D4FF"
      role: "secondary accent, gradients"
  neutral:
    - name: "Slate Gray"
      hex: "#425466"
      role: "body text, secondary content"
    - name: "Light Gray"
      hex: "#F6F9FC"
      role: "section backgrounds, cards"

typography:
  display:
    family: "Söhne, Inter, system-ui"
    weight: "600"
    style: "sentence case, tight tracking"
  body:
    family: "Söhne, Inter, system-ui"
    weight: "400"
    style: "generous line height, comfortable reading"
  caption:
    family: "Söhne Mono, monospace"
    weight: "400"
    style: "code blocks, technical details"
  rules:
    - "Clear size hierarchy: 64px → 48px → 32px → 24px → 16px"
    - "Generous line heights for readability"
    - "Monospace for code and technical content"

layout:
  grid: "12 columns, max-width 1200px"
  alignment: "Center-aligned sections, left-aligned text"
  aspect_ratio: "16:9 for hero, varied for content"
  notes:
    - "Generous vertical spacing between sections"
    - "Cards with subtle shadows and rounded corners"
    - "Alternating section backgrounds"

motion:
  transitions:
    - "subtle fade-in on scroll"
    - "smooth hover state transitions (0.2s)"
    - "parallax on hero backgrounds"
  animation_style: "Subtle, smooth, professional. Nothing bouncy or playful."
  pacing: "Measured, confident transitions"

mood:
  keywords:
    - "professional"
    - "trustworthy"
    - "clean"
    - "modern"
    - "approachable"
  era: "2020s fintech"
  cultural_reference: "Modern SaaS, developer-focused design"
  avoid:
    - "harsh or neon colors"
    - "busy patterns or textures"
    - "stock photography"
    - "overly playful animations"
    - "dark mode (unless requested)"

assets:
  reference_images: []
  color_palette_image:
    url: ""
---

## Design Principles

Trust through clarity. Every element earns its place. Typography and whitespace
do the heavy lifting. Color is used sparingly and intentionally.

## Extraction Notes

Extracted from https://stripe.com on 2026-03-12.
Primary purple sampled from CTA buttons.
Typography stack identified via browser dev tools.
Mesh gradient patterns noted in hero sections.
```

## 提示

- **使用开发者工具** — 检查元素以获取精确的十六进制值和字体栈
- **检查 CSS 变量** — 许多网站在 `:root` 中定义调色板
- **记录响应式模式** — 设计如何适配？
- **捕捉感觉** — `style_prompt_full` 应唤起相同的感觉
- **具体说明避免项** — 该品牌明确**不**做什么？
