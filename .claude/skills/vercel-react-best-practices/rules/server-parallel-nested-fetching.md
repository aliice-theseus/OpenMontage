---
title: 并行嵌套数据获取
impact: CRITICAL
impactDescription: 消除服务端瀑布请求
tags: server, rsc, parallel-fetching, promise-chaining
---

## 并行嵌套数据获取

在并行获取嵌套数据时，将依赖获取链式绑定在每个条目的 promise 中，这样慢的条目不会阻塞其他条目。

**错误做法（单个慢条目阻塞所有嵌套获取）：**

```tsx
const chats = await Promise.all(
  chatIds.map(id => getChat(id))
)

const chatAuthors = await Promise.all(
  chats.map(chat => getUser(chat.author))
)
```

如果 100 个 `getChat(id)` 中有一个极其缓慢，其他 99 个聊天的作者数据即使已准备就绪，也无法开始加载。

**正确做法（每个条目链式绑定自己的嵌套获取）：**

```tsx
const chatAuthors = await Promise.all(
  chatIds.map(id => getChat(id).then(chat => getUser(chat.author)))
)
```

每个条目独立链式执行 `getChat` → `getUser`，所以一个慢聊天不会阻塞其他条目的作者获取。
