---
title: 拆分合并的 Hook 计算
impact: MEDIUM
impactDescription: 避免重新计算独立步骤
tags: rerender, useMemo, useEffect, dependencies, optimization
---

## 拆分合并的 Hook 计算

当 hook 包含多个具有不同依赖的独立任务时，将它们拆分为单独的 hook。合并的 hook 在任何依赖变化时都会重新运行所有任务，即使某些任务不使用变化的值。

**错误做法（更改 `sortOrder` 会重新计算过滤）：**

```tsx
const sortedProducts = useMemo(() => {
  const filtered = products.filter((p) => p.category === category)
  const sorted = filtered.toSorted((a, b) =>
    sortOrder === "asc" ? a.price - b.price : b.price - a.price
  )
  return sorted
}, [products, category, sortOrder])
```

**正确做法（过滤仅在 products 或 category 变化时重新计算）：**

```tsx
const filteredProducts = useMemo(
  () => products.filter((p) => p.category === category),
  [products, category]
)

const sortedProducts = useMemo(
  () =>
    filteredProducts.toSorted((a, b) =>
      sortOrder === "asc" ? a.price - b.price : b.price - a.price
    ),
  [filteredProducts, sortOrder]
)
```

此模式也适用于组合了不相关副作用时的 `useEffect`：

**错误做法（任一依赖变化时两个 effect 都运行）：**

```tsx
useEffect(() => {
  analytics.trackPageView(pathname)
  document.title = `${pageTitle} | 我的应用`
}, [pathname, pageTitle])
```

**正确做法（effect 独立运行）：**

```tsx
useEffect(() => {
  analytics.trackPageView(pathname)
}, [pathname])

useEffect(() => {
  document.title = `${pageTitle} | 我的应用`
}, [pageTitle])
```

**注意：** 如果你的项目启用了 [React Compiler](https://react.dev/learn/react-compiler)，它会自动优化依赖追踪，并可能为你处理其中一些情况。
