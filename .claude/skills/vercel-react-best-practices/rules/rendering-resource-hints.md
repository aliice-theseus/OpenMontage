---
title: 使用 React DOM 资源提示
impact: HIGH
impactDescription: 减少关键资源的加载时间
tags: rendering, preload, preconnect, prefetch, resource-hints
---

## 使用 React DOM 资源提示

**影响：高（减少关键资源的加载时间）**

React DOM 提供了向浏览器提示它将需要的资源的 API。这些在服务端组件中特别有用，可以在客户端收到 HTML 之前就开始加载资源。

- **`prefetchDNS(href)`**：为你预期要连接的域名解析 DNS
- **`preconnect(href)`**：与服务器建立连接（DNS + TCP + TLS）
- **`preload(href, options)`**：获取你即将使用的资源（样式表、字体、脚本、图片）
- **`preloadModule(href)`**：获取你即将使用的 ES 模块
- **`preinit(href, options)`**：获取并立即评估样式表或脚本
- **`preinitModule(href)`**：获取并立即评估 ES 模块

**示例（预连接到第三方 API）：**

```tsx
import { preconnect, prefetchDNS } from 'react-dom'

export default function App() {
  prefetchDNS('https://analytics.example.com')
  preconnect('https://api.example.com')

  return <main>{/* 内容 */}</main>
}
```

**示例（预加载关键字体和样式）：**

```tsx
import { preload, preinit } from 'react-dom'

export default function RootLayout({ children }) {
  // 预加载字体文件
  preload('/fonts/inter.woff2', { as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' })

  // 立即获取并应用关键样式表
  preinit('/styles/critical.css', { as: 'style' })

  return (
    <html>
      <body>{children}</body>
    </html>
  )
}
```

**示例（为代码分割路由预加载模块）：**

```tsx
import { preloadModule, preinitModule } from 'react-dom'

function Navigation() {
  const preloadDashboard = () => {
    preloadModule('/dashboard.js', { as: 'script' })
  }

  return (
    <nav>
      <a href="/dashboard" onMouseEnter={preloadDashboard}>
        仪表盘
      </a>
    </nav>
  )
}
```

**每种 API 的适用场景：**

| API | 使用场景 |
|-----|----------|
| `prefetchDNS` | 稍后要连接的第三方域名 |
| `preconnect` | 立即要获取的 API 或 CDN |
| `preload` | 当前页面所需的关键资源 |
| `preloadModule` | 可能下一次导航需要的 JS 模块 |
| `preinit` | 必须早期执行的样式表/脚本 |
| `preinitModule` | 必须早期执行的 ES 模块 |

参考：[React DOM Resource Preloading APIs](https://react.dev/reference/react-dom#resource-preloading-apis)
