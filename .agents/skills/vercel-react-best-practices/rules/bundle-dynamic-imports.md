---
title: 对重型组件使用动态导入
impact: CRITICAL
impactDescription: 直接影响 TTI 和 LCP
tags: bundle, dynamic-import, code-splitting, next-dynamic
---

## 对重型组件使用动态导入

使用 `next/dynamic` 延迟加载初始渲染不需要的大型组件。

**不正确（Monaco 与主包一起打包 ~300KB）：**

```tsx
import { MonacoEditor } from './monaco-editor'

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

**正确（Monaco 按需加载）：**

```tsx
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('./monaco-editor').then(m => m.MonacoEditor),
  { ssr: false }
)

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```
