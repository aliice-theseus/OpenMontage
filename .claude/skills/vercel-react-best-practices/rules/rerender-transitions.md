---
title: 对非紧急更新使用 Transition
impact: MEDIUM
impactDescription: 保持 UI 响应性
tags: rerender, transitions, startTransition, performance
---

## 对非紧急更新使用 Transition

将频繁的非紧急状态更新标记为 transition，以保持 UI 响应性。

**错误做法（每次滚动都阻塞 UI）：**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

**正确做法（非阻塞更新）：**

```tsx
import { startTransition } from 'react'

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY))
    }
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```
