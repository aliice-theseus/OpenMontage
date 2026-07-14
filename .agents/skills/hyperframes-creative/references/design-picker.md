# 设计选择器

两阶段视觉选择器：先看情绪板（选择一个完整方向），然后微调各个类别。

## 目录

- 前置条件
- 构建选择器
- 服务和用户选择

## 前置条件

在生成选项前阅读——它们定义了你的选项必须遵循的规则：

- `references/typography.md`
- `house-style.md`
- `references/video-composition.md`
- `visual-styles.md`
- `references/beat-direction.md`

## 构建选择器

1. 生成**深度上下文相关于用户提示的**选项。每个类别——不仅仅是架构——必须反映特定的产品、品牌、受众和情绪。可能出现在任何选择器上的通用选项是失败的。

   **情绪板** — 创意空间允许的范围内尽可能多（4-8个）。每个板必须讲述关于品牌的一个不同故事，而不仅仅是重新排列相同的元素。问："有哪些真正不同的方式来定位这个产品？"一个猫粮品牌可能是：俏皮混乱、高端定位、舒适温馨、社交原生、口味展示、幽默主导、感官/开胃。每个都是不同的叙事，而不是在同一布局上使用不同的字体。

   **架构** — 每个情绪板至少一个，每个视觉上独特。使用 `{{prompt_headline}}` 和 `{{prompt_sub}}` 令牌。如果用户提供了媒体资源，将其用作背景图片（使用不带引号的 `url(path)` —— `style='...'` 内部的单引号会破坏属性）。

   **调色板**（5-6个）— 以品牌的世界命名，而不是通用情绪。调色板名称和颜色应感觉属于这个特定的产品。始终混合深色 + 浅色 + 色调。**每个调色板在色板尺寸下必须视觉上不同。** 如果两个调色板共享相同的背景亮度**和**相似的强调色调，去掉一个。测试：用户能在 14px 色板中看出区别吗？如果不能，它们是重复的。

   **字体搭配**（5-6对）— **在生成搭配前运行 typography.md 中的字体发现脚本。** 这不是可选的。下载 Google Fonts 元数据，运行脚本，从其输出中选择。否则你每次都会选择相同的 8 种字体（Bricolage Grotesque、Instrument Serif、Fraunces、Archivo Black、DM Serif Display、Space Grotesk、Fredoka）——那是你的训练数据默认值，不是上下文相关的选择。匹配品牌的能量和受众。根据 typography.md 跨类别搭配（永远不要两种无衬线体）。

2. `mkdir -p .hyperframes` 然后将 [../templates/design-picker.html](../templates/design-picker.html) 复制到 `.hyperframes/pick-design.html`。
3. 使用 Python 替换这些占位符（不要在 sed 中手动转义引号）：
   - `__ARCHITECTURES_JSON__` — 架构对象数组
   - `__PALETTES_JSON__` — 调色板对象数组
   - `__TYPEPAIRS_JSON__` — 字体搭配对象数组
   - `__MOODBOARDS_JSON__` — 情绪板对象数组（格式见下方）
   - `__PROMPT_JSON__` — 包含提示上下文的对象（格式见下方）

### 架构数据格式

每个架构对象必须包含一个 `preview_html` 字段——在预览面板中渲染的 HTML。使用模板在运行时替换的令牌占位符：`{{bg}}`、`{{fg}}`、`{{ac}}`、`{{mt}}`、`{{hf}}`、`{{hw}}`、`{{bf}}`、`{{bw}}`、`{{cr}}`（圆角半径）、`{{pad}}`、`{{gap}}`、`{{shadow}}`、`{{g}}`（网格线颜色）、`{{fg3}}`/`{{fg6}}`/`{{fg8}}`/`{{fg15}}`（不透明度下的 fg）、`{{ac3}}`/`{{ac5}}`/`{{ac25}}`（不透明度下的强调色）。

**每个令牌都必须被使用。** 将 `{{cr}}` 应用于所有卡片、按钮和容器。将 `{{shadow}}` 应用于抬升元素（卡片、按钮、代码块）。将 `{{pad}}` 和 `{{gap}}` 用于控制间距。如果令牌未在 preview_html 中使用，该选项将没有可见效果。

**密度很重要。** 每个架构预览必须包含 15 个以上不同的元素，以给用户真实的布局感受。包括：标题、副标题、正文段落、标签/顶线、带数字的统计、次要统计、引用/推荐、署名、带标题+正文的卡片、第二张卡片（不同处理）、代码/命令块、主要按钮、次要按钮、列表或标签、强调分割线/标尺，以及数据元素（表格行、进度条或图表）。

可选包含 `components`（组件样式规则）和 `dos`（该做与不该做）作为字符串——它们出现在生成的 design.md 中。

**布局约束：** 所有预览 HTML 必须使用百分比宽度或 `max-width: 100%`。在所有 flex 行上使用 `flex-wrap: wrap`。绝对定位的装饰元素必须保持在带有 `overflow: hidden` 的父元素内。

**安全：** 架构 `preview_html` 不能包含 `<script>` 标签、事件处理器（`onclick`、`onerror` 等）或 `javascript:` URL。它通过 `innerHTML` 注入。

**图片 URL：** 在 `preview_html` 中使用背景图片时，使用不带引号的 `url(path/to/image.jpg)`。像 `url('path.jpg')` 这样的单引号会出问题，因为 `preview_html` 位于 `style='...'` 属性内部——内部的单引号会终止外部属性。

**调色板多样性：** 始终在 6 个调色板中混合浅色、深色和色调背景——即使对于平静/健康提示也是如此。

### 示例架构对象

