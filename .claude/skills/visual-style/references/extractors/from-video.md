# 从视频提取

从视频关键帧生成 `visual-style.md`。

## 工作流程

1. **接收视频** — 用户提供视频 URL 或文件
2. **采样关键帧** — 在不同时间点捕获 4-6 张截图
3. **分析帧** — 识别所有帧间一致的视觉模式
4. **关注动效** — 特别注意过渡和动画
5. **生成** — 输出完整的 `visual-style.md`
6. **验证** — 确保所有必填字段齐全

## 关键帧采样策略

按以下间隔采样帧：
- **0:00-0:02** — 开场/标题帧
- **0:05-0:10** — 早期内容帧
- **0:15-0:20** — 中间内容帧
- **接近结尾** — 结束帧
- **过渡处** — 如可能，捕获过渡中间帧

寻找帧间的**一致性**——风格是保持不变的部分。

## 提取提示

分析视频帧时使用此提示模板：

```
Analyze these video keyframes and extract a visual-style.md.

These are [N] frames from a single video. Identify the CONSISTENT visual
system across all frames, not the unique content of each frame.

Identify and output:

REQUIRED:
- name: A descriptive name for this style
- version: "1.0"
- style_prompt_short: 1-2 sentence hook
- style_prompt_full: Detailed generation prompt covering:
  - Color palette (consistent colors across frames)
  - Typography style (font appearance, text treatment)
  - Motion patterns (transitions, animation style)
  - Layout approach (composition, spacing)
  - Overall mood
- colors.primary: At least 2 consistent colors

CRITICAL FOR VIDEO:
- motion.transitions: How do scenes change?
- motion.animation_style: How do elements move?
- motion.pacing: Fast cuts vs. slow fades?
- mood.keywords: What feeling does the motion create?

Be specific about MOTION patterns:
- Do elements snap or ease?
- Are transitions hard cuts or smooth fades?
- Do things bounce, slide, or appear suddenly?
- What's the rhythm? Quick and energetic, or slow and measured?

Output format:
Complete YAML frontmatter between --- delimiters
Plus Markdown body sections
```

## 分析检查清单

从视频提取时，注意查找：

### 颜色
- [ ] 背景色（场景间是否变化？）
- [ ] 主要文字/图形颜色
- [ ] 用于强调的强调色
- [ ] 颜色过渡（颜色是否变化？）

### 排版
- [ ] 标题处理（大小、字重、动画）
- [ ] 正文样式（如有）
- [ ] 说明文字/字幕样式
- [ ] 文字动画（淡入、滑入、打字效果）

### 动效（关键）
- [ ] 场景过渡（剪切、擦除、溶解、变形）
- [ ] 元素入场（淡入、滑入、弹出、缩放）
- [ ] 元素退场（如何消失？）
- [ ] 缓动风格（线性、ease-out、弹跳、吸附）
- [ ] 时间/节奏（快切、慢揭示）
- [ ] 循环模式（如有）

### 布局
- [ ] 构图风格（居中、不对称、网格锁定）
- [ ] 构图框架（满版、包含、信箱格式）
- [ ] 文字位置（底部三分之一、居中、动态）
- [ ] 宽高比（16:9、9:16、1:1）

### 氛围
- [ ] 能量水平（平静、活力、激烈）
- [ ] 语气（严肃、趣味、戏剧性）
- [ ] 时代/类型参考
- [ ] 声音-视觉关系（如有音频）

## 示例输出

给定复古街机风格视频的帧：

```yaml
---
name: "Pac-Man Arcade Style"
version: "1.0"
tags:
  - pixel retro
  - gaming
author: "Extracted"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  8-bit arcade nostalgia. Pixel graphics, neon on black,
  classic Pac-Man yellow with ghost accents.

style_prompt_full: >
  Retro 8-bit arcade aesthetic inspired by Pac-Man. Pure black
  backgrounds with neon pixel graphics. Classic Pac-Man yellow
  (#FFFF00) as the hero color. Ghost colors for accents: Blinky
  red (#FF0000), Pinky pink (#FFB8FF), Inky cyan (#00FFFF),
  Clyde orange (#FFB852). Chunky pixel fonts. Elements move in
  discrete pixel steps, not smooth curves. Maze-like compositions.
  Screen flicker and CRT scanline effects. 8-bit sound design
  aesthetic applied visually. Hard cuts between scenes. No
  gradients, no anti-aliasing, no rounded corners.

colors:
  primary:
    - name: "Arcade Black"
      hex: "#000000"
      role: "background, the void"
    - name: "Pac-Man Yellow"
      hex: "#FFFF00"
      role: "hero element, primary accent"
  accent:
    - name: "Blinky Red"
      hex: "#FF0000"
      role: "danger, emphasis"
    - name: "Inky Cyan"
      hex: "#00FFFF"
      role: "secondary accent"
    - name: "Pinky Pink"
      hex: "#FFB8FF"
      role: "tertiary accent"
    - name: "Clyde Orange"
      hex: "#FFB852"
      role: "warm accent"
  neutral:
    - name: "Maze Blue"
      hex: "#2121DE"
      role: "structure, maze walls"

typography:
  display:
    family: "Press Start 2P, monospace"
    weight: "400"
    style: "uppercase, pixel-perfect"
  body:
    family: "VT323, monospace"
    weight: "400"
    style: "8-bit rendering"
  caption:
    family: "Press Start 2P, monospace"
    weight: "400"
    style: "small, all caps"
  rules:
    - "All text must appear pixel-perfect"
    - "No anti-aliasing on fonts"
    - "Text animates character by character"

layout:
  grid: "Pixel grid, 8px base unit"
  alignment: "Centered compositions"
  aspect_ratio: "4:3 or 16:9"
  notes:
    - "Maze-like structures as compositional elements"
    - "Frame content like an arcade cabinet"
    - "Leave scanline space at edges"

motion:
  transitions:
    - "hard cuts (no dissolves)"
    - "screen wipe from Pac-Man eating across"
    - "pixel dissolve / scatter"
  animation_style: >
    Discrete pixel movement — elements jump from position to position,
    never smooth tweening. Characters animate at 12fps max. Screen
    flicker for emphasis. Chomping animation on any moving element.
  pacing: "Energetic, game-loop rhythm"
  audio_cues:
    - "wakka-wakka sound on transitions"
    - "8-bit beeps and boops"

mood:
  keywords:
    - "nostalgic"
    - "playful"
    - "arcade"
    - "8-bit"
    - "energetic"
  era: "1980s arcade golden age"
  cultural_reference: "Pac-Man, Space Invaders, Galaga, arcade cabinets"
  avoid:
    - "smooth gradients"
    - "anti-aliased edges"
    - "photorealistic elements"
    - "modern UI patterns"
    - "slow, smooth animations"
    - "muted or desaturated colors"

assets:
  reference_images: []
  color_palette_image:
    url: ""
---

## Design Principles

Everything is a pixel. Movement is discrete, never continuous.
Colors are pure and saturated. The arcade cabinet is the frame.

## Extraction Notes

Extracted from video keyframes.
Color palette based on original Pac-Man game (1980).
Motion patterns reflect 8-bit hardware limitations as aesthetic choice.
```

## 提示

- **关注一致的内容** — 忽略独特内容，找到系统
- **动效优先** — 视频风格由事物如何移动决定
- **描述节奏** — 是快切还是慢淡？
- **注意缓动** — 是吸附、弹跳还是滑行？
- **参考时代** — 许多视频风格引用特定年代或类型
