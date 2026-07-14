---
name: visual-style
description: |
  通过 visual-style.md 文件创建、提取和应用可移植的视觉设计系统。用于：(1) 从头创建 visual-style.md 设计系统，(2) 从网站 URL、视频或 PDF 品牌指南提取视觉风格，(3) 将视觉风格应用于 HeyGen 视频、HTML 幻灯片、Figma 或 paper.design，(4) 浏览预构建视觉风格库（瑞士风格、Saul Bass、Game Boy 等），(5) 用户提到"视觉风格"、"设计系统"、"品牌风格"或"风格指南"，(6) 使用一致的设计语言为 HeyGen 视频设置样式。
---

# 视觉风格

创建、提取和应用可移植的视觉设计系统。一个 `visual-style.md` 文件在一个文件中定义颜色、排版、布局、动态和氛围，任何 AI 工具都可以使用。

## 快速参考

| 模式 | 触发条件 | 功能 |
|------|---------|--------------|
| **创建** | "创建一个 visual-style.md..." | 通过引导式提示从头构建风格 |
| **提取** | "从 [URL/图片/视频] 提取 visual-style.md" | 分析来源并生成风格文件 |
| **应用** | "将此 visual-style.md 应用于 [工具]" | 使用特定连接器应用风格 |
| **图库** | "显示可用的视觉风格" | 浏览和使用示例风格 |

## 默认工作流

### 创建

1. **收集氛围** — 询问氛围、时代、参考、灵感
2. **定义颜色** — 主色（2+）、强调色、中性色，包含十六进制值和角色
3. **设置排版** — 展示、正文、说明文字系列 + 字重/样式规则
4. **布局与动效** — 网格系统、过渡、节奏
5. **生成** — 使用 [references/templates/minimal.visual-style.md](references/templates/minimal.visual-style.md) 或 [references/templates/full.visual-style.md](references/templates/full.visual-style.md) 输出完整的 `visual-style.md`
6. **预览** — 显示一个小型 HTML 色板或描述视觉效果
7. **可选应用** — 询问用户是否要使用连接器

要批量询问的问题：
1. 氛围如何？（氛围关键词、时代、参考）
2. 有任何特定颜色吗？（或从氛围推导？）
3. 排版偏好？（干净、编辑感、技术感、俏皮感？）
4. 您将将此用于什么工具？（HeyGen、幻灯片、paper.design、Figma？）

### 提取

1. **接收来源** — URL、图片、视频或 PDF
2. **加载提取器** — 读取相应的提取器参考文件
3. **分析** — 识别颜色、排版、布局、动效、氛围
4. **生成** — 输出完整的 `visual-style.md`，设置 `source_url`
5. **验证** — 确保所有必填字段存在

### 应用

1. **读取风格** — 加载 `visual-style.md` 文件
2. **询问使用哪个连接器** — 或从上下文检测
3. **加载连接器** — 读取相应的连接器参考文件
4. **转换** — 将风格字段映射到工具特定格式
5. **生成输出** — 生成工具就绪的指令或代码

### 图库

1. **列出风格** — 显示 [references/gallery/](references/gallery/) 中的可用风格
2. **预览** — 描述所选风格的视觉特征
3. **加载** — 读取完整的 `visual-style.md`
4. **应用** — 与连接器一起使用

## 格式快速参考

### 必填字段

```yaml
name: "Style Name"
version: "1.0"
style_prompt_short: "1-2 句电梯演讲"
style_prompt_full: "详细的生成提示 — 最重要的字段"
colors:
  primary:
    - name: "Color Name"
      hex: "#000000"
      role: "how this color is used"
```

**`style_prompt_full` 是核心。** 如果一个工具只能读取一个字段，它会读取这个。其他所有内容是为需要更精细控制的工具提供的结构化数据。

完整规范： [references/spec.md](references/spec.md)

## 参考文件

### 连接器（应用模式）

| 连接器 | 使用场景 | 文件 |
|-----------|----------|------|
| HeyGen Video Agent | AI 视频生成 | [references/connectors/heygen-video-agent.md](references/connectors/heygen-video-agent.md) |
| HTML Slides | 网页演示 | [references/connectors/html-slides.md](references/connectors/html-slides.md) |
| paper.design | 设计文档 | [references/connectors/paper-design.md](references/connectors/paper-design.md) |
| Figma | 设计工具样式 | [references/connectors/figma.md](references/connectors/figma.md) |

### 提取器（提取模式）

| 来源 | 文件 |
|--------|------|
| 网站 URL | [references/extractors/from-website.md](references/extractors/from-website.md) |
| 视频关键帧 | [references/extractors/from-video.md](references/extractors/from-video.md) |
| PDF / 品牌指南 | [references/extractors/from-pdf.md](references/extractors/from-pdf.md) |

### 图库（预构建风格）

| 风格 | 时代 | 文件 |
|-------|-----|------|
| Müller-Brockmann 瑞士风格 | 1950–70 年代 | [references/gallery/mueller-brockmann-swiss.visual-style.md](references/gallery/mueller-brockmann-swiss.visual-style.md) |
| Neville Brody 工业风格 | 1980 年代末–90 年代 | [references/gallery/neville-brody-industrial.visual-style.md](references/gallery/neville-brody-industrial.visual-style.md) |
| Saul Bass 电影风格 | 1950–60 年代 | [references/gallery/saul-bass-cinematic.visual-style.md](references/gallery/saul-bass-cinematic.visual-style.md) |
| Game Boy Color | 1998–2003 | [references/gallery/game-boy-color.visual-style.md](references/gallery/game-boy-color.visual-style.md) |
| HeyGen AI 视频 | 2020 年代 | [references/gallery/heygen-ai-video.visual-style.md](references/gallery/heygen-ai-video.visual-style.md) |

### 模板与规范

- [references/templates/minimal.visual-style.md](references/templates/minimal.visual-style.md) — 最简模板
- [references/templates/full.visual-style.md](references/templates/full.visual-style.md) — 完整模板（含所有字段）
- [references/spec.md](references/spec.md) — 完整格式规范

## 最佳实践

1. **`style_prompt_full` 是核心** — 始终可作为独立的生成提示使用
2. **一种风格，一个文件** — 不捆绑多种风格
3. **资产使用 URL** — 绝不嵌入二进制数据
4. **展示，而非陈述** — 创建风格时生成预览
5. **有主见的默认值，灵活的扩展** — 核心模式固定；`x_*` 用于工具特定配置
