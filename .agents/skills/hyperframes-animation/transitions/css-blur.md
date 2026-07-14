## 模糊

所有模糊过渡按能量缩放。参见 SKILL.md 中"按能量的模糊强度"获取完整表格。

### 模糊穿过

内容在解析前变得完全抽象。最重的模糊过渡。

**平静（此类型的默认 — 它本质上是重的）：**

```js
tl.to(old, { filter: "blur(30px)", scale: 1.08, duration: 0.5, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.3, ease: "power1.in" }, T + 0.3);
// 保持：两个场景都在抽象模糊状态
tl.fromTo(new,
  { filter: "blur(30px)", scale: 0.92, opacity: 0 },
  { filter: "blur(30px)", scale: 0.92, opacity: 1, duration: 0.2, ease: "none" }, T + 0.5);
// 慢速解析
tl.to(new, { filter: "blur(0px)", scale: 1, duration: 0.7, ease: "power1.out" }, T + 0.7);
```

**中等：**

```js
tl.to(old, { filter: "blur(15px)", scale: 1.05, opacity: 0, duration: 0.4, ease: "power2.in" }, T);
tl.fromTo(new,
  { filter: "blur(15px)", scale: 0.95, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.4, ease: "power2.out" }, T + 0.2);
```

**高能：**

```js
tl.to(old, { filter: "blur(6px)", scale: 1.03, opacity: 0, duration: 0.2, ease: "power4.in" }, T);
tl.fromTo(new,
  { filter: "blur(6px)", scale: 0.97, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.2, ease: "power4.out" }, T + 0.15);
```

### 方向模糊

在运动方向上仅模糊一个轴 — 横向或垂直。

```js
// 横向：模糊 X 轴
tl.to(old, { filter: "blur(20px) saturate(0)", scale: 0.97, x: -200, opacity: 0, duration: 0.5, ease: "power2.in" }, T);
tl.fromTo(new,
  { filter: "blur(20px) saturate(0)", scale: 1.03, x: 200, opacity: 0 },
  { filter: "blur(0px) saturate(1)", scale: 1, x: 0, opacity: 1, duration: 0.5, ease: "power2.out" }, T + 0.1);
```
