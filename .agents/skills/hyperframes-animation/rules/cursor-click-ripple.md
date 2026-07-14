---
name: cursor-click-ripple
description: 动画鼠标光标移动到目标，以缩放下压点击并扩展涟漪环。
metadata:
  tags: cursor, click, ripple, interaction, mouse, button
---

# 光标点击涟漪

一个动画光标移动到目标元素，执行带有视觉下压的点击，并从点击点发出扩展的涟漪环。

## 工作原理

三个顺序阶段由单个 GSAP 时间线驱动：

1. **移动**：缓动光标平移从入口点到目标元素的中心
2. **点击**：光标和目标上的缩放下压（yoyo：缩小然后返回）
3. **涟漪**：扩展圆圈从点击点向外辐射并淡出。1–3 个错开环放大点击反馈

使用 GSAP 时间线，因为阶段排序（移动 → 稳定 → 点击 → 涟漪）正是时间线干净表达的。

## HTML

```html
<div
  class="scene"
  id="cursor-click-scene"
  data-composition-id="cursor-click-scene"
  data-start="0"
  data-duration="2"
  data-track-index="0"
>
  <button class="target-button">{ctaLabel}</button>

  <div class="cursor">
    <svg width="24" height="24" viewBox="0 0 24 24">
      <path
        d="M5 3L19 12L12 13L9 20L5 3Z"
        fill="{cursorFill}"
        stroke="{cursorStroke}"
        stroke-width="1.5"
      />
    </svg>
  </div>

  <!-- 涟漪环 — 以点击目标为中心，隐藏直到触发 -->
  <div class="ripple ripple-1"></div>
  <div class="ripple ripple-2"></div>
  <div class="ripple ripple-3"></div>
</div>
```

## CSS

光标定位在入口点。按钮位于其最终位置。涟漪位于点击目标中心，`scale: 0` 和 `opacity: 0`，使它们保持不可见直到时间线触发：

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
}

.target-button {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  /* ...按钮样式（背景、颜色、字体来自项目标记） */
}

.cursor {
  position: absolute;
  left: 10%;
  top: 80%; /* 入口角 */
  pointer-events: none;
  z-index: 999;
}

.ripple {
  position: absolute;
  left: 50%;
  top: 50%; /* 点击目标中心 */
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid {rippleColor};
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  pointer-events: none;
}
```

## GSAP 时间线

构建一个暂停的时间线。在 `window.__timelines` 上以与场景根元素 `data-composition-id` 相同的键注册。所有调谐值都是命名常量 — 参见下方如何选择值。

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // MOVE_DUR、MOVE_EASE、CLICK_AT、PRESS_DUR、CURSOR_PRESS_SCALE、TARGET_PRESS_SCALE、
  // RIPPLE_AT、RIPPLE_DUR、RIPPLE_SCALE、RIPPLE_STAGGER、RIPPLE_EASE
  // — 都是命名常量；值按如何选择值。

  // 阶段 1 — 将光标移动到目标中心（缓动，非线性）
  tl.to(
    ".cursor",
    {
      x: TARGET_X,
      y: TARGET_Y,
      duration: MOVE_DUR,
      ease: MOVE_EASE,
    },
    0,
  );

  // 阶段 2 — 点击：光标 + 目标一起下压，然后返回
  tl.to(
    ".cursor",
    {
      scale: CURSOR_PRESS_SCALE,
      duration: PRESS_DUR,
      ease: "power2.in",
      yoyo: true,
      repeat: 1,
    },
    CLICK_AT,
  );
  tl.to(
    ".target-button",
    {
      scale: TARGET_PRESS_SCALE,
      duration: PRESS_DUR,
      ease: "power2.in",
      yoyo: true,
      repeat: 1,
    },
    CLICK_AT,
  );

  // 阶段 3 — 涟漪爆发，从点击点错开 N 个环
  tl.set([".ripple-1", ".ripple-2", ".ripple-3"], { opacity: 1 }, RIPPLE_AT);
  tl.to(
    [".ripple-1", ".ripple-2", ".ripple-3"],
    {
      scale: RIPPLE_SCALE,
      opacity: 0,
      duration: RIPPLE_DUR,
      ease: RIPPLE_EASE,
      stagger: RIPPLE_STAGGER,
      immediateRender: false,
    },
    RIPPLE_AT,
  );

  window.__timelines["cursor-click-scene"] = tl;
</script>
```

