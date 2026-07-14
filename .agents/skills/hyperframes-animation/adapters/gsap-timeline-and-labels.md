# 时间线与标签

HyperFrames 是一个 seek 驱动的运行时。每个组合创建一个暂停的时间线，将其附加到 `window.__timelines["<composition-id>"]`，让 HyperFrames 定位它。不要为渲染关键运动调用 `.play()`。

## 创建时间线

```javascript
const tl = gsap.timeline({
  paused: true,
  defaults: { duration: 0.5, ease: "power2.out" },
});

tl.to(".a", { x: 100 }).to(".b", { y: 50 }).to(".c", { opacity: 0 });
```

时间线选项：

- **paused: true** — 在 HyperFrames 中必需。框架驱动播放头。
- **repeat**、**yoyo** — 应用于整个时间线。`repeat: -1` 被禁止；使用有限次数。
- **defaults** — 合并到每个子补间的 vars。使用此选项而非在每一行重复 `ease` 和 `duration`。

## 位置参数

`.to()`/`.from()`/`.fromTo()` 的第三个参数控制补间在时间线上的位置：

| 形式            | 含义                              |
| --------------- | --------------------------------- |
| `0`、`1.5`      | 以秒为单位的绝对时间               |
| `"+=0.5"`       | 在时间线末尾后 0.5 秒              |
| `"-=0.2"`       | 在时间线末尾前 0.2 秒              |
| `"intro"`       | 在 `intro` 标签处                 |
| `"intro+=0.3"`  | 在 `intro` 标签后 0.3 秒           |
| `"<"`           | 与前一个补同同时开始               |
| `">"`           | 在前一个补间结束后立即开始         |
| `"<0.2"`        | 在前一个补间开始后 0.2 秒          |
| `">-0.1"`       | 在前一个补间结束前 0.1 秒          |

```javascript
tl.to(".a", { x: 100 }, 0);
tl.to(".b", { y: 50 }, "<"); // 与 .a 同时开始
tl.to(".c", { opacity: 0 }, "<0.2"); // 在 .b 开始后 0.2 秒
```

优先使用位置参数而非 `delay:`——它天然地组合，并且在重新排序补间时能够保持正确。

## 标签

```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");

tl.addLabel("outro", "+=0.5");
tl.to(".a", { opacity: 0 }, "outro");
```

标签使长时间线可读，并让多个补间收敛在同一节拍上而无需重复输入绝对时间。

## 嵌套时间线

```javascript
const master = gsap.timeline({ paused: true });

const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });

master.add(child, 0);
```

在 HyperFrames 中，**不要**将子组合时间线嵌套到宿主中。通过 `data-composition-src` 加载的子组合由 HyperFrames 根据它们自己的 `data-start` 独立定位。嵌套仅用于对**同一**组合的时间线进行分组。

## 在子组合内部：优先使用 `fromTo` 而非 `from`

对于子组合内部的入场补间，优先使用 `gsap.fromTo()` 而非 `gsap.from()`：

```javascript
// 子组合入场 —— 在重新定位时保持干净
tl.fromTo(".title", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0.2);
```

原因：HyperFrames 每次宿主剪辑可见时都会重新定位子组合。`gsap.from()` 在**注册时间**（页面加载时）快照起始状态；当播放头跳回 `data-start` 之前时，该快照可能与实际的 CSS 状态不同步，导致元素渲染在错误位置。`gsap.fromTo()` 显式声明了两个端点，因此 seek 回退总是产生相同的起始状态。

在顶层（独立）组合中，两种形式都可以——因为没有重新定位-通过-挂载循环。

## 播放控制（仅调试/预览）

```javascript
tl.play();
tl.pause();
tl.reverse();
tl.restart();
tl.time(2);
tl.progress(0.5);
tl.kill();
```

这些在浏览器中预览时很有用。在渲染输出中，HyperFrames 内部调用 `seek()`——你的时间线必须在每次被定位时，对相同的时间值产生相同的状态。
