---
name: "Saul Bass 电影标题风格"
version: "1.0"
tags:
  - 标志性设计
  - 电影感
author: "视觉风格图库"
created: "2026-03-12"

style_prompt_short: >
  大胆的图形电影。鲜明的剪影、撕纸边缘、
  戏剧性对比。希区柯克时代的片头序列栩栩如生。

style_prompt_full: >
  Saul Bass 电影片头序列风格。大胆、图形化、戏剧性。
  高对比度黑白配单一强调色（橙红 #FF4500 或
  黄 #FFD700）。鲜明的剪影和大胆形状。
  撕纸边缘和剪裁美学。尽管几何精确，但有手工制作感。
  戏剧性的揭示和变换。文字与图像
  融为一体，而非浮于其上。眩晕螺旋、
  谋杀解剖的剪纸、金臂人的排版。
  强烈对角线。动效是戏剧性的 — 元素
  揭示、旋转、变换。爵士影响的节奏。无照片写实、
  无柔和边缘、无渐变。

colors:
  primary:
    - name: "深黑"
      hex: "#000000"
      role: "剪影，戏剧性底色"
    - name: "纯白"
      hex: "#FFFFFF"
      role: "留白空间，对比"
  accent:
    - name: "Saul Bass 橙"
      hex: "#FF4500"
      role: "单一戏剧性强调"
    - name: "金黄"
      hex: "#FFD700"
      role: "替代强调色（每个项目选一个）"
  neutral:
    - name: "暖灰"
      hex: "#8B8680"
      role: "微妙纹理，旧纸感"

typography:
  display:
    family: "大胆几何无衬线或手绘字体"
    weight: "black"
    style: "通常定制，与图像融为一体"
  body:
    family: "简单无衬线字体"
    weight: "medium"
    style: "仅辅助致谢"
  caption:
    family: "与展示字体相同"
    weight: "bold"
    style: "融入构图"
  rules:
    - "字体是图像的一部分，不是分离的"
    - "鼓励定制或修改的字母形式"
    - "强烈的字重对比"
    - "文字可以碎片化、撕裂或变换"

layout:
  grid: "构图性，非严格列"
  alignment: "居中或强烈对角线"
  aspect_ratio: "2.39:1（电影宽屏）或 16:9"
  notes:
    - "全出血构图"
    - "剪影作为主要视觉元素"
    - "撕纸边缘，剪裁美学"
    - "强烈对角线创造张力"

motion:
  transitions:
    - "戏剧性揭示"
    - "旋转螺旋（眩晕）"
    - "纸剪裁动画"
    - "剪影变换"
  animation_style: >
    戏剧性揭示。元素有目的地变换和旋转。
    纸剪裁美学 — 事物组装和拆卸。
    爵士影响的节奏：切分、惊喜、有节奏。
  pacing: "戏剧性，建立张力，强调时刻"
  audio_cues:
    - "爵士配乐"
    - "管弦乐张力"
    - "Bernard Herrmann 影响"

mood:
  keywords:
    - "戏剧性"
    - "大胆"
    - "电影感"
    - "图形化"
    - "永恒"
    - "神秘"
  era: "1950–1960 年代好莱坞（永恒）"
  cultural_reference: "Saul Bass，《眩晕》、《谋杀解剖》、《金臂人》、《惊魂记》"
  avoid:
    - "照片写实图像"
    - "柔和渐变"
    - "多种强调色"
    - "通用图库素材"
    - "3D 效果"
    - "镜头光晕"
    - "现代 UI 模式"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: "2e4dfda94a3341fb849571bb7449b4c2"
  orientation: "landscape"
---

## Design Principles

片头序列本身就是电影，而非序曲。
每一帧都可以是一张海报。
剪影揭示角色而不展示它。
几何创造情感。

## Connectors

### HeyGen Video Agent
逐字使用 `style_prompt_full`。强调：剪影、大胆形状、
戏剧性揭示。纸剪裁美学。爵士影响的节奏。
无虚拟角色 — 纯图形电影。

### HTML Slides
黑色背景配鲜明的白色和单一强调色。全出血剪影。
与图像融为一体的戏剧性排版。强烈的对角线构图。

### paper.design
用大胆形状替代照片写实。剪影作为主要元素。
排版和图像作为统一构图。撕纸边缘效果。

### Figma
颜色样式：`brand/deep-black`、`brand/stark-white`、`accent/bass-orange`。
创建剪影形状作为可复用组件。
定制文字处理替代标准文本样式。
