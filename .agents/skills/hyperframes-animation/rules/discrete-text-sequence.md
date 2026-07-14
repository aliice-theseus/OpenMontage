---
name: discrete-text-sequence
description: 在帧阈值处替换完整的文本状态，实现非线性打字效果 — 输入错误、批量添加、暂停、退格、模拟思考。
metadata:
  tags: text, typing, discrete, threshold, non-linear, sequence
---

# 离散文本序列

非逐字打字机，而是在时间阈值处替换完整字符串状态。实现平滑逐字打字无法实现的非线性效果（输入错误、批量添加、暂停、"思考"间隙）。

## 工作原理

一个 `{ text, t }` 对的数组，其中 `t` 是以秒为单位的时间。在每个 onUpdate 上，扫描数组找到其 `t` 已通过的最新条目并渲染该文本。显示在状态之间跳转；它们之间没有动画。

对于连续逐字打字机（无暂停、无编辑），使用底部的**平滑切片**变体。

## HTML

```html
<div
  class="scene"
  id="seq-scene"
  data-composition-id="seq-scene"
  data-start="0"
  data-duration="6"
  data-track-index="0"
>
  <div class="terminal">
    <div class="prompt">$</div>
    <div class="text-wrap">
      <span class="text" id="text">|</span>
      <span class="cursor" id="cursor">_</span>
    </div>
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
  font-family: {monoFont}; /* 等宽字体是必需的 — 参见关键约束 */
}
.terminal {
  display: flex;
  align-items: baseline;
  gap: GUTTER;
  font-weight: 800;
  font-size: TERMINAL_FONT_SIZE;
  color: {textColor};
}
.prompt {
  color: {accentColor};
}
.text-wrap {
  display: inline-flex;
  align-items: baseline;
  /* 固定宽度容器防止内容长度变化时右侧抖动。
     选择宽度 ≥ 最长状态的宽度。 */
  min-width: TEXT_WRAP_MIN_WIDTH;
  white-space: nowrap;
}
.text {
  color: {textColor};
}
.cursor {
  display: inline-block;
  width: CURSOR_WIDTH;
  color: {accentColor};
  margin-left: CURSOR_GAP;
}
```

## GSAP 时间线 + 离散状态逻辑

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};

  // SEQUENCE — 每个条目从 t 显示到下一个条目的 t。
  // 非线性：输入错误、修正、批量添加、暂停。
  // 形状（一种实现）：
  //   [热身击键] → [输入错误] → [退格回到分叉点] →
  //   [批量粘贴修正后的续写] → [完成标记]
  const SEQUENCE = [
    { t: 0.0, text: "" },
    { t: T_K1, text: "{p1}" }, // 首次击键（~3-5 字符，0.1-0.2s 间隔）
    { t: T_K2, text: "{p1 + ' ' + p2_typo}" }, // 包含输入错误的续写
    { t: T_BS, text: "{p1 + ' ' + p2_partial}" }, // 退格 — 返回到分叉点
    { t: T_BULK, text: "{fullCorrectedText}" }, // 批量粘贴 — 一次替换多个字符
    { t: T_DONE, text: "{fullCorrectedText + ' ✓'}" }, // 完成标记
  ];

  // 反向搜索其 t 已通过的最新条目。
  function textAt(time) {
    for (let i = SEQUENCE.length - 1; i >= 0; i--) {
      if (time >= SEQUENCE[i].t) return SEQUENCE[i].text;
    }
    return "";
  }

  const textEl = document.getElementById("text");
  const cursorEl = document.getElementById("cursor");
  const tl = gsap.timeline({ paused: true });

  // 通过 0→TOTAL_DURATION 补间的 onUpdate 驱动离散显示
  const driver = { t: 0 };
  tl.to(
    driver,
    {
      t: TOTAL_DURATION,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        textEl.textContent = textAt(driver.t);
      },
    },
    0,
  );

  // 光标闪烁 — 通过 sin 确定性驱动，非 CSS 动画
  const blinkDriver = { p: 0 };
  tl.to(
    blinkDriver,
    {
      p: Math.PI * 2 * BLINK_CYCLES, // BLINK_CYCLES = 跨组合闪烁次数
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        cursorEl.style.opacity = Math.sin(blinkDriver.p) > 0 ? "1" : "0";
      },
    },
    0,
  );

  window.__timelines["seq-scene"] = tl;
</script>
```

## 变体

### 平滑字符切片（连续打字机 — 无暂停，无编辑）

对于直接的打字机，无非线性混乱：

```js
const fullText = "{fullPhrase}";
const len = { v: 0 };
tl.to(
  len,
  {
    v: fullText.length,
    duration: TYPE_DUR,
    ease: "power1.inOut",
    onUpdate: () => {
      textEl.textContent = fullText.substring(0, Math.floor(len.v));
    },
  },
  0,
);
```

这编写更快，但产生均匀的"机器打字"感觉 — 缺少真人打字真实感。

### 思考暂停（在关键状态上延长保持）

插入一个状态，在 `THINK_HOLD_DUR` 秒内保持不变 — 感觉像用户停下来思考：

```js
{ t: T_PRE_PAUSE, text: '{partialPhrase}' },        // 暂停前的最后状态
// ... 无条目持续 THINK_HOLD_DUR 秒 ...
{ t: T_PRE_PAUSE + THINK_HOLD_DUR, text: '{resumedPhrase}' },
```

### 完成时状态脉冲

当最终状态着陆时（例如"✓"），为强调短暂脉冲缩放行：

```js
tl.to(
  ".text",
  { scale: COMPLETION_PULSE_SCALE, duration: COMPLETION_PULSE_DUR, yoyo: true, repeat: 1 },
  T_DONE,
);
```

### 每状态颜色偏移

按阶段对状态进行颜色编码（例如编辑期间变暗，完成标记后成功色，可选输入错误时警告色）：

```js
// 在 onUpdate 中设置 textContent 后：
if (driver.t > T_DONE) textEl.style.color = "{successColor}";
else if (driver.t < T_K2)
  textEl.style.color = "{textColor}"; // 正常打字
