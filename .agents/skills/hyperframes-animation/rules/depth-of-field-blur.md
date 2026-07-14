---
name: depth-of-field-blur
description: 选择性聚焦/焦距拉动 — 通过 GSAP 补间滤镜模糊（+ 微小不透明度变暗）在脱焦层上拉取视线到聚焦元素，同时聚焦层保持清晰。通过 `--dof` CSS 变量驱动模糊；有限补间，无 CSS 过渡，确定性。覆盖单次焦距拉动、两个深度平面之间的焦距拉动、以及推进时模糊集群。
metadata:
  tags: blur, focus, depth-of-field, dof, rack-focus, filter, dim, spotlight, cinematic, push-in
---

# 景深模糊（选择性聚焦/焦距拉动）

通过**模糊**（和轻微**变暗**）聚焦元素周围的一切，同时聚焦层保持清晰，将视线拉到聚焦元素上 — 摄像机的景深在背景上衰减，或焦距拉动切换聚焦平面。运动是 `filter: blur(Npx)` 加上小的 `opacity` 变暗，在焦距移动窗口内从清晰（0）到模糊补间 — 两者都是 seek 安全的，因为 `filter` 和 `opacity` 是仅绘制的属性，HF 能正确逐帧插值。

这是蓝图不断要求的焦点衰减节拍的支持规则：推进期间的外部节点模糊（`constellation-hub`）、跨视差卡片堆栈的焦距拉动（`cursor-ui-demo`）、以及变暗 + 模糊非高亮卡片以聚光灯主角度量（`dataviz-countup`）。它们每个都为移动的景深一半标记"无支持规则" — 这就是它。

## 工作原理

每个层携带一个 `--dof` 自定义属性（px 模糊），由 `filter: blur(var(--dof))` 读取，加上自己的 `opacity`。单个 GSAP 补间在焦距移动窗口内将每个层的 `--dof` 从 `0` 推进到其目标模糊，并将其不透明度从 `1` 推进到变暗级别。聚焦层的补间目标是 `--dof: 0`（保持清晰）；脱焦层的目标为正值模糊。

三种机制，相同原语：

1. **焦距拉动** — 一个窗口：脱焦层从清晰（0）→ 模糊，同时聚焦层保持在 0。眼睛被拉到唯一仍然清晰的东西上。
2. **焦距切换** — 相同属性上的两个相邻窗口：焦点离开平面 A（其模糊斜率 0 → 最大）在相同位置平面 B 的模糊斜率最大 → 0。状态连续性如 `press-release-spring` 中一样重要：切换后 A 的休息模糊必须是 B 之前保持的值，因此将两者编写为相同 `--dof` 上的相邻补间是使交接无缝的关键。
3. **推进时模糊集群** — 景深补间与摄像机推进（`multi-phase-camera` / `coordinate-target-zoom`）并发运行：周围集群在摄像机朝聚焦核心缩放的**相同**时间线位置模糊 + 变暗，使"世界后退"和"我们推进"读作一个动作。

因为模糊是补间目标（而非 CSS `transition`），渲染器可以在任何帧着陆 — 且因为每个层的目标从索引/数据属性派生（从不 `Math.random`），衰减在每次 seek 时相同。

## HTML

