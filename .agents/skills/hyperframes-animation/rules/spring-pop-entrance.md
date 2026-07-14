---
name: spring-pop-entrance
description: 规范的入场弹出 — 元素（或错开组）通过从 0→1 缩放到达，以平滑长尾稳定（默认 power3）；弹跳过冲是罕见的、明确俏皮的例外。使用 fromTo 使其在 seek 下 t=0 时正确。
metadata:
  tags: spring, entrance, pop, scale, power3, settle, stagger, reveal, arrival
---

# 弹簧弹出入场

> **平滑优于弹跳。** 根据动效原则（`references/motion-language.md`），此入场**默认为平滑长尾稳定 — `power3.out`（或 `expo.out` 用于更快的到达）**，干净减速到静止尺寸，**无过冲**。弹跳的 `back.out` 过冲是代理制作视频中的**第一号即时反感因素**，几乎从未被很好地执行；它在此降级为**罕见的、明确俏皮的例外**（面向消费者/趣味品牌），绝非常规。不确定时，选择平滑稳定。

入场原语：一个元素（或它们的错开组）通过从无到有弹簧到达屏幕上 — `scale: 0 → 1`，可选带小 `y` 上升 — 使用**平滑长尾缓动（默认 `power3.out`）**，使其自信地增长到休息尺寸并稳定不弹跳。这是**到达**，而非反应。

与 [press-release-spring.md](press-release-spring.md) 明确区分：该规则是点击/按下 → 释放反馈链（一个按下阶段，然后弹簧恢复到 `1.0`）。此规则**没有按下阶段** — 没有先前的休息状态，元素在屏幕上不存在，它弹簧进入存在。许多蓝图过去借用 `press-release-spring` 来伪造入场；改用此规则。

## 工作原理

一个单一的 `fromTo` 承载整个到达：

1. **起点状态**：`{ scale: 0, opacity: 0 }` — 元素塌缩为一个点且不可见。在 `from` 对象中显式陈述，使 seek 到 `t=0` 时将元素定位到这个确切状态（永远不要依赖 CSS 隐藏的起始状态 — 参见关键约束）。
2. **终点状态（默认）**：`{ scale: 1, opacity: 1, ease: "power3.out" }` — 长尾减速，将元素生长到其休息尺寸并**平滑稳定，无过冲**。使用 `expo.out` 以获得更有力、更快前端的到达（仍无弹跳）。这个平滑稳定是风格标准；弹跳的 `back.out` 变体是罕见的俏皮例外（参见变体）。

对于**组**，每个元素运行相同的 `fromTo`，带有**确定性的、索引派生的错开**（`i * STAGGER`），总进入窗口**有上限**（`ITEM_COUNT × STAGGER ≤ ~0.5 秒`），使组读作一个到达节拍，而非缓慢的琶音。

一个小 `y` 上升（`y: 24 → 0`）在弹出之上叠加微妙的"提升到位"效果 — 可选装饰；平滑缓动上的 `scale` 生长是承载运动。（`rotation` 稳定仅属于下方俏皮过冲变体。）

## HTML

