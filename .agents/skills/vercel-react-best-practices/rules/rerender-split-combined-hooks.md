---
title: 拆分组合的 Hook 计算
impact: MEDIUM
impactDescription: 避免重新计算独立步骤
tags: rerender, useMemo, useEffect, dependencies, optimization
---

## 拆分组合的 Hook 计算

当一个 hook 包含多个具有不同依赖的独立任务时，将它们拆分为单独的 hooks。组合的 hook 在任何依赖发生变化时都会重新运行所有任务，即使某些任务不使用变化的值。

**不正确（更改 `sortOrder` 重新计算过滤）：**

```tsx
const sortedProducts = useMemo(() => {
  const filtered = products.filter((p) => p.category === category)
  const sorted = filtered.toSorted((a, b) =>
    sortOrder === "asc" ? a.price - b.price : b.price - a.price
  )
  return sorted
}, [products, category, sortOrder])
```

**正确（仅在 products 或 category 变化时重新计算过滤）：**

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

此模式也适用于组合不相关副作用时的 `useEffect`：

**不正确（任一依赖变化时两个 effect 都执行）：**

```tsx
useEffect(() => {
  analytics.trackPageView(pathname)
  document.title = `${pageTitle} | My App`
}, [pathname, pageTitle])
```

**正确（effects 独立执行）：**

```tsx
useEffect(() => {
  analytics.trackPageView(pathname)
}, [pathname])

useEffect(() => {
  document.title = `${pageTitle} | My App`
}, [pageTitle])
```

**注意：** 如果你的项目启用了 [React Compiler](https://react.dev/learn/react-compiler)，它会自动优化依赖追踪，可能会为你处理部分情况。
