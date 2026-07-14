# 从 PDF / 品牌指南提取

从 PDF 品牌指南或样式文档生成 `visual-style.md`。

## 工作流

1. **接收 PDF** — 用户上传品牌指南、样式指南或设计文档
2. **解析章节** — 识别颜色、排版、布局和指南章节
3. **映射到字段** — 将品牌指南规格转换为 visual-style.md 字段
4. **填补空白** — 从结构化数据生成 `style_prompt_full`
5. **输出** — 完整的 `visual-style.md`
6. **验证** — 确保所有必填字段存在

## 常见品牌指南章节

| 品牌指南章节 | 映射到 |
|--------------------|---------|
| 品牌概述 / 使命 | `style_prompt_short`、`mood.keywords` |
| 调色板 | `colors.*` |
| 主色 | `colors.primary` |
| 辅助/强调色 | `colors.accent` |
| 排版 | `typography.*` |
| 标题 | `typography.display` |
| 正文 | `typography.body` |
| 网格系统 | `layout.grid` |
| 间距 | `layout.notes` |
| 应做与不应做 | `typography.rules`、`mood.avoid` |
| 语气与语调 | `mood.keywords`、`style_prompt_full` |
| 摄影风格 | `mood.keywords`、`mood.avoid` |
| 图标设计 | `style_prompt_full` |

## 提取提示

解析品牌指南 PDF 时使用此提示：

```
解析此品牌指南 PDF 并生成 visual-style.md。

将品牌指南章节映射到 visual-style.md 字段：

必填：
- name：品牌名称 + "品牌风格"
- version："1.0"
- style_prompt_short：从品牌概述/使命综合
- style_prompt_full：将所有视觉规格组合成连贯的
  生成提示。包括具体的十六进制码、字体名称、间距
  值和设计原则。
- colors.primary：来自"主色"章节

来自颜色章节：
- colors.primary：主调色板（将所有颜色规格转换为十六进制）
- colors.accent：辅助/强调色
- colors.neutral：灰色、背景、辅助色

来自排版章节：
- typography.display：标题字体规格
- typography.body：正文字体规格
- typography.caption：说明文字/标签规格（如已定义）
- typography.rules：任何排版指南或限制

来自布局章节：
- layout.grid：网格系统规格
- layout.alignment：对齐规则
- layout.notes：间距、边距、填充指南

来自指南章节：
- mood.keywords：从语气/语调/个性章节提取
- mood.avoid：从"不应做"列表、错误使用示例提取

精确：
- 将所有颜色规格转换为十六进制（RGB、CMYK、Pantone → hex）
- 使用指定的精确字体族名称
- 包括给出的具体测量值
- 在 style_prompt_full 中保留品牌声明的价值观

输出格式：
--- 分隔符之间的完整 YAML 前置元数据
加上 Markdown 正文章节（## Design Principles 来自品牌哲学）
```

## 颜色转换参考

品牌指南通常以多种格式指定颜色：

| 格式 | 示例 | 十六进制转换 |
|--------|---------|----------------|
| Hex | #FF5500 | 直接使用 |
| RGB | 255, 85, 0 | → #FF5500 |
| CMYK | 0, 67, 100, 0 | 近似为十六进制 |
| Pantone | PMS 021 C | 查找对应的十六进制 |
| HSL | 20°, 100%, 50% | 转换为十六进制 |

对于 Pantone 颜色，使用官方的 Pantone 到十六进制映射或在 `role` 字段中注明 Pantone 代码。

## 示例输出

给定公司品牌指南 PDF：

