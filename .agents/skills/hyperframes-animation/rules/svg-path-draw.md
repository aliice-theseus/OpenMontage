---
name: svg-path-draw
description: 使用 stroke-dasharray 和 stroke-dashoffset 逐步动画化 SVG 路径绘制。
metadata:
  tags: svg, stroke, draw, path, reveal, icon, vector
---

# SVG 路径绘制

通过动画化 SVG 形状的描画来揭示它，就像用笔实时描绘一样。

## 工作原理

该技巧一起使用两个 SVG 描画属性：

1. **`stroke-dasharray = <pathLength>`** — 将虚线模式设置为等于路径总长度的单个虚线，使整个路径成为"一条虚线"
2. **`stroke-dashoffset`** — 控制虚线的多少部分被移出视野。从 `pathLength` 开始（整个路径偏移出去 → 不可见），动画化到 `0`（无偏移 → 完全绘制）

路径长度通过 DOM API `path.getTotalLength()` 计算。

## HTML

```html
<div
  class="scene"
  id="svg-draw-scene"
  data-composition-id="svg-draw-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <svg class="logo-mark" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <!-- 多段字形；顺序绘制所有段 -->
    <path id="bar-left" d="M 60 40 L 60 160" />
    <path id="bar-right" d="M 140 40 L 140 160" />
    <path id="bar-mid" d="M 60 100 L 140 100" />
  </svg>
  <div class="brand-line">{Brand}</div>
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
  gap: 32px;
}

.logo-mark {
  width: 320px;
  height: 320px;
}

.logo-mark path {
  fill: none;
  stroke: {accentColor};
  stroke-width: 12;
  stroke-linecap: round; /* 柔化端点 */
  stroke-linejoin: round;
  /* 初始状态：不可见。GSAP 根据每个路径的测量长度填充
     strokeDasharray + strokeDashoffset。 */
}

.brand-line {
  font-family: {font};
  font-weight: 700;
  font-size: 48px;
  color: {textColor};
  opacity: 0; /* 描画完成后淡入 */
  letter-spacing: 0.04em;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};

  // 命名常量 — 赋值在示例中，不在此处。
  // 参见下方"如何选择值"以了解范围和选择标准。
  const SEGMENT_DRAW_DUR; // 每段描画时长
  const FINAL_SEGMENT_DUR; // 最后（较短）段的较短描画
  const SEG_1_START; // 第一段开始时间
  const SEG_2_START; // 第二段开始时间（与 SEG_1 尾部重叠）
  const SEG_3_START; // 第三段开始时间（与 SEG_2 尾部重叠）
  const BRAND_FADE_DUR; // wordmark 淡入时长
  const BRAND_FADE_START; // wordmark 淡入开始（最后描画稳定后）

  // 测量每个路径的总长度并设置其虚线模式。
  // getTotalLength() 是一个真实的 DOM API — 其返回值是动态
  // 测量的几何数据，不是魔术数字。
  const paths = document.querySelectorAll(".logo-mark path");
  paths.forEach((p) => {
    const len = p.getTotalLength();
    p.style.strokeDasharray = `${len}`;
    p.style.strokeDashoffset = `${len}`;
  });

  const tl = gsap.timeline({ paused: true });

  // 跨段的错开绘制 — 每个在前一个完成前开始
  // 使眼睛读作连续运动。
  tl.to(
    "#bar-left",
    {
      strokeDashoffset: 0,
      duration: SEGMENT_DRAW_DUR,
      ease: "power2.out",
    },
    SEG_1_START,
  );
  tl.to(
    "#bar-right",
    {
      strokeDashoffset: 0,
      duration: SEGMENT_DRAW_DUR,
      ease: "power2.out",
    },
    SEG_2_START,
  );
  tl.to(
    "#bar-mid",
    {
      strokeDashoffset: 0,
      duration: FINAL_SEGMENT_DUR,
      ease: "power2.out",
    },
    SEG_3_START,
  );

  // 品牌线在描画稳定后淡入
  tl.to(
    ".brand-line",
    {
      opacity: 1,
      duration: BRAND_FADE_DUR,
      ease: "power1.out",
    },
    BRAND_FADE_START,
  );

  window.__timelines["svg-draw-scene"] = tl;
</script>
```

## 如何选择值

- **SEGMENT_DRAW_DUR** — 每段描画时长
  - 范围：0.3-0.8 秒
  - 效果：低端读作快速快照（适合短段）；高端读作有意的笔迹（适合长曲线）
  - 约束：必须足够短，使总链（最后段完成）在 BRAND_FADE_START 前结束；长于 ~1 秒对于 logo 揭示感觉迟缓
  - 参考：短轮廓段使用 ~0.5 秒

- **FINAL_SEGMENT_DUR** — 最短/最终段的时长
  - 范围：0.25-0.6 秒
  - 效果：应与段长度成比例 — 以 SEGMENT_DRAW_DUR 绘制的短连接件看起来比其较长的兄弟更慢
  - 约束：当段明显比其他段短时，通常为 SEGMENT_DRAW_DUR 的 60-80%
  - 参考：大约为垂直段 2/3 长度的中间条使用 ~0.35 秒

- **SEG_1_START** — 第一段开始时间
  - 范围：0-0.4 秒
  - 效果：0 立即开始播放；>0 在运动前给一段短暂的空白舞台
  - 约束：应为 ≥ 0
  - 参考：~0.2 秒的小引导让观看者在运动前稳定

