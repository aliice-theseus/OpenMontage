---
title: 对瞬态值使用 useRef
impact: MEDIUM
impactDescription: 避免频繁更新时的不必要重渲染
tags: rerender, useref, state, performance
---

## 对瞬态值使用 useRef

当一个值频繁变化且你不希望每次更新都重渲染时（例如鼠标跟踪器、定时器、瞬时标志），将其存储在 `useRef` 中而不是 `useState`。将组件状态留给 UI；对临时的 DOM 相关值使用 refs。更新 ref 不会触发重渲染。

**不正确（每次更新都渲染）：**

```tsx
function Tracker() {
  const [lastX, setLastX] = useState(0)

  useEffect(() => {
    const onMove = (e: MouseEvent) => setLastX(e.clientX)
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: lastX,
        width: 8,
        height: 8,
        background: 'black',
      }}
    />
  )
}
```

**正确（追踪时不重渲染）：**

```tsx
function Tracker() {
  const lastXRef = useRef(0)
  const dotRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      lastXRef.current = e.clientX
      const node = dotRef.current
      if (node) {
        node.style.transform = `translateX(${e.clientX}px)`
      }
    }
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      ref={dotRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: 8,
        height: 8,
        background: 'black',
        transform: 'translateX(0px)',
      }}
    />
  )
}
```
