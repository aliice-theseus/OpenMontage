# paper.design 连接器

将 `visual-style.md` 应用于 paper.design 文档。

## 概述

paper.design 是一个用于创建用户界面的专业设计工具。此连接器将 `visual-style.md` 字段映射到 paper.design 文档默认值和 AI 布局指导。

## 字段映射

| visual-style.md 字段 | paper.design 使用方式 |
|-----------------------|-------------------|
| `colors.primary` | 文档调色板（主色）|
| `colors.accent` | 文档调色板（强调色）|
| `colors.neutral` | 文档调色板（中性色）|
| `typography.display.family` | 默认展示字体 |
| `typography.body.family` | 默认正文字体 |
| `typography.caption.family` | 默认说明文字字体 |
| `style_prompt_full` | AI 布局建议提示 |
| `mood.keywords` | 设计方向关键词 |
| `mood.avoid` | 设计约束检查清单 |
| `assets.reference_images` | 风格板参考 |
| `layout.grid` | 画板网格系统 |
| `layout.alignment` | 默认对齐规则 |

## 应用风格

### 1. 设置调色板

创建新画板时，应用风格中的颜色：

```
背景：colors.primary[0].hex
文字：colors.primary[1].hex
强调元素：colors.accent[0].hex
次要元素：colors.neutral[0].hex
```

### 2. 配置排版

加载指定的字体并设置默认值：

```
展示/标题：typography.display.family，typography.display.weight
正文：typography.body.family，typography.body.weight
标签/说明文字：typography.caption.family，typography.caption.weight
```

### 3. 应用布局规则

遵循 `layout.grid` 的画板结构：

- "12 列" → 设置 12 列网格
- "严格的模块化网格" → 启用网格吸附
- "左对齐" → 左对齐所有文本块

### 4. 使用 style_prompt_full 进行 AI 指导

在 paper.design 中使用 AI 功能时，在提示中包含 `style_prompt_full`：

```
创建一个着陆页主角区域。

视觉风格：
[粘贴 style_prompt_full 此处]

约束：
[来自 mood.avoid 的项目]
```

## 示例：应用瑞士风格

给定 `mueller-brockmann-swiss.visual-style.md`：

**颜色设置：**
- 背景：`#000000`（纯黑）
- 文字：`#FFFFFF`（纯白）
- 强调：`#0066FF`（电光蓝）
- 网格线：`#CCCCCC`（网格灰）

**排版：**
- 所有文字：Helvetica 系列
- 标题：Helvetica Bold，大写
- 正文：Helvetica Regular，左对齐
- 说明文字：Helvetica Light，小号，大写

**布局：**
- 12 列模块化网格
- 所有元素对齐到网格
- 无居中文字
- 在正交结构内的大胆对角线构图

**设计约束（来自 mood.avoid）：**
- 无有机或曲线形状
- 无渐变
- 无图库摄影
- 无圆角
- 无装饰元素

## 工作流

1. **读取风格** — 加载 `visual-style.md` 文件
2. **创建画板** — 从 `layout.aspect_ratio` 设置尺寸
3. **应用背景** — 使用 `colors.primary[0].hex`
4. **设置网格** — 遵循 `layout.grid` 规格
5. **配置字体** — 加载 `typography.*` 系列
6. **构建内容** — 遵循 `mood.keywords` 的方向
7. **审查** — 对照 `mood.avoid` 约束检查

## 设计简报格式

在 paper.design 中开始新设计时，从风格生成简报：

```markdown
## 设计简报

**风格：** [name]

**调色板：**
- [colors.primary[0].name]：[hex] — [role]
- [colors.primary[1].name]：[hex] — [role]
- [colors.accent[0].name]：[hex] — [role]

**排版：**
- 展示：[typography.display.family] [weight]
- 正文：[typography.body.family] [weight]

**布局：** [layout.grid]，[layout.alignment]

**氛围：** [mood.keywords 连接]

**避免：** [mood.avoid 连接]
```

## 技巧

- **从网格开始** — 在放置元素前设置 `layout.grid`
- **排版优先** — 让 `typography.rules` 指导层级决策
- **定期检查约束** — 设计时参考 `mood.avoid`
- **使用参考图片** — 如果 `assets.reference_images` 有 URL，导入为风格板
