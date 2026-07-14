---
name: press-release-spring
description: 触觉按钮按下，带线性压缩、基于弹簧的弹性恢复和分层视觉反馈（阴影缩小 + 释放爆发 + 背景辉光）。
metadata:
  tags: spring, press, interaction, button, physics, glow, burst, ui
---

# 按下-释放弹簧链

将输入（线性压缩）与输出（弹簧恢复）分离，创造触觉感觉。过冲是弹簧配置的自然副产品，非手动编码。与在同一触发帧上分层的次级运动（阴影缩小、释放爆发、背景辉光）配对。

## 工作原理

两个不同的阶段在**释放**时刻分割：

1. **按下**：线性缓动 → 压缩（`scale: 1 → PRESS_SCALE`，阴影缩小）。线性，非弹簧 — 下压必须读作瞬时/触觉，而非软绵绵。
2. **释放**：`back.out(${BOUNCE_FACTOR})` 弹簧 → 弹性弹回 `1.0`（过冲与 `BOUNCE_FACTOR` 成比例）。可选爆发辉光环在按钮后扩大；可选背景环境辉光淡入。

状态连续性至关重要：释放补间的起始值**必须**等于按下补间的结束值，否则弹簧会跳到不同位置。当两个补间在同一时间线的相邻位置定位相同属性时，GSAP 自动处理这一点。

## HTML

```html
<div
  class="scene"
  id="press-scene"
  data-composition-id="press-scene"
  data-start="0"
  data-duration="DURATION"
  data-track-index="0"
>
  <div class="press-stage">
    <div class="bg-glow" id="bg-glow"></div>
    <div class="burst" id="burst"></div>
    <button class="btn" id="btn">{buttonLabel}</button>
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
  background: {bgColor};
}
.press-stage {
  position: relative;
  display: grid;
  place-items: center;
}
.btn {
  position: relative;
  z-index: 2;
  /* 视觉重量：在 1080p 画面上按下可读需要 ≥4% 的画布 */
  width: BTN_WIDTH;
  height: BTN_HEIGHT;
  background: {btnBg};
  border: none;
  border-radius: BTN_RADIUS;
  font-family: {font};
  font-weight: 900;
  font-size: BTN_FONT_SIZE;
  letter-spacing: BTN_LETTER_SPACING;
  color: {btnTextColor};
  text-transform: uppercase;
  /* 将压缩锚定在中心 — 参见关键约束 */
  transform-origin: 50% 50%;
  /* 初始浮动阴影 — 大而扩散 */
  box-shadow: {btnRestShadow};
}
.burst {
  /* 位于按钮后面，相同占地面积 */
  position: absolute;
  z-index: 1;
  inset: 0;
  width: BTN_WIDTH;
  height: BTN_HEIGHT;
  background: {burstGradient};
  filter: blur(BURST_BLUR);
  opacity: 0;
  transform: scale(1);
  pointer-events: none;
}
.bg-glow {
  /* 全舞台径向 — 通过负 inset 扩展到舞台之外 */
  position: absolute;
  inset: BG_GLOW_INSET;
  background: {bgGlowGradient};
  opacity: 0;
  pointer-events: none;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 阶段 1 — 按下（线性压缩）
  tl.to(
    "#btn",
    {
      scale: PRESS_SCALE,
      boxShadow: "{btnPressedShadow}",
      duration: PRESS_DUR,
      ease: "power1.in",
    },
    PRESS_START,
  );

  // 阶段 2 — 释放（带过冲的弹簧回弹）
  // 关键：起始缩放 == 阶段 1（PRESS_SCALE）的结束值以保持状态连续性。
  tl.to(
    "#btn",
    {
      scale: 1,
      boxShadow: "{btnRestShadow}",
      duration: RELEASE_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`,
    },
    RELEASE_START,
  );

  // 阶段 3 — 爆发辉光（按钮后的径向弹出），与释放同时触发
  tl.fromTo(
    "#burst",
    { scale: 1, opacity: 0 },
    {
      scale: BURST_PEAK_SCALE,
      opacity: BURST_PEAK_OPACITY,
      duration: BURST_GROW_DUR,
      ease: "power2.out",
    },
    RELEASE_START,
  );
  // 爆发然后淡出
  tl.to("#burst", { opacity: 0, duration: BURST_FADE_DUR, ease: "power2.in" }, BURST_FADE_START);

  // 阶段 4 — 背景环境辉光在释放后淡入
  tl.to(
    "#bg-glow",
    {
      opacity: BG_GLOW_PEAK_OPACITY,
      duration: BG_GLOW_FADE_DUR,
      ease: "power2.out",
    },
    RELEASE_START,
  );

  window.__timelines["press-scene"] = tl;
