---
title: 使用 requestIdleCallback 延迟非关键工作
impact: MEDIUM
impactDescription: 在后台任务期间保持 UI 响应
tags: javascript, performance, idle, scheduling, analytics
---

## 使用 requestIdleCallback 延迟非关键工作

**影响：中（在后台任务期间保持 UI 响应）**

使用 `requestIdleCallback()` 在浏览器空闲期间安排非关键工作。这使主线程保持空闲以处理用户交互和动画，减少卡顿并提高感知性能。

**错误做法（用户交互期间阻塞主线程）：**

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

**正确做法（将非关键工作延迟到空闲时间）：**

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

**为需要完成的工作设置超时：**

```typescript
// 确保分析在 2 秒内触发，即使浏览器一直繁忙
requestIdleCallback(
  () => analytics.track('page_view', { path: location.pathname }),
  { timeout: 2000 }
)
```

**将大型任务分块：**

```typescript
function processLargeDataset(items: Item[]) {
  let index = 0

  function processChunk(deadline: IdleDeadline) {
    // 在有空闲时间时处理项目（目标 <50ms 每块）
    while (index < items.length && deadline.timeRemaining() > 0) {
      processItem(items[index])
      index++
    }

    // 如果还有更多项目，安排下一个块
    if (index < items.length) {
      requestIdleCallback(processChunk)
    }
  }

  requestIdleCallback(processChunk)
}
```

**不支持的浏览器的回退方案：**

```typescript
const scheduleIdleWork = window.requestIdleCallback ?? ((cb: () => void) => setTimeout(cb, 1))

scheduleIdleWork(() => {
  // 非关键工作
})
```

**何时使用：**

- 分析和遥测
- 将状态保存到 localStorage/IndexedDB
- 预取可能下一步操作的资源
- 处理非紧急的数据转换
- 非关键功能的懒初始化

**何时不使用：**

- 需要即时反馈的用户发起操作
- 用户正在等待的渲染更新
- 时间敏感的操作
