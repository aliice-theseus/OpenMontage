---
name: physics-press-reaction
description: 光标 + 元素通过减法弹簧力同步按下 — 光标着陆在元素上，两者一起压缩，然后释放。与 press-release-spring（没有光标）不同。
metadata:
  tags: spring, click, physics, cursor, subtractive, interaction, synchronized
---

# 物理按下反应（光标 + 元素同步）

模拟真实点击：光标接近按钮，着陆，两者同步压缩，然后一起释放。两个不同的时间事件（按下帧和释放帧）由弹簧力约束。与 [press-release-spring](press-release-spring.md)**不同**（没有光标 — 只是一个按下发生）；此规则是**组合的**光标 + 元素行为。

## 工作原理

一个单一的 `PRESS_INTENSITY` 值同时驱动光标和按钮：

- **按下**：两者压缩到 `1 - PRESS_INTENSITY`
- **释放**：两者以过冲弹回 1.0

光标在按下开始前的接近阶段也**平移**到按钮中心。释放后，光标可以继续移动（下一个交互）或保持。

## HTML

```html
<div
  class="scene"
  id="press-react-scene"
  data-composition-id="press-react-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="stack">
    <button class="btn" id="btn">
      <span class="btn-icon">{ctaIcon}</span>
      <span class="btn-label">{ctaCopy}</span>
    </button>
    <div class="brand">{Brand}</div>
  </div>
  <!-- 光标位于场景根级别，以便自由平移 -->
  <svg class="cursor" id="cursor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M3 2 L21 12 L12 13 L7 22 Z"
      fill="{cursorFill}"
      stroke="{cursorStroke}"
      stroke-width="1.5"
    />
  </svg>
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
  background: {sceneBg};
  font-family: {font};
  overflow: hidden;
}
.stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: STACK_GAP;
}
.btn {
  display: flex;
  align-items: center;
  gap: BTN_INNER_GAP;
  padding: BTN_PADDING_V BTN_PADDING_H;
  background: {btnBg};
  border: none;
  border-radius: BTN_RADIUS;
  color: {btnTextColor};
  font-family: {font};
  font-weight: 900;
  font-size: BTN_FONT_SIZE;
  letter-spacing: BTN_TRACKING;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: {btnRestingShadow};
  transform-origin: 50% 50%;
  will-change: transform;
}
.btn-icon {
  font-size: BTN_ICON_SIZE;
  line-height: 1;
}
.brand {
  font-size: BRAND_SIZE;
  font-weight: 800;
  letter-spacing: BRAND_TRACKING;
  color: {brandColor};
  text-transform: uppercase;
}
/* 光标 — 绝对定位，由 GSAP 定位 */
.cursor {
  position: absolute;
  width: CURSOR_SIZE;
  height: CURSOR_SIZE;
  pointer-events: none;
  z-index: 100;
  /* 初始位置由 gsap.set() 设置 */
  transform-origin: 0 0; /* 箭头尖端是点击点 */
  filter: {cursorDropShadow};
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 初始将光标定位在目标外（屏幕外或远角）。
  gsap.set("#cursor", { x: CURSOR_START_X, y: CURSOR_START_Y });

  // 按钮的屏幕中心，在组合坐标中。
  const BUTTON_CENTER = { x: BUTTON_CENTER_X, y: BUTTON_CENTER_Y };

  // 阶段 1 — 光标接近按钮
  tl.to(
    "#cursor",
    {
      x: BUTTON_CENTER.x,
      y: BUTTON_CENTER.y,
      duration: APPROACH_DUR,
      ease: "power2.inOut",
    },
    APPROACH_START,
  );

  // 阶段 2 — 协调按下（按钮 + 光标都缩放到 1 - PRESS_INTENSITY）
  tl.to(
    ["#btn", "#cursor"],
    {
      scale: 1 - PRESS_INTENSITY,
      duration: PRESS_DOWN_DUR,
      ease: "power1.in",
    },
    PRESS_DOWN_AT,
  );

  // 阶段 3 — 释放（两者以过冲弹回 1.0）
  tl.to(
    ["#btn", "#cursor"],
    {
      scale: 1,
      duration: RELEASE_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`,
    },
    RELEASE_AT,
  );

  // 阶段 4 — 按下期间内部辉光（boxShadow 变化与按下缩放同步）
  tl.to(
    "#btn",
    {
      boxShadow: `{btnPressedShadow}`,
      duration: PRESS_DOWN_DUR,
      ease: "power1.in",
    },
    PRESS_DOWN_AT,
  );
  tl.to(
    "#btn",
    {
      boxShadow: `{btnRestingShadow}`,
      duration: RELEASE_DUR,
      ease: "power2.out",
    },
    RELEASE_AT,
  );

  // 品牌提前淡入（上下文）
  tl.from(
    ".brand",
    { opacity: 0, y: BRAND_REVEAL_Y_PX, duration: BRAND_REVEAL_DUR, ease: "power3.out" },
    BRAND_REVEAL_AT,
  );

  // 光标可选在按下后移开（或保持停留）
  tl.to(
    "#cursor",
    { x: CURSOR_EXIT_X, y: CURSOR_EXIT_Y, duration: CURSOR_EXIT_DUR, ease: "power2.out" },
    CURSOR_EXIT_AT,
  );

  window.__timelines["press-react-scene"] = tl;
