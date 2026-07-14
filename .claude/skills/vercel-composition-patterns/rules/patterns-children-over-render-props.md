---
title: 优先使用 Children 而非渲染属性
impact: MEDIUM
impactDescription: 更清晰的组合，更好的可读性
tags: composition, children, render-props
---

## 优先使用 Children 而非渲染属性

使用 `children` 进行组合，而不是 `renderX` 属性。Children 更易读、
组合更自然，且不需要理解回调签名。

**错误（渲染属性）：**

```tsx
function Composer({
  renderHeader,
  renderFooter,
  renderActions,
}: {
  renderHeader?: () => React.ReactNode
  renderFooter?: () => React.ReactNode
  renderActions?: () => React.ReactNode
}) {
  return (
    <form>
      {renderHeader?.()}
      <Input />
      {renderFooter ? renderFooter() : <DefaultFooter />}
      {renderActions?.()}
    </form>
  )
}

// 用法笨拙且不灵活
return (
  <Composer
    renderHeader={() => <CustomHeader />}
    renderFooter={() => (
      <>
        <Formatting />
        <Emojis />
      </>
    )}
    renderActions={() => <SubmitButton />}
  />
)
```

**正确（带 children 的复合组件）：**

```tsx
function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>
}

function ComposerFooter({ children }: { children: React.ReactNode }) {
  return <footer className='flex'>{children}</footer>
}

// 用法灵活
return (
  <Composer.Frame>
    <CustomHeader />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Emojis />
      <SubmitButton />
    </Composer.Footer>
  </Composer.Frame>
)
```

**何时渲染属性合适：**

```tsx
// 当需要向子组件传递数据时，渲染属性效果很好
<List
  data={items}
  renderItem={({ item, index }) => <Item item={item} index={index} />}
/>
```

当父组件需要向子组件提供数据或状态时，使用渲染属性。
当组合静态结构时，使用 children。