```html
<div
  class="scene"
  id="dof-scene"
  data-composition-id="dof-scene"
  data-start="0"
  data-duration="DURATION"
  data-track-index="0"
>
  <div class="world" id="world">
    <!-- 聚焦层 — 保持清晰 -->
    <div class="layer focal" id="focal" data-dof="0">{FocalLabel}</div>

    <!-- 脱焦层 — 模糊 + 变暗。data-depth 按近→远排序
         使衰减可以按深度缩放模糊（参见变体）。 -->
    <div class="layer ctx" data-depth="1">{Context A}</div>
    <div class="layer ctx" data-depth="2">{Context B}</div>
    <div class="layer ctx" data-depth="3">{Context C}</div>
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
.world {
  /* 单一包裹容器，使并发摄像机推进（multi-phase-camera）
     一起变换所有内容；景深独立于摄像机。 */
  position: relative;
  width: 100%;
  height: 100%;
  transform-origin: 50% 50%;
}
.layer {
  /* --dof 是模糊的 px 值；filter 读取它。开始时清晰。 */
  --dof: 0px;
  filter: blur(var(--dof));
  /* will-change: filter — 提升图层，使模糊每帧重新栅格化成本低。
     参见关键原则中的性能说明。 */
  will-change: filter;
  font-family: {font};
  font-weight: 900;
  color: {textColor};
}
.focal {
  /* 位于上下文层之上，从不模糊。 */
  z-index: 2;
  font-size: FOCAL_FONT_SIZE;
}
.ctx {
  /* 脱焦平面。较小/分组使模糊半径保持适度但仍可读 —
     模糊小层成本低。 */
  z-index: 1;
  font-size: CTX_FONT_SIZE;
  opacity: 1;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const ctx = gsap.utils.toArray(".ctx");

  // ── 机制 1：焦距拉动 ─────────────────────────────────────────
  // 脱焦层在焦距移动窗口内从清晰到散焦模糊 + 变暗。
  // 模糊按 data-depth 缩放，使远平面比近平面更模糊
  //（确定性 — 从属性派生，从不 Math.random）。
  ctx.forEach((el) => {
    const depth = Number(el.dataset.depth) || 1;
    const targetBlur = BLUR_PER_DEPTH * depth; // px
    tl.to(
      el,
      {
        "--dof": `${targetBlur}px`,
        opacity: DIM_LEVEL, // 例如 0.55 — 变暗，非消失
        duration: FOCUS_DUR,
        ease: "power2.inOut",
      },
      FOCUS_START,
    );
  });
  // 聚焦层已经清晰（--dof:0, opacity:1）且未被触碰。

  window.__timelines["dof-scene"] = tl;
</script>
```

## 变体

### 两个深度平面之间的焦距切换（前景 ⇄ 背景）

每平面相同 `--dof` 上的两个相邻补间 — 焦点离开平面 A，同时落在平面 B 上。状态连续性：切换前 B 的**休息**模糊等于 A 切换后保持的值，因此交接无跳跃。

```js
// 开始：A 清晰，B 预模糊（在切换前设置，使无弹出）。
gsap.set("#planeA", { "--dof": "0px", opacity: 1 });
gsap.set("#planeB", { "--dof": `${MAX_BLUR}px`, opacity: DIM_LEVEL });

// 切换：A 散焦而 B 聚焦，相同位置 + 时长。
tl.to(
  "#planeA",
  { "--dof": `${MAX_BLUR}px`, opacity: DIM_LEVEL, duration: RACK_DUR, ease: "power2.inOut" },
  RACK_START,
);
tl.to(
  "#planeB",
  { "--dof": "0px", opacity: 1, duration: RACK_DUR, ease: "power2.inOut" },
  RACK_START,
);
```

### 推进时模糊集群（景深 + 摄像机，一个节拍）

在**相同时间线位置**同时运行焦距拉动补间和摄像机推进，使周围集群在摄像机朝核心缩放时正好退入模糊。摄像机变换 `.world`；景深补间变换层 — 独立属性，无冲突。

```js
// 摄像机朝聚焦核心推进（参见 multi-phase-camera / coordinate-target-zoom）。
tl.to(
  "#world",
  { scale: PUSH_SCALE, x: PUSH_X, y: PUSH_Y, duration: FOCUS_DUR, ease: "power2.inOut" },
  FOCUS_START,
);
// 集群在相同位置模糊 + 变暗 — "我们推进时世界后退。"
ctx.forEach((el) => {
  const depth = Number(el.dataset.depth) || 1;
  tl.to(
    el,
    {
      "--dof": `${BLUR_PER_DEPTH * depth}px`,
      opacity: DIM_LEVEL,
      duration: FOCUS_DUR,
      ease: "power2.inOut",
    },
    FOCUS_START,
  );
});
```

### 在卡片网格中聚光灯主角度量（变暗 + 模糊其余）

`dataviz-countup` 节拍：网格卡片的一个子集保持清晰（主角度量），其余变暗 + 模糊。标记主角并跳过它们；其他所有内容在一个共享窗口上散焦。

```js
gsap.utils.toArray(".card:not(.hero)").forEach((el) => {
  tl.to(
    el,
    { "--dof": `${GRID_BLUR}px`, opacity: DIM_LEVEL, duration: FOCUS_DUR, ease: "power2.out" },
    FOCUS_START,
  );
});
```

### 重新聚焦/稳定（场景结束前释放模糊）

如果节拍解析回"所有内容可见"（或移交给需要清晰退出帧的交叉淡入淡出），在尾部将模糊渐回 0，使场景在结束时清晰而非中途散焦。