```html
<!-- 单主角弹出 -->
<div
  class="scene"
  data-composition-id="pop-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="pop-hero" id="hero">{heroLabel}</div>
</div>

<!-- 错开组：节点/卡片/图标/胶囊/标注 -->
<div
  class="scene"
  data-composition-id="pop-group-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="pop-grid">
    <div class="pop-item">{itemA}</div>
    <div class="pop-item">{itemB}</div>
    <div class="pop-item">{itemC}</div>
    <div class="pop-item">{itemD}</div>
    <div class="pop-item">{itemE}</div>
    <div class="pop-item">{itemF}</div>
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
.pop-hero {
  display: grid;
  place-items: center;
  width: {heroSize};
  height: {heroSize};
  background: {heroBg};
  border-radius: HERO_RADIUS;
  font-family: {font};
  font-weight: 900;
  font-size: HERO_FONT_SIZE;
  color: {heroTextColor};
  /* 弹出围绕中心缩放 — 参见关键约束 */
  transform-origin: 50% 50%;
  will-change: transform;
}
.pop-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: GRID_GAP;
  place-items: center;
}
.pop-item {
  display: grid;
  place-items: center;
  width: {itemSize};
  height: {itemSize};
  background: {itemBg};
  border-radius: ITEM_RADIUS;
  font-family: {font};
  font-weight: 800;
  font-size: ITEM_FONT_SIZE;
  color: {itemTextColor};
  transform-origin: 50% 50%;
  will-change: transform;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // --- 单主角弹出（默认：平滑长尾稳定，无过冲）---
  // fromTo 显式陈述塌缩起点，使主角在 seek 下 t=0 时正确。
  // power3.out 将缩放生长到 1.0 并平滑减速。
  tl.fromTo(
    "#hero",
    { scale: 0, opacity: 0 },
    {
      scale: 1,
      opacity: 1,
      duration: POP_DUR,
      ease: "power3.out", // 平滑优于弹跳；expo.out 用于更有力的前端
    },
    ENTRY_AT,
  );

  // --- 错开组弹出 ---
  // 确定性的、索引派生的错开（无 Math.random）。上限保持整个组
  // 在一个到达节拍内：ITEM_COUNT * STAGGER <= ~0.5s。
  const items = gsap.utils.toArray(".pop-item");
  items.forEach((el, i) => {
    tl.fromTo(
      el,
      { scale: 0, opacity: 0, y: Y_RISE },
      {
        scale: 1,
        opacity: 1,
        y: 0,
        duration: POP_DUR,
        ease: "power3.out",
      },
      GROUP_ENTRY_AT + i * STAGGER,
    );
  });

  window.__timelines["pop-scene"] = tl;
</script>
```

## 变体

### 平静稳定（精致/企业/"高级平静"）— 默认

`power3.out`，无旋转，去掉 `y` 上升或保持极小（~12px）。读作自信、有重量的稳定 — 适合主角 wordmark 或单个产品镜头着陆。高级/企业品牌的默认安全选择。

### 坚定稳定（默认产品揭示）— 默认

日常入场。`power3.out`（或 `expo.out` 用于更有力的前端），可选 `Y_RISE` ~24px。清晰、有意的到达，干净减速 — 卡片、图标和标注的默认安全选择。**无过冲。**

### 弹跳弹出（罕见 — 仅明确俏皮时）

例外，非常规。**仅**用于有意俏皮的基调（面向消费者/趣味品牌、玩具式图标集），其中弹跳明显是意图 — 绝不要用于产品/企业/严肃发布语调。弹跳是第一号反感因素，代理很少做得好，因此有意识且克制地使用。将 `power3.out` 替换为 `back.out(OVERSHOOT)` 并（可选）添加 `rotation` 稳定，使每个元素看起来像手工放置：

```js
// 仅俏皮例外 — 默认为 power3.out（见上方）。
tl.fromTo(
  el,
  { scale: 0, opacity: 0, rotation: ROT_FROM },
  { scale: 1, opacity: 1, rotation: 0, duration: POP_DUR, ease: `back.out(${OVERSHOOT})` },
  GROUP_ENTRY_AT + i * STAGGER,
);
```

即使在此也保持 `OVERSHOOT` 适度（≤ ~2）— 超过此值会读作卡通晃动，而非到达。

### 原点锚定弹出（标注从指针/源弹出）

当标注应看起来从特定点生长出来时（例如站点标记或指针尖端），将 `transform-origin` 设置到该点而非中心，使 `scale: 0 → 1` 读作"从源涌现"而非"在原地膨胀。"

```css
.callout {
  transform-origin: 0% 100%; /* 左下角 = 指针尖端；匹配锚点 */
}
```

### 弹出到保持槽位 — 然后保持（最多抖动）

