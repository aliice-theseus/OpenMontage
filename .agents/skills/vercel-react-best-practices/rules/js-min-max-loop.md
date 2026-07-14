---
title: 使用循环而非排序求最小/最大值
impact: LOW
impactDescription: O(n) 而非 O(n log n)
tags: javascript, arrays, performance, sorting, algorithms
---

## 使用循环而非排序求最小/最大值

找到最小或最大元素只需要一次遍历数组。排序是浪费且较慢的。

**不正确（O(n log n) - 排序找最新）：**

```typescript
interface Project {
  id: string
  name: string
  updatedAt: number
}

function getLatestProject(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => b.updatedAt - a.updatedAt)
  return sorted[0]
}
```

仅为了找到最大值就对整个数组排序。

**不正确（O(n log n) - 排序找最旧和最新）：**

```typescript
function getOldestAndNewest(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => a.updatedAt - b.updatedAt)
  return { oldest: sorted[0], newest: sorted[sorted.length - 1] }
}
```

当只需要最小/最大值时仍然不必要地排序。

**正确（O(n) - 单次循环）：**

```typescript
function getLatestProject(projects: Project[]) {
  if (projects.length === 0) return null
  
  let latest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > latest.updatedAt) {
      latest = projects[i]
    }
  }
  
  return latest
}

function getOldestAndNewest(projects: Project[]) {
  if (projects.length === 0) return { oldest: null, newest: null }
  
  let oldest = projects[0]
  let newest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt < oldest.updatedAt) oldest = projects[i]
    if (projects[i].updatedAt > newest.updatedAt) newest = projects[i]
  }
  
  return { oldest, newest }
}
```

单次遍历数组，不复制，不排序。

**替代方案（对小数组使用 Math.min/Math.max）：**

```typescript
const numbers = [5, 2, 8, 1, 9]
const min = Math.min(...numbers)
const max = Math.max(...numbers)
```

这对小数组有效，但对于非常大的数组，由于展开运算符的限制，可能会变慢或抛出错误。Chrome 143 中最大数组长度约为 124000，Safari 18 中约为 638000；具体数字可能有所不同——请参阅[此 fiddle](https://jsfiddle.net/qw1jabsx/4/)。为了可靠性，请使用循环方法。