- **SEG_2_START** — 第二段开始时间
  - 范围：SEG_1_START + (0.5 × SEGMENT_DRAW_DUR) 到 SEG_1_START + SEGMENT_DRAW_DUR
  - 效果：接近 SEG_1_START + 0.5×SEGMENT_DRAW_DUR 感觉快速/重叠；接近 SEG_1_START + SEGMENT_DRAW_DUR 感觉顺序
  - 约束：错开 ~SEGMENT_DRAW_DUR 的 70-80% 读作连续运动（而非 3 个独立的动画）
  - 参考：SEG_1_START + ~0.25 秒（约 SEGMENT_DRAW_DUR 的一半）

- **SEG_3_START** — 第三段开始时间
  - 范围：SEG_2_START + (0.5 × SEGMENT_DRAW_DUR) 到 SEG_2_START + SEGMENT_DRAW_DUR
  - 效果：与 SEG_2_START 相同 — 控制感知节奏
  - 约束：应保持与 SEG_1 和 SEG_2 之间相同的错开比例
  - 参考：SEG_2_START + ~0.4 秒

- **BRAND_FADE_DUR** — wordmark 淡入时长
  - 范围：0.3-0.8 秒
  - 效果：低端快照进入（紧急）；高端滑入（高级/品牌）
  - 约束：必须在组合的 `data-duration` 结束前完成
  - 参考：平静的 logo 组合使用 ~0.5 秒

- **BRAND_FADE_START** — wordmark 淡入开始时间
  - 范围：max(SEG_3_START + FINAL_SEGMENT_DUR, …) 到该值 + 0.4 秒
  - 效果：正好在最后描画结束时开始感觉紧密链接；增加一个小节拍给描画一些"稳定"时间，然后 wordmark 加入
  - 约束：**必须** ≥ SEG_3_START + FINAL_SEGMENT_DUR（否则 wordmark 在绘制期间出现并与它竞争）
  - 参考：SEG_3_START + FINAL_SEGMENT_DUR + ~0.2 秒

此处使用的缓动族是离散选择，而非可调标量：

- **描画绘制**使用 `power2.out` — 柔和减速模仿笔在描画结束时抬起。不要使用 `back.out` 或 `elastic.out`（笔不会弹跳）。
- **品牌淡入**使用 `power1.out` — 不透明度补间上的柔和尾迹。
- 对于恒定速度的"真实笔"描绘感觉，使用 `none`（参见变体）。

## 变体

### 旋转起始点（从顶部开始而非 3 点钟方向）

默认情况下，`<circle>` 和 `<rect>` 的描画从 3 点钟方向开始。旋转元素使其从顶部开始：

```html
<circle
  cx="100"
  cy="100"
  r="60"
  id="ring"
  style="transform-origin: 100px 100px; transform: rotate(-90deg);"
/>
```

### 线性（恒定速度）绘制

使用 `ease: 'none'` 实现稳定速度绘制（如实际笔迹）：

```js
tl.to("#path", { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "none" }, SEG_1_START);
```

### 绘制然后填充

对于有填充颜色的 SVG 形状，在描画完成后动画化填充不透明度：

```js
tl.to(
  "#path",
  { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "power2.out" },
  SEG_1_START,
);
tl.to(
  "#path",
  { fillOpacity: 1, duration: FILL_FADE_DUR, ease: "power1.out" },
  SEG_1_START + SEGMENT_DRAW_DUR,
);
```

需要在 CSS 中初始设置 `fill-opacity: 0` 和真实的 `fill` 颜色。

## 关键原则

- **将 `strokeDasharray` 设置为路径的 `getTotalLength()` 值**，而非任意数字 — 猜测意味着描画会动画但不匹配几何体
- **从相同长度开始设置 `strokeDashoffset`**，动画化到 `0`
- **在时间线设置中测量，而非模块顶部** — 在某些环境中模块代码运行时 SVG 可能尚未渲染。在 HF 运行时中，由于 SVG 是内联的，在顶部可以工作，但安全起见
- **`stroke-linecap: round`** 用于更柔和的端点（不那么突兀的结束）
- **对于顺序多路径绘制，以前一段时长的大约 70-80% 错开** — 眼睛读作连续运动，而非 N 个独立的动画
- **不要与 `back.out` 或 `elastic.out` 配对** — 弹跳的描画感觉不对（笔不会弹跳）

## 关键约束

- **仅轮廓绘制的 CSS 中设置 `fill: none`** — 否则填充区域立即出现，破坏揭示效果
- **路径长度在浏览器中测量**：要求 SVG 在 DOM 中。HF 内联 SVG 没问题；加载的 `<image>` SVG 可能不行
- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **适用于**：`<path>`、`<circle>`、`<rect>`、`<line>`、`<polyline>`、`<polygon>`、`<ellipse>`（任何带描画属性的元素）
- **对于复杂路径**，如果 `getTotalLength()` 看起来不对，略微高估 `strokeDasharray`（例如 `len * 1.05`）— 太大在动画开始时不可见（无可见间隙），太小会裁剪末端

## 组合

- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 配对：描画绘制图标，同时数字在其旁边计数递增
- [hacker-flip-3d.md](hacker-flip-3d.md) — 配对：SVG logo 绘制，然后在其下揭示黑客翻转的 wordmark

## 与 HF 技能配对

- `/hyperframes-animation` — 时间线 + 描画属性补间
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