## 如何选择值

- **MOVE_DUR** — 光标从入口到目标的移动时间（秒）
  - 范围：0.4–1.0 秒
  - 效果：短感觉快速移动；长感觉慎重/"经过考虑的点击"
  - 约束：必须在 `CLICK_AT` 前结束 — 否则在光标仍在移动时触发点击，读作误点击
  - 参考：../../examples/cta-orbit-collapse.html 使用 0.5 秒
- **MOVE_EASE** — 移动补间的缓动族
  - 离散选择。选项：
    - `power2.inOut` — 对称、平静；适合"用户深思熟虑地移动光标"
    - `back.out(<n>)` — 过冲着陆；适合点击目标是按钮且希望光标以微小可见后坐力"稳定到"其上。配合低过冲系数（~1.2–1.4）— 更高读作卡通化
    - `power3.out` — 快速启动，柔和着陆；适合"果断"移动
  - 参考：../../examples/cta-orbit-collapse.html 使用 `back.out(1.3)`
- **CLICK_AT** — 点击触发的时间（秒）
  - 范围：必须 ≥ `MOVE_DUR`（光标已稳定）；通常 `MOVE_DUR + 0.0–0.3 秒"决策暂停"`
  - 效果：零暂停读作自动驾驶；>0.3 秒暂停读作犹豫
  - 参考：../../examples/cta-orbit-collapse.html 在光标稳定后 0.2 秒点击
- **PRESS_DUR** — 下压的半时长（yoyo 运行两次此值）
  - 范围：0.06–0.12 秒
  - 效果：短感觉干脆；长感觉糊软
  - 约束：总按下 = `2 * PRESS_DUR`；必须在下个场景阶段需要光标/按钮回到正常缩放前完成
  - 参考：../../examples/cta-orbit-collapse.html 使用 0.08 秒
- **CURSOR_PRESS_SCALE / TARGET_PRESS_SCALE** — 每个在点击期间压缩的程度
  - 范围：光标 0.80–0.90；目标 0.92–0.97
  - 效果：更小数字 = 更强的"此点击算数"感觉；接近 1 的值读作轻柔点击
  - 约束：光标压缩**比**目标更多 — 光标是行动者，目标是接受者
  - 参考：../../examples/cta-orbit-collapse.html 使用光标 0.85 / 目标 0.95
- **RIPPLE_AT** — 环开始扩展的时间（秒）
  - 范围：`CLICK_AT + 0.0–0.08 秒`
  - 效果：与按下同时感觉因果；轻微延迟感觉声学（"点击发生，然后波辐射"）
  - 参考：../../examples/cta-orbit-collapse.html 在 `CLICK_AT` 精确开始时启动涟漪
- **RIPPLE_DUR** — 每个环完全扩展并淡出的时间
  - 范围：0.5–1.0 秒
  - 效果：短环感觉锐利；长环感觉像柔和声纳
  - 约束：必须在任何依赖环消失的阶段（例如屏幕擦拭）前完成
  - 参考：../../examples/cta-orbit-collapse.html 使用 0.7 秒
- **RIPPLE_SCALE** — 每个环在淡出前的最终缩放
  - 范围：3–6
  - 效果：3 保持环靠近点击位置；6 让它扫过周围区域
  - 约束：如果环在达到不透明度 0 前会退出可见画面，降低缩放或缩短时长
  - 参考：../../examples/cta-orbit-collapse.html 使用 5
