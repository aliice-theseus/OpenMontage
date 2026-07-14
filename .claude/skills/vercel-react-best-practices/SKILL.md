---
name: vercel-react-best-practices
description: 来自 Vercel 工程团队的 React 和 Next.js 性能优化指南。在编写、审查或重构 React/Next.js 代码时使用此技能以确保最佳性能模式。适用于涉及 React 组件、Next.js 页面、数据获取、打包优化或性能改进的任务。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React 最佳实践

由 Vercel 维护的 React 和 Next.js 应用综合性能优化指南。包含跨 8 个类别的 65 条规则，按影响程度排序，以指导自动化重构和代码生成。

> **扩展参考：** 本目录中的 [`AGENTS.md`](AGENTS.md) 是长格式上游指南（从 Vercel 引入）。它是仅限于此技能的补充参考材料 — `SKILL.md` 是可加载的入口点和权威文档。它不会覆盖或扩展仓库根目录的 `AGENTS.md` / `AGENT_GUIDE.md`。

## 何时应用

在以下情况下参考这些指南：
- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务端）
- 审查代码的性能问题
- 重构现有 React/Next.js 代码
- 优化包大小或加载时间

## 按优先级分类的规则类别

| 优先级 | 类别 | 影响 | 前缀 |
|--------|------|------|------|
| 1 | 消除瀑布请求 | 严重 | `async-` |
| 2 | 包大小优化 | 严重 | `bundle-` |
| 3 | 服务端性能 | 高 | `server-` |
| 4 | 客户端数据获取 | 中-高 | `client-` |
| 5 | 重渲染优化 | 中 | `rerender-` |
| 6 | 渲染性能 | 中 | `rendering-` |
| 7 | JavaScript 性能 | 低-中 | `js-` |
| 8 | 高级模式 | 低 | `advanced-` |

## 快速参考

### 1. 消除瀑布请求（严重）

- `async-defer-await` - 将 await 移到实际使用的分支中
- `async-parallel` - 对独立操作使用 Promise.all()
- `async-dependencies` - 对部分依赖使用 better-all
- `async-api-routes` - 在 API 路由中提前启动 Promise，延迟 await
- `async-suspense-boundaries` - 使用 Suspense 流式传输内容

### 2. 包大小优化（严重）

- `bundle-barrel-imports` - 直接导入，避免 barrel 文件
- `bundle-dynamic-imports` - 对重型组件使用 next/dynamic
- `bundle-defer-third-party` - 在 hydration 后加载分析/日志库
- `bundle-conditional` - 仅在功能激活时加载模块
- `bundle-preload` - 在悬停/聚焦时预加载以提高感知速度

### 3. 服务端性能（高）

- `server-auth-actions` - 像 API 路由一样认证 Server Actions
- `server-cache-react` - 使用 React.cache() 进行请求内去重
- `server-cache-lru` - 使用 LRU 缓存进行跨请求缓存
- `server-dedup-props` - 避免 RSC props 中的重复序列化
- `server-hoist-static-io` - 将静态 I/O（字体、logo）提升到模块级别
- `server-serialization` - 最小化传递给客户端组件的数据
- `server-parallel-fetching` - 通过组件组合实现并行数据获取
- `server-parallel-nested-fetching` - 在 Promise.all 中为每个条目链式嵌套获取
- `server-after-nonblocking` - 使用 after() 进行非阻塞操作

### 4. 客户端数据获取（中-高）

- `client-swr-dedup` - 使用 SWR 进行自动请求去重
- `client-event-listeners` - 去重全局事件监听器
- `client-passive-event-listeners` - 为滚动使用 passive 监听器
- `client-localstorage-schema` - 版本化和最小化 localStorage 数据

### 5. 重渲染优化（中）

- `rerender-defer-reads` - 不要订阅仅在回调中使用的状态
- `rerender-memo` - 将昂贵计算提取到 memoized 组件中
- `rerender-memo-with-default-value` - 将默认非原始 props 提升为常量
- `rerender-dependencies` - 在 effect 中使用原始类型依赖
- `rerender-derived-state` - 订阅派生布尔值，而非原始值
- `rerender-derived-state-no-effect` - 在渲染期间派生状态，而非 effect
- `rerender-functional-setstate` - 使用函数式 setState 实现稳定回调
- `rerender-lazy-state-init` - 对昂贵初始值传递函数给 useState
- `rerender-simple-expression-in-memo` - 避免对简单原始类型使用 memo
- `rerender-split-combined-hooks` - 拆分具有独立依赖的 hooks
- `rerender-move-effect-to-event` - 将交互逻辑放在事件处理函数中
- `rerender-transitions` - 对非紧急更新使用 startTransition
- `rerender-use-deferred-value` - 延迟昂贵渲染以保持输入响应
- `rerender-use-ref-transient-values` - 对频繁变化的瞬态值使用 refs
- `rerender-no-inline-components` - 不要在组件内部定义组件

### 6. 渲染性能（中）

- `rendering-animate-svg-wrapper` - 动画作用于 div 包装器，而非 SVG 元素
- `rendering-content-visibility` - 对长列表使用 content-visibility
- `rendering-hoist-jsx` - 将静态 JSX 提取到组件外部
- `rendering-svg-precision` - 降低 SVG 坐标精度
- `rendering-hydration-no-flicker` - 对内联脚本使用客户端专属数据
- `rendering-hydration-suppress-warning` - 抑制预期的不匹配警告
- `rendering-activity` - 使用 Activity 组件进行显示/隐藏
- `rendering-conditional-render` - 使用三元运算符，而非 &&
- `rendering-usetransition-loading` - 优先使用 useTransition 处理加载状态
- `rendering-resource-hints` - 使用 React DOM 资源提示进行预加载
- `rendering-script-defer-async` - 在 script 标签上使用 defer 或 async

### 7. JavaScript 性能（低-中）

- `js-batch-dom-css` - 通过 class 或 cssText 分组 CSS 更改
- `js-index-maps` - 为重复查找构建 Map
- `js-cache-property-access` - 在循环中缓存对象属性
- `js-cache-function-results` - 在模块级 Map 中缓存函数结果
- `js-cache-storage` - 缓存 localStorage/sessionStorage 读取
- `js-combine-iterations` - 将多个 filter/map 合并为一个循环
- `js-length-check-first` - 在昂贵比较之前检查数组长度
- `js-early-exit` - 从函数中提前返回
- `js-hoist-regexp` - 将 RegExp 创建提升到循环外部
- `js-min-max-loop` - 使用循环找最小/最大值，而非排序
- `js-set-map-lookups` - 使用 Set/Map 进行 O(1) 查找
- `js-tosorted-immutable` - 使用 toSorted() 保持不可变性
- `js-flatmap-filter` - 使用 flatMap 一次完成 map 和 filter
- `js-request-idle-callback` - 将非关键工作延迟到浏览器空闲时间

### 8. 高级模式（低）

- `advanced-event-handler-refs` - 将事件处理函数存储在 refs 中
- `advanced-init-once` - 每次应用加载仅初始化一次
- `advanced-use-latest` - 使用 useLatest 实现稳定的回调引用

## 如何使用

阅读单个规则文件以获取详细解释和代码示例：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

每个规则文件包含：
- 简要说明为什么重要
- 错误代码示例及解释
- 正确代码示例及解释
- 额外的上下文和参考

## 完整编译文档

查看包含所有规则的完整指南：`AGENTS.md`
