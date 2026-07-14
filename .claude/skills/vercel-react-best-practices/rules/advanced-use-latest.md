---
title: 使用 useEffectEvent 实现稳定的回调引用
impact: LOW
impactDescription: 防止 effect 重新运行
tags: advanced, hooks, useEffectEvent, refs, optimization
---

## 使用 useEffectEvent 实现稳定的回调引用

在回调中访问最新值，无需将其添加到依赖数组中。防止 effect 重新运行，同时避免过期闭包。

**错误做法（每次回调变化时 effect 都重新运行）：**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300)
    return () => clearTimeout(timeout)
  }, [query, onSearch])
}
```

**正确做法（使用 React 的 useEffectEvent）：**

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
