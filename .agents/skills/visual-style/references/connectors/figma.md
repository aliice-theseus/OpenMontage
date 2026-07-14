# Figma 连接器

将 `visual-style.md` 应用于生成 Figma 样式和组件。

## 概述

此连接器将 `visual-style.md` 字段映射到 Figma 的样式系统：颜色样式、文本样式、效果样式和布局网格。

## 字段映射

| visual-style.md 字段 | Figma 输出 |
|-----------------------|--------------|
| `colors.primary` | 颜色样式（`brand/primary`、`brand/secondary`）|
| `colors.accent` | 颜色样式（`accent/primary`、`accent/secondary`）|
| `colors.neutral` | 颜色样式（`neutral/100`、`neutral/200` 等）|
| `typography.display` | 文本样式（`heading/display`）|
| `typography.body` | 文本样式（`body/default`、`body/large`）|
| `typography.caption` | 文本样式（`label/default`、`label/small`）|
| `typography.rules` | 设计审查检查清单 |
| `layout.grid` | 布局网格预设 |
| `layout.aspect_ratio` | 框架尺寸 |
| `mood.avoid` | 设计审查检查清单 |
| `assets.reference_images` | 样式指南框架 |

## 颜色样式

从 `colors` 对象生成 Figma 颜色样式：

```
文件夹：brand/
  - brand/black         → colors.primary[0].hex
  - brand/white         → colors.primary[1].hex

文件夹：accent/
  - accent/primary      → colors.accent[0].hex
  - accent/secondary    → colors.accent[1].hex（如存在）

文件夹：neutral/
  - neutral/light       → colors.neutral[0].hex
  - neutral/dark        → colors.neutral[1].hex
```

**命名惯例：** 使用 `role` 字段作为样式描述。

## 文本样式

从 `typography` 生成 Figma 文本样式：

```
文件夹：heading/
  - heading/display
    字体：typography.display.family
    字重：typography.display.weight
    大小：48px（或从样式推导）

文件夹：body/
  - body/default
    字体：typography.body.family
    字重：typography.body.weight
    大小：16px

文件夹：label/
  - label/default
    字体：typography.caption.family
    字重：typography.caption.weight
    大小：12px
```

## 布局网格

从 `layout.grid` 生成布局网格预设：

```
"12 列" →
  列数：12
  类型：拉伸
  边距：64px
  间距：24px

"8 点网格" →
  行数：计数
  高度：8px

"严格的模块化网格" →
  同时启用列 AND 行
```

## 样式指南框架

创建记录系统的样式指南框架：

```
┌─────────────────────────────────────────────────────┐
│  [name]                                             │
│  [style_prompt_short]                               │
├─────────────────────────────────────────────────────┤
│  颜色                                               │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                │
│  │████│ │████│ │████│ │████│ │████│                │
│  └────┘ └────┘ └────┘ └────┘ └────┘                │
│  主色    辅助色   强调色   中性色                    │
├─────────────────────────────────────────────────────┤
│  排版                                               │
│                                                     │
│  展示标题                                           │
│  [typography.display.family] [weight]               │
│                                                     │
│  正文字段                                           │
│  [typography.body.family] [weight]                  │
│                                                     │
│  说明文字 / 标签                                    │
│  [typography.caption.family] [weight]               │
├─────────────────────────────────────────────────────┤
│  规则                                               │
│  ✓ [typography.rules[0]]                           │
│  ✓ [typography.rules[1]]                           │
│                                                     │
│  避免                                               │
│  ✗ [mood.avoid[0]]                                 │
│  ✗ [mood.avoid[1]]                                 │
└─────────────────────────────────────────────────────┘
```

## 工作流

1. **读取风格** — 加载 `visual-style.md` 文件
2. **创建颜色样式** — 调色板中每种颜色一个样式
3. **创建文本样式** — 展示、正文和说明文字样式
4. **设置布局网格** — 创建网格预设
5. **构建样式指南框架** — 记录系统
6. **添加参考图片** — 导入 `assets.reference_images`（如可用）

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
  // ... 其他字段
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

## 技巧

- **字体可用性** — 检查 `typography.*.family` 字体在 Figma 中是否可用（Google Fonts 或本地安装）
- **颜色组织** — 使用文件夹按用途对颜色样式进行分组
- **样式描述** — 使用 `role` 字段作为样式描述
- **设计审查** — 从 `typography.rules` 和 `mood.avoid` 创建检查清单
