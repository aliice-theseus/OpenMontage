---
name: gsap-utils
description: GSAP gsap.utils 的官方技能 — clamp、mapRange、normalize、interpolate、random、snap、toArray、wrap、pipe。当用户询问 gsap.utils、clamp、mapRange、random、snap、toArray、wrap 或 GSAP 中的工具函数时使用。
license: MIT
---

# gsap.utils

## 何时使用此技能

在编写或审查使用 **gsap.utils** 进行数学、数组/集合处理、单位解析或动画中的值映射（例如将滚动映射到值、随机化、吸附到网格或归一化输入）的代码时应用。

**相关技能：** 与 **gsap-core**、**gsap-timeline** 和 **gsap-scrolltrigger** 一起构建动画时使用；CustomEase 和其他缓动工具在 **gsap-plugins** 中。

## 概述

**gsap.utils** 提供纯工具函数；无需注册。在补间 vars（例如基于函数的值）、ScrollTrigger 或 Observer 回调中，或任何驱动 GSAP 的 JS 中使用。所有函数都在 **gsap.utils** 上（例如 `gsap.utils.clamp()`）。

**省略值：函数形式。** 许多工具接受要转换的值作为**最后一个**参数。如果省略该参数，工具返回一个**函数**，稍后接受该值。当需要使用相同配置多次 clamp、map、normalize 或 snap 值时（例如在 mousemove 处理程序或补间回调中），使用函数形式。**例外：random()** — 传递 **true** 作为最后一个参数以获得可复用函数（不要省略值）；参见 [random()](https://gsap.com/docs/v3/GSAP/UtilityMethods/random())。

```javascript
// 带值：返回结果
gsap.utils.clamp(0, 100, 150); // 100

// 无值：返回一个稍后调用的函数
let c = gsap.utils.clamp(0, 100);
c(150);  // 100
c(-10);  // 0
```

## 钳制和范围

### clamp(min, max, value?)

将值约束在最小值和最大值之间。省略 **value** 获取函数：`clamp(min, max)(value)`。

```javascript
gsap.utils.clamp(0, 100, 150); // 100
gsap.utils.clamp(0, 100, -10); // 0

let clampFn = gsap.utils.clamp(0, 100);
clampFn(150); // 100
```

### mapRange(inMin, inMax, outMin, outMax, value?)

将值从一个范围映射到另一个范围。在将滚动位置、进度（0-1）或输入范围转换为动画范围时使用。省略 **value** 获取函数：`mapRange(inMin, inMax, outMin, outMax)(value)`。

```javascript
gsap.utils.mapRange(0, 100, 0, 500, 50);  // 250
gsap.utils.mapRange(0, 1, 0, 360, 0.5);   // 180（进度转为角度）

let mapFn = gsap.utils.mapRange(0, 100, 0, 500);
mapFn(50);  // 250
```

### normalize(min, max, value?)

返回给定范围下归一化到 0-1 的值。当目标范围为 0-1 时是映射的逆操作。省略 **value** 获取函数：`normalize(min, max)(value)`。

```javascript
gsap.utils.normalize(0, 100, 50);   // 0.5
gsap.utils.normalize(100, 300, 200); // 0.5

let normFn = gsap.utils.normalize(0, 100);
normFn(50); // 0.5
```

### interpolate(start, end, progress?)

在给定进度（0-1）下在两个值之间插值。处理数字、颜色和具有匹配键的对象。省略 **progress** 获取函数：`interpolate(start, end)(progress)`。

```javascript
gsap.utils.interpolate(0, 100, 0.5);       // 50
gsap.utils.interpolate("#ff0000", "#0000ff", 0.5); // 中间颜色
gsap.utils.interpolate({ x: 0, y: 0 }, { x: 100, y: 50 }, 0.5); // { x: 50, y: 25 }

let lerp = gsap.utils.interpolate(0, 100);
lerp(0.5); // 50
```

## 随机和吸附

### random(minimum, maximum[, snapIncrement, returnFunction]) / random(array[, returnFunction])

返回范围 **minimum**–**maximum** 内的随机数，或来自**数组**的随机元素。可选的 **snapIncrement** 将结果吸附到最近的倍数（例如 `5` → 5 的倍数）。**要获取可复用函数**，传递 **true** 作为最后一个参数（**returnFunction**）；返回的函数不接受参数，每次返回一个新的随机值。这是唯一使用 `true` 表示函数形式（而非省略值）的工具。

```javascript
// 立即值：范围内的数字
gsap.utils.random(-100, 100);        // 例如 42.7
gsap.utils.random(0, 500, 5);        // 0–500，吸附到最近的 5

// 可复用函数：传递 true 作为最后一个参数
let randomFn = gsap.utils.random(-200, 500, 10, true);
randomFn();  // 范围内随机值，吸附到 10
randomFn();  // 另一个随机值

// 数组：随机选取一个值
gsap.utils.random(["red", "blue", "green"]);  // "red"、"blue" 或 "green"
let randomFromArray = gsap.utils.random([0, 100, 200], true);
randomFromArray();  // 0、100 或 200
```

**补间 vars 中的字符串形式：** 使用 `"random(-100, 100)"`、`"random(-100, 100, 5)"` 或 `"random([0, 100, 200])"`；GSAP 按目标进行求值。

```javascript
gsap.to(".box", { x: "random(-100, 100, 5)", duration: 1 });
gsap.to(".item", { backgroundColor: "random([red, blue, green])" });
```

### snap(snapTo, value?)

将值吸附到 **snapTo** 的最近倍数，或允许值数组中的最近值。省略 **value** 获取函数：`snap(snapTo)(value)`（或 `snap(snapArray)(value)`）。

```javascript
gsap.utils.snap(10, 23);     // 20
gsap.utils.snap(0.25, 0.7);  // 0.75
gsap.utils.snap([0, 100, 200], 150); // 100 或 200（数组中最接近的）

let snapFn = gsap.utils.snap(10);
snapFn(23); // 20
```

在补间中用于网格或基于步长的动画：

```javascript
gsap.to(".x", { x: 200, snap: { x: 20 } });
```

### shuffle(array)

返回一个元素相同但顺序随机的新数组。用于随机化顺序（例如从 "random" 开始交错并制作副本）。

```javascript
gsap.utils.shuffle([1, 2, 3, 4]); // 例如 [3, 1, 4, 2]
```

### distribute(config)

**返回一个函数**，根据每个目标在数组（或网格）中的位置为其分配一个值。内部用于高级交错；每当需要将值分布到多个元素（例如 scale、opacity、x、delay）时使用。返回的函数接收 `(index, target, targets)` — 可以手动调用，或将结果直接传入补间；GSAP 会按目标使用 index、element 和 array 调用它。

**配置（全部可选）：**

| 属性 | 类型 | 描述 |
|----------|------|-------------|
| `base` | Number | 起始值。默认 `0`。 |
| `amount` | Number | 分布到所有目标的总量（加到 base 上）。例如 `amount: 1` 加上 100 个目标 → 每个之间 0.01。使用 **each** 替代可为每个目标设置固定步长。 |
| `each` | Number | 每个目标之间增加的量（加到 base 上）。例如 `each: 1` 加上 4 个目标 → 0、1、2、3。使用 **amount** 替代可拆分总量。 |
| `from` | Number \| String \| Array | 分布从哪里开始：索引，或 `"start"`、`"center"`、`"edges"`、`"random"`、`"end"`，或如 `[0.25, 0.75]` 的比例。默认 `0`。 |
| `grid` | String \| Array | 使用网格位置而非平面索引：`[rows, columns]`（例如 `[5, 10]`）或 `"auto"` 自动检测。省略为平面数组。 |
| `axis` | String | 对于网格：限制到一个轴（`"x"` 或 `"y"`）。 |
| `ease` | Ease | 沿缓动曲线分布值（例如 `"power1.inOut"`）。默认 `"none"`。 |

**在补间中：** 将 `distribute(config)` 的结果作为属性值传入；GSAP 对每个目标用 `(index, target, targets)` 调用该函数。

```javascript
// 缩放：中间元素 0.5，外边 3（从中心分布 2.5 的总量）
gsap.to(".class", {
  scale: gsap.utils.distribute({
    base: 0.5,
    amount: 2.5,
    from: "center"
  })
});
```

**手动使用：** 用 `(index, target, targets)` 调用返回的函数以获取该索引的值。

```javascript
const distributor = gsap.utils.distribute({
  base: 50,
  amount: 100,
  from: "center",
  ease: "power1.inOut"
});
const targets = gsap.utils.toArray(".box");
const valueForIndex2 = distributor(2, targets[2], targets);
```

更多信息参见 [distribute()](https://gsap.com/docs/v3/GSAP/UtilityMethods/distribute/)。

## 单位和解析

### getUnit(value)

返回值的单位字符串（例如 `"px"`、`"%"`、`"deg"`）。在归一化或转换值时使用。

```javascript
gsap.utils.getUnit("100px");   // "px"
gsap.utils.getUnit("50%");     // "%"
gsap.utils.getUnit(42);        // ""（无单位）
```

### unitize(value, unit)

为数字附加单位，或如果值已有单位则原样返回。在构建 CSS 值或补间结束值时使用。

```javascript
gsap.utils.unitize(100, "px");  // "100px"
gsap.utils.unitize("2rem", "px"); // "2rem"（不变）
```

### splitColor(color, returnHSL?)

将颜色字符串转换为数组：**[red, green, blue]** (0-255)，或 **[red, green, blue, alpha]**（当 alpha 存在或需要时 4 个元素）。传递 **true** 作为第二个参数（**returnHSL**）以获取 **[hue, saturation, lightness]** 或 **[hue, saturation, lightness, alpha]**（HSL/HSLA）。适用于 `"rgb()"`、`"rgba()"`、`"hsl()"`、`"hsla()"`、十六进制和命名颜色（例如 `"red"`）。在动画颜色组件或构建渐变时使用。参见 [splitColor()](https://gsap.com/docs/v3/GSAP/UtilityMethods/splitColor/)。

```javascript
gsap.utils.splitColor("red");                    // [255, 0, 0]
gsap.utils.splitColor("#6fb936");                // [111, 185, 54]
gsap.utils.splitColor("rgba(204, 153, 51, 0.5)"); // [204, 153, 51, 0.5]（4 个元素）
gsap.utils.splitColor("#6fb936", true);          // [94, 55, 47]（HSL：色调、饱和度、明度）
```

## 数组和集合

### selector(scope)

返回一个作用域化的选择器函数，仅在给定元素（或 ref）内查找元素。在组件中使用，使 `.box` 等选择器仅匹配该组件的后代，而非整个文档。接受 DOM 元素或 ref（例如 React ref；处理 `.current`）。

```javascript
const q = gsap.utils.selector(containerRef);
q(".box");        // container 内的 .box 元素数组
gsap.to(q(".circle"), { x: 100 });
```

### toArray(value, scope?)

将值转换为数组：选择器字符串（作用域到元素）、NodeList、HTMLCollection、单个元素或数组。在将混合输入传递給 GSAP（例如 targets）且需要真正的数组时使用。

```javascript
gsap.utils.toArray(".item");           // 元素数组
gsap.utils.toArray(".item", container); // 作用域到 container
gsap.utils.toArray(nodeList);          // [ ... ] 来自 NodeList
```

### pipe(...functions)

组合函数：**pipe(f1, f2, f3)(value)** 返回 f3(f2(f1(value)))。在补间或回调中应用变换链（例如 normalize → mapRange → snap）时使用。

```javascript
const fn = gsap.utils.pipe(
  (v) => gsap.utils.normalize(0, 100, v),
  (v) => gsap.utils.snap(0.1, v)
);
fn(50); // 先归一化然后吸附
```

### wrap(min, max, value?)

将值包裹到 min-max 范围内（包括 min，排除 max）。用于无限滚动或循环值。省略 **value** 获取函数：`wrap(min, max)(value)`。

```javascript
gsap.utils.wrap(0, 360, 370);  // 10
gsap.utils.wrap(0, 360, -10);   // 350

let wrapFn = gsap.utils.wrap(0, 360);
wrapFn(370); // 10
```

### wrapYoyo(min, max, value?)

以悠悠球方式（在边界弹回）包裹范围内的值。用于范围内的来回运动。省略 **value** 获取函数：`wrapYoyo(min, max)(value)`。

```javascript
gsap.utils.wrapYoyo(0, 100, 150); // 50（弹回）

let wrapY = gsap.utils.wrapYoyo(0, 100);
wrapY(150); // 50
```

## 最佳实践

- ✅ 当相同范围/配置被多次使用时（例如滚动处理程序、补间回调），省略 value 参数以获取可复用函数：`let mapFn = gsap.utils.mapRange(0, 1, 0, 360); mapFn(progress)`
- ✅ 对网格对齐或基于步长的值使用 **snap**；当 GSAP 或你的代码需要从选择器或 NodeList 获取真正的数组时使用 **toArray**
- ✅ 在组件中使用 **gsap.utils.selector(scope)**，以便选择器作用域到容器或 ref

## 禁止

- ❌ 假设 **mapRange** / **normalize** 处理单位；它们对数字起作用。在意单位时使用 **getUnit** / **unitize**
- ❌ 覆盖或依赖未文档化的行为；坚持使用文档化的 API

### 了解更多

https://gsap.com/docs/v3/HelperFunctions
