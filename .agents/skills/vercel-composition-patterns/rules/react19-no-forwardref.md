---
title: React 19 API 变更
impact: MEDIUM
impactDescription: 更清晰的组件定义和上下文使用
tags: react19, refs, context, hooks
---

## React 19 API 变更

> **⚠️ 仅 React 19+。** 如果你使用的是 React 18 或更早版本，请跳过此部分。

在 React 19 中，`ref` 现在是一个常规 prop（无需 `forwardRef` 包装器），并且 `use()` 替代了 `useContext()`。

**Incorrect (forwardRef in React 19):**

```tsx
const ComposerInput = forwardRef<TextInput, Props>((props, ref) => {
  return <TextInput ref={ref} {...props} />
})
```

**Correct (ref as a regular prop):**

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
  return <TextInput ref={ref} {...props} />
}
```

**Incorrect (useContext in React 19):**

```tsx
const value = useContext(MyContext)
```

**Correct (use instead of useContext):**

```tsx
const value = use(MyContext)
```

`use()` can also be called conditionally, unlike `useContext()`.
