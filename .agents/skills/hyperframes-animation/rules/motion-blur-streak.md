---
name: motion-blur-streak
description: 在快进入或摄像机推进穿过上伪造方向速度模糊 — 模糊在最大速度时达到峰值，在稳定时解析为 0，使元素条纹进入然后快照清晰。两条路径 — 运动轴上的 SVG feGaussianBlur，或塌缩到前导的回声/鬼影轨迹。
metadata:
  tags: motion-blur, velocity, streak, entrance, fly-in, ghost, echo, svg-filter, kinetic, camera, snap
---

# 运动模糊条纹

真正的逐帧运动模糊对于 seek 的渲染器不可用（它在快门时间上积分，暂停的时间线没有这个概念），因此此规则为快速元素飞入或硬摄像机推进穿过**伪造**它。模糊在**最大速度时达到峰值，在稳定时解析为 0** — 元素读作条纹进入然后在到达时清晰快照。关键是**耦合**：模糊包络与位置补间使用相同的缓动和窗口，因此峰值模糊精确落在峰值速度上，元素在停止瞬间极其清晰。

两个实现路径，都是有限、确定性和 seek 安全的：

- **(A) 方向 SVG 模糊** — 内联 `<filter>` 带 `<feGaussianBlur stdDeviation="X 0">`（X 在运动轴上，0 在垂直轴上）。GSAP 通过代理对象将 `X` 从高 → 0 补间，在 `onUpdate` 中调用 `setAttribute`。最干净，一个元素，真实的方向拖影。
- **(B) 回声/鬼影轨迹** — 2–4 个重复副本，以递减不透明度沿运动向量向后偏移，在元素稳定时塌缩到前导元素。无滤镜开销；读作"速度线"结巴轨迹。当你想要条纹**彩色**或**风格化**而非字面光学模糊时更好。

这仅用于**入场和镜头中段移动** — 快速到达、缩放过摄像机的节拍、撞入网格槽位的卡片、冲进组合的 logo。**绝不是非最终帧上的退出**（在组合中段模糊元素从画面逃离读作故障，场景间的硬退出是过渡的工作，而非逐元素模糊）。

## 工作原理

快速移动有一个速度轮廓：它从起点加速，达到峰值，然后减速进入稳定。`out` 缓动（`expo.out`、`power4.out`）提前加载该特性 — 速度在开始时最高，在结束时降到零。伪造通过将**模糊（或回声）包络映射到同一曲线**来工作：

1. **位置补间** — 元素从画面外/推回起点以快速 `out` 缓动在 `MOVE_DUR` 内旅行到其休息变换（`x`/`y` 用于飞入，`scale` 用于推进穿过）。
2. **模糊包络** — 在**相同窗口和缓动**上步调一致，拖影从 `PEAK_BLUR` → 0。由于缓动提前加载速度且包络共享它，最大模糊与最大速度重合，模糊在元素着陆时精确达到 0。
3. **稳定是清晰的** — 到 `MOVE_START + MOVE_DUR` 时，元素在其休息变换，模糊为 0（路径 A）或所有回声塌缩到前导上（路径 B）。然后保持，完全清晰，用于高潮停留。

路径 A 通过**代理对象**补间滤镜的 `stdDeviation` 属性（一个非 DOM 风格的数字属性） — GSAP 不能直接补间 SVG 属性，因此你补间一个纯 `{ v: PEAK_BLUR }` 并在 `onUpdate` 中用 `setAttribute` 写回。路径 B 将鬼影放置在确定性向后偏移（`i * ECHO_STEP_PX`）并在相同包络上淡出/塌缩它们。

## HTML

### 路径 A — 方向 SVG 模糊（推荐默认）