当弹出的元素然后**保持**一个持续槽位（星群节点、持久徽章）时，**不要**将此入场烘焙为空闲循环 — 它必须保持有限。让弹出着陆并保持静止；如果保持的画面确实需要生命力，在单独的、较晚的补间上移交给 [sine-wave-loop.md](sine-wave-loop.md) 用于**微妙抖动**（低振幅）— 而非呼吸循环。优先在 VO 提示上揭示下一个元素，而非让此元素持续动画。

## 如何选择值

- **缓动** — 稳定曲线（承载决策）
  - 默认：**`power3.out`** — 平滑长尾稳定，无过冲；产品/企业/严肃语调的风格标准。使用 `expo.out` 获得更有力、更快前端的到达（仍平滑）。
  - 仅俏皮例外：`back.out(OVERSHOOT)` — 参见弹跳弹出变体；仅当弹跳明显是品牌意图时才使用。

- **OVERSHOOT** — `back.out(OVERSHOOT)` 过冲强度 — **仅在罕见的俏皮变体中使用**；平滑默认没有过冲调节
  - 范围（仅俏皮）：~1.3（几乎不可见）→ ~2.0（明显弹跳）
  - 约束：保持 ≤ ~2 — 超过此值过冲超出元素边界，读作卡通晃动，而非到达。如果你不在明确俏皮的情况中，不要使用此值 — 使用 `power3.out`。

- **POP_DUR** — 每个元素的 `scale: 0 → 1` 补间时长
  - 范围：0.4 – 0.7 秒
  - 效果：更短 = 紧密快照；更长 = 更松散、更漂浮的弹出
  - 约束：主要主体必须在 **`t ≤ 0.5 秒`** 时可见 — 使 `ENTRY_AT + POP_DUR` 的可读中点提前；不要让主角在半秒标记后完成到达

- **STAGGER** — 连续项目开始时间之间的间隔（仅组）
  - 范围：0.04 – 0.08 秒
  - 效果：< 0.04 读作同时和弦；> 0.08 感觉懒散/琶音
  - 约束：**`ITEM_COUNT × STAGGER ≤ ~0.5 秒`**（上限）— 超过此值组停止读作一个节拍。大型组的每项错开上限：`STAGGER = min(0.06, 0.5 / ITEM_COUNT)`

- **ITEM_COUNT** — 组弹出中的元素数
  - 范围：3 – 9
  - 效果：3 = 稀疏；9 = 完整网格。超过 ~9 迫使 `STAGGER` 如此之小，错开消失 — 改为使用擦拭/扫过揭示

- **Y_RISE** — 元素提升的可选向上偏移（`y: Y_RISE → 0`）
  - 范围：0（纯弹出）– 32 px
  - 效果：添加微妙的"提升到位"效果；保持小量使 `scale` 弹出保持主导
  - 约束：平静稳定变体为 0；永远不要大到读作上滑（那是不同的原语）

- **ROT_FROM** — 可选的起始旋转，**仅俏皮（弹跳）变体**（`rotation: ROT_FROM → 0`）
  - 范围：-10° – +10°
  - 效果：一个解析的小倾斜使元素看起来像手工放置
  - 约束：如果你想要交替倾斜，从索引确定性派生符号/大小（例如 `i % 2 ? 6 : -6`）— 绝不要 `Math.random`

- **ENTRY_AT / GROUP_ENTRY_AT** — （组的）弹出开始前的时间线偏移
  - 范围：0 – 0.4 秒
  - 效果：> 0 在到达前给一个安静节拍；保持小量使主体仍在 `t ≤ 0.5s` 着陆

### 几何与标记

- **{heroSize} / {itemSize}** — 占地面积。主角入场应占据清晰可读的画面份额；组项目缩小使网格适应 `GRID_GAP` 呼吸空间。
- **HERO_RADIUS / ITEM_RADIUS** — `height × 0.15`（锋利）→ `height / 2`（胶囊）。
- **{heroBg} / {itemBg} / {\*TextColor}** — 表面 + 标签标记；从组合调色板继承。

## 关键原则

