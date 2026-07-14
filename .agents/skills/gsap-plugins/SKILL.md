---
name: gsap-plugins
description: GSAP 插件的官方技能 — 注册、ScrollToPlugin、ScrollSmoother、Flip、Draggable、Inertia、Observer、SplitText、ScrambleText、SVG 和物理插件、CustomEase、EasePack、CustomWiggle、CustomBounce、GSDevTools。当用户询问 GSAP 插件、滚动到指定位置、Flip 动画、拖拽、SVG 绘制或插件注册时使用。
license: MIT
---

# GSAP 插件

## 何时使用此技能

在使用或审查使用 GSAP 插件的代码时应用：注册插件、滚动到指定位置、翻转/FLIP 动画、可拖拽元素、SVG（DrawSVG、MorphSVG、MotionPath）、文本（SplitText、ScrambleText）、物理、缓动插件（CustomEase、EasePack、CustomWiggle、CustomBounce）或 GSDevTools。ScrollTrigger 有其自己的技能（gsap-scrolltrigger）。

**相关技能：** 核心补间使用 **gsap-core**；ScrollTrigger 使用 **gsap-scrolltrigger**；React 使用 **gsap-react**。

## 注册插件

每个插件注册一次，以便 GSAP（和打包工具）知道要包含它。使用 **gsap.registerPlugin()** 注册项目中使用的每个插件：

```javascript
import gsap from "gsap";
import { ScrollToPlugin } from "gsap/ScrollToPlugin";
import { Flip } from "gsap/Flip";
import { Draggable } from "gsap/Draggable";

gsap.registerPlugin(ScrollToPlugin, Flip, Draggable);
```

- ✅ 在任何补间或 API 调用中使用插件之前注册。
- ✅ 在 React 中，在顶层或一次在应用中注册（例如在使用 useGSAP 之前）；不要在重新渲染的组件内部注册。useGSAP 本身是一个插件，需要在使用前注册。

## 滚动

### ScrollToPlugin

动画滚动位置（窗口或可滚动元素）。用于"滚动到元素"或"滚动到位置"而不使用 ScrollTrigger。

```javascript
gsap.registerPlugin(ScrollToPlugin);

gsap.to(window, { duration: 1, scrollTo: { y: 500 } });
gsap.to(window, { duration: 1, scrollTo: { y: "#section", offsetY: 50 } });
gsap.to(scrollContainer, { duration: 1, scrollTo: { x: "max" } });
```

**ScrollToPlugin — 关键配置（scrollTo 对象）：**

| 选项 | 描述 |
|--------|-------------|
| `x`、`y` | 目标滚动位置（数字），或 `"max"` 表示最大值 |
| `element` | 要滚动到的选择器或元素（用于滚动到视图中） |
| `offsetX`、`offsetY` | 与目标位置的像素偏移 |

### ScrollSmoother

平滑滚动包装器（平滑化原生滚动）。需要 ScrollTrigger 和特定的 DOM 结构（内容包装器 + 平滑包装器）。在需要平滑、惯性风格滚动时使用。参见 GSAP 文档进行设置；在 ScrollTrigger 之后注册。DOM 结构如下：

```html
<body>
	<div id="smooth-wrapper">
		<div id="smooth-content">
			<!--- 你所有的内容放在这里 --->
		</div>
	</div>
	<!-- position: fixed 元素可以放在外面 --->
</body>
```

## DOM / UI

### Flip

用 `Flip.getState()` 捕获状态，然后应用更改（例如布局或类更改），然后使用 `Flip.from()` 从先前状态动画到新状态（FLIP：First、Last、Invert、Play）。在两种布局状态之间动画时使用（列表、网格、展开/折叠）。

```javascript
gsap.registerPlugin(Flip);

const state = Flip.getState(".item");
// 更改 DOM（重新排序、添加/删除、更改类）
Flip.from(state, { duration: 0.5, ease: "power2.inOut" });
```

**Flip — 关键配置（Flip.from vars）：**

