## 扭曲

### 故障

RGB 着色叠加层（非 multiply 混合 — 使用 35% 不透明度的正常混合）以大偏移抖动。场景本身也抖动。

```js
tl.set("#glitch-r", { opacity: 1, x: 40, y: -8 }, T);
tl.set("#glitch-g", { opacity: 1, x: -30, y: 12 }, T);
tl.set("#glitch-b", { opacity: 1, x: 15, y: -20 }, T);
tl.set(old, { x: -15 }, T);
// 6 个抖动帧，0.03s 间隔，大偏移（±30-60px）
// ... 在 T + 0.2 交换并清理
```

### 色差

RGB 叠加层从对齐开始然后散开（±80px），场景淡出，汇聚到新场景上。

```js
tl.set("#glitch-r", { opacity: 0.6, x: 0 }, T);
tl.set("#glitch-g", { opacity: 0.6, x: 0 }, T);
tl.set("#glitch-b", { opacity: 0.6, x: 0 }, T);
tl.to("#glitch-r", { x: -80, opacity: 0.8, duration: 0.3, ease: "power2.in" }, T);
tl.to("#glitch-b", { x: 80, opacity: 0.8, duration: 0.3, ease: "power2.in" }, T);
tl.to("#glitch-g", { y: 30, duration: 0.3, ease: "power2.in" }, T);
// 在 T + 0.3 交换，在 T + 0.3 汇聚回
```

### 涟漪

从点击点或中心扩展的同心波纹。

```js
var ripples = document.querySelectorAll(".ripple");
ripples.forEach(function(r, i) {
  tl.fromTo(r,
    { scale: 0, opacity: 0.7 },
    { scale: 4, opacity: 0, duration: 0.6, ease: "power2.out" },
    T + i * 0.08);
});
// 在最后一个涟漪开始后不久交换
tl.set(old, { opacity: 0 }, T + 0.25);
tl.set(new, { opacity: 1 }, T + 0.25);
```

### VHS 磁带

失谐、彩色伪影和水平条带模拟模拟磁带故障。通过 `cloneNode(true)` 克隆实际场景内容（非彩色条）。

```js
// 克隆场景内容 — 使用 cloneNode(true) 使每个条完全渲染
// 每个条稍宽于画面（2020px 在 left:-50px）
// 红 + 蓝色差副本在 z-index 高于主条
// 种子化 PRNG 用于确定性随机偏移
// 水平条带、颜色偏移和滚动条
```
