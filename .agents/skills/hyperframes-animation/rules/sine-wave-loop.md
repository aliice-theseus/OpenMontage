---
name: sine-wave-loop
description: 有界正弦驱动空闲 — 保持元素上的微妙抖动或单个确实需要的有界环境呼吸。降低优先级：作为"生命力"的循环呼吸很廉价；优先选择按 VO 定时的顺序揭示，然后是微妙抖动，最后才使用此规则。
metadata:
  tags: idle, jitter, bounded-ambient, sine, trigonometry, low-amplitude, post-entry
---

# 正弦波循环（微妙抖动 / 有界环境）

> **最后才使用此规则。** 根据动效原则（`references/motion-language.md`）：**循环呼吸 — 将文本/卡片上下缩放以显得"有生命" — 是廉价的，是代理的条件反射式作弊，读作软弱。** "我宁愿没有运动也不要有糟糕的运动。"在使用此规则保持画面活跃之前，优先选择 (1) **按配音定时的顺序揭示** — 在场景的后半部分，当配音说出时揭示下一行/元素；那，而非环境运动，才是填充镜头的关键。如果画面确实已经稳定且仍需要一点生命力，**被认可的动作是微妙抖动** — 一个小的、低振幅的抖动（此规则，在其振幅范围的**低端**）。完整的呼吸循环保留给罕见的单个保持主角确实需要有界环境的情况；保持低调且小量。

使用由有限时间线补间驱动的 `Math.sin` 来保持稳定元素不显得死板 — 作为**微妙抖动**或，罕见的，单个有界环境呼吸。这是动词语汇中"微妙抖动"动作背后的实现；它**不是**让每个主角都呼吸的许可证。

## 工作原理

一个长补间将 `phase` 值从 0 → 2π（或 0 → 某个倍数）推进。在每个 onUpdate 上，相位反馈到 `Math.sin()` 以产生添加到元素变换（`scale`、`translateY`、`rotate`）的小周期偏移。

从进入过渡到空闲"无跳跃"的技巧：在 `phase = 0` 时，`sin(0) = 0` — 偏移为零，因此元素从其进入后休息状态开始。

## HTML

```html
<div
  class="scene"
  id="idle-scene"
  data-composition-id="idle-scene"
  data-start="0"
  data-duration="6"
  data-track-index="0"
>
  <div class="stack">
    <div class="hero" id="hero">{HeroLabel}</div>
    <div class="dot" id="dot"></div>
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
}
.stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: STACK_GAP;
}
.hero {
  font-family: {font};
  font-weight: 900;
  font-size: HERO_FONT_SIZE;
  letter-spacing: HERO_LETTER_SPACING;
  color: {textColor};
  text-transform: uppercase;
  /* 元素获得进入后休息变换；空闲仅向其添加 */
  will-change: transform;
}
.dot {
  width: DOT_SIZE;
  height: DOT_SIZE;
  border-radius: 50%;
  background: {accentColor};
  box-shadow: {accentGlow};
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const hero = document.getElementById("hero");
  const dot = document.getElementById("dot");

  // 阶段 1 — 进入节拍（例如标题淡入）
  tl.fromTo(
    hero,
    { opacity: 0, y: ENTRY_Y, scale: ENTRY_SCALE },
    { opacity: 1, y: 0, scale: 1, duration: ENTRY_DUR, ease: "power3.out" },
    0,
  );
  tl.fromTo(
    dot,
    { opacity: 0, scale: 0 },
    { opacity: 1, scale: 1, duration: DOT_ENTRY_DUR, ease: `back.out(${BOUNCE_FACTOR})` },
    DOT_ENTRY_START,
  );

  // 阶段 2 — 空闲呼吸。在进入稳定后在 IDLE_START_TIME 开始。
  // 通过单个补间驱动相位 0 → 2π * CYCLES，将 sin() 写入变换。

  const phase = { p: 0 };
  tl.to(
    phase,
    {
      p: Math.PI * 2 * CYCLES,
      duration: IDLE_DUR,
      ease: "none",
      onUpdate: () => {
        // 主角：缩放呼吸 ±SCALE_AMP，y 摆动 ±Y_AMP_PX
        const scale = 1 + Math.sin(phase.p) * SCALE_AMP;
        const y = Math.sin(phase.p) * Y_AMP_PX;
        hero.style.transform = `translateY(${y}px) scale(${scale})`;

        // 点：异相缩放（偏移 π/2）— 感觉生动而非同步
        const dotScale = 1 + Math.sin(phase.p + Math.PI / 2) * DOT_SCALE_AMP;
        dot.style.transform = `scale(${dotScale})`;
      },
    },
    IDLE_START_TIME,
  );

  window.__timelines["idle-scene"] = tl;
</script>
```

