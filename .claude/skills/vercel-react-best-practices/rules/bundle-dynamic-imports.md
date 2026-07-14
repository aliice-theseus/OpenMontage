---
title: 对重型组件使用动态导入
impact: CRITICAL
impactDescription: 直接影响 TTI 和 LCP
tags: bundle, dynamic-import, code-splitting, next-dynamic
---

## 对重型组件使用动态导入

使用 `next/dynamic` 懒加载初始渲染不需要的大型组件。

**错误做法（Monaco 与主 chunk 打包，约 300KB）：**

```tsx
import { MonacoEditor } from './monaco-editor'

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

**正确做法（Monaco 按需加载）：**

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
