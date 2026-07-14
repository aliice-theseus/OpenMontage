---
title: 使用函数式 setState 更新
impact: MEDIUM
impactDescription: 防止过期闭包和不必要的回调重建
tags: react, hooks, useState, useCallback, callbacks, closures
---

## 使用函数式 setState 更新

当基于当前状态值更新状态时，使用 setState 的函数式更新形式，而不是直接引用状态变量。这可以防止过期闭包，消除不必要的依赖，并创建稳定的回调引用。

**错误做法（需要将 state 作为依赖）：**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // 回调必须依赖 items，每次 items 变化都重新创建
  const addItems = useCallback((newItems: Item[]) => {
    setItems([...items, ...newItems])
  }, [items])  // ❌ items 依赖导致重新创建
  
  // 如果忘记依赖，存在过期闭包风险
  const removeItem = useCallback((id: string) => {
    setItems(items.filter(item => item.id !== id))
  }, [])  // ❌ 缺少 items 依赖 - 将使用过期的 items！
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

第一个回调在每次 `items` 变化时都会重新创建，可能导致子组件不必要的重渲染。第二个回调存在过期闭包 bug——它将始终引用初始的 `items` 值。

**正确做法（稳定的回调，无过期闭包）：**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // 稳定回调，永不重新创建
  const addItems = useCallback((newItems: Item[]) => {
    setItems(curr => [...curr, ...newItems])
  }, [])  // ✅ 无需依赖
  
  // 始终使用最新状态，无过期闭包风险
  const removeItem = useCallback((id: string) => {
    setItems(curr => curr.filter(item => item.id !== id))
  }, [])  // ✅ 安全且稳定
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

**好处：**

1. **稳定的回调引用** - 状态变化时无需重新创建回调
2. **无过期闭包** - 始终操作最新状态值
3. **更少的依赖** - 简化依赖数组并减少内存泄漏
4. **防止错误** - 消除 React 闭包错误最常见的来源

**何时使用函数式更新：**

- 任何依赖于当前状态值的 setState
- 在 useCallback/useMemo 内部需要状态时
- 引用状态的事件处理函数
- 更新状态的异步操作

**何时直接更新没问题：**

- 将状态设置为静态值：`setCount(0)`
- 仅从 props/arguments 设置状态：`setName(newName)`
- 状态不依赖于先前的值

**注意：** 如果你的项目启用了 [React Compiler](https://react.dev/learn/react-compiler)，编译器可以自动优化某些情况，但为了正确性和防止过期闭包错误，仍然推荐使用函数式更新。
