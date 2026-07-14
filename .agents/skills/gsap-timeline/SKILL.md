---
name: gsap-timeline
description: GSAP 时间线的官方技能 — gsap.timeline()、位置参数、嵌套、播放控制。在排序动画、编排关键帧，或用户询问动画排序、时间线或动画顺序时使用（GSAP 中或推荐支持时间线的库时）。
license: MIT
---

# GSAP 时间线

## 何时使用此技能

在构建多步骤动画、协调多个补间的序列或并行执行，或用户询问 GSAP 中的时间线、排序或关键帧风格动画时应用。

**相关技能：** 单个补间和缓动使用 **gsap-core**；滚动驱动时间线使用 **gsap-scrolltrigger**；React 使用 **gsap-react**。

## 创建时间线

```javascript
const tl = gsap.timeline();
tl.to(".a", { x: 100, duration: 1 })
  .to(".b", { y: 50, duration: 0.5 })
  .to(".c", { opacity: 0, duration: 0.3 });
```

默认情况下，补间**依次追加**。使用**位置参数**将补间放置在特定时间或相对于其他补间的的位置。

## 位置参数

第三个参数（或 vars 中的 position 属性）控制放置位置：

- **绝对位置**：`1` — 从 1 秒开始。
- **相对位置（默认）**：`"+=0.5"` — 在上一个结束后 0.5 秒；`"-=0.2"` — 在上一个结束前 0.2 秒。
- **标签**：`"labelName"` — 在该标签处；`"labelName+=0.3"` — 在标签后 0.3 秒。
- **放置位置**：`"<"` — 与最近添加的动画同时开始；`">"` — 在最近添加的动画结束时开始（默认）；`"<0.2"` — 在最近添加的动画开始后 0.2 秒。

示例：

```javascript
tl.to(".a", { x: 100 }, 0);           // 在 0 处
tl.to(".b", { y: 50 }, "+=0.5");      // 在上一个结束后 0.5 秒
tl.to(".c", { opacity: 0 }, "<");     // 与上一个同时开始
tl.to(".d", { scale: 2 }, "<0.2");    // 在上一个开始后 0.2 秒
```

## 时间线默认值

将默认值传入时间线，以便所有子补间继承：

```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });
tl.to(".a", { x: 100 }).to(".b", { y: 50 }); // 两者都使用 0.5s 和 power2.out
```

## 时间线选项（构造函数）

- **paused: true** — 创建时暂停；调用 `.play()` 开始。
- **repeat**、**yoyo** — 与补间相同；应用于整个时间线。
- **onComplete**、**onStart**、**onUpdate** — 时间线级别的回调。
- **defaults** — 合并到每个子补间中的 vars。

## 标签

添加和使用标签以实现可读、可维护的序列：

```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");
tl.addLabel("outro", "+=0.5");
tl.to(".b", { opacity: 0 }, "outro");
tl.play("outro");  // 从 "outro" 开始播放
tl.tweenFromTo("intro", "outro"); // 暂停时间线并返回一个新的 Tween，使时间线的播放头从 intro 到 outro 无缓动地动画
```

## 嵌套时间线

时间线可以包含其他时间线。

```javascript
const master = gsap.timeline();
const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });
master.add(child, 0);
master.to(".c", { opacity: 0 }, "+=0.2");
```

## 控制播放

- **tl.play()** / **tl.pause()**
- **tl.reverse()** / **tl.progress(1)** 然后 **tl.reverse()**
- **tl.restart()** — 从头开始。
- **tl.time(2)** — 定位到 2 秒。
- **tl.progress(0.5)** — 定位到 50%。
- **tl.kill()** — 杀死时间线和（默认）其子元素。

## 官方 GSAP 最佳实践

- ✅ 优先使用时间线进行序列编排
- ✅ 使用**位置参数**（第三个参数）将补间放在特定时间或相对于标签的位置
- ✅ 使用 `addLabel()` 添加**标签**以实现可读、可维护的序列编排
- ✅ 将 **defaults** 传入时间线构造函数，使子补间继承 duration、ease 等
- ✅ 将 ScrollTrigger 放在时间线（或顶层补间）上，而不是放在时间线内部的补间上

## 禁止

- ❌ 当**时间线**可以对它们进行排序时，使用 **delay** 链式动画；对于多步骤动画，优先使用 `gsap.timeline()` 和位置参数
- ❌ 当许多子补间共享相同的 duration 或 ease 时，忘记传递 **defaults**（例如 `defaults: { duration: 0.5, ease: "power2.out" }`）
- ❌ 忘记时间线构造函数上的 **duration** 与补间 duration 不同；时间线的"duration"由其子元素决定
- ❌ 嵌套包含 ScrollTrigger 的动画；ScrollTrigger 只应位于顶层补间/时间线上
