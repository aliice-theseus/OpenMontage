---
name: vertical-spring-ticker
description: 老虎机型垂直滚动，在遮罩容器内使用累加弹簧物理 — 每个弹簧贡献一个"步进"的滚动。
metadata:
  tags: text, ticker, spring, scroll, vertical, slot-machine, sequence
---

# 垂直弹簧滚动条（老虎机）

多个弹簧补间**累加在一起**产生总 Y 平移。每个弹簧贡献一个离散的"步进"。组合运动具有干脆利落的独立移动和自然稳定感 — 而不是单一的线性滚动，你得到老虎机的"咔嗒咔嗒咔嗒"节奏。

## 工作原理

容器具有固定高度 `ITEM_HEIGHT`，`overflow: hidden`。内部是项目的垂直堆栈，每个也有 `ITEM_HEIGHT` 高度。内部堆栈的平移计算为：

```
translateY = -ITEM_HEIGHT * sum(spring_i.progress for each spring)
```

每个弹簧在不同时间触发，稳定，然后下一个触发。累加时，堆栈逐步向前快照。"弹簧"缓动使每一步有一个微小的过冲/稳定，将其与线性滚动区分开。

## HTML

```html
<div
  class="scene"
  id="ticker-scene"
  data-composition-id="ticker-scene"
  data-start="0"
  data-duration="5"
  data-track-index="0"
>
  <div class="stack">
    <div class="eyebrow">{eyebrow}</div>
    <div class="ticker" id="ticker">
      <div class="stack-inner" id="stack-inner">
        <!-- 每项对应 ticker 滚动经过的一个状态。
             示例文件列出了具体标签；对于规则，将其视为位置槽位（{item0} … {itemN}）。 -->
        <div class="item">{item0}</div>
        <div class="item">{item1}</div>
        <div class="item">{item2}</div>
        <div class="item">{item3}</div>
        <div class="item">{itemN}</div>
      </div>
    </div>
    <div class="brand">{footerLine}</div>
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
  font-family: {font};
}
.stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: STACK_GAP;
}
.eyebrow {
  font-size: EYEBROW_FONT_SIZE;
  font-weight: 800;
  letter-spacing: 14px;
  text-transform: uppercase;
  color: {accentColor};
}
/* 必须：容器高度精确匹配每项高度 */
.ticker {
  width: TICKER_WIDTH;
  height: ITEM_HEIGHT;       /* 必须匹配 .item 高度 */
  overflow: hidden;
  border-top: 2px solid {dividerColor};
  border-bottom: 2px solid {dividerColor};
  position: relative;
}
.stack-inner {
  display: flex;
  flex-direction: column;    /* 垂直 ticker 必须 */
  will-change: transform;
}
.item {
  height: ITEM_HEIGHT;       /* 必须等于 .ticker 高度 */
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: ITEM_FONT_SIZE;
  font-weight: 900;
  letter-spacing: 8px;
  text-transform: uppercase;
  color: {textColor};
  /* font-variant-numeric: tabular-nums; — 用于数字 ticker */
}
.brand {
  font-size: BRAND_FONT_SIZE;
  font-weight: 800;
  letter-spacing: 10px;
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

  const innerEl = document.getElementById("stack-inner");

  // 每个弹簧对象持有一个 0→1 进度；它们累加成一个步进计数器。
  // 总和 * -ITEM_HEIGHT 成为 translateY。
  const springs = Array.from({ length: STEPS }, () => ({ p: 0 }));

  function applyTransform() {
    const sumP = springs.reduce((acc, s) => acc + s.p, 0);
    innerEl.style.transform = `translateY(${-sumP * ITEM_HEIGHT}px)`;
  }
  applyTransform(); // 初始状态

  // 顺序触发每个弹簧，带重叠 — 每个快照一步
  springs.forEach((spring, i) => {
    tl.to(
      spring,
      {
        p: 1,
        duration: STEP_DUR,
        ease: `back.out(${BOUNCE_FACTOR})`,
        onUpdate: applyTransform,
      },
      STEP_START + i * STEP_SPACING,
    );
  });

  // ticker 在最终项上稳定后页脚揭示。
  tl.from(
    ".brand",
    { opacity: 0, y: BRAND_Y, duration: BRAND_FADE_DUR, ease: "power3.out" },
    STEP_START + STEPS * STEP_SPACING + BRAND_DELAY,
  );

  window.__timelines["ticker-scene"] = tl;
</script>
```

## 如何选择值

- **ITEM_HEIGHT** — 每个 ticker 槽位的 px 高度以及遮罩窗口的高度。
  - 范围：~`ITEM_FONT_SIZE × 1.25`；行必须容纳大写下行字母而不裁剪
  - 约束：**`.ticker` 高度必须精确等于 `.item` 高度** — 不匹配的值会导致部分项目在遮罩上方/下方露出
  - 参考：../../examples/proof-logo-chain.html 使用 `204px`
- **TICKER_WIDTH** — 遮罩窗口的 px 宽度。
  - 范围：足够宽以容纳最长项目而不省略号；通常为视口宽度的 30-60%
- **STEPS** — 累加弹簧的数量（状态转换次数，而非项目数）。
  - 范围：通常 1-4；每一步 = 老虎机节奏中的一个"咔嗒"
  - 约束：`STEPS ≤ itemCount − 1`（你只能滚到可见项目下方有多少项目）
  - 参考：../../examples/proof-logo-chain.html 使用 `1`（两个状态间单次滚动）
