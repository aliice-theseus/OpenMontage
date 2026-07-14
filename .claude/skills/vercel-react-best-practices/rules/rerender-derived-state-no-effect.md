---
title: 在渲染期间计算派生状态
impact: MEDIUM
impactDescription: 避免冗余渲染和状态漂移
tags: rerender, derived-state, useEffect, state
---

## 在渲染期间计算派生状态

如果可以从当前 props/state 计算出值，不要将其存储在 state 中或在 effect 中更新。在渲染期间派生它以避免额外的渲染和状态漂移。不要仅仅因为 prop 变化就在 effect 中设置状态；优先使用派生值或带 key 的重置。

**错误做法（冗余状态和 effect）：**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const [fullName, setFullName] = useState('')

  useEffect(() => {
    setFullName(firstName + ' ' + lastName)
  }, [firstName, lastName])

  return <p>{fullName}</p>
}
```

**正确做法（在渲染期间派生）：**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const fullName = firstName + ' ' + lastName

  return <p>{fullName}</p>
}
```

参考：[你可能不需要 Effect](https://react.dev/learn/you-might-not-need-an-effect)
