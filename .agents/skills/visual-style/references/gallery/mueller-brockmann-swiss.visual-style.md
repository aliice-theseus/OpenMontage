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
  每一帧都对齐到数学网格。几何、系统、精确。

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
      role: "网格线、次要结构"
    - name: "深灰"
      hex: "#333333"
      role: "辅助文字、次要标签"

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
    - "字重对比决定层级"

layout:
  grid: "严格的模块化网格 — 12 列"
  alignment: "左对齐，对齐到网格"
  aspect_ratio: "16:9"
  notes:
    - "每个元素锁定到网格"
    - "在正交网格内的大胆对角线构图"
    - "数据可视化是主角元素"

motion:
  transitions:
    - "水平网格擦拭"
    - "元素对齐到网格位置"
    - "干净硬切"
  animation_style: >
    几何精度。元素对齐到网格位置。图表系统化地
    动画。计数器机械地跳动。没有什么会弹跳。
  pacing: "沉稳、自信、不慌不忙"

mood:
  keywords:
    - "精确"
    - "系统化"
    - "权威"
    - "几何"
  era: "1950–1970 年代（永恒）"
  cultural_reference: "Müller-Brockmann，《平面设计中的网格系统》，苏黎世学派"
  avoid:
    - "有机或曲线形状"
    - "渐变"
    - "图库摄影"
    - "超过一种强调色"
    - "居中文字"
    - "装饰元素"
    - "手写或衬线字体"
    - "投影或辉光"
    - "圆角"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: ""
  orientation: "landscape"
---

## Design Principles

排版和网格是唯一需要的设计元素。
数学关系创造视觉和谐。
克制是终极的优雅。
网格不是限制 — 它是通过结构获得的解放。

## Connectors

### HeyGen Video Agent
逐字使用 `style_prompt_full`。指定：无虚拟角色，无 B 卷 — 纯动态图形。
场景之间硬切。数据可视化应系统化地动画。

### HTML Slides
CSS 变量：`--color-bg: #000`、`--color-text: #FFF`、`--color-accent: #0066FF`。
所有文字左对齐。12 列网格。Helvetica 或系统无衬线后备字体。

### paper.design
设置 12 列网格。背景黑色，文字白色。单一强调色。
每个元素应对齐到网格交叉点。

### Figma
颜色样式：`brand/black`、`brand/white`、`accent/electric-blue`、`neutral/grid-gray`。
文本样式：`heading/display`（Helvetica Bold）、`body/default`（Helvetica Regular）。
布局网格：12 列，严格对齐。
