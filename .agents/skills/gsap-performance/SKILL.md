---
name: gsap-performance
description: GSAP 性能官方技能 — 优先使用变换、避免布局抖动、will-change、批处理。在优化 GSAP 动画、减少卡顿或用户询问动画性能、FPS 或流畅的 60fps 时使用。
license: MIT
---

# GSAP 性能

## 何时使用此技能

在优化 GSAP 动画以实现流畅的 60fps、减少布局/绘制开销，或用户询问性能、卡顿或快速动画最佳实践时应用。

**相关技能：** 使用 **gsap-core**（变换、autoAlpha）和 **gsap-timeline** 构建动画；ScrollTrigger 性能参见 **gsap-scrolltrigger**。

## 优先使用变换和不透明度

动画 **transform**（`x`、`y`、`scaleX`、`scaleY`、`rotation`、`rotationX`、`rotationY`、`skewX`、`skewY`）和 **opacity** 将工作保留在合成器上，避免布局和大部分绘制。当变换能实现相同效果时，避免动画布局密集属性。

- ✅ 优先使用：**x**、**y**、**scale**、**rotation**、**opacity**。
- ❌ 尽可能避免：**width**、**height**、**top**、**left**、**margin**、**padding**（它们触发布局并可能导致卡顿）。

GSAP 的 **x** 和 **y** 默认使用变换（translate）；使用它们替代 **left**/**top** 进行移动。

## will-change

在将动画的元素上使用 CSS 中的 **will-change**。它提示浏览器提升图层。

```css
will-change: transform;
```

## 批量读取和写入

GSAP 内部会批量更新。当将 GSAP 与直接 DOM 读取/写入或布局相关代码混合使用时，避免以导致重复布局抖动的方式交错读取和写入。优先先完成所有读取，然后进行所有写入（或让 GSAP 一次性处理写入）。

## 许多元素（Stagger、列表）

- 当动画相同时，使用 **stagger** 而非使用手动延迟的多个单独补间；效率更高。
- 对于长列表，考虑**虚拟化**或仅动画可见项；如果导致卡顿，避免创建数百个同时补间。
- 尽可能复用时间线；避免每帧创建新时间线。

## 频繁更新的属性（例如鼠标追随器）

对于频繁更新的属性（例如鼠标追随器的 x/y），优先使用 **gsap.quickTo()**。它复用一个补间而不是在每次更新时创建新补间。

```javascript
let xTo = gsap.quickTo("#id", "x", { duration: 0.4, ease: "power3" }),
    yTo = gsap.quickTo("#id", "y", { duration: 0.4, ease: "power3" });

document.querySelector("#container").addEventListener("mousemove", (e) => {
  xTo(e.pageX);
  yTo(e.pageY);
});
```

## ScrollTrigger 和性能

- **pin: true** 会提升固定元素；只固定需要的内容。
- **scrub** 使用较小值（例如 `scrub: 1`）可以减少滚动时的工作；在低端设备上测试。
- 仅在布局实际变化时（例如内容加载后）调用 **ScrollTrigger.refresh()**，而非每次调整大小时；尽可能防抖。

## 减少同时工作

- 暂停或杀死屏幕外或不活动的动画（例如用户导航离开时）。
- 避免一次在多个元素上动画大量属性；必要时简化或排序。

## 最佳实践

- ✅ 动画 **transform** 和 **opacity**；仅对正在动画的元素使用 CSS 中的 **will-change**。
- ✅ 当动画相同时使用 **stagger** 而非带手动延迟的多个单独补间。
- ✅ 对频繁更新的属性使用 **gsap.quickTo()**（例如鼠标追随器）。
- ✅ 清理或杀死屏幕外动画；当布局变化时调用 **ScrollTrigger.refresh()**，尽可能防抖。

## 禁止

- ❌ 当 **x**/**y**/**scale** 能实现相同效果时，动画 **width**/**height**/**top**/**left** 进行移动。
- ❌ 在每个元素上设置 **will-change** 或 **force3D**"以防万一"；仅对实际正在动画的元素使用。
- ❌ 在不经过低端设备测试的情况下创建数百个重叠的补间或 ScrollTrigger。
- ❌ 忽略清理；游离的补间和 ScrollTrigger 会持续运行，损害性能和正确性。
