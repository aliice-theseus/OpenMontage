# 合成导演 — 解说片流水线

## 使用时机

你是生成式解说视频的合成师。你有包含完整编辑时间线的 `edit_decisions` 和包含所有文件路径的 `asset_manifest`。你的工作是渲染最终视频：组装视觉、分层音频、烧录字幕并编码为目标格式。

这是视频作为可播放文件存在之前的最后一个技术阶段。一切都汇聚于此。

## 运行时路由（强制第一步）

在任何其他操作之前读取 `edit_decisions.render_runtime`。它在提案时被锁定，不得悄悄更改。本技能其余部分的流程步骤（Remotion 公开/暂存、词级字幕烧录等）假定 `render_runtime="remotion"` — 数据驱动解说片的默认值。

- **`render_runtime="hyperframes"`** — HTML/CSS/GSAP 渲染。不要按照下面的 Remotion 特定步骤操作。而是：阅读 `skills/core/hyperframes.md`、`.agents/skills/hyperframes/SKILL.md` 和 `.agents/skills/hyperframes-cli/SKILL.md`。调用 `video_compose` 时保持 edit_decisions 不变 — 它将委托给 `hyperframes_compose`，它会在 `projects/<name>/hyperframes/` 下实例化一个工作区，运行 `lint → validate → render`，并返回 MP4。lint 和 validate 都必须在渲染前通过；对比可以在迭代期间推迟，但最终交付不行。
- **`render_runtime="ffmpeg"`** — 简单拼接/修剪。直接调用 `video_compose`；当此运行时明确锁定时，它不会自动升级到 Remotion。
- **运行时不可用** — 根据 AGENT_GUIDE.md > "明确上报阻塞问题"上报阻塞问题，并在切换前获得用户批准（在 decision_log 中记录为 `render_runtime_selection` 决策）。

`final_review.checks.promise_preservation.render_runtime_used` 必须等于实际运行的运行时；`runtime_swap_detected` 必须为 `false`，除非批准的决策授权了交换。

