---
title: 合并多个数组迭代
impact: LOW-MEDIUM
impactDescription: 减少迭代次数
tags: javascript, arrays, loops, performance
---

## 合并多个数组迭代

多个 `.filter()` 或 `.map()` 调用会多次迭代数组。合并为一个循环。

**不正确（3 次迭代）：**

```typescript
const admins = users.filter(u => u.isAdmin)
const testers = users.filter(u => u.isTester)
const inactive = users.filter(u => !u.isActive)
```

**正确（1 次迭代）：**

```typescript
const admins: User[] = []
const testers: User[] = []
const inactive: User[] = []

for (const user of users) {
  if (user.isAdmin) admins.push(user)
  if (user.isTester) testers.push(user)
  if (!user.isActive) inactive.push(user)
}
```
