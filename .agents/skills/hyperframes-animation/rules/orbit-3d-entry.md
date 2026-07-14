---
name: orbit-3d-entry
description: 元素从 3D 空间翻转入场，然后稳定到围绕焦点的连续椭圆轨道。
metadata:
  tags: orbit, 3d, flip, ellipse, circular, icon, entry, continuous
---

# 带 3D 入场的轨道

元素从 3D 空间翻转入场（rotateX + rotateY + translateZ），然后过渡到围绕焦点的连续椭圆轨道。与一次性揭示不同 — 轨道持续运行。

## 工作原理

每个元素两个阶段：

1. **入场（每元素）**：GSAP 补间从隐藏的 3D 方向（`rotateX`、`rotateY`、负 `z`）到平面（`rotateX: 0, rotateY: 0, z: 0`）。翻转使用弹簧样缓动（`back.out`）。
2. **轨道（入场后）**：围绕中心点的连续三角位置。元素的 `x` 和 `y` 平移由 `cos(t)` 和 `sin(t)` 以慢角速度驱动。

轨道在**时间线内**运行 — 而非通过 `requestAnimationFrame` — 使 HF 逐帧定位保持确定性。

## HTML

```html
<div
  class="scene"
  id="orbit-scene"
  data-composition-id="orbit-scene"
  data-start="0"
  data-duration="5"
  data-track-index="0"
>
  <div class="orbit-stage">
    <div class="orbit-item" data-angle="0">{glyph1}</div>
    <div class="orbit-item" data-angle="60">{glyph2}</div>
    <div class="orbit-item" data-angle="120">{glyph3}</div>
    <div class="orbit-item" data-angle="180">{glyph4}</div>
    <div class="orbit-item" data-angle="240">{glyph5}</div>
    <div class="orbit-item" data-angle="300">{glyph6}</div>
    <div class="orbit-center">{centerLabel}</div>
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
  background: {sceneBackground};
  perspective: 1800px; /* 必需 — 没有透视，rotateX/Y 会平面化 */
}
.orbit-stage {
  position: relative;
  width: 1000px;
  height: 700px;
  display: grid;
  place-items: center;
  transform-style: preserve-3d;
}
.orbit-item {
  position: absolute;
  /* 项目位于舞台中心；GSAP 沿轨道平移它们。 */
  top: 50%;
  left: 50%;
  width: 140px;
  height: 140px;
  display: grid;
  place-items: center;
  background: {accentColor};
  border-radius: 50%;
  font-family: {font};
  font-weight: 900;
  font-size: 64px;
  color: {itemTextColor};
  transform-style: preserve-3d;
  will-change: transform;
  box-shadow: 0 12px 36px {accentShadowColor};
}
.orbit-center {
  position: relative;
  z-index: 5;
  font-family: {font};
  font-weight: 900;
  font-size: 96px;
  letter-spacing: 8px;
  color: {centerTextColor};
  text-transform: uppercase;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const items = document.querySelectorAll(".orbit-item");
  // RADIUS_X、RADIUS_Y、ORBIT_DURATION、ENTRY_DUR、STAGGER、FLIP_BACK、CENTER_BACK
  // — 都是命名常量；值见下方"如何选择值"。
  const RADIUS_Y = RADIUS_X * Y_TO_X_RATIO; // 透视展平的椭圆

  items.forEach((el, i) => {
    const initialAngleDeg = Number(el.dataset.angle);
    const initialAngleRad = (initialAngleDeg / 360) * Math.PI * 2;
    const startX = Math.cos(initialAngleRad) * RADIUS_X;
    const startY = Math.sin(initialAngleRad) * RADIUS_Y;

    // 1) 以不透明度 0 放置在轨道位置 — 在任何补间触发之前
    gsap.set(el, {
      xPercent: -50,
      yPercent: -50,
      x: startX,
      y: startY,
      rotateX: ROTATE_X_FROM,
      rotateY: ROTATE_Y_FROM,
      z: Z_FROM,
      opacity: 0,
      scale: SCALE_FROM,
    });

    // 2) 阶段 1 — 在轨道位置原位翻转进入
    tl.to(
      el,
      {
        rotateX: 0,
        rotateY: 0,
        z: 0,
        opacity: 1,
        scale: 1,
        duration: ENTRY_DUR,
        ease: `back.out(${FLIP_BACK})`,
      },
      i * STAGGER,
    );

    // 3) 阶段 2 — 通过 0→1 进度补间驱动连续轨道
    const orbitState = { p: 0 };
    tl.to(
      orbitState,
      {
        p: 1,
        duration: ORBIT_DURATION,
        ease: "none",
        onUpdate: () => {
          const angle = initialAngleRad + orbitState.p * Math.PI * 2;
          const x = Math.cos(angle) * RADIUS_X;
          const y = Math.sin(angle) * RADIUS_Y;
          // 按轨道 Y 的 z-index — 参见关键原则中的"中心标签间距"
          // 以获取当存在中心标签时有上限范围的表单。
          el.style.zIndex = String(Math.round(y + RADIUS_Y));
          el.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
        },
      },
      i * STAGGER + ENTRY_DUR,
    );
  });

  // 中心标签在几个轨道项目着陆后淡入
  tl.from(
    ".orbit-center",
    { opacity: 0, scale: 0.6, duration: ENTRY_DUR, ease: `back.out(${CENTER_BACK})` },
    CENTER_FADE_AT,
  );

  window.__timelines["orbit-scene"] = tl;
</script>
```

