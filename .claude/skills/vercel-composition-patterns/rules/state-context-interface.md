---
title: 定义通用 Context 接口以实现依赖注入
impact: HIGH
impactDescription: 实现跨用例的可依赖注入状态
tags: composition, context, state, typescript, dependency-injection
---

## 定义通用 Context 接口以实现依赖注入

为你的组件 context 定义一个**通用接口**，包含三个部分：
`state`、`actions` 和 `meta`。这个接口是一个契约，任何 Provider
都可以实现——使同一组 UI 组件能够与完全不同的
状态实现一起工作。

**核心原则：** 提升状态，组合内部组件，使状态
可依赖注入。

**错误（UI 耦合到特定状态实现）：**

```tsx
function ComposerInput() {
  // 紧密耦合到特定 hook
  const { input, setInput } = useChannelComposerState()
  return <TextInput value={input} onChangeText={setInput} />
}
```

**正确（通用接口启用依赖注入）：**

```tsx
// 定义任何 Provider 都可以实现的通用接口
interface ComposerState {
  input: string
  attachments: Attachment[]
  isSubmitting: boolean
}

interface ComposerActions {
  update: (updater: (state: ComposerState) => ComposerState) => void
  submit: () => void
}

interface ComposerMeta {
  inputRef: React.RefObject<TextInput>
}

interface ComposerContextValue {
  state: ComposerState
  actions: ComposerActions
  meta: ComposerMeta
}

const ComposerContext = createContext<ComposerContextValue | null>(null)
```

**UI 组件消费接口，而非实现：**

```tsx
function ComposerInput() {
  const {
    state,
    actions: { update },
    meta,
  } = use(ComposerContext)

  // 此组件可与实现该接口的任何 Provider 一起使用
  return (
    <TextInput
      ref={meta.inputRef}
      value={state.input}
      onChangeText={(text) => update((s) => ({ ...s, input: text }))}
    />
  )
}
```

**不同的 Provider 实现相同的接口：**

```tsx
// Provider A：临时表单的本地状态
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  const inputRef = useRef(null)
  const submit = useForwardMessage()

  return (
    <ComposerContext
      value={{
        state,
        actions: { update: setState, submit },
        meta: { inputRef },
      }}
    >
      {children}
    </ComposerContext>
  )
}

// Provider B：频道的全局同步状态
function ChannelProvider({ channelId, children }: Props) {
  const { state, update, submit } = useGlobalChannel(channelId)
  const inputRef = useRef(null)

  return (
    <ComposerContext
      value={{
        state,
        actions: { update, submit },
        meta: { inputRef },
      }}
    >
      {children}
    </ComposerContext>
  )
}
```

**相同组合的 UI 可与两者一起使用：**

```tsx
// 与 ForwardMessageProvider（本地状态）一起使用
<ForwardMessageProvider>
  <Composer.Frame>
    <Composer.Input />
    <Composer.Submit />
  </Composer.Frame>
</ForwardMessageProvider>

// 与 ChannelProvider（全局同步状态）一起使用
<ChannelProvider channelId="abc">
  <Composer.Frame>
    <Composer.Input />
    <Composer.Submit />
  </Composer.Frame>
</ChannelProvider>
```

**组件外部的自定义 UI 可以访问状态和操作：**

Provider 边界才是重要的——而不是视觉嵌套。需要
共享状态的组件不必位于 `Composer.Frame` 内部。它们只需要
在 Provider 内部即可。

```tsx
function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        {/* 编辑器 UI */}
        <Composer.Frame>
          <Composer.Input placeholder="如果你愿意，可以添加一条消息。" />
          <Composer.Footer>
            <Composer.Formatting />
            <Composer.Emojis />
          </Composer.Footer>
        </Composer.Frame>

        {/* 编辑器外部的自定义 UI，但在 Provider 内部 */}
        <MessagePreview />

        {/* 对话框底部的操作 */}
        <DialogActions>
          <CancelButton />
          <ForwardButton />
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  )
}

// 此按钮位于 Composer.Frame 外部，但仍可基于其 context 提交！
function ForwardButton() {
  const {
    actions: { submit },
  } = use(ComposerContext)
  return <Button onPress={submit}>转发</Button>
}

// 此预览位于 Composer.Frame 外部，但可以读取编辑器的状态！
function MessagePreview() {
  const { state } = use(ComposerContext)
  return <Preview message={state.input} attachments={state.attachments} />
}
```

`ForwardButton` 和 `MessagePreview` 不在视觉上位于编辑器
框内，但它们仍然可以访问其状态和操作。这就是
将状态提升到 Provider 中的力量。

UI 是你组合在一起的可复用片段。状态由 Provider
进行依赖注入。切换 Provider，保留 UI。