</script>
```

## 变体

### 微妙按下（状态保存 / 静音 CTA）

较少压缩，较温和过冲，较小爆发。`PRESS_SCALE` 朝向范围高端（~0.96），`BOUNCE_FACTOR` 朝向范围低端（~1.4），`BURST_PEAK_SCALE` 和 `BURST_PEAK_OPACITY` 减小。

### 戏剧性按下（主角 CTA / "发货"时刻）

更深压缩，更多过冲，更大爆发。`PRESS_SCALE` 朝向范围低端（~0.88），`BOUNCE_FACTOR` 朝向范围高端（~2.5），`BURST_PEAK_SCALE` 和 `BURST_PEAK_OPACITY` 最大化。

### 按下期间颜色偏移

在按下中段使按钮变暗，在释放时恢复。与缩放补间相同的时间线位置 — 在 `#btn` 上插值的 `backgroundColor`。状态连续性规则仍然适用：释放颜色补间的起始等于按下颜色补间的结束。

```js
tl.to("#btn", { backgroundColor: "{btnPressedColor}", duration: PRESS_DUR }, PRESS_START);
tl.to("#btn", { backgroundColor: "{btnRestColor}", duration: RELEASE_DUR }, RELEASE_START);
```

### 释放时状态变化（批准/确认模式）

当按下确认信号时，在 `RELEASE_START` 时（而非返回到 `{btnRestColor}`）将按钮的休息颜色交换为成功标记，然后通过在同一位置的独立 `back.out(${CHECK_BOUNCE})` 补间弹出勾选标记。按钮现在处于终端状态 — 不再期望进一步按下。

```js
tl.to("#btn", { backgroundColor: "{successColor}", duration: RELEASE_DUR }, RELEASE_START);
tl.to(
  ".btn-check",
  { scale: 1, duration: CHECK_POP_DUR, ease: `back.out(${CHECK_BOUNCE})` },
  RELEASE_START,
);
```

## 如何选择值

### 几何

- **BTN_WIDTH / BTN_HEIGHT** — 按钮占地面积。
  - 范围：按钮面积 ≥ 画布的 3-5%（1080p 下 320×68 的按钮约 1%，读作视觉上微不足道）
  - 效果：较小 → 按下几乎不可读；较大 → 按下主导画面
  - 约束：`BTN_WIDTH × BTN_HEIGHT / (canvasW × canvasH) ≥ 0.03`
- **BTN_RADIUS** — 圆角半径。
  - 范围：`BTN_HEIGHT × 0.15`（锐利/现代）→ `BTN_HEIGHT / 2`（胶囊）
- **BTN_FONT_SIZE / BTN_LETTER_SPACING** — 排版重量。
  - 范围：`BTN_FONT_SIZE ≈ BTN_HEIGHT × 0.4-0.5`；字母间距 4-10 px 读作"可操作标签"

### 按下动力学

- **PRESS_SCALE** — 压缩深度。
  - 范围：0.88（戏剧性）→ 0.92（默认）→ 0.96（微妙）
  - 效果：较低 → 更触觉/更重；较高 → 几乎不可察觉的确认
  - 约束：决不低于 0.85（按钮感觉损坏）或高于 0.98（无明显下压）
- **PRESS_DUR** — 压缩时长。
  - 范围：0.10-0.30 秒
  - 效果：更短 → 更干脆/"瞬时感"；更长 → 缓慢挤压
  - 约束：比 `RELEASE_DUR` 短（输入比弹簧恢复快）
- **RELEASE_DUR** — 弹簧恢复时长。
  - 范围：0.40-0.90 秒
  - 效果：更短 → 紧密弹出；更长 → 宽松、摇晃稳定
- **BOUNCE_FACTOR** — `back.out(BOUNCE_FACTOR)` 过冲强度。
  - 范围：1.4（柔和）→ 2.0（坚定弹出）→ 2.8（卡通）
  - 效果：低端几乎没有过冲；高端读作卡通化；按感觉调节
  - 替代：切换到 `elastic.out(amplitude, period)` 以获得橡胶振荡而非单次过冲
- **PRESS_START / RELEASE_START** — 时间线位置。
  - 约束：`RELEASE_START = PRESS_START + PRESS_DUR`（状态连续性 — 参见关键约束）

### 爆发辉光

- **BURST_PEAK_SCALE** — 径向弹出最大缩放。
  - 范围：3（微妙）→ 6（默认）→ 8（戏剧性）
  - 约束：≤ ~8 — 超过此值径向渐变像素化明显
