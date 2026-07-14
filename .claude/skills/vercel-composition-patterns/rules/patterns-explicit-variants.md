---
title: 创建显式组件变体
impact: MEDIUM
impactDescription: 自文档化的代码，无隐藏条件
tags: composition, variants, architecture
---

## 创建显式组件变体

不要创建一个带有许多布尔属性的组件，而是创建显式的变体
组件。每个变体组合它所需的部分。代码文档化了
自身。

**错误（一个组件，多种模式）：**

```tsx
// 这个组件实际渲染了什么？
<Composer
  isThread
  isEditing={false}
  channelId='abc'
  showAttachments
  showFormatting={false}
/>
```

**正确（显式变体）：**

```tsx
// 立即清楚它渲染什么
<ThreadComposer channelId="abc" />

// 或
<EditMessageComposer messageId="xyz" />

// 或
<ForwardMessageComposer messageId="123" />
```

每个实现都是独特、明确且自包含的。但它们每个都可以
使用共享部分。

**实现：**

```tsx
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <ThreadProvider channelId={channelId}>
      <Composer.Frame>
        <Composer.Input />
        <AlsoSendToChannelField channelId={channelId} />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.Submit />
        </Composer.Footer>
      </Composer.Frame>
    </ThreadProvider>
  )
}

function EditMessageComposer({ messageId }: { messageId: string }) {
  return (
    <EditMessageProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.CancelEdit />
          <Composer.SaveEdit />
        </Composer.Footer>
      </Composer.Frame>
    </EditMessageProvider>
  )
}

function ForwardMessageComposer({ messageId }: { messageId: string }) {
  return (
    <ForwardMessageProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input placeholder="如果你愿意，可以添加一条消息。" />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.Mentions />
        </Composer.Footer>
      </Composer.Frame>
    </ForwardMessageProvider>
  )
}
```

每个变体明确说明：

- 它使用什么 Provider/状态
- 它包含哪些 UI 元素
- 哪些操作可用

无需推理布尔属性的组合。没有不可能的状态。
