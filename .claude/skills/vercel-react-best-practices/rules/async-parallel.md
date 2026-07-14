---
title: 对独立操作使用 Promise.all()
impact: CRITICAL
impactDescription: 提升 2-10 倍
tags: async, parallelization, promises, waterfalls
---

## 对独立操作使用 Promise.all()

当异步操作之间没有相互依赖时，使用 `Promise.all()` 并行执行它们。

**错误做法（串行执行，3 次往返）：**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**正确做法（并行执行，1 次往返）：**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```
