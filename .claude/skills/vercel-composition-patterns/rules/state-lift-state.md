---
title: 将状态提升到 Provider 组件中
impact: HIGH
impactDescription: 实现在组件边界之外共享状态
tags: composition, state, context, providers
---

## 将状态提升到 Provider 组件中

将状态管理移到专用的 Provider 组件中。这允许主 UI
之外的兄弟组件在不进行属性钻取或使用笨重的 ref 的情况下
访问和修改状态。

**错误（状态困在组件内部）：**

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

// 问题：这个按钮如何访问编辑器状态？
function ForwardMessageDialog() {
  return (
    <Dialog>
      <ForwardMessageComposer />
      <MessagePreview /> {/* 需要编辑器状态 */}
      <DialogActions>
        <CancelButton />
        <ForwardButton /> {/* 需要调用 submit */}
      </DialogActions>
    </Dialog>
  )
}
```

**错误（使用 useEffect 同步状态向上）：**

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
    onInputChange(state.input) // 每次变化都同步 😬
  }, [state.input])
}
```

**错误（提交时从 ref 读取状态）：**

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

**正确（状态提升到 Provider）：**

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
        <MessagePreview /> {/* 自定义组件可以访问状态和操作 */}
        <DialogActions>
          <CancelButton />
          <ForwardButton /> {/* 自定义组件可以访问状态和操作 */}
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  )
}

function ForwardButton() {
  const { actions } = use(Composer.Context)
  return <Button onPress={actions.submit}>转发</Button>
}
```

ForwardButton 位于 Composer.Frame 外部，但仍然可以访问
submit 操作，因为它位于 Provider 内部。即使它是一个一次性
组件，它仍然可以从 UI 本身外部访问编辑器的状态和操作。

**关键洞察：** 需要共享状态的组件不必在视觉上
相互嵌套——它们只需要在同一个 Provider 内部即可。
