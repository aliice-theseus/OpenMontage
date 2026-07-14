## 缩放

### 缩放穿过

旧场景缩放越过相机 + 模糊，新场景从后面放大进入。

```js
tl.to(old, { scale: 2.5, opacity: 0, filter: "blur(8px)", duration: 0.4, ease: "power3.in" }, T);
tl.fromTo(new,
  { scale: 0.5, opacity: 0, filter: "blur(8px)" },
  { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }, T + 0.15);
```

### 缩小

旧场景缩小消失，新场景在其后面。需要 z-index 管理。

```js
tl.set(new, { opacity: 1, zIndex: 1 }, T);
tl.set(old, { zIndex: 10, transformOrigin: "50% 50%" }, T);
tl.to(old, { scale: 0.3, opacity: 0, duration: 0.4, ease: "power3.in" }, T);
tl.set(old, { zIndex: "auto" }, T + 0.4);
tl.set(new, { zIndex: "auto" }, T + 0.4);
```
