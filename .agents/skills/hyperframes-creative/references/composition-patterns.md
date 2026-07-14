# 构图模式

## 目录

- 画中画
- 主体后文字
- 淡入淡出标题卡
- 带章节标题的幻灯片
- 顶层合成示例

## 画中画（框架中的视频）

对包装 div 进行位置/大小的动画。视频填充包装器。包装器没有 data 属性。

```html
<div
  id="pip-frame"
  style="position:absolute;top:0;left:0;width:1920px;height:1080px;z-index:50;overflow:hidden;"
>
  <video
    id="el-video"
    data-start="0"
    data-duration="60"
    data-track-index="0"
    src="talking-head.mp4"
    muted
    playsinline
  ></video>
</div>
```

```js
tl.to(
  "#pip-frame",
  { top: 700, left: 1360, width: 500, height: 280, borderRadius: 16, duration: 1 },
  10,
);
tl.to("#pip-frame", { left: 40, duration: 0.6 }, 30);
```

## 主体后文字（透明 webm 叠加层）

将标题放在演讲者_后面_，使其轮廓遮挡文字。需要由 `npx hyperframes remove-background presenter.mp4 -o presenter.webm` 生成的透明抠像。

三层，加一条关键规则：

```html
<!-- z=1 基础层 — 全不透明 mp4（背景+演讲者），始终可见 -->
<video
  id="cf-base"
  data-start="0"
  data-duration="6"
  data-media-start="0"
  data-track-index="0"
  src="presenter.mp4"
  muted
  playsinline
></video>

<!-- z=2 标题 — 始终可见 -->
<h1
  id="cf-headline"
  style="position:absolute;top:50%;left:50%;
     transform:translate(-50%,-50%); z-index:2; font-size:220px; font-weight:900;
     color:#fff; text-shadow:0 6px 32px rgba(0,0,0,.55); clip-path:inset(0 0 100% 0);"
>
  MAKE IT IN HYPERFRAMES
</h1>

<!-- z=3 抠像 — 相同源，演讲者周围透明，在切换前隐藏 -->
<!-- WRAPPER 控制不透明度，而不是视频本身（见下面的规则）。 -->
<div class="cutout-wrap" style="position:absolute;inset:0;z-index:3;opacity:0">
  <video
    id="cf-cutout"
    data-start="0"
    data-duration="6"
    data-media-start="0"
    data-track-index="1"
    src="presenter.webm"
    muted
    playsinline
  ></video>
</div>
```

```js
const tl = gsap.timeline({ paused: true });
const CUT = 3.3;

// 提前显示标题
tl.to("#cf-headline", { clipPath: "inset(0 0 0% 0)", duration: 0.6, ease: "expo.out" }, 0.25);

// 在切换点，使抠像包装器可见 — 演讲者的轮廓
// 穿透标题。
tl.set(".cutout-wrap", { opacity: 1 }, CUT);

// Sentinel：将时间线扩展到合成的完整时长，这样
// 渲染器不会在最后一个有意义的补间之后退出。
tl.set({}, {}, 6);

window.__timelines["cover-flip"] = tl;
```

**为什么用包装 div，而不是对视频本身设置不透明度？**

框架会在任何带有 `data-start`/`data-duration` 的元素"活跃"时强制设置 `opacity: 1`——这就是它管理片段生命周期的方式。视频元素上的 CSS `opacity: 0` 会被静默覆盖。将视频包裹在没有 `data-*` 属性的 div 中；包装器由你的 CSS/GSAP 控制。

**为什么两个视频都在 `data-start="0"`？**

这样它们从 t=0 开始同步解码。延迟挂载抠像（`data-start=3.3`）会使 Chrome 在挂载时执行搜寻 + 解码器预热，这可能导致帧与基础 mp4 错位——表现为切换时的单帧抖动。

**颜色匹配：** `remove-background` 默认为 `--quality balanced`（crf 18），使抠像的 RGB 与源 mp4 几乎相同——叠加时边缘光晕或颜色偏移最小。对于英雄镜头使用 `--quality best`（crf 12）；仅当抠像位于_不同_背景上且文件大小重要时才降级到 `--quality fast`（crf 30）。

## 淡入淡出标题卡

```html
<div
  id="title-card"
  data-start="0"
  data-duration="5"
  data-track-index="5"
  style="display:flex;align-items:center;justify-content:center;background:#111;z-index:60;"
>
  <h1 style="font-size:64px;color:#fff;opacity:0;">My Video Title</h1>
</div>
```

```js
tl.to("#title-card h1", { opacity: 1, duration: 0.6 }, 0.3);
tl.to("#title-card", { opacity: 0, duration: 0.5 }, 4);
```

## 带章节标题的幻灯片

在同一轨道上使用独立的元素，每个都有自己的时间范围。幻灯片根据 `data-start`/`data-duration` 自动挂载/卸载。

```html
<div class="slide" data-start="0" data-duration="30" data-track-index="3">...</div>
<div class="slide" data-start="30" data-duration="25" data-track-index="3">...</div>
<div class="slide" data-start="55" data-duration="20" data-track-index="3">...</div>
```

## 顶层合成示例

```html
<div
  id="comp-1"
  data-composition-id="my-video"
  data-start="0"
  data-duration="60"
  data-width="1920"
  data-height="1080"
>
  <!-- 基本片段 -->
  <video
    id="el-1"
    data-start="0"
    data-duration="10"
    data-track-index="0"
    src="..."
    muted
    playsinline
  ></video>
  <video
    id="el-2"
    data-start="el-1"
    data-duration="8"
    data-track-index="0"
    src="..."
    muted
    playsinline
  ></video>
  <img id="el-3" data-start="5" data-duration="4" data-track-index="1" src="..." />
  <audio id="el-4" data-start="0" data-duration="30" data-track-index="2" src="..." />

  <!-- 从文件加载的子合成 -->
  <div
    id="el-5"
    data-composition-id="intro-anim"
    data-composition-src="compositions/intro-anim.html"
    data-start="0"
    data-track-index="3"
  ></div>

  <div
    id="el-6"
    data-composition-id="captions"
    data-composition-src="compositions/caption-overlay.html"
    data-start="0"
    data-track-index="4"
  ></div>

  <script>
    // 只需注册时间线 — 框架自动嵌套子合成
    const tl = gsap.timeline({ paused: true });
    window.__timelines["my-video"] = tl;
  </script>
</div>
```
