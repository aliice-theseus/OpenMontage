---
title: 将记忆化组件的默认非原始参数值提取为常量
impact: MEDIUM
impactDescription: 通过使用常量作为默认值恢复记忆化
tags: rerender, memo, optimization
---

## 将记忆化组件的默认非原始参数值提取为常量

当记忆化组件对某些非原始可选参数（如数组、函数或对象）有默认值时，调用该组件时不传递该参数会导致记忆化失效。这是因为每次重渲染都会创建新的值实例，它们无法通过 `memo()` 中的严格相等比较。

为解决此问题，将默认值提取为常量。

**错误做法（`onClick` 每次重渲染都有不同的值）：**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// 使用时不传可选 onClick
<UserAvatar />
```

**正确做法（稳定的默认值）：**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// 使用时不传可选 onClick
<UserAvatar />
```