| 选项 | 描述 |
|--------|-------------|
| `absolute` | 在 flip 过程中使用 `position: absolute`（默认：`false`） |
| `nested` | 为 true 时，仅测量第一级子元素（更适合嵌套变换） |
| `scale` | 为 true 时，缩放元素以适配（避免拉伸）；默认 `true` |
| `simple` | 为 true 时，仅动画位置/缩放（更快，精度较低） |
| `duration`、`ease` | 标准补间选项 |

#### 更多信息

https://gsap.com/docs/v3/Plugins/Flip

### Draggable

使元素可通过鼠标/触摸拖拽、旋转或投掷。用于滑块、卡片、可重新排序列表或任何拖拽交互。

```javascript
gsap.registerPlugin(Draggable, InertiaPlugin);

Draggable.create(".box", { type: "x,y", bounds: "#container", inertia: true });
Draggable.create(".knob", { type: "rotation" });
```

**Draggable — 关键配置选项：**

| 选项 | 描述 |
|--------|-------------|
| `type` | `"x"`、`"y"`、`"x,y"`、`"rotation"`、`"scroll"` |
| `bounds` | 元素、选择器或 `{ minX, maxX, minY, maxY }` 以约束拖拽 |
| `inertia` | `true` 启用投掷/动量（需要 InertiaPlugin） |
| `edgeResistance` | 0–1；拖拽超过边界时的阻力 |
| `cursor` | 拖拽期间的 CSS 光标 |
| `onDragStart`、`onDrag`、`onDragEnd` | 回调；接收事件和目标 |
| `onThrowUpdate`、`onThrowComplete` | 惯性活动时的回调 |

### Inertia（InertiaPlugin）

与 Draggable 配合用于释放后的动量，或跟踪任何对象的任何属性的惯性/速度，使其能够通过简单的补间平滑滑行停止。在使用 `inertia: true` 时与 Draggable 一起注册：

```javascript
gsap.registerPlugin(Draggable, InertiaPlugin);
Draggable.create(".box", { type: "x,y", inertia: true });
```

或跟踪某个属性的速度：
```javascript
InertiaPlugin.track(".box", "x");
```

然后使用 `"auto"` 继续当前速度并滑行停止：

```javascript
gsap.to(obj, { inertia: { x: "auto" } });
```

### Observer

跨设备标准化指针和滚动输入。用于滑动手势、滚动方向或自定义手势逻辑，而不像 ScrollTrigger 那样直接绑定到滚动位置。

```javascript
gsap.registerPlugin(Observer);

Observer.create({
  target: "#area",
  onUp: () => {},
  onDown: () => {},
  onLeft: () => {},
  onRight: () => {},
  tolerance: 10
});
```

**Observer — 关键配置选项：**

| 选项 | 描述 |
|--------|-------------|
| `target` | 要观察的元素或选择器 |
| `onUp`、`onDown`、`onLeft`、`onRight` | 当滑动手势/滚动在该方向超过容差时的回调 |
| `tolerance` | 检测方向前的像素数；默认 10 |
| `type` | `"touch"`、`"pointer"` 或 `"wheel"`（默认：`"touch,pointer"`） |

## 文本

### SplitText

将元素的文本拆分为字符、单词和/或行（每个在其自己的元素中），用于交错或按单位动画。在逐字符、逐词或逐行动画文本时使用。返回一个包含 **chars**、**words**、**lines**（以及当设置 `mask` 时的 **masks**）的实例。使用 **revert()** 恢复原始标记，或让 **gsap.context()** 还原。与 **gsap.context()**、**matchMedia()** 和 **useGSAP()** 集成。API：**SplitText.create(target, vars)**（目标 = 选择器、元素或数组）。

```javascript
gsap.registerPlugin(SplitText);

const split = SplitText.create(".heading", { type: "words, chars" });
gsap.from(split.chars, { opacity: 0, y: 20, stagger: 0.03, duration: 0.4 });
// 稍后：split.revert() 或让 gsap.context() 清理还原
```

