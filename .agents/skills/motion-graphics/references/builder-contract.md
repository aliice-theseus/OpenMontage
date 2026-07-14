# Builder 约定 — 合成规则（`agents/builder.md` 的详细说明）

## 根必须有尺寸

根 `#stage`（`data-composition-id`）需要 `position: relative; width: <W>px; height: <H>px`。没有明确的高度，flex 子元素会折叠到约0，内容堆积到左上角 — 而 `lint`/`inspect` 不会捕获到这个问题。

## 先布局后动画

1. 识别**主角帧**（大多数元素可见的时刻）→ 先用静态 CSS 构建该状态，不使用 GSAP。
2. `.scene-content` 使用 padding 而非偏移来填充场景：
   ```css
   display: flex;
   flex-direction: column;
   justify-content: center;
   width: 100%;
   height: 100%;
   padding: 120px 160px;
   gap: 24px;
   box-sizing: border-box;
   ```
   绝不在内容容器上使用 `position:absolute; top:Npx`（会溢出）。保留 absolute 给装饰元素。保持 ≥80px 内边距（标题安全边距）。
3. **入场**：`gsap.from()` 从屏幕外/不可见到 CSS 位置（在子组件中使用 `fromTo()`）。CSS 位置是基准真实值；补间动画是到达该位置的旅程。
4. **退出**：仅最终场景将元素动画退出；场景之间的过渡本身就是退出。

## 时间线/剪辑约定

- 一个 `gsap.timeline({paused:true})` 在 `window.__timelines["<id>"]` 上；`tl.seek(0)`；绝不用 `tl.play()`。
- 时间元素：`class="clip"` + `data-start`/`data-duration`/`data-track-index` + 稳定的 `id`。一个全时长剪辑内的时间线驱动组不需要每个都有定时属性。
- 仅确定性 — 无 `Date.now()`/`Math.random()`/网络。计数通过 `onUpdate` 补间代理对象（seek 安全），绝不用时钟计数器。

## 正确性

- **延迟元素的 seek 安全揭示**：`gsap.set(el, {autoAlpha:0})` 一次，然后在入场时用 `gsap.to(el, {autoAlpha:1})` 揭示（搭配仅运动的 `from()`）。**不要**用 `set(opacity:1) + from(opacity:0)` 门控 — 在暂停/seek 渲染下，元素将_永远_保持不可见（浏览器播放隐藏了此问题；seek 捕获暴露了它）。_（评估发现。）_
- **计数**通过 `onUpdate` 补间代理对象；它们仅在宿主推进时间线且**事件启用**时渲染（`tl.time()`/非抑制的 seek）。裸 `seek(t, true)` 会将其冻结在 0 — HF 渲染宿主必须启用事件来 seek。_（评估发现。）_
- 在补间边界处钳制；不要让弹簧超调超出保持值。
- 允许的缓动：`power1–4`、`back`、`bounce`、`circ`、`elastic`、`expo`、`sine`（`.in/.out/.inOut`）。
- 每场景一个主题。运行 `hyperframes inspect`；标记有意的溢出为 `data-layout-allow-overflow="true"`。
- **调色板纪律**：在一个 `palette` 对象/CSS 自定义属性中定义所有颜色 — 标记中不要散布内联十六进制值（对于 `asset-fusion`，从资产取色）。