- **RIPPLE_STAGGER** — 连续环之间的延迟
  - 范围：0.06–0.12 秒（或 0 用于单环；参见变体）
  - 效果：低于 ~0.06 秒读作一个粗环；高于 ~0.12 秒读作独立事件
  - 参考：../../examples/cta-orbit-collapse.html 使用单环（无错开）
- **RIPPLE_EASE** — 扩展的缓动族
  - 离散选择。选项：
    - `power2.out` — 快速启动，柔和尾巴；标准的"砰"感觉
    - `power3.out` — 甚至更锐利的攻击，更长的尾巴
    - `expo.out` — 几乎瞬时扩展，长时间安静淡出；读作强、遥远的脉冲
  - 参考：../../examples/cta-orbit-collapse.html 使用 `power2.out`
- **TARGET_X / TARGET_Y** — 点击目标距光标 CSS 布局原点的像素偏移
  - 这些是布局派生的，非创意旋钮 — 它们必须匹配实际点击目标的视觉重心。4px 的偏差读作没点到按钮
  - 参考：../../examples/cta-orbit-collapse.html 以 `CENTER_X + 130, CENTER_Y + 15` 的白色按钮为目标

## 变体

- **单环** — 保留一个 `.ripple` 元素，去掉错开；当场景其余部分繁忙时读作更优雅
- **键控攻击-衰减** — 用 `keyframes` 块替换简单的扩展并淡出，该块在时长内从不透明度 0 → 峰值 → 0 渐变；给出更清晰的"能量辐射并消散"包络（在 ../../examples/cta-orbit-collapse.html 中使用）
- **多环扩展脉冲** — 3 个环，0.08 秒错开，当点击是场景的高潮时刻时感觉更丰富

## 关键原则

- **移动然后点击**：仅在移动补间稳定后触发点击 — 运动中点击读作无意
- **同步下压**：光标 + 目标在相同 `position` 时间下压，相同时长（并都 yoyo 返回）
- **从点击点涟漪**：涟漪从精确的点击位置扩展（按钮的视觉中心），而非任何元素的边界框原点
- **微妙缩放**：光标压缩比目标更多 — 参见 `CURSOR_PRESS_SCALE` / `TARGET_PRESS_SCALE`
- **高 z-index 光标**：光标在整个序列中渲染在所有内容之上

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`。永远不要调用 `tl.play()` — HyperFrames 确定性逐帧定位时间线
- **注册键 = `data-composition-id`**：`window.__timelines["<id>"]` 必须精确匹配场景根元素上的 `data-composition-id`
- **涟漪扩展上设置 `immediateRender: false`**：保持初始状态（`scale: 0`、`opacity: 0`）直到点击时刻，否则补间预渲染，环在 t=0 时以错误大小出现
- **有限时长**：验证 `tl.duration()` 匹配场景的 `data-duration`
- **光标 + 涟漪上设置 `pointer-events: none`**：它们是纯视觉的；永不阻塞底层交互性（对可悬停导出物重要）
- **无 CSS 过渡/动画**：所有运动在 GSAP 时间线中，使定位保持确定性

## 组合

- [orbit-3d-entry.md](orbit-3d-entry.md) — 当点击是枢轴，将轨道元素向光标目标塌缩时
- [center-outward-expansion.md](center-outward-expansion.md) — 点击可以是从点击点向外爆发的触发
- [press-release-spring.md](press-release-spring.md) 用于目标按钮上更强的物理感
- [scale-swap-transition.md](scale-swap-transition.md) 用于按钮点击后的状态变化（按钮变形为成功状态、下一个视图等）

## 与 HF 技能配对

- `/hyperframes-animation` — 时间线 + 补间 API 参考（缓动、错开、`immediateRender` 等）
- `/hyperframes-core` — 组合接线（`data-*` 属性、场景结构、注册约定）
- `/hyperframes-cli` — `hyperframes lint` 验证注册键 + 时长匹配
