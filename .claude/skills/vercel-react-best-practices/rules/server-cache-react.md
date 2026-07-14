---
title: 使用 React.cache() 进行请求内去重
impact: MEDIUM
impactDescription: 在请求内去重
tags: server, cache, react-cache, deduplication
---

## 使用 React.cache() 进行请求内去重

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

在单个请求内，多次调用 `getCurrentUser()` 只会执行一次查询。

**避免使用内联对象作为参数：**

`React.cache()` 使用浅比较（`Object.is`）来判断缓存命中。内联对象每次调用都会创建新的引用，导致无法命中缓存。

**错误做法（总是缓存未命中）：**

```typescript
const getUser = cache(async (params: { uid: number }) => {
  return await db.user.findUnique({ where: { id: params.uid } })
})

// 每次调用创建新对象，永远无法命中缓存
getUser({ uid: 1 })
getUser({ uid: 1 })  // 缓存未命中，再次执行查询
```

**正确做法（缓存命中）：**

```typescript
const getUser = cache(async (uid: number) => {
  return await db.user.findUnique({ where: { id: uid } })
})

// 原始类型参数使用值相等性
getUser(1)
getUser(1)  // 缓存命中，返回缓存结果
```

如果必须传递对象，请传递相同的引用：

```typescript
const params = { uid: 1 }
getUser(params)  // 执行查询
getUser(params)  // 缓存命中（相同引用）
```

**Next.js 特定说明：**

在 Next.js 中，`fetch` API 会自动扩展请求记忆化。具有相同 URL 和选项的请求会在单个请求内自动去重，因此你不需要为 `fetch` 调用使用 `React.cache()`。但是，`React.cache()` 对于其他异步任务仍然至关重要：

- 数据库查询（Prisma、Drizzle 等）
- 重型计算
- 身份验证检查
- 文件系统操作
- 任何非 fetch 的异步工作

使用 `React.cache()` 在组件树中去重这些操作。

参考：[React.cache 文档](https://react.dev/reference/react/cache)
