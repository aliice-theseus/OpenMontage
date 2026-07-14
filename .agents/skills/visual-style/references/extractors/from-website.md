# 从网站提取

从网站 URL 生成 `visual-style.md`。

## 工作流

1. **接收 URL** — 用户提供网站 URL
2. **获取页面** — 使用网页抓取获取 HTML/CSS
3. **截取屏幕截图** — 尽可能视觉捕获页面
4. **分析** — 识别颜色、排版、布局、动效、氛围
5. **生成** — 输出完整的 `visual-style.md`
6. **验证** — 确保所有必填字段存在

## 提取提示

分析网站时使用此提示模板：

```
分析此网站并按规范提取 visual-style.md。

URL：[URL]

识别并输出这些字段：

必填：
- name：此风格的描述性名称（例如 "[品牌] Web 风格"）
- version："1.0"
- style_prompt_short：捕捉视觉精髓的 1-2 句钩子
- style_prompt_full：详细的生成提示，包含具体的：
  - 十六进制颜色代码（使用精确值，不猜测）
  - 字体族名称（检查 CSS）
  - 布局结构（网格系统、间距模式）
  - 动效模式（动画、过渡）
  - 整体氛围和感觉
- colors.primary：至少 2 种颜色，含 name、hex、role

推荐：
- colors.accent：强调色，含 name、hex、role
- colors.neutral：中性/灰色，含 name、hex、role
- typography.display：标题字体族、字重、样式
- typography.body：正文字体族、字重、样式
- typography.caption：说明文字/标签字体族、字重、样式
- typography.rules：排版约束和模式
- layout.grid：网格系统描述
- layout.alignment：对齐模式
- layout.notes：额外布局观察
- motion.transitions：使用的过渡类型
- motion.animation_style：整体动画方式
- mood.keywords：4-6 个氛围/感觉词
- mood.era：设计时代参考
- mood.avoid：要避免的反模式

具体说明：
- 使用 CSS 中的精确十六进制值，不是近似值
- 为每种颜色描述性地命名（不是"蓝色 1"，而是"海洋蓝"）
- 描述每种颜色在系统中的角色
- 注意任何自定义字体及其后备字体

输出格式：
--- 分隔符之间的完整 YAML 前置元数据
加上 Markdown 正文章节（## Design Principles，## Extraction Notes）
```

## 分析检查清单

提取时，查找：

### 颜色
- [ ] 背景色（主要表面）
- [ ] 文字颜色（标题 vs 正文）
- [ ] 强调/行动号召按钮颜色
- [ ] 链接颜色（默认、悬停、已访问）
- [ ] 边框/分割线颜色
- [ ] 渐变使用（如有）

### 排版
- [ ] 标题字体族
- [ ] 正文字体族
- [ ] 使用的字重（细体、常规、粗体等）
- [ ] 文字大小（标题比例）
- [ ] 行高
- [ ] 字距模式
- [ ] 文字变换（大写、小写）

### 布局
- [ ] 最大内容宽度
- [ ] 网格列（如可见）
- [ ] 间距节奏（一致间隙）
- [ ] 对齐模式（左、中、混合）
- [ ] 卡片/组件模式
- [ ] 留白使用

### 动效
- [ ] 页面过渡
- [ ] 悬停效果
- [ ] 滚动动画
- [ ] 加载状态
- [ ] 微交互

### 氛围
- [ ] 整体感觉（专业、俏皮、极简、大胆）
- [ ] 设计时代（现代、复古、永恒）
- [ ] 品牌个性（严肃、友好、技术感）
- [ ] 他们明确避免什么

## 示例输出

给定 URL `https://stripe.com`：

```yaml
---
name: "Stripe 网页风格"
version: "1.0"
tags:
  - 金融科技
  - 极简风格
author: "提取"
source_url: "https://stripe.com"
created: "2026-03-12"

style_prompt_short: >
  干净的金融科技极简主义，白色背景上的深紫色强调。
  宽敞的留白，清晰的排版，微妙的渐变。

style_prompt_full: >
  受 Stripe 启发的现代金融科技设计。干净的白色背景
  配宽敞的留白。深紫色 (#635BFF) 作为主要强调色。
  排版使用自定义几何无衬线字体（类似 Inter 或 Söhne）
  具有清晰的层级。背景中有微妙的网格渐变。
  卡片和按钮使用圆角。平滑、微妙的滚动动画。
  专业、可信、平易近人。无刺眼颜色、无杂乱图案、无图库照片。

colors:
  primary:
    - name: "纯白"
      hex: "#FFFFFF"
      role: "主要背景，留白空间"
    - name: "石板深色"
      hex: "#0A2540"
      role: "主要文字，标题"
  accent:
    - name: "Stripe 紫"
      hex: "#635BFF"
      role: "行动号召、链接、品牌强调"
    - name: "青色强调"
      hex: "#00D4FF"
      role: "次要强调，渐变"
  neutral:
    - name: "石板灰"
      hex: "#425466"
      role: "正文，次要内容"
    - name: "浅灰"
      hex: "#F6F9FC"
      role: "章节背景，卡片"

typography:
  display:
    family: "Söhne, Inter, system-ui"
    weight: "600"
    style: "句首大写，紧凑字距"
  body:
    family: "Söhne, Inter, system-ui"
    weight: "400"
    style: "宽松行高，舒适阅读"
  caption:
    family: "Söhne Mono, monospace"
    weight: "400"
    style: "代码块，技术细节"
  rules:
    - "清晰的大小层级：64px → 48px → 32px → 24px → 16px"
    - "宽行高以确保可读性"
    - "代码和技术内容使用等宽字体"

layout:
  grid: "12 列，最大宽度 1200px"
  alignment: "居中章节，左对齐文字"
  aspect_ratio: "主角区域 16:9，内容多变"
  notes:
    - "章节之间有宽敞的垂直间距"
    - "卡片带有微妙的阴影和圆角"
    - "交替章节背景"

motion:
  transitions:
    - "滚动时的微妙淡入"
    - "平滑的悬停状态过渡（0.2s）"
    - "主角背景的视差效果"
  animation_style: "微妙、平滑、专业。无弹跳或俏皮效果。"
  pacing: "沉稳、自信的过渡"

mood:
  keywords:
    - "专业"
    - "可信"
    - "干净"
    - "现代"
    - "平易近人"
  era: "2020 年代金融科技"
  cultural_reference: "现代 SaaS，开发者导向的设计"
  avoid:
    - "刺眼或霓虹色"
    - "杂乱图案或纹理"
    - "图库摄影"
    - "过于俏皮的动画"
    - "暗色模式（除非要求）"

assets:
  reference_images: []
  color_palette_image:
    url: ""
---

## Design Principles

通过清晰建立信任。每个元素都靠实力赢得位置。排版和留白
承担主要工作。颜色使用克制且有意图。

## Extraction Notes

于 2026-03-12 从 https://stripe.com 提取。
主紫色从行动号召按钮采样。
通过浏览器开发工具识别排版堆栈。
在主角区域注意到网格渐变模式。
```

## 技巧

- **使用开发工具** — 检查元素以获取精确的十六进制值和字体堆栈
- **检查 CSS 变量** — 许多网站在 `:root` 中定义调色板
- **注意响应式模式** — 设计如何适配？
- **捕捉感觉** — `style_prompt_full` 应唤起相同的感觉
- **具体说明避免项** — 该品牌明确不做什么？