else textEl.style.color = "{mutedColor}"; // 编辑中变暗
```

## 如何选择值

### 布局

- **TERMINAL_FONT_SIZE** — 打字行的字体大小。
  - 范围：全出血组合 48-96 px；终端风格细节较小
  - 约束：与 `TEXT_WRAP_MIN_WIDTH` 组合必须适应视口
- **TEXT_WRAP_MIN_WIDTH** — 持有文本的固定宽度容器。
  - 约束：必须 `≥ widthOf(longest SEQUENCE state) at TERMINAL_FONT_SIZE`。如果不确定，在 `document.fonts.ready` 后用隐藏探针测量
  - 效果：太小 → 右侧随状态长度变化抖动；太大 → 未使用的水平空白填充组合
- **GUTTER** — 提示字形（`$`、`>`）和文本之间的 flex 间距。
  - 范围：~0.3-0.5× `TERMINAL_FONT_SIZE`
- **CURSOR_WIDTH / CURSOR_GAP** — 块状光标尺寸。
  - 范围：宽度 ~0.3× `TERMINAL_FONT_SIZE`；间隙小（个位数 px）使光标感觉与文本相连

### 序列时间

- **TOTAL_DURATION** — 组合长度。
  - 约束：必须 ≥ `T_DONE` + ~1 秒高潮停留，使观看者看到完成标记
- **T_K1 / T_K2 / T_BS / T_BULK / T_DONE** — SEQUENCE 中的里程碑时间戳。
  - 范围："真人打字"击键间隔 0.06-0.20 秒；自然词间断暂停 0.3-0.6 秒；批量粘贴在一个条目中跳过多字符
  - 约束：单调递增；`T_DONE ≤ TOTAL_DURATION - dwell`
- **TYPE_DUR**（平滑切片变体）— 连续打字机的总打字时长。
  - 范围：`chars × 0.06s`（快）到 `chars × 0.12s`（放松）
- **THINK_HOLD_DUR**（思考暂停变体）— 两个 SEQUENCE 状态之间的保持时间。
  - 范围：0.8-2.0 秒；低于 0.5 秒读作口吃而非思考
- **COMPLETION_PULSE_SCALE / COMPLETION_PULSE_DUR**（脉冲变体）。
  - 范围：缩放 1.03-1.08（微妙），时长 0.15-0.30 秒

### 光标

- **BLINK_CYCLES** — 在 `TOTAL_DURATION` 内的完整闪烁周期数。
  - 范围：`TOTAL_DURATION / 0.8s ≤ BLINK_CYCLES ≤ TOTAL_DURATION / 0.5s`（每 0.5-0.8 秒周期读作自然光标）

### 颜色标记

- **{bgColor} / {textColor} / {accentColor} / {successColor} / {mutedColor}** — 离散选择，非数值范围。从组合调色板选择；提示 + 光标共享 `{accentColor}`，使它们读作相同的"系统"元素。

## 关键原则

- **阈值序列驱动真实感** — 分组快速连续击键（0.1-0.2 秒间隔），然后在词断处暂停（0.3-0.5 秒），单次跳转批量粘贴（一个条目替换多个字符），包括一两个输入错误以获得真人打字感觉
- **每帧反向搜索数组** — 每帧 O(n)，其中 n 小（通常 ≤30）。不要尝试按帧索引；序列是稀疏的
- **固定宽度容器是强制的** — 没有 `min-width`，文本包裹的右侧随状态长度变化抖动。设置宽度 ≥ 最长预期状态
- **光标必须是确定性的** — 基于 sin 或序列驱动的闪烁，而非 CSS 动画。HF 逐帧定位；CSS 动画会不同步
- **文本元素上无 `transition`** — 离散跳转应该是**即时的**。CSS 过渡会将跳转变成拖影，破坏"打字"感觉
- **❗ 区分离散与平滑** — 如果你的效果是"逐个键入字符，无编辑" → 使用平滑切片变体。离散序列对于那种情况过于复杂。仅在需要非线性状态时（输入错误、暂停、批量粘贴）使用离散

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **文本或其任何父级上无 CSS `transition`**
- **光标 `display: inline-block`** — `display: inline` 忽略宽度/变换
- **终端风格效果使用等宽字体** — 即使有固定宽度容器，比例字体也会导致视觉抖动
- **文本包裹上 `whitespace: nowrap`** — 中间状态折行破坏幻觉

## 组合

- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 带分层深度的离散文本渲染（厚重、戏剧性）
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 标签的离散文本，同时计数器平滑动画化
- [press-release-spring.md](press-release-spring.md) — 序列完成后，该行像确认成功的按钮一样"按下"

## 与 HF 技能配对

- `/hyperframes-animation` — onUpdate 驱动的离散状态查找
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
