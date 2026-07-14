# React 组合模式

**版本 1.0.0**  
Engineering  
2026 年 1 月

> **注意：**  
> 本文档主要供 AI 代理和 LLM 在使用组合模式维护、
> 生成或重构 React 代码库时遵循。人类
> 也可能发现它有用，但这里的指导针对 AI 辅助工作流的自动化
> 和一致性进行了优化。

---

## 摘要

用于构建灵活、可维护的 React 组件的组合模式。通过使用
复合组件、状态提升和内部组合来避免布尔属性泛滥。
这些模式使代码库在规模化时对人和 AI 代理都更易于协作。

---

## 目录

1. [组件架构](#1-组件架构) — **高**
   - 1.1 [避免布尔属性泛滥](#11-避免布尔属性泛滥)
   - 1.2 [使用复合组件](#12-使用复合组件)
2. [状态管理](#2-状态管理) — **中**
   - 2.1 [将状态管理与 UI 解耦](#21-将状态管理与-ui-解耦)
   - 2.2 [定义通用 Context 接口以实现依赖注入](#22-定义通用-context-接口以实现依赖注入)
   - 2.3 [将状态提升到 Provider 组件中](#23-将状态提升到-provider-组件中)
3. [实现模式](#3-实现模式) — **中**
   - 3.1 [创建显式组件变体](#31-创建显式组件变体)
   - 3.2 [优先使用 Children 而非渲染属性](#32-优先使用-children-而非渲染属性)
4. [React 19 API](#4-react-19-api) — **中**
   - 4.1 [React 19 API 变化](#41-react-19-api-变化)

---

## 1. 组件架构

**影响：高**

构建组件的基本模式，以避免属性
泛滥并实现灵活的组合。

### 1.1 避免布尔属性泛滥

**影响：关键（防止不可维护的组件变体）**

不要像 `isThread`、`isEditing`、`isDMThread` 这样添加布尔属性来自定义

组件行为。每个布尔属性都会使可能的状态翻倍，并产生

不可维护的条件逻辑。请使用组合代替。

**错误：布尔属性产生指数级复杂性**

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

**正确：组合消除条件判断**

```tsx
// Channel composer
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

// Thread composer - adds "also send to channel" field
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

// Edit composer - different footer actions
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

### 1.2 使用复合组件

**影响：高（实现灵活的组合，无需属性钻取）**

将复杂组件结构化为具有共享 context 的复合组件。每个

子组件通过 context 而非属性访问共享状态。消费者组合

他们需要的部分。

**错误：带渲染属性的单体组件**

```tsx
function Composer({
  renderHeader,
  renderFooter,
  renderActions,
  showAttachments,
  showFormatting,
  showEmojis,
}: Props) {
  return (
    <form>
      {renderHeader?.()}
      <Input />
      {showAttachments && <Attachments />}
      {renderFooter ? (
        renderFooter()
      ) : (
        <Footer>
          {showFormatting && <Formatting />}
          {showEmojis && <Emojis />}
          {renderActions?.()}
        </Footer>
      )}
    </form>
  )
}
```

**正确：带共享 context 的复合组件**

```tsx
const ComposerContext = createContext<ComposerContextValue | null>(null)

function ComposerProvider({ children, state, actions, meta }: ProviderProps) {
  return (
    <ComposerContext value={{ state, actions, meta }}>
      {children}
    </ComposerContext>
  )
}

function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>
}

function ComposerInput() {
  const {
    state,
    actions: { update },
    meta: { inputRef },
  } = use(ComposerContext)
  return (
    <TextInput
      ref={inputRef}
      value={state.input}
      onChangeText={(text) => update((s) => ({ ...s, input: text }))}
    />
  )
}

function ComposerSubmit() {
  const {
    actions: { submit },
  } = use(ComposerContext)
  return <Button onPress={submit}>发送</Button>
}

// 作为复合组件导出
const Composer = {
  Provider: ComposerProvider,
  Frame: ComposerFrame,
  Input: ComposerInput,
  Submit: ComposerSubmit,
  Header: ComposerHeader,
  Footer: ComposerFooter,
  Attachments: ComposerAttachments,
  Formatting: ComposerFormatting,
  Emojis: ComposerEmojis,
}
```

**用法：**

```tsx
<Composer.Provider state={state} actions={actions} meta={meta}>
  <Composer.Frame>
    <Composer.Header />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Submit />
    </Composer.Footer>
  </Composer.Frame>
</Composer.Provider>
```

消费者明确地组合他们需要的内容。没有隐藏的条件判断。而且 state、actions 和 meta 由父级 Provider 进行依赖注入，允许同一组件结构的多次使用。

---

## 2. 状态管理

**影响：中**

在组合组件中提升状态和管理共享 context 的模式。

### 2.1 将状态管理与 UI 解耦

**影响：中（无需更改 UI 即可切换状态实现）**

Provider 组件应该是唯一知道状态管理方式的地方。

UI 组件消费 context 接口——它们不知道状态来自

useState、Zustand 还是服务器同步。

**错误：UI 耦合到状态实现**

```tsx
function ChannelComposer({ channelId }: { channelId: string }) {
  // UI component knows about global state implementation
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

**正确：状态管理隔离在 Provider 中**

```tsx
// Provider handles all state management details
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

// UI component only knows about the context interface
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

// Usage
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
// Local state for ephemeral forms
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

// Global synced state for channels
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

### 2.2 定义通用 Context 接口以实现依赖注入

**影响：高（实现跨用例的可依赖注入状态）**

为你的组件 context 定义一个**通用接口**，包含三个部分：

`state`、`actions` 和 `meta`。这个接口是一个契约，任何 Provider

都可以实现——使同一组 UI 组件能够与完全不同的

状态实现一起工作。

**核心原则：** 提升状态，组合内部组件，使状态

可依赖注入。

**错误：UI 耦合到特定状态实现**

```tsx
function ComposerInput() {
  // Tightly coupled to a specific hook
  const { input, setInput } = useChannelComposerState()
  return <TextInput value={input} onChangeText={setInput} />
}
```

**正确：通用接口启用依赖注入**

```tsx
// Define a GENERIC interface that any provider can implement
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

  // This component works with ANY provider that implements the interface
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
// Provider A: Local state for ephemeral forms
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

// Provider B: Global synced state for channels
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
// Works with ForwardMessageProvider (local state)
<ForwardMessageProvider>
  <Composer.Frame>
    <Composer.Input />
    <Composer.Submit />
  </Composer.Frame>
</ForwardMessageProvider>

// Works with ChannelProvider (global synced state)
<ChannelProvider channelId="abc">
  <Composer.Frame>
    <Composer.Input />
    <Composer.Submit />
  </Composer.Frame>
</ChannelProvider>
```

**组件外部的自定义 UI 可以访问状态和操作：**

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

Provider 边界才是重要的——而不是视觉嵌套。需要

共享状态的组件不必位于 `Composer.Frame` 内部。它们只需要

在 Provider 内部即可。

`ForwardButton` 和 `MessagePreview` 不在视觉上位于编辑器

框内，但它们仍然可以访问其状态和操作。这就是

将状态提升到 Provider 中的力量。

UI 是你组合在一起的可复用片段。状态由 Provider

进行依赖注入。切换 Provider，保留 UI。

### 2.3 将状态提升到 Provider 组件中

**影响：高（实现在组件边界之外共享状态）**

将状态管理移到专用的 Provider 组件中。这允许主 UI

之外的兄弟组件在不进行属性钻取或使用笨重的 ref 的情况下

访问和修改状态。

**错误：状态困在组件内部**

```tsx
function ForwardMessageComposer() {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()

  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer />
    </Composer.Frame>
  )
}

// Problem: How does this button access composer state?
function ForwardMessageDialog() {
  return (
    <Dialog>
      <ForwardMessageComposer />
      <MessagePreview /> {/* Needs composer state */}
      <DialogActions>
        <CancelButton />
        <ForwardButton /> {/* Needs to call submit */}
      </DialogActions>
    </Dialog>
  )
}
```

**错误：使用 useEffect 同步状态向上**

```tsx
function ForwardMessageDialog() {
  const [input, setInput] = useState('')
  return (
    <Dialog>
      <ForwardMessageComposer onInputChange={setInput} />
      <MessagePreview input={input} />
    </Dialog>
  )
}

function ForwardMessageComposer({ onInputChange }) {
  const [state, setState] = useState(initialState)
  useEffect(() => {
    onInputChange(state.input) // Sync on every change 😬
  }, [state.input])
}
```

**错误：提交时从 ref 读取状态**

```tsx
function ForwardMessageDialog() {
  const stateRef = useRef(null)
  return (
    <Dialog>
      <ForwardMessageComposer stateRef={stateRef} />
      <ForwardButton onPress={() => submit(stateRef.current)} />
    </Dialog>
  )
}
```

**正确：状态提升到 Provider**

```tsx
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()
  const inputRef = useRef(null)

  return (
    <Composer.Provider
      state={state}
      actions={{ update: setState, submit: forwardMessage }}
      meta={{ inputRef }}
    >
      {children}
    </Composer.Provider>
  )
}

function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        <ForwardMessageComposer />
        <MessagePreview /> {/* Custom components can access state and actions */}
        <DialogActions>
          <CancelButton />
          <ForwardButton /> {/* Custom components can access state and actions */}
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  )
}

function ForwardButton() {
  const { actions } = use(Composer.Context)
  return <Button onPress={actions.submit}>Forward</Button>
}
```

The ForwardButton lives outside the Composer.Frame but still has access to the

submit action because it's within the provider. Even though it's a one-off

component, it can still access the composer's state and actions from outside the

UI itself.

**Key insight:** Components that need shared state don't have to be visually

nested inside each other—they just need to be within the same provider.

---

## 3. 实现模式

**影响：中**

实现复合组件和 context Provider 的具体技术。

### 3.1 创建显式组件变体

**影响：中（自文档化的代码，无隐藏条件）**

不要创建一个带有许多布尔属性的组件，而是创建显式的变体

组件。每个变体组合它所需的部分。代码文档化了

自身。

**错误：一个组件，多种模式**

```tsx
// What does this component actually render?
<Composer
  isThread
  isEditing={false}
  channelId='abc'
  showAttachments
  showFormatting={false}
/>
```

**正确：显式变体**

```tsx
// Immediately clear what this renders
<ThreadComposer channelId="abc" />

// Or
<EditMessageComposer messageId="xyz" />

// Or
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
        <Composer.Input placeholder="Add a message, if you'd like." />
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

### 3.2 优先使用 Children 而非渲染属性

**影响：中（更清晰的组合，更好的可读性）**

使用 `children` 进行组合，而不是 `renderX` 属性。Children 更易读、

组合更自然，且不需要理解回调签名。

**错误：渲染属性**

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

// Usage is awkward and inflexible
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

**正确：带 children 的复合组件**

```tsx
function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>
}

function ComposerFooter({ children }: { children: React.ReactNode }) {
  return <footer className='flex'>{children}</footer>
}

// Usage is flexible
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

---

## 4. React 19 API

**影响：中**

仅 React 19+。不要使用 `forwardRef`；使用 `use()` 替代 `useContext()`。

### 4.1 React 19 API 变化

**影响：中（更清晰的组件定义和 context 使用）**

> **⚠️ 仅 React 19+。** 如果使用 React 18 或更早版本，请跳过本节。

在 React 19 中，`ref` 现在是一个常规属性（不再需要 `forwardRef` 包装），并且 `use()` 替代了 `useContext()`。

**错误：在 React 19 中使用 forwardRef**

```tsx
const ComposerInput = forwardRef<TextInput, Props>((props, ref) => {
  return <TextInput ref={ref} {...props} />
})
```

**正确：ref 作为常规属性**

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
  return <TextInput ref={ref} {...props} />
}
```

**错误：在 React 19 中使用 useContext**

```tsx
const value = useContext(MyContext)
```

**正确：使用 use 替代 useContext**

```tsx
const value = use(MyContext)
```

`use()` 还可以有条件地调用，而 `useContext()` 不行。

---

## 参考

1. [https://react.dev](https://react.dev)
2. [https://react.dev/learn/passing-data-deeply-with-context](https://react.dev/learn/passing-data-deeply-with-context)
3. [https://react.dev/reference/react/use](https://react.dev/reference/react/use)
