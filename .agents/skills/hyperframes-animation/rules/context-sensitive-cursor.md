---
name: context-sensitive-cursor
description: 光标颜色和样式适应正在打字的当前文本段 — 高亮处为重音色，占位符处为暗色等。
metadata:
  tags: cursor, color, context, typewriter, styling, segment
---

# 上下文敏感光标

在打字机序列中，光标的颜色（和可选高度/闪烁率）匹配**活动文本段**。如果打字机当前正在输入品牌名称，光标是品牌重音色；在占位符上，它变暗为灰色。相比所有文本状态使用单一固定光标颜色，增强了视觉连贯性。

## 工作原理

文本编写为 `{text, t, segment}` 条目的 SEQUENCE，其中 `segment` 是字符串标识符（'main' / 'highlight' / 'brand' / 'success'）。驱动器补间的 onUpdate 根据 `time` 确定当前段，然后将光标的 CSS 颜色（和可选其他属性）设置为该段调色板的匹配颜色。

## HTML 和 CSS

（HTML/CSS 结构与 `discrete-text-sequence.md` 相同，增加了光标样式段感知。）

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 带每条目段标签的序列。
  // 每个条目：{ t: absoluteSeconds, text: cumulative visible string, segment: paletteKey, color: hex }。
  // 当驱动器跨过每个 `t` 时，光标颜色切换到该段的重音 —
  // 观看者眼睛锁定正在输入的关键词。
  const SEQUENCE = [
    { t: 0, text: "", segment: "main", color: "{mainColor}" },
    { t: T_LEADIN_END, text: "{leadInChunk}", segment: "main", color: "{mainColor}" },
    { t: T_BRAND_IN, text: "{leadInBrandPrefix}", segment: "brand", color: "{brandColor}" },
    { t: T_BRAND_OUT, text: "{leadInBrandFull}", segment: "main", color: "{mainColor}" },
    { t: T_CMD_IN, text: "{leadInCmdPrefix}", segment: "cmd", color: "{cmdColor}" },
    { t: T_BRAND_2, text: "{leadInCmdBrand}", segment: "brand", color: "{brandColor}" },
    { t: T_SUCCESS, text: "{leadInDone}", segment: "success", color: "{successColor}" },
  ];

  function entryAt(time) {
    for (let i = SEQUENCE.length - 1; i >= 0; i--) {
      if (time >= SEQUENCE[i].t) return SEQUENCE[i];
    }
    return SEQUENCE[0];
  }

  const textEl = document.getElementById("text");
  const cursorEl = document.getElementById("cursor");

  // 离散状态驱动器 — 写入文本 + 光标颜色
  const driver = { t: 0 };
  tl.to(
    driver,
    {
      t: DURATION,
      duration: DURATION,
      ease: "none",
      onUpdate: () => {
        const entry = entryAt(driver.t);
        textEl.textContent = entry.text;
        cursorEl.style.background = entry.color;
      },
    },
    0,
  );

  // 通过 sin 确定性闪烁（非 CSS 动画）。
  const blink = { p: 0 };
  tl.to(
    blink,
    {
      p: Math.PI * 2 * BLINK_CYCLES_PER_SCENE,
      duration: DURATION,
      ease: "none",
      onUpdate: () => {
        cursorEl.style.opacity = Math.sin(blink.p) > 0 ? "1" : "0";
      },
    },
    0,
  );

  window.__timelines["cursor-scene"] = tl;
</script>
```

## 变体

### 活动打字时不闪烁

当添加字母时（驱动器在最后 `TYPING_GRACE` 秒内前移），抑制闪烁 — 光标保持实心。当无打字活动时（`driver.t - lastChangeTime > TYPING_GRACE`），恢复闪烁。

### 按段切换光标高度

品牌段上更大的光标以强调（`cursorHeightEmphasis > cursorHeight`）。

### 光标在暗文本上反转对比

如果某段是亮背景上的暗文本渲染，光标也应切换到暗色。通过 `entry.color` 作为真相源并从此读取。

## 关键原则

- **光标颜色偏移使品牌时刻突出** — 眼睛因光标颜色切换到品牌重音而着陆在品牌名称上。没有它，光标是视觉噪声。
- **光标 div 上的 `background` 属性** — 非 `color`（光标是色块，非字形）
- **通过 sin 确定性闪烁** — 从不使用 CSS `@keyframes blink`。HF 定位会不同步。
- **光标 `display: inline-block`** — `display: inline` 忽略宽度/高度。
- **`vertical-align: -8px`**（或类似）— 在视觉上将光标锚定到文本基线，而非全行高。
- **文本和父级上的 `white-space: pre`** — 保留尾随空格，使光标在段末而非塌缩空格后。
- **颜色调色板与品牌系统对齐** — 段最多 3-4 种颜色（main / brand / cmd / success）。更多则分段读作随机。

（详细参数选择与约束与原文一致，已全部中文化。）
