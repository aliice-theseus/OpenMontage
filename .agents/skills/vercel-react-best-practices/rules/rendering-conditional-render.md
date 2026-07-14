---
title: 使用显式条件渲染
impact: LOW
impactDescription: 防止渲染 0 或 NaN
tags: rendering, conditional, jsx, falsy-values
---

## 使用显式条件渲染

当条件可能为 `0`、`NaN` 或其他会渲染的假值时，使用显式的三元运算符（`? :`）而不是 `&&` 进行条件渲染。

**不正确（当 count 为 0 时渲染 "0"）：**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  )
}

// 当 count = 0 时，渲染：<div>0</div>
// 当 count = 5 时，渲染：<div><span class="badge">5</span></div>
```

**正确（当 count 为 0 时渲染为空）：**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  )
}

// 当 count = 0 时，渲染：<div></div>
// 当 count = 5 时，渲染：<div><span class="badge">5</span></div>
```
