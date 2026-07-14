---
title: 提升 RegExp 创建
impact: LOW-MEDIUM
impactDescription: 避免重复创建
tags: javascript, regexp, optimization, memoization
---

## 提升 RegExp 创建

不要在渲染中创建 RegExp。提升到模块作用域或使用 `useMemo()` 记忆化。

**错误做法（每次渲染都 new RegExp）：**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, 'gi')
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**正确做法（记忆化或提升）：**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query]
  )
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**警告（全局 regex 有可变状态）：**

全局 regex（`/g`）有可变的 `lastIndex` 状态：

```typescript
const regex = /foo/g
regex.test('foo')  // true, lastIndex = 3
regex.test('foo')  // false, lastIndex = 0
```
