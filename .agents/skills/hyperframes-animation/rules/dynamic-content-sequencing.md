---
name: dynamic-content-sequencing
description: 从内容长度 + 每项时长配置自动计算时间线开始/结束时间 — 更长的内容获得更多屏幕时间，无需硬编码数字。
metadata:
  tags: timeline, sequencing, dynamic, duration, content-aware, utility
---

# 动态内容排序

一个实用模式（本身不是动效规则），用于显示一系列项目（卡片、短语、统计）的场景。每个项目的时长从其内容长度 + 逐项配置计算；排序器自动分配绝对开始/结束时间。与 [discrete-text-sequence](discrete-text-sequence.md)**不同**（后者是一个文本元素改变状态）— 此规则在离散内容块之间交换。

## 工作原理

1. 定义内容数组 — 每个条目有 `{ text, speedFactor, hold }`（或任意字段）
2. 预计算绝对开始时间：`start[i] = sum of durations 0..i-1`
3. 在 onUpdate 中，找到哪个条目是活动的（最后一个其 `start ≤ time` 的条目）并渲染它

"动态"部分：文本较长的项目获得更多屏幕时间（公式：`baseDuration + textLength * msPerChar`）。无硬编码的 `from` / `durationInFrames` 每项。

## HTML

```html
<div
  class="scene"
  id="seq-scene"
  data-composition-id="seq-scene"
  data-start="0"
  data-duration="{DURATION}"
  data-track-index="0"
>
  <div class="display">
    <div class="eyebrow" id="eyebrow">{eyebrow}</div>
    <div class="title" id="title"></div>
    <div class="body" id="body"></div>
    <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
  </div>
  <div class="brand">— {Brand}</div>
</div>
```

## CSS

占位符：`{font}` 是项目无衬线栈；`{bgColor1}`/`{bgColor2}` 制作暗背景渐变；`{accentColor}` 高亮眉标/品牌/进度填充；`{textColor}` 是主要可读前景。

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: radial-gradient(ellipse at center, {bgColor1} 0%, {bgColor2} 70%);
  font-family: {font};
}
.display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  text-align: center;
  max-width: 1400px;
}
.eyebrow {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: 14px;
  color: {accentColor};
  text-transform: uppercase;
}
.title {
  font-size: 120px;
  font-weight: 900;
  letter-spacing: -2px;
  line-height: 1;
  color: {textColor};
}
.body {
  font-size: 48px;
  font-weight: 500;
  line-height: 1.4;
  color: {accentColor};
  opacity: 0.9;
  min-height: 160px; /* 保留空间使布局不跳变 */
}
.progress-bar {
  width: 600px;
  height: 4px;
  background: {accentColor}26; /* ~15% 不透明度 */
  border-radius: 2px;
  margin-top: 16px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, {accentColor} 0%, {accentColor2} 100%);
  width: 0%;
}
.brand {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 32px;
  font-weight: 900;
  letter-spacing: 12px;
  color: {accentColor};
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 内容数组 — N 个条目，每个有自己的节奏配置。
  // 形状：短眉标标签、短标题、较长正文句子，加上每项节奏。
  // 最后一个条目通常使用更大的 `hold`（结束节拍）。
  const CONTENT = [
    {
      eyebrow: "{eyebrow1}",
      title: "{title1}",
      body: "{body1}",
      speedFactor: SPEED_FACTOR,
      hold: HOLD_MID,
    },
    {
      eyebrow: "{eyebrow2}",
      title: "{title2}",
      body: "{body2}",
      speedFactor: SPEED_FACTOR,
      hold: HOLD_MID,
    },
    // …
    {
      eyebrow: "{eyebrowN}",
      title: "{titleN}",
      body: "{bodyN}",
      speedFactor: SPEED_FACTOR,
      hold: HOLD_FINAL,
    },
  ];

  // 预计算绝对开始时间。
  // 每项时长：BASE_DURATION + body.length * SEC_PER_CHAR + entry.hold 秒。
  // BASE_DURATION、SEC_PER_CHAR 在"如何选择值"中有文档。
  let cumulative = 0;
  const TIMELINE = CONTENT.map((entry) => {
    const dur = BASE_DURATION + entry.body.length * SEC_PER_CHAR + entry.hold;
    const start = cumulative;
    cumulative += dur;
    return { ...entry, start, end: cumulative };
  });

  // 反向搜索当前条目
  function entryAt(time) {
    for (let i = TIMELINE.length - 1; i >= 0; i--) {
      if (time >= TIMELINE[i].start) return TIMELINE[i];
    }
    return TIMELINE[0];
  }

  const eyebrowEl = document.getElementById("eyebrow");
  const titleEl = document.getElementById("title");
  const bodyEl = document.getElementById("body");
  const progressEl = document.getElementById("progress-fill");

  const TOTAL_DURATION = cumulative + TAIL_PAD;
  const driver = { t: 0 };
  let lastTitle = "";

  tl.to(
    driver,
    {
      t: TOTAL_DURATION,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        const entry = entryAt(driver.t);
        // 仅在过渡时交换内容（避免每帧 DOM 抖动）
        if (entry.title !== lastTitle) {
          eyebrowEl.textContent = entry.eyebrow;
          titleEl.textContent = entry.title;
          bodyEl.textContent = entry.body;
          lastTitle = entry.title;
        }
        // 进度条填充 0% → 100% 随组合推进
        progressEl.style.width = `${(driver.t / TOTAL_DURATION) * 100}%`;
      },
    },
    0,
  );

  window.__timelines["seq-scene"] = tl;