**将 `proposal_packet` 传递给 `video_compose.execute()`**，以便工具内的交换检测能够实际触发。没有它，`runtime_swap_check` 会报告为 `skipped`，你只能依赖审查者技能的跨工件比较。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/render_report.schema.json` | 工件验证 |
| 前置工件 | `state.artifacts["edit"]["edit_decisions"]`、`state.artifacts["assets"]["asset_manifest"]` | 要渲染的内容 |
| 剧本 | 活动风格剧本 | 质量目标 |
| 工具 | `video_compose`、`audio_mixer` | 渲染能力 |
| 媒体配置 | `lib/media_profiles.py` | 输出格式规格（分辨率、编码器、比特率） |

## 流程

### 步骤 1：选择渲染策略

基于编辑决策，选择渲染方法：

**Remotion 渲染**（默认 — 除非明确覆盖，否则使用此方法）：
- 动画文字卡片、统计卡片、图表场景
- 复杂过渡（变形、缩放、Ken Burns）
- 程序化运动图形
- 音频嵌入（带淡入/淡出和音量的旁白 + 音乐）
- 通过 CaptionOverlay 组件实现词级字幕
- 最适合：所有解说视频，无论基于图像还是动画密集

**FFmpeg 流水线**（回退 — 仅当 Remotion 不可用时）：
- 静态图像带 Ken Burns
- 音频分层
- SRT 字幕烧录
- 最适合：没有 Node.js/Remotion 安装的环境

**重要：使用 Remotion 时，所有这些都通过 Remotion — 而不是 FFmpeg：**
- 音频（旁白 + 音乐）→ Remotion `audio` prop，不是外部 audio_mixer
- 字幕 → Remotion `captions` prop（词级），不是通过 FFmpeg 的 SRT 烧录
- 文字叠加（CTA、标题）→ Remotion `text_card` 剪辑类型，不是 AI 生成的图像

### 步骤 2：音频获取（旁白、音乐、字幕）

在渲染之前，向用户展示音频选项并获取他们的偏好。

**向用户展示：**

> **此视频的音频设置：**
>
> **旁白：** 我可以使用 OpenAI TTS（`gpt-4o-mini-tts` — $0.015/分钟，6 种声音，声音指示）生成 TTS 旁白。你想要哪种声音和基调？我会根据视频主题提出一种声音，或者你可以选择：
> - `onyx` — 深沉、权威（纪录片、技术）
> - `echo` — 共鸣、未来感（产品广告、科幻）
> - `nova` — 明亮、精力充沛（乐观、解说）
> - `fable` — 温暖、讲故事（叙事、教育）
> - `shimmer` — 表现力、温暖（有机、生活方式）
> - `alloy` — 中性、平衡（通用）
>
> **音乐：** 我可以自动从 Pixabay 找到免版税背景音乐（无需密钥）。如果你有 `FREESOUND_API_KEY`，我也可以搜索 Freesound 作为备份。
>
> **字幕：** 我会使用 WhisperX 对最终旁白进行转录，生成词级字幕，通过 Remotion 字幕烧录到视频中。
>
> 想要我按推荐继续，还是调整什么？

**在用户确认后：**

1. **用时序预算写旁白脚本**（参见场景导演步骤 4b）：
   - 从剪辑计算视频时长
   - 预算占视频时长的 85-90%
   - 纪录片用 2.0-2.5 词/秒，精力充沛用 2.5-3.0
   - 在生成 TTS 前验证词数

2. **生成 TTS 旁白：**
   ```python
   from tools.audio.openai_tts import OpenAITTS
   result = OpenAITTS().execute({
       'text': narration_script,
       'voice': '<用户选择或代理推荐>',
       'instructions': '<与视频基调匹配的声音指示>',
       'output_path': 'path/to/narration.mp3',
   })
   # 关键：检查 result.data['audio_duration_seconds'] 与视频时长对比
   # 如果旁白超过视频 >1 秒：缩短脚本并重新生成
   ```

3. **下载背景音乐：**
   ```python
   from tools.audio.pixabay_music import PixabayMusic
   result = PixabayMusic().execute({
       'query': '<匹配视频主题的情绪/流派>',
       'min_duration': video_duration_seconds,
       'max_duration': 300,
       'output_path': 'path/to/music.mp3',
   })
   ```

4. **通过 WhisperX 生成字幕：**
   ```python
   from tools.analysis.transcriber import Transcriber
   result = Transcriber().execute({
       'input_path': 'path/to/narration.mp3',
       'model_size': 'base',
       'language': 'en',
   })
   # 将 word_timestamps 转换为 Remotion 字幕格式：
   # [{ "word": "Hello", "startMs": 0, "endMs": 340 }, ...]
   ```

5. **组装合成 JSON** 带音频配置：
   ```json
   {
     "audio": {
       "narration": { "src": "path/to/narration.mp3", "volume": 1 },
       "music": { "src": "path/to/music.mp3", "volume": 0.1, "fadeInSeconds": 2, "fadeOutSeconds": 3 }
     },
     "captions": [ ... 来自 WhisperX 的词级字幕 ... ]
   }
   ```

### 步骤 3：准备渲染输入

对于编辑决策中的每个剪辑：
1. 验证源资产在其声明路径存在
2. 检查资产尺寸/时长是否匹配预期
3. 准备变换参数（缩放、位置、裁切）

对于音频：
1. 验证旁白时长在视频时长内（使用 `audio_probe`）
2. 验证音乐时长覆盖视频时长
3. 从编辑决策准备闪避参数

### 步骤 3：确定输出配置

从概要工件读取目标平台。映射到媒体配置：

| 平台 | 配置 | 分辨率 | 说明 |
|----------|---------|-----------|-------|
| YouTube | `youtube_landscape` | 1920x1080 | 大多数解说片默认 |
| TikTok/Reels | `tiktok` | 1080x1920 | 竖屏，需要重新构图 |
| Twitter/X | `twitter_landscape` | 1280x720 | 更短格式 |
| LinkedIn | `linkedin` | 1920x1080 | 专业上下文 |

通过 `ffmpeg_output_args(get_profile(name))` 获取确切的编码参数。

### 步骤 4：渲染视频

调用 `video_compose` 工具：

```
{
  "operation": "render",
  "edit_decisions": <edit_decisions artifact>,
  "asset_manifest": <asset_manifest artifact>,
  "output_profile": "youtube_landscape",
  "output_path": "renders/output.mp4",
  "options": {
    "subtitle_burn": true,
    "audio_normalize": true,
    "two_pass_encode": true
  }
}
```

如果使用 Remotion 渲染动画段落：
1. 从编辑决策生成 Remotion 合成数据
2. 对动画段落调用 `video_compose` 带 `operation: "remotion_render"`
3. 通过 FFmpeg 将 Remotion 输出与其余段落组装

**零密钥 Remotion 渲染（纯组件视频）：**
当所有场景都是 Remotion 组件类型（hero_title、stat_card、bar_chart、line_chart、pie_chart、kpi_grid、comparison、callout、progress_bar、text_card）时，使用 Explainer 入口点将整个视频渲染为单个 Remotion 合成。无需 FFmpeg 组装。edit_decisions cuts 数组直接映射到 Remotion props。有关经过验证的公式，请参见 `skills/core/remotion.md` — 特别是视觉一致性的全暗背景规则。

### 步骤 5：音频后处理

**Remotion 路径（默认）：** 完全跳过外部音频混合。Remotion 通过 `<Audio>` 组件原生处理所有音频。在合成 props 中传递音频源：
```json
{
  "audio": {
    "narration": { "src": "project/narration.mp3", "volume": 1.0 },
    "music": { "src": "project/music.mp3", "volume": 0.12, "fadeInSeconds": 1.5, "fadeOutSeconds": 2.5 }
  }
}
```
Remotion 在一次传递中渲染音频和视频 — 无需外部复用。
通过 Remotion 渲染时，不要使用 `audio_mixer` 进行闪避/混音。

**FFmpeg 回退（仅当 Remotion 不可用时）：**
调用 `audio_mixer` 工具：
1. 按顺序分层旁白段落
2. 按剧本音量混音背景音乐
3. 应用闪避（旁白期间音乐降低）
4. 标准化整体音频电平
5. 输出最终的混音音频轨
video_compose 工具将它与视频复用。

### 步骤 5b：生成字幕（强制）

所有解说内容必须包含字幕。从旁白音频生成 — 不要跳过此步骤。

**Remotion 路径（默认 — 使用 Remotion 渲染时）：**

1. **转录**使用 `transcriber` 工具（whisperx）的完整旁白：
   ```python
   from tools.analysis.transcriber import Transcriber
   result = Transcriber().execute({
       'input_path': 'projects/<project>/assets/audio/narration_full.mp3',
       'model_size': 'base',
       'language': 'en',
       'output_dir': 'projects/<project>/assets/audio'
   })
   # result.data 包含带词级时间戳的段落
   ```

2. **转换为 Remotion WordCaption 格式**（不是 SRT）：
   ```python
   captions = []
   for segment in result.data['segments']:
       for word_info in segment.get('words', []):
           captions.append({
               'word': word_info['word'],
               'startMs': int(word_info['start'] * 1000),
               'endMs': int(word_info['end'] * 1000),
           })
   ```

3. **将字幕添加到合成 props** — 它们放在 `captions` 数组中，与 `cuts` 和 `audio` 并列：
   ```json
   {
     "cuts": [...],
     "audio": {...},
     "captions": [
       { "word": "Root", "startMs": 120, "endMs": 340 },
       { "word": "canals", "startMs": 340, "endMs": 680 }
     ]
   }
   ```

   Remotion 的 CaptionOverlay 将这些渲染为逐词高亮字幕，使用主题的 `captionHighlightColor` 和 `captionBackgroundColor`。这优于 FFmpeg SRT 烧录，因为它产生与旁白同步的动画词级高亮。

**FFmpeg 回退（仅当 Remotion 不可用时）：**

如果 Remotion 不可用，回退到 SRT 生成 + FFmpeg 烧录：
   ```python
   from tools.subtitle.subtitle_gen import SubtitleGen
   SubtitleGen().execute({
       'segments': transcription_data['segments'],
       'format': 'srt',
       'output_path': 'projects/<project>/assets/subtitles.srt',
       'max_words_per_cue': 8,
       'max_chars_per_line': 42
   })
   # 然后用 video_compose operation='burn_subtitles' 烧录
   ```

**最终交付物**必须**有字幕** — 要么通过 Remotion 字幕要么 FFmpeg 烧录。

### 步骤 5c：渲染前验证（强制）

**在渲染前始终运行合成验证器。** 这能捕获浪费渲染时间的问题。

```python
from tools.analysis.composition_validator import CompositionValidator
result = CompositionValidator().execute({
    'composition_path': 'path/to/composition.json',
    'assets_root': 'remotion-composer/public',
})
# result.data['valid'] 必须为 True 才能继续渲染
# 如果为 False：首先修复报告的错误（丢失的资产、音视频不匹配等）
```

常见捕获：
- 旁白音频比视频长（会被截断）
- 缺少图像/音频文件（渲染会失败）
- 音乐比视频短（结尾静音）

**不要跳过此步骤。** 如果验证失败，修复问题并在渲染前重新验证。

### 步骤 6：渲染后自我审查（强制 — 所有步骤必需）

渲染后，代理**必须审查自己的输出**，然后再呈现给用户。这能捕获验证器无法发现的问题（视觉质量、音频同步、字幕可读性）。

**关键：你必须完成 6a 到 6e 的所有步骤。不要跳过任何步骤。
最常见的代理失败是做 6a（帧）和 6c（视觉）而跳过 6b（音频转录）—— 这错过了灾难性的问题，如完全缺失音频。**

**6a. 探测渲染文件（首先 — 所有其他检查的关卡）：**
```bash
ffprobe -v quiet -print_format json -show_format -show_streams rendered_video.mp4
```
验证：
- 视频流存在（codec_type: "video"）且分辨率正确
- **音频流存在（codec_type: "audio"）** — 如果没有音频流，立即停止并修复
- 时长在目标的 ±5% 以内
- 文件大小合理（不是 0 字节）

**如果音频流丢失：渲染没有嵌入音频。不要继续向用户展示视频。修复音频配置并重新渲染。**

**6b. 提取审查帧：**
```python
from tools.analysis.frame_sampler import FrameSampler
midpoints = [(cut['in_seconds'] + cut['out_seconds']) / 2 for cut in cuts]
FrameSampler().execute({
    'input_path': 'path/to/rendered_video.mp4',
    'strategy': 'timestamps',
    'timestamps': midpoints,
    'output_dir': 'path/to/review-frames',
    'format': 'png',
})
```

**6c. 转录渲染音频（强制 — 不要跳过）：**
```python
from tools.analysis.transcriber import Transcriber
result = Transcriber().execute({
    'input_path': 'path/to/rendered_video.mp4',
    'model_size': 'base',
    'language': 'en',
    'output_dir': 'path/to/review-frames',
})
# 如果 result 返回 0 个词：音频已静音/丢失 — 停止并修复
# 如果词数 < 脚本词数的 80%：音频被截断 — 调查
```

**6d. 视觉检查 — 审查每帧：**
- 背景颜色/渐变是否与意图匹配？（注意深色主题视频上的白色背景）
- 图像是否正确渲染？（不是空白，不是拉伸）
- 字幕是否可见且间距适当？
- 叠加层（章节标题、统计揭示）是否正确定位？
- 开场场景视觉上是否强烈？（对社交媒体缩略图很重要）
- CTA/结束画面显示的文字是否正确？（AI 生成图像中的文字经常产生幻觉 — 对于任何需要精确的文字，使用 Remotion text_card）

**6e. 音频检查 — 将转录与脚本对比：**
- 完整旁白是否被捕获？（将最后一个转录词与最后一个脚本词对比）
- 结尾是否有词被截断？（旁白超过视频时长）
- 时序对齐 — 旁白段落是否大致匹配其预期的场景？
- 背景音乐是否可听见？（转录器可能不会捕获音乐，但 ffprobe 确认音频流）

**6f. 编译并向用户展示审查：**

> **"[视频标题]" 的渲染后审查：**
>
> **文件：** [时长]s、[分辨率]、[文件大小] — 音频流：[存在/缺失]
> **音频：** [完整/在 Xs 处截断] — 从渲染输出转录了 [N]/[M] 个词
> **视觉：** [审查了 N 个场景] — [问题 或 "所有场景渲染正确"]
> **字幕：** [Remotion CaptionOverlay / FFmpeg SRT / 缺失] — [词级高亮工作 / 问题]
> **发现的问题：** [列出任何问题及严重程度]
>
> **建议：** [要修复的内容，如果有]
>
> 想要我修复这些问题并重新渲染，还是这样就够了？

**只有在用户批准后（或代理发现零问题）视频才被视为最终版。**

### 步骤 6-old：文件和内容验证

**文件验证：**
- [ ] 输出文件在声明的路径存在
- [ ] 文件大小合理（不是 0 字节，不是可疑地小）
- [ ] 文件是有效的容器（ffprobe 成功）

**内容验证：**
- [ ] 时长在目标的 ±5% 以内
- [ ] 分辨率与选定的配置匹配
- [ ] 音频通道存在（立体声）
- [ ] 没有音频削波或 > 1 秒的静音空白

**质量检查（由上述自我审查覆盖）：**
- [ ] 视觉：所有场景帧已检查
- [ ] 音频：完整转录已验证
- [ ] 字幕：可见且计时正确

### 步骤 7：构建渲染报告

```json
{
  "version": "1.0",
  "outputs": [
    {
      "path": "renders/output.mp4",
      "format": "mp4",
      "codec": "h264",
      "resolution": "1920x1080",
      "fps": 30,
      "duration_seconds": 62.4,
      "file_size_mb": 45.2,
      "audio_codec": "aac",
      "audio_channels": 2,
      "render_strategy": "ffmpeg",
      "render_time_seconds": 180
    }
  ],
  "render_summary": {
    "total_cuts_rendered": 12,
    "subtitles_burned": true,
    "audio_tracks_mixed": 3,
    "target_duration_seconds": 60,
    "actual_duration_seconds": 62.4
  }
}
```

### 步骤 8：自我评估

评分（1-5）：

| 标准 | 问题 |
|-----------|----------|
| **可播放性** | 视频是否在标准播放器中无错误播放？ |
| **时长准确性** | 实际时长是否在目标的 ±5% 以内？ |
| **音频质量** | 旁白是否清晰、音乐平衡、无削波？ |
| **视觉质量** | 图像是否清晰、过渡流畅、无伪影？ |
| **字幕准确性** | 字幕是否存在、可读且同步？ |

如果任何维度得分低于 3，调查并重新渲染。

### 步骤 9：提交

对照模式验证 render_report 并通过检查点持久化。

## 常见陷阱

- **缺少资产文件**：在开始渲染前始终验证每个引用的文件存在。渲染过程中的缺失文件会浪费时间。
- **音频同步漂移**：跨旁白段落累积的时序错误导致音视频不同步。使用绝对时间戳，不是相对偏移。
- **字幕编码**：将字幕烧录到视频中（硬编码）以获得最大兼容性。不要依赖软字幕用于社交媒体。
- **单遍编码**：双遍编码在相同文件大小下产生更高质量。值得额外的渲染时间。
- **忽略媒体配置**：YouTube 和 TikTok 的要求非常不同。始终检查目标配置。
