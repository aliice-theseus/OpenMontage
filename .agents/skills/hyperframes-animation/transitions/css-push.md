## 线性 / 推动

### 推动滑动

两个场景一起移动 — 新场景将旧场景推出。

```js
tl.to(old, { x: -1920, duration: 0.5, ease: "power3.inOut" }, T);
tl.fromTo(new, { x: 1920, opacity: 1 }, { x: 0, duration: 0.5, ease: "power3.inOut" }, T);
```

### 垂直推动

与推动滑动相同但垂直方向。

```js
tl.to(old, { y: -1080, duration: 0.5, ease: "power3.inOut" }, T);
tl.fromTo(new, { y: 1080, opacity: 1 }, { y: 0, duration: 0.5, ease: "power3.inOut" }, T);
```

### 弹性推动

推动进入场景带过冲弹跳。

```js
tl.to(old, { x: -1920, duration: 0.5, ease: "power3.in" }, T);
tl.fromTo(new, { x: 1920, opacity: 1 }, { x: 30, duration: 0.4, ease: "power4.out" }, T + 0.1);
tl.to(new, { x: -15, duration: 0.15, ease: "sine.inOut" }, T + 0.5);
tl.to(new, { x: 0, duration: 0.1, ease: "sine.out" }, T + 0.65);
```

### 挤压

旧场景压缩到一条垂直线；新场景从一条垂直线展开。新旧必须使用 transformOrigin 防止意外旋转。

```js
tl.to(old, { scaleX: 0, transformOrigin: "left center", duration: 0.4, ease: "power3.inOut" }, T);
tl.fromTo(new,
  { scaleX: 0, transformOrigin: "right center", opacity: 1 },
  { scaleX: 1, transformOrigin: "right center", duration: 0.4, ease: "power3.inOut" }, T);
```

无需 z-index 管理 — 旧场景压缩到 0 宽度，因此新场景在其后自然可见。
