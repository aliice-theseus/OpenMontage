---
title: 不要将结果类型为原始类型的简单表达式包裹在 useMemo 中
impact: LOW-MEDIUM
impactDescription: 每次渲染都浪费计算
tags: rerender, useMemo, optimization
---

## 不要将结果类型为原始类型的简单表达式包裹在 useMemo 中

当表达式很简单（少量逻辑或算术运算符）且结果类型为原始类型（boolean、number、string）时，不要将其包裹在 `useMemo` 中。
调用 `useMemo` 和比较 hook 依赖项可能比表达式本身消耗更多资源。

**错误做法：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading
  }, [user.isLoading, notifications.isLoading])

  if (isLoading) return <Skeleton />
  // 返回一些标记
}
```

**正确做法：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading

  if (isLoading) return <Skeleton />
  // 返回一些标记
}
```
