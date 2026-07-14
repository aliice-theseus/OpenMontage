# 字体翻译

字体是主要的非翻译噪声基底。在未安装真实字体的情况下，相同的 `font-weight: 800` 在 HF 的 `chrome-headless-shell` 上比 Remotion 捆绑的 Chromium 渲染得明显更粗。验证显示，这在噪声基底处造成了约 ~0.025 的平均 SSIM 损失。

## 模式：`@remotion/google-fonts/<Family>`

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";
loadFont("normal", { weights: ["400", "800"] });
```

翻译为 `<head>` 中的 `<link>` 标签：

```html
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap"
    rel="stylesheet"
  />
  <style>
    body {
      font-family: Inter, sans-serif;
    }
  </style>
</head>
```

从导入路径和 `loadFont` 参数中提取字体系列名称和字重。HF 的编译器在渲染时内联 Google Fonts CSS，因此你无需为每次渲染支付网络往返开销。

## 模式：通过 `@font-face` 使用本地字体

```tsx
import { Font } from "remotion";

Font.loadFont("/MyFont.woff2", "MyFont");
```

翻译为 `@font-face` 规则：

```html
<style>
  @font-face {
    font-family: "MyFont";
    src: url("assets/MyFont.woff2") format("woff2");
    font-weight: 400;
    font-style: normal;
  }
</style>
```

将字体文件复制到 HTML 旁边的 `hf-src/assets/` 中。

## 模式：系统字体回退（无字体加载）

```tsx
<div style={{ fontFamily: "Helvetica, Arial, sans-serif" }}>...</div>
```

在 HF 中保留相同字符串 — 但要注意：在没有安装真实 Helvetica 的 Linux 上（典型的 CI 环境），Remotion 和 HF 会回退到_不同的_无衬线系统字体，因为它们捆绑了不同版本的 Chromium。这就是噪声基底：约 ~0.025 的平均 SSIM 损失，在大字重（800+）时表现为不同的笔画宽度。

如果特定测试用例需要精确匹配 Remotion 渲染，显式加载相同的字体 — 不要依赖系统回退。

## 如有疑问：使用 Inter

Inter 在不同 Chromium 版本之间渲染一致且免费。当你需要在验证框架中最小化字体漂移时，将任何"系统无衬线"的 Remotion 合成翻译为使用 Inter。

## 字体加载和 `delayRender`

Remotion 使用 `delayRender()` 来延迟第一帧直到字体加载完成。HF 的编译器在编译时内联 Google Fonts，并通过 Frame Adapter 模式等待 `@font-face` 就绪 — `delayRender` 调用在翻译时丢弃。参见 [media.md](media.md)。

## 多字重加载

当 Remotion 加载多个字重时：

```tsx
loadFont("normal", { weights: ["400", "500", "700", "800"] });
```

将所有字重内联到 Google Fonts URL 中：

```
?family=Inter:wght@400;500;700;800&display=swap
```

翻译规则：枚举合成 CSS 中出现的每个不同的 `font-weight` 值（`font-weight: 800` → 必须加载字重 800）。如果 Remotion 源码加载了实际未使用的字重，则丢弃它们。

## 字体子集化

Remotion 的 `loadFont` 不做子集化；HF 的编译器目前也不做。不要在翻译中尝试优化这一点 — 保持与 Remotion 源码相同的字重集合是无损的。