## 如何选择值

- **RADIUS_X** — 轨道椭圆的水平半径（px）
  - 范围：300–900 px
  - 效果：小半径读作紧密群组；大半径将环铺展到画面中，让大的中心元素呼吸
  - 约束：必须在每个角度从水平方向避让中心元素 — 参见关键原则中的 `RADIUS_X * min(|cos(θ)|) ≥ L_w + I_w + 间距` 规则
  - 参考：../../examples/cta-orbit-collapse.html 使用 480
- **Y_TO_X_RATIO** — `RADIUS_Y / RADIUS_X`，轨道的透视展平
  - 范围：0.4–0.7
  - 效果：低值读作从上方看到的近乎水平的盘；接近 1 的值读作面向摄像机的平面
  - 约束：保持 < 1 — 轨道看起来应该像一个倾斜的环，而非正面光环
  - 参考：../../examples/cta-orbit-collapse.html 使用 ≈ 0.58
- **ORBIT_DURATION** — 一次完整公转的秒数
  - 范围：4–25 秒（环境背景取较长，活跃功能运动取较短）
  - 效果：短时长看起来狂乱；长时长读作漂移/平静
  - 约束：必须 ≥ 轨道在屏幕上的时间，否则补间结束，项目停止
  - 参考：../../examples/cta-orbit-collapse.html 使用 ~25 秒有效时间（轨道速度 0.25 rad/s）
- **ENTRY_DUR** — 每元素翻转入场时长
  - 范围：0.4–0.8 秒
  - 效果：短感觉有力；长感觉庄重
  - 约束：必须 ≤ 第一个和最后一个元素开始之间的间隔，以免级联重叠到不连贯
  - 参考：../../examples/cta-orbit-collapse.html 使用 0.55 秒
- **STAGGER** — 连续元素入场之间的延迟
  - 范围：0.06–0.12 秒
  - 效果：低于 ~0.06 秒读作"爆米花"；高于 ~0.12 秒读作拖沓
  - 约束：总级联 `(n - 1) * STAGGER` 应在下一个场景阶段开始前完成
  - 参考：../../examples/cta-orbit-collapse.html 使用 0.10 秒
- **FLIP_BACK** — 翻转的 `back.out(<n>)` 过冲
  - 范围：1.2–2.0
  - 效果：低端是柔和到达；高端快照带有明显过冲
  - 约束：如果两者接近触发，与较平静的 `CENTER_BACK` 配对 — 竞争的过冲会互相抵消
  - 参考：../../examples/cta-orbit-collapse.html 使用 1.4
- **CENTER_BACK** — 中心标签淡入的 `back.out(<n>)` 过冲
  - 范围：1.2–1.8
  - 效果：低端在繁忙轨道下保持标签平静；高端给它一个小小的"弹出"到达感
  - 参考：../../examples/cta-orbit-collapse.html 使用 1.4
- **CENTER_FADE_AT** — 中心标签淡入的时间（秒）
  - 范围：刚好在前 2–4 个元素着陆后
  - 效果：太早与级联竞争；太晚在轨道中心留下空洞
  - 参考：../../examples/cta-orbit-collapse.html 在场景前部开始中心品牌
- **ROTATE_X_FROM / ROTATE_Y_FROM / Z_FROM / SCALE_FROM** — 初始 3D 方向
  - 范围：rotateX ±60° 到 ±120°；rotateY ±45° 到 ±120°；z −200 到 −400；scale 0.2–0.6
  - 效果：更高的绝对旋转 + 更深的负 z = 更戏剧性的"卡片从深处翻出"；较低 = 微妙重定向
  - 约束：选择一个与场景透视一致的方向；跨项目混合正负 rotateY 读作噪声
  - 参考：../../examples/cta-orbit-collapse.html 使用 rotateX 90、rotateY −45、z −100、scale 0

## 变体

### 塌缩到中心