```js
ctx.forEach((el) =>
  tl.to(
    el,
    { "--dof": "0px", opacity: 1, duration: REFOCUS_DUR, ease: "power2.inOut" },
    REFOCUS_START,
  ),
);
```

### 聚焦层上的有界焦点呼吸（可选）

对于微妙的"焦距稳定"感觉，让聚焦层的模糊在其保持期间在 0 附近吹拂 — 一个**有限的** `ease:"none"` 驱动器将 `sin()` 写入 `--dof`（从不 `repeat:-1`，从不 CSS 动画）。保持振幅远低于 1px，否则读作"仍在聚焦。"

```js
const drift = { p: 0 };
tl.to(
  drift,
  {
    p: Math.PI * 2 * BREATH_CYCLES,
    duration: BREATH_DUR,
    ease: "none",
    onUpdate: () => {
      const b = Math.max(0, Math.sin(drift.p)) * FOCAL_BREATH_PX; // ≤ ~0.6px
      document.getElementById("focal").style.setProperty("--dof", `${b}px`);
    },
  },
  BREATH_START,
);
```

## 如何选择值

### 几何/布局

- **FOCAL_FONT_SIZE / CTX_FONT_SIZE** — 聚焦 vs 上下文尺寸。
  - 范围：聚焦是视觉引领；上下文层较小，使适度模糊半径仍读作"失焦。"
  - 效果：小上下文层让你使用更小的 `BLUR_PER_DEPTH`（更便宜）但仍看起来柔和。
- **z-index** — 聚焦 `z-index: 2`，上下文 `z-index: 1`。
  - 约束：清晰的聚焦层必须位于模糊层**之上**，否则其清晰边缘读作渗入雾中。

### 模糊量

- **BLUR_PER_DEPTH** — 每深度步进（`data-depth`）添加的模糊 px。
  - 范围：每步 3-6 px（3 层堆栈最高约 9-18 px）
  - 效果：低 → 柔和景深；高 → 强烈微缩/移轴衰减
  - 约束：大层上**每层模糊 ≤ ~24 px** — 半径成本随模糊和面积增长；全帧元素上的大半径是昂贵情况（参见关键原则）
- **MAX_BLUR** — 完全散焦平面的终端模糊（焦距切换/焦距拉动峰值）。
  - 范围：8（柔和）→ 16（默认）→ 24（重）px
  - 约束：在大表面上超过 ~24 px，优先将层缩小或分组其内容，使模糊占地面积缩小
- **GRID_BLUR** — 变暗网格卡片上的模糊（聚光灯变体）。
  - 范围：6-12 px — 足够将它们推回而不丢失网格形状

### 变暗量

- **DIM_LEVEL** — 完全散焦时脱焦层的不透明度。
  - 范围：0.4（强推回）→ 0.55（默认）→ 0.7（微妙）
  - 效果：较低 → 上下文强烈退后/近乎聚光灯；较高 → 仍清晰可见，仅为次要
  - 约束：很少低于 0.35 — 完全黑暗的脱焦层读作"被移除"，而非"散焦"

### 时间

- **FOCUS_START / FOCUS_DUR** — 焦距拉动开始时间及其时长。
  - 范围：`FOCUS_DUR` 0.5-1.2 秒 — 焦距拉动/切换是一个有意的动作，而非快照
  - 效果：更短 → 急促"快照对焦"；更长 → 悠闲电影感焦距拉动
- **RACK_START / RACK_DUR** — 焦距切换窗口（前景 ⇄ 背景）。
  - 约束：两个平面的补间共享 `RACK_START` 和 `RACK_DUR`，使它们在中间点交叉；在 `RACK_START` 前 `gsap.set` 预模糊平面
- **REFOCUS_START / REFOCUS_DUR** — 稳定回切换窗口。
  - 约束：`REFOCUS_START + REFOCUS_DUR ≤ DURATION`，使场景在结束/交接前实际达到清晰
- **PUSH_SCALE / PUSH_X / PUSH_Y**（推进时模糊集群变体）— `.world` 上的摄像机移动。
  - 约束：与景深补间共享 `FOCUS_START` + `FOCUS_DUR`，使移动和散焦读作一个节拍；反向平移数学在 `coordinate-target-zoom` / `viewport-change` 中
- **BREATH_CYCLES / BREATH_DUR / FOCAL_BREATH_PX**（焦点呼吸变体）。
  - 范围：`FOCAL_BREATH_PX ≤ 0.6` px；周期 2-3 秒；这是一个几乎不可察觉的细微优化，默认省略

