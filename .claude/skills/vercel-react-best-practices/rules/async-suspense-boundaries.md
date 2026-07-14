---
title: 战略性 Suspense 边界
impact: HIGH
impactDescription: 加快首次绘制
tags: async, suspense, streaming, layout-shift
---

## 战略性 Suspense 边界

在异步组件返回 JSX 之前，不要等待数据，而是使用 Suspense 边界在数据加载时更快地显示包装 UI。

**错误做法（包装层被数据获取阻塞）：**

```tsx
async function Page() {
  const data = await fetchData() // 阻塞整个页面
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <DataDisplay data={data} />
      </div>
      <div>Footer</div>
    </div>
  )
}
```

整个布局都在等待数据，即使只有中间部分需要它。

**正确做法（包装层立即显示，数据流式传入）：**

```tsx
function Page() {
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <Suspense fallback={<Skeleton />}>
          <DataDisplay />
        </Suspense>
      </div>
      <div>Footer</div>
    </div>
  )
}

async function DataDisplay() {
  const data = await fetchData() // 仅阻塞此组件
  return <div>{data.content}</div>
}
```

Sidebar、Header 和 Footer 立即渲染。只有 DataDisplay 等待数据。

**替代方案（跨组件共享 promise）：**

```tsx
function Page() {
  // 立即开始获取，但不 await
  const dataPromise = fetchData()
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
      <div>Footer</div>
    </div>
  )
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // 解包 promise
  return <div>{data.content}</div>
}

function DataSummary({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // 复用同一个 promise
  return <div>{data.summary}</div>
}
```

两个组件共享同一个 promise，所以只发生一次获取。布局立即渲染，两个组件一起等待。

**何时不使用此模式：**

- 布局决策需要的关键数据（影响定位）
- 首屏之上对 SEO 关键的内容
- 小而快的查询，suspense 开销不值得
- 当你想避免布局偏移（加载 → 内容跳动）

**权衡：** 更快的初始绘制 vs 潜在的布局偏移。根据你的 UX 优先级进行选择。
