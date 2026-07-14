---
title: 对昂贵的派生渲染使用 useDeferredValue
impact: MEDIUM
impactDescription: 在重型计算期间保持输入响应
tags: rerender, useDeferredValue, optimization, concurrent
---

## 对昂贵的派生渲染使用 useDeferredValue

当用户输入触发昂贵的计算或渲染时，使用 `useDeferredValue` 来保持输入响应。延迟的值会滞后，使 React 能够优先处理输入更新，并在空闲时渲染昂贵的结果。

**不正确（过滤时输入感觉卡顿）：**

```tsx
function Search({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const filtered = items.filter(item => fuzzyMatch(item, query))

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <ResultsList results={filtered} />
    </>
  )
}
```

**正确（输入保持灵敏，结果就绪时渲染）：**

```tsx
function Search({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const deferredQuery = useDeferredValue(query)
  const filtered = useMemo(
    () => items.filter(item => fuzzyMatch(item, deferredQuery)),
    [items, deferredQuery]
  )
  const isStale = query !== deferredQuery

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <div style={{ opacity: isStale ? 0.7 : 1 }}>
        <ResultsList results={filtered} />
      </div>
    </>
  )
}
```

**何时使用：**

- 过滤/搜索大型列表
- 响应输入的昂贵可视化（图表、图形）
- 任何导致明显渲染延迟的派生状态

**注意：** 将昂贵的计算包裹在 `useMemo` 中，并将延迟的值作为依赖，否则它仍然在每次渲染时执行。

参考：[React useDeferredValue](https://react.dev/reference/react/useDeferredValue)