</script>
```

## 变体

### 项目间交叉淡入淡出（非硬切）

向查找函数添加 `overlap` — 在重叠窗口期间返回前一个和下一个条目，以交叉淡入淡出不透明度渲染：

```js
function activeEntries(time, overlap = 0.3) {
  const result = [];
  TIMELINE.forEach((e) => {
    if (time >= e.start - overlap && time <= e.end + overlap) result.push(e);
  });
  return result;
}
```

然后基于与边界的距离用计算的不透明度渲染两个相邻条目。

### 每项运动变化

每个条目有自己的运动风格。将 `entry.style` 映射到现有规则之一：第 1 章使用 [3d-text-depth-layers](3d-text-depth-layers.md)，第 2 章使用 [hacker-flip-3d](hacker-flip-3d.md)，第 3 章使用 [counting-dynamic-scale](counting-dynamic-scale.md)。排序器仅编排时间；逐项渲染使用适当的规则。

### 自动延长组合时长

如果你事先不知道序列有多长（动态内容数量），将 `data-duration` 绑定到计算出的 `TOTAL_DURATION`。在时间线注册**之前**在脚本中执行此操作：

```js
document
  .querySelector("[data-composition-id]")
  .setAttribute("data-duration", String(Math.ceil(TOTAL_DURATION)));