- **平滑优于弹跳** — 默认为 `power3.out`（或 `expo.out`）：长尾稳定到 `scale: 1`，无过冲。弹跳的 `back.out` 是罕见的、明确俏皮的例外（第一号反感因素，且代理很少做得好）。不确定时，平滑稳定。
- **始终使用 fromTo** — 塌缩的 `{ scale: 0, opacity: 0 }` 起点在 `from` 对象中陈述，使 seek 到 `t=0` 时精确地定位到那里。基于 CSS 隐藏起点（例如 CSS 中的 `opacity:0` + `.to()`）的入会在 HF 定位下闪烁 — 元素在补间声明它之前就已渲染可见。
- **缓动承载运动，而非关键帧** — 让缓动免费产生稳定。不要手动设置 `scale: 1.1` 中间状态；那会双重弹跳并与曲线冲突。（在俏皮变体中，过冲是 `back.out` 的副产品，而非手动键控的弹跳。）
- **生长就是运动** — `scale` 是承重的；`y` 上升（以及在俏皮变体中，`rotation` 稳定）是叠加在顶部的装饰。如果除了 `scale` 生长你放弃一切，它仍应读作一个干净的入场。
- **限制错开窗口** — 组必须在总 ~0.5 秒内到达，否则它不再读作一个节拍，而是读作一个慢列表揭示。从 `ITEM_COUNT` 派生错开，使其自上限。
- **按索引确定性** — 所有错开和任何旋转/倾斜变化来自循环索引，永远不是 `Math.random` — 渲染器必须在每次 seek 时产生相同的帧。
- **尽早可见** — 主要主体必须在 `t ≤ 0.5 秒` 时在屏幕上。在 `t=1s` 才完成到达的主角浪费了开场节拍。
- **不要在此烘焙空闲循环** — 此入场是有限的。如果元素然后保持一个槽位，在较晚的补间上移交给 `sine-wave-loop`；此处的无限 `repeat`/`yoyo` 会破坏定位。

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **入场使用 `fromTo`** — 显式 `{ scale: 0, opacity: 0 }` 起点状态；永远不要依赖 CSS 隐藏的起始状态
- **弹跳元素上无 CSS `transition`** — 那些会独立于 HF 定位插值并导致闪烁
- **无 `repeat` / `yoyo` / 无限补间** — 这是一个有限到达；空闲运动是单独的 `sine-wave-loop` 补间
- **无 `Math.random` / `Date.now`** — 错开和倾斜是索引派生的、确定性的
- **仅使用 GSAP 变换别名**：`x`、`y`、`scale`、`rotation`。永远不要补间 `width` / `height` / `left` / `top`
- **`transform-origin: 50% 50%`** 用于原位弹出（默认）；仅原点锚定变体将其设置为源点
- **默认缓动 `power3.out`**（平滑，无过冲）；仅在明确俏皮变体中使用 `back.out(OVERSHOOT)`，且保持 **`OVERSHOOT ≤ ~2`** — 超过此值读作卡通晃动，而非到达
- **`ITEM_COUNT × STAGGER ≤ ~0.5 秒`** — 组必须在一个节拍内着陆
- **弹出元素上设置 `will-change: transform`**，尤其是组 — 许多同时弹簧补间受益于合成器提示

## 组合

- [sine-wave-loop.md](sine-wave-loop.md) — 在弹出着陆后，保持的节点/徽章上最多**微妙抖动**（不要将任何循环烘焙到入场中；且优先选择 VO 定时的揭示而非环境运动 — 参见该规则的警告）
- [center-outward-expansion.md](center-outward-expansion.md) — 元素在从中心辐射到其槽位时弹出
- [press-release-spring.md](press-release-spring.md) — 反应的对应物：一旦弹出，按钮可以接受按下→释放；此规则提供到达，那条规则提供点击反馈

## 与 HF 技能配对

- `/hyperframes-animation` — `power3.out` 稳定（平滑默认）、`fromTo` 入场、确定性错开
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
