---
name: reactive-displacement
description: 物理碰撞，进入元素的弹簧驱动退出元素的位移 — 单一真相源使运动因果关联。
metadata:
  tags: transition, physics, collision, displacement, spring, causal
---

# 反应性位移

元素 A 的退出动画从元素 B 的进入弹簧**数学推导**而来。创建因果链接："A 移动**因为** B 撞击了它。"与 [scale-swap-transition](scale-swap-transition.md)（重叠但不是因果的）和 [card-morph-anchor](card-morph-anchor.md)（使用一个容器变形尺寸）不同。

## 工作原理

一个单一的 0→1 驱动补间（"进入弹簧"）供给两个派生运动：

- **侵入者**（B，进入）：位置从舞台外插值到稳定位置
- **受害者**（A，退出）：位置从稳定位置向**相反**方向插值到舞台外，但在驱动器的 `VICTIM_FRACTION`（不是 1.0）时完成

受害者的退出在侵入者进入**之前**完成的事实创造了"撞击然后稳定"的节奏。两个运动共享相同的缓动驱动器，因此撞击时刻在数学上同步。

## HTML

```html
<div
  class="scene"
  id="collide-scene"
  data-composition-id="collide-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="stage">
    <div class="card victim" id="victim">
      <div class="card-title">{victimHeadline}</div>
      <div class="card-sub">{victimSubline}</div>
    </div>
    <div class="card intruder" id="intruder">
      <div class="card-title">{intruderHeadline}</div>
      <div class="card-sub">{intruderSubline}</div>
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
  overflow: hidden;
  background: radial-gradient(ellipse at center, {bgColor} 0%, {bgColorDeep} 70%);
  font-family: {font};
}
.stage {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
}
.card {
  position: absolute;
  /* 两者都在中心；变换平移它们 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 64px 80px;
  border-radius: 28px;
  will-change: transform, opacity;
}
.victim {
  background: linear-gradient(160deg, {victimTint} 0%, {bgColorDeep} 70%);
  border: 1px solid {victimTint};
  z-index: 1;
}
.intruder {
  background: linear-gradient(160deg, {intruderTint} 0%, {bgColorDeep} 70%);
  border: 2px solid {intruderBorder};
  box-shadow: 0 28px 96px {intruderTint};
  z-index: 2;
}
.card-title {
  font-size: 200px;
  font-weight: 900;
  color: {textColor};
  line-height: 1;
  letter-spacing: -4px;
}
.card-sub {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: 10px;
  text-transform: uppercase;
  color: {accentColor};
  text-align: center;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // 舞台外距离从舞台宽度派生。
  const INTRUDER_START_X = STAGE_W; // 舞台外右侧
  const VICTIM_END_X = -STAGE_W; // 舞台外左侧，相反方向

  // 初始状态 — 受害者居中，侵入者在舞台外右侧
  gsap.set("#victim", { x: 0, opacity: 1, rotation: 0 });
  gsap.set("#intruder", { x: INTRUDER_START_X, opacity: 0, rotation: -INTRUDER_TILT });

  // 单一驱动器 — 进入弹簧 — 在撞击弧线上从 0→1 运行
  const driver = { p: 0 };
  tl.to(
    driver,
    {
      p: 1,
      duration: DRIVER_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`, // 侵入者弹簧
      onUpdate: () => {
        // 侵入者：完整 0→1 进度映射到进入（舞台外 → 中心）
        const intruderX = INTRUDER_START_X * (1 - driver.p);
        const intruderOpacity = Math.min(1, driver.p * FADE_IN_SHARPNESS);
        const intruderRot = -INTRUDER_TILT * (1 - driver.p); // 稳定到 0°
        const intruder = document.getElementById("intruder");
        intruder.style.transform = `translate(-50%, -50%) translateX(${intruderX}px) rotate(${intruderRot}deg)`;
        intruder.style.opacity = String(intruderOpacity);

        // 受害者：在 VICTIM_FRACTION 的驱动器处完成退出（侵入者仍在飞入）
        // 使撞击**时刻**是视觉冲击 — 到侵入者中心时，
        // 受害者已离开舞台。
        const victimP = Math.min(1, driver.p / VICTIM_FRACTION);
        const victimX = VICTIM_END_X * victimP;
        const victimOpacity = 1 - victimP;
        const victim = document.getElementById("victim");
        victim.style.transform = `translate(-50%, -50%) translateX(${victimX}px)`;
        victim.style.opacity = String(victimOpacity);
      },
    },
    DRIVER_AT,
  );

  // 高潮停留 — 侵入者在稳定后保持在中心（无额外运动；
  // 组合以侵入者居中继续 ≥ DWELL_MIN 秒）。

  window.__timelines["collide-scene"] = tl;