使用 **onSplit()**（v3.13.0+），每次拆分和重新拆分时运行动画；从 **onSplit()** 返回补间/时间线让 SplitText 在重新拆分时清理和同步进度：

```javascript
SplitText.create(".split", {
  type: "lines",
  autoSplit: true,
  onSplit(self) {
    return gsap.from(self.lines, { y: 100, opacity: 0, stagger: 0.05, duration: 0.5 });
  }
});
```

**SplitText — 关键配置（SplitText.create vars）：**

| 选项 | 描述 |
|--------|-------------|
| **type** | 逗号分隔：`"chars"`、`"words"`、`"lines"`。默认 `"chars,words,lines"`。仅拆分需要的内容（例如如果不用 lines，则 `"words, chars"`）以获得性能。避免仅 chars 而不加 words/lines，或使用 **smartWrap: true** 防止异常换行。 |
| **charsClass**、**wordsClass**、**linesClass** | 每个拆分元素上的 CSS 类。追加 `"++"` 以添加递增类（例如 `linesClass: "line++"` → `line1`、`line2` 等）。 |
| **aria** | `"auto"`（默认）、`"hidden"` 或 `"none"`。可访问性：`"auto"` 在拆分元素上添加 `aria-label`，并在行/词/字符元素上添加 `aria-hidden`，使屏幕阅读器读取标签；`"hidden"` 将所有内容对阅读器隐藏；`"none"` 不改变 aria。如果必须暴露嵌套链接/语义，使用 `"none"` 加上仅屏幕阅读器的副本。 |
| **autoSplit** | 当为 `true` 时，在字体加载完成或元素宽度变化（且行被拆分）时还原并重新拆分，避免错误的换行。**动画必须在 onSplit() 内部创建**，以便它们针对新拆分的元素；从 **onSplit()** **返回**动画以实现自动清理和重新拆分时的时间同步。 |
| **onSplit(self)** | 拆分完成时（以及如果 **autoSplit** 为 `true` 时的每次重新拆分时）的回调。接收 SplitText 实例。返回 GSAP 补间或时间线可在重新拆分时自动还原/同步该动画。 |
| **mask** | `"lines"`、`"words"` 或 `"chars"`。在每个单位外包裹一个带有 `overflow: clip` 的额外元素，用于遮罩/揭示效果。仅一种类型；在实例的 **masks** 数组上访问包装器（如果设置了类，则使用类名 `-mask`）。 |
| **tag** | 包装器元素标签；默认 `"div"`。使用 `"span"` 表示内联（注意：某些浏览器中变换如旋转/缩放在内联元素上可能不渲染）。 |
| **deepSlice** | 当为 `true`（默认）时，跨多行的嵌套元素（例如 `<strong>`）会被细分，使行不会垂直拉伸。仅在拆分行时适用。 |
| **ignore** | 保持不拆分的选择器或元素（例如 `ignore: "sup"`）。 |
| **smartWrap** | 当仅拆分 **chars** 时，将单词包装在 `white-space: nowrap` 的 span 中，以避免词中途换行。如果拆分 words 或 lines 则忽略。默认 `false`。 |
| **wordDelimiter** | 单词边界：字符串（默认 `" "`）、RegExp 或 `{ delimiter: RegExp, replaceWith: string }` 用于自定义拆分（例如标签的零宽度连接符或非拉丁语）。 |
| **prepareText(text, parent)** | 接收原始文本和父元素的函数；在拆分前返回修改后的文本（例如为无空格语言插入断点标记）。 |
| **propIndex** | 当为 `true` 时，在每个拆分元素上添加带索引的 CSS 变量（例如 `--word: 1`、`--char: 2`）。 |
| **reduceWhiteSpace** | 折叠连续空格；默认 `true`。从 v3.13.0 起也支持换行，并可为 `<pre>` 插入 `<br>`。 |
| **onRevert** | 实例还原时的回调。 |

