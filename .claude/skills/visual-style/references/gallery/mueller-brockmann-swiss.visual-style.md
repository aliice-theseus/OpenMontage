---
name: "Josef Müller-Brockmann 瑞士国际风格"
version: "1.0"
tags:
  - 标志性设计
  - 时尚简约
author: "Bin"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  网格锁定的瑞士精度。黑白基底搭配电蓝
  强调色。仅用 Helvetica。数据可视化作为主角。
  每一帧都对齐数学网格。几何、系统、精确。

style_prompt_full: >
  Josef Müller-Brockmann 瑞士国际风格。数学精度的
  网格锁定布局。黑白基底搭配一种强调色
  （电蓝 #0066FF）。强烈的对角线构图。仅使用 Helvetica
  字体。数据可视化是主角——动画图表、
  计数器、网格。每一帧都对齐网格。过渡为水平
  网格擦除。无有机形状。无渐变。无素材照片。
  一切都是几何的、系统的、精确的。

colors:
  primary:
    - name: "纯黑"
      hex: "#000000"
      role: "主导底色，文字，结构元素"
    - name: "纯白"
      hex: "#FFFFFF"
      role: "背景区域，负空间"
  accent:
    - name: "电蓝"
      hex: "#0066FF"
      role: "唯一强调色——数据高亮，关键强调"
  neutral:
    - name: "网格灰"
      hex: "#CCCCCC"
      role: "网格线，辅助结构"
    - name: "深灰"
      hex: "#333333"
      role: "辅助文字，次要标签"

typography:
  display:
    family: "Helvetica"
    weight: "bold"
    style: "大写或句首大写，紧排"
  body:
    family: "Helvetica"
    weight: "regular"
    style: "左对齐，右缘不齐，宽松行距"
  caption:
    family: "Helvetica"
    weight: "light"
    style: "小号，大写，宽排"
  rules:
    - "仅用 Helvetica——无其他字体"
    - "字号遵循数学比例"
    - "始终左对齐——绝不居中"
    - "字重对比实现层级"

layout:
  grid: "严格模块化网格——12 列"
  alignment: "左对齐，网格吸附"
  aspect_ratio: "16:9"
  notes:
    - "每个元素都锁定在网格上"
    - "在正交网格内做强烈对角线构图"
    - "数据可视化是主角"

motion:
  transitions:
    - "水平网格擦除"
    - "元素吸附到网格位置"
    - "清晰硬切"
  animation_style: >
    几何精度。元素吸附到网格位置。图表系统化动画。
    计数器机械跳动。无弹跳效果。
  pacing: "有节奏，自信，从容"

mood:
  keywords:
    - "精确"
    - "系统"
    - "权威"
    - "几何"
  era: "1950s–1970s（永恒）"
  cultural_reference: "Müller-Brockmann, 平面设计网格系统, 苏黎世学派"
  avoid:
    - "有机或曲线形状"
    - "渐变"
    - "素材照片"
    - "超过一种强调色"
    - "居中文字"
    - "装饰性元素"
    - "手写或衬线字体"
    - "投影或发光"
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

## 设计原则

排版和网格是唯二需要的设计元素。
数学关系创造视觉和谐。
克制是极致的优雅。
网格不是限制——它是通过结构获得的解放。

## 连接器

### HeyGen 视频代理
逐字使用 `style_prompt_full`。指定：无虚拟形象，无 B 卷——纯动态图形。
场景间硬切。数据可视化应有系统化动画。

### HTML 幻灯片
CSS 变量：`--color-bg: #000`、`--color-text: #FFF`、`--color-accent: #0066FF`。
所有文字左对齐。12 列网格。Helvetica 或系统无衬线后备字体。

### paper.design
设置 12 列网格。背景黑色，文字白色。单一强调色。
每个元素应对齐网格交点。

### Figma
颜色样式：`brand/black`、`brand/white`、`accent/electric-blue`、`neutral/grid-gray`。
文本样式：`heading/display`（Helvetica Bold）、`body/default`（Helvetica Regular）。
布局网格：12 列，严格对齐。
