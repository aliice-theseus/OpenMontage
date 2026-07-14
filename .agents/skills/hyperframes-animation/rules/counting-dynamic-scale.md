---
name: counting-dynamic-scale
description: 计数器动画，字号随计数值增长，创造递增的视觉重量。
metadata:
  tags: counter, counting, scale, font-size, number, dynamic, emphasis
---

# 动态缩放计数

数字从 A 计数到 B，同时其字号增长，创造递增的视觉重量，强化量级。

## 工作原理

一个单一的缓动时间线驱动**两个同步属性**：

1. 数值（通过 `onUpdate` 渲染为 DOM 文本）
2. 字号（从 `START_SIZE` → `END_SIZE` 补间）

随着数字变大，文本也变大 — 视觉上传达"这令人印象深刻。"

## 缓动

按所需的戏剧性选择（选择是离散的；系数是隐式的）：

| GSAP 缓动     | 效果                                        |
| ------------- | ------------------------------------------- |
| `power1.out`  | 温和 — 轻微减速                             |
| `power2.out`  | 默认 — 缓出，快起始慢结束                    |
| `power3.out`  | 强 — 戏剧性减速 ⭐ 推荐                      |
| `expo.out`    | 非常戏剧性 — 几乎在结束时停止                |

`power3.out` 匹配多项式 `1 - (1-x)^k` 族在 k ≈ 2.5 处 — 数字冲上去然后在峰值剧烈减速。

## HTML

```html
<div
  class="scene"
  data-composition-id="counter-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="counter-wrap">
    <span class="counter" id="counter">0</span><span class="counter-suffix">{suffix}</span>
  </div>
  <div class="counter-label">{label}</div>
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

.counter-wrap {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 8px;
  /* 固定宽度容器防止数字位数变化时布局偏移 */
  width: {counterContainerWidth};
  text-align: center;
}

.counter {
  font-family: {font};
  font-weight: 900;
  color: {textColor};
  /* 必须 — tabular-nums 保持数字宽度相同 */
  font-variant-numeric: tabular-nums;
  /* 初始字号；GSAP 将补间此属性 */
  font-size: {startSize};
  letter-spacing: -2px;
  line-height: 1;
}

.counter-suffix {
  font-family: {font};
  font-weight: 800;
  color: {accentColor};
  font-size: {suffixSize};
  opacity: 0;
  transform: translateY(20px);
}

.counter-label {
  margin-top: 24px;
  font-family: {font};
  font-size: {labelSize};
  color: {mutedTextColor};
  text-align: center;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const counter = document.getElementById("counter");
  const state = { value: 0, fontSize: START_SIZE };

  // 同步计数 + 字号补间
  tl.to(
    state,
    {
      value: TARGET_VALUE,
      fontSize: END_SIZE,
      duration: COUNT_DUR,
      ease: COUNT_EASE,
      onUpdate: () => {
        counter.textContent = Math.round(state.value).toLocaleString();
        counter.style.fontSize = `${state.fontSize}px`;
      },
    },
    0,
  );

  // 后缀在计数完成后滑入
  tl.to(
    ".counter-suffix",
    {
      opacity: 1,
      y: 0,
      duration: SUFFIX_DUR,
      ease: `back.out(${SUFFIX_BOUNCE_FACTOR})`,
    },
    COUNT_DUR,
  );

  // 标签提前淡入
  tl.from(
    ".counter-label",
    {
      opacity: 0,
      y: 12,
      duration: LABEL_DUR,
      ease: "power2.out",
    },
    LABEL_AT,
  );

  window.__timelines["counter-scene"] = tl;
</script>
```

## 如何选择值

- **TARGET_VALUE** — 计数器着陆的数字
  - 效果：2–3 位数字在主角大小时读作最佳；4+ 位数字需要更宽的容器
  - 约束：必须在 END_SIZE 时水平适应容器
- **START_SIZE / END_SIZE** — 初始和最终字号
  - 范围：START_SIZE ≈ END_SIZE 的 40–60%
  - 效果：更小的 START_SIZE = 更戏剧性的增长；更大 = 更微妙
  - 约束：END_SIZE × 数字位数必须适应容器宽度而不裁剪
- **COUNT_DUR** — 计数 + 缩放补间时长
  - 范围：1.2–2.5 秒
  - 效果：更短 = 激进；更长 = 稳定，给阅读时间
  - 约束：必须让眼睛能阅读滚过的数字；低于 ~0.8 秒读作闪烁
- **COUNT_EASE** — 值和字号的共享缓动
  - 离散选择：`power2.out`、`power3.out`、`expo.out`（参见上表）
  - 约束：避免 `back.out` / `elastic.out` — 过冲读作不稳定数据
- **SUFFIX_DUR** — 后缀滑入时长
  - 范围：0.3–0.6 秒
  - 效果：更短 = 快照；更长 = 浮动
  - 约束：必须在计数着陆后触发（在 COUNT_DUR 开始），而非期间
