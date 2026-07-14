---
name: "Saul Bass 电影片头风格"
version: "1.0"
tags:
  - 标志性设计
  - 电影感
author: "视觉风格图库"
created: "2026-03-12"

style_prompt_short: >
  大胆的图形电影。鲜明的剪影、撕裂的纸张边缘、
  戏剧性的对比。希区柯克时代的片头序列重现生机。

style_prompt_full: >
  Saul Bass 电影片头序列风格。大胆、图形化、戏剧化。
  高对比度黑白搭配单一强调色（橙红色
  #FF4500 或黄色 #FFD700）。鲜明的剪影和大胆的形状。
  撕裂纸张边缘和剪裁美学。尽管几何精确，
  却带有手工制作的感觉。戏剧性的揭示和变换。文字
  与图像融合，而非浮于其上。迷魂记螺旋、
  谋杀解剖的纸板剪裁、金臂人的
  字体设计。强烈的对角线。动效具有戏剧性——元素
  揭示、旋转、变换。受爵士乐影响的节奏。无照片写实，
  无柔和边缘，无渐变。

colors:
  primary:
    - name: "深黑"
      hex: "#000000"
      role: "剪影，戏剧性底色"
    - name: "亮白"
      hex: "#FFFFFF"
      role: "负空间，对比"
  accent:
    - name: "Saul Bass 橙"
      hex: "#FF4500"
      role: "单一戏剧性强调色"
    - name: "金黄"
      hex: "#FFD700"
      role: "备用强调色（每个项目选一种）"
  neutral:
    - name: "暖灰"
      hex: "#8B8680"
      role: "微妙纹理，做旧纸张质感"

typography:
  display:
    family: "粗体几何无衬线或手绘"
    weight: "black"
    style: "通常为定制，与图像融合"
  body:
    family: "简洁无衬线"
    weight: "medium"
    style: "仅用于辅助演职员表"
  caption:
    family: "与展示字体相同"
    weight: "bold"
    style: "融入构图"
  rules:
    - "文字是图像的一部分，而非独立元素"
    - "鼓励使用定制或修改的字体"
    - "强烈的字重对比"
    - "文字可以碎片化、撕裂或变形"

layout:
  grid: "构图性，非严格列网格"
  alignment: "居中或戏剧性对角线"
  aspect_ratio: "2.39:1（宽银幕）或 16:9"
  notes:
    - "满版构图"
    - "剪影作为主要视觉元素"
    - "撕裂纸张边缘，剪裁美学"
    - "强烈的对角线营造张力"

motion:
  transitions:
    - "戏剧性揭示"
    - "旋转螺旋（迷魂记）"
    - "纸板剪裁动画"
    - "剪影变换"
  animation_style: >
    戏剧化的揭示。元素有目的地变换和旋转。
    纸板剪裁美学——事物组合与分解。
    受爵士乐影响的节奏：切分、惊喜、有韵律。
  pacing: "戏剧性，营造张力，重点时刻"
  audio_cues:
    - "爵士配乐"
    - "管弦乐的紧张感"
    - "Bernard Herrmann 影响"

mood:
  keywords:
    - "戏剧性"
    - "大胆"
    - "电影感"
    - "图形化"
    - "永恒"
    - "神秘"
  era: "1950s–1960s 好莱坞（永恒）"
  cultural_reference: "Saul Bass, 迷魂记, 谋杀解剖, 金臂人, 惊魂记"
  avoid:
    - "照片写实图像"
    - "柔和渐变"
    - "多种强调色"
    - "通用素材片段"
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

## 设计原则

片头序列本身就是电影，而非前奏。
每一帧都可以是一张海报。
剪影无需展示即可揭示角色。
几何创造情感。

## 连接器

### HeyGen 视频代理
逐字使用 `style_prompt_full`。强调：剪影、大胆的形状、
戏剧性揭示。纸板剪裁美学。受爵士乐影响的节奏。
无虚拟形象——纯图形电影。

### HTML 幻灯片
黑色背景搭配亮白和单一强调色。满版剪影。
与图像融为一体的戏剧性字体。强烈的对角线构图。

### paper.design
大胆形状优先于照片写实。剪影作为主要元素。
文字与图像作为统一构图。撕裂纸张边缘效果。

### Figma
颜色样式：`brand/deep-black`、`brand/stark-white`、`accent/bass-orange`。
将剪影形状创建为可复用组件。
自定义字体处理而非标准文本样式。
