## 3D

### 3D 卡片翻转

180° Y 轴旋转。在两个场景内部元素上需要 CSS：`backface-visibility: hidden; transform-style: preserve-3d;`。父级需要 `perspective: 1200px`。

```js
tl.set(new, { rotationY: -180, opacity: 1 }, T);
tl.to(old, { rotationY: 180, duration: 0.6, ease: "power2.inOut" }, T);
tl.to(new, { rotationY: 0, duration: 0.6, ease: "power2.inOut" }, T);
tl.set(old, { opacity: 0 }, T + 0.6);
```
