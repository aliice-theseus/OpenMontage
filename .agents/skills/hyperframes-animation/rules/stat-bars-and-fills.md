---
name: stat-bars-and-fills
description: 数据可视化原语，将数字与图形配对 — 增长条（CSS scaleY 错开）、进度填充（条或环）和部分星级评分擦拭。seek 安全、确定性。
metadata:
  tags: data, stats, chart, bars, progress, ring, stars, rating, infographic, number
---

# 统计条与填充

给统计数据在其数字旁边**视觉重量**的图形：一个小条形图、一个填充到百分比的进度条/环、或一个填充到分数评分的一行星。将这些与 [counting-dynamic-scale.md](counting-dynamic-scale.md)（数字）配对，形成完整的统计场景。

**布局蓝图 — 选择一个并在所有统计数据中保持一致：**

- **单焦点** — 一个居中画面，数字是主角，环或条在其下方/周围。对于顺序揭示（同一画面中统计 1 → 统计 2 → 统计 3）最干净。
- **分屏** — 左侧大数字，右侧配对图形。当统计一起显示或每个需要不同的视觉效果时更好。

不要在一个片段中混用蓝图 — 那会读作不一致。

## 1 — 增长条（CSS `scaleY` 错开）

条从基线错开生长；最后一个条是重音。

```css
.bars {
  display: flex;
  align-items: flex-end;
  gap: 14px;
  height: 280px;
}
.bar {
  width: 48px;
  background: #3a4a64;
  transform: scaleY(0);
  transform-origin: bottom center; /* 从基线向上生长，而非从中心 */
}
.bar:last-child {
  background: #ffc300;
} /* 重音最终/当前条 */
```

```js
// 高度在 CSS 中编写（例如每个条的内联高度）；GSAP 仅揭示 scaleY 0→1。
tl.to(".bar", { scaleY: 1, duration: 0.7, ease: "power3.out", stagger: 0.08 }, 0.3);
```

> 使用 `scaleY`（一个变换），永远不要动画化 `height` — 高度补间被运行时禁止。在 CSS 中设置每个条的最终高度，从 0 开始缩放。

## 2 — 进度填充

**条形形式** — 从左原点开始的 `scaleX`：

```css
.track {
  width: 520px;
  height: 16px;
  background: #1b263b;
  border-radius: 8px;
  overflow: hidden;
}
/* width:100% 是必需的 — 绝对定位的填充没有宽度就是 0px，并且 scaleX(0) 仍然是 0
   → 条渲染为不可见（且没有 lint/inspect 检查捕获零宽度缩放元素）。 */
.fill {
  width: 100%;
  height: 100%;
  background: #ffc300;
  transform: scaleX(0);
  transform-origin: left center;
}
```

```js
const PCT = 0.92; // 92%
tl.to(".fill", { scaleX: PCT, duration: 1.0, ease: "power2.out" }, 0.3);
```

**环形形式** — 测量的描画绘制（委托给 [svg-path-draw.md](svg-path-draw.md)）：

```js
const ring = document.querySelector("#ring");
const LEN = ring.getTotalLength(); // 测量，不要硬编码周长
ring.style.strokeDasharray = LEN;
ring.style.strokeDashoffset = LEN; // 空
// 在 CSS 中将 <circle> 旋转 -90°，使填充从 12 点钟方向开始
tl.to(ring, { strokeDashoffset: LEN * (1 - 0.92), duration: 1.1, ease: "power2.out" }, 0.3);
```

## 3 — 星级评分填充（分数）

一行金星从左到右揭示到分数值（例如 4.6/5），通过金色层上的剪辑擦拭，金色层位于灰色层之上。

```html
<div class="stars">
  <div class="stars-gray">★★★★★</div>
  <div class="stars-gold" id="goldStars">★★★★★</div>
</div>
```

```css
.stars {
  position: relative;
  font-size: 64px;
  letter-spacing: 8px;
}
.stars-gray {
  color: #2b3548;
}
.stars-gold {
  position: absolute;
  inset: 0;
  color: #ffc300;
  width: 100%;
  clip-path: inset(0 100% 0 0);
}
```

```js
const RATING = 4.6,
  MAX = 5;
tl.to(
  "#goldStars",
  { clipPath: `inset(0 ${100 - (RATING / MAX) * 100}% 0 0)`, duration: 1.0, ease: "power2.out" },
  0.3,
);
```

## 如何选择值

- **条数** — 4–6 读作"趋势"而不杂乱；最后一个条是当前/重音值。
- **填充时长** — 0.8–1.2 秒，与配对的计数递增匹配，使数字和图形一起着陆（共享缓动）。
- **重音色调** — 恰好一个；条/填充/星都使用相同重音，其余为柔和色。
- **错开** — 条上 0.06–0.1 秒；更大感觉迟缓，0 丢失构建感。

## 关键原则

- **仅使用变换** — `scaleY` / `scaleX` / `clipPath`，永不使用 `width`/`height` 补间（运行时禁止）。
- **匹配数字的时机** — 填充和计数递增应同时达到峰值（相同开始 + 缓动），使统计解析为一个节拍，而非两个。
- **测量，而非硬编码** — 通过 `getTotalLength()` 获取环长度；如果半径变化，硬编码的周长会失效。
- **一个重音色调，一致蓝图** — 参见 `hyperframes-creative/references/data-in-motion.md`。

## 关键约束

- **时间线暂停**；同步构建；注册键 = `data-composition-id`。
- **`onUpdate`（如果配对计数器）必须为 O(1)** — 运行时逐帧定位（参见 [counting-dynamic-scale.md](counting-dynamic-scale.md)）。
- **无 `height`/`width` 补间，无 `repeat: -1`** — 仅变换 + 有限重复。
- **`transform-origin`** 必须为 `bottom`（条向上生长）/ `left`（条/填充向右生长）— 默认中心原点从中间缩放，看起来不对。

## 组合

- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 图形旁边的数字（配对；相同缓动/时长）
- [svg-path-draw.md](svg-path-draw.md) — 进度环绘制机制

## 与 HF 技能配对

- `/hyperframes-animation` — 时间线 + 变换补间
- `/hyperframes-creative` — `references/data-in-motion.md`（统计布局 + 视觉重量）
- `/hyperframes-core` — 组合接线；无 `width`/`height` 补间规则
