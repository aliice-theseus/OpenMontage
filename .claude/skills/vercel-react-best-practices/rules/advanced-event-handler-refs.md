---
title: 将事件处理函数存储在 Refs 中
impact: LOW
impactDescription: 稳定的订阅
tags: advanced, hooks, refs, event-handlers, optimization
---

## 将事件处理函数存储在 Refs 中

当在不应因回调变化而重新订阅的 effect 中使用回调时，将回调存储在 refs 中。

**错误做法（每次渲染都重新订阅）：**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}
```

**正确做法（稳定的订阅）：**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  const handlerRef = useRef(handler)
  useEffect(() => {
    handlerRef.current = handler
  }, [handler])

  useEffect(() => {
    const listener = (e) => handlerRef.current(e)
    window.addEventListener(event, listener)
    return () => window.removeEventListener(event, listener)
  }, [event])
}
```

**替代方案：如果你使用的是最新版 React，使用 `useEffectEvent`：**

```tsx
import { useEffectEvent } from 'react'

function useWindowEvent(event: string, handler: (e) => void) {
  const onEvent = useEffectEvent(handler)

  useEffect(() => {
    window.addEventListener(event, onEvent)
    return () => window.removeEventListener(event, onEvent)
  }, [event])
}
```

`useEffectEvent` 为同一模式提供了更干净的 API：它创建一个始终调用最新版本处理函数的稳定函数引用。
