# 创意导演 - 纪录片蒙太奇流水线

## 使用时机

你将用户提示转化为下游每个阶段都会读取的概要工件。对于本流水线，概要就是主题核心：蒙太奇要讲什么、它应该是什么感觉、以及它应该多长。

## 运行时选择（强制 — 展示约束条件，不要默默选择）

锁定 `render_runtime = "remotion"`。**Phase 1 中 HyperFrames 在本流水线上不是有效运行时** — 纪录片蒙太奇依赖 Remotion 的 `CinematicRenderer` 合成及其 ProRes-4444 alpha 尾标叠加栈，HyperFrames 目前没有与之对等的功能。

根据 AGENT_GUIDE.md → "展示两种合成运行时（硬性规则）"：不要默默默认。告诉用户："您的机器上可以使用 HyperFrames 作为替代运行时，但纪录片蒙太奇依赖于 Remotion CinematicRenderer + 尾标叠加栈，因此 remotion 是唯一可行的选择 — 可以继续吗？" 在 `decision_log` 中记录 `render_runtime_selection` 决策，在 `options_considered` 中列出两个运行时，hyperframes 的 `rejected_because` 设置为 "CinematicRenderer + 尾标叠加对等在纪录片蒙太奇上推迟实现"。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/brief.schema.json` | 工件验证 |
| 用户输入 | 对话历史 | 原始需求 |
| 元 | `skills/meta/reviewer.md` | 自我审查环节 |

## 流程

### 1. 提炼主题性问题

纪录片蒙太奇回答的是用户无法用一句话说清楚的问题。你的任务是将那个问题用**一行**文本来命名。

好的主题性问题：

- "回家的感觉是什么？"
- "20 世纪是如何想象未来的？"
- "凌晨四点的城市在发生什么？"
- "地球上所有的脚印看起来是怎样的？"

不好的主题性问题（过于抽象或过于具体）：

- "一个关于城市的视频"（过于抽象 — 没有感觉）
- "一个包含 8 个特定月球镜头的蒙太奇"（过于具体 — 那是镜头列表，不是主题）

### 2. 确定基调

选择**一个**情感基调。写下来。下游的一切都以此为准。

本流水线常见的基调：

- **挽歌式（elegiac）** — 长停留、柔和色彩、慢切（失落、记忆、家）
- **紧迫式（urgent）** — 短切、硬同步、运动密集（危机、城市、当下）
- **敬畏式（reverent）** — 庄严、对称、耐心（自然、仪式、宏大）
- **诙谐式（wry）** — 讽刺并置、荒谬处剪辑（消费文化、政治、世纪中期乐观主义）
- **梦幻式（dreamlike）** — 慢速溶解、重复主题、非线性（童年、悲伤、记忆）

### 3. 选择时长和结构

时长很重要，因为它限制了节拍的数量。

| 时长 | 节拍 | 用途 |
|----------|-------|-----|
| 30-45秒 | 8-12个剪辑 | 社交/Instagram/短视频 — 单一情感，无弧线 |
| 60-90秒 | 15-25个剪辑 | 标准短片 — 带有转折的小弧线 |
| 2-3分钟 | 30-50个剪辑 | 真正的散文式蒙太奇 — 可实现三幕弧线 |

结构选项：

- **单图扩展** — 从多个角度呈现一个想法（适合 60 秒以下的挽歌式作品）
- **前后对比** — 前半段建立，后半段转折（适合诙谐或紧迫基调）
- **三幕式** — 建立 → 转折 → 释放（Adam Curtis 风格，需要 >90 秒）
- **列表/目录式** — "每个……的人"结构，没有弧线，只是积累（适合敬畏或挽歌式）

### 4. 注明音乐意图（强制）

纪录片蒙太奇与其音乐基底密不可分。**本流水线强制要求音乐。** 唯一的例外是用户明确选择不使用（例如"不要音乐，我要静音"）— 这必须在 `music_plan.source = "none"` 中记录，并附带 `music_plan.opt_out_reason` 字段。

在设计阶段感觉"纯粹"的静音式概要，到合成阶段通常看起来像被废弃的素材。不要假设静音能自我证明价值。如果用户没有提到音乐，**假设他们需要音乐**并选择：

- 用户提供的曲目（将路径填入 `music_plan.source_path`）
- 音乐库选择（列出 `music_library/` 中的内容）
- 生成式音乐（命名工具和提示种子，附基调）
- 明确选择不使用（`source: "none"` + `opt_out_reason`）

**如果没有任何音乐来源可用，请警告用户。** 不要默默推迟这个问题 — 这会在资产阶段成为昂贵的意外。

### 5. 注明尾标意图（强制）

每部纪录片蒙太奇电影都以一个哲学性的尾标结束 — 一个简短、抽象的句子，赋予整个作品意义。它作为 Remotion 结尾卡片渲染（"闪耀下划线标签"基调 — 粗体、字间距、动画下划线）。

**默认模式为 `"overlay"`** — 标签在主体素材的最后几幕上渐入，使其感觉像是电影的一部分，而不是最后附加的独立卡片。替代方案是 `"concat"`，它在主体之后追加一个独立的黑底卡片。仅在用户明确要求分离的标题卡片时，或当最终素材视觉上过于复杂无法清晰叠加文字时，使用 concat 模式。

**尾标是强制要求的。** 唯一的例外是用户明确选择不使用，记录为 `end_tag_plan: null` 并附带 `end_tag_opt_out_reason` 字段。

在概要阶段提出尾标。写 3 个选项并推荐一个。预期结构：

```json
{
  "end_tag_plan": {
    "text": "WE BUILT BOTH WITH THE SAME HANDS.",
    "palette": "warm_ivory_on_black",
    "duration_seconds": 5.5,
    "render_engine": "remotion",
    "component": "EndTag",
    "mode": "overlay"
  }
}
```

字段说明：
- `text` — 3-9 个词。一个论点，不是总结。
- `palette` — `"cool_offwhite_on_black"` 或 `"warm_ivory_on_black"`。
- `duration_seconds` — 尾标总屏幕时间（淡入 + 停留 + 淡出）。5-8 秒是最佳区间。
- `render_engine` — 始终为 `"remotion"`。
- `component` — 始终为 `"EndTag"`。
- `mode` — `"overlay"`（默认）或 `"concat"`。
  - **overlay**：尾标渲染为带 alpha 通道的 ProRes 4444 → 通过 FFmpeg overlay 滤镜合成到最终主体素材上。尾标淡入出现在现场素材的最后 N 秒。主体自身的淡出和尾标的淡出应对齐。
  - **concat**：尾标渲染为不透明 MP4 → 通过 FFmpeg concat 在主体后追加。输出总时长 = 主体 + 尾标。

### 6. 注明旁白意图（可选）

与音乐和尾标不同，旁白是可选的。如果视觉 + 音乐 + 尾标能承载基调，没有旁白也没问题。如果使用旁白，请注明 TTS 提供商和声音。如果没有旁白，请明确记录 `narration: "none"` — 不要留下缺失的字段。

### 7. 记录概要

概要必须携带的最少字段：

```json
{
  "topic": "雨中一分钟",
  "thematic_question": "雨水向你展示了一座城市的什么？",
  "tone": "elegiac",
  "duration_seconds": 90,
  "shape": "list",
  "sources_allowed": ["pexels", "pixabay_video", "coverr", "mixkit", "archive_org", "nara", "nasa"],
  "generated_clips_allowed": false,
  "narration": "none",
  "music_plan": {
    "source": "generated",
    "provider": "elevenlabs",
    "prompt_seed": "A 小调慢速环境 drone，无打击乐，60 秒持续渐强，Max Richter 风格"
  },
  "end_tag_plan": {
    "text": "THE CITY KEEPS ITS OWN VIGIL.",
    "palette": "cool_offwhite_on_black",
    "duration_seconds": 5.5,
    "render_engine": "remotion",
    "component": "EndTag"
  },
  "era_mix": "any",
  "target_platform": "social_short"
}
```

`era_mix` 是纪录片特有的字段："modern"偏向 Pexels，"vintage"偏向 Archive.org Prelinger，"any"留给场景导演按槽位自行决定。

### 8. 质量门

- 主题性问题是一句话。
- 基调是固定列表中的一个基调。
- 时长和结构是具体的数字/枚举值。
- `music_plan` 存在且要么命名了真实来源，要么有 `source: "none"` + `opt_out_reason`（用户的明确决定）。
- `end_tag_plan` 存在且要么有非空的 `text`，要么是 `null` 并附带 `end_tag_opt_out_reason`（用户的明确决定）。
- 来源列表非空，且至少一个请求的来源在预检中显示的 `corpus_builder.source_provider_menu` 中标记为 `available`。

## 常见陷阱

- 提出多个主题（"这是关于城市 AND 技术 AND 失去"）。选一个。其他的成为下游的关联。
- 跳到镜头列表。概要关乎**意义**。镜头是下一步的事。
- 忽略时长。45 秒的作品配 50 个剪辑会让人眩晕。3 分钟的作品配 12 个剪辑是幻灯片。
- 忘记询问音乐。用户通常有意见。
- 假设静音能自我证明价值。它不能。除非用户明确说不要，否则音乐是强制性的。
- 跳过尾标因为"图像会自己说话"。它们不会 — 尾标就是论点。每次都提出一个。
