---
name: measuring-text
description: 测量文本尺寸、将文本适配到容器中以及检查溢出
metadata:
  tags: measure, text, layout, dimensions, fitText, fillTextBox
---

# 在 Remotion 中测量文本

## 前置条件

如果尚未安装 @remotion/layout-utils，请安装：

```bash
npx remotion add @remotion/layout-utils
```

## 测量文本尺寸

使用 `measureText()` 计算文本的宽度和高度：

```tsx
import { measureText } from "@remotion/layout-utils";

const { width, height } = measureText({
  text: "Hello World",
  fontFamily: "Arial",
  fontSize: 32,
  fontWeight: "bold",
});
```

结果会被缓存——重复调用会返回缓存的结果。

## 将文本适配到指定宽度

使用 `fitText()` 查找容器的最佳字体大小：

```tsx
import { fitText } from "@remotion/layout-utils";

const { fontSize } = fitText({
  text: "Hello World",
  withinWidth: 600,
  fontFamily: "Inter",
  fontWeight: "bold",
});

return (
  <div
    style={{
      fontSize: Math.min(fontSize, 80), // 限制最大 80px
      fontFamily: "Inter",
      fontWeight: "bold",
    }}
  >
    Hello World
  </div>
);
```

## 检查文本溢出

使用 `fillTextBox()` 检查文本是否超出框：

```tsx
import { fillTextBox } from "@remotion/layout-utils";

const box = fillTextBox({ maxBoxWidth: 400, maxLines: 3 });

const words = ["Hello", "World", "This", "is", "a", "test"];
for (const word of words) {
  const { exceedsBox } = box.add({
    text: word + " ",
    fontFamily: "Arial",
    fontSize: 24,
  });
  if (exceedsBox) {
    // 文本会溢出，相应处理
    break;
  }
}
```

## 最佳实践

**先加载字体：** 只有在字体加载完成后才调用测量函数。

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily, waitUntilDone } = loadFont("normal", {
  weights: ["400"],
  subsets: ["latin"],
});

waitUntilDone().then(() => {
  // 现在可以安全测量
  const { width } = measureText({
    text: "Hello",
    fontFamily,
    fontSize: 32,
  });
});
```

**使用 validateFontIsLoaded：** 尽早捕获字体加载问题：

```tsx
measureText({
  text: "Hello",
  fontFamily: "MyCustomFont",
  fontSize: 32,
  validateFontIsLoaded: true, // 如果字体未加载则抛出错误
});
```

**匹配字体属性：** 在测量和渲染时使用相同的属性：

```tsx
const fontStyle = {
  fontFamily: "Inter",
  fontSize: 32,
  fontWeight: "bold" as const,
  letterSpacing: "0.5px",
};

const { width } = measureText({
  text: "Hello",
  ...fontStyle,
});

return <div style={fontStyle}>Hello</div>;
```

**避免 padding 和 border：** 使用 `outline` 代替 `border` 以防止布局差异：

```tsx
<div style={{ outline: "2px solid red" }}>文本内容</div>
```