</script>
```

## 变体

### 多元素链式按下

光标按下按钮 A → 按钮 A 触发交换 → 光标移动到按钮 B → 再次按下。每次按下是一个完整的按下-释放子程序。

### 保持按下（持续压力）

在按下和释放之间插入一个 `HOLD_DUR` 窗口。光标缩放保持在 `1 - PRESS_INTENSITY`，按钮缩放保持在 `1 - PRESS_INTENSITY`，内部辉光保持。暗示"思考中"或"加载中"。

### 同步内部辉光脉冲

在保持阶段，内部辉光脉冲（正弦驱动）。暗示"处理中"：

```js
const holdGlow = { p: 0 };
tl.to(
  holdGlow,
  {
    p: Math.PI * GLOW_PULSE_CYCLES * 2,
    duration: HOLD_DUR,
    ease: "none",
    onUpdate: () => {
      const alpha = GLOW_BASE_ALPHA + Math.sin(holdGlow.p) * GLOW_PULSE_AMP;
      document.getElementById("btn").style.boxShadow =
        `inset 0 0 GLOW_BLUR rgba(255, 255, 255, ${alpha})`;
    },
  },
  HOLD_START_AT,
);
```

## 如何选择值

### 时间（秒）

- **APPROACH_START** — 光标开始向按钮移动的时间。
  - 范围：0-0.3 秒（小的引导没问题；长延迟读作死帧）
- **APPROACH_DUR** — 光标接近时长。
  - 范围：0.7-1.3 秒；更快读作紧急，更慢读作慎重
- **PRESS_DOWN_AT** — 按下触发时间。
  - 约束：必须等于 `APPROACH_START + APPROACH_DUR`，使光标在按下开始时精确到达（避免"在空中点击"）
- **PRESS_DOWN_DUR** — 压缩时长。
  - 范围：0.1-0.25 秒
- **RELEASE_AT** — 释放触发时间。
  - 约束：必须 > `PRESS_DOWN_AT + PRESS_DOWN_DUR`；可选短暂保持（0.05-0.4 秒，或保持按下变体的 `HOLD_DUR`）用于"思考"交互
- **RELEASE_DUR** — 释放弹簧时长。
  - 范围：0.4-0.7 秒（足够长让过冲稳定）
- **BRAND_REVEAL_AT** — 品牌行淡入时间。
  - 约束：必须 < `PRESS_DOWN_AT`（上下文在交互之前）
- **BRAND_REVEAL_DUR** — 品牌淡入时长。
  - 范围：0.4-0.8 秒
- **CURSOR_EXIT_AT / CURSOR_EXIT_DUR** — 释放后可选的光标外向运动。
  - 约束：`CURSOR_EXIT_AT` 必须 ≥ `RELEASE_AT + RELEASE_DUR`，使光标在按下稳定后**才**退出，而非期间

### 物理

- **PRESS_INTENSITY** — 按下压缩的深度。
  - 范围：0.05（微妙）- 0.10（标准）- 0.15（重）
  - 应用为光标和按钮上的 `scale: 1 - PRESS_INTENSITY`（单个 GSAP 目标数组）
- **BOUNCE_FACTOR** — 释放上的 `back.out(${BOUNCE_FACTOR})` 过冲。
  - 范围：1.6（柔和）- 2.0（坚定）- 2.4（卡通）

### 定位

- **CURSOR_START_X / CURSOR_START_Y** — 光标在组合坐标中的初始位置。
  - 约束：在屏幕外或远离按钮的角落，使接近读作运动进入，而非传送
- **BUTTON_CENTER_X / BUTTON_CENTER_Y** — 按钮在屏幕空间中测量的中心。
  - 来源：在组合坐标中测量；对于 1920×1080 下的 `place-items: center`，这是 `(960, 540)`
- **CURSOR_EXIT_X / CURSOR_EXIT_Y** — 释放后光标移动的位置（如果使用）。
  - 范围：任何舞台外或不碍事的位置
- **BRAND_REVEAL_Y_PX** — 品牌初始 y 偏移。
  - 范围：8-20 px

### 布局 / 排版

- **STACK_GAP** — 按钮和品牌行之间的间距。
  - 范围：40-96 px
- **BTN_PADDING_V / BTN_PADDING_H** — 按钮填充。
  - 范围：V 24-40 px，H 60-100 px（水平填充 2-3× 垂直读作胶囊形 CTA）
- **BTN_INNER_GAP** — 按钮内部图标和标签之间的间距。
  - 范围：16-32 px
- **BTN_RADIUS** — 按钮圆角半径。
  - 范围：20-40 px，或 `BTN_PADDING_V + BTN_FONT_SIZE/2` 用于完全圆角端部
- **BTN_FONT_SIZE / BTN_ICON_SIZE** — 按钮内部的排版尺寸。
  - 范围：1080p 下字体 60-100 px；图标 ~1.0-1.1× 字体大小
- **BTN_TRACKING** — 大写按钮文本的字母间距。
  - 范围：4-12 px
- **BRAND_SIZE / BRAND_TRACKING** — 品牌行排版。
  - 范围：40-60 px，间距 8-16 px
- **CURSOR_SIZE** — 光标 SVG 大小。
  - 范围：1080p 下 48-96 px

### 保持按下变体

- **HOLD_DUR** — 按下和释放之间的保持窗口。
  - 范围：0.3-0.8 秒
- **HOLD_START_AT** — 辉光脉冲开始时间。
  - 约束：通常等于 `PRESS_DOWN_AT + PRESS_DOWN_DUR`
- **GLOW_PULSE_CYCLES** — 在 `HOLD_DUR` 内的完整正弦周期数。
  - 范围：1-4（更多周期读作更快的"处理"）
- **GLOW_BASE_ALPHA** — 阿尔法脉冲的中心值。
  - 范围：0.15-0.3
- **GLOW_PULSE_AMP** — 与 `GLOW_BASE_ALPHA` 的峰值偏差。
  - 范围：0.1-0.2；必须满足 `GLOW_BASE_ALPHA - GLOW_PULSE_AMP ≥ 0`
- **GLOW_BLUR** — 内部辉光模糊半径（px）。
  - 范围：24-48 px

### 标记

- **{sceneBg}** — 背景渐变/颜色
- **{font}** — 排版栈
- **{btnBg}** — 按钮背景（通常朝向重音色调的渐变）
- **{btnTextColor}** — 按钮文本颜色
- **{btnRestingShadow}** / **{btnPressedShadow}** — 休息和按下状态的外部和内部 box-shadow 字符串
- **{brandColor}** — 重音品牌颜色
- **{cursorFill}** / **{cursorStroke}** — 光标 SVG 填充和描画
- **{cursorDropShadow}** — 光标深度的 `filter: drop-shadow(...)` 值
- **{Brand}** — 品牌行文案
- **{ctaCopy}** / **{ctaIcon}** — 按钮标签和内联图标字形

## 关键原则

- **光标和按钮上相同的按下缩放** — 物理同步性。如果只有按钮缩放，光标看起来"在空中点击"；如果只有光标缩放，按钮感觉断开连接。
- **光标在按下开始前到达** — 在缩放变化之前必须有清晰的"光标在目标上"时刻。否则按下是未归属的。
- **释放使用 `back.out(${BOUNCE_FACTOR})`** — 两个元素需要一起弹簧过冲。线性释放失去触觉感。
- **内部辉光在按下期间出现，释放时淡出** — 接触的视觉确认。外部阴影缩小（推入），内部辉光出现（能量集中）。
- **光标 `pointer-events: none`** — 光标是装饰性的；如果它捕获事件，下方按钮的悬停/点击行为会损坏。
- **光标 `transform-origin: 0 0`** — 箭头的尖端是点击点，不是其中心。围绕尖端缩放保持点击点稳定。
- **高潮停留 ≥1 秒** — 释放后，组合必须继续 ≥1 秒。按下是一个节拍；观看者需要时间看到结果。

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **光标或按钮上无 CSS `transition`** — 与 GSAP 竞争
- **光标 SVG 带 `pointer-events: none`**
- **按钮上设置 `will-change: transform`**（光标如果需要也可设置）
- **`释放帧 > 按下帧`** — 释放必须在按下之后；否则组合显示无按下的释放
- **不要使用真实的 `mouseenter` / `click` 事件** — HF 是渲染上下文，不是 UI；一切必须通过时间线运行

## 组合

- [press-release-spring.md](press-release-spring.md) — **仅按钮**按下变体；此规则在其上叠加光标
- [cursor-click-ripple.md](cursor-click-ripple.md) — 在点击点添加涟漪效果
- [scale-swap-transition.md](scale-swap-transition.md) — 按下**触发**交换

## 与 HF 技能配对

- `/hyperframes-animation` — 通过数组的协调多目标补间
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
