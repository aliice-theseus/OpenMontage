# React 组合模式

一个结构化的可扩展 React 组合模式仓库。这些模式通过使用复合组件、
提升状态和组合内部结构来避免布尔属性泛滥。

## 结构

- `rules/` - 单个规则文件（每条规则一个）
  - `_sections.md` - 章节元数据（标题、影响、描述）
  - `_template.md` - 创建新规则的模板
  - `area-description.md` - 单个规则文件
- `metadata.json` - 文档元数据（版本、组织、摘要）
- **`AGENTS.md`** - 编译输出（已生成）

## 规则

### 组件架构（关键）

- `architecture-avoid-boolean-props.md` - 不要添加布尔属性来自定义行为
- `architecture-compound-components.md` - 使用共享上下文构建复合组件

### 状态管理（高）

- `state-lift-state.md` - 将状态提升到 provider 组件中
- `state-context-interface.md` - 定义清晰的上下文接口（state/actions/meta）
- `state-decouple-implementation.md` - 将状态管理与 UI 解耦

### 实现模式（中等）

- `patterns-children-over-render-props.md` - 优先使用 children 而非 renderX props
- `patterns-explicit-variants.md` - 创建显式组件变体

## 核心原则

1. **组合优于配置** — 与其添加 props，不如让消费者组合
2. **提升你的状态** — 状态在 providers 中，而非困在组件中
3. **组合内部结构** — 子组件访问上下文而非 props
4. **显式变体** — 创建 ThreadComposer、EditComposer，而不是带 isThread 的 Composer

## 创建新规则

1. 将 `rules/_template.md` 复制到 `rules/area-description.md`
2. 选择适当区域前缀：
   - `architecture-` 用于组件架构
   - `state-` 用于状态管理
   - `patterns-` 用于实现模式
3. 填写前置元数据和内容
4. 确保有清晰的示例和解释

## 影响级别

- `CRITICAL` - 基础模式，防止不可维护的代码
- `HIGH` - 显著的可维护性改进
- `MEDIUM` - 更干净代码的良好实践
