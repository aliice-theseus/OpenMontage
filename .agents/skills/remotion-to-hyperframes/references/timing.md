# 时间翻译：interpolate, spring, 缓动

这是最高杠杆率的参考。缓动和时间是读者最注意的；弄错它们会比任何其他翻译选择损失更多的 SSIM。已根据 T1–T3 层级进行了经验验证。

## 转换：帧 → 秒

HF 的时间线以秒为单位。Remotion 基于帧。始终：

```
time_seconds = frame / fps
```

因此在 fps=30 时：

- 第 15 帧 → 0.5 秒
- 第 30 帧 → 1.0 秒
- 第 90 帧 → 3.0 秒

在翻译时一次性完成此转换，而非在运行时。

## interpolate — 线性

```tsx
const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
```

翻译为：

```js
gsap.to(target, { opacity: 1, duration: 1.0, ease: "none" }, 0);
// 如果属性从 0 开始且 CSS 尚未设置它，则使用 fromTo
gsap.fromTo(target, { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "none" }, 0);
```

`ease: "none"` 匹配 Remotion 的默认线性插值。如果初始状态在 CSS 中，CSS 设置 `from` 值；否则使用 `fromTo`。

`extrapolateLeft`/`extrapolateRight` 在 Remotion 中默认为 `"extend"`，但代理最常看到的是 `"clamp"`。GSAP 不支持 extend — 值在补间的开始和结束处保持不变。因此对于 `clamp`，GSAP 匹配；对于 `extend`，你需要在输出前手动扩展输入范围。

## interpolate — 多段

```tsx
const opacity = interpolate(frame, [0, 15, 75, 90], [0, 1, 1, 0]);
```

在偏移 `[0]/fps`、`[1]/fps`、`[2]/fps` 处的三个关键帧补间：

```js
const tl = gsap.timeline({ paused: true });
tl.to(target, { opacity: 1, duration: 0.5, ease: "none" }, 0);
tl.to(target, { opacity: 1, duration: 2.0, ease: "none" }, 0.5);
tl.to(target, { opacity: 0, duration: 0.5, ease: "none" }, 2.5);
```

在 T1 中验证 — 与 Remotion 基线的平均 SSIM 为 0.974。

## spring → GSAP back.out

Remotion 的 `spring()` 是最有损的翻译。映射是近似的，但足够接近，真实世界的合成能保持 ≥ 0.92 SSIM（T2：0.985，T3：0.953）。

| Remotion `spring` 配置                          | GSAP 等价物                                            | 已验证于                     |
| ------------------------------------------------- | ---------------------------------------------------- | -------------------------------- |
| `{damping: 12, stiffness: 100, mass: 1}`（明快） | `back.out(1.4)` 约 ~0.7 秒                            | T2, T3 (TitleScene)              |
| `{damping: 14, stiffness: 90, mass: 1}`（平静）  | `back.out(1.2)` 约 ~0.7 秒                            | T3 (StatCard)                    |
| `{damping: 8, stiffness: 200}`（非常有弹性）      | `back.out(2.0)` 或 `elastic.out(1, 0.5)` 约 ~0.6 秒   | 未验证；预算约 0.05 SSIM         |
| `{overshootClamping: true}`                       | `power3.out` 约 ~0.6 秒（无过冲）                     | 未验证                           |

**经验法则**：`back.out(N)` 过冲比 ≈ `(stiffness / damping^2) * 1.4`。对于 `damping:12, stiffness:100`，得到 `1.4 * 100/144 = 0.97`，接近已验证的 1.4（公式是粗略的；通过视觉调整）。典型配置的默认持续时间约为 ~0.7 秒。

当 spring 的 `delay`/`from`/`to` 非默认值时，按比例缩放持续时间。

## 带自定义缓动的 interpolate

```tsx
import { Easing } from "remotion";
interpolate(frame, [0, 30], [0, 1], { easing: Easing.out(Easing.cubic) });
```

| Remotion                     | GSAP                                                                                      |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| `Easing.in(Easing.linear)`   | `ease: "none"`                                                                            |
| `Easing.out(Easing.cubic)`   | `ease: "power3.out"`                                                                      |
| `Easing.inOut(Easing.cubic)` | `ease: "power3.inOut"`                                                                    |
| `Easing.out(Easing.poly(N))` | `ease: "power<N>.out"`（N=2 二次, 3 三次, 4 四次, 5 五次）                                 |
| `Easing.bezier(a,b,c,d)`     | `CustomEase.create("c", "M0,0 C${a},${b} ${c},${d} 1,1")`（需要 CustomEase 插件）          |
| `Easing.elastic(bounciness)` | `ease: "elastic.out(${bounciness}, 0.3)"`                                                 |
| `Easing.bounce`              | `ease: "bounce.out"`                                                                      |
| `Easing.back(overshoot)`     | `ease: "back.out(${overshoot * 1.7})"`（Remotion 的过冲比例不同）                           |

## interpolate 驱动非数值属性

```tsx
const color = interpolateColors(frame, [0, 30], ["#ff0000", "#0000ff"]);
```

GSAP 原生支持颜色补间：

```js
gsap.to(target, { color: "#0000ff", duration: 1.0, ease: "none" }, 0);
```

`backgroundColor`、`borderColor` 同理。`from` 值从 CSS 或内联样式中读取。

## 自定义计数 / 数字补间

当 Remotion 使用基于帧的数字渐变时（`Math.round(value * eased)`）：

```tsx
const t = interpolate(frame, [0, 45], [0, 1]);
const eased = 1 - (1 - t) ** 3; // 三次缓出
const value = Math.round(target * eased);
return <div>{value.toLocaleString()}</div>;
```

GSAP 等价物 — 对计数器对象进行补间，在更新时写入 `textContent`：

```js
const counter = { v: 0 };
tl.to(
  counter,
  {
    v: target,
    duration: 1.5,
    ease: "power3.out",
    onUpdate: () => {
      el.textContent = Math.round(counter.v).toLocaleString();
    },
  },
  0,
);
```

`power3.out` 完全匹配 `1 - (1-t)^3`。在 T3 中验证（平均 SSIM 0.953）。逐帧数字不匹配发生在子帧时间偏移上，但最终值收敛 — 在噪声基底以上无 SSIM 影响。

## 通过实例属性交错

当自定义子组件接受 `delayInFrames` 属性时：

```tsx
<StatCard delayInFrames={i * 12} value={...} />
```

翻译为 GSAP 时间线偏移：

```js
cards.forEach((card, i) => {
  const start = base + i * (12 / fps); // fps=30 时 i * 0.4秒
  tl.to(card, { ... }, start);
});
```

在 T3 中验证 — 三个 StatCards 以 0.0/0.4/0.8 秒交错。