</script>
```

## 如何选择值

- **DRIVER_AT** — 进入弹簧开始时间
  - 范围：阶段相关（通常在进入几秒后）
  - 效果：太早跳过设置节拍；太晚延迟切换
  - 约束：必须在组合结束前允许 ≥ DWELL_MIN 的高潮停留
  - 参考：示例在先前阅读节拍解析后调度位移
- **DRIVER_DUR** — 完整侵入者进入时长
  - 范围：0.6-1.4 秒
  - 效果：短 = 快速/有力撞击；长 = 沉重/着陆撞击
  - 约束：与 `BOUNCE_FACTOR` 协调 — 时长长 + 高弹跳读作漂浮
  - 参考：参见相应的蓝图/示例
- **BOUNCE_FACTOR** — 侵入者弹簧上的 `back.out()` 系数
  - 范围：1.2-2.0（`back.out` 族内离散选择）
  - 效果：低 ≈ 稳定坚定；高 ≈ 过冲/弹跳
  - 约束：缓动族保持 `back.out`（如果你想要振荡，升级到 `elastic.out`）；改变族会重写感觉
  - 参考：示例通常在 1.4 和 1.6 之间
- **VICTIM_FRACTION** — 受害者完成退出占 `DRIVER_DUR` 的分数
  - 范围：0.4-0.5
  - 效果：< 0.4 受害者在撞击读出来前消失；> 0.5 运动感觉平行，非因果
  - 约束：硬上限 ~0.6；超过此值碰撞隐喻破裂
  - 参考：此规则模式使用 ~0.5
- **STAGE_W** — 舞台宽度像素，用于将元素放置在舞台外
  - 范围：等于组合的 `data-width`
  - 效果：较小值使舞台外元素在开始部分可见
  - 约束：必须 ≥ 组合宽度
  - 参考：示例直接使用项目的渲染宽度
- **INTRUDER_TILT** — 侵入者稳定到 0° 时的初始旋转角度（度）
  - 范围：5-15°
  - 效果：低 = 干净滑动；高 = 可见"旋转并着陆"
  - 约束：保持符号与进入方向一致（匹配动量传递）
  - 参考：~10° 是典型的中撞击倾斜
- **FADE_IN_SHARPNESS** — 控制侵入者不透明度达到 1 的速度的乘数
  - 范围：3-8（侵入者在进度的 `1/FADE_IN_SHARPNESS` 处达到不透明度 1）
  - 效果：低 = 伴随运动的柔和淡入；高 = 提前弹出并读作实体
  - 约束：> 1；低于 1 意味着侵入者在中心时仍透明
  - 参考：大多数示例使用锐利早期揭示
- **DWELL_MIN** — 侵入者稳定后的最小高潮停留
  - 范围：≥ 1.0 秒
  - 效果：更短感觉匆忙且不可读；更长延迟组合
  - 约束：冲击后停留是新内容被阅读的地方 — 不要跳过
  - 参考：1.0-1.5 秒是典型

## 变体

### 受害者上的冲击旋转

受害者不仅滑出 — 它还从撞击角度旋转：

```js
const victimRot = victimP * -VICTIM_KICK_DEG; // 滑动时旋转
victim.style.transform = `translate(-50%, -50%) translateX(${victimX}px) rotate(${victimRot}deg)`;
```

`VICTIM_KICK_DEG` 通常为 15-25°；选择幅度以匹配感知的侵入者重量。

### 垂直碰撞

侵入者从顶部进入，受害者向下位移。使用 Y 而非 X 的相同数学。视觉感觉像"重量落在上面"。

### 稳定后晃动

在侵入者中心后，在静止前有一个阻尼正弦晃动（`±WOBBLE_AMP_DEG` 旋转，在 `WOBBLE_DUR` 上衰减）。在高潮停留前添加"冲击余波"。

```js
const wobble = { p: 0 };
tl.to(
  wobble,
  {
    p: Math.PI * WOBBLE_CYCLES * 2,
    duration: WOBBLE_DUR,
    ease: "none",
    onUpdate: () => {
      const rot =
        Math.sin(wobble.p) * WOBBLE_AMP_DEG * (1 - wobble.p / (Math.PI * WOBBLE_CYCLES * 2)); // 线性衰减
      intruder.style.transform = `translate(-50%, -50%) rotate(${rot}deg)`;
    },
  },
  DRIVER_AT + DRIVER_DUR,
);
```

### 多受害者涟漪

侵入者位移多个对齐的卡片，每个受害者获得略微延迟的退出（级联涟漪）。每个受害者的 `victimP` 使用不同的驱动器相位偏移。

## 关键原则

- **单一驱动器 = 单一真相源** — 进入弹簧驱动**两个**运动。侵入者和受害者的独立补间破坏因果链接；它们只是恰好时间上接近，而非碰撞。
- **受害者在驱动器的分数处完成** — 到侵入者到达中心时，受害者**已消失**。"撞击"是它们重叠的时刻；之后受害者只是退出侵入者将要填充的空间。
- **方向动量传递** — 侵入者从正 X → 受害者向负 X 移动。相同轴。如果它们在不同轴上移动，看起来像它们互相穿过，而非碰撞。
- **侵入者的 z-index 高于受害者** — 重叠期间，侵入者应出现在**前面**（它是碰撞的"赢家"）。否则受害者看起来像隧道穿过了。
- **侵入者以旋转进入，稳定为平面** — 添加动量可视化。小的初始倾斜 → 稳定时 0° 读作"旋转进入然后着陆。"
- **冲击后的高潮停留** — 冲击是标题节拍。冲击后停留是新内容被阅读的地方。

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **单一驱动器，同一 onUpdate 中的多个派生值** — 不要使用单独的 `tl.to()` 调用来补间侵入者和受害者；使用一个驱动器并在其 onUpdate 内计算两者
- **`.scene` 上设置 `overflow: hidden`** — 舞台外运动超出画面
- **两张卡片上设置 `will-change: transform, opacity`**
- **侵入者的 z-index > 受害者的 z-index** — 显式设置，不依赖 DOM 顺序

## 组合

- [hacker-flip-3d.md](hacker-flip-3d.md) — 侵入者在进入阶段通过黑客翻转揭示文本
- [sine-wave-loop.md](sine-wave-loop.md) — 高潮停留期间侵入者的空闲呼吸
- [vertical-spring-ticker.md](vertical-spring-ticker.md) — 侵入者是一个 ticker，"推"出之前的内容

## 与 HF 技能配对

- `/hyperframes-animation` — 单一驱动器，多值 onUpdate
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
