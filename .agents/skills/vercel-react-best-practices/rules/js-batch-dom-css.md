---
title: 避免布局颠簸
impact: MEDIUM
impactDescription: 防止强制同步布局并减少性能瓶颈
tags: javascript, dom, css, performance, reflow, layout-thrashing
---

## 避免布局颠簸

避免在样式写入和布局读取之间交替。当你在样式更改之间读取布局属性（如 `offsetWidth`、`getBoundingClientRect()` 或 `getComputedStyle()`）时，浏览器被迫触发同步回流。

**这是可以的（浏览器批处理样式更改）：**
```typescript
function updateElementStyles(element: HTMLElement) {
  // 每行都使样式失效，但浏览器会批处理重新计算
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
}
```

**不正确（交替读写强制回流）：**
```typescript
function layoutThrashing(element: HTMLElement) {
  element.style.width = '100px'
  const width = element.offsetWidth  // 强制回流
  element.style.height = '200px'
  const height = element.offsetHeight  // 再次强制回流
}
```

**正确（批处理写入，然后一次读取）：**
```typescript
function updateElementStyles(element: HTMLElement) {
  // 将所有写入批处理在一起
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
  
  // 在所有写入完成后读取（单次回流）
  const { width, height } = element.getBoundingClientRect()
}
```

**正确（批处理读取，然后写入）：**
```typescript
function avoidThrashing(element: HTMLElement) {
  // 读取阶段 - 先执行所有布局查询
  const rect1 = element.getBoundingClientRect()
  const offsetWidth = element.offsetWidth
  const offsetHeight = element.offsetHeight
  
  // 写入阶段 - 之后再执行所有样式更改
  element.style.width = '100px'
  element.style.height = '200px'
}
```

**更好的做法：使用 CSS 类**
```css
.highlighted-box {
  width: 100px;
  height: 200px;
  background-color: blue;
  border: 1px solid black;
}
```
```typescript
function updateElementStyles(element: HTMLElement) {
  element.classList.add('highlighted-box')
  
  const { width, height } = element.getBoundingClientRect()
}
```

**React 示例：**
```tsx
// 不正确：在样式更改和布局查询之间交替
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  const ref = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (ref.current && isHighlighted) {
      ref.current.style.width = '100px'
      const width = ref.current.offsetWidth // 强制布局
      ref.current.style.height = '200px'
    }
  }, [isHighlighted])
  
  return <div ref={ref}>Content</div>
}

// 正确：切换类
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  return (
    <div className={isHighlighted ? 'highlighted-box' : ''}>
      Content
    </div>
  )
}
```

尽可能优先使用 CSS 类而非内联样式。CSS 文件由浏览器缓存，类提供了更好的关注点分离且更易于维护。

有关强制布局操作的更多信息，请参阅[此 gist](https://gist.github.com/paulirish/5d52fb081b3570c81e3a) 和 [CSS Triggers](https://csstriggers.com/)。
