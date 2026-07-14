---
name: "Game Boy Color"
version: "1.0"
tags:
  - 像素复古
  - 游戏
author: "视觉风格图库"
created: "2026-03-12"

style_prompt_short: >
  90 年代末掌机游戏怀旧。有限调色板、
  粗圆像素、口袋中的便携冒险。

style_prompt_full: >
  1990 年代末的 Game Boy Color 美学。每场景有限的调色板
  （最初 56 色，每个精灵通常使用 4-10 色）。
  标志性的 GBC 颜色：那种特定的青绿（#0F380F 到
  #9BBC0F 渐变）、紫色外壳（#663399）、莓红（#CC3366）、
  青（#339999）、原子紫（#6B3FA0）。粗圆像素图形，低
  分辨率（原生 160x144）。用于阴影的抖动模式。
  低帧率（10-15fps）的简单精灵动画。UI 元素
  具有那种独特的 GBC 边框风格。声音设计将是
  芯片音乐 — 4 通道音频美学。便携、多彩、迷人。
  不如原始 Game Boy 受限，但仍明显受限。
  《宝可梦 水晶》、《塞尔达传说 织梦岛 DX》、《瓦力欧大陆 3》作为参考。

colors:
  primary:
    - name: "GBC 深绿"
      hex: "#0F380F"
      role: "最深色调，轮廓"
    - name: "GBC 浅绿"
      hex: "#9BBC0F"
      role: "最浅色调，高亮"
  accent:
    - name: "GBC 紫"
      hex: "#663399"
      role: "原版外壳颜色，品牌强调"
    - name: "莓红"
      hex: "#CC3366"
      role: "莓红外壳变体"
    - name: "青"
      hex: "#339999"
      role: "青色外壳变体"
    - name: "原子紫"
      hex: "#6B3FA0"
      role: "原子紫外壳，特殊强调"
  neutral:
    - name: "GBC 中绿"
      hex: "#306230"
      role: "中色调，次要元素"
    - name: "GBC 浅绿"
      hex: "#8BAC0F"
      role: "浅中色调"

typography:
  display:
    family: "像素字体（8x8 或 16x16）"
    weight: "常规（像素就是像素）"
    style: "大写或混合，粗圆"
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
    - "有限的字符集（像真实 GBC 一样）"
    - "带特征边框的文本框"
    - "文字逐字符揭示"

layout:
  grid: "8 像素基础单位"
  alignment: "居中菜单，左对齐对话"
  aspect_ratio: "10:9（GBC 原生）或 16:9（现代）"
  notes:
    - "原生分辨率 160x144，均匀放大"
    - "HUD 元素在屏幕边缘"
    - "对话框在下方三分之一处"
    - "基于精灵的构图"

motion:
  transitions:
    - "屏幕擦拭（虹膜、水平、垂直）"
    - "调色板淡入淡出（到白色或黑色）"
    - "无平滑过渡"
  animation_style: >
    低帧率精灵动画（10-15fps）。两帧行走循环。
    屏幕过渡是即时的或使用经典擦拭。
    UI 元素出现和消失，不淡入淡出。
  pacing: "快速、响应式、类似游戏"
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
    - "俏皮"
    - "冒险"
  era: "1998-2003"
  cultural_reference: "《宝可梦 水晶》、《塞尔达传说 织梦岛 DX》、《瓦力欧大陆 3》、Game Boy Color 硬件"
  avoid:
    - "平滑渐变"
    - "高分辨率图形"
    - "照片写实元素"
    - "现代 UI 模式"
    - "总共超过 56 色"
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

## Design Principles

约束孕育创造力。
当你只有 160x144 时，每个像素都重要。
颜色是宝贵的 — 有意图地使用它。
魅力来自角色，而非复杂度。

## Connectors

### HeyGen Video Agent
逐字使用 `style_prompt_full`。强调：粗圆像素、有限颜色、
低帧率动画。屏幕擦拭过渡。芯片音乐音频美学。
无平滑移动 — 一切都是离散的像素步骤。

### HTML Slides
使用像素字体（Press Start 2P、VT323）。仅以整数倍（2x、3x、4x）
缩放图形以保持像素清晰度。GBC 绿色调色板为默认，
外壳颜色用于强调。对话框边框。

### paper.design
以低分辨率设计，再放大。使用 GBC 调色板。
用于阴影的抖动模式。基于精灵的构图。
所有元素的 8 像素网格。

### Figma
颜色样式：`gbc/dark-green`、`gbc/mid-green`、`gbc/pale-green`、`gbc/light-green`，
加上外壳颜色变体。8x8 像素网格。使用像素字体或
设计自定义像素字体。导出时无抗锯齿。
