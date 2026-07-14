---
name: viewport-change
description: 虚拟摄像机 — 通过变换包裹所有场景内容的容器来模拟缩放/平移/焦点锁定。摄像机右移 → 世界左移。
metadata:
  tags: viewport, camera, zoom, pan, focus-lock, virtual-camera
---

# 视口变化（虚拟摄像机）

通过变换包裹**所有**场景内容的容器来模拟摄像机效果（缩放/平移/焦点锁定在移动元素上）。"世界"向感知摄像机的反方向移动。与 [multi-phase-camera](multi-phase-camera.md)（2-3 个离散阶段 + 漂移）不同 — viewport-change 是一个连续的缩放/平移，常用于跟随移动元素的焦点锁定。

## 工作原理

摄像机意图 → 世界变换：

- 摄像机**右移** → 世界 `translateX(-distance)`
- 摄像机**放大** → 世界 `scale(>1)`
- 摄像机**跟随元素 X** → 世界 `translateX(viewportCenter - elementWorldX)` 每帧更新

包裹容器持有摄像机变换；内部的元素在"世界空间"中位置不变。

**单元素复合变换（此规则的形式）。** 缩放和平移都位于一个包裹容器上，作为 `translate(x, y) scale(S)`。CSS 先应用 scale，然后 translate（从右到左的矩阵组合），因此世界偏移 `(ox, oy)` 处的点落在屏幕上的 `(S × ox + x, S × oy + y)`。要将目标映射到视口中心：

```
T = -offset × S
```

这与 [coordinate-target-zoom](coordinate-target-zoom.md)**不同**，后者使用两个嵌套包裹容器（外部缩放，内部平移）并推导出 `T = -offset`（与 S 无关）。当你想通过 `onUpdate` 更新摄像机状态（`cam.scale`、`cam.x`、`cam.y`）的单一真相源时，使用此规则的单包裹容器形式；当缩放和平移可以独立补间并共享缓动时，使用嵌套包裹容器。

## HTML

```html
<div
  class="scene"
  id="viewport-scene"
  data-composition-id="viewport-scene"
  data-start="0"
  data-duration="5"
  data-track-index="0"
>
  <div class="world" id="world">
    <div class="content">
      <div class="hero" id="hero">{Brand}</div>
      <div class="tagline">{tagline}</div>
      <div class="cta-row">
        <div class="cta" id="cta">{ctaUrl}</div>
      </div>
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
  background: {bgGradient};
  font-family: {font};
}
.world {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  transform-origin: 50% 50%;
  will-change: transform;
}
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: CONTENT_GAP;
  text-align: center;
}
.hero {
  font-size: HERO_FONT_SIZE;
  font-weight: 900;
  letter-spacing: HERO_LETTER_SPACING;
  text-transform: uppercase;
  color: {textColor};
}
.tagline {
  font-size: TAGLINE_FONT_SIZE;
  font-weight: 600;
  color: {labelColor};
}
.cta {
  display: inline-block;
  padding: CTA_PADDING_Y CTA_PADDING_X;
  font-family: {monoFont};
  font-size: CTA_FONT_SIZE;
  font-weight: 700;
  letter-spacing: CTA_LETTER_SPACING;
  color: {accentColor};
  text-transform: uppercase;
  background: {ctaBg};
  border: 1px solid {ctaBorder};
  border-radius: CTA_BORDER_RADIUS;
}
```

