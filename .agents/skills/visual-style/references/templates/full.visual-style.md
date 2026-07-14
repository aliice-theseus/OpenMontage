---
name: "风格名称"
version: "1.0"
tags:
  - 标签1
  - 标签2
author: "您的名字"
source_url: ""
created: "YYYY-MM-DD"

style_prompt_short: >
  捕捉此风格视觉精髓的一到两句话。
  这是电梯演讲。

style_prompt_full: >
  详细的生成提示。包括具体的十六进制颜色、字体名称、
  布局结构、动效模式和整体氛围。这是最重要的
  字段 — 任何 AI 工具都应能读取此内容并生成
  一致的视觉效果。具体说明要做什么和不要做什么。
  包括内联的十六进制码（如 #FF5500），以便工具可以提取它们。

colors:
  primary:
    - name: "描述性颜色名称"
      hex: "#000000"
      role: "主导背景、结构元素"
    - name: "描述性颜色名称"
      hex: "#FFFFFF"
      role: "主要文字、留白空间"
  accent:
    - name: "强调色名称"
      hex: "#FF5500"
      role: "行动号召、强调、关键高亮"
  neutral:
    - name: "中性色名称"
      hex: "#888888"
      role: "辅助文字、边框、次级元素"

typography:
  display:
    family: "字体族名称"
    weight: "bold"
    style: "大写，紧凑字距"
  body:
    family: "字体族名称"
    weight: "regular"
    style: "句首大写，舒适行高"
  caption:
    family: "字体族名称"
    weight: "medium"
    style: "小号，标签大写"
  rules:
    - "排版规则或约束"
    - "另一条排版指南"
    - "字体使用限制"

layout:
  grid: "网格系统描述（例如 12 列，8px 基础单位）"
  alignment: "对齐方式（例如左对齐，居中主角）"
  aspect_ratio: "默认宽高比（例如 16:9、4:3）"
  notes:
    - "额外布局指南"
    - "间距或构图说明"

motion:
  transitions:
    - "过渡类型 1"
    - "过渡类型 2"
  animation_style: >
    元素如何移动和动画的描述。包括缓动、
    时间和整体感觉。
  pacing: "整体节奏描述"
  audio_cues:
    - "声音设计说明"

mood:
  keywords:
    - "氛围词 1"
    - "氛围词 2"
    - "氛围词 3"
    - "氛围词 4"
  era: "时代参考（例如 1990 年代，当代）"
  cultural_reference: "激发此风格的设计师、运动或作品"
  avoid:
    - "明确避免的内容"
    - "另一个反模式"
    - "不适配的设计元素"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: ""
  orientation: "landscape"

x_figma:
  library_id: ""
---

## Design Principles

用于设计哲学和指导原则的自由格式章节。
什么信念驱动这个视觉系统？
它有意做出了哪些权衡？

## Connectors

### HeyGen Video Agent
关于如何将此风格应用于 HeyGen Video Agent 的说明。
在提示中强调什么、使用什么动效模式。

### HTML Slides
关于 CSS 映射、布局方法、字体加载的说明。

### paper.design
关于文档设置、网格配置、AI 指导的说明。

### Figma
关于样式生成、组件模式、设计令牌的说明。

## Extraction Notes

如果此风格是从某个来源提取的，请在此记录。
包括来源 URL、提取日期和任何值得注意的决策。
