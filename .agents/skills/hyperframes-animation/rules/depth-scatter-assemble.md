---
name: depth-scatter-assemble
description: N 个元素散开进入/重新组装自旋转的 3D 深度云，每个从确定性的索引派生的 3D 偏移开始并稳定到干净的平面布局。
metadata:
  tags: 3d, scatter, assemble, depth, cloud, tumble, kinetic, letter, fragment, logo, reassemble
---

# 深度散开 ↔ 组装

N 个元素（字形、卡片、图标、logo 碎片）从旋转的 3D 深度云飞入并锁定到清晰的屏幕布局 — 或反过来。每个元素从**确定性**的 3D 偏移开始（translateZ 深度 + rotateX/rotateY + 从其索引派生的 x/y 散开），然后补间到其组装的平面位置（`z: 0, rotation: 0`）。因为每个散开位置通过索引的三角函数计算 — 从不 `Math.random` — 每帧渲染相同。

与 `orbit-3d-entry`（翻转入场然后连续轨道）和 `center-outward-expansion`（从共享中心的平面 2D 爆发）不同：这里每个元素在 3D 云中有其**自己的**点，解析是平面组装布局，而非轨道或径向喷射。

## 工作原理

每个元素解析到平面布局位置（`targetX/Y`，在 CSS 中或通过 `data-*` 设置一次）。其**散开**状态从其索引 `i` 派生：

```js
const GOLDEN = Math.PI * (3 - Math.sqrt(5)); // ~2.39943 rad — 均匀角度分布，无聚集
const a = i * GOLDEN; // 此元素在云中的角度
const scatterX = Math.cos(a) * RADIUS; // 索引派生，确定性
const scatterY = Math.sin(a) * RADIUS;
const scatterZ = Z_NEAR - (i / (n - 1)) * (Z_NEAR - Z_FAR); // 跨云的步进深度
const rotX = Math.sin(a) * TUMBLE; // 翻滚方向，也来自角度
const rotY = Math.cos(a) * TUMBLE;
```

一个单一的 0→1 `progress` 代理将每个元素在散开和组装之间插值（每通道 lerp）。在 `progress = 0` 时元素形成深度云；在 `progress = 1` 时它们平面坐落在布局中。正向运行是**组装**；云本身缓慢旋转（一个舞台 `rotateY` 补间），使散开在锁定前具有生命力。

需要在舞台上设置 `perspective`，并在舞台**和**每个元素上设置 `transform-style: preserve-3d`，否则 z 深度和翻滚会平面化为 2D 缩放。

## HTML

```html
<div
  class="scene"
  id="assemble-scene"
  data-composition-id="assemble-scene"
  data-start="0"
  data-duration="4"
  data-track-index="0"
>
  <!-- 云旋转；布局生活在其中。targetX/Y = 每个
       元素距离舞台中心（px）的平面组装偏移。 -->
  <div class="cloud-stage">
    <div class="frag" data-target-x="-260" data-target-y="0">{glyph1}</div>
    <div class="frag" data-target-x="-130" data-target-y="0">{glyph2}</div>
    <div class="frag" data-target-x="0" data-target-y="0">{glyph3}</div>
    <div class="frag" data-target-x="130" data-target-y="0">{glyph4}</div>
    <div class="frag" data-target-x="260" data-target-y="0">{glyph5}</div>
  </div>
</div>
```

对于 logo 组合，`targetX/Y` 描述部件的休息布局；对于动感排版，每个字形一个 `.frag`（在设置时从短语字符串注入 span 使宽度精确 — 参见变体）。

