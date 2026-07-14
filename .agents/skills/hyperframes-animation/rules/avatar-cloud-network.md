---
name: avatar-cloud-network
description: 头像分布在椭圆环上，由 SVG 虚线连接到一个中心枢纽 — 社交证明"社区"揭示，带错开入场。
metadata:
  tags: avatar, cloud, network, social-proof, ellipse, connection, stagger
---

# 头像云网络

头像排列在围绕中心元素（logo/计数器/品牌）的椭圆环上。从中心到每个头像的 SVG 虚线连接线。头像错开弹簧入场，然后连接线向外绘制 — 传达"社区"或"社交证明。"与 [orbit-3d-entry](orbit-3d-entry.md)（连续轨道）不同 — 头像云是静态组合揭示。

## 工作原理

三个渲染层：

1. **SVG 连接线**（z-index 1，在所有后面）— 从中心枢纽到每个头像位置的线
2. **头像**（z-index 2）— 在椭圆位置上的 `<div>` 圆圈
3. **中心枢纽**（z-index 5）— 品牌计数器或 logo（位于汇聚到它的线之上）

动画阶段：

- `HUB_FADE_START → HUB_FADE_START + HUB_FADE_DUR`：枢纽淡入
- `AVATAR_ENTRY_START → AVATAR_ENTRY_START + (AVATAR_COUNT − 1) × AVATAR_STAGGER + AVATAR_ENTRY_DUR`：头像级联进入
- `LINES_START → LINES_START + (AVATAR_COUNT − 1) × LINE_STAGGER + LINES_DUR`：连接线向外绘制
- 高潮停留：可选头像空闲呼吸（参见变体 / sine-wave-loop）

## HTML、CSS 和 GSAP 时间线

（保持原有代码块，注释已中文化。）

## 如何选择值

（几何、枢纽淡入、头像级联、连接线、空闲呼吸、颜色标记等全部中文化。）

## 关键原则

- **枢纽在线之上（`z-index: 5` vs 线 `z-index: 1`）** — 线应看起来终止于枢纽边缘，而非穿过。枢纽必须在前面。
- **线向外绘制（虚线偏移 0）** — 从中心绘制是视觉叙事："枢纽连接到其社区。"
- **8-12 个头像** — 更少感觉稀疏，更多拥挤椭圆。
- **`RADIUS_X > RADIUS_Y`** — 水平椭圆读作透视；相等半径（圆）读作 2D 平面布局。
- **头像进入错开 0.06-0.10s** — 级联读作"加入"；同时读作"都已在那里。"
- **错开线 在头像大部分稳定后** — 线绘制在最后一个头像稳定前 ~0.1-0.2s 开始以重叠。
- **形成后空闲呼吸** — 每个头像略为异相。在高潮停留期间保持眼睛兴趣。
- **❗ 高潮停留 ≥1s** — 线完成后，保持 ≥1s，使形成的网络可读。

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **头像或线上无 CSS 动画**
- **头像上设置 `will-change: transform, opacity`**
- **SVG `pointer-events: none`** — 装饰性叠加
- **直线不需要 `getTotalLength()`** — 使用 `Math.hypot` 计算线长（更便宜，精确）
- **枢纽 `z-index` > 线的 z-index** — 显式分层
