---
title: useEffectEvent 用于稳定回调引用
impact: LOW
impactDescription: 防止 effect 重复执行
tags: advanced, hooks, useEffectEvent, refs, optimization
---

## useEffectEvent 用于稳定回调引用

在回调中访问最新值，而不必将它们添加到依赖数组中。防止 effect 重复执行，同时避免过期闭包。

**不正确（每次回调更改时 effect 都重新执行）：**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300)
    return () => clearTimeout(timeout)
  }, [query, onSearch])
}
```

**正确（使用 React 的 useEffectEvent）：**

```tsx
import { useEffectEvent } from 'react';

function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  const onSearchEvent = useEffectEvent(onSearch)

  useEffect(() => {
    const timeout = setTimeout(() => onSearchEvent(query), 300)
    return () => clearTimeout(timeout)
  }, [query])
}
```
