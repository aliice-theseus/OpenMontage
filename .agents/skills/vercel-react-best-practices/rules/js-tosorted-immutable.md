---
title: 使用 toSorted() 而非 sort() 以保持不可变性
impact: MEDIUM-HIGH
impactDescription: 防止 React 状态中的变更错误
tags: javascript, arrays, immutability, react, state, mutation
---

## 使用 toSorted() 而非 sort() 以保持不可变性

`.sort()` 会原地改变数组，这可能导致 React 状态和属性出现错误。使用 `.toSorted()` 创建新的排序数组而无需改变原数组。

**不正确（改变原始数组）：**

```typescript
function UserList({ users }: { users: User[] }) {
  // 改变了 users 属性数组！
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**正确（创建新数组）：**

```typescript
function UserList({ users }: { users: User[] }) {
  // 创建新的排序数组，原数组不变
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**为什么这很重要：**

1. Props/state 的变更破坏了 React 的不可变性模型——React 期望 props 和 state 被视为只读
2. 导致过期闭包错误——在闭包（回调、effects）中改变数组可能导致意外行为

**浏览器支持（旧浏览器回退）：**

`.toSorted()` 在所有现代浏览器中都可用（Chrome 110+、Safari 16+、Firefox 115+、Node.js 20+）。对于旧环境，使用展开运算符：

```typescript
// 旧浏览器的回退
const sorted = [...items].sort((a, b) => a.value - b.value)
```

**其他不可变数组方法：**

- `.toSorted()` - 不可变排序
- `.toReversed()` - 不可变反转
- `.toSpliced()` - 不可变拼接
- `.with()` - 不可变元素替换
