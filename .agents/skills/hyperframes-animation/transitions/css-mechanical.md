## 机械

### 快门

两个全屏半部从顶部和底部关闭，在中间汇合。关闭时交换。再次打开。

```js
tl.to("#shutter-top", { y: 0, duration: 0.25, ease: "power3.in" }, T);
tl.to("#shutter-bot", { y: 0, duration: 0.25, ease: "power3.in" }, T);
tl.set(old, { opacity: 0 }, T + 0.25);
tl.set(new, { opacity: 1 }, T + 0.25);
tl.to("#shutter-top", { y: -540, duration: 0.25, ease: "power3.out" }, T + 0.3);
tl.to("#shutter-bot", { y: 540, duration: 0.25, ease: "power3.out" }, T + 0.3);
```

### 时钟擦拭

径向多边形扫过，步进通过象限。使用 9 点多边形，带中间边缘位置以实现平滑扫过。

```js
tl.set(new, { opacity: 1, zIndex: 10 }, T);
var d = 0.1; // 每象限时长
tl.set(new, { clipPath: "polygon(50% 50%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%, 50% 0%)" }, T);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 50%, 100% 50%, 100% 50%, 100% 50%, 100% 50%)", duration: d, ease: "none" }, T);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 50% 100%, 50% 100%, 50% 100%)", duration: d, ease: "none" }, T + d);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 0% 100%, 0% 50%, 0% 50%)", duration: d, ease: "none" }, T + d*2);
tl.to(new, { clipPath: "polygon(50% 50%, 50% 0%, 100% 0%, 100% 50%, 100% 100%, 50% 100%, 0% 100%, 0% 50%, 0% 0%)", duration: d, ease: "none" }, T + d*3);
tl.set(new, { clipPath: "none", zIndex: "auto" }, T + d*4 + 0.02);
tl.set(old, { opacity: 0, zIndex: "auto" }, T + d*4 + 0.02);
```
