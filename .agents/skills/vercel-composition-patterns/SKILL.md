---
name: vercel-composition-patterns
description:
  可扩展的 React 组合模式。在重构带有布尔属性泛滥的组件、构建灵活的组件库或
  设计可复用的 API 时使用。触发于涉及复合组件、渲染属性、上下文提供者或
  组件架构的任务。包含 React 19 API 变更。
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React 组合模式

用于构建灵活、可维护的 React 组件的组合模式。通过使用复合组件、提升状态和
组合内部结构来避免布尔属性泛滥。这些模式使代码库更容易让人类和 AI 代理
在规模化时进行协作。

> **扩展参考：** 本目录中的 [`AGENTS.md`](AGENTS.md) 是长篇上游指南（来自 Vercel）。它是限定于此技能的补充参考资料 — `SKILL.md` 是可加载的入口点和权威来源。它不会覆盖或扩展仓库根目录的 `AGENTS.md` / `AGENT_GUIDE.md`。

## 何时应用

在以下情况下参考这些指南：

- 重构具有许多布尔属性的组件
- 构建可复用的组件库
- 设计灵活的组件 API
- 审查组件架构
- 使用复合组件或上下文提供者

## 按优先级分类的规则类别

| 优先级 | 类别             | 影响   | 前缀             |
| ------ | ---------------- | ------ | ---------------- |
| 1      | 组件架构         | 高     | `architecture-` |
| 2      | 状态管理         | 中等   | `state-`        |
| 3      | 实现模式         | 中等   | `patterns-`     |
| 4      | React 19 API     | 中等   | `react19-`      |

## 快速参考

### 1. 组件架构（高）

- `architecture-avoid-boolean-props` - 不要添加布尔属性来自定义行为；使用组合
- `architecture-compound-components` - 使用共享上下文构建复杂组件

### 2. 状态管理（中等）

- `state-decouple-implementation` - Provider 是唯一知道状态如何管理的地方
- `state-context-interface` - 定义包含 state、actions、meta 的通用接口用于依赖注入
- `state-lift-state` - 将状态移动到 provider 组件中以便兄弟组件访问

### 3. 实现模式（中等）

- `patterns-explicit-variants` - 创建显式变体组件而非布尔模式
- `patterns-children-over-render-props` - 使用 children 进行组合而非 renderX props

### 4. React 19 API（中等）

> **⚠️ 仅 React 19+。** 如果使用 React 18 或更早版本，请跳过此部分。

- `react19-no-forwardref` - 不要使用 `forwardRef`；使用 `use()` 替代 `useContext()`

## 使用方法

阅读各个规则文件以获取详细解释和代码示例：

```
rules/architecture-avoid-boolean-props.md
rules/state-context-interface.md
```

每个规则文件包含：

- 关于为什么重要的简要说明
- 带解释的错误代码示例
- 带解释的正确代码示例
- 额外的上下文和参考

## 完整编译文档

完整指南包含所有规则扩展：`AGENTS.md`