```yaml
---
name: "Acme Corp 品牌风格"
version: "1.0"
tags:
  - 企业
  - 科技
author: "从 Acme 品牌指南 v2.3 提取"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  专业科技品牌，大胆的蓝色强调。
  干净、可信、前瞻性思维。

style_prompt_full: >
  Acme Corp 品牌风格。专业科技公司美学。
  主蓝色 (#0052CC) 用于品牌元素、行动号召和强调。
  深蓝 (#172B4D) 用于标题和高对比度文字。干净的白色
  (#FFFFFF) 背景配宽敞留白。中性灰色
  用于辅助内容。排版使用 Roboto 用于数字
  和 Avenir 用于印刷 — 传达精度的干净几何无衬线字体。
  8 点间距网格。交互元素圆角 (4px)。
  摄影应真实、多样且乐观 — 无图库照片陈词滥调。
  图标为线框风格，2px 描边，圆角端点。
  专业但平易近人。绝不企业式古板或过于俏皮。

colors:
  primary:
    - name: "Acme 蓝"
      hex: "#0052CC"
      role: "主要品牌色，行动号召，链接"
    - name: "深蓝"
      hex: "#172B4D"
      role: "标题，高对比度文字"
  accent:
    - name: "成功绿"
      hex: "#36B37E"
      role: "正面状态，确认"
    - name: "警告黄"
      hex: "#FFAB00"
      role: "警告，注意"
    - name: "错误红"
      hex: "#DE350B"
      role: "错误，破坏性操作"
  neutral:
    - name: "白色"
      hex: "#FFFFFF"
      role: "主要背景"
    - name: "浅灰"
      hex: "#F4F5F7"
      role: "次要背景，卡片"
    - name: "中灰"
      hex: "#6B778C"
      role: "次要文字，占位符"
    - name: "深灰"
      hex: "#42526E"
      role: "正文"

typography:
  display:
    family: "Roboto"
    weight: "700"
    style: "句首大写，-0.02em 字距"
  body:
    family: "Roboto"
    weight: "400"
    style: "16px 基础，1.5 行高"
  caption:
    family: "Roboto"
    weight: "500"
    style: "12px，标签大写"
  rules:
    - "所有数字应用使用 Roboto"
    - "印刷材料使用 Avenir"
    - "最小正文字号：14px"
    - "最大行长：75 个字符"
    - "使用 Medium (500) 字重表示强调，而非 bold"

layout:
  grid: "8 点网格，12 列"
  alignment: "左对齐文字，居中主角内容"
  aspect_ratio: "演示文稿 16:9"
  notes:
    - "最小边距：24px（移动端），48px（桌面端）"
    - "标准间距：8, 16, 24, 32, 48, 64px"
    - "卡片边框圆角：4px"
    - "按钮边框圆角：4px"

motion:
  transitions:
    - "ease-out，200ms 微交互"
    - "ease-in-out，300ms 页面过渡"
  animation_style: "微妙、有目的。动画应阐明，而非装饰。"
  pacing: "快速、响应式反馈"

mood:
  keywords:
    - "专业"
    - "可信"
    - "创新"
    - "平易近人"
    - "精确"
  era: "当代科技（2020 年代）"
  cultural_reference: "企业 SaaS，开发者工具"
  avoid:
    - "过于俏皮或随意的语气"
    - "通用图库摄影"
    - "品牌元素上的渐变"
    - "一个构图中超过 3 种颜色"
    - "居中正文"
    - "全大写正文"
    - "深度超过 2px 的投影"

assets:
  reference_images: []
  color_palette_image:
    url: ""
---

## Design Principles

来自 Acme 品牌指南：

1. **清晰胜过机巧** — 沟通应立即可理解
2. **一致性建立信任** — 每个接触点强化品牌
3. **有目的的克制** — 只添加增加价值的内容
4. **默认可访问** — 为所有人设计

## Extraction Notes

从"Acme 品牌指南 v2.3"（PDF，48 页）提取。
颜色值从 Pantone 规格转换。
排版从"数字标准"章节映射。
应做与不应做综合到 mood.avoid 列表中。
```

## 技巧

- **优先精确** — 品牌指南是精确的；保留精确值
- **不要发明** — 如果 PDF 中没有某个章节，保持字段为空
- **综合 style_prompt_full** — 读起来应像给设计师的简报
- **捕获不应做的内容** — `mood.avoid` 通常在品牌指南中明确说明
- **注明来源** — 在提取说明中包括页码或章节名称
