---
title: 将状态管理与 UI 解耦
impact: MEDIUM
impactDescription: 无需更改 UI 即可切换状态实现
tags: composition, state, architecture
---

## 将状态管理与 UI 解耦

Provider 组件应该是唯一知道状态管理方式的地方。
UI 组件消费 context 接口——它们不知道状态来自
useState、Zustand 还是服务器同步。

**错误（UI 耦合到状态实现）：**

```tsx
function ChannelComposer({ channelId }: { channelId: string }) {
  // UI 组件了解全局状态实现
  const state = useGlobalChannelState(channelId)
  const { submit, updateInput } = useChannelSync(channelId)

  return (
    <Composer.Frame>
      <Composer.Input
        value={state.input}
        onChange={(text) => sync.updateInput(text)}
      />
      <Composer.Submit onPress={() => sync.submit()} />
    </Composer.Frame>
  )
}
```

**正确（状态管理隔离在 Provider 中）：**

```tsx
// Provider 处理所有状态管理细节
function ChannelProvider({
  channelId,
  children,
}: {
  channelId: string
  children: React.ReactNode
}) {
  const { state, update, submit } = useGlobalChannel(channelId)
  const inputRef = useRef(null)

  return (
    <Composer.Provider
      state={state}
      actions={{ update, submit }}
      meta={{ inputRef }}
    >
      {children}
    </Composer.Provider>
  )
}

// UI 组件只知道 context 接口
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// 用法
function Channel({ channelId }: { channelId: string }) {
  return (
    <ChannelProvider channelId={channelId}>
      <ChannelComposer />
    </ChannelProvider>
  )
}
```

**不同的 Provider，相同的 UI：**

```tsx
// 临时表单的本地状态
function ForwardMessageProvider({ children }) {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()

  return (
    <Composer.Provider
      state={state}
      actions={{ update: setState, submit: forwardMessage }}
    >
      {children}
    </Composer.Provider>
  )
}

// 频道的全局同步状态
function ChannelProvider({ channelId, children }) {
  const { state, update, submit } = useGlobalChannel(channelId)

  return (
    <Composer.Provider state={state} actions={{ update, submit }}>
      {children}
    </Composer.Provider>
  )
}
```

同一个 `Composer.Input` 组件可以同时与两个 Provider 一起工作，因为它只
依赖于 context 接口，而非实现。
