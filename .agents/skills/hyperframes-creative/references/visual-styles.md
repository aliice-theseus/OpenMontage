# 视觉风格库

HyperFrames 视频的命名视觉标识。每种风格都基于真实的平面设计传统，并以 DESIGN.md 兼容的令牌块形式表达。将其作为起点——将 YAML 复制到项目的 `design.md` front matter 中，然后进行自定义。

**如何选择：** 先匹配情绪，再匹配内容。问：_"观众应该感受到什么？"_

**如何使用：** 将风格的 YAML 令牌块复制到 `design.md` 的 front matter 中。添加 `## 概述`、`## 颜色`、`## 排版`、`## 层级`、`## 组件`、`## 该做与不该做` 等散文段落以完善文件。

## 目录

- 快速参考
- Swiss Pulse（瑞士脉动）
- Velvet Standard（丝绒标准）
- Deconstructed（解构）
- Maximalist Type（极繁主义字体）
- Data Drift（数据漂移）
- Soft Signal（软信号）
- Folk Frequency（民谣频率）
- Shadow Cut（阴影切割）
- 情绪到风格指南
- 创建自定义风格

## 快速参考

| 风格             | 情绪                 | 最适合                         | 过渡着色器                       |
| --------------- | --------------------- | ------------------------------ | -------------------------------- |
| Swiss Pulse     | 临床、精确             | SaaS、数据、开发工具、指标       | Cinematic Zoom 或 SDF Iris       |
| Velvet Standard | 高级、永恒             | 奢侈品、企业、主题演讲           | Cross-Warp Morph                 |
| Deconstructed   | 工业、原始             | 技术发布、安全、朋克             | Glitch 或 Whip Pan               |
| Maximalist Type | 响亮、动态             | 重大公告、发布会                 | Ridged Burn                      |
| Data Drift      | 未来感、沉浸式          | AI、ML、尖端科技               | Gravitational Lens 或 Domain Warp |
| Soft Signal     | 亲密、温暖             | 健康、个人故事、品牌             | Thermal Distortion               |
| Folk Frequency  | 文化、生动             | 消费者应用、食品、社区           | Swirl Vortex 或 Ripple Waves     |
| Shadow Cut      | 黑暗、电影感            | 戏剧性揭示、安全、曝光           | Domain Warp                      |

---

## 1. Swiss Pulse — Josef Müller-Brockmann

**情绪：** 临床、精确 | **最适合：** SaaS 仪表盘、开发者工具、API、指标

```yaml
name: Swiss Pulse
colors:
  primary: "#1a1a1a"
  on-primary: "#ffffff"
  accent: "#0066FF"
typography:
  headline:
    fontFamily: Helvetica Neue
    fontSize: 5rem
    fontWeight: 700
  label:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
  stat:
    fontFamily: Helvetica Neue
    fontSize: 7rem
    fontWeight: 700
rounded:
  none: 0px
  sm: 2px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
motion:
  energy: high
  easing:
    entry: "expo.out"
    exit: "power4.in"
    ambient: "none"
  duration:
    entrance: 0.4
    hold: 1.5
    transition: 0.6
  atmosphere:
    - grid-lines
    - registration-marks
  transition: cinematic-zoom
```

网格锁定构图。每个元素都对齐到不可见的 12 列网格。数字以 80-120px 占据画面主导。动画计数器从 0 开始计数。硬切，无装饰性过渡。没有浮动元素。

---

## 2. Velvet Standard — Massimo Vignelli

**情绪：** 高级、永恒 | **最适合：** 奢侈品、企业软件、主题演讲、投资者演示

```yaml
name: Velvet Standard
colors:
  primary: "#0a0a0a"
  on-primary: "#ffffff"
  accent: "#1a237e"
typography:
  headline:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 300
    letterSpacing: 0.15em
    textTransform: uppercase
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 300
    lineHeight: 1.6
rounded:
  sm: 0px
  md: 2px
spacing:
  sm: 16px
  md: 32px
  lg: 64px
motion:
  energy: calm
  easing:
    entry: "sine.inOut"
    exit: "power1.in"
    ambient: "sine.inOut"
  duration:
    entrance: 1.2
    hold: 3.0
    transition: 1.5
  atmosphere:
    - subtle-grain
    - hairline-rules
  transition: cross-warp-morph
```

慷慨的负空间。对称、居中、建筑般的精确性。纤细无衬线体，全大写，宽字距。顺序揭示配以长停留。没有突兀——一切都带着意图滑行。奢华不赶时间。

---

## 3. Deconstructed — Neville Brody

