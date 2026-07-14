---
title: 初始化应用一次，而非每次挂载
impact: LOW-MEDIUM
impactDescription: 避免开发环境中的重复初始化
tags: initialization, useEffect, app-startup, side-effects
---

## 初始化应用一次，而非每次挂载

不要将必须每次应用加载运行一次的全局初始化放在组件的 `useEffect([])` 中。组件可能重新挂载，effects 会重新执行。使用模块级守卫或入口模块中的顶级初始化。

**不正确（开发环境中执行两次，重新挂载时再次执行）：**

```tsx
function Comp() {
  useEffect(() => {
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

**正确（每次应用加载一次）：**

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