## CSS

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: {bgColor};
  perspective: 1400px; /* 必需 — 没有它，z 深度 + 翻滚读作平面 2D 缩放 */
}
.cloud-stage {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  transform-style: preserve-3d; /* 必需 —  preserve child 3D context */
  will-change: transform;
}
.frag {
  position: absolute;
  /* 位于舞台中心；GSAP 将每个平移到其布局/云点。 */
  top: 50%;
  left: 50%;
  display: grid;
  place-items: center;
  font-family: {font};
  font-weight: 900;
  font-size: 120px;
  color: {textColor};
  transform-style: preserve-3d; /* 每个碎片保持其自己的 3D 上下文 */
  backface-visibility: hidden; /* 在翻滚中隐藏镜像面 */
  will-change: transform, opacity;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const frags = Array.from(document.querySelectorAll(".frag"));
  const n = frags.length;
  const GOLDEN = Math.PI * (3 - Math.sqrt(5)); // ~2.39943 — 均匀分布，无聚集

  // RADIUS、Z_NEAR、Z_FAR、TUMBLE、ASSEMBLE_DUR、ASSEMBLE_EASE、STAGGER、
  // CLOUD_SPIN_DEG、CLOUD_SPIN_DUR — 按"如何选择值"中的命名常量。

  // 从每个碎片的索引预计算其确定性的散开状态。
  const scatter = frags.map((el, i) => {
    const a = i * GOLDEN;
    const depthT = n > 1 ? i / (n - 1) : 0;
    return {
      x: Math.cos(a) * RADIUS,
      y: Math.sin(a) * RADIUS,
      z: Z_NEAR - depthT * (Z_NEAR - Z_FAR),
      rotationX: Math.sin(a) * TUMBLE,
      rotationY: Math.cos(a) * TUMBLE,
    };
  });

  // 1) 在任何补间触发前，将每个碎片放置在云中。
  frags.forEach((el, i) => {
    const s = scatter[i];
    gsap.set(el, {
      xPercent: -50,
      yPercent: -50, // 烘焙自居中，使 x/y 成为距舞台中心的偏移
      x: s.x,
      y: s.y,
      z: s.z,
      rotationX: s.rotationX,
      rotationY: s.rotationY,
      opacity: 0,
    });
  });

  // 2) 云旋转，使散开在组装前/期间有生命力。
  tl.to(
    ".cloud-stage",
    { rotationY: CLOUD_SPIN_DEG, duration: CLOUD_SPIN_DUR, ease: "power1.out" },
    0,
  );

  // 3) 组装 — 每个碎片从其云点补间到其平面目标。
  frags.forEach((el, i) => {
    tl.to(
      el,
      {
        x: Number(el.dataset.targetX),
        y: Number(el.dataset.targetY),
        z: 0,
        rotationX: 0,
        rotationY: 0,
        opacity: 1,
        duration: ASSEMBLE_DUR,
        ease: ASSEMBLE_EASE, // out 缓动 — 碎片飞入然后稳定
      },
      i * STAGGER, // 索引错开读作"云向内塌缩"
    );
  });

  window.__timelines["assemble-scene"] = tl;
</script>
```

## 变体

### 翻滚交换（两个短语之间的镜头中段交接）

`kinetic-type-beats` 节拍变化的标志性动作：一个短语的字形**进入**云中散开，同时下一个短语的字形从云中**出来**组装 — 两个状态之间的 3D 交接，从无空帧。两组字形共享云；用一个共享的 0→1 `progress` 驱动两者，使它们确定性交叉。

```js
// outgoing[] 和 incoming[] 是两个字形数组，每个有预计算的 scatter[]（见上）。
const swap = { p: 0 };
tl.to(
  swap,
  {
    p: 1,
    duration: SWAP_DUR,
    ease: "power2.inOut",
    onUpdate: () => {
      const p = swap.p;
      outgoing.forEach((el, i) => {
        // 1 → 0：布局 → 云（散开**离开**）
        const s = outScatter[i];
        const tx = Number(el.dataset.targetX);
        const ty = Number(el.dataset.targetY);
        el.style.opacity = String(1 - p);
        el.style.transform =
          `translate(-50%,-50%) translate3d(${tx + (s.x - tx) * p}px,${ty + (s.y - ty) * p}px,${s.z * p}px)` +
          ` rotateX(${s.rotationX * p}deg) rotateY(${s.rotationY * p}deg)`;
      });
      incoming.forEach((el, i) => {
        // 0 → 1：云 → 布局（组装**进入**）
        const s = inScatter[i];
        const tx = Number(el.dataset.targetX);
        const ty = Number(el.dataset.targetY);
        el.style.opacity = String(p);
        el.style.transform =
          `translate(-50%,-50%) translate3d(${s.x + (tx - s.x) * p}px,${s.y + (ty - s.y) * p}px,${s.z * (1 - p)}px)` +
          ` rotateX(${s.rotationX * (1 - p)}deg) rotateY(${s.rotationY * (1 - p)}deg)`;
      });
    },
  },
  SWAP_AT,
);
```

在设置时为每个短语注入逐字形 span 集（使每个字形的 `targetX` 是精确的布局前进宽度 — 在 `document.fonts.ready` 后测量），并将每组的不透明度隐藏到 0 直到其窗口。

### 径向字母爆炸 → 解析

平面特例（`kinetic-type-beats` "字母径向爆炸然后解析"缺口）：设置 `Z_NEAR = Z_FAR = 0` 和 `TUMBLE` 小，使云成为 2D 环，然后反转组装用于爆炸 — 碎片飞出到 `scatter[i]` 然后快照回布局。纯平面内，无深度。

### 散开退出（仅最终帧退出）

仅作为组合的最后一个节拍反转组装（布局 → 云，不透明度 1→0）。镜头中段的散开退出读作退出并破坏镜头 — 保持入场和交接为组装或翻滚交换。

### 视差深度滑入（logo 组合）

对于 `logo-assemble-lockup`，给后层更大的 `|Z_FAR|` 和更长的 `ASSEMBLE_DUR`，前景部分更浅的深度和更短的时长 — 不同深度的部分以不同的表观速度滑入（视差）并锁定到组合中。

## 如何选择值

- **n（元素数量）** — 云中的碎片/字形
  - 范围：4–14（字形集跟随词长；对于碎片/卡片保持 4–9）
  - 效果：少读作有意的组装；多读作密集蜂群凝聚
  - 约束：超过 ~14 云拥挤中心，个别路径停止可读
- **RADIUS** — 云在 x/y 平面中的扩散（px）
  - 范围：250–700 px
  - 效果：小 = 几乎不分离的紧结；大 = 碎片从画面边缘到达
  - 约束：保持最远散开在所选 `perspective` 的画面内，否则碎片从屏幕外弹出，无行进可读
- **Z_NEAR / Z_FAR** — 云的深度带（px），前/后
  - 范围：Z_NEAR +150 到 +450；Z_FAR −150 到 −500
  - 效果：宽带（例如 +400 / −400）给出强烈的朝摄像机飞/远离摄像机深度；窄带保持几乎平坦
  - 约束：非常大的 `|z|` 配合短 `perspective` 会过度扭曲（碎片先巨大然后微小）— 加宽 `perspective` 以匹配
- **TUMBLE** — 散开碎片的峰值 rotateX/rotateY（度）
  - 范围：40–110°
  - 效果：低 = 碎片几乎直立漂入；高 = 它们在空中翻滚并在到达时旋转直立
  - 约束：使用 `backface-visibility: hidden`，超过 90° 的字形在补间中间显示空白（翻滚意图如此）；对于单面有内容的卡片，上限约为 80°
- **ASSEMBLE_DUR** — 每碎片云 → 布局补间（秒）
  - 范围：0.7–1.4 秒
  - 效果：短 = 干脆锁定；长 = 浮动凝聚
  - 约束：`(n − 1) × STAGGER + ASSEMBLE_DUR` 必须适应场景的组装窗口
- **ASSEMBLE_EASE** — 跨碎片的共享缓动
  - 离散选择：`power3.out`、`expo.out`、`back.out(1.4)`
  - 选择：`power3.out` 默认（飞入，稳定）。`expo.out` 在末端快照硬着陆。`back.out` 添加座位时的微小过冲。避免 `in` 缓动 — 碎片看起来像被吸入云中
- **STAGGER** — 连续碎片组装开始之间的间隔（秒）
  - 范围：0.03–0.09 秒
  - 效果：< 0.03 = 单一和弦（整个云同时塌缩）；> 0.09 = 缓慢滴答，失去"蜂群"读感
  - 约束：`n × STAGGER` 应保持在 `ASSEMBLE_DUR` 以下，使云作为一个运动塌缩，而非队列
- **CLOUD_SPIN_DEG / CLOUD_SPIN_DUR** — 组装期间舞台 rotateY（度/秒）
  - 范围：15–60°，时长 ≥ `ASSEMBLE_DUR`
  - 效果：轻柔旋转给散开生命力，使其不读作冻结的爆炸图；太快与组装竞争
  - 约束：保持有限并在稳定时结束 — 无 `repeat`
- **SWAP_DUR / SWAP_AT**（翻滚交换）— 交接长度/触发时间（秒）
  - 范围：SWAP_DUR 0.5–1.0 秒；SWAP_AT 在节拍边界上
  - 效果：更短 = 硬交叉；更长 = 可见的穿云溶解
  - 约束：传入和传出**必须**共享一个 `progress`（一个补间），使它们在相同瞬间交叉

## 关键原则

- **场景根上的 `perspective` + 舞台**和**每个碎片上的 `preserve-3d`** — 没有全部三个，z 深度和翻滚塌缩为平面缩放
- **每个散开值都是索引派生的** — `cos/sin(i × GOLDEN)`，按 `i/(n−1)` 步进的 `z`。黄金角度均匀分布点，无聚集，且（关键）**无 `Math.random`**，因此云每次渲染 bit 相同
- **在添加补间**之前 **`gsap.set` 云** — 先将每个碎片以 `opacity: 0` 停在其散开点；组装补间从那里开始。跳过设置会使第 0 帧显示组装好的布局，然后在第一个补间开始时传送
- **解析为平面** — 稳定状态是布局中的 `z: 0, rotationX: 0, rotationY: 0`。解析后仍倾斜的云读作未完成
- **仅组装/交接；散开退出是退出** — 碎片在镜头中段离开进入云读作镜头结束。使用正向组装用于入场，翻滚交换用于节拍变化；保留散开退出给最终帧
- **深度排序是自动的** — 在 `preserve-3d` 内，绘制顺序遵循实际 Z，因此较近的碎片正确地遮挡较远的碎片，无需手动 z-index（与轨道情况不同，那里在 2D 中伪造轨道，需要上限 z-index）

## 关键约束

- **无 `Math.random` / `Date.now`** — 从索引派生每个散开坐标（黄金角三角函数 + 步进深度）。这是本规则的全部要点：随机化的云每帧渲染不同，定位会破坏
- **无 CSS `transition`** — 所有运动都是暂停时间线上的 GSAP 补间
- **无 `repeat` / `yoyo` / 无限** — 云旋转和每次组装都是有限的、一次性的补间，在稳定前结束
- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **仅使用变换别名** — `x`、`y`、`z`、`scale`、`rotation`/`rotationX`/`rotationY`。永远不要 `width`/`height`/`left`/`top`；`x`/`y` 与 `xPercent/yPercent -50` 自居中组合
- **舞台 + 碎片上设置 `will-change: transform`** — 许多同时的 3D 变换受益于合成器提示
- **在翻滚交换中，两组字形使用一个共享 `progress`** — 两个独立的补间可以在定位下相位漂移，交叉看起来不再像一个交接

## 组合

- [orbit-3d-entry.md](orbit-3d-entry.md) — 替代 3D 入场（稳定到连续轨道而非平面组合）；共享 `perspective` + `preserve-3d` 舞台设置
- [hacker-flip-3d.md](hacker-flip-3d.md) — 碎片就座时的逐字形 3D 翻转/解码；分层实现"字母翻滚进入并在到达时解码"效果
- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 一旦锁定，给组装的 wordmark 堆叠挤压效果
- [center-outward-expansion.md](center-outward-expansion.md) — 平面 2D 表亲（单个共享中心，无深度），当不需要透视时
- [press-release-spring.md](press-release-spring.md) — 云解析后组装组合上的弹簧稳定
- [sine-wave-loop.md](sine-wave-loop.md) — 在解析布局上空闲呼吸，而非冻结保持

## 与 HF 技能配对

- `/hyperframes-animation` — 时间线 + `onUpdate` API（共享进度的翻滚交换）
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
