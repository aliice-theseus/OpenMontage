---
title: 从函数中提前返回
impact: LOW-MEDIUM
impactDescription: 避免不必要的计算
tags: javascript, functions, optimization, early-return
---

## 从函数中提前返回

当结果已确定时提前返回，以跳过不必要的处理。

**错误做法（即使在找到答案后仍处理所有项目）：**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  let errorMessage = ''
  
  for (const user of users) {
    if (!user.email) {
      hasError = true
      errorMessage = '需要邮箱'
    }
    if (!user.name) {
      hasError = true
      errorMessage = '需要姓名'
    }
    // 即使找到错误仍继续检查所有用户
  }
  
  return hasError ? { valid: false, error: errorMessage } : { valid: true }
}
```

**正确做法（在第一个错误时立即返回）：**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) {
      return { valid: false, error: '需要邮箱' }
    }
    if (!user.name) {
      return { valid: false, error: '需要姓名' }
    }
  }

  return { valid: true }
}
```
