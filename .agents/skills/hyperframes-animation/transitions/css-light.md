## 光

### 漏光

多个暖色叠加层冲刷画面。需要：一个平坦暖色调层 + 2-3 个亮径向渐变 div，全部大于画面使边缘从不可见。

```js
// 暖色调冲洗整个画面
tl.to("#leak-warm", { opacity: 0.4, duration: 0.3, ease: "power1.in" }, T);
// 亮漏光元素漂入
tl.to("#leak-1", { opacity: 0.9, x: 300, duration: 0.5, ease: "sine.inOut" }, T + 0.05);
tl.to("#leak-2", { opacity: 0.8, x: 200, duration: 0.6, ease: "sine.inOut" }, T + 0.1);
// 峰值温暖然后交换
tl.to("#leak-warm", { opacity: 0.6, duration: 0.15, ease: "power2.in" }, T + 0.35);
tl.set(old, { opacity: 0 }, T + 0.45);
tl.set(new, { opacity: 1 }, T + 0.45);
// 漏光淡出
tl.to("#leak-warm", { opacity: 0, duration: 0.4, ease: "power2.out" }, T + 0.5);
tl.to("#leak-1", { opacity: 0, x: 600, duration: 0.35, ease: "power1.out" }, T + 0.5);
```

### 过曝光灼烧

场景通过 CSS `filter: brightness()` 逐渐爆发为白色，然后白色叠加淡入。在峰值白色交换。白色退去揭示新场景。

```js
tl.to(old, { filter: "brightness(1.5)", scale: 1.03, duration: 0.2, ease: "power1.in" }, T);
tl.to(old, { filter: "brightness(3)", scale: 1.06, duration: 0.2, ease: "power2.in" }, T + 0.2);
tl.to("#flash-overlay", { opacity: 0.5, duration: 0.25, ease: "power1.in" }, T + 0.15);
tl.to("#flash-overlay", { opacity: 1, duration: 0.15, ease: "power2.in" }, T + 0.4);
tl.set(old, { opacity: 0 }, T + 0.5);
tl.set(new, { opacity: 1 }, T + 0.5);
tl.to(old, { filter: "brightness(1)", scale: 1 }, T + 0.5);
tl.to(new, { filter: "brightness(1.08)", scale: 1.02, duration: 0.2, ease: "power2.in" }, T + 0.5);
tl.to("#flash-overlay", { opacity: 0, duration: 0.3, ease: "power1.out" }, T + 0.5);
tl.to(new, { filter: "brightness(1)", scale: 1, duration: 0.3, ease: "power1.out" }, T + 0.7);
```

**过曝光灼烧 — 极简变体**（无叠加层，仅滤镜）：

```js
tl.to(old, { filter: "brightness(2.5)", opacity: 0, duration: 0.4, ease: "power2.in" }, T);
tl.fromTo(new,
  { filter: "brightness(0.6)", opacity: 0 },
  { filter: "brightness(1)", opacity: 1, duration: 0.3, ease: "power2.out" }, T + 0.25);
```

### 胶片灼烧

场景在灼烧边缘效果下淡出，然后新场景从黑色淡入。比过曝光更有机。

```js
tl.to(old, { filter: "brightness(1.3) saturate(1.3)", duration: 0.15, ease: "power1.in" }, T);
tl.to(old, { filter: "brightness(2) saturate(0)", duration: 0.3, ease: "power2.in" }, T + 0.15);
tl.to(old, { opacity: 0, duration: 0.1, ease: "power1.in" }, T + 0.45);
tl.set(new, { opacity: 1, filter: "brightness(0.8) saturate(0.8)" }, T + 0.55);
tl.to(new, { filter: "brightness(1) saturate(1)", duration: 0.3, ease: "power2.out" }, T + 0.55);
```
