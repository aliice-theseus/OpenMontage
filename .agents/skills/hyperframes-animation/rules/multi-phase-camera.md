---
name: multi-phase-camera
description: 顺序摄像机缩放，带 2-3 个不同阶段（拉回/聚焦/推进）加连续微漂移，营造有机电影感。
metadata:
  tags: camera, zoom, phase, drift, scale, cinematic
---

# 多阶段摄像机

一个围绕整个场景的摄像机包裹容器，在脚本化触发时间推进通过离散的缩放阶段。连续的、正弦驱动的微漂移叠加，使摄像机在阶段之间从不会感觉静态。与单一线性缩放不同 — 多阶段创造"电影节奏"（预期 → 揭示 → 稳定）。

## 工作原理

摄像机是一个单一的包裹 `<div>`，其 `transform: scale() translate(x, y)` 由以下驱动：

1. **阶段缩放** — 一个分步缩放值，在触发时间通过阶段推进（例如 `t=0` 时 `PHASE_1_SCALE` → `PHASE_2_AT` 时 `PHASE_2_SCALE` → `PHASE_3_AT` 时 `PHASE_3_SCALE`）
2. **漂移偏移** — 一个连续的、基于正弦的 `translateX` / `translateY`（小振幅、慢频率）**添加**到阶段变换

两者都在 GSAP 时间线内运行，使 HF 确定性逐帧定位。

## HTML

```html
<div
  class="scene"
  data-composition-id="cam-scene"
  data-start="0"
  data-duration="6"
  data-track-index="0"
>
  <div class="camera" id="camera">
    <div class="content">
      <div class="hero">{Brand}</div>
      <div class="tagline">{tagline}</div>
      <div class="cta">{ctaText}</div>
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
  overflow: hidden;
  background: {sceneBgColor};
}
.camera {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  transform-origin: 50% 50%;
  will-change: transform;
}
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  text-align: center;
}
.hero {
  font-family: {font};
  font-weight: 900;
  font-size: {heroSize};
  letter-spacing: 8px;
  color: {textColor};
  text-transform: uppercase;
}
.tagline {
  font-family: {font};
  font-weight: 600;
  font-size: {taglineSize};
  color: {accentColor};
}
.cta {
  font-family: {monoFont};
  font-weight: 700;
  font-size: {ctaSize};
  letter-spacing: 6px;
  color: {accentColor};
  text-transform: uppercase;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const camera = document.getElementById("camera");

  // 三阶段缩放计划：拉回 → 聚焦 → 推进
  const phase = { scale: PHASE_1_SCALE };

  // 阶段 1 — 以拉远开始
  //（初始值不需要补间；通过 phase 对象设置）

  // 阶段 2 — 稳定到中性聚焦
  tl.to(
    phase,
    {
      scale: PHASE_2_SCALE,
      duration: PHASE_2_DUR,
      ease: PHASE_2_EASE,
    },
    PHASE_2_AT,
  );

  // 阶段 3 — 为高潮缓慢推进
  tl.to(
    phase,
    {
      scale: PHASE_3_SCALE,
      duration: PHASE_3_DUR,
      ease: PHASE_3_EASE,
    },
    PHASE_3_AT,
  );

  // 漂移驱动器 — 叠加在阶段缩放上的连续正弦运动
  const drift = { p: 0 };

  tl.to(
    drift,
    {
      p: Math.PI * 2 * DRIFT_CYCLES,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        const dx = Math.sin(drift.p) * DRIFT_AMP_X;
        const dy = Math.sin(drift.p * DRIFT_FREQ_RATIO) * DRIFT_AMP_Y;
        camera.style.transform = `scale(${phase.scale}) translate(${dx}px, ${dy}px)`;
      },
    },
    0,
  );

  // 内容揭示（摄像机画面内的入场节拍）
  tl.from(".hero", { opacity: 0, y: 32, scale: 0.96, duration: 0.9, ease: "power3.out" }, HERO_AT);
  tl.from(".tagline", { opacity: 0, y: 16, duration: 0.7, ease: "power3.out" }, TAGLINE_AT);
  tl.from(".cta", { opacity: 0, y: 8, duration: 0.7, ease: "power3.out" }, CTA_AT);

  window.__timelines["cam-scene"] = tl;
</script>
```