- **SUFFIX_BOUNCE_FACTOR** — 后缀入场的 back.out 系数
  - 范围：1.4–2.0
  - 效果：1.4 = 小过冲；2.0 = 弹跳
- **LABEL_AT / LABEL_DUR** — 标签淡入的时间和时长
  - 范围：LABEL_AT < COUNT_DUR / 2（标签在计数达到峰值前到达）；LABEL_DUR 0.4–0.7 秒

## 变体

### 直接 `innerText` 补间（无代理对象）

GSAP 检查器直接读取 `innerText`，因此仅数字的计数器可以跳过 `state` 代理：

```js
tl.to(
  counter,
  { innerText: TARGET_VALUE, duration: COUNT_DUR, ease: COUNT_EASE, snap: { innerText: 1 } },
  0,
);
```

`snap: { innerText: 1 }` 保持为整数。当必须**共同驱动**字号、区域格式（`toLocaleString`）或同一补间中的后缀时，保留代理对象 `onUpdate` 形式（如上）— `innerText` 单独无法做到这些，而动态缩放正是此规则的要点，因此代理形式是这里的默认值。

### 3D 深度入场

与 `translateZ` 组合实现视差风格深度入场：

```js
tl.from(
  ".counter",
  {
    z: -300,
    duration: 0.6,
    ease: "power2.out",
    // 需要父级或 .counter 本身设置 perspective
  },
  0,
);
```

CSS 先决条件：

```css
.counter-wrap {
  perspective: 1000px;
}
.counter {
  transform-style: preserve-3d;
}
```

### 多统计协调揭示

对于并行计数的 3 个统计，共享相同的缓动和时长，使它们同时完成 — 视觉上是一个和弦，而非琶音。每个统计通常也需要一个**配对图形**（条/环/星）— 不要只停在数字上；参见 [stat-bars-and-fills.md](stat-bars-and-fills.md)：

```js
["#stat1", "#stat2", "#stat3"].forEach((sel, i) => {
  const obj = { v: 0 };
  tl.to(
    obj,
    {
      v: TARGETS[i],
      duration: COUNT_DUR,
      ease: COUNT_EASE,
      onUpdate: () => (document.querySelector(sel).textContent = Math.round(obj.v)),
    },
    0,
  ); // 相同起始位置 — 和弦
});
```

## 关键原则

- **在一个补间中同步值和大小**，使它们共享缓动并保持协调
- **`font-variant-numeric: tabular-nums` 是强制性的** — 没有它，数字位数转换（例如 9 → 10 → 100）会因字形宽度变化引起可见抖动
- **固定宽度容器**作为双重保障 — 即使有 tabular-nums，字形形状变化也可能偏移基线
- **原位增长，不弹跳** — 数字应感觉有重量，而非有弹性。`power3.out` 在精确值结束；`back.out` 过冲并感觉卡通化
- **从小到足以明显增长开始**（最终大小的 ~50%）；结束大到足以感觉果断但不超过视口
- **后缀在计数后动画，而非期间** — 给数字自己的节拍
- **❗ 标签是大字体，而非页面风格的小标题** — 对于视频，主角大小数字下方的小段落风格标题读作视觉噪声。使用展示大小、大写、跟踪的标签，使布局为"两行大字体"；标签是标题的一部分，而非页脚。

## 关键约束

- **`tabular-nums` 必须** — 布局稳定性所需的 CSS
- **时间线必须暂停**：`gsap.timeline({ paused: true })`。永远不要 `tl.play()`
- **注册键 = `data-composition-id`**：`window.__timelines["counter-scene"]` 必须匹配场景根元素
- **`onUpdate` 变更 DOM**：HF 运行时逐帧定位时间线，因此 `onUpdate` 在每次 seek 调用时运行。保持 `onUpdate` 工作为 O(1) — 设置文本 + 字号，无 DOM 创建
- **使用 `Math.round` 而非 `Math.floor`** — 最终整数的一半处应短暂显示最终值，而非前一个值
- **避免计数器本身使用 `back.out` / `elastic.out`** — 过冲使数字看起来不稳定（它是数据，非装饰）

## 组合

- [stat-bars-and-fills.md](stat-bars-and-fills.md) — **数字旁边的配对图形**（增长条/进度环/星擦拭）。一个统计场景通常同时需要两个规则：这里的计数递增 + 那里的填充。给填充相同的缓动和时长，使数字和图形作为一个节拍着陆。
- [svg-path-draw.md](svg-path-draw.md) — 图标在数字周围绘制
- [center-outward-expansion.md](center-outward-expansion.md) — 相关图标在计数峰值时向外爆发

## 与 HF 技能配对

- `/hyperframes-animation` — 时间线 + `onUpdate` API
- `/hyperframes-core` — 组合接线、`data-*` 属性
- `/hyperframes-cli` — `hyperframes lint` 验证场景