**情绪：** 工业、原始 | **最适合：** 科技新闻、开发者发布会、安全产品、朋克能量揭示

```yaml
name: Deconstructed
colors:
  primary: "#1a1a1a"
  on-primary: "#f0f0f0"
  accent: "#D4501E"
typography:
  headline:
    fontFamily: Space Grotesk
    fontSize: 4rem
    fontWeight: 700
  label:
    fontFamily: Space Mono
    fontSize: 0.75rem
    fontWeight: 700
    textTransform: uppercase
rounded:
  none: 0px
spacing:
  sm: 4px
  md: 12px
  lg: 24px
motion:
  energy: high
  easing:
    entry: "back.out(2.5)"
    exit: "steps(8)"
    ambient: "elastic.out(1.2, 0.4)"
  duration:
    entrance: 0.3
    hold: 1.0
    transition: 0.5
  atmosphere:
    - scan-lines
    - glitch-artifacts
    - grain-overlay
  transition: glitch
```

倾斜的字体、重叠的边缘、溢出画框。粗犷的工业重量。砂砾质感：扫描线效果、故障伪影融入了设计。文字砰然撞击并碎裂。字母打乱然后弹跳到最终位置。故意的不规则——不应有任何抛光感。

---

## 4. Maximalist Type — Paula Scher

**情绪：** 响亮、动态 | **最适合：** 大型产品发布会、里程碑公告、高能量宣传视频

```yaml
name: Maximalist Type
colors:
  primary: "#0a0a0a"
  on-primary: "#ffffff"
  accent-red: "#E63946"
  accent-yellow: "#FFD60A"
typography:
  headline:
    fontFamily: Anton
    fontSize: 8rem
    fontWeight: 400
    textTransform: uppercase
  subhead:
    fontFamily: Space Grotesk
    fontSize: 3rem
    fontWeight: 700
rounded:
  none: 0px
spacing:
  sm: 0px
  md: 8px
motion:
  energy: high
  easing:
    entry: "expo.out"
    exit: "back.out(1.8)"
    ambient: "power3.out"
  duration:
    entrance: 0.3
    hold: 0.8
    transition: 0.4
  atmosphere:
    - type-layers
    - color-blocks
  transition: ridged-burn
```

文字就是视觉本身。不同比例和角度的重叠字体层，填充画幅的 50-80%。大胆饱和的颜色——最大对比度。一切都是动态的：撞击、滑动、缩放。2-3 秒的快速场景。没有静态时刻。快速入场，硬性停止。

---

## 5. Data Drift — Refik Anadol

**情绪：** 未来感、沉浸式 | **最适合：** AI 产品、ML 平台、数据公司、前瞻科技

```yaml
name: Data Drift
colors:
  primary: "#0a0a0a"
  on-primary: "#e0e0e0"
  accent-purple: "#7c3aed"
  accent-cyan: "#06b6d4"
typography:
  headline:
    fontFamily: Inter
    fontSize: 2.5rem
    fontWeight: 200
    letterSpacing: 0.05em
  body:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 300
rounded:
  sm: 4px
  md: 12px
  full: 9999px
spacing:
  sm: 16px
  md: 32px
  lg: 64px
motion:
  energy: moderate
  easing:
    entry: "sine.inOut"
    exit: "power2.out"
    ambient: "sine.inOut"
  duration:
    entrance: 1.0
    hold: 2.5
    transition: 1.5
  atmosphere:
    - particle-field
    - light-traces
    - radial-glow
  transition: gravitational-lens
```

纤细的未来感无衬线体——漂浮、失重、极简。流体变形构图。极端的尺度转换（微观 → 宏观）。粒子聚合成数字。光线在画幅中描绘数据路径。流畅、连续、有机。没有硬边缘。

---

## 6. Soft Signal — Stefan Sagmeister

**情绪：** 亲密、温暖 | **最适合：** 健康品牌、个人故事、生活方式产品、以人为本的应用

```yaml
name: Soft Signal
colors:
  primary: "#FFF8EC"
  on-primary: "#2a2a2a"
  accent-amber: "#F5A623"
  accent-rose: "#C4A3A3"
  accent-sage: "#8FAF8C"
typography:
  headline:
    fontFamily: Playfair Display
    fontSize: 3rem
    fontWeight: 400
    fontStyle: italic
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 300
    lineHeight: 1.7
rounded:
  sm: 8px
  md: 16px
  lg: 24px
  full: 9999px
spacing:
  sm: 12px
  md: 24px
  lg: 48px
motion:
  energy: calm
  easing:
    entry: "sine.inOut"
    exit: "power1.inOut"
    ambient: "sine.inOut"
  duration:
    entrance: 1.0
    hold: 3.0
    transition: 1.5
  atmosphere:
    - soft-gradient
    - warm-grain
  transition: thermal-distortion
```