```html
<div
  class="scene"
  id="streak-scene"
  data-composition-id="streak-scene"
  data-start="0"
  data-duration="DURATION"
  data-track-index="0"
>
  <!-- 内联滤镜：仅在 X 轴上模糊（stdDeviation="X 0"）；Y 上为 0 保持干净的横向拖影。 -->
  <svg width="0" height="0" aria-hidden="true" style="position: absolute">
    <defs>
      <filter id="streak" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur id="streak-blur" in="SourceGraphic" stdDeviation="0 0" />
      </filter>
    </defs>
  </svg>

  <div class="streak-stage">
    <div class="streak-el" id="streak-el">{phrase}</div>
  </div>
</div>
```

### 路径 B — 回声/鬼影轨迹

```html
<div
  class="scene"
  id="streak-scene"
  data-composition-id="streak-scene"
  data-start="0"
  data-duration="DURATION"
  data-track-index="0"
>
  <div class="streak-stage">
    <!-- N-1 个鬼影在前导后面，然后前导在最上面。鬼影是 aria-hidden 的重复副本。 -->
    <div class="streak-ghost" data-i="3" aria-hidden="true">{phrase}</div>
    <div class="streak-ghost" data-i="2" aria-hidden="true">{phrase}</div>
    <div class="streak-ghost" data-i="1" aria-hidden="true">{phrase}</div>
    <div class="streak-el" id="streak-el">{phrase}</div>
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
  background: {sceneBg};
  font-family: {font};
  overflow: hidden; /* 拖影/回声在稳定前延伸到休息位置之外 */
}
.streak-stage {
  position: relative;
  display: grid;
  place-items: center;
}
.streak-el {
  position: relative;
  z-index: 2;
  font-size: EL_FONT_SIZE;
  font-weight: 900;
  letter-spacing: EL_TRACKING;
  color: {textColor};
  /* 仅路径 A — 引用方向滤镜。路径 B 省略此项。 */
  filter: url(#streak);
  will-change: transform, filter;
}

/* 路径 B 鬼影 — 前导后面相同的字形，递减不透明度 */
.streak-ghost {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  z-index: 1;
  font-size: EL_FONT_SIZE;
  font-weight: 900;
  letter-spacing: EL_TRACKING;
  color: {textColor};
  opacity: 0;
  will-change: transform, opacity;
  pointer-events: none;
}
```

## GSAP 时间线

### 路径 A — 方向 SVG 模糊

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // GSAP 不能直接补间 SVG 属性 — 补间一个代理并在每帧写回。
  const blurNode = document.getElementById("streak-blur");
  const blurProxy = { v: PEAK_BLUR };
  const writeBlur = () => blurNode.setAttribute("stdDeviation", `${blurProxy.v} 0`); // 仅 X 轴
  writeBlur(); // 种子帧 0，使 seek 到 t=0 显示条纹起始，而非清晰的预帧

  // 位置：从画面外到休息位置，使用快的 `out` 缓动（速度提前加载）。
  tl.fromTo(
    "#streak-el",
    { x: ENTER_FROM_X, opacity: 0 },
    { x: 0, opacity: 1, duration: MOVE_DUR, ease: MOVE_EASE },
    MOVE_START,
  );

  // 模糊包络：相同窗口 + 相同缓动，使峰值模糊 == 峰值速度，在稳定时解析为 0。
  tl.to(blurProxy, { v: 0, duration: MOVE_DUR, ease: MOVE_EASE, onUpdate: writeBlur }, MOVE_START);

  window.__timelines["streak-scene"] = tl;
</script>
```

### 路径 B — 回声 / 鬼影轨迹

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 前导元素：与路径 A 相同的快速 `out` 移动。
  tl.fromTo(
    "#streak-el",
    { x: ENTER_FROM_X, opacity: 0 },
    { x: 0, opacity: 1, duration: MOVE_DUR, ease: MOVE_EASE },
    MOVE_START,
  );

  // 鬼影：每个沿运动向量从更**远**处开始（按索引确定性），
  // 更暗，并塌缩到前导 — 都在相同缓动/窗口上，使它们在稳定时消失。
  const ghosts = gsap.utils.toArray(".streak-ghost");
  ghosts.forEach((g) => {
    const i = Number(g.dataset.i); // 1..N-1，在 HTML 中设置（无 Math.random）
    tl.fromTo(
      g,
      { x: ENTER_FROM_X - i * ECHO_STEP_PX, opacity: GHOST_BASE_OPACITY / i },
      { x: 0, opacity: 0, duration: MOVE_DUR, ease: MOVE_EASE },
      MOVE_START,
    );
  });

  window.__timelines["streak-scene"] = tl;
</script>
```

