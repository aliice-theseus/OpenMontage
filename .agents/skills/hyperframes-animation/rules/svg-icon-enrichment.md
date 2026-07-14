---
name: svg-icon-enrichment
description: 动画化内部 SVG 元素（旋转指针、打开刀片、脉冲点、虚线流）使图标在不替换它们的情况下感觉生动。
metadata:
  tags: svg, icon, animation, internal, micro-animation, pulse, rotation
---

# SVG 图标丰富化

将 SVG 图标视为可动画化**部件**的组合，而非不透明图像。每个有意义的内部元素（时钟指针、剪刀刀片、录制点、数据线）获得自己的 GSAP 驱动微动画。与 [svg-path-draw](svg-path-draw.md)**不同**（后者动画化**轮廓**绘制）— 丰富化动画化**内部部件**，理想情况下在轮廓绘制之后。

## 工作原理

SVG 使用命名的 `<line>`、`<circle>`、`<path>` 或 `<g>` 子元素编写。GSAP 时间线通过选择器定位它们，应用 4 种标志性运动模式之一：

1. **旋转** — 时钟指针、齿轮、加载旋转器（`transform: rotate(deg)`）
2. **振荡** — 剪刀刀片、翅膀拍打、开关（对侧组上的 `transform: rotate(±sin*amp)`）
3. **脉冲** — 录制点、心形、通知（通过 sin 实现的 `scale + opacity`）
4. **虚线流** — 沿描画的移动虚线，如数据流（`strokeDashoffset` 线性）

所有运行都在暂停的 GSAP 时间线内，因此 HF 可确定性定位。

## HTML

```html
<div
  class="scene"
  data-composition-id="enrichment-scene"
  data-start="0"
  data-duration="4"
  data-track-index="0"
>
  <div class="stack">
    <div class="row">
      <!-- 时钟图标 — 分针旋转 -->
      <svg class="icon-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <circle cx="60" cy="60" r="50" fill="none" stroke="{accentColor}" stroke-width="6" />
        <line
          class="clock-hand"
          id="hand-min"
          x1="60"
          y1="60"
          x2="60"
          y2="22"
          stroke="{textColor}"
          stroke-width="6"
          stroke-linecap="round"
        />
        <line
          class="clock-hand"
          id="hand-sec"
          x1="60"
          y1="60"
          x2="60"
          y2="30"
          stroke="{recordColor}"
          stroke-width="3"
          stroke-linecap="round"
        />
        <circle cx="60" cy="60" r="6" fill="{textColor}" />
      </svg>

      <!-- 录制点 — 脉冲 -->
      <svg class="icon-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <circle
          id="rec-ring"
          cx="60"
          cy="60"
          r="50"
          fill="none"
          stroke="{recordColor}"
          stroke-width="4"
        />
        <circle id="rec-dot" cx="60" cy="60" r="22" fill="{recordColor}" />
      </svg>

      <!-- 数据流 — 虚线沿线条流动 -->
      <svg class="icon-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect
          x="14"
          y="48"
          width="92"
          height="24"
          rx="12"
          fill="none"
          stroke="{accentColor}"
          stroke-width="4"
        />
        <line
          id="data-flow"
          x1="14"
          y1="60"
          x2="106"
          y2="60"
          stroke="{accentColor}"
          stroke-width="6"
          stroke-linecap="round"
          stroke-dasharray="14 12"
        />
      </svg>
    </div>
    <div class="brand">{brandPhrase}</div>
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
  font-family: {font};
}
.stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 80px;
}
.row {
  display: flex;
  gap: 120px;
}
.icon-svg {
  width: 320px;
  height: 320px;
  filter: drop-shadow(0 12px 32px {shadowColor});
}
.clock-hand {
  /* SVG 中的 transform-origin 必须使用 viewBox 单位，而非像素 */
  transform-origin: 60px 60px;
  transform-box: fill-box;
}
.brand {
  font-size: 64px;
  font-weight: 900;
  letter-spacing: 14px;
  text-transform: uppercase;
  color: {textColor};
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 模式 1 — 旋转（时钟指针）
  // 分针：在 TOTAL_DURATION 内 MIN_REVOLUTIONS 次完整旋转
  const minState = { deg: 0 };
  tl.to(
    minState,
    {
      deg: 360 * MIN_REVOLUTIONS,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        document.getElementById("hand-min").style.transform = `rotate(${minState.deg}deg)`;
      },
    },
    0,
  );

  // 秒针：在 TOTAL_DURATION 内 SEC_REVOLUTIONS 次完整旋转（更快）
  const secState = { deg: 0 };
  tl.to(
    secState,
    {
      deg: 360 * SEC_REVOLUTIONS,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        document.getElementById("hand-sec").style.transform = `rotate(${secState.deg}deg)`;
      },
    },
    0,
  );

  // 模式 2 — 脉冲（录制点，环不透明度反向）
  const pulseState = { p: 0 };
  tl.to(
    pulseState,
    {
      p: Math.PI * 2 * PULSE_CYCLES,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        const dotScale = 1 + Math.sin(pulseState.p) * PULSE_DOT_AMP;
        const ringScale = 1 + Math.sin(pulseState.p + Math.PI / 2) * PULSE_RING_AMP;
        const ringOpacity =
          PULSE_RING_OPACITY_BASE + Math.sin(pulseState.p) * PULSE_RING_OPACITY_AMP;
        const dot = document.getElementById("rec-dot");
        const ring = document.getElementById("rec-ring");
        dot.style.transform = `scale(${dotScale})`;
        dot.style.transformOrigin = "60px 60px";
        ring.style.transform = `scale(${ringScale})`;
        ring.style.transformOrigin = "60px 60px";
        ring.style.opacity = String(ringOpacity);
      },
    },
    0,
  );

  // 模式 3 — 虚线流（数据流）
  const flowState = { offset: 0 };
  tl.to(
    flowState,
    {
      offset: DASH_FLOW_TOTAL_OFFSET, // 负值 = 从左到右流，正值 = 从右到左
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        document.getElementById("data-flow").style.strokeDashoffset = String(flowState.offset);
      },
    },
    0,
  );

  // 品牌提前淡入
  tl.from(".brand", { opacity: 0, y: 16, duration: 0.6, ease: "power3.out" }, BRAND_AT);

  window.__timelines["enrichment-scene"] = tl;
</script>
```

