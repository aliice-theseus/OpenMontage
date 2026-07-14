# 变换与性能

## 变换别名

优先使用 GSAP 的变换别名而非原始 `transform` 字符串：

| GSAP 属性                    | 等价属性               |
| ---------------------------- | ---------------------- |
| `x`、`y`、`z`                | `translateX/Y/Z` (px)  |
| `xPercent`、`yPercent`       | `translateX/Y` 百分比  |
| `scale`、`scaleX`、`scaleY`  | `scale`                |
| `rotation`                   | `rotate` (度)          |
| `rotationX`、`rotationY`     | 3D 旋转                |
| `skewX`、`skewY`             | `skew`                 |
| `transformOrigin`            | `transform-origin`      |

别名让 GSAP 能够独立跟踪和插值每个轴，防止同一元素上不同补间之间的意外覆盖。

## autoAlpha

在显示/隐藏时优先使用 `autoAlpha` 而非 `opacity`：

```javascript
gsap.to(".panel", { autoAlpha: 0, duration: 0.4 });
```

`autoAlpha: 0` 同时设置 `opacity: 0` 和 `visibility: hidden`，在 alpha 为零时将元素从点击测试和可访问性树中移除——比单纯的 `opacity: 0` 更接近"消失"。

## clearProps

在补间完成时移除 GSAP 设置的内联样式：

```javascript
gsap.to(".item", { x: 100, rotation: 45, clearProps: "all" });
gsap.to(".item", { x: 100, rotation: 45, clearProps: "rotation,x" });
```

在动画片段结束时有用，将元素交还给 CSS。

## CSS 变量

```javascript
gsap.to(".chart", { "--hue": 180, duration: 1 });
```

动画化任何自定义属性。适用于颜色、长度、数字——CSS 能插值的任何类型。

## 相对值和方向值

- 相对值：`"+=20"`、`"-=10"`、`"*=2"`。
- 方向旋转：`"360_cw"`、`"-170_short"`、`"90_ccw"`——控制在两个值之间时角度选取的方向。

## SVG 细节

- `svgOrigin` 在 SVG 的全局坐标空间（而非元素的局部盒模型）中设置变换原点。**不要**在同一元素上组合使用 `svgOrigin` 和 `transformOrigin`——选择其一。
- 通过相同的别名名称（`x`、`y`、`rotation`）动画化 SVG 变换属性——GSAP 会处理 SVG 特有的细节。

## 性能规则

### 优先使用 transforms 和 opacity

动画化 `x`、`y`、`scale`、`rotation`、`opacity` 保持在 GPU 合成器上。当 transforms 能达到相同效果时，避免使用 `width`、`height`、`top`、`left`、`margin`、`padding`。

### will-change（谨慎使用）

```css
.title {
  will-change: transform;
}
```

仅在实际**进行**动画的元素上使用。到处使用会使其失效并浪费内存。

### gsap.quickTo 用于频繁更新（仅预览）

对于由**事件**驱动的高频更新——指针移动、滚动、音频拖拽——`quickTo` 复用同一个补间而非每帧创建新的：

```javascript
const xTo = gsap.quickTo("#cursor", "x", { duration: 0.4, ease: "power3" });
const yTo = gsap.quickTo("#cursor", "y", { duration: 0.4, ease: "power3" });

container.addEventListener("mousemove", (e) => {
  xTo(e.pageX);
  yTo(e.pageY);
});
```

> **渲染模式没有输入事件。** 渲染器逐帧 seek；`mousemove`、`scroll` 等永远不会触发。`quickTo` 的主要用例仅在浏览器的**实时预览**中适用。对于渲染中的音频响应动画，预先提取音频数据并声明式驱动时间线（参见 `../rules/gsap-effects.md`）。

### Stagger 胜过 N 个补间

一个带 `stagger` 的补间在可读性和运行时成本上都优于 N 个带手动延迟的补间。

### 清理

在实时预览中，暂停或 `kill()` 掉屏幕外的动画。渲染模式不受影响（渲染器直接驱动时间）。
