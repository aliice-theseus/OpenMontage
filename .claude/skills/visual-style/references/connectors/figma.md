# Figma 连接器

将 `visual-style.md` 应用于生成 Figma 样式和组件。

## 概述

此连接器将 `visual-style.md` 字段映射到 Figma 的样式系统：颜色样式、文本样式、效果样式和布局网格。

## 字段映射

| visual-style.md 字段 | Figma 输出 |
|----------------------|-----------|
| `colors.primary` | 颜色样式（`brand/primary`、`brand/secondary`） |
| `colors.accent` | 颜色样式（`accent/primary`、`accent/secondary`） |
| `colors.neutral` | 颜色样式（`neutral/100`、`neutral/200` 等） |
| `typography.display` | 文本样式（`heading/display`） |
| `typography.body` | 文本样式（`body/default`、`body/large`） |
| `typography.caption` | 文本样式（`label/default`、`label/small`） |
| `typography.rules` | 设计审查检查清单 |
| `layout.grid` | 布局网格预设 |
| `layout.aspect_ratio` | 框架尺寸 |
| `mood.avoid` | 设计审查检查清单 |
| `assets.reference_images` | 风格指南框架 |

## 颜色样式

从 `colors` 对象生成 Figma 颜色样式：

```
Folder: brand/
  - brand/black         → colors.primary[0].hex
  - brand/white         → colors.primary[1].hex

Folder: accent/
  - accent/primary      → colors.accent[0].hex
  - accent/secondary    → colors.accent[1].hex (if exists)

Folder: neutral/
  - neutral/light       → colors.neutral[0].hex
  - neutral/dark        → colors.neutral[1].hex
```

**命名约定：** 使用 `role` 字段作为样式描述。

## 文本样式

从 `typography` 生成 Figma 文本样式：

```
Folder: heading/
  - heading/display
    Font: typography.display.family
    Weight: typography.display.weight
    Size: 48px (or derive from style)

Folder: body/
  - body/default
    Font: typography.body.family
    Weight: typography.body.weight
    Size: 16px

Folder: label/
  - label/default
    Font: typography.caption.family
    Weight: typography.caption.weight
    Size: 12px
```

## 布局网格

从 `layout.grid` 生成布局网格预设：

```
"12 columns" →
  Columns: 12
  Type: Stretch
  Margin: 64px
  Gutter: 24px

"8-point grid" →
  Rows: Count
  Height: 8px

"Strict modular grid" →
  Both columns AND rows enabled
```

## 风格指南框架

创建一个记录系统的风格指南框架：

```
┌─────────────────────────────────────────────────────┐
│  [name]                                             │
│  [style_prompt_short]                               │
├─────────────────────────────────────────────────────┤
│  COLORS                                             │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                │
│  │████│ │████│ │████│ │████│ │████│                │
│  └────┘ └────┘ └────┘ └────┘ └────┘                │
│  Primary  Secondary  Accent   Neutral              │
├─────────────────────────────────────────────────────┤
│  TYPOGRAPHY                                         │
│                                                     │
│  Display Heading                                    │
│  [typography.display.family] [weight]               │
│                                                     │
│  Body text paragraph                                │
│  [typography.body.family] [weight]                  │
│                                                     │
│  CAPTION / LABEL                                    │
│  [typography.caption.family] [weight]               │
├─────────────────────────────────────────────────────┤
│  RULES                                              │
│  ✓ [typography.rules[0]]                           │
│  ✓ [typography.rules[1]]                           │
│                                                     │
│  AVOID                                              │
│  ✗ [mood.avoid[0]]                                 │
│  ✗ [mood.avoid[1]]                                 │
└─────────────────────────────────────────────────────┘
```

## 工作流程

1. **读取风格** — 加载 `visual-style.md` 文件
2. **创建颜色样式** — 调色板中每种颜色一个样式
3. **创建文本样式** — 展示、正文和说明样式
4. **设置布局网格** — 创建网格预设
5. **构建风格指南框架** — 记录系统
6. **添加参考图片** — 如有，导入 `assets.reference_images`

## Figma 插件集成

如果构建读取 `visual-style.md` 的 Figma 插件：

```typescript
interface VisualStyle {
  name: string;
  version: string;
  style_prompt_short: string;
  style_prompt_full: string;
  colors: {
    primary: Color[];
    accent?: Color[];
    neutral?: Color[];
  };
  typography: {
    display: TypographyStyle;
    body: TypographyStyle;
    caption: TypographyStyle;
    rules?: string[];
  };
  // ... other fields
}

interface Color {
  name: string;
  hex: string;
  role: string;
}

interface TypographyStyle {
  family: string;
  weight: string;
  style?: string;
}
```

## 提示

- **字体可用性** — 检查 `typography.*.family` 字体在 Figma 中是否可用（Google Fonts 或本地安装）
- **颜色组织** — 使用文件夹按用途分组颜色样式
- **样式描述** — 使用 `role` 字段作为样式描述
- **设计审查** — 从 `typography.rules` 和 `mood.avoid` 创建检查清单
