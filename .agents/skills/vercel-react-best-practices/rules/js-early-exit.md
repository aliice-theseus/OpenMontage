---
title: 从函数中提前返回
impact: LOW-MEDIUM
impactDescription: 避免不必要的计算
tags: javascript, functions, optimization, early-return
---

## 从函数中提前返回

当结果已确定时提前返回，以跳过不必要的处理。

**不正确（即使在找到答案后仍处理所有项目）：**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  let errorMessage = ''
  
  for (const user of users) {
    if (!user.email) {
      hasError = true
      errorMessage = '邮箱必填'
    }
    if (!user.name) {
      hasError = true
      errorMessage = '姓名必填'
    }
    // 即使在发现错误后仍继续检查所有用户
  }
  
  return hasError ? { valid: false, error: errorMessage } : { valid: true }
}
```

**正确（在第一个错误时立即返回）：**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) {
      return { valid: false, error: '邮箱必填' }
    }
    if (!user.name) {
      return { valid: false, error: '姓名必填' }
    }
  }

  return { valid: true }
}
```
