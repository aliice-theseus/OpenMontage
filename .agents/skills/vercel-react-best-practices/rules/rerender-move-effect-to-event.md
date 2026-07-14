---
title: 将交互逻辑放入事件处理程序
impact: MEDIUM
impactDescription: 避免 effect 重复执行和重复副作用
tags: rerender, useEffect, events, side-effects, dependencies
---

## 将交互逻辑放入事件处理程序

如果副作用是由特定的用户操作（提交、点击、拖拽）触发的，在事件处理程序中执行它。不要将操作建模为状态 + effect；这会使 effects 在无关更改时重新执行，并且可能重复操作。

**不正确（事件被建模为状态 + effect）：**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false)
  const theme = useContext(ThemeContext)

  useEffect(() => {
    if (submitted) {
      post('/api/register')
      showToast('Registered', theme)
    }
  }, [submitted, theme])

  return <button onClick={() => setSubmitted(true)}>提交</button>
}
```

**正确（在 handler 中执行）：**

```tsx
function Form() {
  const theme = useContext(ThemeContext)

  function handleSubmit() {
    post('/api/register')
    showToast('Registered', theme)
  }

  return <button onClick={handleSubmit}>提交</button>
}
```

参考：[这段代码应该移到事件处理程序中吗？](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)
