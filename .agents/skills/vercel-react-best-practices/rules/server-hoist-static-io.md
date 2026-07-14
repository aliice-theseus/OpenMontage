---
title: 将静态 I/O 提升到模块级别
impact: HIGH
impactDescription: 避免每次请求重复的文件/网络 I/O
tags: server, io, performance, next.js, route-handlers, og-image
---

## 将静态 I/O 提升到模块级别

**影响：高（HIGH）（避免每次请求重复的文件/网络 I/O）**

在路由处理程序或服务端函数中加载静态资源（字体、Logo、图片、配置文件）时，将 I/O 操作提升到模块级别。模块级代码在模块首次导入时执行一次，而不是每次请求都执行。这消除了否则会在每次调用时都执行的冗余文件系统读取或网络获取。

**不正确：每次请求都读取字体文件**

```typescript
// app/api/og/route.tsx
import { ImageResponse } from 'next/og'

export async function GET(request: Request) {
  // 每次请求都执行 - 非常昂贵！
  const fontData = await fetch(
    new URL('./fonts/Inter.ttf', import.meta.url)
  ).then(res => res.arrayBuffer())
  
  const logoData = await fetch(
    new URL('./images/logo.png', import.meta.url)
  ).then(res => res.arrayBuffer())

  return new ImageResponse(
    <div style={{ fontFamily: 'Inter' }}>
      <img src={logoData} />
      Hello World
    </div>,
    { fonts: [{ name: 'Inter', data: fontData }] }
  )
}
```

**正确：在模块初始化时加载一次**

```typescript
// app/api/og/route.tsx
import { ImageResponse } from 'next/og'

// 模块级别：在模块首次导入时执行一次
const fontData = fetch(
  new URL('./fonts/Inter.ttf', import.meta.url)
).then(res => res.arrayBuffer())

const logoData = fetch(
  new URL('./images/logo.png', import.meta.url)
).then(res => res.arrayBuffer())

export async function GET(request: Request) {
  // await 已经启动的 promises
  const [font, logo] = await Promise.all([fontData, logoData])

  return new ImageResponse(
    <div style={{ fontFamily: 'Inter' }}>
      <img src={logo} />
      Hello World
    </div>,
    { fonts: [{ name: 'Inter', data: font }] }
  )
}
```

**替代方案：使用 Node.js fs 同步读取文件**

```typescript
// app/api/og/route.tsx
import { ImageResponse } from 'next/og'
import { readFileSync } from 'fs'
import { join } from 'path'

// 在模块级别同步读取 - 仅在模块初始化时阻塞
const fontData = readFileSync(
  join(process.cwd(), 'public/fonts/Inter.ttf')
)

const logoData = readFileSync(
  join(process.cwd(), 'public/images/logo.png')
)

export async function GET(request: Request) {
  return new ImageResponse(
    <div style={{ fontFamily: 'Inter' }}>
      <img src={logoData} />
      Hello World
    </div>,
    { fonts: [{ name: 'Inter', data: fontData }] }
  )
}
```

**通用的 Node.js 示例：加载配置或模板**

```typescript
// 不正确：每次调用都读取配置
export async function processRequest(data: Data) {
  const config = JSON.parse(
    await fs.readFile('./config.json', 'utf-8')
  )
  const template = await fs.readFile('./template.html', 'utf-8')
  
  return render(template, data, config)
}

// 正确：在模块级别加载一次
const configPromise = fs.readFile('./config.json', 'utf-8')
  .then(JSON.parse)
const templatePromise = fs.readFile('./template.html', 'utf-8')

export async function processRequest(data: Data) {
  const [config, template] = await Promise.all([
    configPromise,
    templatePromise
  ])
  
  return render(template, data, config)
}
```

**何时使用此模式：**

- 为 OG 图片生成加载字体
- 加载静态 Logo、图标或水印
- 读取运行时不会更改的配置文件
- 加载邮件模板或其他静态模板
- 在所有请求中相同的任何静态资源

**何时不使用此模式：**

- 每个请求或用户不同的资源
- 可能在运行时更改的文件（改用带 TTL 的缓存）
- 如果保持加载会消耗过多内存的大文件
- 不应在内存中持久存在的敏感数据

**结合 Vercel 的 [Fluid Compute](https://vercel.com/docs/fluid-compute)：** 模块级缓存特别有效，因为多个并发请求共享同一个函数实例。静态资源在请求之间保持加载在内存中，没有冷启动惩罚。

**在传统 Serverless 环境中：** 每次冷启动重新执行模块级代码，但后续的温调用会重用已加载的资源，直到实例被回收。
