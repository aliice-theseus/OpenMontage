---
title: 基于依赖的并行化
impact: CRITICAL
impactDescription: 提升 2-10 倍
tags: async, parallelization, dependencies, better-all
---

## 基于依赖的并行化

对于存在部分依赖的操作，使用 `better-all` 最大化并行度。它会自动在最早可能的时间启动每个任务。

**错误做法（profile 不必要地等待 config）：**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**正确做法（config 和 profile 并行运行）：**

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

**无需额外依赖的替代方案：**

我们也可以先创建所有 promise，最后再 `Promise.all()`。

```typescript
const userPromise = fetchUser()
const profilePromise = userPromise.then(user => fetchProfile(user.id))

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise
])
```

参考：[https://github.com/shuding/better-all](https://github.com/shuding/better-all)
