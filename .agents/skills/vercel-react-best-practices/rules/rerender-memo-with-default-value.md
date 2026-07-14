---
title: 将 Memo 化组件的默认非原始参数值提取为常量
impact: MEDIUM
impactDescription: 通过使用常量作为默认值恢复 memo 化
tags: rerender, memo, optimization
---

## 将 Memo 化组件的默认非原始参数值提取为常量

当 memo 化组件对某些非原始可选参数（如数组、函数或对象）具有默认值时，不带该参数调用组件会导致 memo 化失效。这是因为每次重渲染都会创建新的值实例，它们无法通过 `memo()` 中的严格相等比较。

为了解决这个问题，将默认值提取为常量。

**不正确（`onClick` 在每次重渲染时都不同）：**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// 不带可选的 onClick 使用
<UserAvatar />
```

**正确（稳定的默认值）：**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// 不带可选的 onClick 使用
<UserAvatar />
```
