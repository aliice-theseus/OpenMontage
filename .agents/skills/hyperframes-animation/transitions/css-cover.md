## 覆盖

### 错开颜色块

全屏（1920x1080）彩色 div 错开滑过。覆盖时场景交换。

**2 块**（标准）：

```js
tl.set("#wipe-a", { x: -1920 }, T - 0.01);
tl.set("#wipe-b", { x: -1920 }, T - 0.01);
tl.to("#wipe-a", { x: 0, duration: 0.25, ease: "power3.inOut" }, T);
tl.to("#wipe-b", { x: 0, duration: 0.25, ease: "power3.inOut" }, T + 0.06);
tl.set(old, { opacity: 0 }, T + 0.2);
tl.set(new, { opacity: 1 }, T + 0.2);
tl.to("#wipe-a", { x: 1920, duration: 0.25, ease: "power3.inOut" }, T + 0.28);
tl.to("#wipe-b", { x: 1920, duration: 0.25, ease: "power3.inOut" }, T + 0.34);
```

**5 块**（密集变体）：相同模式，5 个块，0.04s 错开。使用构图调色板颜色。

### 水平百叶窗

全宽条错开滑过。每个条：`width: 1920px; height: Xpx`。

**6 条**（各 180px）：`0.03s` 错开
**12 条**（各 90px）：`0.018s` 错开

```js
for (var i = 0; i < N; i++) {
  var strip = document.createElement("div");
  strip.className = "blinds-strip";
  strip.style.top = (i * STRIP_HEIGHT) + "px";
  strip.style.height = STRIP_HEIGHT + "px";
  strip.dataset.i = i;
  container.appendChild(strip);
}
// 条使用 `transform-origin: right center` 从右→左滑入
gsap.utils.toArray(".blinds-strip").forEach(function(el, i) {
  tl.fromTo(el, { x: 0 }, { x: -1920, duration: 0.5, ease: "power3.inOut" }, T + i * STAGGER);
});
```

### 垂直百叶窗

与水平百叶窗相同但垂直。全高条。

```js
// 6 条（各 320px）或 12 条（各 160px）。条使用 `transform-origin: bottom center` 从下→上滑动。
gsap.utils.toArray(".vblinds-strip").forEach(function(el, i) {
  tl.fromTo(el, { y: 0 }, { y: -1080, duration: 0.5, ease: "power3.inOut" }, T + i * STAGGER);
});
```
