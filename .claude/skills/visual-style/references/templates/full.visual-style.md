---
name: "风格名称"
version: "1.0"
tags:
  - 标签1
  - 标签2
author: "你的名字"
source_url: ""
created: "YYYY-MM-DD"

style_prompt_short: >
  一到两句话捕捉此风格的视觉精髓。
  这是电梯游说。

style_prompt_full: >
  详细的生成提示。包括具体的十六进制颜色、字体名称、
  布局结构、动效模式和整体氛围。这是最重要的
  字段——任何 AI 工具都应能读取此字段并生成
  一致的视觉效果。具体说明该做什么和不该做什么。
  内联包含十六进制代码（如 #FF5500），以便工具提取。

colors:
  primary:
    - name: "描述性颜色名称"
      hex: "#000000"
      role: "主背景，结构元素"
    - name: "描述性颜色名称"
      hex: "#FFFFFF"
      role: "主要文字，负空间"
  accent:
    - name: "强调色名称"
      hex: "#FF5500"
      role: "CTA、重点、关键高亮"
  neutral:
    - name: "中性色名称"
      hex: "#888888"
      role: "辅助文字、边框、次要元素"

typography:
  display:
    family: "字体族名称"
    weight: "bold"
    style: "uppercase, tight tracking"
  body:
    family: "字体族名称"
    weight: "regular"
    style: "sentence case, comfortable line height"
  caption:
    family: "字体族名称"
    weight: "medium"
    style: "small, uppercase for labels"
  rules:
    - "排版规则或约束"
    - "另一条排版指南"
    - "字体使用限制"

layout:
  grid: "网格系统描述（例如 12 列，8px 基本单位）"
  alignment: "对齐方式（例如 flush left, centered hero）"
  aspect_ratio: "默认宽高比（例如 16:9, 4:3）"
  notes:
    - "额外布局指南"
    - "间距或构图说明"

motion:
  transitions:
    - "过渡类型 1"
    - "过渡类型 2"
  animation_style: >
    描述元素如何移动和动画。包括缓动函数、
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
  era: "时代参考（例如 1990s, contemporary）"
  cultural_reference: "启发此风格的设计师、运动或作品"
  avoid:
    - "需明确避免的内容"
    - "另一个反模式"
    - "不匹配的设计元素"

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

## 设计原则

设计理念和指导原则的自由格式部分。
什么信念驱动这个视觉系统？
它有意做了哪些权衡？

## 连接器

### HeyGen 视频代理
关于如何将此风格应用于 HeyGen 视频代理的说明。
在提示中应强调什么，使用什么动效模式。

### HTML 幻灯片
关于 CSS 映射、布局方法、字体加载的说明。

### paper.design
关于文档设置、网格配置、AI 指导的说明。

### Figma
关于风格生成、组件模式、设计令牌的说明。

## 提取说明

如果此风格是从某个来源提取的，请在此记录。
包括来源 URL、提取日期以及任何重要决策。