## 变体

### 多偏移频率（有机多八度呼吸）

组合频率比纯正弦感觉更生动：

```js
const primary = Math.sin(phase.p) * SCALE_AMP_PRIMARY;
const secondary = Math.sin(phase.p * OCTAVE_RATIO) * SCALE_AMP_SECONDARY; // 更高频率覆盖
const scale = 1 + primary + secondary;
```

### 条件激活（仅在进入稳定后）

如果进入是可交互或可跳过的，门控空闲：

```js
const idleActive = entryProgress >= GATE_THRESHOLD;
const scale = idleActive ? 1 + Math.sin((time - IDLE_START_TIME) / PERIOD) * SCALE_AMP : 1;
```

### 稳定并淡出（长时空闲门控 — 当 `IDLE_DUR > 6s` 时强烈推荐）

通过一个在空闲最后 ~20% 淡入淡出到零的包络驱动振幅，使场景在场景间过渡到来之前明显稳定：

```js
const phase = { p: 0 };
const FADE_FRAC = 0.2; // 空闲最后 20% = 振幅渐降到 0
tl.to(
  phase,
  {
    p: Math.PI * 2 * CYCLES,
    duration: IDLE_DUR,
    ease: "none",
    onUpdate: () => {
      const t = phase.p / (Math.PI * 2 * CYCLES); // 在空闲中 0 → 1
      const env = t < 1 - FADE_FRAC ? 1 : (1 - t) / FADE_FRAC; // 尾部中 1 → 0
      const scale = 1 + Math.sin(phase.p) * SCALE_AMP * env;
      const y = Math.sin(phase.p) * Y_AMP_PX * env;
      hero.style.transform = `translateY(${y}px) scale(${scale})`;
    },
  },
  IDLE_START_TIME,
);
```

元素在空闲的前 80% 处于运动中，然后在后 20% 停下。天然适配边界中断的 Tier-B 过渡（当交叉淡入淡出/推进开始时，退出的视觉是静态的）。

### 周期 vs 循环计算

对于精确的 N 秒周期：

```js
const divisor = (idleDurationSec * fps) / (Math.PI * 2);
const value = Math.sin(frame / divisor) * amplitude;
```

对于 HF（`onUpdate` 不直接暴露帧），使用补间的 `phase` 值：在 `duration: idleDurationSec` 上驱动 `p: Math.PI * 2 * cyclesWanted`。

## 如何选择值

### 布局 / 排版

- **STACK_GAP** — 主角和点之间的垂直间距。
  - 范围：0.2-0.4× `HERO_FONT_SIZE`
- **HERO_FONT_SIZE / HERO_LETTER_SPACING** — 排版强调。
  - 范围：全出血组合 100-240 px；间距 0.04-0.06em
- **DOT_SIZE** — 重音指示器大小。
  - 范围：~0.15-0.25× `HERO_FONT_SIZE` 使点读作重音而非同级
- **{accentGlow}** — 点上的 `box-shadow` 光晕；通常为 `0 0 (DOT_SIZE) rgba(accentColor, 0.5-0.7)`

