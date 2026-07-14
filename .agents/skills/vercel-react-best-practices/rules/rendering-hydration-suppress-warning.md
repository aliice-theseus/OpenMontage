---
title: 抑制预期的注水不匹配
impact: LOW-MEDIUM
impactDescription: 避免已知差异导致的大量注水警告
tags: rendering, hydration, ssr, nextjs
---

## 抑制预期的注水不匹配

在 SSR 框架（例如 Next.js）中，某些值在服务端和客户端上故意不同（随机 ID、日期、区域设置/时区格式化）。对于这些*预期*的不匹配，将动态文本包裹在带有 `suppressHydrationWarning` 的元素中，以防止大量警告。不要用此来隐藏真正的错误。不要过度使用。

**不正确（已知不匹配的警告）：**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>
}
```

**正确（仅抑制预期的不匹配）：**

```tsx
function Timestamp() {
  return (
    <span suppressHydrationWarning>
      {new Date().toLocaleString()}
    </span>
  )
}
```