## 如何选择值

- **PHASE_1_SCALE / PHASE_2_SCALE / PHASE_3_SCALE** — 三步缩放值
  - 范围：PHASE_1 0.88–0.96；PHASE_2 0.98–1.02；PHASE_3 1.04–1.15
  - 效果：更紧的分布 = 更微妙的摄像机；更宽 = 更电影感
  - 约束：在 PHASE_1_SCALE < 1 时，`.scene` **必须**有 `overflow: hidden`，否则内部内容的边缘会漏出画面
- **PHASE_2_AT / PHASE_2_DUR** — 聚焦阶段开始时间及其时长
  - 范围：PHASE_2_AT 0.3–1.0 秒；PHASE_2_DUR 1.0–1.8 秒
  - 效果：更长的 DUR = 更慢的稳定，更电影感
- **PHASE_3_AT / PHASE_3_DUR** — 推进阶段开始时间及其时长
  - 范围：PHASE_3_AT 2.0–4.0 秒；PHASE_3_DUR 1.0–2.0 秒
  - 约束：PHASE_3_AT 必须 ≥ PHASE_2_AT + PHASE_2_DUR（否则聚焦被抢占）
- **PHASE_2_EASE / PHASE_3_EASE** — 每次过渡的缓动
  - 离散选择：`power2.out`、`power3.out`、`power2.inOut`
  - 选择：电影感；摄像机上的弹簧/回弹缓动感觉不舒服。每个后续阶段应比前一个暗示更多稳定（更长时长或更多的出缓动）
- **TOTAL_DURATION** — 组合的总运行时间（匹配 `data-duration`）
  - 参考：漂移补间必须跨越整个组合
- **DRIFT_CYCLES** — 在 TOTAL_DURATION 内的正弦周期数
  - 范围：1–3
  - 效果：1 = 一次缓慢呼吸；3 = 明显更忙
  - 约束：高值读作机械晃动而非有机漂移
- **DRIFT_AMP_X / DRIFT_AMP_Y** — 峰值漂移偏移（px）
  - 范围：DRIFT_AMP_X 2–8 px；DRIFT_AMP_Y 1–4 px
  - 效果：每帧不可察觉，随时间可见。如果漂移是离散晃动，那就太多了
- **DRIFT_FREQ_RATIO** — Y 轴正弦频率的乘数
  - 范围：1.2–1.5
  - 效果：1.0 = 完美对角线（读作机械）；~1.3 = 有机 Lissajous
- **HERO_AT / TAGLINE_AT / CTA_AT** — 内容揭示节拍
  - 约束：HERO_AT 应在 PHASE_1 通过 PHASE_2 稳定**后**着陆（否则主角感觉像在摄像机仍在拉回时飞走）

## 阶段模式

| 模式               | 缩放序列（阶段 1 → 2 → 3） | 感受                           | 何时使用                   |
| ------------------ | ------------------------- | ------------------------------ | -------------------------- |
| **聚焦进入**       | 拉回 → 中性 → 轻微推进    | 接近 → 稳定 → 轻微推进         | 默认产品揭示               |
| **戏剧性揭示**     | 推进 → 中性 → 拉回        | 宽 → 聚焦 → 稳定拉回           | 带呼吸空间的主角镜头       |
| **稳定推进**       | 中性 → 轻微推进 → 更多推进 | 渐进的向前动量                 | 连续叙事推进               |
| **书挡拉出**       | 中性 → 强推进 → 中性      | 稳定 → 推进 → 释放             | CTA 强调然后释放           |

