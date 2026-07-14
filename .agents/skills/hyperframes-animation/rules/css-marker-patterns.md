# 标记高亮的 CSS 模式

所有五种 MarkerHighlight.js 绘制模式的纯 CSS + GSAP 实现。用于 HyperFrames 组合中的确定性渲染 — 无外部库依赖，完全 GSAP 时间线控制。

## 内容

- [1. 高亮模式](#1-高亮模式) — 文本后的黄色标记扫过
- [2. 圆圈模式](#2-圆圈模式) — 文本周围手绘椭圆
- [3. 爆发模式](#3-爆发模式) — 从文本辐射的线条
- [4. 涂鸦模式](#4-涂鸦模式) — 文本上的混乱涂鸦
- [5. 素描模式](#5-素描模式) — 粗糙矩形轮廓

## 1. 高亮模式

文本后的黄色标记扫过。最常见的模式。

```html
<span class="mh-highlight-wrap">
  <span class="mh-highlight-bar" id="hl-1"></span>
  <span class="mh-highlight-text">高亮文本</span>
</span>
```

```css
.mh-highlight-wrap {
  position: relative;
  display: inline;
}
.mh-highlight-bar {
  position: absolute;
  top: 0;
  left: -6px;
  right: -6px;
  bottom: 0;
  background: #fdd835;
  opacity: 0.35;
  transform: scaleX(0);
  transform-origin: left center;
  border-radius: 3px;
  z-index: 0;
}
.mh-highlight-text {
  position: relative;
  z-index: 1;
}
```

```js
// 从左扫入
tl.to("#hl-1", { scaleX: 1, duration: 0.5, ease: "power2.out" }, 0.6);

// 可选：手绘感的倾斜
// gsap.set("#hl-1", { skewX: -2 });
```

### 多行高亮

跨多行错开条：

```js
tl.to(
  ".mh-highlight-bar",
  {
    scaleX: 1,
    duration: 0.5,
    ease: "power2.out",
    stagger: 0.3,
  },
  0.6,
);
```

## 2. 圆圈模式

文本周围手绘圆圈。使用 `border-radius: 50%` 配合轻微旋转以获得有机感。

```html
<span class="mh-circle-wrap">
  <span class="mh-circle-text" id="circle-word">重要</span>
  <span class="mh-circle-ring" id="circle-1"></span>
</span>
```

```css
.mh-circle-wrap {
  position: relative;
  display: inline;
}
.mh-circle-text {
  position: relative;
  z-index: 1;
}
.mh-circle-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 130%;
  height: 160%;
  transform: translate(-50%, -50%) rotate(-3deg) scale(0);
  border: 3px solid #e53935;
  border-radius: 50%;
  pointer-events: none;
  z-index: 0;
}
```

```js
// 圆圈带晃动缩放进入
tl.to(
  "#circle-1",
  {
    scale: 1,
    rotation: -3,
    duration: 0.6,
    ease: "back.out(1.7)",
    transformOrigin: "center center",
  },
  0.7,
);
```

### 变体

```css
/* 更紧的圆圈（用于短词） */
.mh-circle-ring.tight {
  width: 150%;
  height: 180%;
}

/* 方圆形圈（圆角矩形） */
.mh-circle-ring.rounded {
  border-radius: 30%;
  width: 120%;
  height: 140%;
}

/* 椭圆（宽大于高） */
.mh-circle-ring.ellipse {
  width: 150%;
  height: 130%;
  border-radius: 50%;
}
```

## 3. 爆发模式

从文本中心辐射的线条。每行是一个定位的 div，旋转到其角度。

```html
<span class="mh-burst-wrap">
  <span class="mh-burst-text">哇</span>
  <span class="mh-burst-container" id="burst-1">
    <span class="mh-burst-line" style="--angle: 0deg; --len: 70px;"></span>
    <span class="mh-burst-line" style="--angle: 30deg; --len: 55px;"></span>
    <span class="mh-burst-line" style="--angle: 60deg; --len: 80px;"></span>
    <span class="mh-burst-line" style="--angle: 90deg; --len: 45px;"></span>
    <span class="mh-burst-line" style="--angle: 120deg; --len: 65px;"></span>
    <span class="mh-burst-line" style="--angle: 150deg; --len: 75px;"></span>
    <span class="mh-burst-line" style="--angle: 180deg; --len: 50px;"></span>
    <span class="mh-burst-line" style="--angle: 210deg; --len: 60px;"></span>
    <span class="mh-burst-line" style="--angle: 240deg; --len: 80px;"></span>
    <span class="mh-burst-line" style="--angle: 270deg; --len: 40px;"></span>
    <span class="mh-burst-line" style="--angle: 300deg; --len: 70px;"></span>
    <span class="mh-burst-line" style="--angle: 330deg; --len: 55px;"></span>
  </span>
</span>
```

```css
.mh-burst-wrap {
  position: relative;
  display: inline;
}
.mh-burst-text {
  position: relative;
  z-index: 2;
}
.mh-burst-container {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  z-index: 1;
}
.mh-burst-line {
  position: absolute;
  display: block;
  width: 3px;
  height: var(--len);
  background: #1e88e5;
  left: -1.5px;
  top: calc(-1 * var(--len));
  transform: rotate(var(--angle));
  transform-origin: bottom center;
  opacity: 0;
}
```

```js
// 所有行同时向外爆发，轻微错开
tl.fromTo(
  "#burst-1 .mh-burst-line",
  { scaleY: 0, opacity: 0 },
  { scaleY: 1, opacity: 1, duration: 0.4, ease: "power2.out", stagger: 0.03 },
  0.7,
);
```

**变化线条长度**（40-80px 范围）以获得有机、手绘感觉。等长看起来机械。

## 4. 涂鸦模式

通过 `stroke-dashoffset` 绘制自身的波浪 SVG 下划线和删除线。

```html
<span class="mh-scribble-wrap">
  <span class="mh-scribble-text">带下划线的文本</span>
  <svg class="mh-scribble-svg" viewBox="0 0 500 24" preserveAspectRatio="none">
    <path
      id="scribble-1"
      d="M0,12 Q31,0 62,12 Q93,24 125,12 Q156,0 187,12 Q218,24 250,12 Q281,0 312,12 Q343,24 375,12 Q406,0 437,12 Q468,24 500,12"
      fill="none"
      stroke="#FDD835"
      stroke-width="3"
      stroke-linecap="round"
    />
  </svg>
</div>
```

```css
.mh-scribble-wrap {
  position: relative;
  display: inline;
}
.mh-scribble-text {
  position: relative;
  z-index: 1;
}
.mh-scribble-svg {
  position: absolute;
  left: 0;
  bottom: -6px;
  width: 100%;
  height: 24px;
  z-index: 0;
}
```

```js
// 测量路径长度并设置初始虚线状态
var path = document.querySelector("#scribble-1");
var len = path.getTotalLength();
gsap.set(path, { strokeDasharray: len, strokeDashoffset: len });

// 绘制线条
tl.to(
  "#scribble-1",
  {
    strokeDashoffset: 0,
    duration: 0.8,
    ease: "power1.inOut",
  },
  0.7,
);
```

### 删除线变体

将 SVG 定位在 `top: 50%; transform: translateY(-50%)` 而非 `bottom: -6px`。

### 波浪路径生成器

缩放路径的 viewBox 宽度以匹配文本宽度。波形模式 `Q x1,y1 x2,y2` 在 `y=0` 和 `y=24` 之间交替以获得自然晃动。调整控制点以获得更紧或更松的波浪：

- **紧波浪**：更小的 x 增量（每半波 25px）
- **松波浪**：更大的 x 增量（每半波 50px）
- **振幅**：改变 y 范围（标准 0-24，微妙 0-16）

## 5. 素描模式

去强调文本上的交叉排线。多条斜线创建"划掉"效果。

```html
<span class="mh-sketchout-wrap">
  <span class="mh-sketchout-text">旧价格</span>
  <span class="mh-sketchout-lines" id="sketchout-1">
    <span class="mh-sketchout-line mh-sketchout-fwd"></span>
    <span class="mh-sketchout-line mh-sketchout-bwd"></span>
  </span>
</span>
```

```css
.mh-sketchout-wrap {
  position: relative;
  display: inline;
}
.mh-sketchout-text {
  position: relative;
  z-index: 0;
}
.mh-sketchout-lines {
  position: absolute;
  top: 0;
  left: -4px;
  right: -4px;
  bottom: 0;
  overflow: hidden;
  z-index: 1;
}
.mh-sketchout-line {
  position: absolute;
  display: block;
  top: 50%;
  left: 0;
  width: 100%;
  height: 2px;
  background: #e53935;
  transform-origin: left center;
  transform: scaleX(0);
}
.mh-sketchout-fwd {
  transform: scaleX(0) rotate(-12deg);
}
.mh-sketchout-bwd {
  transform: scaleX(0) rotate(12deg);
}
```

```js
// 正斜线先绘制
tl.to(
  "#sketchout-1 .mh-sketchout-fwd",
  {
    scaleX: 1,
    duration: 0.3,
    ease: "power2.out",
  },
  1.0,
);

// 反斜线跟随
tl.to(
  "#sketchout-1 .mh-sketchout-bwd",
  {
    scaleX: 1,
    duration: 0.3,
    ease: "power2.out",
  },
  1.15,
);
```

## 在字幕中组合模式

使用模式循环在字幕组中实现视觉多样性：

```js
var MODES = ["highlight", "circle", "burst", "scribble"];

GROUPS.forEach(function (group, gi) {
  var mode = MODES[gi % MODES.length];
  // 将模式的 CSS 模式应用于此组中的强调词
  group.emphasisWords.forEach(function (word) {
    applyMode(word.el, mode, tl, word.start);
  });
});
```

每 2-3 组循环一次用于高能量，每 3-4 组用于中等，每 4-5 组用于低能量。
