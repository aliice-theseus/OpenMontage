---
title: 缩小 Effect 依赖范围
impact: LOW
impactDescription: 最小化 effect 重复执行
tags: rerender, useEffect, dependencies, optimization
---

## 缩小 Effect 依赖范围

指定原始类型依赖而非对象，以最小化 effect 的重复执行。

**不正确（任何用户字段更改都重新执行）：**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**正确（仅在 id 更改时重新执行）：**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**对于派生状态，在 effect 外部计算：**

```tsx
// 不正确：在 width=767, 766, 765... 时都执行
useEffect(() => {
  if (width < 768) {
    enableMobileMode()
  }
}, [width])

// 正确：仅在布尔值转换时执行
const isMobile = width < 768
useEffect(() => {
  if (isMobile) {
    enableMobileMode()
  }
}, [isMobile])
```