要反转 — 轨道然后向内塌缩 — 通过在最后阶段将两个半径乘以一个 1→0 驱动器来将 `RADIUS_X` 和 `RADIUS_Y` 插值到 0：

```js
const collapse = { r: 1 };
tl.to(
  collapse,
  {
    r: 0,
    duration: COLLAPSE_DUR,
    ease: "power3.inOut",
    onUpdate: () =>
      items.forEach((el) => {
        const a = (Number(el.dataset.angle) / 360) * Math.PI * 2;
        const x = Math.cos(a) * RADIUS_X * collapse.r;
        const y = Math.sin(a) * RADIUS_Y * collapse.r;
        el.style.transform = `translate(-50%,-50%) translate(${x}px,${y}px) scale(${collapse.r})`;
      }),
  },
  COLLAPSE_AT,
);
```

### 倾斜轨道平面

为了更戏剧性的 3D 轨道，在 X 轴上旋转整个 `.orbit-stage`：

```css
.orbit-stage {
  transform: rotateX(25deg);
}
```

赤道上方/下方渲染的项目在平面上视觉弧形穿过。

## 关键原则

- **场景根元素上的 `perspective` 必需** — 没有它，rotateX/Y 读作 2D 缩放，翻转入场看起来平坦
- **舞台和每个项目上的 `transform-style: preserve-3d`** — 保持 3D 上下文，因为项目有自己的变换
- **错开入场** — 级联读作"蜂群形成"，同时读作"爆米花"。参见"如何选择值"中的 `STAGGER`
- **元素数量 4-12** — 更少感觉空旷，更多拥挤中心
- **❗ 中心标签间距 — translateZ + 有上限的项目 z-index** — 在 `transform-style: preserve-3d` 舞台内，单独使用 `z-index` 不可靠（绘制顺序遵循 Z 位置，而非堆叠上下文 z-index）。为使轨道**永不**遮挡标题：
  1. 将中心标签向前推：`transform: translateZ(220px); z-index: 9999;`
  2. 将轨道项目动态 z-index 限制在 `[1, 50]`，使轨道底部项目仍读作在轨道顶部项目"前面"，但**永不超过中心标签**。例如：`el.style.zIndex = String(1 + Math.round((y + RADIUS_Y) / (2 * RADIUS_Y) * 49));`
  3. **选择 `RADIUS_X` 使项目在所有角度也**水平**避让中心标签。** 如果标签半宽为 `L_w` 且项目半宽为 `I_w`，则 `RADIUS_X` 必须满足 `RADIUS_X * min(|cos(θ_minimum)|) ≥ L_w + I_w + 间距`。对于 60° 角间距的 6 项目轨道，最坏情况是项目间的 `cos(30°) ≈ 0.866`。根据中心标签宽度缩放 `RADIUS_X` — 更重的 wordmark 需要更宽的环。
- **❗ 中心元素是标题** — 轨道是围绕它的装饰性运动。如果轨道主导视线，增加中心元素大小或降低轨道项目不透明度

## 关键约束

- **无 `requestAnimationFrame`** — 轨道必须在时间线内运行，使 HF 确定性逐帧定位
- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **每个项目获得自己的轨道补间** — 不要用 `targets: '.orbit-item'` 共享一个补间，因为每个从不同的 `initialAngle` 开始
- **设置 `will-change: transform`** — 许多同时发生的轨道变换受益于合成器提示
- **不要动画化 `left`/`top`** — 使用 `translate()`（与 `translate(-50%, -50%)` 居中组合）
- **❗ 入场必须在轨道位置原位翻转，不在中心** — 一个 fromTo 其"from"和"to"都有 `x: 0, y: 0` 在阶段 1 将项目保持在舞台中心，因此它在翻转期间与中心标签碰撞（然后在阶段 2 开始时跳到轨道上 — 一个可见的传送）。
  
  正确的模式（见上方 GSAP 时间线）是在添加补间**之前** `gsap.set()` 每个项目在 `(cos(initialAngle)*RADIUS_X, sin(initialAngle)*RADIUS_Y)` 带 `opacity: 0`，然后阶段 1 仅动画化旋转/不透明度/缩放 — 而非平移。项目在其轨道起始点**原位**淡入，阶段 2 从那里平滑接续轨道。

## 组合

- [center-outward-expansion.md](center-outward-expansion.md) — 替代入场模式（爆发，非轨道）；也是轨道塌缩结束的反向驱动器
- [cursor-click-ripple.md](cursor-click-ripple.md) — 当中心元素是用户"点击"以触发塌缩的 CTA 时自然配对
- [sine-wave-loop.md](sine-wave-loop.md) — 在轨道之上的每元素空闲晃动

## 与 HF 技能配对

- `/hyperframes-animation` — 时间线 + `onUpdate` API
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
