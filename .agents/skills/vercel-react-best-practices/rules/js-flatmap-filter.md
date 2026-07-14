---
title: 使用 flatMap 一步完成映射和过滤
impact: LOW-MEDIUM
impactDescription: 消除中间数组
tags: javascript, arrays, flatMap, filter, performance
---

## 使用 flatMap 一步完成映射和过滤

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
