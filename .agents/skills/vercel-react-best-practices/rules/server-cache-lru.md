---
title: 跨请求 LRU 缓存
impact: HIGH
impactDescription: 跨请求缓存
tags: server, cache, lru, cross-request
---

## 跨请求 LRU 缓存

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
