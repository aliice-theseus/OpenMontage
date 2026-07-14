---
title: 抑制预期的 hydration 不匹配
impact: LOW-MEDIUM
impactDescription: 避免已知差异产生嘈杂的 hydration 警告
tags: rendering, hydration, ssr, nextjs
---

## 抑制预期的 hydration 不匹配

在 SSR 框架（如 Next.js）中，某些值在服务端和客户端有意不同（随机 ID、日期、区域设置/时区格式）。对于这些*预期*的不匹配，将动态文本包裹在带有 `suppressHydrationWarning` 的元素中，以防止嘈杂的警告。不要将其用于隐藏真正的错误。不要过度使用。

**错误做法（已知的不匹配警告）：**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>
}
```

**正确做法（仅抑制预期的不匹配）：**

```tsx
function Timestamp() {
  return (
    <span suppressHydrationWarning>
      {new Date().toLocaleString()}
    </span>
  )
}
```
