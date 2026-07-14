---
name: scale-swap-transition
description: 两个元素之间协调的缩小退出 + 弹簧弹入变形过渡 — 无需 SVG 路径插值。
metadata:
  tags: transition, morph, scale, swap, spring, pop
---

# 缩放交换过渡

通过重叠退出和进入缩放动画来模拟两个 DOM 元素之间的"变形"。比 [card-morph-anchor](card-morph-anchor.md)（变形容器尺寸）更轻量，比 SVG 路径插值更简单。

## 工作原理

在单个触发时间，两个协调的补间触发：

1. **退出元素**：缩放 `1.0 → EXIT_SCALE` + 不透明度 `1 → 0`（快速 `power2.in`）
2. **进入元素**：缩放 `EXIT_SCALE → 1.0` + 不透明度 `0 → 1`（带过冲的弹跳 `back.out(${BOUNCE_FACTOR})`）

一个小的 `OVERLAP` 窗口，在此期间两者都处于补间中间，创造了"变形"错觉。进入元素通过 z-index 位于顶部，使退出元素的淡出尾部不渗透过来。

## HTML

```html
<div
  class="scene"
  id="swap-scene"
  data-composition-id="swap-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="stack">
    <div class="swap-wrap">
      <div class="card outgoing" id="outgoing">
        <div class="icon">{outgoingIcon}</div>
        <div class="title">{outgoingLabel}</div>
      </div>
      <div class="card incoming" id="incoming">
        <div class="icon">{incomingIcon}</div>
        <div class="title">{incomingLabel}</div>
        <div class="sub" id="sub">{incomingSubline}</div>
      </div>
    </div>
    <div class="brand">{Brand}</div>
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
}
.stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: STACK_GAP;
}
.swap-wrap {
  position: relative;
  width: SWAP_WRAP_W;
  height: SWAP_WRAP_H;
}
.card {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: CARD_INNER_GAP;
  border-radius: CARD_RADIUS;
  padding: CARD_PADDING;
  /* 两个元素共享 transform-origin，使它们围绕同一锚点"变形" */
  transform-origin: 50% 50%;
  will-change: transform, opacity;
}
.card .icon {
  font-size: ICON_SIZE;
}
.card .title {
  font-size: TITLE_SIZE;
  font-weight: 900;
  letter-spacing: TITLE_TRACKING;
  text-transform: uppercase;
}
.card .sub {
  font-size: SUB_SIZE;
  font-weight: 700;
  color: {accentColor};
  opacity: 0;
}
.outgoing {
  z-index: 1;
  background: {outgoingBg};
  border: 1px solid {outgoingBorder};
  color: {textColor};
}
.incoming {
  /* 进入元素开始时隐藏 + 较小，将弹入 */
  z-index: 2;
  background: {incomingBg};
  border: 1px solid {incomingBorder};
  color: {textColor};
  opacity: 0;
  transform: scale(EXIT_SCALE);
}
.brand {
  font-size: BRAND_SIZE;
  font-weight: 900;
  letter-spacing: BRAND_TRACKING;
  text-transform: uppercase;
  color: {brandColor};
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 退出：快速缩小 + 淡出
  tl.to(
    "#outgoing",
    {
      scale: EXIT_SCALE,
      opacity: 0,
      duration: EXIT_DUR,
      ease: "power2.in",
    },
    TRIGGER,
  );

  // 进入：带过冲放大 + 淡入，在退出完成前稍早开始
  //（OVERLAP 创建变形错觉）。
  tl.to(
    "#incoming",
    {
      scale: 1.0,
      opacity: 1,
      duration: ENTER_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`,
    },
    TRIGGER + EXIT_DUR - OVERLAP,
  );

  // 副标题在进入卡片稳定后揭示
  tl.fromTo(
    "#sub",
    { opacity: 0, y: SUB_REVEAL_Y_PX },
    { opacity: 1, y: 0, duration: SUB_REVEAL_DUR, ease: "power3.out" },
    TRIGGER + EXIT_DUR + SUB_REVEAL_DELAY,
  );

  // 品牌提前淡入以设置上下文
  tl.from(
    ".brand",
    { opacity: 0, y: BRAND_REVEAL_Y_PX, duration: BRAND_REVEAL_DUR, ease: "power3.out" },
    BRAND_REVEAL_AT,
  );

  window.__timelines["swap-scene"] = tl;
