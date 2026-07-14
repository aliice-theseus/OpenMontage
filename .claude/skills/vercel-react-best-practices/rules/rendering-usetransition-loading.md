---
title: 优先使用 useTransition 而非手动加载状态
impact: LOW
impactDescription: 减少重渲染并提高代码清晰度
tags: rendering, transitions, useTransition, loading, state
---

## 优先使用 useTransition 而非手动加载状态

使用 `useTransition` 而不是手动的 `useState` 来管理加载状态。它提供了内置的 `isPending` 状态并自动管理过渡。

**错误做法（手动加载状态）：**

```tsx
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async (value: string) => {
    setIsLoading(true)
    setQuery(value)
    const data = await fetchResults(value)
    setResults(data)
    setIsLoading(false)
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isLoading && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**正确做法（useTransition 带内置 pending 状态）：**

```tsx
import { useTransition, useState } from 'react'

function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  const handleSearch = (value: string) => {
    setQuery(value) // 立即更新输入
    
    startTransition(async () => {
      // 获取并更新结果
      const data = await fetchResults(value)
      setResults(data)
    })
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**好处：**

- **自动 pending 状态**：无需手动管理 `setIsLoading(true/false)`
- **错误弹性**：即使 transition 抛出异常，pending 状态也能正确重置
- **更好的响应性**：在更新期间保持 UI 响应
- **中断处理**：新的 transition 自动取消待处理的 transition

参考：[useTransition](https://react.dev/reference/react/useTransition)