手写风格或人文主义衬线字体。个人化、小写、精致。特写构图：单个元素充满画框。缓慢漂移和浮动，从不突兀。柔软的有机运动。不应感到匆忙或抛光。亲密，从不企业化。

---

## 7. Folk Frequency — Eduardo Terrazas

**情绪：** 文化、生动 | **最适合：** 消费者应用、食品平台、社区产品、节日发布

```yaml
name: Folk Frequency
colors:
  primary: "#ffffff"
  on-primary: "#1a1a1a"
  accent-pink: "#FF1493"
  accent-blue: "#0047AB"
  accent-yellow: "#FFE000"
  accent-green: "#009B77"
typography:
  headline:
    fontFamily: Fredoka One
    fontSize: 4rem
    fontWeight: 400
  body:
    fontFamily: Nunito
    fontSize: 1rem
    fontWeight: 600
rounded:
  sm: 8px
  md: 16px
  lg: 32px
  full: 9999px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
motion:
  energy: high
  easing:
    entry: "back.out(1.6)"
    exit: "elastic.out(1, 0.5)"
    ambient: "sine.inOut"
  duration:
    entrance: 0.5
    hold: 1.5
    transition: 0.8
  atmosphere:
    - pattern-tiles
    - confetti-burst
    - color-blocks
  transition: swirl-vortex
```

大胆温暖的圆角字体。图案和重复——民间艺术的节奏和密度。层次丰富的构图，视觉纹理丰富。每一帧都感觉是手工制作的。多彩运动：元素跳跃、弹出、快乐地旋转到位。过冲感觉是有意的。庆祝的能量。

---

## 8. Shadow Cut — Hans Hillmann

**情绪：** 黑暗、电影感 | **最适合：** 安全产品、戏剧性揭示、调查内容、高强度发布

```yaml
name: Shadow Cut
colors:
  primary: "#0a0a0a"
  on-primary: "#f0f0f0"
  surface: "#3a3a3a"
  accent: "#C1121F"
typography:
  headline:
    fontFamily: Oswald
    fontSize: 4rem
    fontWeight: 700
    textTransform: uppercase
  body:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
rounded:
  none: 0px
  sm: 2px
spacing:
  sm: 8px
  md: 16px
  lg: 48px
motion:
  energy: moderate
  easing:
    entry: "power3.out"
    exit: "power4.in"
    ambient: "sine.inOut"
  duration:
    entrance: 0.8
    hold: 2.5
    transition: 1.2
  atmosphere:
    - deep-shadow
    - vignette
    - grain-overlay
  transition: domain-warp
```

近单色：深黑、冷灰、纯白 + 一个血色强调。锐利的棱角字体，如同黑色电影标题卡。重对比度，无柔和感。元素从黑暗中浮现——揭示即是叙事。缓慢爬行的推进，戏剧性的尺度展示。节奏中的停顿至关重要。Domain Warp 在下一场景前溶解现实。

---

## 情绪 → 风格指南

| 如果内容感觉...                    | 使用...         |
| ---------------------------------- | --------------- |
| 数据驱动、分析型、技术感            | Swiss Pulse     |
| 高端、企业、奢华                    | Velvet Standard |
| 原始、朋克、激进、反叛              | Deconstructed   |
| 炒作、响亮、高能量发布              | Maximalist Type |
| AI、ML、推测性、未来感             | Data Drift      |
| 人性化、温暖、个人、健康            | Soft Signal     |
| 文化、有趣、消费、节日              | Folk Frequency  |
| 黑暗、戏剧、强烈、电影感            | Shadow Cut      |

---

## 创建自定义风格

这 8 种风格是起点——不是限制。创建你自己的：

1. **命名**— 以设计师、艺术运动或文化参考命名
2. **编写 YAML 令牌** — `colors`（2-5 个令牌）、`typography`（2-3 个等级）、`rounded`、`spacing`、`motion`（能量 + 缓动 + 时长 + 氛围 + 过渡）
3. **添加散文** — 一段描述感觉、该做什么、避免什么
4. **令牌引用** — 在组件定义中使用 `{colors.accent}`、`{typography.headline}`

模式：**YAML 令牌（什么）→ 散文理由（为什么）→ 组件（它们如何组合）。**