## 变体

### 按内容节拍（而非时间）触发阶段

如果组合有关节拍（例如一个入场完成，然后轨道开始），将摄像机补间开始时间与内容补间结束时间对齐，而非使用固定的时钟值。

### 摄像机抖动（恐慌/冲击）

对于短暂抖动而非漂移，用一个短窗口内更高振幅、更高频率的补间替换漂移补间：

```js
tl.to(
  drift,
  {
    p: Math.PI * 2 * SHAKE_CYCLES,
    duration: SHAKE_DUR,
    ease: "none",
    onUpdate: () => {
      const dx = Math.sin(drift.p) * SHAKE_AMP_X;
      const dy = Math.sin(drift.p * SHAKE_FREQ_RATIO) * SHAKE_AMP_Y;
      camera.style.transform = `scale(${phase.scale}) translate(${dx}px, ${dy}px)`;
    },
  },
  SHAKE_AT,
);
```

### 针对偏离中心元素的目标缩放

如果高潮应放大到一个非中心元素，将缩放与反向平移组合。计算偏移，使目标在缩放后落在视口中心：

```js
const target = document.querySelector(".cta");
const tRect = target.getBoundingClientRect();
const viewportCenter = { x: STAGE_W / 2, y: STAGE_H / 2 };
const offsetX = (viewportCenter.x - (tRect.left + tRect.width / 2)) / phase.scale;
const offsetY = (viewportCenter.y - (tRect.top + tRect.height / 2)) / phase.scale;
// 然后在 onUpdate 中：translate(offsetX + dx, offsetY + dy)
```

## 关键原则

- **漂移每帧不可察觉，随时间可见** — 如果漂移读作离散晃动，振幅太高
- **漂移 X 和 Y 使用略有不同的频率** — `DRIFT_FREQ_RATIO ≈ 1.3` 防止完美对角线运动，那读作机械
- **阶段弹簧比 UI 弹簧更柔和** — `power2.inOut` 或 `power3.out` 用于电影感；摄像机上的弹簧/回弹缓动感觉不舒服
- **每个后续阶段稳定"更深"** — 阶段 2 缓动应比阶段 1 暗示更多稳定（更长时长或更多的出缓动）。唤醒 → 稳定 → 稳定更深
- **摄像机包裹场景中的**所有**内容** — 逐元素应用摄像机会产生视差错误并破坏"这是一个视点"
- **❗ 场景上设置 `overflow: hidden`** — 拉回阶段（`scale < 1`）揭示内部内容的边缘。没有 `overflow: hidden`，这些边缘会漏出舞台画面，HF 将其渲染为可见内容
- **❗ 主角揭示在初始拉回缓动着陆后开始** — 如果标题淡入时摄像机仍在拉回，标题感觉像在飞走

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **`.camera` 上无 CSS `transition`** — 与 GSAP 变换竞争
- **摄像机上的 `transform-origin: 50% 50%`** — 偏离中心的原点创建不可预测的阶段间漂移
- **`.camera` 上设置 `will-change: transform`** — 摄像机变换每帧更新
- **`.scene` 上设置 `overflow: hidden`** — 当任何阶段缩放 < 1 时必需
- **场景背景在 `.scene` 上，不在 `.camera` 上** — 如果背景在摄像机上，缩放/平移它会揭示外部的虚空

## 组合

- [orbit-3d-entry.md](orbit-3d-entry.md) — 缓慢漂移摄像机内的轨道运动
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 与计数器峰值同步的高潮阶段推进
- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 带电影级摄像机移动的深度堆叠主角
- [sine-wave-loop.md](sine-wave-loop.md) — 摄像机内元素空闲（复合运动）

## 与 HF 技能配对

- `/hyperframes-animation` — 多阶段补间 + 漂移 onUpdate
- `/hyperframes-core` — 组合接线，场景包裹
- `/hyperframes-cli` — `hyperframes lint`
