---
name: "Neville Brody 工业排版风格"
version: "1.0"
tags:
  - 标志性设计
  - 极简风格
author: "Teo @ HeyGen"
created: "2026-03-12"

style_prompt_short: >
  深色工业排版。压缩和扭曲的字母形式
  以受控的攻击性撞击破碎的网格。Brody
  80 年代末的广播粗粝遇上编辑张力。

style_prompt_full: >
  受 Neville Brody 80 年代末和 90 年代排版实验启发的深色实验性图形系统：
  工业质感、压缩和扩展的字母形式、媒体粗粝、破碎
  对齐和受控的攻击性。使用炭黑、钢灰、脏白、信号红和柔和电光蓝。排版
  应感觉工程化、扭曲且承载文化重量。文字
  应压缩、拉伸、分裂并以锋利的工业力量撞击网格。
  视觉和文字应碰撞而非礼貌地融合。
  裁剪的图像碎片、静态纹理和密集
  标签应通过粗粝的排版切割和广播般的断裂
  重新组装画面。动效应感觉媒体重、紧张
  且当代。

colors:
  primary:
    - name: "炭黑"
      hex: "#1A1A1A"
      role: "主导背景"
    - name: "脏白"
      hex: "#E0E0E0"
      role: "主要文字"
  accent:
    - name: "信号红"
      hex: "#CC3333"
      role: "强调，中断"
    - name: "柔和电光蓝"
      hex: "#4488AA"
      role: "次要强调"
  neutral:
    - name: "钢灰"
      hex: "#666666"
      role: "辅助文字，网格线"

typography:
  display:
    family: "压缩工业无衬线字体"
    weight: "超粗/黑色"
    style: "大写，极端压缩"
  body:
    family: "中性无衬线字体（Univers、Akzidenz-Grotesk）"
    weight: "常规到中等"
  caption:
    family: "等宽或压缩无衬线字体"
    style: "小号，密集，全大写"
  rules:
    - "文字本身就是视觉 — 与内容碰撞，而非放置在内容上"
    - "破碎对齐是有意的"
    - "混合极端字重"
    - "绝不居中 — 始终左对齐或破碎对齐"
    - "文字可以溢出画框"

layout:
  grid: "激进的不对称网格，有意打破"
  alignment: "左对齐，破碎离轴"
  aspect_ratio: "16:9"
  notes:
    - "密集 — 最小留白"
    - "裁剪的图像碎片作为纹理"
    - "标签感觉像广播控制室覆盖层"

motion:
  transitions:
    - "粗粝的排版切割"
    - "广播般的静态爆发"
    - "垂直/水平面板切换"
  animation_style: "文字撞击网格。无柔和缓动。元素碰撞。"
  pacing: "紧张、有节奏、受控"

mood:
  keywords:
    - "工业"
    - "有攻击性"
    - "编辑感"
    - "广播"
    - "紧张"
  era: "1980 年代末–1990 年代"
  cultural_reference: "Neville Brody，The Face 杂志，Arena，Fuse"
  avoid:
    - "柔和渐变或粉彩"
    - "居中布局"
    - "友好语气"
    - "圆润字体或手写体"
    - "装饰性插图"
    - "平滑缓动"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: "c22c70a499a048cfa67a1426313ec345"
  orientation: "landscape"
---

## Design Principles

排版不是装饰 — 它是建筑。
张力创造注意力。
有意打破网格。
每一次碰撞都是精心设计的。

## Connectors

### HeyGen Video Agent
逐字使用 `style_prompt_full`。强调：粗粝切割、静态纹理、
撞击画面的文字。无平滑过渡。广播控制室美学。

### HTML Slides
深色背景 (#1A1A1A)。溢出边缘的压缩字体。
不对称布局。红色强调用于突出。密集信息展示。

### paper.design
有意打破网格。让文字与边缘碰撞。
使用图像碎片，而非完整照片。控制室覆盖层美学。

### Figma
颜色样式：`brand/charcoal`、`brand/dirty-white`、`accent/signal-red`、`accent/electric-blue`。
文本样式：展示用压缩黑色字重。允许文字超出框架。
