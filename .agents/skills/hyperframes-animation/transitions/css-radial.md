## 径向 / 形状

### 圆形虹膜

从中心扩展的圆揭示新场景。

```js
tl.set(new, { opacity: 1 }, T);
tl.fromTo(new,
  { clipPath: "circle(0% at 50% 50%)" },
  { clipPath: "circle(75% at 50% 50%)", duration: 0.5, ease: "power2.out" }, T);
tl.set(old, { opacity: 0 }, T + 0.5);
```

### 菱形虹膜

从中心扩展的菱形。

```js
tl.set(new, { opacity: 1 }, T);
tl.fromTo(new,
  { clipPath: "polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%)" },
  { clipPath: "polygon(50% -20%, 120% 50%, 50% 120%, -20% 50%)", duration: 0.5, ease: "power2.out" }, T);
tl.set(old, { opacity: 0 }, T + 0.5);
```

### 对角分割

旧场景缩小到一个角的三角形。

```js
tl.set(new, { opacity: 1, zIndex: 1 }, T);
tl.set(old, { zIndex: 10, transformOrigin: "top right" }, T);
tl.to(old,
  { clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)", duration: 0.05, ease: "none" }, T);
tl.to(old,
  { clipPath: "polygon(100% 100%, 100% 100%, 100% 100%, 100% 100%)", duration: 0.4, ease: "power3.in" }, T + 0.05);
tl.set(old, { opacity: 0, clipPath: "none", zIndex: "auto" }, T + 0.45);
tl.set(new, { zIndex: "auto" }, T + 0.45);
```