- **STEP_DUR** — 每个弹簧补间的时长。
  - 范围：0.3-0.7 秒；低于 0.3 秒过冲不可见，高于 0.7 秒咔嗒读作滑动
  - 参考：../../examples/proof-logo-chain.html 使用 `0.45s`
- **STEP_SPACING** — 连续弹簧开始时间之间的秒数。
  - 范围：0.3-0.5 秒；更近则步骤模糊在一起（看起来像线性滚动），更远则 ticker 感觉懒散
  - 约束：`STEP_SPACING ≤ STEP_DUR` 使前一步在下一步触发时仍在稳定（这就是使它们"累加"的原因）
- **STEP_START** — 第一个弹簧触发的时间。
  - 范围：0+；在前置节拍后门控
- **BOUNCE_FACTOR** — 每步 `back.out(BOUNCE_FACTOR)` 过冲强度。
  - 范围：1.4（轻柔咔嗒）→ 2.0（坚定咔嗒）→ 2.5+（卡通式旋转着陆用于高潮步）
  - 效果：低端读作精致 UI，高端读作赌场/游戏节目
- **BRAND_DELAY** — 最后一步后到页脚行揭示的间隔秒数。
  - 范围：0.2-0.5 秒；让最终过冲稳定后再让下一个元素竞争注意力
- **BRAND_FADE_DUR** — 页脚淡入时长。
  - 范围：0.4-0.7 秒
- **BRAND_Y** — 页脚淡入前的初始垂直偏移（以 px 为单位）。
  - 范围：8-24 px；更大感觉"冲击"，更小感觉柔和
- **EYEBROW_FONT_SIZE / ITEM_FONT_SIZE / BRAND_FONT_SIZE / STACK_GAP** — 排版 + 布局缩放。
  - 约束：项目是焦点节拍，尺寸比眉标/页脚大 4-8×
- **{bgColor} / {accentColor} / {textColor} / {dividerColor}** — 语义颜色标记；重音保留给眉标和页脚，使 ticker 项目保持中性。
- **{font}** — 基础排版栈。对于数字 ticker，添加 `font-variant-numeric: tabular-nums` 使数字宽度保持不变。

## 变体

### 数字 ticker（价格/计数器滚动）

用数字序列替换文本项目，并在每个十进制位置（个位、十位、百位…）使用相同的弹簧步进模式。添加 `font-variant-numeric: tabular-nums` 保证数字宽度稳定性。

### 反向方向（倒数）

交换平移符号：`transform: translateY(${sumP * ITEM_HEIGHT}px)` 并按相反顺序排列项目。读作倒数。

### 连续无限 ticker（无稳定）

永远循环（例如新闻 ticker）— 在单个长补间上使用线性缓动，复制项目列表，当平移超过总高度时重置。**不是**此规则 — 参见 [sine-wave-loop](sine-wave-loop.md) 模式用于连续运动，而此规则是离散步进语义。

### 组间暂停

为了戏剧性的"旋转然后着陆"感觉，分组几个快速弹簧步进（`STEP_SPACING` 小）+ 一个 `BRAND_DELAY` 风格长暂停 + 一个具有更大 `BOUNCE_FACTOR` 的最终戏剧性步进。暂停是眼睛锁定的地方。

## 关键原则

- **容器高度必须等于项目高度** — 否则项目不会干净地快照进入可见窗口。如果容器是 200px 而项目是 220px，每一步都会在可见区域上方/下方显示部分项目边缘。
- **容器的 `overflow: hidden`，不是内部堆栈的** — 遮罩是窗口；内部的堆栈可以自由向下延伸。
- **内部堆栈上的 `flex-direction: column`** — 垂直堆叠必需；行会使项目水平排列。
- **步进间距比步进时长更紧** — 重叠是使弹簧累加并产生"咔嗒咔嗒"节奏的关键；非重叠步进读作线性滚动。
- **每步 `back.out`** — 过冲是使每步感觉像"咔嗒"的关键。线性缓动或仅出缓动会丢失老虎机感觉。
- **在 onUpdate 中累加弹簧，不要直接补间最终位置** — 这是"累加"技巧；每个弹簧贡献自己的快照，这就是老虎机的节奏。
- **❗ 不要在步进之间通过 `innerHTML` 更新项目** — ticker 通过平移移动**相同**项目；替换内容会使前一个项目在**新项目**出现时仍然可见（破碎的幻觉）。
- **❗ 最终步后高潮停留 ≥1 秒** — 参见 SKILL 通用约束。

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **stack-inner 上无 CSS `transition`** — 与累加变换竞争
- **stack-inner 上设置 `will-change: transform`** — 每秒许多小变换更新
- **所有项目相同高度（像素精确）** — 不匹配的高度会导致累积漂移
- **对于数字：`font-variant-numeric: tabular-nums`** — 可变数字宽度破坏对齐

## 组合

- [reactive-displacement.md](reactive-displacement.md) — ticker 被进入的元素"推动"
- [scale-swap-transition.md](scale-swap-transition.md) — ticker 在稳定到最终状态后缩放退出，缩放的副标题替换它
- [press-release-spring.md](press-release-spring.md) — 按钮按下**触发** ticker 旋转

## 与 HF 技能配对

- `/hyperframes-animation` — 通过共享 onUpdate 的累加弹簧补间
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
