---
title: 基于用户意图预加载
impact: MEDIUM
impactDescription: 减少感知延迟
tags: bundle, preload, user-intent, hover
---

## 基于用户意图预加载

在需要之前预加载重型包以减少感知延迟。

**示例（悬停/聚焦时预加载）：**

```tsx
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => {
    if (typeof window !== 'undefined') {
      void import('./monaco-editor')
    }
  }

  return (
    <button
      onMouseEnter={preload}
      onFocus={preload}
      onClick={onClick}
    >
      Open Editor
    </button>
  )
}
```

**示例（功能标志启用时预加载）：**

```tsx
function FlagsProvider({ children, flags }: Props) {
  useEffect(() => {
    if (flags.editorEnabled && typeof window !== 'undefined') {
      void import('./monaco-editor').then(mod => mod.init())
    }
  }, [flags.editorEnabled])

  return <FlagsContext.Provider value={flags}>
    {children}
  </FlagsContext.Provider>
}
```

`typeof window !== 'undefined'` 检查防止将预加载模块打包用于 SSR，优化了服务端包大小和构建速度。