**提示：** 仅拆分要动画的部分（例如如果只动画单词则跳过 chars）。对于自定义字体，在其加载后拆分（例如 `document.fonts.ready.then(...)`）或使用 **autoSplit: true** 配合 **onSplit()**。为避免拆分 chars 时的字距偏移，使用 CSS `font-kerning: none; text-rendering: optimizeSpeed;`。避免使用 `text-wrap: balance`；它可能干扰拆分。SplitText 不支持 SVG `<text>`。

**了解更多：** [SplitText](https://gsap.com/docs/v3/Plugins/SplitText/)

### ScrambleText

用混乱/故障效果动画文本。在需要以乱码方式揭示或过渡文本时使用。

```javascript
gsap.registerPlugin(ScrambleTextPlugin);

gsap.to(".text", {
  duration: 1,
  scrambleText: { text: "New message", chars: "01", revealDelay: 0.5 }
});
```

## SVG

### DrawSVG（DrawSVGPlugin）

通过动画 `stroke-dashoffset` / `stroke-dasharray` 来揭示或隐藏 SVG 元素的描边。适用于 `<path>`、`<line>`、`<polyline>`、`<polygon>`、`<rect>`、`<ellipse>`。在需要"绘制"或"擦除"描边时使用。

**drawSVG 值：** 描述沿路径的描边**可见段**（开始和结束位置），不是"随时间从 A 动画到 B"。格式：百分比或长度值的 `"start end"`。示例：`"0% 100%"` = 完整描边；`"20% 80%"` = 仅在 20% 和 80% 之间的描边（两端有间隙）。补间从元素的**当前**段动画到**目标**段 — 例如 `gsap.to("#path", { drawSVG: "0% 100%" })` 从当前状态到完整描边。单一值（如 `0`、`"100%"`）表示起点为 0：`"100%"` 等同于 `"0% 100%"`。

**必要条件：** 元素必须有可见的描边 — 在 CSS 或 SVG 属性中设置 `stroke` 和 `stroke-width`；否则不会绘制任何内容。

```javascript
gsap.registerPlugin(DrawSVGPlugin);

// 从无到完整描边绘制
gsap.from("#path", { duration: 1, drawSVG: 0 });
// 或显式段：从 0–0 到 0–100%
gsap.fromTo("#path", { drawSVG: "0% 0%" }, { drawSVG: "0% 100%", duration: 1 });
// 仅中间描边（两端有间隙）
gsap.to("#path", { duration: 1, drawSVG: "20% 80%" });
```

**注意事项：** 仅影响描边（不影响填充）。优先使用单段 `<path>` 元素；多段路径在某些浏览器中可能渲染异常。`<use>` 的内容不能视觉上更改。**DrawSVGPlugin.getLength(element)** 和 **DrawSVGPlugin.getPosition(element)** 返回描边长度和当前位置。

**了解更多：** [DrawSVG](https://gsap.com/docs/v3/Plugins/DrawSVGPlugin)

### MorphSVG（MorphSVGPlugin）

通过动画 `d` 属性（路径数据）将一个 SVG 形状变形为另一个。开始和结束形状不需要具有相同数量的点 — MorphSVG 会转换为三次贝塞尔曲线并根据需要添加点。用于图标到图标的变形、形状过渡或基于路径的动画。适用于 `<path>`、`<polyline>` 和 `<polygon>`；`<circle>`、`<rect>`、`<ellipse>` 和 `<line>` 在内部转换或通过 **MorphSVGPlugin.convertToPath(selector | element)**（在 DOM 中用 `<path>` 替换元素）。

**morphSVG 值：** 可以是**选择器**（例如 `"#lightning"`）、**元素**、**原始路径数据**（例如 `"M47.1,0.8 73.3,0.8..."`），或对于 polygon/polyline 的**点字符串**（例如 `"240,220 240,70 70,70 70,220"`）。对于完整配置使用**对象形式**，其中 **shape** 是唯一必需属性。

```javascript
gsap.registerPlugin(MorphSVGPlugin);

// 如果需要，先将原始形状转换为路径：
MorphSVGPlugin.convertToPath("circle, rect, ellipse, line");

gsap.to("#diamond", { duration: 1, morphSVG: "#lightning", ease: "power2.inOut" });
// 对象形式：
gsap.to("#diamond", {
  duration: 1,
  morphSVG: { shape: "#lightning", type: "rotational", shapeIndex: 2 }
});

```

**MorphSVG — 关键配置（morphSVG 对象）：**

| 选项 | 描述 |
|--------|-------------|
| **shape** | _(必需)_ 目标形状：选择器、元素或原始路径字符串。 |
| **type** | `"linear"`（默认）或 `"rotational"`。Rotational 使用角度/长度插值，可避免变形中途的扭结；在线性看起来不对时尝试此选项。 |
| **map** | 段如何匹配：`"size"`（默认）、`"position"` 或 `"complexity"`。在开始/结束段不对齐时使用；如果都不行，拆分为多个路径并分别变形。 |
| **shapeIndex** | 偏移起始路径中的哪个点映射到结束路径中的第一个点（避免形状"交叉"或反转）。单段路径为数字；多段路径为**数组**（例如 `[5, 1, -8]`）。负值反转该段。使用 **shapeIndex: "log"** 一次来记录自动计算的值，然后将数字/数组粘贴到补间中。**findShapeIndex(start, end)**（单独工具）提供交互式 UI 来查找良好值。仅适用于闭合路径。 |
| **smooth** | (v3.14+) 添加平滑点。数字（例如 `80`）、`"auto"` 或对象：`{ points: 40 \| "auto", redraw: true \| false, persist: true \| false }`。`redraw: false` 保持原始锚点（完美保真，间距不太均匀）。`persist: false` 在补间结束时移除添加的点。在默认变形看起来锯齿状或不自然时使用。 |
| **curveMode** | 布尔值 (v3.14+)。插值控制柄角度/长度而非原始 x/y，以避免曲线上的扭结。如果变形中途出现扭结，可尝试此选项。 |
| **origin** | **type: "rotational"** 的旋转原点。字符串：`"50% 50%"`（默认）或 `"20% 60%, 35% 90%"` 用于不同的开始/结束原点。 |
| **precision** | 输出路径数据的小数位数；默认 `2`。 |
| **precompile** | 预计算的路径字符串数组（或使用 **precompile: "log"** 一次，从控制台复制）。跳过昂贵的启动计算；用于非常复杂的变形。仅适用于 `<path>`（先将 polygon/polyline 转换）。 |
| **render** | 每次更新时调用的函数(rawPath, target) — 例如绘制到 canvas。RawPath 是一个段数组（每个段 = 交替 x、y 三次贝塞尔坐标的数组）。 |
| **updateTarget** | 当使用 **render**（例如仅 canvas）时，设置 **updateTarget: false**，以便原始 `<path>` 不被更新。**MorphSVGPlugin.defaultUpdateTarget** 设置默认值。 |

**实用工具：** **MorphSVGPlugin.convertToPath(selector | element)** 将 circle/rect/ellipse/line/polygon/polyline 转换为 DOM 中的 `<path>`。**MorphSVGPlugin.rawPathToString(rawPath)** 和 **stringToRawPath(d)** 在路径字符串和原始数组之间转换。插件在目标上存储原始 `d`（例如用于补间返回：`morphSVG: "#originalId"` 或同一元素）。

**提示：** 对于扭曲或反转的变形，设置 **shapeIndex**（使用 `"log"` 或 findShapeIndex()）。对于多段路径，**shapeIndex** 是一个数组（每段一个值）。仅在第一帧慢时预编译；它不能修复补间期间的卡顿（如果需要，简化 SVG 或减小大小）。

**了解更多：** [MorphSVG](https://gsap.com/docs/v3/Plugins/MorphSVGPlugin)

### MotionPath（MotionPathPlugin）

沿 SVG 路径动画元素。在需要沿路径（例如曲线或自定义路线）移动对象时使用。

```javascript
gsap.registerPlugin(MotionPathPlugin);

gsap.to(".dot", {
  duration: 2,
  motionPath: { path: "#path", align: "#path", alignOrigin: [0.5, 0.5] }
});
```

**MotionPath — 关键配置（motionPath 对象）：**

| 选项 | 描述 |
|--------|-------------|
| `path` | SVG 路径元素、选择器或路径数据字符串 |
| `align` | 用于对齐目标的路径元素或选择器 |
| `alignOrigin` | `[x, y]` 原点 (0–1)；默认 `[0.5, 0.5]` |
| `autoRotate` | 旋转元素以跟随路径切线 |
| `curviness` | 0–2；路径平滑度 |

### MotionPathHelper

MotionPath 的视觉编辑器（对齐、偏移）。在开发期间用于调整路径对齐。

```javascript
gsap.registerPlugin(MotionPathPlugin, MotionPathHelperPlugin);

const helper = MotionPathHelper.create(".dot", "#path", { end: 0.5 });
// 在 UI 中调整，然后在动画中使用 helper.path 或 helper.getProgress()
```

## 缓动

### CustomEase

自定义缓动曲线（三次贝塞尔或 SVG 路径）。在内置缓动不足时使用。基本用法在 gsap-core 中涵盖；使用时注册：

```javascript
gsap.registerPlugin(CustomEase);
const ease = CustomEase.create("name", ".17,.67,.83,.67");
gsap.to(".el", { x: 100, ease: ease, duration: 1 });
```

### EasePack

添加更多命名缓动（例如 SlowMo、RoughEase、ExpoScaleEase）。注册并在补间中使用缓动名。

### CustomWiggle

抖动/摇晃缓动。在值需要"抖动"（多次振荡）时使用。

### CustomBounce

弹跳风格缓动，可配置强度。

## 物理

### Physics2D（Physics2DPlugin）

2D 物理（速度、角度、重力）。在使用简单物理（例如抛射物、弹跳）做动画时使用。

```javascript
gsap.registerPlugin(Physics2DPlugin);

gsap.to(".ball", {
  duration: 2,
  physics2D: {
    velocity: 250,
    angle: 80,
    gravity: 500
  }
});
```

### PhysicsProps（PhysicsPropsPlugin）

将物理应用于属性值。用于物理驱动的属性动画。

```javascript
gsap.registerPlugin(PhysicsPropsPlugin);

gsap.to(".obj", {
  duration: 2,
  physicsProps: {
    x: { velocity: 100, end: 300 },
    y: { velocity: -50, acceleration: 200 }
  }
});
```

## 开发

### GSDevTools

用于刮擦时间线、切换动画和调试的 UI。仅在开发期间使用；不要发布。注册并创建带有时间线引用的实例。

```javascript
gsap.registerPlugin(GSDevTools);
GSDevTools.create({ animation: tl });
```

## 其他

### Pixi（PixiPlugin）

将 GSAP 与 PixiJS 集成，用于动画 Pixi 显示对象。在使用 GSAP 动画 Pixi 对象时注册。

```javascript
gsap.registerPlugin(PixiPlugin);

const sprite = new PIXI.Sprite(texture);
gsap.to(sprite, { pixi: { x: 200, y: 100, scale: 1.5 }, duration: 1 });
```

## 最佳实践

- ✅ 首次使用前用 **gsap.registerPlugin()** 注册每个使用的插件。
- ✅ 对布局过渡使用 **Flip.getState()** → DOM 更改 → **Flip.from()**；对带动量的拖拽使用 **Draggable** + **InertiaPlugin**。
- ✅ 在组件卸载或元素被移除时还原插件实例（例如 `SplitTextInstance.revert()`）。

## 禁止

- ❌ 在未先注册插件（**gsap.registerPlugin()**）的情况下在补间或 API 中使用插件。
- ❌ 将 GSDevTools 或仅开发插件发布到生产环境。

### 了解更多

https://gsap.com/docs/v3/Plugins/