### 进入阶段

- **ENTRY_Y / ENTRY_SCALE** — 淡入前的初始状态。
  - 范围：`ENTRY_Y` 16-32 px（微妙上升），`ENTRY_SCALE` 0.94-0.98（微妙膨胀）
- **ENTRY_DUR** — 主角淡入时长。
  - 范围：0.6-1.2 秒；更大的主角需要更长的稳定
- **DOT_ENTRY_START** — 点相对于主角弹出时间。
  - 约束：通常 `≈ 0.4-0.6× ENTRY_DUR` 使点在主角仍在稳定时着陆，而非之后
- **DOT_ENTRY_DUR** — 点 back-out 弹出时长。
  - 范围：0.4-0.7 秒
- **BOUNCE_FACTOR** — 点弹出上的 `back.out(BOUNCE_FACTOR)` 过冲强度。
  - 范围：1.4（柔和）→ 2.0（坚定）→ 2.8（卡通）

### 空闲阶段

- **IDLE_START_TIME** — 呼吸开始时间。
  - 约束：`≥ ENTRY_DUR + 小缓冲（~0.1 秒）` 使呼吸不与进入尾部冲突。此时 `sin(0) = 0`，因此偏移正是进入的休息状态 — 无跳跃
- **IDLE_DUR** — 呼吸补间长度。
  - 约束：必须等于 `TOTAL_DURATION − IDLE_START_TIME` 以用运动填满组合
- **CYCLES** — 在 `IDLE_DUR` 内完整呼吸周期数。
  - 范围：`IDLE_DUR / 3s ≤ CYCLES ≤ IDLE_DUR / 1.5s`（周期 1.5-3 秒读作自然呼吸）
- **SCALE_AMP** — 缩放的正弦振幅（主角）。
  - **默认：0.008-0.015**（几乎不可察觉的呼吸 — 大多数场景的正确答案）
  - 仅当元素在 canvas 上**单独**、场景**短（< 6s）**或需求明确要求**动感/俏皮**基调时推到 0.02-0.04
  - 参见关键原则了解长时空闲/并发元素缩放规则
- **Y_AMP_PX** — y 平移的正弦振幅（主角）。
  - **默认：2-3 px**（几乎不可察觉 — 大多数场景的正确答案）
  - 仅当隔离/短/动感时推到 4-6 px — 与 `SCALE_AMP` 相同的门控条件
- **DOT_SCALE_AMP** — 点缩放的正弦振幅（偏移 π/2 以实现异相运动）。
  - 范围：0.04-0.12 — 比主角振幅大可以接受，因为点是小的重音
- **PERIOD**（条件激活变体）— 使用 `(time - IDLE_START_TIME) / PERIOD` 形式时每秒周期数。
  - 范围：1.5-3 秒
- **GATE_THRESHOLD**（条件激活变体）— 开始空闲所需的 entryProgress。
  - 范围：0.85-1.0；较低的阈值在进入完成前稍早开始空闲以重叠

### 多八度变体

- **SCALE_AMP_PRIMARY / SCALE_AMP_SECONDARY** — 两个堆叠正弦的振幅。
  - 约束：`SCALE_AMP_PRIMARY > SCALE_AMP_SECONDARY`（副部是高频覆盖，而非同级）；组合最大振幅应保持在上述 SCALE_AMP 范围内
- **OCTAVE_RATIO** — 副部相对于主部的频率倍数。
  - 范围：2.0-4.0（整数组比例感觉音乐化/连贯；非整数比例感觉有机/不可预测）

### 颜色标记

- **{bgGradient}** — 通常为暗色径向渐变，使点亮的主角突出
- **{textColor}** — 与 `{bgGradient}` 的高对比度
- **{accentColor}** — 保留给点的单一重音；`{accentGlow}` 中的辉光颜色是相同色相

## 关键原则

