---
title: 为重复查找构建索引映射
impact: LOW-MEDIUM
impactDescription: 从 100 万次操作降到 2000 次
tags: javascript, map, indexing, optimization, performance
---

## 为重复查找构建索引映射

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

构建一次映射（O(n)），然后所有查找都是 O(1)。
1000 个订单 × 1000 个用户：100 万次操作 → 2000 次操作。