## GSAP 时间线

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const world = document.getElementById("world");

  // 摄像机状态 — 单一真相源。世界变换在 applyCamera() 内部从此对象组合，
  // 使变换字符串顺序稳定。
  const cam = { scale: 1, x: 0, y: 0 };

  function applyCamera() {
    world.style.transform = `translate(${cam.x}px, ${cam.y}px) scale(${cam.scale})`;
  }
  applyCamera();

  // 阶段 1 — 中性摄像机下的内容揭示
  tl.from(".hero", { opacity: 0, y: HERO_Y, duration: HERO_DUR, ease: "power3.out" }, HERO_START);
  tl.from(
    ".tagline",
    { opacity: 0, y: TAGLINE_Y, duration: TAGLINE_DUR, ease: "power3.out" },
    TAGLINE_START,
  );

  // 阶段 2 — 放大到 CTA（单元素复合变换）
  // CSS 先应用 scale 再 translate：世界点 (ox, oy) 落在
  // (S × ox + x, S × oy + y)。解 S × offset + T = 0 → T = -offset × S。
  // 这与 coordinate-target-zoom（嵌套包裹容器，T = -offset）不同。
  const counterY = -TARGET_OFFSET_Y * TARGET_SCALE;

  tl.to(
    cam,
    {
      scale: TARGET_SCALE,
      y: counterY,
      duration: ZOOM_DUR,
      ease: "power3.inOut",
      onUpdate: applyCamera,
    },
    ZOOM_START,
  );

  // 阶段 3 — 缩放稳定后 CTA 揭示/停留
  tl.from(
    "#cta",
    {
      opacity: 0,
      scale: CTA_REVEAL_SCALE,
      duration: CTA_REVEAL_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`,
    },
    CTA_REVEAL_START,
  );

  window.__timelines["viewport-scene"] = tl;
</script>
```

## 缩放值参考

| 效果       | 缩放值      | 感觉                              |
| ---------- | ----------- | --------------------------------- |
| 微妙       | 1.02 - 1.05 | 几乎不可察觉 — "专业"             |
| 中等       | 1.05 - 1.15 | "哒哒"强调                        |
| 明显       | 1.15 - 1.30 | 聚焦区域                          |
| 戏剧性     | 1.5 - 2.5   | 元素填满屏幕                      |
| 全屏       | 3.0+        | 元素覆盖视口                      |

| 感知阈值 | 结果               |
| -------- | ------------------ |
| < 5%     | 不可察觉           |
| 10-15%   | 舒适的强调         |
| > 30%    | 电影感 / 戏剧性    |

## 变体

### 焦点锁定（摄像机跟随移动的光标/角色）

对于在世界中移动的元素，将其保持在固定的屏幕 X 位置。每帧计算世界偏移：

```js
const focusEl = document.querySelector(".moving-cursor");
const targetScreenX = VIEWPORT_WIDTH * FOCUS_SCREEN_X_FRAC;
const focusUpdate = { p: 0 };
tl.to(
  focusUpdate,
  {
    p: 1,
    duration: FOLLOW_DUR,
    ease: "power2.inOut",
    onUpdate: () => {
      const rect = focusEl.getBoundingClientRect();
      const focusWorldX = rect.left + rect.width / 2;
      cam.x = targetScreenX - focusWorldX;
      applyCamera();
    },
  },
  FOLLOW_START,
);
```

### 复合缩放（多阶段）

将两个缩放补间相乘实现复合效果：

```js
const scaleUp = { v: 1 };
const scaleDown = { v: 1 };
function applyCompositeCamera() {
  cam.scale = scaleUp.v * scaleDown.v;
  applyCamera();
}
tl.to(
  scaleUp,
  { v: SCALE_UP_TARGET, duration: SCALE_UP_DUR, onUpdate: applyCompositeCamera },
  SCALE_UP_START,
);
tl.to(
  scaleDown,
  { v: SCALE_DOWN_TARGET, duration: SCALE_DOWN_DUR, onUpdate: applyCompositeCamera },
  SCALE_DOWN_START,
);
```

### 摄像机模式过渡（居中 → 跟随）

通过 0→1 权重补间在两个摄像机模式之间交叉淡入淡出。权重为 0 时模式 A，权重为 1 时模式 B，中间值插值。

## 如何选择值

### 布局（CSS）

- **CONTENT_GAP** — 主角、标语和 CTA 之间的垂直间距。
  - 范围：16-48 px
  - 效果：小 → 紧密堆叠（logo 组合感）；大 → 通风、编辑风格
- **HERO_FONT_SIZE / TAGLINE_FONT_SIZE / CTA_FONT_SIZE** — 排版层次。
  - 范围：主角 >> 标语 > CTA（主角是品牌标记，CTA 是可操作页脚）
  - 约束：主角必须在中性摄像机缩小**时**和缩放**期间**放大时都保持可读 — 选择中性摄像机时的尺寸，缩放只会放大它
- **HERO_LETTER_SPACING / CTA_LETTER_SPACING** — 大写跟踪。
  - 范围：大写展示字体 4-10 px；句子大小写 0
- **CTA_PADDING_X / CTA_PADDING_Y / CTA_BORDER_RADIUS** — CTA 文本周围的胶囊几何。
  - 约束：`CTA_BORDER_RADIUS ≥ CTA_FONT_SIZE` 以保持胶囊端部完全圆角

### 阶段 1 — 内容揭示

- **HERO_START** — 主角开始淡入的时间。
  - 范围：0.2-0.5 秒（内容出现前黑色画面的小偏移量）
- **HERO_DUR** — 主角淡入时长。
  - 范围：0.6-1.2 秒
- **HERO_Y** — 主角淡入前初始 Y 偏移（以 px 为单位）。
  - 范围：16-48 px
- **TAGLINE_START** — 标语开始淡入的时间。
  - 约束：`≥ HERO_START + 0.3`（让主角先着陆，使眼睛读作自上而下）
- **TAGLINE_DUR / TAGLINE_Y** — 与主角相同的形状，通常更小（`TAGLINE_Y` 为 `HERO_Y` 的一半）。

### 阶段 2 — 缩放

- **TARGET_OFFSET_Y** — 中性摄像机下 CTA 距视口中心的 Y 偏移（以 px 为单位）。
  - 约束：从布局推导，**不是**自由参数。通过 `getBoundingClientRect()` 测量或从 `CONTENT_GAP + (HERO_HEIGHT + TAGLINE_HEIGHT) / 2` 计算。符号重要 — 正 = 中心下方。
- **TARGET_SCALE** — 世界的最终放大倍数。
  - 范围：1.3×（适度）→ 1.6-2.0×（典型 CTA 缩放）→ 3×+（电影感）
  - 约束：栅格源媒体需要 `sourceResolution ≥ rendered × TARGET_SCALE`；文本在任何缩放级别都保持清晰
- **ZOOM_START** — 缩放开始时间。
  - 约束：`≥ TAGLINE_START + TAGLINE_DUR + viewer-scan-time`（内容着陆后给观看者 ~0.5 秒，然后摄像机再移动）
- **ZOOM_DUR** — 缩放补间时长。
  - 范围：1.0-2.0 秒；低于 0.8 秒感觉像传送，超过 2.5 秒拖沓

### 阶段 3 — CTA 揭示 + 停留

- **CTA_REVEAL_START** — CTA 弹出时间。
  - 约束：`≥ ZOOM_START + ZOOM_DUR × 0.9`（在缩放接近结束时开始，使 CTA 与摄像机一起"着陆"）
- **CTA_REVEAL_DUR** — CTA 淡入/弹出时长。
  - 范围：0.4-0.8 秒
- **CTA_REVEAL_SCALE** — CTA 弹出前的初始缩放。
  - 范围：0.85-0.95（小于 1 → 增长到位）；>1.0 反转成缩小到位感
- **BOUNCE_FACTOR** — `back.out(${BOUNCE_FACTOR})` 的过冲系数。
  - 范围：1.2-2.5；较低 = 微妙稳定，较高 = 明显过冲。
  - 参考：缓动族选项：`back.out`（过冲然后稳定）、`elastic.out`（振荡）、`power3.out`（干净减速，无过冲）
- **DWELL_DUR** — `CTA_REVEAL_START + CTA_REVEAL_DUR` 之后直到 `data-duration` 结束的隐式保持。
  - 范围：≥ 1.0 秒（参见关键原则中的"高潮停留"）

### 焦点锁定变体

- **VIEWPORT_WIDTH** — 组合宽度（以 px 为单位）。实际值（根元素上的 `data-width`）；非抽象值。
- **FOCUS_SCREEN_X_FRAC** — 锁定聚焦元素在屏幕上的位置。
  - 范围：0.4-0.7（三分法位置）；0.5 是正中心
- **FOLLOW_START / FOLLOW_DUR** — 跟随摄像机何时启动以及持续多久。
  - 约束：`FOLLOW_DUR` 匹配聚焦元素运动的时间

### 复合缩放变体

- **SCALE_UP_TARGET / SCALE_DOWN_TARGET** — 通过 `cam.scale = scaleUp.v * scaleDown.v` 组合的乘数。
  - 效果：将缓慢推进（`SCALE_UP_TARGET` ~1.15）与短暂释放（`SCALE_DOWN_TARGET` ~0.9）组合，形成呼吸/冲击形状
- **SCALE_UP_START / SCALE_UP_DUR / SCALE_DOWN_START / SCALE_DOWN_DUR** — 每个乘数的阶段时间。

### 颜色标记

- **{bgGradient}** — 场景背景（通常为暗色径向暗角，使边缘在缩放揭示时消失）
- **{textColor}** — 主角文本；与 `{bgGradient}` 的最高对比度
- **{labelColor}** — 标语/辅助文案；比 `{textColor}` 柔和一级
- **{accentColor}** — CTA 文本 + 边框；揭示时弹出的保留色相
- **{ctaBg} / {ctaBorder}** — 从 `{accentColor}` 衍生的半透明填充（典型 10-15% / 35-45% 不透明度的 `rgba`）

### 字体标记

- **{font}** — 无衬线正文/主角字体栈（例如 `"Inter", sans-serif`）
- **{monoFont}** — 等宽 CTA 字体栈（例如 `"JetBrains Mono", monospace`）；保留给 URL/代码风格 CTA，使其读作可操作

## 关键原则

- **世界向感知摄像机的反方向移动** — 摄像机右移 = 世界包裹容器上的 `translateX(-x)`。确保这个符号正确，否则一切都会朝错误方向移动。
- **单包裹容器变换顺序重要** — `translate(x, y) scale(S)` 先应用 scale；反向平移是 `T = -offset × S`。与嵌套包裹容器形式（`T = -offset`）混淆会导致目标在缩放变化时偏离中心。
- **`.scene` 上必须有 `overflow: hidden`** — 在任何非 1.0 缩放时，世界变换会露出边缘或将内容推出画面。
- **世界包裹容器上的 `transform-origin: 50% 50%`** — 居中缩放是数学假设的。
- **背景在 `.scene` 上，**不是**在 `.world` 上** — 如果背景在世界容器上，变换世界会扭曲/平移背景。
- **通过 `cam` 对象 + `applyCamera()` 的单一真相源** — 缩放和平移同时变化时，在一个地方写入。否则变换字符串组合顺序不可预测。
- **微妙连续运动 > 突然大缩放** — 为了自然的產品视频感觉，使用 1.05-1.15× 缩放持续 2-3 秒。大于 1.3× 的缩放读作戏剧性叙事时刻，保留使用。
- **高潮停留 >=1 秒** — 缩放稳定后，组合必须继续 >=1 秒，使观看者能够阅读焦点。

## 关键约束

- **时间线必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **`.world` 上无 CSS `transition`** — 与 GSAP 竞争
- **`.world` 上设置 `will-change: transform`**
- **`.scene` 上设置 `overflow: hidden`**
- **`.world` 上设置 `transform-origin: 50% 50%`**
- **背景在 `.scene` 上** — 绝不在 `.world` 上
- **缩放和平位移共享一个 `onUpdate`** — 两者都从 `cam` 读取并一起写入复合变换字符串；从不将它们分散到直接触碰 `world.style.transform` 的补间中

## 组合

- [multi-phase-camera.md](multi-phase-camera.md) — 多阶段摄像机的一个阶段内的视口变化
- [coordinate-target-zoom.md](coordinate-target-zoom.md) — 偏离中心缩放的替代方案（嵌套包裹容器，`T = -offset` 形式）
- [sine-wave-loop.md](sine-wave-loop.md) — 视口稳定后的空闲微漂移

## 与 HF 技能配对

- `/hyperframes-animation` — 写入复合变换的单一补间
- `/hyperframes-core` — 组合接线
- `/hyperframes-cli` — `hyperframes lint`
