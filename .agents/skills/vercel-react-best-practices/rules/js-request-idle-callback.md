---
title: 使用 requestIdleCallback 延迟非关键工作
impact: MEDIUM
impactDescription: 在后台任务期间保持 UI 响应
tags: javascript, performance, idle, scheduling, analytics
---

## 使用 requestIdleCallback 延迟非关键工作

**影响：中（MEDIUM）（在后台任务期间保持 UI 响应）**

使用 `requestIdleCallback()` 在浏览器空闲期间安排非关键工作。这使主线程有空处理用户交互和动画，减少卡顿并改善感知性能。

**不正确（在用户交互期间阻塞主线程）：**

```typescript
function handleSearch(query: string) {
  const results = searchItems(query)
  setResults(results)

  // 这些立即阻塞主线程
  analytics.track('search', { query })
  saveToRecentSearches(query)
  prefetchTopResults(results.slice(0, 3))
}
```

**正确（将非关键工作延迟到空闲时间）：**

```typescript
function handleSearch(query: string) {
  const results = searchItems(query)
  setResults(results)

  // 将非关键工作延迟到空闲时段
  requestIdleCallback(() => {
    analytics.track('search', { query })
  })

  requestIdleCallback(() => {
    saveToRecentSearches(query)
  })

  requestIdleCallback(() => {
    prefetchTopResults(results.slice(0, 3))
  })
}
```

**带超时以确保工作执行：**

```typescript
// 确保分析在 2 秒内触发，即使浏览器保持忙碌
requestIdleCallback(
  () => analytics.track('page_view', { path: location.pathname }),
  { timeout: 2000 }
)
```

**拆分大型任务：**

```typescript
function processLargeDataset(items: Item[]) {
  let index = 0

  function processChunk(deadline: IdleDeadline) {
    // 在有空闲时间时处理项目（目标 <50ms 每块）
    while (index < items.length && deadline.timeRemaining() > 0) {
      processItem(items[index])
      index++
    }

    // 如果还有剩余项目，安排下一块
    if (index < items.length) {
      requestIdleCallback(processChunk)
    }
  }

  requestIdleCallback(processChunk)
}
```

**不支持的浏览器的回退：**

```typescript
const scheduleIdleWork = window.requestIdleCallback ?? ((cb: () => void) => setTimeout(cb, 1))

scheduleIdleWork(() => {
  // 非关键工作
})
```

**何时使用：**

- 分析和遥测
- 将状态保存到 localStorage/IndexedDB
- 预取下一步可能用到的资源
- 处理非紧急的数据转换
- 非关键功能的惰性初始化

**何时不使用：**

- 需要即时反馈的用户发起操作
- 用户正在等待的渲染更新
- 时间敏感的操作