## 如何选择值

- **MIN_REVOLUTIONS** — 分针在 TOTAL_DURATION 内的旋转次数
  - 范围：0.5–2.0（连续；更快读作延时摄影）
  - 约束：如果可见结束帧重要，避免整数旋转（会回到起点）

- **SEC_REVOLUTIONS** — 秒针在 TOTAL_DURATION 内的旋转次数
  - 范围：4–10（应明显快于分针）
  - 约束：SEC_REVOLUTIONS > MIN_REVOLUTIONS × 3 才能使速度差异可读

- **PULSE_CYCLES** — 在 TOTAL_DURATION 内的脉冲周期数
  - 范围：在 3–5 秒组合上 2–4
  - 效果：≥ 5 读作焦虑闪烁；≤ 1 读作被遗忘

- **PULSE_DOT_AMP** — 点缩放振幅
  - 范围：0.05–0.20
  - 效果：0.05 = 呼吸；0.20 = 搏动

- **PULSE_RING_AMP** — 环缩放振幅（通常低于 DOT_AMP）
  - 范围：0.04–0.12
  - 约束：必须 < PULSE_DOT_AMP，否则环掩盖点

- **PULSE_RING_OPACITY_BASE / PULSE_RING_OPACITY_AMP** — 环不透明度基线 + 正弦振幅
  - 范围：BASE 0.4–0.6；AMP 0.3–0.5
  - 约束：BASE − AMP ≥ 0 且 BASE + AMP ≤ 1

- **DASH_FLOW_TOTAL_OFFSET** — 在 TOTAL_DURATION 内 stroke-dashoffset 的总变化
  - 范围：-400 到 -100（负值从左到右）或 +100 到 +400（从右到左）
  - 效果：|大| = 快速流；|小| = 缓慢漂移
  - 约束：必须为虚线周期（虚线 + 间隙）的整数倍，否则循环结束帧会显示相位跳变

- **BRAND_AT** — 品牌短语淡入的时间
  - 范围：0.3–1.0 秒
  - 效果：太早与图标入场竞争；太晚感觉附加