### 标记

- **{bgGradient}** — 通常为暗色，使清晰的聚焦层读作被照亮且向前
- **{textColor}** — 在 `{bgGradient}` 上高对比度；模糊柔化边缘，因此不要依赖极细对比度
- **{font}** — 展示重量；模糊的副本需要重字重才能在散焦时保持形状可读

## 关键原则

- **`--dof` 驱动模糊；补间变量，永不使用 CSS `transition`。** 在 GSAP 时间线上读取 `filter: blur(var(--dof))` 并动画化 `--dof` 使模糊保持在 HF 定位时钟上。`filter` 上的 CSS `transition` 在浏览器自己的时钟上插值，在逐帧定位下闪烁/不同步。
- **模糊小的/分组的层，而非巨大的层。** 滤镜模糊成本随半径和模糊元素的像素面积增长。全帧背景上的 20px 模糊是最坏情况；较小的上下文卡片上或单个分组包裹上的相同模糊是便宜的。优先将聚焦平面**向前推并保持清晰**，而非加大背景模糊半径。
- **每个动画化模糊的层上设置 `will-change: filter`** — 将其提升到自己的层，使每帧的重新栅格化成本低。一旦模糊稳定，如果层也做繁重变换工作，则移除它。
- **保持半径适度。** 大表面上 ≤ ~24 px；依靠 `opacity` **变暗**配合较小的模糊完成"推回"工作，而非仅靠模糊。变暗 + 适度模糊比最大模糊读作更像真实景深。
- **聚焦层保持真正清晰** — 其 `--dof` 为 `0` 且未被触碰（或呼吸 ≤0.6 px）。聚焦元素上的任何可见模糊都会杀死"这就是它"的读感。
- **切换上的状态连续性** — 离开聚焦的平面必须在切换开始时具有进入平面**之前**保持的模糊，反之亦然；将两者编写为相同 `--dof` 在相同位置的补间，使交叉无缝（与 `press-release-spring` 的按下↔释放相同规则）。
- **景深独立于摄像机** — 模糊层，变换 `.world` 用于推进。它们是不同的属性通道，因此它们无冲突地组合。不要试图用摄像机变换伪造景深，反之亦然。
- **交接前稳定清晰** — 如果下一个节拍是交叉淡入淡出/推进，在尾部重新聚焦到 `--dof:0`，使退出帧清晰；半散焦地交接读作"渲染故障。"

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **`filter` / `opacity` 上无 CSS `transition`** — 改为在时间线上动画化 `--dof` 和 `opacity`
- **无 `repeat` / `yoyo` / 无限补间** — 焦距拉动是有限补间；任何呼吸都是有界 `onUpdate` 读取驱动器相位（或有限补间），永不 `repeat:-1`
- **无 `Math.random` / `Date.now`** — 每层模糊从 `data-depth` / 元素索引派生，使每次 seek 相同
- **此处仅补间 `filter`（blur）+ `opacity`** — 两者都是仅绘制且 seek 安全。对于任何并发摄像机移动，使用 GSAP 变换别名（`x`、`y`、`scale`）；永不补间 `width` / `height` / `left` / `top`
- **模糊动画化的层上设置 `will-change: filter`**；保持模糊占地面积小
- **大表面上每层模糊半径 ≤ ~24 px** — 超出此值成本（和可见条带）攀升；改为缩小/分组层

## 组合

- [multi-phase-camera.md](multi-phase-camera.md) — 此规则提供焦点衰减的推进/推进穿过；在 PUSH 阶段的相同位置运行景深补间
- [coordinate-target-zoom.md](coordinate-target-zoom.md) — 缩放到聚焦核心，同时偏离中心层模糊（`constellation-hub` 钩子）
- [viewport-change.md](viewport-change.md) — 跨倾斜卡片平面平移，近远卡片之间焦距拉动（`cursor-ui-demo` 焦距拉动）
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 主角度量在清晰中计数递增，同时周围卡片变暗 + 模糊（`dataviz-countup` 聚光灯）
- [3d-page-scroll.md](3d-page-scroll.md) — 视差卡片堆栈，你在其平面之间切换焦距
- [sine-wave-loop.md](sine-wave-loop.md) — 聚焦层在焦距拉动稳定后空闲呼吸（保持空闲振幅和焦点呼吸都很小）

## 与 HF 技能配对

- `/hyperframes-animation` — 补间 CSS 自定义属性 + 多补间协调
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