</script>
```

## 变体

### 延迟内部内容揭示

经典模式：变形容器，然后在容器稳定后揭示内部文本（如上面 `.sub` 示例）。变形结束和内容揭示之间的 0.2-0.4 秒间隔让观看者眼睛在阅读内容之前着陆在新容器形状上。

### 三次交换（3 状态循环）

链式：A→B→C，两个触发点 `TRIGGER_AB` 和 `TRIGGER_BC`。每个转换需要自己的补间对，且之前的进入成为下一个退出。适用于状态演变叙事（例如早期状态 → 中期状态 → 最终状态标签）。

```js
tl.to("#stateA", { scale: EXIT_SCALE, opacity: 0, duration: EXIT_DUR }, TRIGGER_AB);
tl.to(
  "#stateB",
  { scale: 1.0, opacity: 1, duration: ENTER_DUR, ease: `back.out(${BOUNCE_FACTOR})` },
  TRIGGER_AB + EXIT_DUR - OVERLAP,
);
tl.to("#stateB", { scale: EXIT_SCALE, opacity: 0, duration: EXIT_DUR }, TRIGGER_BC);
tl.to(
  "#stateC",
  { scale: 1.0, opacity: 1, duration: ENTER_DUR, ease: `back.out(${BOUNCE_FACTOR})` },
  TRIGGER_BC + EXIT_DUR - OVERLAP,
);
```

### 颜色偏移过渡（无缩放）

对于两个相同形状状态之间的平面变形，去掉缩放，仅保持不透明度 + 简短背景色调补间。戏剧性较小，但更匹配产品 UI 基调。

## 如何选择值

### 时间（秒）

- **TRIGGER** — 交换触发时间。
  - 约束：必须 ≥ 退出元素的稳定时间 + 存在停留，使退出在变换前"着陆"
- **EXIT_DUR** — 退出缩小 + 淡出时长。
  - 范围：0.3-0.5 秒
- **ENTER_DUR** — 进入弹入时长。
  - 范围：0.45-0.7 秒（比 `EXIT_DUR` 长，让过冲稳定）
- **OVERLAP** — 进入在退出完成前提前开始的量。
  - 范围：0.1-0.2 秒
  - 约束：太多（>0.3 秒）使两者同时清晰可见（无变形）；太少（<0.05 秒）留下可见的空隙
- **SUB_REVEAL_DELAY** — 进入稳定和副标题揭示之间的间隔。
  - 范围：0.2-0.4 秒；变形期间的揭示与交换竞争注意力
- **SUB_REVEAL_DUR** — 副标题淡入。
  - 范围：0.3-0.5 秒
- **BRAND_REVEAL_AT** — 品牌/上下文行淡入时间。
  - 约束：必须 < `TRIGGER`（品牌是交换的上下文，不与交换同步）
- **BRAND_REVEAL_DUR** — 品牌淡入时长。
  - 范围：0.4-0.8 秒

### 物理

- **EXIT_SCALE** — 退出的目标缩放（和进入的起始缩放）。
  - 范围：0.6-0.8；更小的退出感觉更戏剧性但可能读作"消失"而非"变形"
- **BOUNCE_FACTOR** — 进入上的 `back.out(${BOUNCE_FACTOR})` 过冲。
  - 范围：1.4（柔和）- 1.8（坚定）- 2.2（卡通）

### 定位偏移

- **SUB_REVEAL_Y_PX** — 副标题初始 y 偏移（正 = 休息位置下方）。
  - 范围：8-20 px
- **BRAND_REVEAL_Y_PX** — 品牌初始 y 偏移。
  - 范围：10-24 px

### 布局

- **STACK_GAP** — 交换容器和品牌行之间的间距。
  - 范围：40-96 px
- **SWAP_WRAP_W / SWAP_WRAP_H** — 固定交换容器尺寸；内部两张卡片 `inset: 0`。
  - 约束：选择适合两个状态内容的尺寸；容器在交换期间不调整大小
- **CARD_INNER_GAP** — 卡片内图标和标题之间的间距。
  - 范围：16-32 px
- **CARD_RADIUS / CARD_PADDING** — 卡片圆角和内部填充。
  - 范围：radius 24-40 px；padding 32-64 px
- **ICON_SIZE / TITLE_SIZE / SUB_SIZE / BRAND_SIZE** — 排版尺寸。
  - 约束：标题主导（1080p 下 ~80-120 px）；副标题和品牌为重音大小
- **TITLE_TRACKING / BRAND_TRACKING** — 大写标签上的字母间距。
  - 范围：4-16 px（大写配合正跟踪更好）

### 标记

- **{sceneBg}** — 背景渐变/颜色
- **{font}** — 排版栈
- **{textColor}** / **{accentColor}** / **{brandColor}** — 语义颜色标记
- **{outgoingBg}** / **{outgoingBorder}** — 退出卡片表面 + 边框（通常为暖色或动作前色调）
- **{incomingBg}** / **{incomingBorder}** — 进入卡片表面 + 边框（通常为冷色或动作后色调）
- **{outgoingIcon}** / **{incomingIcon}** — 每个状态的单个字形/表情符号
- **{outgoingLabel}** / **{incomingLabel}** — 状态标签
- **{incomingSubline}** — 进入稳定后淡入的支持文案
- **{Brand}** — 交换下方显示的品牌行

## 关键原则

- **进入元素的 z-index 高于退出元素** — 否则退出的淡出尾部（不透明度 0.3-0.5）渗透进入元素的较低不透明度，创建"双重曝光"的模糊帧
- **两个元素共享 `transform-origin: 50% 50%`** — 不同的原点使变形感觉像一个东西传送到了别处
- **`OVERLAP` 在 0.1-0.2 秒窗口内** — 重叠太多两者都清晰可见（无变形）；太少则有可见空隙
- **仅在进入上使用弹跳缓动** — 退出使用 `power2.in`（匆匆离开），进入使用 `back.out(${BOUNCE_FACTOR})`（带着重量到达）。反过来则交换感觉机械
- **内部内容在容器稳定后揭示** — 参见 `SUB_REVEAL_DELAY`。变形期间的揭示竞争注意力且失败
- **最终状态着陆后高潮停留 ≥1 秒** — 参见 SKILL 通用约束。进入 + 副标题都稳定后，保持 ≥1 秒
- **品牌提前揭示，不在交换时** — 上下文（品牌、眉标）设置舞台；交换是标题。如果品牌在交换时揭示，它会竞争

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **两个交换元素上无 CSS `transition`** — 与 GSAP 竞争
- **两个交换元素上设置 `will-change: transform, opacity`**
- **两个元素在同一个包裹容器中使用 `position: absolute; inset: 0`** — 它们占据相同空间，交换淡出一个并弹入一个
- **淡出后不要 `display: none` 退出元素** — 将其保持在 `opacity: 0` 以免布局回流

## 组合

- [press-release-spring.md](press-release-spring.md) — 按钮按**触发**交换（因果）
- [sine-wave-loop.md](sine-wave-loop.md) — 最终状态上的空闲呼吸
- [card-morph-anchor.md](card-morph-anchor.md) — 用于**形状**变化过渡的替代方案（此规则用于**相同形状**状态交换）

## 与 HF 技能配对

- `/hyperframes-animation` — 带重叠的两个协调补间
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
