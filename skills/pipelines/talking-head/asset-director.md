# 资产导演 —  Talking Head 流水线

## 使用时机

你已获得场景计划和脚本。你的任务是生成 talking-head 视频的辅助资产：字幕、提取的音频、叠加图形（图表、文字卡片、统计揭示）以及任何补充性视觉内容。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/asset_manifest.schema.json` | 产物校验 |
| 前置产物 | 场景计划、脚本 | 需要创建哪些资产 |
| 工具 | `subtitle_gen`、`audio_mixer` | 字幕和音频生成 |
| 工具 | `image_selector`（可选） | 叠加层用库存图片 |
| 工具 | `pixabay_music`（可选） | 免版税背景音乐 |

## 流程

### 步骤 0: 主角场景采样（必做）

在批量资产生成之前：
1. 确定主角场景（视频的视觉高潮点）
2. 为该场景生成**一个**样本资产（字幕风格、叠加层或背景）
3. 展示给用户："这是最重要场景的视觉方向。是否符合你的想象？我将按此风格生成其余部分。"
4. 在继续批量生成之前等待批准

这可以防止最昂贵的错误：以用户不喜欢的风格生成 10+ 个资产。

### 步骤 1: 生成字幕

使用脚本阶段的转录数据创建：
- 带字级时序的 SRT 或 ASS 字幕文件
- 根据剧本设置字幕样式（字体、大小、颜色、位置）

如果场景计划包含 `corrections` 字典，将其传递给 `subtitle_gen`：
```
subtitle_gen.execute({
    "segments": <transcript_segments>,
    "corrections": {"cloud": "Claude"},
    "max_words_per_line": 5,
    "output_path": "<project>/assets/subtitles/subtitles.srt"
})
```

### 步骤 2: 提取和处理音频

- 从原始素材中提取音轨
- 如果需要，应用降噪（通过 `audio_mixer`）
- 归一化音频电平

### 步骤 3: 获取背景音乐

如果场景计划包含背景音乐：

1. **检查本地 pixabay 音乐库** — 查找与情绪匹配的已下载 MP3
2. **使用 `pixabay_music` 工具** — 按场景计划中的情绪/风格关键词搜索
3. **对所选曲目运行 `audio_energy` 分析** — 找到最佳起始偏移（跳过安静的引子）

在资产清单中记录音乐路径、偏移以及是否需要循环。

### 步骤 4: 生成叠加资产

如果场景计划包含叠加场景（来自场景导演的观看与提出步骤），为每个场景生成资产。

**对于 Remotion 渲染的叠加层**（图表、比较、KPI 网格、统计卡片）：

为每个叠加层创建一个合成 JSON 片段。这些将由合成导演渲染。每个叠加层需要：

```json
{
  "overlay_id": "overlay_1",
  "remotion_cut": {
    "id": "term-agentic-ai",
    "type": "callout",
    "text": "Agentic AI：自主朝着目标行动的软件",
    "in_seconds": 0,
    "out_seconds": 4,
    "backgroundColor": "<theme_background>",
    "accentColor": "<theme_accent>",
    "icon": "💡"
  },
  "overlay_timestamp": 22.0,
  "position": "lower_third"
}
```

**叠加类型 → Remotion cut 映射：**

| 场景计划叠加 | Remotion `type` | 必需属性 |
|-------------------|-----------------|----------------|
| 关键术语定义 | `callout` | `text`、`icon`（可选） |
| 统计/数字 | `stat_card` | `stat`（数字）、`text`（标签） |
| 比较 | `comparison` | `leftLabel`、`rightLabel`、`leftValue`、`rightValue` |
| 数据图表 | `bar_chart` | `chartData`（`{label, value}` 数组） |
| 饼图 | `pie_chart` | `chartData`（`{label, value}` 数组） |
| 折线图 | `line_chart` | `chartSeries`（`{name, data: number[]}` 数组） |
| KPI 仪表盘 | `kpi_grid` | `chartData`（`{label, value}` 数组）— 保持数字较小并带后缀（例如 "2.4M"） |
| 进度指示器 | `progress_bar` | `progress`（0-100）、`text` |
| 章节标题 | `hero_title` | `text`、`subtitle`（可选） |
| 标注/引用 | `callout` | `text`、`icon` |
| 下三分之一 | `text_card` | `text` |

**Remotion AnimatedBackground：**

讲解类合成现在包含一个 `AnimatedBackground` 组件，可渲染动画渐变网格、浮动球体和细微网格图案。这提供了远比纯色更专业的外观。

- 场景背景应使用活跃的主题背景，使 AnimatedBackground 和叠加卡片感觉像同一系统。
- 不要使用任意的纯色作为背景——让 AnimatedBackground 和主题驱动处理方式。
- 在合成绿幕素材时，将 AnimatedBackground 渲染为替换背景（参见 compose-director 步骤 3c）。

**组件约束：**

| 组件 | 最小宽度 | 720px 竖版？ | 值类型 |
|-----------|-----------|-----------------|------------|
| comparison | 900px | 不行 -> 使用 2 个 stat_card | string |
| kpi_grid | 720px | 可以 | 仅限数值（无 "15+"） |
| bar_chart | 500px | 可以 | numeric |
| stat_card | 300px | 可以 | string 也可以 |
| callout | 400px | 可以 | string |
| hero_title | 400px | 可以 | string |
| line_chart | 500px | 可以 | numeric |
| progress_bar | 600px | 可以 | numeric |
| stat_reveal | 300px | 可以 | string 也可以 |

关键规则：
- `comparison` 需要 900px+ 宽度。在 720px 竖版画面中，使用两个顺序显示的 `stat_card` 组件代替。
- `kpi_grid` 的值**必须**是纯数值的（例如 `4.8`、`73`、`2400`）。格式化的字符串如 `"15+"`、`"$4.8B"` 或 `"2.4M"` 会导致渲染错误。对于字符串格式的数字，请使用 `stat_card`。
- 在选择组件之前，始终检查目标帧宽度。竖版（720px）排除了 `comparison`。

**叠加主题规则** —— 从选定的剧本或自定义标识中推导叠加层的背景、强调色和文字颜色。仅在素材/主题需要时才使用深色卡片；明亮风格的谈话节目如果对比度足够，也可以合理地使用浅色卡片。

**对于简单的文字叠加层**（如果使用 Remotion 大材小用）：

使用 FFmpeg 或 PIL 生成 PNG 图像，存储在 `<project>/assets/overlays/overlay_<id>.png`。

### 步骤 5: 构建资产清单

记录所有生成的资产及其路径、类型和工具引用：

```json
{
  "subtitles": {
    "path": "assets/subtitles/subtitles.srt",
    "format": "srt",
    "word_count": 208
  },
  "music": {
    "path": "assets/audio/bg_music.mp3",
    "offset_seconds": 3.5,
    "needs_loop": true
  },
  "overlays": [
    {
      "overlay_id": "overlay_1",
      "type": "callout",
      "timestamp": 22.0,
      "duration": 4.0,
      "remotion_cut": { ... },
      "position": "lower_third"
    }
  ],
  "transcript_segments": "assets/audio/transcript.json"
}
```

### 步骤 6: 自我评估

| 标准 | 问题 |
|-----------|----------|
| **字幕** | 字幕是否存在并与语音时序匹配？ |
| **音频** | 音频是否干净且归一化？ |
| **音乐** | 是否在音乐上运行了 audio_energy 以找到最佳偏移？ |
| **叠加层** | 场景计划中的每个叠加层是否都有生成的资产？ |
| **叠加内容** | 叠加层中的数据是否与演讲者实际所说的内容一致？ |
| **文件** | 所有资产路径是否指向存在的文件？ |

### 步骤 7: 提交

根据模式校验资产清单，并通过检查点持久化。

### 中期事实核查

如果在资产生成过程中遇到不确定的情况：
- 使用 `web_search` 验证主题的视觉准确性（例如，这个建筑实际上长什么样？）
- 使用 `web_search` 在生成插画前查找参考图片
- 在决策日志中记录核查结果：`category="visual_accuracy_check"`

视觉准确性非常重要。如果脚本提到某个特定地点、人物或物体，
在生成图片之前验证其实际外观。不要依赖
AI 模型的训练数据——它可能是错误或过时的。

## 当你不知道如何做时

如果你遇到不确定的生成技术、供应商行为或提示模式：

1. **搜索网络**了解当前最佳实践——模型和 API 变化频繁，代理的训练数据可能过时
2. **检查 `.agents/skills/`** 中是否存在现有的第 3 层知识（供应商特定的提示指南、API 模式）
3. **如果两者都无帮助**，在 `projects/<project-name>/skills/<name>.md` 编写项目级技能文档，记录你所学的
4. **引用来源 URL** 到技能中，使知识可追溯
5. **记录到决策日志**中：`category: "capability_extension"`，`subject: "learned technique: <name>"`

这对于以下内容尤其重要：
- **视频生成提示**——模型响应的特定词汇随版本变化
- **图像模型参数**——FLUX、DALL-E、Imagen 的最佳设置各不相同且不断演进
- **音频供应商的特殊性**——语音克隆、音乐生成和 TTS 各有模型特定的最佳实践
- **Remotion 组件模式**——随着框架演进，新的合成技术不断涌现

不要依赖过时的知识。有疑问时，先搜索。
