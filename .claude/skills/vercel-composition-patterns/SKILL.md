---
name: vercel-composition-patterns
description:
  可扩展的 React 组合模式。在重构存在布尔属性泛滥的组件、
  构建灵活的组件库或设计可复用的 API 时使用。触发的任务涉及复合组件、
  渲染属性、Context Provider 或组件架构。包含 React 19
  API 变化。
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React 组合模式

用于构建灵活、可维护的 React 组件的组合模式。避免
布尔属性泛滥，使用复合组件、状态提升和
内部组合。这些模式使代码库在扩展时对人和 AI
代理都更易于协作。

> **扩展参考：** 本目录中的 [`AGENTS.md`](AGENTS.md) 是完整版上游指南（来自 Vercel）。它是本技能范围内的补充参考材料——`SKILL.md` 是可加载的入口点和权威文件。它不会覆盖或扩展仓库根目录的 `AGENTS.md` / `AGENT_GUIDE.md`。

## 何时应用

在以下场景参考这些指南：

- 重构具有大量布尔属性的组件
- 构建可复用的组件库
- 设计灵活的组件 API
- 审查组件架构
- 使用复合组件或 Context Provider

## 按优先级的规则类别

| 优先级 | 类别                | 影响   | 前缀          |
| -------- | ----------------------- | ------ | --------------- |
| 1        | 组件架构  | 高   | `architecture-` |
| 2        | 状态管理        | 中 | `state-`        |
| 3        | 实现模式 | 中 | `patterns-`     |
| 4        | React 19 API           | 中 | `react19-`      |

## 快速参考

### 1. 组件架构（高）

- `architecture-avoid-boolean-props` - 不要添加布尔属性来自定义行为；使用组合
- `architecture-compound-components` - 使用共享 context 构建复杂组件

### 2. 状态管理（中）

- `state-decouple-implementation` - Provider 是唯一知道状态管理方式的地方
- `state-context-interface` - 使用 state、actions、meta 定义通用接口以实现依赖注入
- `state-lift-state` - 将状态移入 Provider 组件以实现兄弟组件访问

### 3. 实现模式（中）

- `patterns-explicit-variants` - 创建显式的变体组件而非布尔模式
- `patterns-children-over-render-props` - 使用 children 进行组合而非 renderX 属性

### 4. React 19 API（中）

> **⚠️ 仅 React 19+。** 如果使用 React 18 或更早版本，请跳过本节。

- `react19-no-forwardref` - 不要使用 `forwardRef`；使用 `use()` 替代 `useContext()`

## 如何使用

阅读各规则文件以获取详细说明和代码示例：

```
rules/architecture-avoid-boolean-props.md
rules/state-context-interface.md
```

每个规则文件包含：

- 简洁的重要性说明
- 带解释的错误代码示例
- 带解释的正确代码示例
- 额外的上下文和参考

## 完整编译文档

查看包含所有规则展开的完整指南：`AGENTS.md`