## 变体

### 垂直条纹（上升/下落）

交换运动轴：位置补间使用 `y` 而非 `x`，路径 A 使用 `stdDeviation="0 Y"`（Y 上模糊，X 上为 0），路径 B 使用 `ENTER_FROM_Y` / 垂直回声偏移。一个短语**向上**条纹进入位置与 `kinetic-type-beats` 的上升旋转节拍配对。

### 摄像机推进穿过（缩放条纹进入组合）

元素平移而非平移：以快速 `out` 缓动从 `scale: SCALE_FROM → 1`，通过对称 `stdDeviation="B B"` 包络近似**径向/缩放模糊**感觉（因为拖影是深度方向而非方向性的）。这是 `logo-assemble-lockup` 推进穿过 — wordmark 从柔和失焦向前冲出并在组合处清晰快照。

```js
tl.fromTo(
  "#streak-el",
  { scale: SCALE_FROM, opacity: 0 },
  { scale: 1, opacity: 1, duration: MOVE_DUR, ease: MOVE_EASE },
  MOVE_START,
);
tl.to(
  blurProxy,
  {
    v: 0,
    duration: MOVE_DUR,
    ease: MOVE_EASE,
    onUpdate: () => blurNode.setAttribute("stdDeviation", `${blurProxy.v} ${blurProxy.v}`),
  },
  MOVE_START,
);
```

### 错开网格条纹进入（卡片组装）

对于 `grid-card-assemble`：每张卡片从其自身的向后偏移条纹进入其槽位，错开。以逐索引延迟从相同缓动/窗口驱动每张卡片；从卡片索引派生出入口偏移和开始时间（无 `Math.random`）。每张卡片在着陆到其槽位的瞬间清晰。

```js
gsap.utils.toArray(".grid-card").forEach((card, i) => {
  const at = MOVE_START + i * CARD_STAGGER;
  tl.fromTo(
    card,
    { x: ENTER_FROM_X, opacity: 0 },
    { x: 0, opacity: 1, duration: MOVE_DUR, ease: MOVE_EASE },
    at,
  );
  // + 在相同 `at`（路径 A）或每卡片鬼影（路径 B）的每卡片模糊代理补间
});
```

### 保持条纹（单节拍上的鞭打强调）

对于单个动感短语"缩放经过"，通过使用比位置略**慢**的曲线缓动模糊，将条纹保持可见稍长一或两帧（例如位置 `expo.out`，模糊 `power3.out`）— 元素到达，然后最后一缕拖影解析。谨慎使用；默认是锁定包络。

## 如何选择值

### 运动

- **MOVE_EASE** — 位置和模糊/回声的共享缓动。
  - 范围：`expo.out`（最硬快照）、`power4.out`（硬撞击，默认）、`power3.out`（坚定但柔和）
  - 效果：更硬的 `out` → 速度更提前加载 → 模糊读作更锐利的条纹，在窗口中后期解析
  - 约束：必须是 `out` 族缓动（速度提前加载）。`inOut` 或 `in` 缓动将峰值速度放在中/后部，模糊-速度耦合破裂。**位置和模糊必须使用相同的缓动**（除了有意的保持条纹变体）。
- **MOVE_DUR** — 行进 + 模糊解析时长。
  - 范围：0.25–0.6 秒
  - 效果：更短 → 更猛烈的鞭打；更长 → 滑行，条纹失去冲击力
  - 约束：条纹是**快的** — 超过 ~0.7 秒它停止读作速度模糊，看起来像焦距拉动
