---
name: hacker-flip-3d
description: 字符级 3D 旋转，带随机字形替换，实现解密揭示效果。
metadata:
  tags: text, 3d, reveal, decode, hacker, randomization, perspective
---

# 黑客翻转 3D 揭示

字符从 90° 在 3D 中向下翻转，同时循环通过随机字形，然后稳定在目标字符上。创造"解密"或机场翻牌显示揭示效果。

## 工作原理

每个字符获得自己的逐字补间，从 `rotateX: 90deg`（隐藏）到 `rotateX: 0deg`（揭示），跨词错开。翻转期间：

1. **阶段 A（进度 0 → ~`REVEAL_THRESHOLD`）**：字符显示随机替换的字形，闪烁（每 `FLICKER_RATE` 帧变化一次）
2. **阶段 B（进度 `REVEAL_THRESHOLD` → 1.0）**：字符显示真实的**目标**字符，稳定到其最终的直立位置

`REVEAL_THRESHOLD` 将"混乱"与"揭示"分开 — 到翻转基本完成时，观看者看到正确的字符卡入到位。

## HTML

```html
<div
  class="scene"
  id="hacker-flip-scene"
  data-composition-id="hacker-flip-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="hacker-text-wrap" id="hacker-text" data-target="{phrase}">
    <!-- 逐字 span 由下方设置脚本注入。
         鬼影占位符（data-ghost）以相同方式渲染以保留宽度。 -->
  </div>
</div>
```

`{phrase}` 是翻转解析到的目标词（通常是品牌或短标签）。

## CSS

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: {bgColor};
  perspective: 1500px; /* 必需 — 没有此属性 rotateX 会平面化渲染 */
}

.hacker-text-wrap {
  font-family: {monoFont};      /* 推荐等宽字体，使闪烁字形保持宽度 */
  font-weight: 900;
  font-size: HACKER_FONT_SIZE;
  color: {textColor};
  letter-spacing: 4px;
  display: flex;
  /* 鬼影/活动字符绝对堆叠；容器保留布局宽度 */
  position: relative;
}

.hacker-char {
  display: inline-block;
  /* 在底边铰链 — 翻牌显示效果 */
  transform-origin: bottom;
  transform-style: preserve-3d;
  /* Will-change 提高渲染性能 */
  will-change: transform, opacity;
}

/* 鬼影占位符隐藏但保留可变字体的宽度。
   没有它，窄目标字形在显示时会塌缩宽度，
   字符在闪烁期间水平移动。 */
.hacker-ghost {
  opacity: 0;
  pointer-events: none;
}
```

## GSAP 时间线 + 随机字形逻辑

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};

  const wrap = document.getElementById("hacker-text");
  const targetWord = wrap.dataset.target;
  const GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*";

  // 构建活动字符 + 鬼影占位符（鬼影保持布局宽度稳定）
  wrap.innerHTML = "";
  const ghostRow = document.createElement("div");
  ghostRow.className = "hacker-ghost";
  ghostRow.style.display = "inline-flex";
  ghostRow.style.position = "absolute";
  ghostRow.style.left = "0";
  ghostRow.style.top = "0";
  ghostRow.textContent = targetWord;
  wrap.appendChild(ghostRow);

  const charEls = [];
  const liveRow = document.createElement("div");
  liveRow.style.display = "inline-flex";
  liveRow.style.position = "relative";
  for (const ch of targetWord) {
    const span = document.createElement("span");
    span.className = "hacker-char";
    span.textContent = ch === " " ? " " : ch;
    span.dataset.target = ch;
    liveRow.appendChild(span);
    charEls.push(span);
  }
  wrap.appendChild(liveRow);

  // 确定性"随机" — 由字符索引 + 帧组种子化，使相同的
  // 帧总是产生相同的字形（HF 定位确定性）。
  function pseudoGlyph(seed) {
    const h = ((seed * 9301 + 49297) % 233280) / 233280;
    return GLYPHS[Math.floor(h * GLYPHS.length)];
  }

  const tl = gsap.timeline({ paused: true });

  // 逐字翻转 — 跨词错开
  charEls.forEach((el, i) => {
    const state = { p: 0 };
    tl.to(
      state,
      {
        p: 1,
        duration: FLIP_DURATION,
        ease: "power3.out",
        onUpdate: () => {
          // 阶段 A：随机字形闪烁。阶段 B：真实字符。
          const progress = state.p;
          if (progress < REVEAL_THRESHOLD) {
            // 每 FLICKER_RATE 进度更新一次字形
            const flickerSeed = i * 1000 + Math.floor(progress * 100);
            el.textContent = pseudoGlyph(flickerSeed);
          } else {
            el.textContent = el.dataset.target === " " ? " " : el.dataset.target;
          }
          // 翻转 rotateX 从 90（向下）到 0（直立）
          const rotateX = 90 - progress * 90;
          const opacity = Math.min(1, progress * 2);
          el.style.transform = `rotateX(${rotateX}deg)`;
          el.style.opacity = opacity;
        },
      },
      i * CHAR_STAGGER,
    );
  });

  window.__timelines["hacker-flip-scene"] = tl;
</script>
```

