---
name: vercel-react-best-practices
description: 来自 Vercel Engineering 的 React 和 Next.js 性能优化指南。在编写、审查或重构 React/Next.js 代码时，应使用此技能以确保最佳性能模式。触发条件包括涉及 React 组件、Next.js 页面、数据获取、包优化或性能改进的任务。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React 最佳实践

React 和 Next.js 应用的全面性能优化指南，由 Vercel 维护。包含 8 个类别的 65 条规则，按影响程度排序，用于指导自动化重构和代码生成。

> **扩展参考：** 本目录中的 [`AGENTS.md`](AGENTS.md) 是从 Vercel 上游获取的长篇指南。它是本技能范围内补充参考材料——`SKILL.md` 是可加载的入口点和权威文件。它不会覆盖或扩展仓库根目录的 `AGENTS.md` / `AGENT_GUIDE.md`。

## 何时应用

在以下情况下参考这些指南：
- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务端）
- 审查代码的性能问题
- 重构现有的 React/Next.js 代码
- 优化包大小或加载时间

## 按优先级分类的规则类别

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | 消除瀑布请求 | 致命（CRITICAL） | `async-` |
| 2 | 包大小优化 | 致命（CRITICAL） | `bundle-` |
| 3 | 服务端性能 | 高（HIGH） | `server-` |
| 4 | 客户端数据获取 | 中高（MEDIUM-HIGH） | `client-` |
| 5 | 重渲染优化 | 中（MEDIUM） | `rerender-` |
| 6 | 渲染性能 | 中（MEDIUM） | `rendering-` |
| 7 | JavaScript 性能 | 低中（LOW-MEDIUM） | `js-` |
| 8 | 高级模式 | 低（LOW） | `advanced-` |

## 快速参考

### 1. 消除瀑布请求（致命 CRITICAL）

- `async-defer-await` - 将 await 移到实际使用的分支中
- `async-parallel` - 对独立操作使用 Promise.all()
- `async-dependencies` - 对部分依赖使用 better-all
- `async-api-routes` - 在 API 路由中尽早启动 promise，延迟 await
- `async-suspense-boundaries` - 使用 Suspense 流式传输内容

### 2. 包大小优化（致命 CRITICAL）

- `bundle-barrel-imports` - 直接导入，避免 barrel 文件
- `bundle-dynamic-imports` - 对重型组件使用 next/dynamic
- `bundle-defer-third-party` - 在注水后加载分析/日志模块
- `bundle-conditional` - 仅在功能激活时加载模块
- `bundle-preload` - 在悬停/聚焦时预加载以提高感知速度

### 3. 服务端性能（高 HIGH）

- `server-auth-actions` - 像 API 路由一样认证 Server Actions
- `server-cache-react` - 使用 React.cache() 进行单请求去重
- `server-cache-lru` - 使用 LRU 缓存进行跨请求缓存
- `server-dedup-props` - 避免 RSC 属性中的重复序列化
- `server-hoist-static-io` - 将静态 I/O（字体、Logo）提升到模块级别
- `server-serialization` - 最小化传递给客户端组件的数据
- `server-parallel-fetching` - 重组组件以实现并行获取
- `server-parallel-nested-fetching` - 在 Promise.all 中链接每个项目的嵌套获取
- `server-after-nonblocking` - 使用 after() 进行非阻塞操作

### 4. 客户端数据获取（中高 MEDIUM-HIGH）

- `client-swr-dedup` - 使用 SWR 进行自动请求去重
- `client-event-listeners` - 去重全局事件监听器
- `client-passive-event-listeners` - 对滚动使用被动监听器
- `client-localstorage-schema` - 版本化和最小化 localStorage 数据

### 5. 重渲染优化（中 MEDIUM）

- `rerender-defer-reads` - 不要订阅仅在回调中使用的状态
- `rerender-memo` - 将昂贵工作提取到 memo 化组件中
- `rerender-memo-with-default-value` - 提升默认的非原始属性
- `rerender-dependencies` - 在 effect 中使用原始类型依赖
- `rerender-derived-state` - 订阅派生后的布尔值，而非原始值
- `rerender-derived-state-no-effect` - 在渲染期间派生状态，而非 effect 中
- `rerender-functional-setstate` - 使用函数式 setState 获得稳定回调
- `rerender-lazy-state-init` - 对昂贵初始值传递函数给 useState
- `rerender-simple-expression-in-memo` - 避免对简单原始类型使用 memo
- `rerender-split-combined-hooks` - 拆分具有独立依赖的 hooks
- `rerender-move-effect-to-event` - 将交互逻辑放入事件处理程序
- `rerender-transitions` - 对非紧急更新使用 startTransition
- `rerender-use-deferred-value` - 延迟昂贵渲染以保持输入响应
- `rerender-use-ref-transient-values` - 对瞬态频繁值使用 ref
- `rerender-no-inline-components` - 不要在组件内部定义组件

### 6. 渲染性能（中 MEDIUM）

- `rendering-animate-svg-wrapper` - 为 div 包装器而非 SVG 元素添加动画
- `rendering-content-visibility` - 对长列表使用 content-visibility
- `rendering-hoist-jsx` - 将静态 JSX 提取到组件外部
- `rendering-svg-precision` - 降低 SVG 坐标精度
- `rendering-hydration-no-flicker` - 对仅客户端数据使用内联脚本
- `rendering-hydration-suppress-warning` - 抑制预期的不匹配警告
- `rendering-activity` - 使用 Activity 组件进行显示/隐藏
- `rendering-conditional-render` - 使用三元运算符，而非 && 进行条件渲染
- `rendering-usetransition-loading` - 优先使用 useTransition 处理加载状态
- `rendering-resource-hints` - 使用 React DOM 资源提示进行预加载
- `rendering-script-defer-async` - 在 script 标签上使用 defer 或 async

### 7. JavaScript 性能（低中 LOW-MEDIUM）

- `js-batch-dom-css` - 通过类或 cssText 分组 CSS 更改
- `js-index-maps` - 为重复查找构建 Map
- `js-cache-property-access` - 在循环中缓存对象属性
- `js-cache-function-results` - 在模块级 Map 中缓存函数结果
- `js-cache-storage` - 缓存 localStorage/sessionStorage 读取
- `js-combine-iterations` - 将多个 filter/map 合并为一个循环
- `js-length-check-first` - 在昂贵比较前检查数组长度
- `js-early-exit` - 从函数中提前返回
- `js-hoist-regexp` - 将 RegExp 创建提升到循环外
- `js-min-max-loop` - 使用循环而非 sort 求最小/最大值
- `js-set-map-lookups` - 使用 Set/Map 进行 O(1) 查找
- `js-tosorted-immutable` - 使用 toSorted() 保持不可变性
- `js-flatmap-filter` - 使用 flatMap 一步完成映射和过滤
- `js-request-idle-callback` - 将非关键工作延迟到浏览器空闲时间

### 8. 高级模式（低 LOW）

- `advanced-event-handler-refs` - 将事件处理程序存储在 refs 中
- `advanced-init-once` - 每次应用加载时初始化一次
- `advanced-use-latest` - 使用 useLatest 获得稳定的回调 refs

## 如何使用

阅读各个规则文件获取详细解释和代码示例：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

每个规则文件包含：
- 为什么重要：简要说明
- 不正确代码示例及解释
- 正确代码示例及解释
- 额外上下文和引用

## 完整编译文档

获取包含所有规则的完整指南：`AGENTS.md`
