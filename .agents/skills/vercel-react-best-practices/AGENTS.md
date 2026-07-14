# React 最佳实践

**版本 1.0.0**  
Vercel Engineering  
2026 年 1 月

> **注意：**  
> 本文档主要供代理和 LLM 在维护、生成或重构 React 和 Next.js 代码库时遵循。  
> 人类也可能发现它有用，但这里的指导针对自动化和 AI 辅助工作流程的一致性进行了优化。

---

## 摘要

React 和 Next.js 应用的全面性能优化指南，专为 AI 代理和 LLM 设计。包含 8 个类别的 40+ 条规则，按影响程度从致命（消除瀑布请求、减少包大小）到增量（高级模式）排序。每条规则包括详细解释、对比错误与正确实现的真实示例，以及具体的影响指标，以指导自动化重构和代码生成。

---

## 目录

1. [消除瀑布请求](#1-消除瀑布请求) — **致命（CRITICAL）**
   - 1.1 [将 Await 延迟到需要时](#11-将-await-延迟到需要时)
   - 1.2 [基于依赖的并行化](#12-基于依赖的并行化)
   - 1.3 [防止 API 路由中的瀑布链](#13-防止-api-路由中的瀑布链)
   - 1.4 [对独立操作使用 Promise.all()](#14-对独立操作使用-promiseall)
   - 1.5 [策略性 Suspense 边界](#15-策略性-suspense-边界)
2. [包大小优化](#2-包大小优化) — **致命（CRITICAL）**
   - 2.1 [避免 Barrel 文件导入](#21-避免-barrel-文件导入)
   - 2.2 [条件模块加载](#22-条件模块加载)
   - 2.3 [延迟非关键第三方库](#23-延迟非关键第三方库)
   - 2.4 [对重型组件使用动态导入](#24-对重型组件使用动态导入)
   - 2.5 [基于用户意图预加载](#25-基于用户意图预加载)
3. [服务端性能](#3-服务端性能) — **高（HIGH）**
   - 3.1 [像 API 路由一样认证 Server Actions](#31-像-api-路由一样认证-server-actions)
   - 3.2 [避免 RSC 属性中的重复序列化](#32-避免-rsc-属性中的重复序列化)
   - 3.3 [跨请求 LRU 缓存](#33-跨请求-lru-缓存)
   - 3.4 [将静态 I/O 提升到模块级别](#34-将静态-io-提升到模块级别)
   - 3.5 [最小化 RSC 边界的序列化](#35-最小化-rsc-边界的序列化)
   - 3.6 [通过组件组合实现并行数据获取](#36-通过组件组合实现并行数据获取)
   - 3.7 [并行嵌套数据获取](#37-并行嵌套数据获取)
   - 3.8 [使用 React.cache() 进行单请求去重](#38-使用-reactcache-进行单请求去重)
   - 3.9 [使用 after() 进行非阻塞操作](#39-使用-after-进行非阻塞操作)
4. [客户端数据获取](#4-客户端数据获取) — **中高（MEDIUM-HIGH）**
   - 4.1 [去重全局事件监听器](#41-去重全局事件监听器)
   - 4.2 [使用被动事件监听器提升滚动性能](#42-使用被动事件监听器提升滚动性能)
   - 4.3 [使用 SWR 进行自动去重](#43-使用-swr-进行自动去重)
   - 4.4 [版本化和最小化 localStorage 数据](#44-版本化和最小化-localstorage-数据)
5. [重渲染优化](#5-重渲染优化) — **中（MEDIUM）**
   - 5.1 [在渲染期间计算派生状态](#51-在渲染期间计算派生状态)
   - 5.2 [将状态读取延迟到使用点](#52-将状态读取延迟到使用点)
   - 5.3 [不要将具有原始结果类型的简单表达式包裹在 useMemo 中](#53-不要将具有原始结果类型的简单表达式包裹在-usememo-中)
   - 5.4 [不要在组件内部定义组件](#54-不要在组件内部定义组件)
   - 5.5 [将 Memo 化组件的默认非原始参数值提取为常量](#55-将-memo-化组件的默认非原始参数值提取为常量)
   - 5.6 [提取到 Memo 化组件中](#56-提取到-memo-化组件中)
   - 5.7 [缩小 Effect 依赖范围](#57-缩小-effect-依赖范围)
   - 5.8 [将交互逻辑放入事件处理程序](#58-将交互逻辑放入事件处理程序)
   - 5.9 [拆分组合的 Hook 计算](#59-拆分组合的-hook-计算)
   - 5.10 [订阅派生状态](#510-订阅派生状态)
   - 5.11 [使用函数式 setState 更新](#511-使用函数式-setstate-更新)
   - 5.12 [使用惰性状态初始化](#512-使用惰性状态初始化)
   - 5.13 [对非紧急更新使用 Transition](#513-对非紧急更新使用-transition)
   - 5.14 [对昂贵的派生渲染使用 useDeferredValue](#514-对昂贵的派生渲染使用-usedeferredvalue)
   - 5.15 [对瞬态值使用 useRef](#515-对瞬态值使用-useref)
6. [渲染性能](#6-渲染性能) — **中（MEDIUM）**
   - 6.1 [为 SVG 包装器添加动画，而非 SVG 元素本身](#61-为-svg-包装器添加动画而非-svg-元素本身)
   - 6.2 [对长列表使用 CSS content-visibility](#62-对长列表使用-css-content-visibility)
   - 6.3 [提升静态 JSX 元素](#63-提升静态-jsx-元素)
   - 6.4 [优化 SVG 精度](#64-优化-svg-精度)
   - 6.5 [防止注水不匹配且不闪屏](#65-防止注水不匹配且不闪屏)
   - 6.6 [抑制预期的注水不匹配](#66-抑制预期的注水不匹配)
   - 6.7 [使用 Activity 组件进行显示/隐藏](#67-使用-activity-组件进行显示隐藏)
   - 6.8 [在 Script 标签上使用 defer 或 async](#68-在-script-标签上使用-defer-或-async)
   - 6.9 [使用显式条件渲染](#69-使用显式条件渲染)
   - 6.10 [使用 React DOM 资源提示](#610-使用-react-dom-资源提示)
   - 6.11 [优先使用 useTransition 而非手动加载状态](#611-优先使用-usetransition-而非手动加载状态)
7. [JavaScript 性能](#7-javascript-性能) — **低中（LOW-MEDIUM）**
   - 7.1 [避免布局颠簸](#71-避免布局颠簸)
   - 7.2 [为重复查找构建索引映射](#72-为重复查找构建索引映射)
   - 7.3 [在循环中缓存属性访问](#73-在循环中缓存属性访问)
   - 7.4 [缓存重复函数调用](#74-缓存重复函数调用)
   - 7.5 [缓存 Storage API 调用](#75-缓存-storage-api-调用)
   - 7.6 [合并多个数组迭代](#76-合并多个数组迭代)
   - 7.7 [使用 requestIdleCallback 延迟非关键工作](#77-使用-requestidlecallback-延迟非关键工作)
   - 7.8 [数组比较前先检查长度](#78-数组比较前先检查长度)
   - 7.9 [从函数中提前返回](#79-从函数中提前返回)
   - 7.10 [提升 RegExp 创建](#710-提升-regexp-创建)
   - 7.11 [使用 flatMap 一步完成映射和过滤](#711-使用-flatmap-一步完成映射和过滤)
   - 7.12 [使用循环而非排序求最小/最大值](#712-使用循环而非排序求最小最大值)
   - 7.13 [使用 Set/Map 进行 O(1) 查找](#713-使用-setmap-进行-o1-查找)
   - 7.14 [使用 toSorted() 而非 sort() 以保持不可变性](#714-使用-tosorted-而非-sort-以保持不可变性)
8. [高级模式](#8-高级模式) — **低（LOW）**
   - 8.1 [初始化应用一次，而非每次挂载](#81-初始化应用一次而非每次挂载)
   - 8.2 [将事件处理程序存储在 Refs 中](#82-将事件处理程序存储在-refs-中)
   - 8.3 [useEffectEvent 用于稳定回调引用](#83-useeffectevent-用于稳定回调引用)

---

## 1. 消除瀑布请求

**影响：致命（CRITICAL）**

瀑布请求是 #1 性能杀手。每个连续的 await 都会增加完整的网络延迟。消除它们能带来最大的收益。

### 1.1 将 Await 延迟到需要时

**影响：高（HIGH）（避免阻塞未使用的代码路径）**

将 `await` 操作移到实际使用的分支中，以避免阻塞不需要它们的代码路径。

**不正确：阻塞两个分支**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  const userData = await fetchUserData(userId)
  
  if (skipProcessing) {
    // 虽然立即返回，但仍然等待了 userData
    return { skipped: true }
  }
  
  // 只有这个分支使用 userData
  return processUserData(userData)
}
```

**正确：仅在需要时阻塞**

```typescript
async function handleRequest(userId: string, skipProcessing: boolean) {
  if (skipProcessing) {
    // 无需等待，立即返回
    return { skipped: true }
  }
  
  // 仅在需要时获取
  const userData = await fetchUserData(userId)
  return processUserData(userData)
}
```

**另一个示例：提前返回优化**

```typescript
// 不正确：总是获取权限
async function updateResource(resourceId: string, userId: string) {
  const permissions = await fetchPermissions(userId)
  const resource = await getResource(resourceId)
  
  if (!resource) {
    return { error: 'Not found' }
  }
  
  if (!permissions.canEdit) {
    return { error: 'Forbidden' }
  }
  
  return await updateResourceData(resource, permissions)
}

// 正确：仅在需要时获取
async function updateResource(resourceId: string, userId: string) {
  const resource = await getResource(resourceId)
  
  if (!resource) {
    return { error: 'Not found' }
  }
  
  const permissions = await fetchPermissions(userId)
  
  if (!permissions.canEdit) {
    return { error: 'Forbidden' }
  }
  
  return await updateResourceData(resource, permissions)
}
```

当跳过的分支经常被执行，或延迟的操作非常昂贵时，这种优化尤其有价值。

### 1.2 基于依赖的并行化

**影响：致命（CRITICAL）（2-10× 改进）**

对于部分依赖的操作，使用 `better-all` 最大化并行度。它会在最早可能的时间自动启动每个任务。

**不正确：profile 不必要地等待 config**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**正确：config 和 profile 并行运行**

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

**没有额外依赖的替代方案：**

```typescript
const userPromise = fetchUser()
const profilePromise = userPromise.then(user => fetchProfile(user.id))

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise
])
```

我们也可以先创建所有 promise，最后再执行 `Promise.all()`。

参考：[https://github.com/shuding/better-all](https://github.com/shuding/better-all)

### 1.3 防止 API 路由中的瀑布链

**影响：致命（CRITICAL）（2-10× 改进）**

在 API 路由和 Server Actions 中，立即启动独立操作，即使你还没有 await 它们。

**不正确：config 等待 auth，data 等待两者**

```typescript
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}
```

**正确：auth 和 config 立即启动**

```typescript
export async function GET(request: Request) {
  const sessionPromise = auth()
  const configPromise = fetchConfig()
  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])
  return Response.json({ data, config })
}
```

对于具有更复杂依赖链的操作，使用 `better-all` 自动最大化并行度（参见基于依赖的并行化）。

### 1.4 对独立操作使用 Promise.all()

**影响：致命（CRITICAL）（2-10× 改进）**

当异步操作之间没有依赖关系时，使用 `Promise.all()` 并发执行它们。

**不正确：顺序执行，3 次往返**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**正确：并行执行，1 次往返**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

### 1.5 策略性 Suspense 边界

**影响：高（HIGH）（更快的初始绘制）**

与其在异步组件中返回 JSX 之前等待数据，不如使用 Suspense 边界在数据加载时更快地显示包装器 UI。

**不正确：包装器被数据获取阻塞**

```tsx
async function Page() {
  const data = await fetchData() // 阻塞整个页面
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <DataDisplay data={data} />
      </div>
      <div>Footer</div>
    </div>
  )
}
```

整个布局等待数据，即使只有中间部分需要它。

**正确：包装器立即显示，数据流式进入**

```tsx
function Page() {
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <Suspense fallback={<Skeleton />}>
          <DataDisplay />
        </Suspense>
      </div>
      <div>Footer</div>
    </div>
  )
}

async function DataDisplay() {
  const data = await fetchData() // 仅阻塞此组件
  return <div>{data.content}</div>
}
```

Sidebar、Header 和 Footer 立即渲染。只有 DataDisplay 等待数据。

**替代方案：在组件间共享 promise**

```tsx
function Page() {
  // 立即开始获取，但不 await
  const dataPromise = fetchData()
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
      <div>Footer</div>
    </div>
  )
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // 解包 promise
  return <div>{data.content}</div>
}

function DataSummary({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // 重用同一个 promise
  return <div>{data.summary}</div>
}
```

两个组件共享同一个 promise，所以只发生一次获取。布局立即渲染，两个组件一起等待。

**何时不使用此模式：**

- 布局决策所需的关键数据（影响定位）
- 首屏 SEO 关键内容
- 小而快的查询，Suspense 开销不值当
- 当你想避免布局偏移（加载 → 内容跳跃）

**权衡：** 更快的初始绘制 vs 潜在的布局偏移。根据你的 UX 优先级选择。

---

## 2. 包大小优化

**影响：致命（CRITICAL）**

减少初始包大小可改善可交互时间和最大内容绘制。

### 2.1 避免 Barrel 文件导入

**影响：致命（CRITICAL）（200-800ms 导入成本，构建缓慢）**

直接从源文件导入，而不是通过 barrel 文件，以避免加载数千个未使用的模块。**Barrel 文件**是重新导出多个模块的入口点（例如，执行 `export * from './module'` 的 `index.js`）。

流行的图标和组件库在其入口文件中可能包含**多达 10,000 个重新导出**。对于许多 React 包，**仅导入就需要 200-800ms**，影响开发速度和生产环境的冷启动。

**为什么 tree-shaking 没有帮助：** 当库被标记为外部（未打包）时，打包器无法优化它。如果将其打包以启用 tree-shaking，构建会因分析整个模块图而变得明显更慢。

**不正确：导入整个库**

```tsx
import { Check, X, Menu } from 'lucide-react'
// 加载 1,583 个模块，开发环境多花 ~2.8s
// 每次冷启动运行时成本：200-800ms

import { Button, TextField } from '@mui/material'
// 加载 2,225 个模块，开发环境多花 ~4.2s
```

**正确 - Next.js 13.5+（推荐）：**

```tsx
// 保留标准导入 - Next.js 将其转换为直接导入
import { Check, X, Menu } from 'lucide-react'
// 完整的 TypeScript 支持，无需手动路径处理
```

这是推荐的方法，因为它保留了 TypeScript 类型安全和编辑器自动补全，同时消除了 barrel 导入成本。

**正确 - 直接导入（非 Next.js 项目）：**

```tsx
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
// 只加载你使用的部分
```

> **TypeScript 警告：** 某些库（特别是 `lucide-react`）不为深度导入路径提供 `.d.ts` 文件。从 `lucide-react/dist/esm/icons/check` 导入会解析为隐式 `any` 类型，在 `strict` 或 `noImplicitAny` 下会导致错误。优先使用 `optimizePackageImports`（如果可用），或在使用直接导入前验证库是否为其子路径导出类型。

这些优化可提供 15-70% 更快的开发启动、28% 更快的构建、40% 更快的冷启动以及显著更快的 HMR。

常受影响的库：`lucide-react`、`@mui/material`、`@mui/icons-material`、`@tabler/icons-react`、`react-icons`、`@headlessui/react`、`@radix-ui/react-*`、`lodash`、`ramda`、`date-fns`、`rxjs`、`react-use`。

参考：[https://vercel.com/blog/how-we-optimized-package-imports-in-next-js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)

### 2.2 条件模块加载

**影响：高（HIGH）（仅在需要时加载大数据）**

仅在功能激活时加载大数据或模块。

**示例：延迟加载动画帧**

```tsx
function AnimationPlayer({ enabled, setEnabled }: { enabled: boolean; setEnabled: React.Dispatch<React.SetStateAction<boolean>> }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js')
        .then(mod => setFrames(mod.frames))
        .catch(() => setEnabled(false))
    }
  }, [enabled, frames, setEnabled])

  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

`typeof window !== 'undefined'` 检查防止将此模块打包用于 SSR，优化了服务端包大小和构建速度。

### 2.3 延迟非关键第三方库

**影响：中（MEDIUM）（在注水后加载）**

分析、日志记录和错误跟踪不会阻挡用户交互。在注水后加载它们。

**不正确：阻塞初始包**

```tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

**正确：在注水后加载**

```tsx
import dynamic from 'next/dynamic'

const Analytics = dynamic(
  () => import('@vercel/analytics/react').then(m => m.Analytics),
  { ssr: false }
)

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

### 2.4 对重型组件使用动态导入

**影响：致命（CRITICAL）（直接影响 TTI 和 LCP）**

使用 `next/dynamic` 延迟加载初始渲染不需要的大型组件。

**不正确：Monaco 与主包一起打包 ~300KB**

```tsx
import { MonacoEditor } from './monaco-editor'

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />
}
```

**正确：Monaco 按需加载**

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

### 2.5 基于用户意图预加载

**影响：中（MEDIUM）（减少感知延迟）**

在需要之前预加载重型包以减少感知延迟。

**示例：悬停/聚焦时预加载**

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
      打开编辑器
    </button>
  )
}
```

**示例：功能标志启用时预加载**

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

---

## 3. 服务端性能

**影响：高（HIGH）**

优化服务端渲染和数据获取可以消除服务端的瀑布请求并减少响应时间。

### 3.1 像 API 路由一样认证 Server Actions

**影响：致命（CRITICAL）（防止对服务端变更的未授权访问）**

Server Actions（使用 `"use server"` 的函数）像 API 路由一样暴露为公共端点。始终**在每个 Server Action 内部**验证身份验证和授权——不要仅依赖中间件、布局守卫或页面级检查，因为 Server Actions 可以直接被调用。

Next.js 文档明确说明："将 Server Actions 视为面向公众的 API 端点，并验证用户是否被允许执行变更操作。"

**不正确：无身份验证检查**

```typescript
'use server'

export async function deleteUser(userId: string) {
  // 任何人都可以调用！没有身份验证检查
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**正确：在 action 内部进行身份验证**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { unauthorized } from '@/lib/errors'

export async function deleteUser(userId: string) {
  // 始终在 action 内部检查身份验证
  const session = await verifySession()
  
  if (!session) {
    throw unauthorized('必须登录')
  }
  
  // 同时检查授权
  if (session.user.role !== 'admin' && session.user.id !== userId) {
    throw unauthorized('不能删除其他用户')
  }
  
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**带输入验证：**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { z } from 'zod'

const updateProfileSchema = z.object({
  userId: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email()
})

export async function updateProfile(data: unknown) {
  // 首先验证输入
  const validated = updateProfileSchema.parse(data)
  
  // 然后验证身份
  const session = await verifySession()
  if (!session) {
    throw new Error('未授权')
  }
  
  // 然后检查授权
  if (session.user.id !== validated.userId) {
    throw new Error('只能更新自己的资料')
  }
  
  // 最后执行变更
  await db.user.update({
    where: { id: validated.userId },
    data: {
      name: validated.name,
      email: validated.email
    }
  })
  
  return { success: true }
}
```

参考：[https://nextjs.org/docs/app/guides/authentication](https://nextjs.org/docs/app/guides/authentication)

### 3.2 避免 RSC 属性中的重复序列化

**影响：低（LOW）（通过避免重复序列化减少网络传输）**

RSC→client 序列化按对象引用去重，而非按值。相同引用 = 序列化一次；新引用 = 再次序列化。在客户端而非服务端进行转换操作（`.toSorted()`、`.filter()`、`.map()`）。

**不正确：重复数组**

```tsx
// RSC：发送 6 个字符串（2 个数组 × 3 项）
<ClientList usernames={usernames} usernamesOrdered={usernames.toSorted()} />
```

**正确：发送 3 个字符串**

```tsx
// RSC：发送一次
<ClientList usernames={usernames} />

// 客户端：在那里转换
'use client'
const sorted = useMemo(() => [...usernames].sort(), [usernames])
```

**嵌套去重行为：**

```tsx
// string[] - 重复所有内容
usernames={['a','b']} sorted={usernames.toSorted()} // 发送 4 个字符串

// object[] - 仅重复数组结构
users={[{id:1},{id:2}]} sorted={users.toSorted()} // 发送 2 个数组 + 2 个唯一对象（不是 4）
```

去重是递归工作的。影响因数据类型而异：

- `string[]`、`number[]`、`boolean[]`：**高影响** - 数组 + 所有原始类型完全重复
- `object[]`：**低影响** - 数组被重复，但嵌套对象按引用去重

**破坏去重的操作（创建新引用）：**

- 数组：`.toSorted()`、`.filter()`、`.map()`、`.slice()`、`[...arr]`
- 对象：`{...obj}`、`Object.assign()`、`structuredClone()`、`JSON.parse(JSON.stringify())`

**更多示例：**

```tsx
// ❌ 不良
<C users={users} active={users.filter(u => u.active)} />
<C product={product} productName={product.name} />

// ✅ 良好
<C users={users} />
<C product={product} />
// 在客户端进行过滤/解构
```

**例外：** 当转换成本很高或客户端不需要原始数据时，传递派生数据。

### 3.3 跨请求 LRU 缓存

**影响：高（HIGH）（跨请求缓存）**

`React.cache()` 仅在一个请求内有效。对于跨顺序请求共享的数据（用户点击按钮 A 然后按钮 B），使用 LRU 缓存。

**实现：**

```typescript
import { LRUCache } from 'lru-cache'

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000  // 5 分钟
})

export async function getUser(id: string) {
  const cached = cache.get(id)
  if (cached) return cached

  const user = await db.user.findUnique({ where: { id } })
  cache.set(id, user)
  return user
}

// 请求 1：数据库查询，结果被缓存
// 请求 2：缓存命中，无数据库查询
```

在连续用户操作在数秒内多次访问需要相同数据的端点时使用。

**结合 Vercel 的 [Fluid Compute](https://vercel.com/docs/fluid-compute)：** LRU 缓存特别有效，因为多个并发请求可以共享同一个函数实例和缓存。这意味着缓存可以在请求之间持久存在，无需 Redis 等外部存储。

**在传统 Serverless 环境中：** 每次调用都在隔离环境中运行，因此考虑使用 Redis 进行跨进程缓存。

参考：[https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)

### 3.4 将静态 I/O 提升到模块级别

**影响：高（HIGH）（避免每次请求重复的文件/网络 I/O）**

在路由处理程序或服务端函数中加载静态资源（字体、Logo、图片、配置文件）时，将 I/O 操作提升到模块级别。模块级代码在模块首次导入时执行一次，而不是每次请求都执行。这消除了否则会在每次调用时都执行的冗余文件系统读取或网络获取。

**不正确：每次请求都读取字体文件**

**正确：在模块初始化时加载一次**

**替代方案：使用 Node.js fs 同步读取文件**

**通用的 Node.js 示例：加载配置或模板**

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

### 3.5 最小化 RSC 边界的序列化

**影响：高（HIGH）（减少数据传输大小）**

React 服务端/客户端边界将所有对象属性序列化为字符串，并嵌入到 HTML 响应和后续的 RSC 请求中。这些序列化数据直接影响页面权重和加载时间，所以**大小非常重要**。只传递客户端实际使用的字段。

**不正确：序列化所有 50 个字段**

```tsx
async function Page() {
  const user = await fetchUser()  // 50 个字段
  return <Profile user={user} />
}

'use client'
function Profile({ user }: { user: User }) {
  return <div>{user.name}</div>  // 只使用 1 个字段
}
```

**正确：仅序列化 1 个字段**

```tsx
async function Page() {
  const user = await fetchUser()
  return <Profile name={user.name} />
}

'use client'
function Profile({ name }: { name: string }) {
  return <div>{name}</div>
}
```

### 3.6 通过组件组合实现并行数据获取

**影响：致命（CRITICAL）（消除服务端瀑布请求）**

React Server Components 在树中顺序执行。通过组件组合重构以并行化数据获取。

**不正确：Sidebar 等待 Page 的 fetch 完成**

```tsx
export default async function Page() {
  const header = await fetchHeader()
  return (
    <div>
      <div>{header}</div>
      <Sidebar />
    </div>
  )
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}
```

**正确：两者同时获取**

```tsx
async function Header() {
  const data = await fetchHeader()
  return <div>{data}</div>
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}

export default function Page() {
  return (
    <div>
      <Header />
      <Sidebar />
    </div>
  )
}
```

**使用 children prop 的替代方案：**

```tsx
async function Header() {
  const data = await fetchHeader()
  return <div>{data}</div>
}

async function Sidebar() {
  const items = await fetchSidebarItems()
  return <nav>{items.map(renderItem)}</nav>
}

function Layout({ children }: { children: ReactNode }) {
  return (
    <div>
      <Header />
      {children}
    </div>
  )
}

export default function Page() {
  return (
    <Layout>
      <Sidebar />
    </Layout>
  )
}
```

### 3.7 并行嵌套数据获取

**影响：致命（CRITICAL）（消除服务端瀑布请求）**

在并行获取嵌套数据时，在每个项目的 promise 中链式依赖获取，这样慢的项目不会阻塞其他项目。

**不正确：单个慢项目阻塞所有嵌套获取**

```tsx
const chats = await Promise.all(
  chatIds.map(id => getChat(id))
)

const chatAuthors = await Promise.all(
  chats.map(chat => getUser(chat.author))
)
```

如果 100 个中的一个 `getChat(id)` 非常慢，其他 99 个聊天的作者即使数据已就绪也无法开始加载。

**正确：每个项目链式自己的嵌套获取**

```tsx
const chatAuthors = await Promise.all(
  chatIds.map(id => getChat(id).then(chat => getUser(chat.author)))
)
```

每个项目独立链式 `getChat` → `getUser`，所以慢的聊天不会阻塞其他项目的作者获取。

### 3.8 使用 React.cache() 进行单请求去重

**影响：中（MEDIUM）（在请求内去重）**

使用 `React.cache()` 进行服务端请求去重。身份验证和数据库查询受益最大。

**用法：**

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({
    where: { id: session.user.id }
  })
})
```

在单个请求中，多次调用 `getCurrentUser()` 只执行一次查询。

**避免使用内联对象作为参数：**

`React.cache()` 使用浅相等（`Object.is`）来判断缓存命中。内联对象每次调用都会创建新的引用，阻止缓存命中。

**不正确：总是缓存未命中**

```typescript
const getUser = cache(async (params: { uid: number }) => {
  return await db.user.findUnique({ where: { id: params.uid } })
})

// 每次调用创建新对象，从未命中缓存
getUser({ uid: 1 })
getUser({ uid: 1 })  // 缓存未命中，再次执行查询
```

**正确：缓存命中**

```typescript
const params = { uid: 1 }
getUser(params)  // 查询执行
getUser(params)  // 缓存命中（相同引用）
```

如果必须传递对象，请传递相同的引用：

**Next.js 特别说明：**

在 Next.js 中，`fetch` API 自动扩展了请求记忆化。相同 URL 和选项的请求在单个请求内自动去重，所以你不需要为 `fetch` 调用使用 `React.cache()`。但是，`React.cache()` 对其他异步任务仍然至关重要：

- 数据库查询（Prisma、Drizzle 等）
- 重型计算
- 身份验证检查
- 文件系统操作
- 任何非 fetch 的异步工作

使用 `React.cache()` 在组件树中跨组件去重这些操作。

参考：[https://react.dev/reference/react/cache](https://react.dev/reference/react/cache)

### 3.9 使用 after() 进行非阻塞操作

**影响：中（MEDIUM）（更快的响应时间）**

使用 Next.js 的 `after()` 来安排在响应发送后执行的工作。这可以防止日志记录、分析和其他副作用阻塞响应。

**不正确：阻塞响应**

```tsx
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // 执行变更
  await updateDatabase(request)
  
  // 日志记录阻塞响应
  const userAgent = request.headers.get('user-agent') || 'unknown'
  await logUserAction({ userAgent })
  
  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  })
}
```

**正确：非阻塞**

```tsx
import { after } from 'next/server'
import { headers, cookies } from 'next/headers'
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // 执行变更
  await updateDatabase(request)
  
  // 响应发送后记录日志
  after(async () => {
    const userAgent = (await headers()).get('user-agent') || 'unknown'
    const sessionCookie = (await cookies()).get('session-id')?.value || 'anonymous'
    
    logUserAction({ sessionCookie, userAgent })
  })
  
  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  })
}
```

响应立即发送，而日志记录在后台进行。

**常见用例：**

- 分析追踪
- 审计日志
- 发送通知
- 缓存失效
- 清理任务

**重要说明：**

- `after()` 即使响应失败或重定向也会执行
- 适用于 Server Actions、路由处理程序和 Server Components

参考：[https://nextjs.org/docs/app/api-reference/functions/after](https://nextjs.org/docs/app/api-reference/functions/after)

---

## 4. 客户端数据获取

**影响：中高（MEDIUM-HIGH）**

自动去重和高效的数据获取模式可减少冗余网络请求。

### 4.1 去重全局事件监听器

**影响：低（LOW）（N 个组件共享一个监听器）**

使用 `useSWRSubscription()` 在组件实例之间共享全局事件监听器。

**不正确：N 个实例 = N 个监听器**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === key) {
        callback()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [key, callback])
}
```

多次使用 `useKeyboardShortcut` 钩子时，每个实例都会注册一个新的监听器。

**正确：N 个实例 = 1 个监听器**

```tsx
import useSWRSubscription from 'swr/subscription'

// 模块级 Map 用于追踪每个键的回调
const keyCallbacks = new Map<string, Set<() => void>>()

function useKeyboardShortcut(key: string, callback: () => void) {
  // 在 Map 中注册此回调
  useEffect(() => {
    if (!keyCallbacks.has(key)) {
      keyCallbacks.set(key, new Set())
    }
    keyCallbacks.get(key)!.add(callback)

    return () => {
      const set = keyCallbacks.get(key)
      if (set) {
        set.delete(callback)
        if (set.size === 0) {
          keyCallbacks.delete(key)
        }
      }
    }
  }, [key, callback])

  useSWRSubscription('global-keydown', () => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && keyCallbacks.has(e.key)) {
        keyCallbacks.get(e.key)!.forEach(cb => cb())
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  })
}

function Profile() {
  // 多个快捷键将共享同一个监听器
  useKeyboardShortcut('p', () => { /* ... */ }) 
  useKeyboardShortcut('k', () => { /* ... */ })
  // ...
}
```

### 4.2 使用被动事件监听器提升滚动性能

**影响：中（MEDIUM）（消除事件监听器导致的滚动延迟）**

为触摸和滚轮事件监听器添加 `{ passive: true }` 以实现即时滚动。浏览器通常会等待监听器执行完毕以检查是否调用了 `preventDefault()`，这会导致滚动延迟。

**不正确：**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  
  document.addEventListener('touchstart', handleTouch)
  document.addEventListener('wheel', handleWheel)
  
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**正确：**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  
  document.addEventListener('touchstart', handleTouch, { passive: true })
  document.addEventListener('wheel', handleWheel, { passive: true })
  
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**使用 passive 时：** 追踪/分析、日志记录、任何不调用 `preventDefault()` 的监听器。

**不要使用 passive 时：** 实现自定义滑动手势、自定义缩放控制或任何需要 `preventDefault()` 的监听器。

### 4.3 使用 SWR 进行自动去重

**影响：中高（MEDIUM-HIGH）（自动去重）**

SWR 在组件实例之间实现请求去重、缓存和重新验证。

**不正确：不去重，每个实例都获取**

```tsx
function UserList() {
  const [users, setUsers] = useState([])
  useEffect(() => {
    fetch('/api/users')
      .then(r => r.json())
      .then(setUsers)
  }, [])
}
```

**正确：多个实例共享一个请求**

```tsx
import useSWR from 'swr'

function UserList() {
  const { data: users } = useSWR('/api/users', fetcher)
}
```

**对于不可变数据：**

```tsx
import { useImmutableSWR } from '@/lib/swr'

function StaticContent() {
  const { data } = useImmutableSWR('/api/config', fetcher)
}
```

**对于变更操作：**

```tsx
import { useSWRMutation } from 'swr/mutation'

function UpdateButton() {
  const { trigger } = useSWRMutation('/api/user', updateUser)
  return <button onClick={() => trigger()}>更新</button>
}
```

参考：[https://swr.vercel.app](https://swr.vercel.app)

### 4.4 版本化和最小化 localStorage 数据

**影响：中（MEDIUM）（防止模式冲突，减少存储大小）**

为键添加版本前缀并仅存储需要的字段。防止模式冲突和敏感数据的意外存储。

**不正确：**

```typescript
// 无版本，存储所有内容，无错误处理
localStorage.setItem('userConfig', JSON.stringify(fullUserObject))
const data = localStorage.getItem('userConfig')
```

**正确：**

```typescript
const VERSION = 'v2'

function saveConfig(config: { theme: string; language: string }) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config))
  } catch {
    // 在隐身/私密浏览、配额超出或禁用时会抛出异常
  }
}

function loadConfig() {
  try {
    const data = localStorage.getItem(`userConfig:${VERSION}`)
    return data ? JSON.parse(data) : null
  } catch {
    return null
  }
}

// 从 v1 迁移到 v2
function migrate() {
  try {
    const v1 = localStorage.getItem('userConfig:v1')
    if (v1) {
      const old = JSON.parse(v1)
      saveConfig({ theme: old.darkMode ? 'dark' : 'light', language: old.lang })
      localStorage.removeItem('userConfig:v1')
    }
  } catch {}
}
```

**从服务端响应中存储最小字段：**

```typescript
// User 对象有 20+ 个字段，只存储 UI 需要的
function cachePrefs(user: FullUser) {
  try {
    localStorage.setItem('prefs:v1', JSON.stringify({
      theme: user.preferences.theme,
      notifications: user.preferences.notifications
    }))
  } catch {}
}
```

**始终包裹在 try-catch 中：** `getItem()` 和 `setItem()` 在隐身/私密浏览（Safari、Firefox）、配额超出或禁用时会抛出异常。

**好处：** 通过版本化实现模式演进、减少存储大小、防止存储令牌/PII/内部标志。

---

## 5. 重渲染优化

**影响：中（MEDIUM）**

减少不必要的重渲染可以最小化浪费的计算并改善 UI 响应性。

### 5.1 在渲染期间计算派生状态

**影响：中（MEDIUM）（避免冗余渲染和状态漂移）**

如果一个值可以从当前的 props/state 计算得出，不要将其存储在 state 中或在 effect 中更新它。在渲染期间派生它以避免额外的渲染和状态漂移。不要仅仅为了响应 prop 变化而在 effect 中设置状态；优先使用派生值或键控重置。

**不正确：冗余的状态和 effect**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const [fullName, setFullName] = useState('')

  useEffect(() => {
    setFullName(firstName + ' ' + lastName)
  }, [firstName, lastName])

  return <p>{fullName}</p>
}
```

**正确：在渲染期间派生**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const fullName = firstName + ' ' + lastName

  return <p>{fullName}</p>
}
```

参考：[https://react.dev/learn/you-might-not-need-an-effect](https://react.dev/learn/you-might-not-need-an-effect)

### 5.2 将状态读取延迟到使用点

**影响：中（MEDIUM）（避免不必要的订阅）**

如果只在回调中读取动态状态（searchParams、localStorage），不要订阅它。

**不正确：订阅所有 searchParams 更改**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams()

  const handleShare = () => {
    const ref = searchParams.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>分享</button>
}
```

**正确：按需读取，无订阅**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search)
    const ref = params.get('ref')
    shareChat(chatId, { ref })
  }

  return <button onClick={handleShare}>分享</button>
}
```

### 5.3 不要将具有原始结果类型的简单表达式包裹在 useMemo 中

**影响：低中（LOW-MEDIUM）（每次渲染浪费计算）**

当表达式很简单（几个逻辑或算术运算符）并且结果类型是原始类型（boolean、number、string）时，不要将其包裹在 `useMemo` 中。调用 `useMemo` 和比较钩子依赖可能比表达式本身消耗更多的资源。

**不正确：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading
  }, [user.isLoading, notifications.isLoading])

  if (isLoading) return <Skeleton />
  // 渲染一些标记
}
```

**正确：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading

  if (isLoading) return <Skeleton />
  // 渲染一些标记
}
```

### 5.4 不要在组件内部定义组件

**影响：高（HIGH）（防止每次渲染都重新挂载）**

在另一个组件内部定义组件会在每次渲染时创建一个新的组件类型。React 每次都会看到一个不同的组件并完全重新挂载它，销毁所有状态和 DOM。

开发者这样做的一个常见原因是为了在不传递 props 的情况下访问父组件变量。始终改为传递 props。

**不正确：每次渲染都重新挂载**

```tsx
function UserProfile({ user, theme }) {
  // 在内部定义以访问 `theme` - 不良做法
  const Avatar = () => (
    <img
      src={user.avatarUrl}
      className={theme === 'dark' ? 'avatar-dark' : 'avatar-light'}
    />
  )

  // 在内部定义以访问 `user` - 不良做法
  const Stats = () => (
    <div>
      <span>{user.followers} 关注者</span>
      <span>{user.posts} 帖子</span>
    </div>
  )

  return (
    <div>
      <Avatar />
      <Stats />
    </div>
  )
}
```

每次 `UserProfile` 渲染时，`Avatar` 和 `Stats` 都是新的组件类型。React 卸载旧实例并挂载新实例，丢失任何内部状态、重新运行 effects 并重建 DOM 节点。

**正确：改为传递 props**

```tsx
function Avatar({ src, theme }: { src: string; theme: string }) {
  return (
    <img
      src={src}
      className={theme === 'dark' ? 'avatar-dark' : 'avatar-light'}
    />
  )
}

function Stats({ followers, posts }: { followers: number; posts: number }) {
  return (
    <div>
      <span>{followers} 关注者</span>
      <span>{posts} 帖子</span>
    </div>
  )
}

function UserProfile({ user, theme }) {
  return (
    <div>
      <Avatar src={user.avatarUrl} theme={theme} />
      <Stats followers={user.followers} posts={user.posts} />
    </div>
  )
}
```

**此错误的症状：**

- 输入框每次按键都失去焦点
- 动画意外重新开始
- `useEffect` 清理/设置在每次父渲染时执行
- 组件内的滚动位置重置

### 5.5 将 Memo 化组件的默认非原始参数值提取为常量

**影响：中（MEDIUM）（通过使用常量作为默认值恢复 memo 化）**

当 memo 化组件对某些非原始可选参数（如数组、函数或对象）具有默认值时，不带该参数调用组件会导致 memo 化失效。这是因为每次重渲染都会创建新的值实例，它们无法通过 `memo()` 中的严格相等比较。

为了解决这个问题，将默认值提取为常量。

**不正确：`onClick` 在每次重渲染时都不同**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// 不带可选的 onClick 使用
<UserAvatar />
```

**正确：稳定的默认值**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// 不带可选的 onClick 使用
<UserAvatar />
```

### 5.6 提取到 Memo 化组件中

**影响：中（MEDIUM）（启用提前返回）**

将昂贵的工作提取到 memo 化组件中，以便在计算之前提前返回。

**不正确：即使在加载时也计算头像**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user)
    return <Avatar id={id} />
  }, [user])

  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}
```

**正确：加载时跳过计算**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  )
}
```

**注意：** 如果你的项目启用了 [React Compiler](https://react.dev/learn/react-compiler)，则不需要手动使用 `memo()` 和 `useMemo()` 进行 memo 化。编译器会自动优化重渲染。

### 5.7 缩小 Effect 依赖范围

**影响：低（LOW）（最小化 effect 重复执行）**

指定原始类型依赖而非对象，以最小化 effect 的重复执行。

**不正确：任何用户字段更改都重新执行**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**正确：仅在 id 更改时重新执行**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**对于派生状态，在 effect 外部计算：**

```tsx
// 不正确：在 width=767, 766, 765... 时都执行
useEffect(() => {
  if (width < 768) {
    enableMobileMode()
  }
}, [width])

// 正确：仅在布尔值转换时执行
const isMobile = width < 768
useEffect(() => {
  if (isMobile) {
    enableMobileMode()
  }
}, [isMobile])
```

### 5.8 将交互逻辑放入事件处理程序

**影响：中（MEDIUM）（避免 effect 重复执行和重复副作用）**

如果副作用是由特定的用户操作（提交、点击、拖拽）触发的，在事件处理程序中执行它。不要将操作建模为状态 + effect；这会使 effects 在无关更改时重新执行，并且可能重复操作。

**不正确：事件被建模为状态 + effect**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false)
  const theme = useContext(ThemeContext)

  useEffect(() => {
    if (submitted) {
      post('/api/register')
      showToast('Registered', theme)
    }
  }, [submitted, theme])

  return <button onClick={() => setSubmitted(true)}>提交</button>
}
```

**正确：在 handler 中执行**

```tsx
function Form() {
  const theme = useContext(ThemeContext)

  function handleSubmit() {
    post('/api/register')
    showToast('Registered', theme)
  }

  return <button onClick={handleSubmit}>提交</button>
}
```

参考：[https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)

### 5.9 拆分组合的 Hook 计算

**影响：中（MEDIUM）（避免重新计算独立步骤）**

当一个 hook 包含多个具有不同依赖的独立任务时，将它们拆分为单独的 hooks。组合的 hook 在任何依赖发生变化时都会重新运行所有任务，即使某些任务不使用变化的值。

**不正确：更改 `sortOrder` 重新计算过滤**

```tsx
const sortedProducts = useMemo(() => {
  const filtered = products.filter((p) => p.category === category)
  const sorted = filtered.toSorted((a, b) =>
    sortOrder === "asc" ? a.price - b.price : b.price - a.price
  )
  return sorted
}, [products, category, sortOrder])
```

**正确：仅在 products 或 category 变化时重新计算过滤**

```tsx
const filteredProducts = useMemo(
  () => products.filter((p) => p.category === category),
  [products, category]
)

const sortedProducts = useMemo(
  () =>
    filteredProducts.toSorted((a, b) =>
      sortOrder === "asc" ? a.price - b.price : b.price - a.price
    ),
  [filteredProducts, sortOrder]
)
```

此模式也适用于组合不相关副作用时的 `useEffect`：

**不正确：任一依赖变化时两个 effect 都执行**

```tsx
useEffect(() => {
  analytics.trackPageView(pathname)
  document.title = `${pageTitle} | My App`
}, [pathname, pageTitle])
```

**正确：effects 独立执行**

```tsx
useEffect(() => {
  analytics.trackPageView(pathname)
}, [pathname])

useEffect(() => {
  document.title = `${pageTitle} | My App`
}, [pageTitle])
```

**注意：** 如果你的项目启用了 [React Compiler](https://react.dev/learn/react-compiler)，它会自动优化依赖追踪，可能会为你处理部分情况。

### 5.10 订阅派生状态

**影响：中（MEDIUM）（减少重渲染频率）**

订阅派生后的布尔状态而非连续值，以减少重渲染频率。

**不正确：每次像素变化都重渲染**

```tsx
function Sidebar() {
  const width = useWindowWidth()  // 持续更新
  const isMobile = width < 768
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

**正确：仅在布尔值变化时重渲染**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)')
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

### 5.11 使用函数式 setState 更新

**影响：中（MEDIUM）（防止过期闭包和不必要的回调重建）**

当基于当前状态值更新状态时，使用 setState 的函数式更新形式，而不是直接引用状态变量。这可以防止过期闭包、消除不必要的依赖并创建稳定的回调引用。

**不正确：需要将状态作为依赖**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // 回调必须依赖 items，每次 items 变化都重建
  const addItems = useCallback((newItems: Item[]) => {
    setItems([...items, ...newItems])
  }, [items])  // ❌ items 依赖导致重建
  
  // 如果忘记依赖，存在过期闭包风险
  const removeItem = useCallback((id: string) => {
    setItems(items.filter(item => item.id !== id))
  }, [])  // ❌ 缺少 items 依赖 - 将使用过期的 items!
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

第一个回调在每次 `items` 变化时重建，可能导致子组件不必要的重渲染。第二个回调存在过期闭包错误——它将始终引用初始的 `items` 值。

**正确：稳定回调，无过期闭包**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // 稳定回调，永远不会被重建
  const addItems = useCallback((newItems: Item[]) => {
    setItems(curr => [...curr, ...newItems])
  }, [])  // ✅ 不需要依赖
  
  // 始终使用最新状态，无过期闭包风险
  const removeItem = useCallback((id: string) => {
    setItems(curr => curr.filter(item => item.id !== id))
  }, [])  // ✅ 安全且稳定
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

**好处：**

1. **稳定的回调引用** - 状态变化时不需要重建回调
2. **无过期闭包** - 始终操作最新的状态值
3. **更少的依赖** - 简化依赖数组，减少内存泄漏
4. **防止错误** - 消除 React 闭包错误的最常见来源

**何时使用函数式更新：**

- 任何依赖当前状态值的 setState
- 在需要状态的 useCallback/useMemo 内部
- 引用状态的事件处理程序
- 更新状态的异步操作

**何时可以直接更新：**

- 设置状态为静态值：`setCount(0)`
- 仅从 props/参数设置状态：`setName(newName)`
- 状态不依赖于前一个值

**注意：** 如果你的项目启用了 [React Compiler](https://react.dev/learn/react-compiler)，编译器可以自动优化某些情况，但为了正确性和防止过期闭包错误，仍然推荐使用函数式更新。

### 5.12 使用惰性状态初始化

**影响：中（MEDIUM）（每次渲染浪费计算）**

对昂贵的初始值传递一个函数给 `useState`。如果不使用函数形式，初始化器会在每次渲染时执行，即使该值只使用一次。

**不正确：每次渲染都执行**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() 在每次渲染时都执行，即使在初始化之后
  const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items))
  const [query, setQuery] = useState('')
  
  // 当 query 变化时，buildSearchIndex 不必要地再次执行
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse 每次渲染都执行
  const [settings, setSettings] = useState(
    JSON.parse(localStorage.getItem('settings') || '{}')
  )
  
  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

**正确：仅执行一次**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() 仅在初始渲染时执行
  const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items))
  const [query, setQuery] = useState('')
  
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse 仅在初始渲染时执行
  const [settings, setSettings] = useState(() => {
    const stored = localStorage.getItem('settings')
    return stored ? JSON.parse(stored) : {}
  })
  
  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

当从 localStorage/sessionStorage 计算初始值、构建数据结构（索引、映射）、从 DOM 读取或执行重型转换时，使用惰性初始化。

对于简单的原始类型（`useState(0)`）、直接引用（`useState(props.value)`）或廉价字面量（`useState({})`），不需要函数形式。

### 5.13 对非紧急更新使用 Transition

**影响：中（MEDIUM）（保持 UI 响应性）**

将频繁、非紧急的状态更新标记为 transition，以保持 UI 响应性。

**不正确：每次滚动都阻塞 UI**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

**正确：非阻塞更新**

```tsx
import { startTransition } from 'react'

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY))
    }
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

### 5.14 对昂贵的派生渲染使用 useDeferredValue

**影响：中（MEDIUM）（在重型计算期间保持输入响应）**

当用户输入触发昂贵的计算或渲染时，使用 `useDeferredValue` 来保持输入响应。延迟的值会滞后，使 React 能够优先处理输入更新，并在空闲时渲染昂贵的结果。

**不正确：过滤时输入感觉卡顿**

```tsx
function Search({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const filtered = items.filter(item => fuzzyMatch(item, query))

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <ResultsList results={filtered} />
    </>
  )
}
```

**正确：输入保持灵敏，结果就绪时渲染**

```tsx
function Search({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const deferredQuery = useDeferredValue(query)
  const filtered = useMemo(
    () => items.filter(item => fuzzyMatch(item, deferredQuery)),
    [items, deferredQuery]
  )
  const isStale = query !== deferredQuery

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <div style={{ opacity: isStale ? 0.7 : 1 }}>
        <ResultsList results={filtered} />
      </div>
    </>
  )
}
```

**何时使用：**

- 过滤/搜索大型列表
- 响应输入的昂贵可视化（图表、图形）
- 任何导致明显渲染延迟的派生状态

**注意：** 将昂贵的计算包裹在 `useMemo` 中，并将延迟的值作为依赖，否则它仍然在每次渲染时执行。

参考：[https://react.dev/reference/react/useDeferredValue](https://react.dev/reference/react/useDeferredValue)

### 5.15 对瞬态值使用 useRef

**影响：中（MEDIUM）（避免频繁更新时的不必要重渲染）**

当一个值频繁变化且你不希望每次更新都重渲染时（例如鼠标跟踪器、定时器、瞬时标志），将其存储在 `useRef` 中而不是 `useState`。将组件状态留给 UI；对临时的 DOM 相关值使用 refs。更新 ref 不会触发重渲染。

**不正确：每次更新都渲染**

```tsx
function Tracker() {
  const [lastX, setLastX] = useState(0)

  useEffect(() => {
    const onMove = (e: MouseEvent) => setLastX(e.clientX)
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: lastX,
        width: 8,
        height: 8,
        background: 'black',
      }}
    />
  )
}
```

**正确：追踪时不重渲染**

```tsx
function Tracker() {
  const lastXRef = useRef(0)
  const dotRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      lastXRef.current = e.clientX
      const node = dotRef.current
      if (node) {
        node.style.transform = `translateX(${e.clientX}px)`
      }
    }
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      ref={dotRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: 8,
        height: 8,
        background: 'black',
        transform: 'translateX(0px)',
      }}
    />
  )
}
```

---

## 6. 渲染性能

**影响：中（MEDIUM）**

优化渲染过程可以减少浏览器需要执行的工作。

### 6.1 为 SVG 包装器添加动画，而非 SVG 元素本身

**影响：低（LOW）（启用硬件加速）**

许多浏览器对 SVG 元素上的 CSS3 动画没有硬件加速。将 SVG 包裹在 `<div>` 中并为包装器添加动画。

**不正确：直接为 SVG 添加动画 - 无硬件加速**

```tsx
function LoadingSpinner() {
  return (
    <svg 
      className="animate-spin"
      width="24" 
      height="24" 
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  )
}
```

**正确：为包装器 div 添加动画 - 硬件加速**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg 
        width="24" 
        height="24" 
        viewBox="0 0 24 24"
      >
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  )
}
```

这适用于所有 CSS 变换和过渡（`transform`、`opacity`、`translate`、`scale`、`rotate`）。包装器 div 允许浏览器使用 GPU 加速以获得更流畅的动画。

### 6.2 对长列表使用 CSS content-visibility

**影响：高（HIGH）（更快的初始渲染）**

应用 `content-visibility: auto` 以延迟屏幕外内容的渲染。

**CSS：**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**示例：**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  )
}
```

对于 1000 条消息，浏览器跳过约 990 条屏幕外项目的布局/绘制（初始渲染速度提升 10 倍）。

### 6.3 提升静态 JSX 元素

**影响：低（LOW）（避免重复创建）**

将静态 JSX 提取到组件外部以避免重复创建。

**不正确：每次渲染都重新创建元素**

```tsx
function LoadingSkeleton() {
  return <div className="animate-pulse h-20 bg-gray-200" />
}

function Container() {
  return (
    <div>
      {loading && <LoadingSkeleton />}
    </div>
  )
}
```

**正确：重用相同元素**

```tsx
const loadingSkeleton = (
  <div className="animate-pulse h-20 bg-gray-200" />
)

function Container() {
  return (
    <div>
      {loading && loadingSkeleton}
    </div>
  )
}
```

这对于大型和静态 SVG 节点特别有帮助，它们在每次渲染时重新创建的成本很高。

**注意：** 如果你的项目启用了 [React Compiler](https://react.dev/learn/react-compiler)，编译器会自动提升静态 JSX 元素并优化组件重渲染，使手动提升变得不必要。

### 6.4 优化 SVG 精度

**影响：低（LOW）（减少文件大小）**

降低 SVG 坐标精度以减少文件大小。最佳精度取决于 viewBox 大小，但通常应考虑降低精度。

**不正确：精度过高**

```svg
<path d="M 10.293847 20.847362 L 30.938472 40.192837" />
```

**正确：1 位小数**

```svg
<path d="M 10.3 20.8 L 30.9 40.2" />
```

**使用 SVGO 自动化：**

```bash
npx svgo --precision=1 --multipass icon.svg
```

### 6.5 防止注水不匹配且不闪屏

**影响：中（MEDIUM）（避免视觉闪烁和注水错误）**

当渲染依赖于客户端存储（localStorage、cookies）的内容时，通过注入一个在 React 注水前同步更新 DOM 的脚本来避免 SSR 破坏和注水后闪烁。

**不正确：破坏 SSR**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  // localStorage 在服务端不可用 - 抛出错误
  const theme = localStorage.getItem('theme') || 'light'
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

服务端渲染会失败，因为 `localStorage` 未定义。

**不正确：视觉闪烁**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState('light')
  
  useEffect(() => {
    // 在注水后执行 - 导致可见闪烁
    const stored = localStorage.getItem('theme')
    if (stored) {
      setTheme(stored)
    }
  }, [])
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

组件首先使用默认值（`light`）渲染，然后在注水后更新，导致错误内容的可见闪烁。

**正确：无闪烁，无注水不匹配**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-wrapper">
        {children}
      </div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                var el = document.getElementById('theme-wrapper');
                if (el) el.className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  )
}
```

内联脚本在显示元素之前同步执行，确保 DOM 已经具有正确的值。无闪烁，无注水不匹配。

这种模式对于主题切换、用户偏好、身份验证状态和任何应立即渲染而不闪烁默认值的仅客户端数据特别有用。

### 6.6 抑制预期的注水不匹配

**影响：低中（LOW-MEDIUM）（避免已知差异导致的大量注水警告）**

在 SSR 框架（例如 Next.js）中，某些值在服务端和客户端上故意不同（随机 ID、日期、区域设置/时区格式化）。对于这些*预期*的不匹配，将动态文本包裹在带有 `suppressHydrationWarning` 的元素中，以防止大量警告。不要用此来隐藏真正的错误。不要过度使用。

**不正确：已知不匹配的警告**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>
}
```

**正确：仅抑制预期的不匹配**

```tsx
function Timestamp() {
  return (
    <span suppressHydrationWarning>
      {new Date().toLocaleString()}
    </span>
  )
}
```

### 6.7 使用 Activity 组件进行显示/隐藏

**影响：中（MEDIUM）（保留状态/DOM）**

使用 React 的 `<Activity>` 来为频繁切换可见性的昂贵组件保留状态/DOM。

**用法：**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

避免昂贵的重渲染和状态丢失。

### 6.8 在 Script 标签上使用 defer 或 async

**影响：高（HIGH）（消除渲染阻塞）**

没有 `defer` 或 `async` 的脚本标签在下载和执行时会阻止 HTML 解析。这会延迟首次内容绘制和可交互时间。

- **`defer`**：并行下载，在 HTML 解析完成后执行，保持执行顺序
- **`async`**：并行下载，就绪后立即执行，不保证执行顺序

对依赖于 DOM 或其他脚本的脚本使用 `defer`。对独立脚本（如分析脚本）使用 `async`。

**不正确：阻塞渲染**

```tsx
export default function Document() {
  return (
    <html>
      <head>
        <script src="https://example.com/analytics.js" />
        <script src="/scripts/utils.js" />
      </head>
      <body>{/* content */}</body>
    </html>
  )
}
```

**正确：非阻塞**

```tsx
import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script src="https://example.com/analytics.js" strategy="afterInteractive" />
      <Script src="/scripts/utils.js" strategy="beforeInteractive" />
    </>
  )
}
```

**注意：** 在 Next.js 中，优先使用 `next/script` 组件配合 `strategy` 属性，而不是原生 script 标签：

参考：[https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#defer](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#defer)

### 6.9 使用显式条件渲染

**影响：低（LOW）（防止渲染 0 或 NaN）**

当条件可能为 `0`、`NaN` 或其他会渲染的假值时，使用显式的三元运算符（`? :`）而不是 `&&` 进行条件渲染。

**不正确：当 count 为 0 时渲染 "0"**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  )
}

// 当 count = 0 时，渲染：<div>0</div>
// 当 count = 5 时，渲染：<div><span class="badge">5</span></div>
```

**正确：当 count 为 0 时渲染为空**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  )
}

// 当 count = 0 时，渲染：<div></div>
// 当 count = 5 时，渲染：<div><span class="badge">5</span></div>
```

### 6.10 使用 React DOM 资源提示

**影响：高（HIGH）（减少关键资源的加载时间）**

React DOM 提供了向浏览器提示其将需要的资源的 API。这些在服务端组件中特别有用，可以在客户端甚至收到 HTML 之前就开始加载资源。

- **`prefetchDNS(href)`**：为你期望连接的域名解析 DNS
- **`preconnect(href)`**：建立到服务器的连接（DNS + TCP + TLS）
- **`preload(href, options)`**：获取你即将使用的资源（样式表、字体、脚本、图片）
- **`preloadModule(href)`**：获取你即将使用的 ES 模块
- **`preinit(href, options)`**：获取并评估样式表或脚本
- **`preinitModule(href)`**：获取并评估 ES 模块

**示例：预连接到第三方 API**

```tsx
import { preconnect, prefetchDNS } from 'react-dom'

export default function App() {
  prefetchDNS('https://analytics.example.com')
  preconnect('https://api.example.com')

  return <main>{/* 内容 */}</main>
}
```

**示例：预加载关键字体和样式**

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

**示例：为代码分割路由预加载模块**

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

**何时使用每个 API：**

| API | 用例 |
|-----|----------|
| `prefetchDNS` | 稍后将要连接的第三方域名 |
| `preconnect` | 即将获取的 API 或 CDN |
| `preload` | 当前页面所需的关键资源 |
| `preloadModule` | 可能的下一个导航的 JS 模块 |
| `preinit` | 必须尽早执行的样式表/脚本 |
| `preinitModule` | 必须尽早执行的 ES 模块 |

参考：[https://react.dev/reference/react-dom#resource-preloading-apis](https://react.dev/reference/react-dom#resource-preloading-apis)

### 6.11 优先使用 useTransition 而非手动加载状态

**影响：低（LOW）（减少重渲染并提高代码清晰度）**

使用 `useTransition` 而不是手动的 `useState` 来处理加载状态。它提供内置的 `isPending` 状态并自动管理过渡。

**不正确：手动加载状态**

```tsx
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async (value: string) => {
    setIsLoading(true)
    setQuery(value)
    const data = await fetchResults(value)
    setResults(data)
    setIsLoading(false)
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isLoading && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**正确：带内置待定状态的 useTransition**

```tsx
import { useTransition, useState } from 'react'

function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  const handleSearch = (value: string) => {
    setQuery(value) // 立即更新输入
    
    startTransition(async () => {
      // 获取并更新结果
      const data = await fetchResults(value)
      setResults(data)
    })
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**好处：**

- **自动待定状态**：无需手动管理 `setIsLoading(true/false)`
- **错误恢复能力**：即使 transition 抛出异常，待定状态也能正确重置
- **更好的响应性**：在更新期间保持 UI 响应
- **中断处理**：新的 transition 自动取消待定的

参考：[https://react.dev/reference/react/useTransition](https://react.dev/reference/react/useTransition)

---

## 7. JavaScript 性能

**影响：低中（LOW-MEDIUM）**

热路径的微优化累积起来可以带来有意义的改进。

### 7.1 避免布局颠簸

**影响：中（MEDIUM）（防止强制同步布局并减少性能瓶颈）**

避免在样式写入和布局读取之间交替。当你在样式更改之间读取布局属性（如 `offsetWidth`、`getBoundingClientRect()` 或 `getComputedStyle()`）时，浏览器被迫触发同步回流。

**这是可以的：浏览器批处理样式更改**

```typescript
function updateElementStyles(element: HTMLElement) {
  // 每行都使样式失效，但浏览器会批处理重新计算
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
}
```

**不正确：交替读写强制回流**

```typescript
function layoutThrashing(element: HTMLElement) {
  element.style.width = '100px'
  const width = element.offsetWidth  // 强制回流
  element.style.height = '200px'
  const height = element.offsetHeight  // 再次强制回流
}
```

**正确：批处理写入，然后一次读取**

```typescript
function updateElementStyles(element: HTMLElement) {
  // 将所有写入批处理在一起
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
  
  // 在所有写入完成后读取（单次回流）
  const { width, height } = element.getBoundingClientRect()
}
```

**正确：批处理读取，然后写入**

```typescript
function updateElementStyles(element: HTMLElement) {
  element.classList.add('highlighted-box')
  
  const { width, height } = element.getBoundingClientRect()
}
```

**更好的做法：使用 CSS 类**

**React 示例：**

```tsx
// 不正确：在样式更改和布局查询之间交替
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  const ref = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (ref.current && isHighlighted) {
      ref.current.style.width = '100px'
      const width = ref.current.offsetWidth // 强制布局
      ref.current.style.height = '200px'
    }
  }, [isHighlighted])
  
  return <div ref={ref}>Content</div>
}

// 正确：切换类
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  return (
    <div className={isHighlighted ? 'highlighted-box' : ''}>
      Content
    </div>
  )
}
```

尽可能优先使用 CSS 类而非内联样式。CSS 文件由浏览器缓存，类提供了更好的关注点分离且更易于维护。

有关强制布局操作的更多信息，请参阅[此 gist](https://gist.github.com/paulirish/5d52fb081b3570c81e3a) 和 [CSS Triggers](https://csstriggers.com/)。

### 7.2 为重复查找构建索引映射

**影响：低中（LOW-MEDIUM）（从 100 万次操作降到 2000 次）**

多次使用相同键进行 `.find()` 调用应使用 Map。

**不正确（每次查找 O(n)）：**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId)
  }))
}
```

**正确（每次查找 O(1)）：**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map(u => [u.id, u]))

  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId)
  }))
}
```

构建一次映射（O(n)），然后所有查找都是 O(1)。1000 个订单 × 1000 个用户：100 万次操作 → 2000 次操作。

### 7.3 在循环中缓存属性访问

**影响：低中（LOW-MEDIUM）（减少查找次数）**

在热路径中缓存对象属性查找。

**不正确（3 次查找 × N 次迭代）：**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}
```

**正确（总共 1 次查找）：**

```typescript
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) {
  process(value)
}
```

### 7.4 缓存重复函数调用

**影响：中（MEDIUM）（避免冗余计算）**

当同一个函数在渲染期间使用相同的输入被重复调用时，使用模块级 Map 来缓存函数结果。

**不正确（冗余计算）：**

```typescript
function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // slugify() 对相同的项目名称被调用了 100+ 次
        const slug = slugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**正确（缓存结果）：**

```typescript
// 模块级缓存
const slugifyCache = new Map<string, string>()

function cachedSlugify(text: string): string {
  if (slugifyCache.has(text)) {
    return slugifyCache.get(text)!
  }
  const result = slugify(text)
  slugifyCache.set(text, result)
  return result
}

function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // 每个唯一项目名称只计算一次
        const slug = cachedSlugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**单值函数的更简单模式：**

```typescript
let isLoggedInCache: boolean | null = null

function isLoggedIn(): boolean {
  if (isLoggedInCache !== null) {
    return isLoggedInCache
  }
  
  isLoggedInCache = document.cookie.includes('auth=')
  return isLoggedInCache
}

// 在身份验证变化时清除缓存
function onAuthChange() {
  isLoggedInCache = null
}
```

使用 Map（而非 hook），这样它可以在任何地方工作：工具函数、事件处理程序，不仅仅是在 React 组件中。

参考：[https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)

### 7.5 缓存 Storage API 调用

**影响：低中（LOW-MEDIUM）（减少昂贵的 I/O 操作）**

`localStorage`、`sessionStorage` 和 `document.cookie` 是同步且昂贵的。在内存中缓存读取。

**不正确（每次调用都读取存储）：**

```typescript
function getTheme() {
  return localStorage.getItem('theme') ?? 'light'
}
// 调用 10 次 = 10 次存储读取
```

**正确（Map 缓存）：**

```typescript
const storageCache = new Map<string, string | null>()

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key))
  }
  return storageCache.get(key)
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value)
  storageCache.set(key, value)  // 保持缓存同步
}
```

使用 Map（而非 hook），这样它可以在任何地方工作：工具函数、事件处理程序，不仅仅是在 React 组件中。

**Cookie 缓存：**

```typescript
let cookieCache: Record<string, string> | null = null

function getCookie(name: string) {
  if (!cookieCache) {
    cookieCache = Object.fromEntries(
      document.cookie.split('; ').map(c => c.split('='))
    )
  }
  return cookieCache[name]
}
```

**重要（在外部更改时使缓存失效）：**

如果存储可以在外部更改（另一个标签页、服务端设置的 cookie），使缓存失效：

```typescript
window.addEventListener('storage', (e) => {
  if (e.key) storageCache.delete(e.key)
})

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    storageCache.clear()
  }
})
```

### 7.6 合并多个数组迭代

**影响：低中（LOW-MEDIUM）（减少迭代次数）**

多个 `.filter()` 或 `.map()` 调用会多次迭代数组。合并为一个循环。

**不正确（3 次迭代）：**

```typescript
const admins = users.filter(u => u.isAdmin)
const testers = users.filter(u => u.isTester)
const inactive = users.filter(u => !u.isActive)
```

**正确（1 次迭代）：**

```typescript
const admins: User[] = []
const testers: User[] = []
const inactive: User[] = []

for (const user of users) {
  if (user.isAdmin) admins.push(user)
  if (user.isTester) testers.push(user)
  if (!user.isActive) inactive.push(user)
}
```

### 7.7 使用 requestIdleCallback 延迟非关键工作

**影响：中（MEDIUM）（在后台任务期间保持 UI 响应）**

使用 `requestIdleCallback()` 在浏览器空闲期间安排非关键工作。这使主线程有空处理用户交互和动画，减少卡顿并改善感知性能。

**不正确（在用户交互期间阻塞主线程）：**

```typescript
function handleSearch(query: string) {
  const results = searchItems(query)
  setResults(results)

  // 这些立即阻塞主线程
  analytics.track('search', { query })
  saveToRecentSearches(query)
  prefetchTopResults(results.slice(0, 3))
}
```

**正确（将非关键工作延迟到空闲时间）：**

```typescript
function handleSearch(query: string) {
  const results = searchItems(query)
  setResults(results)

  // 将非关键工作延迟到空闲时段
  requestIdleCallback(() => {
    analytics.track('search', { query })
  })

  requestIdleCallback(() => {
    saveToRecentSearches(query)
  })

  requestIdleCallback(() => {
    prefetchTopResults(results.slice(0, 3))
  })
}
```

**带超时以确保工作执行：**

```typescript
// 确保分析在 2 秒内触发，即使浏览器保持忙碌
requestIdleCallback(
  () => analytics.track('page_view', { path: location.pathname }),
  { timeout: 2000 }
)
```

**拆分大型任务：**

```typescript
function processLargeDataset(items: Item[]) {
  let index = 0

  function processChunk(deadline: IdleDeadline) {
    // 在有空闲时间时处理项目（目标 <50ms 每块）
    while (index < items.length && deadline.timeRemaining() > 0) {
      processItem(items[index])
      index++
    }

    // 如果还有剩余项目，安排下一块
    if (index < items.length) {
      requestIdleCallback(processChunk)
    }
  }

  requestIdleCallback(processChunk)
}
```

**不支持的浏览器的回退：**

```typescript
const scheduleIdleWork = window.requestIdleCallback ?? ((cb: () => void) => setTimeout(cb, 1))

scheduleIdleWork(() => {
  // 非关键工作
})
```

**何时使用：**

- 分析和遥测
- 将状态保存到 localStorage/IndexedDB
- 预取下一步可能用到的资源
- 处理非紧急的数据转换
- 非关键功能的惰性初始化

**何时不使用：**

- 需要即时反馈的用户发起操作
- 用户正在等待的渲染更新
- 时间敏感的操作

### 7.8 数组比较前先检查长度

**影响：中高（MEDIUM-HIGH）（长度不同时避免昂贵操作）**

在使用昂贵操作（排序、深度相等、序列化）比较数组时，先检查长度。如果长度不同，数组不可能相等。

在实际应用中，当比较在热路径（事件处理程序、渲染循环）中运行时，这种优化特别有价值。

**不正确（总是执行昂贵比较）：**

```typescript
function hasChanges(current: string[], original: string[]) {
  // 即使长度不同也总是排序和拼接
  return current.sort().join() !== original.sort().join()
}
```

即使在 `current.length` 为 5 而 `original.length` 为 100 时，也会执行两次 O(n log n) 排序。还有拼接数组和比较字符串的开销。

**正确（先进行 O(1) 长度检查）：**

```typescript
function hasChanges(current: string[], original: string[]) {
  // 如果长度不同，提前返回
  if (current.length !== original.length) {
    return true
  }
  // 仅在长度匹配时排序
  const currentSorted = current.toSorted()
  const originalSorted = original.toSorted()
  for (let i = 0; i < currentSorted.length; i++) {
    if (currentSorted[i] !== originalSorted[i]) {
      return true
    }
  }
  return false
}
```

这种新方法更高效，因为：
- 长度不同时避免了排序和拼接数组的开销
- 避免了为拼接后的字符串消耗内存（对大数组尤其重要）
- 避免了改变原始数组
- 发现差异时提前返回

### 7.9 从函数中提前返回

**影响：低中（LOW-MEDIUM）（避免不必要的计算）**

当结果已确定时提前返回，以跳过不必要的处理。

**不正确（即使在找到答案后仍处理所有项目）：**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  let errorMessage = ''
  
  for (const user of users) {
    if (!user.email) {
      hasError = true
      errorMessage = '邮箱必填'
    }
    if (!user.name) {
      hasError = true
      errorMessage = '姓名必填'
    }
    // 即使在发现错误后仍继续检查所有用户
  }
  
  return hasError ? { valid: false, error: errorMessage } : { valid: true }
}
```

**正确（在第一个错误时立即返回）：**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) {
      return { valid: false, error: '邮箱必填' }
    }
    if (!user.name) {
      return { valid: false, error: '姓名必填' }
    }
  }

  return { valid: true }
}
```

### 7.10 提升 RegExp 创建

**影响：低中（LOW-MEDIUM）（避免重复创建）**

不要在渲染中创建 RegExp。提升到模块作用域或使用 `useMemo()` 进行 memo 化。

**不正确（每次渲染都创建新的 RegExp）：**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, 'gi')
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**正确（memo 化或提升）：**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query]
  )
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**警告：全局正则表达式有可变状态**

全局正则表达式（`/g`）具有可变的 `lastIndex` 状态：

```typescript
const regex = /foo/g
regex.test('foo')  // true, lastIndex = 3
regex.test('foo')  // false, lastIndex = 0
```

### 7.11 使用 flatMap 一步完成映射和过滤

**影响：低中（LOW-MEDIUM）（消除中间数组）**

链式调用 `.map().filter(Boolean)` 会创建一个中间数组并迭代两次。使用 `.flatMap()` 在单次遍历中完成转换和过滤。

**不正确（2 次迭代，中间数组）：**

```typescript
const userNames = users
  .map(user => user.isActive ? user.name : null)
  .filter(Boolean)
```

**正确（1 次迭代，无中间数组）：**

```typescript
const userNames = users.flatMap(user =>
  user.isActive ? [user.name] : []
)
```

**更多示例：**

```typescript
// 从响应中提取有效邮箱
// 之前
const emails = responses
  .map(r => r.success ? r.data.email : null)
  .filter(Boolean)

// 之后
const emails = responses.flatMap(r =>
  r.success ? [r.data.email] : []
)

// 解析并过滤有效数字
// 之前
const numbers = strings
  .map(s => parseInt(s, 10))
  .filter(n => !isNaN(n))

// 之后
const numbers = strings.flatMap(s => {
  const n = parseInt(s, 10)
  return isNaN(n) ? [] : [n]
})
```

**何时使用：**
- 转换项目同时过滤掉部分项目
- 条件映射，某些输入不产生输出
- 解析/验证时跳过无效输入

### 7.12 使用循环而非排序求最小/最大值

**影响：低（LOW）（O(n) 而非 O(n log n)）**

找到最小或最大元素只需要一次遍历数组。排序是浪费且较慢的。

**不正确（O(n log n) - 排序找最新）：**

```typescript
interface Project {
  id: string
  name: string
  updatedAt: number
}

function getLatestProject(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => b.updatedAt - a.updatedAt)
  return sorted[0]
}
```

仅为了找到最大值就对整个数组排序。

**不正确（O(n log n) - 排序找最旧和最新）：**

```typescript
function getOldestAndNewest(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => a.updatedAt - b.updatedAt)
  return { oldest: sorted[0], newest: sorted[sorted.length - 1] }
}
```

当只需要最小/最大值时仍然不必要地排序。

**正确（O(n) - 单次循环）：**

```typescript
function getLatestProject(projects: Project[]) {
  if (projects.length === 0) return null
  
  let latest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > latest.updatedAt) {
      latest = projects[i]
    }
  }
  
  return latest
}

function getOldestAndNewest(projects: Project[]) {
  if (projects.length === 0) return { oldest: null, newest: null }
  
  let oldest = projects[0]
  let newest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt < oldest.updatedAt) oldest = projects[i]
    if (projects[i].updatedAt > newest.updatedAt) newest = projects[i]
  }
  
  return { oldest, newest }
}
```

单次遍历数组，不复制，不排序。

**替代方案（对小数组使用 Math.min/Math.max）：**

```typescript
const numbers = [5, 2, 8, 1, 9]
const min = Math.min(...numbers)
const max = Math.max(...numbers)
```

这对小数组有效，但对于非常大的数组，由于展开运算符的限制，可能会变慢或抛出错误。Chrome 143 中最大数组长度约为 124000，Safari 18 中约为 638000；具体数字可能有所不同——请参阅[此 fiddle](https://jsfiddle.net/qw1jabsx/4/)。为了可靠性，请使用循环方法。

### 7.13 使用 Set/Map 进行 O(1) 查找

**影响：低中（LOW-MEDIUM）（从 O(n) 到 O(1)）**

将数组转换为 Set/Map 以进行重复的成员检查。

**不正确（每次检查 O(n)）：**

```typescript
const allowedIds = ['a', 'b', 'c', ...]
items.filter(item => allowedIds.includes(item.id))
```

**正确（每次检查 O(1)）：**

```typescript
const allowedIds = new Set(['a', 'b', 'c', ...])
items.filter(item => allowedIds.has(item.id))
```

### 7.14 使用 toSorted() 而非 sort() 以保持不可变性

**影响：中高（MEDIUM-HIGH）（防止 React 状态中的变更错误）**

`.sort()` 会原地改变数组，这可能导致 React 状态和属性出现错误。使用 `.toSorted()` 创建新的排序数组而无需改变原数组。

**不正确（改变原始数组）：**

```typescript
function UserList({ users }: { users: User[] }) {
  // 改变了 users 属性数组！
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**正确（创建新数组）：**

```typescript
function UserList({ users }: { users: User[] }) {
  // 创建新的排序数组，原数组不变
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**为什么这很重要：**

1. Props/state 的变更破坏了 React 的不可变性模型——React 期望 props 和 state 被视为只读
2. 导致过期闭包错误——在闭包（回调、effects）中改变数组可能导致意外行为

**浏览器支持（旧浏览器回退）：**

`.toSorted()` 在所有现代浏览器中都可用（Chrome 110+、Safari 16+、Firefox 115+、Node.js 20+）。对于旧环境，使用展开运算符：

```typescript
// 旧浏览器的回退
const sorted = [...items].sort((a, b) => a.value - b.value)
```

**其他不可变数组方法：**

- `.toSorted()` - 不可变排序
- `.toReversed()` - 不可变反转
- `.toSpliced()` - 不可变拼接
- `.with()` - 不可变元素替换

---

## 8. 高级模式

**影响：低（LOW）**

针对特定需要仔细实现的情况的高级模式。

### 8.1 初始化应用一次，而非每次挂载

**影响：低中（LOW-MEDIUM）（避免开发环境中的重复初始化）**

不要将必须每次应用加载运行一次的全局初始化放在组件的 `useEffect([])` 中。组件可能重新挂载，effects 会重新执行。使用模块级守卫或入口模块中的顶级初始化。

**不正确（开发环境中执行两次，重新挂载时再次执行）：**

```tsx
function Comp() {
  useEffect(() => {
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

**正确（每次应用加载一次）：**

```tsx
let didInit = false

function Comp() {
  useEffect(() => {
    if (didInit) return
    didInit = true
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

参考：[https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application](https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application)

### 8.2 将事件处理程序存储在 Refs 中

**影响：低（LOW）（稳定订阅）**

当在不应因回调更改而重新订阅的 effects 中使用回调时，将其存储在 refs 中。

**不正确（每次渲染都重新订阅）：**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}
```

**正确（稳定订阅）：**

```tsx
import { useEffectEvent } from 'react'

function useWindowEvent(event: string, handler: (e) => void) {
  const onEvent = useEffectEvent(handler)

  useEffect(() => {
    window.addEventListener(event, onEvent)
    return () => window.removeEventListener(event, onEvent)
  }, [event])
}
```

**替代方案：如果你使用最新版 React，可以使用 `useEffectEvent`：**

`useEffectEvent` 为同一模式提供了更清晰的 API：它创建一个总是调用最新版本处理程序的稳定函数引用。

### 8.3 useEffectEvent 用于稳定回调引用

**影响：低（LOW）（防止 effect 重复执行）**

在回调中访问最新值，而不必将它们添加到依赖数组中。防止 effect 重复执行，同时避免过期闭包。

**不正确（每次回调更改时 effect 都重新执行）：**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300)
    return () => clearTimeout(timeout)
  }, [query, onSearch])
}
```

**正确（使用 React 的 useEffectEvent）：**

```tsx
import { useEffectEvent } from 'react';

function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  const onSearchEvent = useEffectEvent(onSearch)

  useEffect(() => {
    const timeout = setTimeout(() => onSearchEvent(query), 300)
    return () => clearTimeout(timeout)
  }, [query])
}
```

---

## 参考

1. [https://react.dev](https://react.dev)
2. [https://nextjs.org](https://nextjs.org)
3. [https://swr.vercel.app](https://swr.vercel.app)
4. [https://github.com/shuding/better-all](https://github.com/shuding/better-all)
5. [https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)
6. [https://vercel.com/blog/how-we-optimized-package-imports-in-next-js](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
7. [https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)
