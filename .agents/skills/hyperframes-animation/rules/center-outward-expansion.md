---
name: center-outward-expansion
description: 元素从屏幕中心聚集并向外扩展到最终位置，由共享进度值驱动。
metadata:
  tags: expansion, scatter, center, reveal, layout, sync, burst
---

# 中心向外扩展

元素从共享中心点开始并向其最终位置辐射。扩展本身可以是入场节拍，或由另一个动画的进度驱动（例如增长的数字）以实现协调运动。

## 工作原理

每个元素有 `targetX/Y`（其最终布局位置）和共享的 `centerX/Y`。一个 `progress` 值（0→1）将每个元素在中心和目标之间插值：

```js
const x = centerX + (targetX - centerX) * progress;
const y = centerY + (targetY - centerY) * progress;
```

当 `progress = 0` 时所有元素在中心重叠；当 `progress = 1` 时它们位于最终位置。

## HTML

```html
<div
  class="scene"
  data-composition-id="burst-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="burst-wrap">
    <div class="burst-item" data-target-x="-360" data-target-y="-180">{itemA}</div>
    <div class="burst-item" data-target-x="360" data-target-y="-180">{itemB}</div>
    <div class="burst-item" data-target-x="-360" data-target-y="180">{itemC}</div>
    <div class="burst-item" data-target-x="360" data-target-y="180">{itemD}</div>
    <div class="burst-item" data-target-x="0" data-target-y="-360">{itemE}</div>
    <div class="burst-item" data-target-x="0" data-target-y="360">{itemF}</div>
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
.burst-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
}
.burst-item {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: {itemSize};
  height: {itemSize};
  display: grid;
  place-items: center;
  background: {itemBgColor};
  border-radius: 28px;
  font-family: {font};
  font-weight: 900;
  font-size: 96px;
  color: {textColor};
  will-change: transform;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const items = document.querySelectorAll(".burst-item");

  items.forEach((el, i) => {
    const targetX = Number(el.dataset.targetX);
    const targetY = Number(el.dataset.targetY);
    tl.fromTo(
      el,
      { xPercent: -50, yPercent: -50, x: 0, y: 0, scale: 0.6, opacity: 0 },
      {
        x: targetX, y: targetY,
        scale: 1, opacity: 1,
        duration: EXPAND_DUR,
        ease: EXPAND_EASE,
      },
      i * STAGGER + ENTRY_AT,
    );
  });

  window.__timelines["burst-scene"] = tl;
</script>
```

## 如何选择值

- **ITEM_COUNT** — 爆发中的元素数量
  - 范围：3–8
  - 效果：3 = 稀疏；8 = 繁忙。> 8 导致卡片在扩展中途重叠的视觉混乱
- **EXPAND_DUR** — 每项从中心到目标补间的时长
  - 范围：1.0–1.8 秒
  - 效果：更短 = 干脆爆发；更长 = 向外浮动
- **EXPAND_EASE** — 跨所有项目的共享缓动
  - 离散选择：`power2.out`、`power3.out`、`expo.out`
  - 选择：`power3.out` 是默认 — 甩出然后稳定。`power2.out` 更温和。`expo.out` 使它们戏剧性停止。避免 `in` 缓动（它们读作项目在空中被吸回）。
- **STAGGER** — 连续项目开始时间之间的间隔
  - 范围：0.04–0.08 秒
  - 效果：< 0.04 = 同时和弦；> 0.08 感觉懒散/琶音
- **ENTRY_AT** — 应用于整个爆发开始的偏移
  - 范围：0 – 0.5 秒
  - 效果：> 0 在爆发前给一个构图的安静节拍

## 变体

### 同步扩展（由计数器驱动）

如果爆发应镜像计数动画的进度，两者共享相同的时长和缓动（和弦）。

### 部分展开开始

为避免初始集中混乱（6+ 元素堆叠在中心），从 `START_PROGRESS` 开始。

### 最终位置的空闲微浮动

与 `sine-wave-loop` 配对，使扩展着陆后元素保持活跃而非冻结。

## 关键原则

- **驱动器 vs 被驱动** — 如果爆发独立存在，使用逐项错开；如果它跟随另一个动画（计数器、音频节拍），共享相同的缓进进度，使它们读作一个节拍
- **错开在 0.04-0.08 秒范围内** — 太紧则集群从不视觉分离，太松则爆发感觉懒散
- **扩展使用出缓动** — 出缓动使项目"甩"出然后稳定。入缓动看起来像在空中被吸回
- **元素数量：3-8** — 更少感觉空旷，更多导致中心处视觉混乱
- **❗ 不要在爆发下方放置标签作为"真实标题"** — 如果你这样做，眼睛会跳到标签并忽略爆发。爆发**就是**节拍。如果需要标签，使用大写块并在爆发后揭示。

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **使用 translate，而非 left/top** — 平移与居中 `translate(-50%, -50%)` 技巧干净组合；变更 `left`/`top` 与居中冲突并导致像素抖动
- **爆发项目上设置 `will-change: transform`**
- **`burst-wrap` 内除了项目自身外无 `position: absolute` 父级** — 兄弟绝对元素会偷走居中基线

## 组合

- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 计数器峰值驱动爆发峰值（和弦）
- [sine-wave-loop.md](sine-wave-loop.md) — 爆发着陆后的空闲运动
- [card-morph-anchor.md](card-morph-anchor.md) — 从变形卡片中爆发
