---
name: beautiful-mermaid
description: 使用 Beautiful Mermaid 库将 Mermaid 图表渲染为 SVG 和 PNG。当用户要求渲染 Mermaid 图表时使用。
---

# Beautiful Mermaid 图表渲染

使用 Beautiful Mermaid 库将 Mermaid 图表渲染为 SVG 和 PNG 图片。

## 依赖

此技能需要 `agent-browser` 技能进行 PNG 渲染。在进行 PNG 截图前，先加载该技能。

## 支持的图表类型

- **流程图** - 流程处理、决策树、CI/CD 管道
- **时序图** - API 调用、OAuth 流程、数据库事务
- **状态图** - 状态机、连接生命周期
- **类图** - UML 类图、设计模式
- **实体关系图** - 数据库模式、数据模型

## 可用主题

Default、Dracula、Solarized、Zinc Dark、Tokyo Night、Tokyo Night Storm、Tokyo Night Light、Catppuccin Latte、Nord、Nord Light、GitHub Dark、GitHub Light、One Dark。

如果未指定主题，使用 `default`。

## 常见语法模式

### 流程图边标签

使用管道语法表示边标签：

```mermaid
A -->|label| B
A ---|label| B
```

避免使用空格-破折号语法，可能导致渲染不完整：

```mermaid
A -- label --> B   # 可能导致问题
```

### 含特殊字符的节点标签

将包含特殊字符的标签用引号包裹：

```mermaid
A["Label with (parens)"]
B["Label with / slash"]
```

## 工作流程

### 步骤 1：生成或验证 Mermaid 代码

如果用户提供的是描述而非代码，生成有效的 Mermaid 语法。查阅 `references/mermaid-syntax.md` 获取完整语法详情。

### 步骤 2：渲染 SVG

运行渲染脚本生成 SVG 文件：

```bash
bun run scripts/render.ts --code "graph TD; A-->B" --output diagram --theme default
```

或从文件渲染：

```bash
bun run scripts/render.ts --input diagram.mmd --output diagram --theme tokyo-night
```

替代运行时：
```bash
npx tsx scripts/render.ts --code "..." --output diagram
deno run --allow-read --allow-write --allow-net scripts/render.ts --code "..." --output diagram
```

这将在当前工作目录生成 `<output>.svg`。

### 步骤 3：创建 HTML 包装器

运行 HTML 包装器脚本准备截图：

```bash
bun run scripts/create-html.ts --svg diagram.svg --output diagram.html
```

这将创建一个展示 SVG 并带有适当内边距和背景的最小 HTML 文件。

### 步骤 4：使用 agent-browser 捕获高分辨率 PNG

使用 agent-browser CLI 捕获高质量截图。有关完整 CLI 文档，请参阅 `agent-browser` 技能。

```bash
# 设置 4K 视口以进行高分辨率捕获
agent-browser set viewport 3840 2160

# 打开 HTML 包装器
agent-browser open "file://$(pwd)/diagram.html"

# 等待渲染完成
agent-browser wait 1000

# 捕获整页截图
agent-browser screenshot --full diagram.png

# 关闭浏览器
agent-browser close
```

对于复杂图表需要更高分辨率，可进一步增加视口或在创建 HTML 包装器时使用 `--padding` 选项为图表提供更多空间。

### 步骤 5：清理中间文件

渲染完成后，删除所有中间文件。仅保留最终的 `.svg` 和 `.png`。

需要清理的文件：
- HTML 包装器文件（如 `diagram.html`）
- 任何用于保存图表代码的临时 `.mmd` 文件
- 渲染过程中创建的任何其他文件

```bash
rm diagram.html
```

如果创建了临时 `.mmd` 文件，也要删除它。

## 输出

始终生成两种输出：
- **SVG**：矢量格式，可无限缩放，文件大小小
- **PNG**：高分辨率光栅图，在 4K（3840×2160）视口下捕获，图表宽度至少 1200px

除非用户明确指定不同路径，否则文件保存到当前工作目录。

## 主题选择指南

| 主题 | 背景 | 最佳用途 |
|-------|------------|----------|
| default | 浅灰色 | 通用 |
| dracula | 深紫色 | 深色模式偏好 |
| tokyo-night | 深蓝色 | 现代深色美学 |
| tokyo-night-storm | 深蓝色 | 更高对比度 |
| nord | 深北极色 | 柔和、平静的视觉效果 |
| nord-light | 浅北极色 | 柔和色调的浅色模式 |
| github-dark | GitHub 深色 | 匹配 GitHub UI |
| github-light | GitHub 浅色 | 匹配 GitHub UI |
| catppuccin-latte | 暖浅色 | 柔和粉彩美学 |
| solarized | 棕褐色 | Solarized 配色方案 |
| one-dark | Atom 深色 | Atom 编辑器美学 |
| zinc-dark | 中性深色 | 极简，无颜色倾向 |

## 故障排除

### 主题未应用

检查渲染脚本输出中的 `bg` 和 `fg` 值，或检查 SVG 开头标签中是否有 `--bg` 和 `--fg` CSS 自定义属性。

### 图表显示截断或不完整

- 检查边标签语法 — 使用 `-->|label|` 管道符号，而非 `-- label -->`
- 验证所有节点 ID 是否唯一
- 检查节点标签中是否有未闭合的括号

### 渲染输出空或损坏的 SVG

- 渲染前在 https://mermaid.live 验证 Mermaid 语法
- 检查需要转义的特殊字符（用引号包裹）
- 确保指定了流程图方向（`graph TD`、`graph LR` 等）
