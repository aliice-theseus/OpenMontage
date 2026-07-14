---
title: 像 API 路由一样认证 Server Actions
impact: CRITICAL
impactDescription: 防止对服务端操作的未授权访问
tags: server, server-actions, authentication, security, authorization
---

## 像 API 路由一样认证 Server Actions

**影响：严重（防止对服务端操作的未授权访问）**

Server Actions（带有 `"use server"` 的函数）像 API 路由一样暴露为公共端点。始终**在每个 Server Action 内部**验证身份验证和授权——不要仅依赖中间件、布局守卫或页面级别检查，因为 Server Actions 可以直接被调用。

Next.js 文档明确指出："像对待公共 API 端点一样对待 Server Actions 的安全考虑，并验证用户是否被允许执行修改操作。"

**错误做法（无身份验证检查）：**

```typescript
'use server'

export async function deleteUser(userId: string) {
  // 任何人都可以调用此函数！没有身份验证检查
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**正确做法（在 action 内部进行身份验证）：**

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
  
  // 然后认证身份
  const session = await verifySession()
  if (!session) {
    throw new Error('未授权')
  }
  
  // 然后验证权限
  if (session.user.id !== validated.userId) {
    throw new Error('只能更新自己的资料')
  }
  
  // 最后执行修改操作
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
