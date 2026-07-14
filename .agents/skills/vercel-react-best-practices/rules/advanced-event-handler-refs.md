---
title: 将事件处理程序存储在 Refs 中
impact: LOW
impactDescription: 稳定订阅
tags: advanced, hooks, refs, event-handlers, optimization
---

## 将事件处理程序存储在 Refs 中

当在不应因回调更改而重新订阅的 effects 中使用回调时，将其存储在 refs 中。

**不正确（每次渲染都重新订阅）：**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}
```

**正确（稳定订阅）：**

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

**替代方案：如果你使用最新版 React，可以使用 `useEffectEvent`：**

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

`useEffectEvent` 为同一模式提供了更清晰的 API：它创建一个总是调用最新版本处理程序的稳定函数引用。