- **优先选择揭示，然后抖动，然后呼吸** — 作为"生命力"的循环呼吸很廉价且读作软弱；"无运动优于不良运动。"首先用**按 VO 定时的顺序揭示**填充镜头的后部；如果确实稳定了仍感觉死板，在此规则的**低端振幅范围作为微妙抖动**使用；完整的呼吸循环是单个保持主角上的罕见最后手段，绝不印在每个元素上。
- **`sin(0) = 0`** — 在空闲开始的时刻，偏移必须为零，这样从进入的稳定状态到空闲没有可见跳跃。从 `phase = 0` 开始相位补间。
- **振幅微妙 — 默认使用范围的低端。** 缩放 `0.008-0.015`（仅当隔离/短场景/动感需求时推到 0.02-0.04），旋转 `±0.3-0.8°`（很少需要），平移 `±2-3px`（仅当隔离时推到 4-6px）。更大的空闲读作"仍在动画"而非"有生命但休息" — 并且观看者在高端连续观看 5+ 场景会将整个影片读作"闪烁。"
- **周期时长：长时空闲每呼吸 2.5-4 秒，否则 1.5-3 秒** — 2.5-3 秒是舒适的呼吸节奏；在长时空闲窗口下 1.5 秒感觉疯狂；在短时间中超过 4 秒感觉无生命。
- **长时空闲窗口（`IDLE_DUR > 6s` 或空闲比例 > 组合的 30%）：** 将 `SCALE_AMP` 和 `Y_AMP_PX` 减半，减慢 `CYCLES` 使每次呼吸为 3-4 秒。考虑门控振幅以在空闲最后 ~20% 淡出到零，使场景实际上**在过渡前稳定**，而非在半途中移交。这是当 finalize 快照显示"所有东西在结束时仍在移动"时最大的单一修复。
- **N 个元素上的并发空闲**（三联列、卡片网格、多统计行、并排面板）：每元素振幅 ≤ 默认值 `/ √N`。三列各在 `±6px` 视觉上累加到 `±18px+` 的竞争运动；三个在 `±2-3px` 读作一个集体呼吸。错开元素之间的**周期**（2.1s / 1.9s / 2.4s）以获得有机感 — 但**振幅**也必须更小，而不仅是周期。
- **不同元素处于不同相位** — 将次级元素偏移 `Math.PI / 2`（90° 偏移）使它们不同步移动。同步运动看起来机械；异相看起来生动。
- **组合，而非替换** — 空闲运动**添加**到元素的休息变换，而非替换它。如果进入稳定在 `translateY(0)`，空闲应产生 `translateY(0 + sin*4)`。不要覆盖进入的最终平移。
- **❗ 不要使用 CSS `@keyframes` 作为空闲循环** — CSS 动画在浏览器的渲染时钟上运行，独立于 HF 定位时钟。HF 逐帧定位，CSS 驱动的空闲会闪烁/不同步。在 GSAP 时间线内驱动空闲。

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **空闲不使用 CSS `animation`** — 必须是时间线驱动
- **如果空闲与同一元素上的其他补间组合，设置 `will-change: transform`**
- **相位补间 `ease: 'none'`** — 正弦本身提供缓动；非线性补间相位会产生非正弦运动
- **不要重新启动空闲补间** — 它是一个从组合空闲窗口开始到结束的单一长补间

## 组合

- 在 [press-release-spring.md](press-release-spring.md) 之后 — 按钮在释放稳定后空闲呼吸
- 在 [counting-dynamic-scale.md](counting-dynamic-scale.md) 之后 — 最终数字呼吸
- 在 [card-morph-anchor.md](card-morph-anchor.md) 之后 — 稳定后的卡片空闲摆动
- 在 [orbit-3d-entry.md](orbit-3d-entry.md) 之后 — 中心标签在项目轨道运行时空闲呼吸

## 与 HF 技能配对

- `/hyperframes-animation` — 写入变换的 `onUpdate`
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
