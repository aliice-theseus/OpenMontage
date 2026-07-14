---
title: 不要将具有原始结果类型的简单表达式包裹在 useMemo 中
impact: LOW-MEDIUM
impactDescription: 每次渲染浪费计算
tags: rerender, useMemo, optimization
---

## 不要将具有原始结果类型的简单表达式包裹在 useMemo 中

当表达式很简单（几个逻辑或算术运算符）并且结果类型是原始类型（boolean、number、string）时，不要将其包裹在 `useMemo` 中。调用 `useMemo` 和比较钩子依赖可能比表达式本身消耗更多的资源。

**不正确：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading
  }, [user.isLoading, notifications.isLoading])

  if (isLoading) return <Skeleton />
  // 渲染一些标记
}
```

**正确：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading

  if (isLoading) return <Skeleton />
  // 渲染一些标记
}
```
