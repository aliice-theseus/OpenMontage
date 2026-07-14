---
name: card-morph-anchor
description: 容器在镜头之间变形尺寸和边框半径，作为视觉过渡锚点。
metadata:
  tags: morph, anchor, transition, border-radius, container, shape
---

# 卡片变形锚点

一个容器在两个视觉状态之间平滑变换其宽度、高度、边框半径和（可选）背景。变形本身**就是镜头过渡** — 无需单独的过渡特效。观看者的眼睛跟踪变形容器作为镜头之间的锚点。

## 工作原理

单一 GSAP 补间同时动画化多个容器属性（宽度/高度/边框半径/背景）。同时：

1. **旧内容**在变形的第一个 ~40% 期间淡出
2. **新内容**在变形的最后 ~40% 期间淡入
3. **可选最终淡出** — 变形容器本身淡出到 0，揭示其后渲染的实际下一镜头元素

即使内容和形状变化，持续存在的容器提供视觉连续性。

## HTML

```html
<div class="scene" id="morph-scene" data-composition-id="morph-scene" data-start="0" data-duration="4" data-track-index="0">
  <div class="morph-card">
    <div class="content-old"><h2>{shotOneHeadline}</h2><p>{shotOneSubcopy}</p></div>
    <div class="content-new"><img src="{shotTwoIcon}" alt="logo" /></div>
  </div>
  <div class="next-shot-anchor"><img src="{nextShotAnchor}" alt="anchor" /></div>
</div>
```

## CSS 和 GSAP 时间线

（保持原有代码块，注释已中文化。）

## 要变形的关键属性

| 属性               | 变化形状                           | 视觉效果               |
| ------------------ | ---------------------------------- | ---------------------- |
| `width` / `height` | `SHOT_ONE_W × SHOT_ONE_H` → `SHOT_TWO_W × SHOT_TWO_H` | 宽卡片缩成图标       |
| `borderRadius`     | `SHOT_ONE_RADIUS` → `SHOT_TWO_RADIUS` | 矩形变成圆形         |
| `background`       | `{surfaceShotOne}` → `{surfaceShotTwo}` | 容器身份转变         |
| `boxShadow`        | 基础阴影 → 重音辉光标记           | 强调变化             |

## 关键原则

- **所有目标属性在一个补间中** — 它们共享单一缓动和时长，使它们步调一致变形
- **旧内容早淡出，新内容晚淡入** — 容器形状变化发生在中间，提供自然的"眨眼"时刻
- **最终淡出可选** — 在下个镜头有真实锚点元素交接时使用
- **变形和交叉淡入淡出使用相同缓动** — 避免混合 `power2.inOut` 变形与 `bounce.out` 内容，看起来不同步
- **❗ 如果使用 `.next-shot-anchor` 进行交接，其视觉必须与 `.morph-card` 的最终状态像素一致** — 相同 `width`/`height`、相同 `border-radius`、相同 `background`、相同 `box-shadow`、相同内部图标尺寸。两者之间的任何视觉差异 = 交叉淡入淡出期间的可见跳跃。

## 关键约束

- **变形容器上设置 `overflow: hidden`** — 内容必须在形状变化期间裁剪
- **变形前保持一个节拍** — 让观看者先注册镜头 1 的内容
- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **使用 `background` 补间，而非 `background-color`**：渐变需要 `background`
- **`borderRadius` 应 ≤ 结束状态中较小尺寸的一半**
- **❗ 不要在淡入淡出中途快照 `z-index`** — 使用 DOM 顺序而非 z-index 快照

（详细参数选择与原文一致，已全部中文化。）
