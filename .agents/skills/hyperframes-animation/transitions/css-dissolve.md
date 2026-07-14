## 溶解

### 交叉淡入淡出

简单的不透明度交换。基线。

```js
tl.to(old, { opacity: 0, duration: 0.5, ease: "power2.inOut" }, T);
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.inOut" }, T);
```

### 模糊交叉淡入淡出

带模糊 + 缩放偏移的溶解。**按能量缩放模糊量** — 参见 SKILL.md 中"按能量的模糊强度"部分。下面示例显示中等（默认）版本。对于平静组成，增加到 20-30px，在峰值模糊处保持 0.3-0.5s。对于高能，减少到 3-6px，不保持。

**中等（默认）：**

```js
tl.to(old, { filter: "blur(10px)", scale: 1.03, opacity: 0, duration: 0.5, ease: "power2.inOut" }, T);
tl.fromTo(new,
  { filter: "blur(10px)", scale: 0.97, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.5, ease: "power2.inOut" }, T + 0.1);
```

**平静（健康、奢华）— 重模糊，保持在抽象颜色：**

```js
tl.to(old, { filter: "blur(25px)", scale: 1.05, duration: 0.6, ease: "power1.in" }, T);
tl.to(old, { opacity: 0, duration: 0.4, ease: "power1.in" }, T + 0.4);
tl.fromTo(new,
  { filter: "blur(25px)", scale: 0.95, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.5, ease: "power1.out" }, T + 0.5);
```

**高能（促销、体育）— 轻模糊，快：**

```js
tl.to(old, { filter: "blur(6px)", opacity: 0, duration: 0.25, ease: "power4.in" }, T);
tl.fromTo(new,
  { filter: "blur(6px)", opacity: 0 },
  { filter: "blur(0px)", opacity: 1, duration: 0.2, ease: "power4.out" }, T + 0.15);
```

### 焦距拉动

旧场景模糊退出，新场景清晰进入。像摄像机重新对焦。所有三种能量水平如下。

**平静：**

```js
tl.to(old, { filter: "blur(20px)", duration: 0.5, ease: "sine.in" }, T);
tl.to(old, { opacity: 0, duration: 0.3 }, T + 0.4);
tl.fromTo(new, { filter: "blur(20px)", opacity: 0 }, { filter: "blur(0px)", opacity: 1, duration: 0.6, ease: "sine.out" }, T + 0.5);
```

**中等/高能 — 使用 `scale` 强化运动（默认）：**

```js
tl.to(old, { filter: "blur(10px)", scale: 1.03, opacity: 0, duration: 0.4, ease: "power2.in" }, T);
tl.fromTo(new,
  { filter: "blur(10px)", scale: 0.97, opacity: 0 },
  { filter: "blur(0px)", scale: 1, opacity: 1, duration: 0.4, ease: "power2.out" }, T + 0.2);
```

### 浸入

场景变为单色（通常为黑色），然后解析为新场景。对情绪转变有效。

```js
tl.to(old, { filter: "saturate(0)", duration: 0.2, ease: "power1.in" }, T);
tl.to(old, { filter: "saturate(0) brightness(0.3)", duration: 0.3, ease: "power2.in" }, T + 0.2);
tl.set(old, { opacity: 0 }, T + 0.5);
tl.set(new, { opacity: 1 }, T + 0.5);
tl.to(new, { filter: "saturate(1) brightness(1)", duration: 0.4, ease: "power2.out" }, T + 0.5);
```
