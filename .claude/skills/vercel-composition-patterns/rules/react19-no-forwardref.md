---
title: React 19 API 变化
impact: MEDIUM
impactDescription: 更清晰的组件定义和 context 使用
tags: react19, refs, context, hooks
---

## React 19 API 变化

> **⚠️ 仅 React 19+。** 如果使用 React 18 或更早版本，请跳过本节。

在 React 19 中，`ref` 现在是一个常规属性（不再需要 `forwardRef` 包装），并且 `use()` 替代了 `useContext()`。

**错误（在 React 19 中使用 forwardRef）：**

```tsx
const ComposerInput = forwardRef<TextInput, Props>((props, ref) => {
  return <TextInput ref={ref} {...props} />
})
```

**正确（ref 作为常规属性）：**

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
  return <TextInput ref={ref} {...props} />
}
```

**错误（在 React 19 中使用 useContext）：**

```tsx
const value = useContext(MyContext)
```

**正确（使用 use 替代 useContext）：**

```tsx
const value = use(MyContext)
```

`use()` 还可以有条件地调用，而 `useContext()` 不行。
