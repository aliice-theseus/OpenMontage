---
name: split-tilt-cards
description: 两张卡片并排，具有相反的 Y 旋转，创建对称的 3D 分屏布局，用于比较或功能配对。
metadata:
  tags: 3d, cards, split, tilt, comparison, symmetric, layout
---

# 分屏倾斜卡片

两张卡片并排定位，各自向相反 Y 方向旋转。创建对称的"书本打开"3D 效果 — 天然适合比较、前后对比或功能配对。

## 工作原理

- 左侧卡片旋转 `+Y`（面向右侧观看者角度）
- 右侧卡片旋转 `-Y`（面向左侧观看者角度）
- 两者共享相同的 `perspective` 父级 → 相反旋转在视觉上平衡
- 每张卡片从外部进入（左侧卡片从左滑入，右侧卡片从右滑入）以增强其身份
- 空闲阶段：温和反相浮动（正弦 `Math.PI` 偏移）— 卡片反向摆动

## HTML

```html
<div
  class="scene"
  id="split-scene"
  data-composition-id="split-scene"
  data-start="0"
  data-duration="4"
  data-track-index="0"
>
  <div class="split-stage">
    <div class="card card-left">
      <div class="card-eyebrow">{leftEyebrow}</div>
      <div class="card-headline">{leftHeadline}</div>
      <div class="card-body">{leftBody}</div>
    </div>
    <div class="card card-right">
      <div class="card-eyebrow">{rightEyebrow}</div>
      <div class="card-headline">{rightHeadline}</div>
      <div class="card-body">{rightBody}</div>
    </div>
  </div>
</div>
```

