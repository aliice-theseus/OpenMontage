---
title: 并行嵌套数据获取
impact: CRITICAL
impactDescription: 消除服务端瀑布请求
tags: server, rsc, parallel-fetching, promise-chaining
---

## 并行嵌套数据获取

在并行获取嵌套数据时，在每个项目的 promise 中链式依赖获取，这样慢的项目不会阻塞其他项目。

**不正确（单个慢项目阻塞所有嵌套获取）：**

```tsx
const chats = await Promise.all(
  chatIds.map(id => getChat(id))
)

const chatAuthors = await Promise.all(
  chats.map(chat => getUser(chat.author))
)
```

如果 100 个中的一个 `getChat(id)` 非常慢，其他 99 个聊天的作者即使数据已就绪也无法开始加载。

**正确（每个项目链式自己的嵌套获取）：**

```tsx
const chatAuthors = await Promise.all(
  chatIds.map(id => getChat(id).then(chat => getUser(chat.author)))
)
```

每个项目独立链式 `getChat` → `getUser`，所以慢的聊天不会阻塞其他项目的作者获取。
