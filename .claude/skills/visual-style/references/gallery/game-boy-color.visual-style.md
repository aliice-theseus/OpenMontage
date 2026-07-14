---
name: "Game Boy Color"
version: "1.0"
tags:
  - 像素复古
  - 游戏
author: "视觉风格图库"
created: "2026-03-12"

style_prompt_short: >
  90 年代末掌机游戏的怀旧情怀。有限的调色板、
  粗颗粒像素、口袋里的便携冒险。

style_prompt_full: >
  1990 年代末的 Game Boy Color 美学。每个场景有限的
  调色板（原版 56 色，每个精灵通常使用 4-10 色）。
  标志性的 GBC 颜色：特有的青绿（#0F380F 到
  #9BBC0F 渐变）、紫色外壳（#663399）、莓果色（#CC3366）、青色
  （#339999）、原子紫（#6B3FA0）。低分辨率下的粗像素图形
  （原生 160x144）。用于阴影的抖动模式。
  低帧率的简单精灵动画（10-15fps）。UI 元素
  具有独特的 GBC 边框风格。声音设计为
  芯片音乐——4 通道音频美学。便携、多彩、迷人。
  不如原版 Game Boy 受限，但仍明显有约束。
  参考：水晶版宝可梦、塞尔达传说 DX、瓦里奥大陆 3。

colors:
  primary:
    - name: "GBC 深绿"
      hex: "#0F380F"
      role: "最深色调，轮廓线"
    - name: "GBC 浅绿"
      hex: "#9BBC0F"
      role: "最浅色调，高光"
  accent:
    - name: "GBC 紫"
      hex: "#663399"
      role: "原版外壳颜色，品牌强调"
    - name: "莓果粉"
      hex: "#CC3366"
      role: "莓果外壳变体"
    - name: "青色"
      hex: "#339999"
      role: "青色外壳变体"
    - name: "原子紫"
      hex: "#6B3FA0"
      role: "原子紫外壳，特殊强调"
  neutral:
    - name: "GBC 中绿"
      hex: "#306230"
      role: "中间色调，次要元素"
    - name: "GBC 淡绿"
      hex: "#8BAC0F"
      role: "浅中间色调"

typography:
  display:
    family: "像素字体（8x8 或 16x16）"
    weight: "常规（像素就是像素）"
    style: "大写或混合，粗颗粒"
  body:
    family: "像素字体"
    weight: "常规"
    style: "对话框风格"
  caption:
    family: "像素字体"
    weight: "常规"
    style: "小号，菜单文字"
  rules:
    - "所有文字必须像素完美"
    - "有限的字符集（像真实的 GBC）"
    - "带特色边框的文本框"
    - "文字逐字符显示"

layout:
  grid: "8 像素基本单位"
  alignment: "菜单居中，对话框左对齐"
  aspect_ratio: "10:9（GBC 原生）或 16:9（现代）"
  notes:
    - "160x144 原生分辨率，均匀缩放"
    - "HUD 元素位于屏幕边缘"
    - "对话框在底部三分之一处"
    - "基于精灵的构图"

motion:
  transitions:
    - "屏幕擦除（虹膜、水平、垂直）"
    - "调色板淡出（到白色或黑色）"
    - "无平滑过渡"
  animation_style: >
    低帧率精灵动画（10-15fps）。两帧行走循环。
    屏幕过渡瞬发或使用经典擦除。
    UI 元素直接出现和消失，不淡入淡出。
  pacing: "快速，响应式，类游戏"
  audio_cues:
    - "芯片音乐"
    - "4 通道音频"
    - "8 位音效"
    - "菜单哔哔声"

mood:
  keywords:
    - "怀旧"
    - "便携"
    - "多彩"
    - "迷人"
    - "有趣"
    - "冒险"
  era: "1998-2003"
  cultural_reference: "水晶版宝可梦、塞尔达传说 DX、瓦里奥大陆 3、Game Boy Color 硬件"
  avoid:
    - "平滑渐变"
    - "高分辨率图形"
    - "照片写实元素"
    - "现代 UI 模式"
    - "超过 56 种颜色"
    - "平滑动画"
    - "抗锯齿"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: "94e43f67cbe546b783e1f5c6f2b66125"
  orientation: "landscape"
---

## 设计原则

约束催生创造力。
当你只有 160x144 时，每个像素都很重要。
色彩是珍贵的——有目的地使用它。
魅力来自个性，而非复杂。

## 连接器

### HeyGen 视频代理
逐字使用 `style_prompt_full`。强调：粗像素、有限颜色、
低帧率动画。屏幕擦除过渡。芯片音乐音频美学。
无平滑运动——一切都是离散的像素步进。

### HTML 幻灯片
使用像素字体（Press Start 2P、VT323）。仅以整数倍
（2x、3x、4x）缩放图形以保持像素清晰度。默认 GBC 绿色调色板，
外壳色用于强调。对话框边框。

### paper.design
在低分辨率下设计，再放大。使用 GBC 调色板。
用于阴影的抖动模式。基于精灵的构图。
所有元素使用 8 像素网格。

### Figma
颜色样式：`gbc/dark-green`、`gbc/mid-green`、`gbc/pale-green`、`gbc/light-green`，
加上外壳颜色变体。8x8 像素网格。使用像素字体或
设计自定义像素字体。导出时无抗锯齿。