- **缓动族选择**：旋转 = `none`（线性运动就是关键）；脉冲驱动 = `none`（正弦处理曲线）；品牌揭示 = `power3.out`

## 标志性运动模式

| 模式     | 用途                     | 数学                                              | 提示                               |
| -------- | ------------------------ | ------------------------------------------------- | ---------------------------------- |
| 旋转     | 时钟、齿轮、加载器、刻度 | `transform: rotate(deg)`，通过秒计数器线性       | `transform-origin` 使用 viewBox 单位 |
| 振荡     | 剪刀、翅膀、开关         | 对侧组上的 `rotate(±sin*amp)`                    | 两个部分使用相反符号               |
| 脉冲     | 录制点、心形、通知       | `scale(1 + sin*amp)` + 不透明度                   | 环延迟点 π/2 以产生涟漪效果        |
| 虚线流   | 切割线、数据流           | 通过时间的 `strokeDashoffset` 线性                | 负值从左到右，正值从右到左         |

## 变体

### 描画绘制 → 丰富化链

首先绘制图标轮廓（通过 [svg-path-draw](svg-path-draw.md)），**然后**激活丰富化。内部动画感觉像图标在组装后"唤醒"。

```js
// 阶段 1：轮廓绘制（0 → OUTLINE_DUR）
tl.fromTo(
  "#icon-outline",
  { strokeDashoffset: 360 },
  { strokeDashoffset: 0, duration: OUTLINE_DUR, ease: "power2.inOut" },
  0,
);
// 阶段 2：丰富化在 OUTLINE_DUR 开始
```

### 每图标进入错开

对于一行图标全部动画化，错开它们的进入。每个图标的丰富化在其淡入时开始，而非同步 — 感觉有机。

## 关键原则

- **❗ 对于围绕 SVG 内部明确点的旋转，使用 SVG `transform` 属性，而非 CSS transform** — `el.setAttribute('transform', \`rotate(${deg} ${cx} ${cy})\`)`。CSS 组合 `transform: rotate(...)` + `transform-origin: 60px 60px` + `transform-box: fill-box` 在元素**自身**的 bbox 局部坐标中解释原点，**而非** viewBox 坐标。对于细 `<line>`（其 bbox 是线条的窄包络），bbox 局部中的 `60 60` 指的是线条**外部**的点，因此指针沿偏离中心的弧线而非在适当位置旋转。对于小的内部形状（rec-dot 圆，其 bbox 是小圆而非完整 viewBox）也是同样的陷阱。
- **对于围绕 SVG 内中心点的缩放**，使用 `el.setAttribute('transform', \`translate(${cx} ${cy}) scale(${s}) translate(-${cx} -${cy})\`)`。原因相同 — 避免 CSS bbox 局部原点陷阱。
- **在时间线内运行连续动画** — 不要使用 CSS `@keyframes` 或 `requestAnimationFrame`。两者都会与 HF 的逐帧定位不同步。
- **振幅微妙** — 图标是装饰性的，非标题。在以上范围内脉冲缩放；相对于组合长度校准旋转速度，而非绝对时间。
- **同一图标的不同部分处于不同相位** — 时钟分针与秒针速度不同，环与点脉冲偏移 π/2。纯同步看起来机械；相位偏移看起来生动。
- **❗ 高潮停留 ≥ 1 秒** — 如果丰富化是标题节拍，组合必须在最戏剧性时刻之后继续 ≥ 1 秒。

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **SVG 子元素上无 CSS `animation`** — 必须是时间线驱动
- **`transform-origin` 每个子元素不同** — 为每个动画元素显式设置
- **流动/虚线线上的 `stroke-linecap: round`** 用于干净的虚线边缘
- **通过 id 定位 SVG 子元素** — `document.getElementById` 没问题；选择器链进入 `<svg>` 与 HTML 相同

## 组合

- [svg-path-draw.md](svg-path-draw.md) — 首先绘制轮廓，然后激活丰富化
- [orbit-3d-entry.md](orbit-3d-entry.md) — 轨道项目是丰富化的图标（时钟围绕品牌标签轨道运行）
- [sine-wave-loop.md](sine-wave-loop.md) — 整个图标浮动，同时内部部件动画化

## 与 HF 技能配对

- `/hyperframes-animation` — onUpdate 为每个 SVG 子元素写入 transform/opacity
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
