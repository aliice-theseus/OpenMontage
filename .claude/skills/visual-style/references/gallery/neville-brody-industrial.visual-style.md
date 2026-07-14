---
name: "Neville Brody 工业字体风格"
version: "1.0"
tags:
  - 标志性设计
  - 时尚简约
author: "Teo @ HeyGen"
created: "2026-03-12"

style_prompt_short: >
  暗黑工业排版。压缩和扭曲的字形以受控的侵略性
  撞击破碎的网格。Brody 80年代末的广播粗粝感
  遇上编辑张力。

style_prompt_full: >
  一个受 Neville Brody 80年代末至90年代排版实验启发的
  黑暗实验性图形系统：工业质感、压缩和扩展的字形、
  媒体粗粝感、破碎的对齐方式以及受控的侵略性。
  使用炭黑、钢灰、脏白、信号红和柔和电蓝。排版
  应感觉像工程产物、扭曲且有文化负荷。文字
  应压缩、拉伸、分裂并以锋利的工业力量撞击网格。
  视觉和文字应相互碰撞而非礼貌地融合。
  裁剪的图像碎片、静态纹理和密集的
  标签应通过粗糙的排版切割和广播式的断裂
  重新组合画面。动效应感觉媒体感强、紧张
  且当代。

colors:
  primary:
    - name: "炭黑"
      hex: "#1A1A1A"
      role: "主要背景"
    - name: "脏白"
      hex: "#E0E0E0"
      role: "主要文字"
  accent:
    - name: "信号红"
      hex: "#CC3333"
      role: "强调，破坏"
    - name: "柔和电蓝"
      hex: "#4488AA"
      role: "辅助强调色"
  neutral:
    - name: "钢灰"
      hex: "#666666"
      role: "辅助文字，网格线"

typography:
  display:
    family: "紧凑工业无衬线"
    weight: "超粗 / 黑色"
    style: "大写，极度压缩"
  body:
    family: "中性无衬线 (Univers, Akzidenz-Grotesk)"
    weight: "常规到中等"
  caption:
    family: "等宽或紧凑无衬线"
    style: "小号，密集，全大写"
  rules:
    - "文字就是视觉本身——与内容碰撞，而非置于其上"
    - "破碎的对齐是故意的"
    - "混合极端字重"
    - "绝不居中——始终左对齐或破碎对齐"
    - "文字可以溢出画框"

layout:
  grid: "侵略性不对称网格，故意打破"
  alignment: "左对齐，破碎偏移"
  aspect_ratio: "16:9"
  notes:
    - "密集——最小留白"
    - "裁剪的图像碎片作为纹理"
    - "标签感觉像广播控制室叠加层"

motion:
  transitions:
    - "粗糙的排版切割"
    - "广播式静态爆裂"
    - "垂直/水平面板交换"
  animation_style: "文字撞击网格。无柔和缓动。元素碰撞。"
  pacing: "紧张，有节奏，可控"

mood:
  keywords:
    - "工业"
    - "侵略性"
    - "编辑风"
    - "广播"
    - "紧张"
  era: "1980年代末–1990年代"
  cultural_reference: "Neville Brody, The Face 杂志, Arena, Fuse"
  avoid:
    - "柔和渐变或粉彩"
    - "居中布局"
    - "友好语气"
    - "圆角字体或手写体"
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

## 设计原则

排版不是装饰——它是建筑。
张力创造注意力。
有意打破网格。
每一次碰撞都是编排好的。

## 连接器

### HeyGen 视频代理
逐字使用 `style_prompt_full`。强调：粗糙切割、静态纹理、
撞击画面的文字。无平滑过渡。广播控制室美学。

### HTML 幻灯片
深色背景（#1A1A1A）。溢出边缘的紧凑字体。
不对称布局。红色强调色。密集信息展示。

### paper.design
故意打破网格。让文字与边缘碰撞。
使用图像碎片而非完整照片。控制室叠加美学。

### Figma
颜色样式：`brand/charcoal`、`brand/dirty-white`、`accent/signal-red`、`accent/electric-blue`。
文本样式：展示用紧凑黑色字重。允许文字超出框架。
