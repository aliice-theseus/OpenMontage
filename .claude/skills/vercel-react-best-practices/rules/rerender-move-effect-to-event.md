---
title: 将交互逻辑放在事件处理函数中
impact: MEDIUM
impactDescription: 避免 effect 重新运行和重复的副作用
tags: rerender, useEffect, events, side-effects, dependencies
---

## 将交互逻辑放在事件处理函数中

如果副作用是由特定的用户操作（提交、点击、拖拽）触发的，请在该事件处理函数中执行。不要将操作建模为 state + effect；这会导致 effect 在不相关的变化时重新运行，并可能重复执行操作。

**错误做法（事件建模为 state + effect）：**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false)
  const theme = useContext(ThemeContext)

  useEffect(() => {
    if (submitted) {
      post('/api/register')
      showToast('已注册', theme)
    }
  }, [submitted, theme])

  return <button onClick={() => setSubmitted(true)}>提交</button>
}
```

**正确做法（在处理函数中执行）：**

```tsx
function Form() {
  const theme = useContext(ThemeContext)

  function handleSubmit() {
    post('/api/register')
    showToast('已注册', theme)
  }

  return <button onClick={handleSubmit}>提交</button>
}
```

参考：[这段代码是否应该移到事件处理函数中？](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)
