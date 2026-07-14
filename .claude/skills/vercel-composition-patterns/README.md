# React 组合模式

一个关于可扩展 React 组合模式的结构化知识库。这些
模式通过使用复合组件、状态提升和内部组合，
帮助避免布尔属性泛滥。

## 结构

- `rules/` - 各规则文件（每条规则一个文件）
  - `_sections.md` - 章节元数据（标题、影响、描述）
  - `_template.md` - 创建新规则的模板
  - `area-description.md` - 各规则文件
- `metadata.json` - 文档元数据（版本、组织、摘要）
- **`AGENTS.md`** - 编译输出（自动生成）

## 规则

### 组件架构（关键）

- `architecture-avoid-boolean-props.md` - 不要添加布尔属性来自定义行为
- `architecture-compound-components.md` - 使用共享 context 构建复合组件

### 状态管理（高）

- `state-lift-state.md` - 将状态提升到 Provider 组件中
- `state-context-interface.md` - 定义清晰的 context 接口（state/actions/meta）
- `state-decouple-implementation.md` - 将状态管理与 UI 解耦

### 实现模式（中）

- `patterns-children-over-render-props.md` - 优先使用 children 而非 renderX 属性
- `patterns-explicit-variants.md` - 创建显式的组件变体

## 核心原则

1. **组合优于配置** — 与其添加属性，不如让消费者自行组合
2. **提升你的状态** — 状态在 Provider 中，而非困在组件里
3. **组合你的内部** — 子组件通过 context 而非属性访问
4. **显式变体** — 创建 ThreadComposer、EditComposer，而非带 isThread 的 Composer

## 创建新规则

1. 复制 `rules/_template.md` 到 `rules/area-description.md`
2. 选择适当的前缀：
   - `architecture-` 用于组件架构
   - `state-` 用于状态管理
   - `patterns-` 用于实现模式
3. 填写前置元数据和内容
4. 确保有清晰的示例和说明

## 影响级别

- `关键` - 基础性模式，防止不可维护的代码
- `高` - 显著的可维护性改进
- `中` - 更干净代码的良好实践