- **BURST_PEAK_OPACITY** — 爆发最大不透明度。
  - 范围：0.4（微妙）→ 0.8（默认）→ 1.0（戏剧性）
- **BURST_GROW_DUR / BURST_FADE_DUR** — 增长 vs 淡出时间。
  - 范围：每个 0.4-0.7 秒；默认增长 ≈ 淡出
- **BURST_BLUR** — 爆发层上的高斯模糊。
  - 范围：40-100 px；较小读作硬环，较大读作环境雾

### 背景辉光

- **BG_GLOW_PEAK_OPACITY** — 环境辉光峰值。
  - 范围：0.1（微妙）→ 0.25（默认）→ 0.45（戏剧性）
  - 约束：≤ 0.45 — 更高会冲刷整个组合
- **BG_GLOW_FADE_DUR** — 淡入时长。
  - 范围：0.6-1.0 秒
- **BG_GLOW_INSET** — 负 inset，使径向扩展到舞台边缘之外。
  - 范围：在 1920×1080 画布上通常为 `-300` 到 `-500` px

### 可选"批准"变体

- **CHECK_BOUNCE** — 勾选标记弹出过冲。
  - 范围：1.4-2.0；比按钮的主 `BOUNCE_FACTOR` 更坚定，读作标点性的"盖章"
- **CHECK_POP_DUR** — 勾选标记放大时长。
  - 范围：0.3-0.6 秒

### 标记

- **{btnBg} / {btnRestColor} / {btnPressedColor}** — 主要按钮表面；按下比休息深
- **{btnRestShadow} / {btnPressedShadow}** — 休息阴影大而扩散；按下小而紧（按钮"向表面下沉"）
- **{burstGradient}** — 径向；中心饱和，渐变为透明（颜色应比 `{btnBg}` 更深、更饱和 — 同色辉光看起来褪色）
- **{bgGlowGradient}** — 全舞台径向，`{btnBg}` 色调系的低不透明度着色
- **{successColor}** — 确认绿色/品牌成功色，用于批准变体

## 关键原则

- **状态连续性** — 释放起始值必须精确匹配按下结束值。使用 GSAP 时间线，当它们在同一时间线上相邻时间定位相同属性时，第一个补间的结束值自动成为第二个补间的起始值。
- **视觉重量** — 按钮面积应 **≥ 画布的 3-5%**。更小则按下读作视觉上微不足道。
- **线性按下，弹簧释放** — 压缩是 `power1.in/out`，恢复是 `back.out`。两者都弹簧 → 软绵绵；都线性 → 机械/无过冲冲击。
- **压缩锚定在中心** — `transform-origin: 50% 50%`（默认）。否则按钮不对称塌缩。
- **爆发在后面，不在前面** — 爆发 `z-index: 1`，按钮 `z-index: 2`。如果爆发在前面，它在峰值不透明度时遮挡按钮。
- **辉光颜色比元素更深、更饱和** — 亮表面 → 暗、饱和辉光。同色辉光看起来褪色。
- **不要在同一元素上同时补间 `boxShadow` 和 `filter`** — 它们在布局管线中竞争；选择其一。阴影在按钮上，模糊在独立的爆发层上。
- **高潮节拍需要停留时间** — 爆发峰值 + 标签/wordmark 揭示后，组合必须在结束前继续运行 **≥1 秒**（"戏剧性"变体 ≥2 秒）。在 `t=DURATION−0.2s` 的揭示读作"闪烁然后消失。"

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **按钮上无 CSS `transition`** — 那些会独立于 HF 定位插值并导致闪烁
- **如果按钮与其他动画层组合，设置 `will-change: transform`**
- **`RELEASE_START = PRESS_START + PRESS_DUR`** — 相同属性上的相邻位置是状态连续性自动保持的关键；间隙或重叠会破坏它
- **爆发最大缩放 ≤ ~8** — 超过此值径向渐变像素化明显
- **背景辉光 `opacity ≤ 0.45`** — 更高会冲刷整个组合
- **仅使用 GSAP 变换别名**：`x`、`y`、`scale`、`rotation`。永远不要补间 `width` / `height` / `left` / `top`。

## 组合

- [sine-wave-loop.md](sine-wave-loop.md) — 按下前按钮上的空闲微浮动（轻微呼吸，传达"就绪"）
- [center-outward-expansion.md](center-outward-expansion.md) — 徽章爆发向外，与释放同步
- [cursor-click-ripple.md](cursor-click-ripple.md) — 触发按下的光标点击

## 与 HF 技能配对

- `/hyperframes-animation` — `back.out` 缓动 + 多补间协调
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
