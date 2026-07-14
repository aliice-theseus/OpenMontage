---
title: 使用 toSorted() 而非 sort() 保持不可变性
impact: MEDIUM-HIGH
impactDescription: 防止 React 状态中的突变错误
tags: javascript, arrays, immutability, react, state, mutation
---

## 使用 toSorted() 而非 sort() 保持不可变性

`.sort()` 会在原数组上进行修改，这可能导致 React 状态和 props 的错误。使用 `.toSorted()` 创建新的排序数组而不改变原数组。

**错误做法（修改原数组）：**

```typescript
function UserList({ users }: { users: User[] }) {
  // 修改了 users prop 数组！
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**正确做法（创建新数组）：**

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

**为什么这在 React 中很重要：**

1. Props/state 的突变破坏了 React 的不可变性模型——React 期望 props 和 state 被视为只读
2. 导致过期闭包错误——在闭包（回调、effect）中修改数组可能导致意外行为

**浏览器支持（旧版浏览器的回退方案）：**

`.toSorted()` 在所有现代浏览器中可用（Chrome 110+、Safari 16+、Firefox 115+、Node.js 20+）。对于旧环境，使用展开运算符：

```typescript
// 旧版浏览器的回退方案
const sorted = [...items].sort((a, b) => a.value - b.value)
```

**其他不可变数组方法：**

- `.toSorted()` - 不可变排序
- `.toReversed()` - 不可变反转
- `.toSpliced()` - 不可变拼接
- `.with()` - 不可变元素替换
