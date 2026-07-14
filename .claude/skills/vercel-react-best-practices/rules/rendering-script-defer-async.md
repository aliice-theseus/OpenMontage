---
title: 在 Script 标签上使用 defer 或 async
impact: HIGH
impactDescription: 消除渲染阻塞
tags: rendering, script, defer, async, performance
---

## 在 Script 标签上使用 defer 或 async

**影响：高（消除渲染阻塞）**

没有 `defer` 或 `async` 的 script 标签在脚本下载和执行时会阻塞 HTML 解析。这会延迟首次内容绘制（FCP）和交互时间（TTI）。

- **`defer`**：并行下载，HTML 解析完成后执行，保持执行顺序
- **`async`**：并行下载，准备好后立即执行，不保证执行顺序

对依赖 DOM 或其他脚本的脚本使用 `defer`。对独立的脚本如分析工具使用 `async`。

**错误做法（阻塞渲染）：**

```tsx
export default function Document() {
  return (
    <html>
      <head>
        <script src="https://example.com/analytics.js" />
        <script src="/scripts/utils.js" />
      </head>
      <body>{/* 内容 */}</body>
    </html>
  )
}
```

**正确做法（非阻塞）：**

```tsx
export default function Document() {
  return (
    <html>
      <head>
        {/* 独立脚本 - 使用 async */}
        <script src="https://example.com/analytics.js" async />
        {/* 依赖 DOM 的脚本 - 使用 defer */}
        <script src="/scripts/utils.js" defer />
      </head>
      <body>{/* 内容 */}</body>
    </html>
  )
}
```

**注意：** 在 Next.js 中，优先使用 `next/script` 组件配合 `strategy` 属性，而不是原生 script 标签：

```tsx
import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script src="https://example.com/analytics.js" strategy="afterInteractive" />
      <Script src="/scripts/utils.js" strategy="beforeInteractive" />
    </>
  )
}
```

参考：[MDN - Script 元素](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#defer)
