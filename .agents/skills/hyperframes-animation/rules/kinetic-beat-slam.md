---
name: kinetic-beat-slam
description: 打击式动感排版 — 短短语以稳定节拍猛烈进入，带有每个短语不同的入场，可选节奏镀铬（节拍器滴答、节拍条），然后锁定终曲。
metadata:
  tags: text, kinetic, typography, beat, rhythm, slam, percussive, punchy
---

# 动感节拍撞击

短短语在**稳定节拍**上一次一个进入，每个有**不同**的入场，然后堆叠成锁定的终曲。这是"有力/节奏"文本前卫片段（标语、宣言、炒作开场）的配方。泛泛和节奏感之间的区别在于 (1) 一个共享的**开始时间数组**驱动每个元素，(2) 每个短语**不同**的入场而非一个重复使用的辅助函数，以及 (3) 可选的**节奏镀铬**，肉眼可见地保持节拍。

## 工作原理

1. **一次定义节拍。** 一个单一的 `BEATS = [t0, t1, t2, …]` 数组（秒）是节奏脊柱。每个短语入场、重音和镀铬滴答从此数组读取其时间 — 因此整个作品锁定一个脉冲，而非漂移的手调偏移。
2. **变化入场。** 短语 1 猛击（缩放 + 模糊），短语 2 从侧边快照，短语 3 上升并旋转。相同的**能量**，不同的**形式** — 为全部三个重用一个 `punchIn()` 读作平铺直叙。
3. **着陆终曲。** 所有短语锁定到左对齐或居中堆叠；一个重音下划线扫入；可选一个持续的低振幅脉冲保持最后一拍。

## 节拍与缓动

按攻击特性选择入场缓动（选择是离散的）：

| GSAP 缓动       | 攻击感觉                               |
| --------------- | -------------------------------------- |
| `power4.out`    | 硬撞击，快速稳定 ⭐ 撞击的默认选择      |
| `expo.out`      | 最硬快照（侧边快照，鞭打进入）         |
| `back.out(2)`   | 过冲弹出 — 重音，非正文单词            |
| `circ.out`      | 带动量的沉重上升                       |

跨作品使用**至少 3 种不同缓动**（入场是其"语气"）。保持时长短 — 撞击 0.35–0.6 秒，退出 ≤0.25 秒 — 使节拍保持打击感。

## HTML

```html
<section class="clip" data-start="0" data-duration="15" data-track-index="1">
  <div class="kbs-stage">
    <div class="kbs-line" id="p1"><span class="verb">Notice</span> more.</div>
    <div class="kbs-line" id="p2"><span class="verb">Decide</span> faster.</div>
    <div class="kbs-line" id="p3"><span class="verb">Act</span> now.</div>
  </div>
  <!-- 可选节奏镀铬 -->
  <div class="kbs-metronome" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
</section>
```

## CSS

```css
.kbs-stage {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
  padding: 120px 160px; /* 标题安全边距 */
  box-sizing: border-box;
}
.kbs-line {
  font-family: "Archivo Black", "League Gothic", sans-serif; /* 嵌入展示字体 */
  font-size: 150px;
  line-height: 0.96;
  letter-spacing: -0.03em;
  color: #f5f5f5;
  will-change: transform, filter, opacity;
}
.kbs-line .verb {
  color: #ff5b2e;
} /* 一个重音色调 */
.kbs-metronome {
  position: absolute;
  bottom: 64px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 14px;
}
.kbs-metronome i {
  width: 6px;
  height: 28px;
  background: #ff5b2e;
  opacity: 0.25;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 一个节奏网格驱动一切 — 短语和节拍器都读取它（无分散偏移）。
  const PULSE = 0.4; // 每子节拍秒数（网格）
  const BEATS = [PULSE * 1, PULSE * 5, PULSE * 9]; // 短语开始时间，在网格上

  // 每个短语不同的入场（不是一个重复使用的辅助函数）。
  tl.fromTo(
    "#p1",
    { scale: 1.5, filter: "blur(16px)", opacity: 0 },
    { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.5, ease: "power4.out" },
    BEATS[0],
  );
  tl.fromTo(
    "#p2",
    { x: -320, opacity: 0 },
    { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" },
    BEATS[1],
  );
  tl.fromTo(
    "#p3",
    { y: 90, rotation: 6, opacity: 0 },
    { y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "circ.out" },
    BEATS[2],
  );

  // 节奏镀铬：每个节拍器滴答在相同网格（PULSE）上闪烁，而非神奇偏移。
  const ticks = gsap.utils.toArray(".kbs-metronome i");
  ticks.forEach((tick, i) => {
    tl.to(
      tick,
      { opacity: 1, duration: 0.08, yoyo: true, repeat: 1, ease: "none" },
      PULSE * (i + 1),
    );
  });

  // 终曲保持：锁定堆栈上的低振幅呼吸。
  // 使用 floor（而非 ceil）使重复从不超过 data-duration；max(0,…) 使短保持
  // 从不产生负重复（GSAP 将负 repeat 视为 -1 = 无限 = 非确定性）。
  const holdStart = BEATS[2] + 0.7,
    cycle = 1.6,
    holdDur = 15 - holdStart;
  tl.to(
    ".kbs-stage",
    {
      scale: 1.01,
      duration: cycle / 2,
      ease: "sine.inOut",
      yoyo: true,
      repeat: Math.max(0, Math.floor(holdDur / cycle) - 1),
    },
    holdStart,
  );

  window.__timelines["main"] = tl;
</script>
```