## 如何选择值

- **HACKER_FONT_SIZE** — 翻转文本的字体大小（px）。
  - 范围：视口最小尺寸的 6-10%；翻转文本是焦点节拍，相应缩放
  - 约束：鬼影行必须使用相同的尺寸，使布局宽度在闪烁期间保持稳定
  - 参考：../../examples/proof-logo-chain.html 在 1920×1080 下使用 `163px`
- **FLIP_DURATION** — 每字符翻转补间时长。
  - 范围：0.4-1.0 秒；低于 0.4 秒随机字形阶段没有时间闪烁，超过 1.0 秒拖沓
  - 效果：更短感觉干脆现代；更长感觉机械/打字机
  - 参考：../../examples/proof-logo-chain.html 使用 `0.55s`
- **CHAR_STAGGER** — 连续字符开始翻转的延迟（秒）。
  - 范围：0.03-0.08 秒；太快则字符视觉重叠，太慢则效果感觉费力
  - 约束：总解码时间 = `CHAR_STAGGER × (charCount − 1) + FLIP_DURATION`；确保它适合阶段预算
  - 参考：../../examples/proof-logo-chain.html 使用 `0.033s`（60fps 下约 2 帧）
- **REVEAL_THRESHOLD** — 字形从随机切换到真实的进度。
  - 范围：0.5-0.7；较低揭示太早（无解码张力），较高感觉像结束时的硬揭示
  - 效果：这是眼睛锁定真实字母时的离散调节
  - 参考：../../examples/proof-logo-chain.html 使用 `0.6`
- **FLICKER_RATE** — 随机阶段期间字形重新洗牌的帧间隔。
  - 范围：3-6；低于 3 看起来像噪声，高于 6 看起来像离散打字而非闪烁
  - 约束：必须 ≥ ~3 帧（参见关键约束）
  - 参考：../../examples/proof-logo-chain.html 使用等效的 `3`（每 3 个内部时钟帧洗牌一次）
- **{bgColor} / {textColor}** — 舞台背景和活动字符颜色标记。
- **{monoFont}** — 优先使用等宽字体系列，使闪烁字形每次交换不改变宽度；如果必须使用比例字体，鬼影占位符使成本可恢复。
- **{phrase}** — 翻转解析到的目标词。通过 `CHAR_STAGGER` 影响总解码时长。

## 变体

- **自上而下铰链** — 将 `transform-origin: bottom` 交换为 `top`，获得向下翻盖效果。
- **中心旋转** — `transform-origin: center` 读作桶滚，而非翻盖。
- **仅数字池** — 将 `GLYPHS` 限制为数字，用于价格/倒计时解码。
- **两遍解码** — 用不同字形池（例如符号 → 字母 → 真实）链接两个 `FLIP_DURATION` 补间，以获得更长的揭示。

## 关键原则

- **在 ~`REVEAL_THRESHOLD` 处从随机到真实字形的阈值** — 接近稳定，使观看者眼睛捕捉到正确字母
- **在 `transform-origin: bottom` 处铰链** 用于翻牌显示效果（vs `top` 用于自上而下，vs `center` 用于旋转）
- **通过种子化哈希的确定性随机** — HF 运行时逐帧定位，因此相同帧必须显示相同字形（无 `Math.random()`）
- **鬼影占位符** 位于活动字符后面，具有相同内容 + 相同字体，保留宽度 — 没有它，窄字形会在闪烁期间移动布局
- **每字符错开在 0.04-0.08s 范围内** — 太快则字符视觉重叠，太慢则效果感觉费力
- **通过 `display: grid; place-items: center;` 将翻转在场景根元素上绝对居中** — 且不要添加装饰性页眉/页脚（时间戳行、"// AUTH"标签、小状态点）。翻转文本就是焦点节拍；周围的杂乱稀释了它。如果辅助标签是必要的，将其提升为相同堆叠布局中的大字号排版（56-72px 大写 + 跟踪），而非小角落注释。

## 关键约束

- **场景根元素上的 `perspective` 必需** — 没有父透视，`rotateX` 看起来像 2D 缩放，而非 3D 翻转
- **每个字符上的 `transform-style: preserve-3d`** — 当字符有自己的变换时保持 3D 上下文完整
- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **确定性随机**：不要使用 `Math.random()`。使用从字符索引 + 帧组派生的种子，使定位确定性保持
- **`onUpdate` 写入 DOM**：HF 每帧定位，因此这运行很多次 — 保持每字符每帧工作为 O(1)
- **闪烁速率 ≥ ~3 帧每次字形交换**：更快看起来像噪声，更慢看起来像离散打字

## 组合

- [card-morph-anchor.md](card-morph-anchor.md) — 配对：黑客翻转揭示一个短语，然后卡片变形到下一个镜头
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 数字揭示的对应物（文本 vs 数字）

## 与 HF 技能配对

- `/hyperframes-animation` — 时间线 + 逐字错开 + `onUpdate`
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
