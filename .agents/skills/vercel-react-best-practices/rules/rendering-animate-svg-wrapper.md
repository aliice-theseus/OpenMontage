---
title: 为 SVG 包装器添加动画，而非 SVG 元素本身
impact: LOW
impactDescription: 启用硬件加速
tags: rendering, svg, css, animation, performance
---

## 为 SVG 包装器添加动画，而非 SVG 元素本身

许多浏览器对 SVG 元素上的 CSS3 动画没有硬件加速。将 SVG 包裹在 `<div>` 中并为包装器添加动画。

**不正确（直接为 SVG 添加动画 - 无硬件加速）：**

```tsx
function LoadingSpinner() {
  return (
    <svg 
      className="animate-spin"
      width="24" 
      height="24" 
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  )
}
```

**正确（为包装器 div 添加动画 - 硬件加速）：**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg 
        width="24" 
        height="24" 
        viewBox="0 0 24 24"
      >
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  )
}
```

这适用于所有 CSS 变换和过渡（`transform`、`opacity`、`translate`、`scale`、`rotate`）。包装器 div 允许浏览器使用 GPU 加速以获得更流畅的动画。