```

（注意：HF 在组合加载时读取 `data-duration`；在 init 后设置可能不会生效 — 基于粗略的总时间计算手动编写时长。）

## 关键原则

- **预计算时间线一次，而非每帧** — 在脚本 init 时构建绝对开始/结束意味着 onUpdate 是 O(log n) 反向搜索，而非 O(n²)。
- **每项时长公式：`BASE_DURATION + body.length × SEC_PER_CHAR + hold`** — 更长的文本需要更多的阅读时间。此公式是本规则的承载教学；每个 const 的范围在"如何选择值"中。
- **在 body 元素上保留 `min-height`** — 内容高度每项不同；没有保留，布局跳变且下游元素（进度条、品牌）抖动。
- **仅在过渡时更新 DOM，而非每帧** — 跟踪 `lastTitle`（或任何键）仅在其变化时调用 `textContent =`。每帧 textContent 赋值在 HF 渲染中导致闪烁。
- **可选进度指示器** — 底部显示 0-100% 的细条完成了"这是一个序列"的框架。
- **高潮停留比序列中段停留更长** — 结尾的 `hold`（HOLD_FINAL）应超过序列中的 `hold`（HOLD_MID），使最终品牌/CTA 着陆。

## 如何选择值

- **BASE_DURATION** — 无论内容长度如何，条目的最小可见时间
  - 范围：0.6-1.5 秒
  - 效果：低端使短条目快速闪过，眼睛来不及看；高端使短标题上停滞
  - 约束：确保即使一个词的条目也有时间阅读
  - 参考：参见 `../../examples/messaging-multi-phrase.html`（以及任何使用此规则的蓝图）
- **SEC_PER_CHAR** — 每个正文字符添加的额外时间
  - 范围：0.03-0.06 秒/字符（≈ 视频阅读速度 17-33 字符/秒）
  - 效果：低端感觉段落式正文急促；高端在正文短时感觉慢
  - 约束：应在整个序列中保持一致，使节奏读作一个引擎；对于字符较宽的语言，偏向高端
  - 参考：参见 `../../examples/messaging-multi-phrase.html`（以及任何使用此规则的蓝图）
- **HOLD_MID** — 非最终条目的打字完成后的停留
  - 范围：0.5-1.0 秒
  - 效果：低端感觉匆忙；高端感觉懒散
  - 约束：`HOLD_MID < HOLD_FINAL`
  - 参考：参见 `../../examples/messaging-multi-phrase.html`（以及任何使用此规则的蓝图）
- **HOLD_FINAL** — 最后一个条目上的停留（结尾/高潮）
  - 范围：1.0-2.0 秒
  - 效果：低端截断结束节拍；高端停留过久
  - 约束：必须明显超过 HOLD_MID，使结尾读作一个节拍，而非另一个序列中段暂停
  - 参考：参见 `../../examples/messaging-multi-phrase.html`（以及任何使用此规则的蓝图）
- **SPEED_FACTOR** — 每项节奏乘数
  - 范围：0.5-2.0（默认 1.0）
  - 效果：<1 拉伸条目的正文驱动时长（适合高密度段落）；>1 压缩它
  - 约束：离散选择 — 使用 1.0，除非一个条目需要特殊节奏；如果每个条目使用相同因子，改为将其合并到 SEC_PER_CHAR 中
  - 参考：参见 `../../examples/messaging-multi-phrase.html`（以及任何使用此规则的蓝图）
- **TAIL_PAD** — 最后一个条目的 `end` 后添加到 `TOTAL_DURATION` 的秒数
  - 范围：0.0-1.0 秒
  - 效果：0 在最后 `hold` 完成时精确结束驱动器；>0 留下一个安静节拍（在过渡到下一个组合前有用）
  - 约束：如果下游是另一个组合，优先使用 0 并在组合接缝处处理呼吸
  - 参考：参见 `../../examples/messaging-multi-phrase.html`（以及任何使用此规则的蓝图）
- **CONTENT 长度（N）** — 序列中条目数
  - 范围：3-6 个条目
  - 效果：<3 不是序列（使用静态场景）；>6 拖沓
  - 约束：每个条目的 `title` 必须适合一行，使用所选 `.title` 字号；正文应在折行后适应 `min-height`
  - 参考：参见 `../../examples/messaging-multi-phrase.html`（以及任何使用此规则的蓝图）

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **预计算 TIMELINE 数组** — 不要在 onUpdate 中重新计算
- **body 上设置 `min-height`** 用于布局稳定性
- **仅在条目过渡时交换 DOM** — 使用 lastTitle/lastKey 守护
- **仅顺序** — 对于并行轨道，使用不同的归约（此规则是顺序的）

## 组合

- [discrete-text-sequence.md](discrete-text-sequence.md) — body 上的每项打字机
- [context-sensitive-cursor.md](context-sensitive-cursor.md) — 每章段的光标颜色
- [vertical-spring-ticker.md](vertical-spring-ticker.md) — 项目之间的动画单词过渡（而非硬切）
- [scale-swap-transition.md](scale-swap-transition.md) — 条目之间的视觉变形

## 与 HF 技能配对

- `/hyperframes-animation` — 单一驱动器，反向搜索分派
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
