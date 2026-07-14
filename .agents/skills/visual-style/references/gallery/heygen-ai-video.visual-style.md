---
name: "HeyGen AI 视频平台"
version: "1.0"
tags:
  - AI
  - 视频
  - 科技
  - 现代
author: "提取"
source_url: "https://heygen.com"
created: "2026-03-12"

style_prompt_short: >
  充满活力的 AI 前沿设计。青色到粉色渐变能量在干净的白色上。
  平易近人的科技感，高级但不冷淡。

style_prompt_full: >
  受 HeyGen 启发的现代 AI 视频平台美学。干净的白色
  背景配宽敞留白。标志性的青粉渐变（#00C3FF 到 #95AAFE 到 #FEA5FE）
  作为主角视觉元素。主要强调色是 Hey Blue (#00C3FF)，
  用于行动号召和交互元素。Prism Pink (#F3A6FF)
  作为次要强调色，用于强调和温暖感。排版
  使用几何无衬线字体（ABC Solar、TT Norms Pro 或类似字体），
  具有清晰层级。卡片和按钮的大圆角（12-48px）。
  平滑的淡入动画和微妙的悬停过渡。科技前沿
  但平易近人 — 创新遇上可访问性。避免刺眼的企业蓝、
  除非特别要求否则避免暗色模式、避免过于
  复杂的渐变或 3D 效果。

colors:
  primary:
    - name: "纯白"
      hex: "#FFFFFF"
      role: "主要背景，干净画布"
    - name: "碳黑"
      hex: "#333333"
      role: "主要文字，标题"
  accent:
    - name: "Hey Blue"
      hex: "#00C3FF"
      role: "行动号召、链接、主要品牌强调"
    - name: "Prism Pink"
      hex: "#F3A6FF"
      role: "次要强调，渐变端点，强调"
    - name: "Gen Green"
      hex: "#35C838"
      role: "成功状态，正面反馈"
  neutral:
    - name: "薄雾"
      hex: "#F2F2F2"
      role: "章节背景，卡片"
    - name: "云"
      hex: "#D9D9D9"
      role: "边框，分割线"
    - name: "深青"
      hex: "#033337"
      role: "深色背景，页脚，对比章节"

typography:
  display:
    family: "ABC Solar, TT Norms Pro, system-ui"
    weight: "700-800"
    style: "大号，自信，宽松字距"
  body:
    family: "TT Norms Pro, system-ui, sans-serif"
    weight: "400-500"
    style: "舒适阅读，18px 基础"
  caption:
    family: "TT Norms Pro, system-ui, sans-serif"
    weight: "500"
    style: "14-15px，中等字重用于标签"
  rules:
    - "大小比例：80px → 60px → 44px → 32px → 24px → 18px → 14px"
    - "宽行高以确保可读性"
    - "UI 元素用中等字重（500-600）"
    - "粗体（700-800）仅用于标题"

layout:
  grid: "12 列，最大宽度 1200px，基于 flex"
  alignment: "居中章节，左对齐内容"
  aspect_ratio: "视频内容 16:9，功能展示多变"
  notes:
    - "4px 基础间距单位（8, 16, 24, 32, 40, 60, 80px 比例）"
    - "大圆角：卡片 12px，按钮 20px，主角元素 48px"
    - "宽敞内边距：内部 16-24px，章节间距 60-120px"
    - "卡片带微妙边框，最小阴影"

motion:
  transitions:
    - "fadeInUp（300ms）内容揭示"
    - "slideDown（250ms）下拉菜单"
    - "平滑悬停过渡（150-200ms）"
  animation_style: >
    平滑而现代。元素优雅地淡入和滑入。
    悬停时微妙的缩放效果。无弹跳或俏皮 —
    自信且专业，带有一丝精致。
  pacing: "快速、响应式、现代感"
  audio_cues:
    - "电子环境音"
    - "现代企业风"
    - "积极但专业"

mood:
  keywords:
    - "创新"
    - "平易近人"
    - "高级"
    - "现代"
    - "创意"
    - "科技前沿"
  era: "2020 年代 AI/SaaS"
  cultural_reference: "现代 AI 工具，创意科技平台，Figma/Notion 能量"
  avoid:
    - "刺眼的企业蓝"
    - "深色沉重界面"
    - "过于复杂的 3D 效果"
    - "图库摄影感"
    - "杂乱布局"
    - "小而拥挤的排版"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  brand_gradient: "linear-gradient(328deg, #00c3ff, #95aafe 50%, #fea5fe)"
  orientation: "landscape"
---

## Design Principles

AI 应感觉可访问，而非令人生畏。
留白传达高品质。
青粉渐变是主角 — 克制但大胆地使用它。
每次交互都应感觉平滑且响应迅速。

## Extraction Notes

于 2026-03-12 从 https://heygen.com 提取。
主色从 CSS 变量和品牌指南采样。
通过计算样式识别排版（ABC Solar、TT Norms Pro）。
渐变从主角区域和品牌元素提取。
间距系统遵循 4px 基础单位模式。

## Connectors

### HeyGen Video Agent
将标志性渐变用作背景或覆盖元素。
Hey Blue 用于文字强调和行动号召。干净的白色背景。
现代、自信的节奏。平易近人的 AI 能量。

### HTML Slides
白色背景配渐变强调条或主角元素。
卡片上的大圆角。宽敞的留白。
Hey Blue 用于交互元素，Prism Pink 用于高亮。

### paper.design
用渐变作为大胆强调元素的干净布局。
具有清晰层级的大号排版。圆角卡片模式。
避免沉重阴影 — 改用微妙边框。

### Figma
颜色样式：`brand/hey-blue`、`brand/prism-pink`、`brand/gradient`。
遵循 80-60-44-32-24-18-14px 比例的文本样式。
大边框半径（12-48px）的组件变体。
