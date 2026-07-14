# 缓动、错开与基于函数的值

## 缓动

内置缓动：`power1`、`power2`、`power3`、`power4`、`back`、`bounce`、`circ`、`elastic`、`expo`、`sine`、`none`。

每个都有 `.in`、`.out`、`.inOut` 变体。

| 缓动                          | 用途                                    |
| ----------------------------- | --------------------------------------- |
| `power1.out`、`power2.out`    | 标准 UI 动效。大多数入场的默认选项。     |
| `power3.out`、`power4.out`    | 更有力的减速。标题卡片、主角展示。       |
| `sine.inOut`                  | 长时间、缓慢、平静的动效。交叉淡入淡出、环境漂移。 |
| `back.out(1.7)`               | 轻微过冲。俏皮的入场。参数控制过冲量。   |
| `elastic.out(1, 0.3)`         | 弹性弹跳。第一个参数 = 振幅，第二个 = 周期。 |
| `expo.inOut`                  | 轻快、戏剧性。主角场景之间的快速过渡。   |
| `none`（线性）                | 有节奏对位的摄像机运动、机械动效。       |

入场选择 `.out`，退场选择 `.in`，对称运动和连续运动选择 `.inOut`。

## 缓动词汇（特性与情绪）

缓动是表达的语气：一个只会低语的视频很无聊；一个在低语、正常和有力之间变化的视频才引人入胜。每个组合应至少使用 3 种不同的缓动——全部使用 `power2.out` 会产生平淡、单调的动效。

按特性分类的完整调色板（每个族都有 `.in`、`.out`、`.inOut` 变体）：

| 族                    | 特性                                                                    | 典型用途                                                                                       |
| --------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `power1`–`power4`     | 温和 (1) 到激进 (4) 的加速曲线                                           | 通用目的。power2 是主力，power4 用于戏剧性快照                                                 |
| `back(N)`             | 过冲后回弹。N 控制超出目标的距离（1=微妙，4=狂野）                       | Logo 展示、徽章弹出、卡片入场。`back.out(2.5)` 用于俏皮，`back.out(1.2)` 用于优雅               |
| `elastic(amp, freq)`  | 弹性弹跳。amp=幅度，freq=振荡速度                                        | 面板散开、充满活力的落下、有趣的展示                                                           |
| `bounce`              | 落地球弹跳                                                              | 物理交互、图标着陆、计分器                                                                     |
| `expo`                | 极端加速曲线（比 power4 陡峭得多）                                       | 高级/奢华展示、戏剧性入场                                                                      |
| `sine`                | 平滑、有机、无硬边                                                      | 环境浮动、呼吸、Ken Burns 效果、任何循环内容。`.inOut` 用于 yoyo 动效                          |
| `circ`                | 圆形加速（开始时非常快，结束时非常温和，反之亦然）                       | 摄像机运动、场景过渡、轨道运动                                                                 |
| `steps(N)`            | 离散的 N 步跳转，无插值                                                  | 打字效果、光标闪烁、计数器滴答、复古/数字美学                                                  |

**情绪映射：** 将缓动特性与节拍的情感内容匹配。平滑/有机的缓动（`sine`、`power1`）感觉沉思和漂移。激进的减速（`power4.out`、`expo.out`）感觉轻快和自信。弹簧过冲（`back.out`）感觉有弹性和物理感。故事板中的情绪描述应指导选择哪个特性——而非固定公式。

## 默认值

```javascript
const tl = gsap.timeline({
  paused: true,
  defaults: { duration: 0.6, ease: "power2.out" },
});
```

或全局设置：

```javascript
gsap.defaults({ duration: 0.6, ease: "power2.out" });
```

在时间线范围内设置默认值是推荐的——它在一个地方记录了该组合的运动语言。

## 错开（Stagger）

```javascript
gsap.fromTo(".item", { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, stagger: 0.08 });
```

对象形式：

```javascript
gsap.fromTo(
  ".item",
  { y: 24, opacity: 0 },
  {
    y: 0,
    opacity: 1,
    stagger: {
      each: 0.08, // 每个之间的延迟
      from: "center", // "start" | "end" | "center" | "edges" | "random" | index
      amount: 0.6, // 总错开时间（如果同时设置 both，会覆盖 each）
      grid: "auto", // 用于 2D 错开
      axis: "x" | "y",
    },
  },
);
```

优先使用 `stagger` 而非 N 个带手动延迟的独立补间——当目标数量或顺序改变时它仍能保持正确。使用 `fromTo()` 而非 `from()` 以使起始状态显式（参见 `gsap-timeline-and-labels.md` → 子组合入场）。

## 基于函数的值

任何 vars 都可以是函数 `(index, target, targets) => value`：

```javascript
gsap.to(".item", {
  x: (i, target, targets) => i * 50,
  rotation: (i) => (i % 2 === 0 ? 5 : -5),
  stagger: 0.1,
});
```

用于依赖于索引、属性或测量尺寸的每个元素的值。这比在循环中构建补间更廉价、更地道。

## gsap.matchMedia（仅预览）

`matchMedia` 仅在媒体查询匹配时运行设置，并在不再匹配时自动恢复。它在浏览器中不同视口大小的**预览**时有用，以及用于 `prefers-reduced-motion`。它**不能**替代在组合的实际 `data-width`/`data-height` 下渲染——HyperFrames 在固定视口下渲染。

```javascript
let mm = gsap.matchMedia();
mm.add(
  {
    isDesktop: "(min-width: 800px)",
    reduceMotion: "(prefers-reduced-motion: reduce)",
  },
  (context) => {
    const { isDesktop, reduceMotion } = context.conditions;
    gsap.to(".box", {
      rotation: isDesktop ? 360 : 180,
      duration: reduceMotion ? 0 : 2,
    });
  },
);
```