## 如何选择值

- **BEATS 间距** — 1.2–1.8 秒之间的撞击读作自信节拍；<0.8 秒感觉狂乱，>2.5 秒失去脉冲。保持间距均匀（它是**节拍**）。
- **入场时长** — 0.35–0.6 秒。撞击必须在下一个节拍前解析。
- **不同入场** — 为每个短语分配不同的变换轴（缩放 / x / y+旋转）。复用_缓动族_，变化_运动_。
- **重音色调** — 恰好一个（动词）。其余为单色白/近黑。
- **节奏镀铬** — 可选但对于"节奏感"高影响力：一个 5 滴答节拍器、一个中心节拍条或一个在节拍上脉冲的 `// label` 等宽标签。根据 `../../transitions/overview.md` 规则，标记必须通过着色器过渡的任何装饰性元素。

## 关键原则

- **一个节拍数组，非分散偏移** — 每个元素从 `BEATS[]` 计时。这是"节奏感"最大的单杠杆。
- **每个短语不同的入场** — 为所有行重用一个 `punchIn()` 是平铺但合格的特征。
- **短攻击** — 打击意味着快进、简短、果断。长淡入淡出杀死节拍。
- **一个重音色调，重字重** — 嵌入展示字体（Archivo Black、League Gothic、Oswald）150px+；参见 `hyperframes-creative/references/typography.md`。
- **终曲赢得保持** — 堆叠 + 下划线扫过 + 可选呼吸；不要只是让最后一个短语坐着。

## 关键约束

- **时间线暂停**：`gsap.timeline({ paused: true })`。永远不要 `tl.play()`。
- **保持/镀铬上无无限重复** — 使用 `repeat: Math.max(0, Math.floor(dur / cycle) - 1)`（无 `repeat: -1`）。使用 **`Math.floor`，而非 `Math.ceil`** — `ceil` 会超过 `data-duration` 并触发 `gsap_repeat_ceil_overshoot` lint 规则；`Math.max(0, …)` 防止当保持短于两个周期时的负重复（GSAP 将其视为 `-1` = 无限 = 非确定性）。
- **场景之间无禁止的退出动画** — 如果这是几个场景之一，**过渡**就是退出（参见 `../../transitions/overview.md`）；只有最终场景可以淡出。
- **展示字体必须嵌入**，否则在渲染时会静默回退（Anton/Bebas-as-literal 未嵌入 — `Bebas Neue` 别名到 League Gothic；在 `typography.md` 中验证）。
- **根元素上的注册键 = `data-composition-id`**。

## 组合

- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 撞击词上的挤压深度
- [css-marker-patterns.md](css-marker-patterns.md) — 终曲上的下划线扫过/圆圈
- [sine-wave-loop.md](sine-wave-loop.md) — 终曲呼吸/脉冲

## 与 HF 技能配对

- `/hyperframes-animation` — 时间线 + 缓动词汇（`../../adapters/gsap-easing-and-stagger.md`）
- `/hyperframes-creative` — `references/video-composition.md`（前景节奏镀铬）、`references/typography.md`（嵌入展示字体）
- `/hyperframes-core` — 组合接线、确定性（有限重复）
