---
title: 避免布尔属性泛滥
impact: CRITICAL
impactDescription: 防止不可维护的组件变体
tags: composition, props, architecture
---

## 避免布尔属性泛滥

不要像 `isThread`、`isEditing`、`isDMThread` 这样添加布尔属性来自定义
组件行为。每个布尔属性都会使可能的状态翻倍，并产生
不可维护的条件逻辑。请使用组合代替。

**错误（布尔属性产生指数级复杂性）：**

```tsx
function Composer({
  onSubmit,
  isThread,
  channelId,
  isDMThread,
  dmId,
  isEditing,
  isForwarding,
}: Props) {
  return (
    <form>
      <Header />
      <Input />
      {isDMThread ? (
        <AlsoSendToDMField id={dmId} />
      ) : isThread ? (
        <AlsoSendToChannelField id={channelId} />
      ) : null}
      {isEditing ? (
        <EditActions />
      ) : isForwarding ? (
        <ForwardActions />
      ) : (
        <DefaultActions />
      )}
      <Footer onSubmit={onSubmit} />
    </form>
  )
}
```

**正确（组合消除条件判断）：**

```tsx
// 频道编辑器
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Attachments />
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// 线程编辑器 - 添加"同时发送到频道"字段
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <AlsoSendToChannelField id={channelId} />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// 编辑编辑器 - 不同的底部操作
function EditComposer() {
  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.CancelEdit />
        <Composer.SaveEdit />
      </Composer.Footer>
    </Composer.Frame>
  )
}
```

每个变体明确地说明了它渲染什么。我们可以在不共享
单个单体父组件的情况下共享内部组件。