- **MOVE_START** — 入场的时间线位置。
  - 约束：在 `MOVE_START + MOVE_DUR` 后留下 **≥1 秒的停留**，然后组合结束（高潮停留 — 在 `t = DURATION − 0.2 s` 着陆的条纹读作"闪烁然后消失"）
- **ENTER_FROM_X / ENTER_FROM_Y** — 沿运动轴从画面外的起始偏移。
  - 范围：元素在该轴上自身尺寸的 40–120%（足够远，读作"从画面外来"）
  - 效果：更大 → 更长行进 → 条纹有更多跑道可读；太小则没有速度感

### 路径 A — SVG 模糊

- **PEAK_BLUR** — 最大速度时的 `stdDeviation`（窗口开始）。
  - 范围：8（微妙）→ 18（默认）→ 30（极端鞭打）
  - 效果：更高 → 峰值速度时更重的拖影；太高会在开始帧完全擦除字形
  - 约束：≤ ~30 — 超过此值元素在前几帧不可读，读作"消失然后出现"；滤镜区域（`<filter>` 上的 `x/y/width/height`）必须足够大（≥`-50% … 200%`），否则拖影在框边缘被裁剪
- **SCALE_FROM**（推进穿过变体）— 摄像机推进的起始缩放。
  - 范围：1.3（轻柔推进）→ 2.5（激进冲入）

### 路径 B — 回声轨迹

- **N（鬼影数量）** — 前导后面的鬼影数量（由你编写多少个 `.streak-ghost` 决定）。
  - 范围：2–4
  - 效果：更多鬼影 → 更长、更平滑的拖影；>4 读作结巴/频闪而非条纹
- **ECHO_STEP_PX** — 沿运动向量每个鬼影的后向偏移。
  - 范围：12–40 px
  - 效果：更大 → 更分散、可见的轨迹；更小 → 紧密的模糊状群组
  - 约束：`(N) × ECHO_STEP_PX` 应 ≲ `ENTER_FROM_X`，使最远的鬼影仍从行进跑道内开始
- **GHOST_BASE_OPACITY** — 最近鬼影（`i = 1`）的不透明度；按 `BASE / i` 衰减。
  - 范围：0.3（微弱）→ 0.6（明显）
  - 约束：≤ ~0.6 — 不透明鬼影读作重复元素，而非轨迹

### 布局与字体

- **EL_FONT_SIZE / EL_TRACKING** — 条纹元素的字体重量（当它是一个短语时）。
  - 约束：重的展示重量（1080p 下 ≥120 px，≥800 字重），使拖影有质量可条纹；细字体拖影为不可见
- **CARD_STAGGER**（网格变体）— 连续卡片之间的延迟。
  - 范围：0.05–0.12 秒 — 紧密到读作一个组装波，而非单独的到达

### 标记

- **{sceneBg}** — 背景；条纹在纯/低细节场上读作最佳（繁忙背景与拖影竞争）
- **{font}** — 排版栈（如果条纹元素是文本，嵌入的展示字体 — 参见排版参考）
- **{textColor}** — 元素颜色；对于路径 B，鬼影继承此颜色，因此通过单独着色 `.streak-ghost` 可以获得稍去饱和的轨迹
- **{phrase}** — 条纹进入的单词/字形/wordmark

## 关键原则

