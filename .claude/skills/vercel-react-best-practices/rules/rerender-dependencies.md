---
title: 缩小 Effect 依赖范围
impact: LOW
impactDescription: 最小化 effect 重新运行
tags: rerender, useEffect, dependencies, optimization
---

## 缩小 Effect 依赖范围

指定原始类型的依赖而不是对象，以最小化 effect 的重新运行。

**错误做法（任何 user 字段变化都重新运行）：**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**正确做法（仅在 id 变化时重新运行）：**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**对于派生状态，在 effect 外部计算：**

```tsx
// 错误做法：在 width=767, 766, 765... 时都运行
useEffect(() => {
  if (width < 768) {
    enableMobileMode()
  }
}, [width])

// 正确做法：仅在布尔值转换时运行
const isMobile = width < 768
useEffect(() => {
  if (isMobile) {
    enableMobileMode()
  }
}, [isMobile])
```
