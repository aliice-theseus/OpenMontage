---
title: 数组比较前先检查长度
impact: MEDIUM-HIGH
impactDescription: 长度不同时避免昂贵操作
tags: javascript, arrays, performance, optimization, comparison
---

## 数组比较前先检查长度

在使用昂贵操作（排序、深度相等、序列化）比较数组时，先检查长度。如果长度不同，数组不可能相等。

在实际应用中，当比较在热路径（事件处理程序、渲染循环）中运行时，这种优化特别有价值。

**不正确（总是执行昂贵比较）：**

```typescript
function hasChanges(current: string[], original: string[]) {
  // 即使长度不同也总是排序和拼接
  return current.sort().join() !== original.sort().join()
}
```

即使在 `current.length` 为 5 而 `original.length` 为 100 时，也会执行两次 O(n log n) 排序。还有拼接数组和比较字符串的开销。

**正确（先进行 O(1) 长度检查）：**

```typescript
function hasChanges(current: string[], original: string[]) {
  // 如果长度不同，提前返回
  if (current.length !== original.length) {
    return true
  }
  // 仅在长度匹配时排序
  const currentSorted = current.toSorted()
  const originalSorted = original.toSorted()
  for (let i = 0; i < currentSorted.length; i++) {
    if (currentSorted[i] !== originalSorted[i]) {
      return true
    }
  }
  return false
}
```

这种新方法更高效，因为：
- 长度不同时避免了排序和拼接数组的开销
- 避免了为拼接后的字符串消耗内存（对大数组尤其重要）
- 避免了改变原始数组
- 发现差异时提前返回