## CSS

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: {bgGradient};
  perspective: SCENE_PERSPECTIVE; /* 必需 — 没有透视 rotateY 会平面化 */
}
.split-stage {
  display: flex;
  gap: STAGE_GAP;
  transform-style: preserve-3d;
}
.card {
  width: CARD_WIDTH;
  min-height: CARD_MIN_HEIGHT;
  padding: CARD_PADDING;
  display: flex;
  flex-direction: column;
  gap: CARD_INNER_GAP;
  border-radius: CARD_RADIUS;
  background: {cardSurface};
  border: 1px solid {cardBorder};
  color: {textColor};
  font-family: {font};
  transform-style: preserve-3d;
  will-change: transform;
}
.card-left {
  /* 面向右侧 → 阴影落在右侧 */
  box-shadow:
    -CARD_SHADOW_OFFSET CARD_SHADOW_DROP CARD_SHADOW_BLUR {shadowColor},
    0 0 CARD_GLOW_BLUR {accentGlowColor};
}
.card-right {
  /* 面向左侧 → 阴影落在左侧 */
  box-shadow:
    CARD_SHADOW_OFFSET CARD_SHADOW_DROP CARD_SHADOW_BLUR {shadowColor},
    0 0 CARD_GLOW_BLUR {accentGlowColor};
}
.card-eyebrow {
  font-size: EYEBROW_FONT_SIZE;
  font-weight: 800;
  letter-spacing: EYEBROW_LETTER_SPACING;
  text-transform: uppercase;
  color: {accentColor};
}
.card-headline {
  font-size: HEADLINE_FONT_SIZE;
  font-weight: 900;
  line-height: 1;
  letter-spacing: HEADLINE_LETTER_SPACING;
}
.card-body {
  font-size: BODY_FONT_SIZE;
  font-weight: 500;
  line-height: 1.3;
  color: {bodyColor};
  opacity: BODY_OPACITY;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 阶段 1 — 从外部进入
  tl.fromTo(
    ".card-left",
    { x: -ENTRY_SLIDE_DIST, rotateY: TILT + TILT_OVERSHOOT, opacity: 0 },
    { x: 0, rotateY: TILT, opacity: 1, duration: ENTRY_DUR, ease: "power3.out" },
    LEFT_AT,
  );
  tl.fromTo(
    ".card-right",
    { x: ENTRY_SLIDE_DIST, rotateY: -TILT - TILT_OVERSHOOT, opacity: 0 },
    { x: 0, rotateY: -TILT, opacity: 1, duration: ENTRY_DUR, ease: "power3.out" },
    RIGHT_AT,
  );

  // 阶段 2 — 反相空闲摆动（卡片反向运动以增强动感）
  tl.to(
    ".card-left",
    { y: -FLOAT_AMP, duration: FLOAT_DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 },
    IDLE_START,
  );
  tl.to(
    ".card-right",
    { y: FLOAT_AMP, duration: FLOAT_DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 },
    IDLE_START,
  );

  // 阶段 3 — 温和文案揭示（卡片到达后正文上滑 + 淡入）
  tl.from(
    ".card-eyebrow, .card-headline, .card-body",
    { opacity: 0, y: COPY_RISE, stagger: COPY_STAGGER, duration: COPY_DUR, ease: "power2.out" },
    COPY_REVEAL_AT,
  );

  window.__timelines["split-scene"] = tl;
</script>
```

## 如何选择值

### 布局 / 排版

- **SCENE_PERSPECTIVE** — 场景根元素上的透视。
  - 范围：1000-2400 px
  - 效果：较低夸大倾斜（更锥形）；较高读作近乎等角、更平面的旋转
- **STAGE_GAP** — 两张卡片之间的水平间距。
  - 范围：40-120 px（≈0.06-0.15× `CARD_WIDTH`）
  - 效果：小间距读作"融合对"；大间距读作"比较但分离"
- **CARD_WIDTH** — 每张卡片的宽度。
  - 范围：在 1920×1080 上 480-820 px
  - 约束：`2 * CARD_WIDTH + STAGE_GAP ≤ 0.95 * stageWidth` 使两张卡片在完全倾斜时保持在屏幕上
- **CARD_MIN_HEIGHT** — 卡片最小高度。
  - 范围：≈0.75-1.05× `CARD_WIDTH`（近方形读作平衡；很高读作海报）
- **CARD_PADDING / CARD_INNER_GAP / CARD_RADIUS** — 内部镀铬。
  - 范围：padding 40-72 px；inner gap 24-48 px；radius 24-40 px
- **CARD_SHADOW_OFFSET / CARD_SHADOW_DROP / CARD_SHADOW_BLUR** — 投影几何。
  - 约束：偏移符号匹配倾斜方向（参见关键原则）；drop > 0 将卡片接地到场景
  - 范围：offset 16-28 px；drop 20-32 px；blur 40-80 px
- **CARD_GLOW_BLUR** — 次级内部辉光模糊半径（`box-shadow` 0 0 blur）。
  - 范围：16-32 px（微妙重音边缘；较大与卡片内容竞争）
- **EYEBROW_FONT_SIZE / EYEBROW_LETTER_SPACING** — 小写大写标签。
  - 范围：22-32 px；间距 6-12 px（大写配合正字母间距更干净）
- **HEADLINE_FONT_SIZE / HEADLINE_LETTER_SPACING** — 主要单行冲击。
  - 范围：在 1920×1080 上 72-104 px；间距 -1 到 -3 px（展示字体的紧密跟踪）
- **BODY_FONT_SIZE / BODY_OPACITY** — 支持文案。
  - 范围：28-40 px；不透明度 0.8-0.92
  - 约束：正文限制为 ≤2 行（参见关键约束 — 倾斜长段落模糊）

### 进入 / 倾斜

- **TILT** — 静态 `rotateY` 角度值，以度为单位（左侧 `+`，右侧 `−`）。
  - 范围：10-18°（低于 10 几乎读作平面；超过 18 卡片折叠闭合，正文难以阅读）
- **TILT_OVERSHOOT** — 在稳定到 `TILT` 之前，起始 `rotateY` 添加的额外角度。
  - 范围：4-12°
  - 效果：给进入一种轻微旋转到位的感觉
- **ENTRY_SLIDE_DIST** — 每张卡片从离轴滑入的像素数。
  - 范围：200-500 px（≈0.3-0.6× `CARD_WIDTH`）
- **ENTRY_DUR** — 每张卡片滑入时长。
  - 范围：0.6-1.2 秒
- **LEFT_AT** — 左侧卡片进入开始时间。
  - 范围：0.0-0.4 秒
- **RIGHT_AT** — 右侧卡片进入开始时间。
  - 范围：`LEFT_AT + 0.0` 到 `LEFT_AT + 0.3` 秒（零错开感觉机械；大错开分裂这个对）

### 空闲摆动

- **FLOAT_AMP** — 空闲 y 摆动的正弦振幅（以 px 为单位）。
  - 范围：3-8 px（参见 sine-wave-loop 规则 — 微妙是要点）
- **FLOAT_DURATION** — 完整 yoyo 往返时长（一次呼吸）。
  - 范围：1.6-3.2 秒（≈呼吸节奏）
- **IDLE_START** — 空闲摆动开始时间。
  - 约束：`≥ max(LEFT_AT, RIGHT_AT) + ENTRY_DUR` 使空闲不与进入尾部冲突

### 文案揭示

- **COPY_REVEAL_AT** — 眉标/标题/正文淡入的时间。
  - 约束：通常在卡片稳定期间开始（与进入尾部重叠）— 内容不应在卡片已空闲后弹出
- **COPY_DUR / COPY_STAGGER / COPY_RISE** — 淡入形状。
  - 范围：时长 0.4-0.7 秒；错开 0.04-0.10 秒；上升 12-24 px

### 颜色 / 排版标记

- **{bgGradient}** — 卡片后的径向或线性渐变；比 `{cardSurface}` 暗，使卡片凸显
- **{cardSurface}** — 卡片背景（通常是在场景上叠加的低饱和度渐变）
- **{cardBorder}** — 1 px 边框颜色，通常为低 alpha 的 `{accentColor}`
- **{shadowColor}** — 投影颜色，通常为 0.5-0.7 alpha 的近黑色
- **{accentGlowColor}** — 内部辉光颜色，通常为低 alpha 的 `{accentColor}`
- **{accentColor}** — 眉标 + 重音边缘颜色（每场景单色相）
- **{textColor}** — 主要标题颜色，与 `{cardSurface}` 高对比度
- **{bodyColor}** — 正文颜色，相对于 `{textColor}` 稍解饱和
- **{font}** — 所有卡片文案的展示字体栈

## 变体

### 中倾斜缩放穿过（与摄像机移动组合）

如果单独的摄像机补间缩放 `.split-stage`，卡片的倾斜读作观看者穿过它们之间的间隙。

### 不对称内容密度（徽章/标签/图标）

在每张卡片附近添加浮动徽章以获得额外上下文。在父级上绝对定位 — 不在卡片内部，使徽章不继承 3D 旋转：

```html
<div class="badge badge-left">{leftBadge}</div>
<div class="badge badge-right">{rightBadge}</div>
```

### 堆叠变体（3+ 卡片）

对于 3 张卡片，中心卡片保持平坦（`rotateY 0`），外部两张向内倾斜 — 对于"你的旧方式/中间无物/我们的方式"比较很有用。

## 关键原则

- **场景根元素上的 `perspective` 必需** — 没有它 rotateY 会平面化，分屏倾斜塌缩为平排布局
- **舞台和每张卡片上的 `transform-style: preserve-3d`** — 保持 3D 平面，因为卡片有自己的变换
- **阴影方向必须匹配倾斜** — 左侧卡片面向右侧，阴影落在右侧（正 X），反之亦然。错误的阴影方向读作"3D 损坏"
- **对称内容重量** — 两张卡片相同宽度、相同垂直中心、相似行数。不对称内容破坏比较隐喻
- **反相浮动（`Math.PI` 偏移）** — 左侧向上摆动时右侧向下摆动。同步摆动看起来像两张卡片在同一个传送带上；反相看起来生动
- **从外部滑入** — 左卡从左，右卡从右 — 加强"它们来自各自的世界并在此相遇"
- **❗ 倾斜幅度 10-15°** — 低于 10° 看起来像轻微透视偏移（几乎平面），超过 18° 看起来像卡片折叠闭合，文案难以阅读

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **空闲浮动不要使用 `requestAnimationFrame`** — 在时间线内驱动，使定位是确定性的
- **不要将徽章放在卡片 div 内部** — 它们会继承 rotateY 并随卡片离轴倾斜。在父级上浮动
- **每张卡片的正文 ≤ 2 行** — 倾斜文本难以阅读；长段落塌缩为透视模糊

## 组合

- [card-morph-anchor.md](card-morph-anchor.md) — 两张卡片之后可以变形为一个统一形状
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 数字作为每侧标题内容

## 与 HF 技能配对

- `/hyperframes-animation` — 时间线 + 空闲摆动的 `yoyo`
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