```json
{
  "name": "Editorial Stack",
  "description": "Vertical rhythm with large type, pull quotes, and data callouts",
  "tag": "editorial / longform / narrative",
  "mood": "Confident, unhurried, typographically driven",
  "preview_html": "<div style='background:{{bg}};color:{{fg}};padding:{{pad}};min-height:100vh;font-family:\"{{bf}}\",sans-serif;font-weight:{{bw}};'><div style='max-width:100%;display:flex;flex-direction:column;gap:{{gap}};'><div style='font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:{{mt}};'>Overline Label</div><div style='font-family:\"{{hf}}\",serif;font-weight:{{hw}};font-size:48px;line-height:1.1;letter-spacing:-0.02em;'>The Headline Goes Here</div><div style='font-size:20px;color:{{mt}};max-width:70%;line-height:1.5;'>Subheading text that introduces the narrative arc of this composition with enough words to fill two lines.</div><div style='font-size:15px;line-height:1.7;color:{{fg}};max-width:65%;'>Body paragraph with real sentences. The quick brown fox jumps over the lazy dog. This gives a sense of text density and reading rhythm at the chosen type size.</div><div style='display:flex;gap:{{gap}};flex-wrap:wrap;'><div style='background:{{fg6}};border-radius:{{cr}};padding:{{pad}};flex:1;min-width:200px;box-shadow:{{shadow}};'><div style='font-size:36px;font-family:\"{{hf}}\",serif;font-weight:{{hw}};color:{{ac}};'>2.4M</div><div style='font-size:12px;color:{{mt}};margin-top:4px;'>Primary Stat</div></div><div style='background:{{fg6}};border-radius:{{cr}};padding:{{pad}};flex:1;min-width:200px;box-shadow:{{shadow}};'><div style='font-size:36px;font-family:\"{{hf}}\",serif;font-weight:{{hw}};color:{{fg}};'>87%</div><div style='font-size:12px;color:{{mt}};margin-top:4px;'>Secondary Stat</div></div></div><div style='border-left:3px solid {{ac}};padding:12px {{pad}};background:{{ac3}};border-radius:0 {{cr}} {{cr}} 0;'><div style='font-size:18px;font-style:italic;color:{{fg}};line-height:1.5;'>\"A pull quote that captures the key insight of the piece.\"</div><div style='font-size:12px;color:{{mt}};margin-top:8px;'>— Attribution Name</div></div><div style='background:{{fg3}};border-radius:{{cr}};padding:{{pad}};box-shadow:{{shadow}};'><div style=... (行被截断到 2000 字符)
}
```

### 情绪板数据格式

每个情绪板从每个类别中预选一个选项。用户在阶段 1 中选择情绪板，然后在阶段 2 中微调，这些选择已预填。

```json
{
  "name": "Terminal Precision",
  "description": "Code-forward, data-dense, CLI energy. Dark canvas, monospace body, sharp corners.",
  "theme": "dark",
  "arch_index": 0,
  "palette_index": 0,
  "type_index": 0,
  "corners_index": 0,
  "density_index": 0,
  "depth_index": 1,
  "easing_index": 0,
  "corners": "0px",
  "padding": "12px",
  "gap": "8px",
  "shadow": "0 2px 16px rgba(0,230,255,0.15)"
}
```

索引引用到 ARCHITECTURES、PALETTES 和 TYPEPAIRS 数组中。模板使用其架构的 `preview_html` 渲染每个情绪板的迷你预览，并应用情绪板的调色板/字体。

### 提示上下文数据格式

```json
{
  "title": "AI Coding Assistant",
  "headline": "Your Code, Understood.",
  "subline": "An AI coding assistant that reads your entire codebase.",
  "section_desc": "Layout options for your product launch"
}
```

`title` 出现在阶段 1 的标题中。`headline` 和 `subline` 替换架构 preview_html 中的 `{{prompt_headline}}` 和 `{{prompt_sub}}`，使预览显示真实内容。

### preview_html 中的内容令牌

除了标准设计令牌（`{{bg}}`、`{{fg}}`、`{{ac}}` 等），架构 `preview_html` 可以使用：

- `{{prompt_headline}}` — 用户的真实标题文本
- `{{prompt_sub}}` — 用户的真实副标题文本

这使得预览具有上下文——用户看到自己的内容被样式化，而不是通用占位符。

## 服务和用户选择

4. 提供文件服务：`cd <project-dir> && python3 -m http.server 8723 &`（使用端口 8723 或任何高于 8000 的未用端口；如果 curl 检查失败，尝试下一个端口）。验证：`curl -s -o /dev/null -w "%{http_code}" http://localhost:8723/.hyperframes/pick-design.html` ——只有在返回 200 时才分享链接。不要为选择器使用 `npx hyperframes preview` ——它会阻塞。仅从主对话线程启动 HTTP 服务器。如果你作为分派的任务或子代理运行，返回文件路径让调用者提供服务。
5. 用户选择后，告诉他们："从选择器中复制 design.md 并粘贴到这里。"用户将 markdown 粘贴回对话。逐字保存到项目根目录的 `design.md` ——它已经是规范格式（YAML frontmatter + 散文段落）。用户粘贴后，杀死后台服务器：`kill %1` 或 `kill $(lsof -ti:8723)`。然后继续构建。

选择器输出一个符合 [google-labs-code/design.md](https://github.com/google-labs-code/design.md) 规范的文件：包含 `colors`、`typography`、`rounded` 和 `spacing` 令牌的 YAML frontmatter，后跟 `## Overview`、`## Colors`、`## Typography`、`## Layout`、`## Elevation`、`## Components` 和 `## Do's and Don'ts` 散文段落。
