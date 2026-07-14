---
title: 每次应用加载仅初始化一次，而非每次挂载
impact: LOW-MEDIUM
impactDescription: 避免开发环境中的重复初始化
tags: initialization, useEffect, app-startup, side-effects
---

## 每次应用加载仅初始化一次，而非每次挂载

不要将必须在每次应用加载时运行一次的全局初始化放在组件的 `useEffect([])` 中。组件可能重新挂载，effect 也会重新运行。改用模块级守卫或入口模块中的顶层初始化。

**错误做法（开发环境运行两次，重新挂载时重新运行）：**

```tsx
function Comp() {
  useEffect(() => {
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

**正确做法（每次应用加载一次）：**

```tsx
let didInit = false

function Comp() {
  useEffect(() => {
    if (didInit) return
    didInit = true
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

参考：[初始化应用](https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application)