- **模糊在峰值速度时达到峰值，在稳定时解析为 0** — 这是整个规则。在位置补间和模糊/回声包络之间共享缓动和窗口，使它们锁定。元素停止后残留的模糊，或在元素已经慢后达到峰值的模糊，读作焦距拉动，而非速度。
- **始终使用 `out` 族缓动** — 速度必须提前加载（从起步快，减速进入）。`expo.out` / `power4.out` / `power3.out`。`in` 或 `inOut` 缓动将峰值速度放在错误位置，耦合崩溃。
- **运动轴上的方向模糊**（路径 A）— 横向移动用 `stdDeviation="X 0"`，垂直移动用 `"0 Y"`，仅深度/缩放推进用 `"B B"`。侧向移动上的对称模糊看起来像失焦，而非速度。
- **补间代理，写入属性**（路径 A）— GSAP 补间纯 `{ v }` 对象；`onUpdate` 调用 `setAttribute("stdDeviation", …)`。你不能直接补间 SVG 属性，且你必须在设置时**种子化一次**，使 seek 到 `t=0` 显示条纹起始。
- **鬼影按索引确定性**（路径 B）— 偏移 `i * ECHO_STEP_PX`，不透明度 `BASE / i`。轨迹绝不用 `Math.random`；索引驱动所有逐鬼影变化，使每次 seek 相同。
- **仅入场，绝不是组合中段的退出** — 条纹是一种**到达**。非最终帧上离开的模糊元素读作故障；场景到场景的退出是过渡的工作（参见 `../../transitions/overview.md`）。
- **赢得清晰的保持** — 快照后，清晰元素必须停留 ≥1 秒。暴力条纹和静止、清晰的稳定之间的对比**就是**效果。
- **重元素，实心背景** — 细字体或繁忙背景都会吞没拖影。在干净场上的大块粗体读得出来。

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`。永远不要 `tl.play()`。
- **根元素上的注册键 = `data-composition-id`**。
- **条纹元素（或鬼影）上无 CSS `transition`** — 它独立于 HF 定位插值并导致闪烁。只有 GSAP 驱动移动和模糊。
- **无 `repeat` / `yoyo` / 无限** — 条纹是单个有限到达。仅限有限补间。
- **无 `Math.random` / `Date.now`** — 鬼影偏移/不透明度和任何错开从元素索引派生；每次 seek 确定性。
- **仅使用 GSAP 变换别名**：`x`、`y`、`scale`、`rotation`。永远不要补间 `width` / `height` / `left` / `top`。补间 `filter`（代理 → `stdDeviation`）和 `opacity` 是 seek 安全且可以的。
- **在设置时种子化 SVG `stdDeviation`**（路径 A）— 在播放前写一次，使 seek 到第一帧渲染条纹起始，而非瞬间清晰的预帧。
- **滤镜区域必须慷慨**（路径 A）— `<filter x="-50%" y="-50%" width="200%" height="200%">`，使拖影不被裁剪在元素的框边缘。
- **场景上设置 `overflow: hidden`** — 拖影/最远的鬼影在行进期间延伸到休息位置之外；容纳它，使其不溢出画面。

## 组合

- [kinetic-beat-slam.md](kinetic-beat-slam.md) — 将此条纹作为节拍序列中一个短语的入场使用（缩放撞击节拍**是**运动模糊飞入）；从共享的 `BEATS[]` 数组读取其开始时间
- [center-outward-expansion.md](center-outward-expansion.md) — 网格条纹进入是中心扩展，每个元素行进上带速度模糊包络
- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 条纹进入的短语上的挤压深度（深度层跟随前导的变换）
- [scale-swap-transition.md](scale-swap-transition.md) — 用于**相同**占地面积状态交换的替代方案（此规则用于从画面外/深度的快速**到达**，而非变形）

## 与 HF 技能配对

- `/hyperframes-animation` — `out` 族缓动、代理驱动的 `onUpdate` 属性补间和锁定包络协调（`../../adapters/gsap-easing-and-stagger.md`）
- `/hyperframes-creative` — `references/typography.md`（文本条纹的嵌入展示字体）、`references/video-composition.md`（拖影后的实心场）
- `/hyperframes-core` — 组合接线、确定性（有限补间、无 `Math.random`）
- `/hyperframes-cli` — `hyperframes lint` / `hyperframes validate`（validate 捕获缺失的 `#streak-blur` 节点或未引用的滤镜）
