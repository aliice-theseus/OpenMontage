---
title: 为重复查找构建索引映射
impact: LOW-MEDIUM
impactDescription: 从 1M 操作降至 2K 操作
tags: javascript, map, indexing, optimization, performance
---

## 为重复查找构建索引映射

对同一键的多个 `.find()` 调用应使用 Map。

**错误做法（每次查找 O(n)）：**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId)
  }))
}
```

**正确做法（每次查找 O(1)）：**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map(u => [u.id, u]))

  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId)
  }))
}
```

Map 构建一次（O(n)），之后所有查找都是 O(1)。
对于 1000 个订单 × 1000 个用户：从 1M 操作降至 2K 操作。
