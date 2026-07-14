## 破坏

### 页面灼烧

退出场景字面意义上从一个角烧掉。火线以基于噪声的不规则边缘扩展，一个 canvas 在灼烧边界绘制烧焦炭线，单个文本字符/元素在火焰到达时脱落并带重力下落。进入场景在灼烧后揭示。

此过渡有三个系统协同工作：

1. **火焰几何** — 从一个角（例如右下角）扩展的径向前沿，带基于噪声的不规则性以获得有机边缘
2. **场景裁剪** — 退出场景使用 SVG clip-path（带 `fill-rule: evenodd`），裁切匹配火焰前沿的孔。随着火焰扩展，更多场景被裁剪掉。所有内容（文本、图像、线条）随页面灼烧 — 无单独的碎片。
3. **烧焦边缘** — 一个 `<canvas>` 叠加层在火焰边界绘制径向渐变边缘以模拟烧焦

**何时使用：** 戏剧性揭示、前卫/破坏性情绪、游戏、赛博朋克。这是目录中最戏剧性的过渡 — 保留给主角时刻。

**要求：**

- 用于灼烧边缘叠加的 `<canvas>` 元素
- 用于有机火焰边缘几何的噪声函数
- 带 evenodd fill-rule 的 SVG clip-path 用于反向裁剪

**火焰几何（确定性噪声）：**

```js
function noise(x) {
  var ix = Math.floor(x), fx = x - ix;
  var a = Math.sin(ix * 127.1 + 311.7) * 43758.5453;
  var b = Math.sin((ix + 1) * 127.1 + 311.7) * 43758.5453;
  var t = fx * fx * (3 - 2 * fx);
  return a - Math.floor(a) + (b - Math.floor(b) - (a - Math.floor(a))) * t;
}
```

**场景裁剪（SVG clipPath，偶数奇填充规则）：**

```html
<svg width="0" height="0"><defs>
  <clipPath id="burn-clip" clipPathUnits="objectBoundingBox">
    <path id="burn-path" fill-rule="evenodd"
      d="M1,1 L1,0 L0,0 L0,1 Z M1,1 L0.95,0.95 ..." />
  </clipPath>
</defs></svg>
```

外部路径覆盖整个画面。内部路径（燃烧孔）从火角收缩。偶数奇填充规则使画面在孔内被裁剪掉，外部保留。

**驱动脚本：**

```js
var burnState = { wp: 1 }; // 1 = 未灼烧，0 = 完全灼烧
var burnDuration = 1.2;
var burnStart = T;

tl.to(burnState, {
  wp: 0,
  duration: burnDuration,
  ease: "power1.in",
  onUpdate: function() {
    var p = 1 - burnState.wp; // 0→1 灼烧进度
    buildBurnPath(p, "#burn-path"); // 更新剪辑路径
    drawCharLayer(p); // 绘制烧焦边缘 canvas
  }
}, burnStart);
// 进入场景在灼烧接近完成时从黑色淡入
tl.fromTo(new, { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power1.out" }, burnStart + burnDuration * 0.9);
// 在灼烧完成时隐藏退出场景
tl.set(old, { opacity: 0, clipPath: "none" }, burnStart + burnDuration);
```

**注意：** `clipPath` 必须通过 `onUpdate` 中的 `setAttribute` 更新（非 GSAP 补间）。`onUpdate` 必须在 `wp <= 0` 时恢复 `clipPath: "none"` 以支持倒带 — `tl.set(old, { clipPath: "none" }, ...)` 不做这件事；它必须在 `onUpdate` 内部发生。
