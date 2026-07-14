# 合成导演 —  Talking Head 流水线

## 使用时机

你已获得编辑决策和资产清单。你的任务是渲染最终的 talking-head 视频：应用增强链、烧录字幕、混音音频，并按照目标配置文件编码。

## 运行时路由（硬性约束——仅限 Remotion 或 FFmpeg）

Phase 1 从 HyperFrames 推迟。`edit_decisions.render_runtime` 必须是 `"remotion"`（推荐——使用 `TalkingHead` 合成 + `remotion_caption_burn`）或 `"ffmpeg"`（用于仅拼接源素材，无合成）。

- 如果 `edit_decisions.render_runtime == "hyperframes"`，停止。重新打开 idea 阶段并展示约束条件。静默重写是治理违规。
- 根据 AGENT_GUIDE.md → "展示两种合成运行时（硬性规则）"：流水线的约束不能跳过对话。向用户展示该约束，让他们知道 HyperFrames 存在但在此不可行。记录一个 `render_runtime_selection` 决策，其中 hyperframes 为 `rejected_because: "TalkingHead + 字幕对等在 talking-head 上推迟"`。
- 将 `proposal_packet`/`brief` 传递给 `video_compose.execute()` 用于运行时交换检测。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/render_report.schema.json` | 产物校验 |
| 前置产物 | 编辑决策、资产清单 | 渲染输入 |
| 工具 | `video_compose`、`audio_mixer` | 渲染 |
| 媒体配置文件 | `lib/media_profiles.py` | 输出格式 |

## 流程

### 步骤 0: 飞行前检查

在渲染任何内容之前，先验证输入并捕获后续修复代价高昂的问题。

1. **静默检测** — 以 mark 模式运行 `silence_cutter`：
   ```
   silence_cutter.execute({
       "input_path": "<raw_footage>",
       "mode": "mark",
       "silence_threshold_db": -35,
       "min_silence_duration": 0.5
   })
   ```
   - 报告所有超过 0.5 秒的间隔及其时间戳。
   - 如果总静默时间 > 5 秒，**建议在继续前进行剪辑**。长时间的静默浪费渲染时间并在最终视频中产生死点。

2. **ASR 置信度检查** — 扫描字级转录中置信度低的词：
   - 标记任何概率 < 0.7 的词。
   - 列出标记的词及其时间戳，以便用户验证转录是否正确。
   - 需要注意的常见误识别：专有名词、品牌名称、领域行话。

3. **自动构建校正词典**，基于常见的 ASR 错误模式：
   ```python
   corrections = {
       # 印度金融上下文
       "DMI": "EMI",
       "AMI": "EMI",
       # 常见品牌拼写错误
       "open montage": "OpenMontage",
       "remotion": "Remotion",
       # ASR 拆分了的数字
       "4 -5": "4-5",
       "10 -15": "10-15",
   }
   ```
   根据视频主题扩展此词典，添加领域特定的校正。在应用前将校正内容呈现给用户审核。

4. **绿幕标记** — 检查场景导演步骤 0 是否标记了绿幕/蓝幕素材。如果是，记下步骤 3c（绿幕合成）将会需要。

### 步骤 1: 运行增强链

严格按照此顺序应用视频增强。**如果工具可用，尝试每一步骤**——不要无故跳过。

1. **面部增强** — 应用 `talking_head_standard` 预设
2. **眼睛增强** — 去除黑眼圈 + 提亮眼睛
3. **色彩分级** — 应用配置文件
4. **音频增强** — 降噪、归一化

**眼睛增强** — 始终在 face_enhance 之后尝试此操作。在网络摄像头/手机素材上效果明显：
```
eye_enhance.execute({
    "input_path": "<face_enhanced_video>",
    "output_path": "<project>/assets/video/eye_enhanced.mp4",
    "operations": ["dark_circles", "brighten_eyes"],
    "dark_circle_intensity": 0.4,       # 0-1，微妙更好
    "eye_brighten_intensity": 0.3,
})
```
**重要：** 保持强度较低（0.2-0.5）。过度处理会使眼睛看起来不自然。如果工具失败（例如未安装 MediaPipe），记录回退并继续使用 face_enhanced 视频。

### 步骤 1b: 速度调整（如果要求）

如果用户希望视频加速或减速，使用 `video_trimmer`：
```
video_trimmer.execute({
    "operation": "speed",
    "input_path": "<enhanced_video>",
    "output_path": "<project>/assets/video/speed_adjusted.mp4",
    "speed_factor": 1.25    # 0.5x（慢速），1.25x，1.5x，2x（快速）
})
```

常见速度系数：
| 系数 | 使用场景 |
|--------|----------|
| `0.5` | 慢动作，用于戏剧效果 |
| `1.0` | 正常（无变化） |
| `1.25` | 稍微快一点——节奏更紧凑，听起来不会不自然 |
| `1.5` | 明显更快——适合回顾或浓缩内容 |
| `2.0` | 双倍速度——延时效果 |

在增强之后、重新构图之前应用速度调整。

### 步骤 2: 自动重新构图（如果目标平台要求）

如果目标平台需要不同的宽高比（例如 Instagram Reels = 9:16），使用 `auto_reframe`：

```
auto_reframe.execute({
    "input_path": "<enhanced_video>",
    "output_path": "<project>/renders/reframed.mp4",
    "target_aspect": "portrait",       # 9:16 用于 Reels/TikTok/Shorts
    "smoothing_window": 15,            # 平滑摄像机平移
    "face_padding": 0.4,              # 面部周围 40% 边距
})
```

**宽高比预设：**
| 预设 | 比例 | 平台 |
|--------|-------|----------|
| `portrait` | 9:16 | Instagram Reels、TikTok、YouTube Shorts |
| `square` | 1:1 | Instagram 信息流 |
| `landscape` | 16:9 | YouTube、LinkedIn |
| `vertical_4_5` | 4:5 | Instagram 竖版帖子 |

该工具自动运行人脸检测并保持演讲者居中。如果未安装 MediaPipe，则回退到中心裁剪。

**重要：** 在 face_enhance 和 color_grade 之后，但在烧录字幕之前运行 auto_reframe。字幕需要针对最终宽高比定位。

### 步骤 2b: 构建 ASR 校正词典

在烧录字幕之前，扫描转录中可能出现的 ASR 误识别。常见问题：
- 产品/品牌名称："cloud" → "Claude"、"co-pilot" → "Copilot"、"remotion" → "Remotion"
- 技术术语："pythonic" 被误听为 "pathonic"、"API" 被误听为 "a pie"
- 演讲者姓名或公司名称
- 领域特定行话

构建校正词典：
```python
corrections = {
    "cloud": "Claude",
    "co pilot": "Copilot",
    "open montage": "OpenMontage",
}
```

将此字典传递给 `subtitle_gen`（如果生成 SRT）和 `remotion_caption_burn`（如果使用 Remotion 字幕）。即使你发现不需要任何校正，也明确传递一个空字典 `{}` 以确认你已检查过。

### 步骤 3: 烧录字幕

**始终使用 Remotion TikTok 风格的字幕**（逐词高亮）。这是默认和首选方法。除非 Remotion 完全不可用，否则不要回退到 FFmpeg ASS 字幕。

**Remotion 字幕要求：**
- **自动检测视频尺寸** — 不要硬编码宽度/高度。使用 `visual_qa` 探针或 ffprobe 获取实际尺寸，然后传递给渲染。
- **根据实际视频时长设置 `--frames`** — 从探针计算：`frames = duration_seconds * fps`。永远不要使用硬编码的帧数。
- 逐词高亮，使用活跃词颜色（`highlight_color`）。
- 字幕位于画面底部，远离面部。

```
remotion_caption_burn.execute({
    "input_path": "<reframed_or_enhanced_video>",
    "output_path": "<project>/assets/video/captioned.mp4",
    "segments": <transcript_segments_from_asset_manifest>,
    "corrections": {"cloud": "Claude", "co-pilot": "Copilot"},
    "words_per_page": 4,
    "font_size": 52,
    "highlight_color": "<theme_accent>",
})
```

**仅在 Remotion 完全不可用时的回退方案：** 使用 `video_compose` 配合 `burn_subtitles` 操作。这是一种降级体验——警告用户逐词高亮功能不可用。

**关键：9:16 竖版视频的字幕定位（仅 FFmpeg 回退）。**
字幕必须在画面的底部 20% 区域内。在 1920 高的画面上，这意味着 `MarginV=160` 或更高。FFmpeg 默认的字幕位置是居中——这**会**遮挡面部。你**必须**覆盖它。

竖版 talking-head 的 FFmpeg 字幕样式字符串：
```
"FontName=Arial,FontSize=22,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=0,MarginV=160,Alignment=2"
```

**永远不要**使用默认的字幕位置。**永远不要**将字幕定位在画面中央或上半部分。如果在视觉 QA 期间看到字幕出现在面部上，则视频必须使用校正后的定位重新渲染。

### 步骤 3b: 烧录叠加图形（如果场景计划包含叠加层）

如果场景计划包含叠加场景（文字卡片、统计卡片、图表、比较、标注），将它们与字幕一起传递给 `remotion_caption_burn`。**字幕和叠加层在同一个 Remotion 过程中渲染**——无需单独的 FFmpeg 合成。

**工作原理：** TalkingHead Remotion 合成渲染三个图层：
1. **视频**（底部）— talking-head 素材
2. **叠加层**（中间）— 定位的图表、统计数据、标注，带淡入/淡出
3. **字幕**（顶部）— 逐词高亮，始终可见

**将步骤 3 和 3b 合并为一次 `remotion_caption_burn` 调用：**
```
remotion_caption_burn.execute({
    "input_path": "<reframed_or_enhanced_video>",
    "output_path": "<project>/assets/video/captioned.mp4",
    "segments": <transcript_segments>,
    "corrections": {"cloud": "Claude"},
    "words_per_page": 4,
    "font_size": 52,
    "highlight_color": "<theme_accent>",
    "overlays": [
        {
            "id": "term-agentic-ai",
            "type": "callout",
            "text": "Agentic AI：自主朝着目标行动的软件",
            "callout_type": "info",
            "in_seconds": 22.0,
            "out_seconds": 26.0,
            "position": "lower_third",
            "backgroundColor": "<theme_background>",
            "accentColor": "<theme_accent>"
        },
        {
            "id": "stat-market-size",
            "type": "stat_card",
            "stat": "$4.8B",
            "subtitle": "全球 AI Agent 市场（2026）",
            "in_seconds": 35.0,
            "out_seconds": 39.0,
            "position": "upper_third",
            "accentColor": "<theme_secondary_accent>"
        },
        {
            "id": "chart-growth",
            "type": "bar_chart",
            "chartData": [
                {"label": "2023", "value": 1.2},
                {"label": "2024", "value": 2.1},
                {"label": "2025", "value": 3.5},
                {"label": "2026", "value": 4.8}
            ],
            "title": "AI Agent 市场（$B）",
            "in_seconds": 40.0,
            "out_seconds": 45.0,
            "position": "lower_third",
            "chartColors": ["<theme_accent>", "<theme_secondary_accent>", "<theme_tertiary_accent>", "<theme_supporting_accent>"]
        }
    ]
})
```

**叠加位置选项：**
- `lower_third` → 底部区域，字幕上方（默认——对大多数叠加层最安全）
- `upper_third` → 顶部区域（适合演讲者居中/靠下时显示统计数据）
- `left_panel` → 画面左侧 45%（与演讲者并排）
- `right_panel` → 画面右侧 45%
- `full_overlay` → 全屏带暗色背景（谨慎使用，最多 1-2 秒）

**叠加类型 → 必需属性**（与 asset-director 映射相同）：

| 类型 | 必需属性 |
|------|---------------|
| `text_card` | `text` |
| `stat_card` | `stat`、`subtitle`（可选） |
| `callout` | `text`、`callout_type`（info/warning/tip/quote） |
| `comparison` | `leftLabel`、`rightLabel`、`leftValue`、`rightValue` |
| `bar_chart` | `chartData`（`{label, value}` 数组） |
| `line_chart` | `chartSeries`（`{name, data: number[]}` 数组） |
| `pie_chart` | `chartData`（`{label, value}` 数组） |
| `kpi_grid` | `chartData`（`{label, value}` 数组） |
| `hero_title` | `text`、`subtitle`（可选） |
| `section_title` | `text`、`subtitle`（可选） |
| `stat_reveal` | `text`（统计数据）、`subtitle`（标签） |

**重要：** 速度调整后，重新计算叠加时间戳：`adjusted_time = original_time / speed_factor`。

**回退（无 Remotion）：** 如果 Remotion 不可用，`remotion_caption_burn` 会回退到仅使用 FFmpeg 处理字幕。叠加层在 FFmpeg 回退模式下**不会**渲染——警告用户叠加层需要 Remotion。

### 步骤 3c: 绿幕合成（如果是绿幕素材）

如果素材有绿幕/蓝幕（在场景导演步骤 0 中检测到），按照以下流程操作：

1. **运行 `green_screen_processor` 工具** 去除绿幕/蓝幕：
   ```
   green_screen_processor.execute({
       "input_path": "<enhanced_video>",
       "output_path": "<project>/assets/video/greenscreen_removed.mp4",
       "method": "auto"
   })
   ```
   `auto` 方法检测背景是绿色还是蓝色，并应用适当的色度键。

2. **使用 Remotion 渲染动画背景**（通过讲解类合成）：
   ```
   # 渲染一个 AnimatedBackground 片段（渐变网格、浮动球体、细微网格）
   # 使用讲解类合成——而不是纯色 #0F172A
   npx remotion render src/index.ts Explainer --props='{"duration":VIDEO_DURATION}' --output=<project>/assets/video/animated_bg.mp4
   ```
   AnimatedBackground 提供带有浮动球体和细微网格图案的专业渐变网格。这远优于纯色。

3. **运行 `green_screen_composite` 工具** 将演讲者叠加到动画背景上：
   ```
   green_screen_composite.execute({
       "foreground_path": "<greenscreen_removed_video>",
       "background_path": "<animated_bg>",
       "output_path": "<project>/assets/video/composited.mp4",
       "layout": "news_anchor"
   })
   ```
   默认布局为 `news_anchor`（演讲者居中底部，背景填满画面）。根据步骤 0 检测到的演讲者位置调整布局。

4. **通过 Remotion TalkingHead 合成烧录字幕**（不是 FFmpeg ASS 字幕）：
   ```
   remotion_caption_burn.execute({
       "input_path": "<composited_video>",
       "output_path": "<project>/assets/video/captioned.mp4",
       "segments": <transcript_segments>,
       "corrections": <corrections_dict>,
       "words_per_page": 4,
       "font_size": 52,
        "highlight_color": "<theme_accent>",
       "overlays": <overlay_list_from_scene_plan>
   })
   ```

5. **混入背景音乐**（语音时闪避至 15% 音量）：
   ```
   audio_mixer.execute({
       "operation": "duck",
       "video_path": "<captioned_video>",
       "music_path": "<bg_music>",
       "music_volume": 0.15,
       "output_path": "<project>/assets/video/with_music.mp4"
   })
   ```

6. **最终编码**为目标平台规格（见下方步骤 6）。

### 步骤 3d: 构建展示卡片（如果是多片段合集）

如果输出是带展示片段的合集，为每个片段使用 `showcase_card`：
```
showcase_card.execute({
    "input_path": "<showcase_video>",
    "output_path": "<project>/assets/video/sc_<name>.mp4",
    "title": "视频标题",
    "subtitle": "描述 | 风格 | 成本：$0.15",
    "background_color": "0x0A0F1A",
})
```
这会创建带排版文字的 9:16 信箱格式卡片。

### 步骤 4: 组装多片段（如适用）

如果输出有多个段落（例如 talking-head + 展示片段），使用 `video_stitch`：
```
video_stitch.execute({
    "operation": "stitch",
    "clips": ["intro.mp4", "showcase1.mp4", ..., "outro.mp4"],
    "output_path": "<project>/renders/assembled.mp4",
    "transition": "crossfade",         # 或 "fade" 用于通过黑色淡入淡出
    "transition_duration": 0.5,
})
```
**过渡指导：**
- `crossfade`（交叉淡入淡出）：在 talking-head 和展示之间平滑融合
- `fade`（通过黑色淡入淡出）：在展示片段之间短暂变黑
- 混合过渡类型：talk→showcase 使用 `crossfade`，展示之间使用 `fade`

### 步骤 5: 混音音频

使用 `audio_mixer` 叠加背景音乐：

**对于多片段合集** — 使用 `segmented_music` 仅在 talking-head 段落播放音乐：
```
audio_mixer.execute({
    "operation": "segmented_music",
    "video_path": "<assembled_video>",
    "music_path": "<bg_music>",
    "music_volume": 0.20,
    "segments": [
        {"start": 0, "end": 17.0},       # 开场讲话
        {"start": 167.0, "end": 175.0}    # 结尾讲话
    ],
    "fade_duration": 0.5,
    "output_path": "<project>/renders/final.mp4",
})
```

**对于单一 talking-head 视频** — 使用 `duck` 或 `full_mix`：
- 将原始音频与背景音乐叠加
- 如果有音乐则应用闪避
- 归一化最终电平

### 步骤 6: 最终编码——必须执行

**不要跳过此步骤。** 没有最终编码，输出会过大，且可能无法在目标平台上正常播放。

使用 `video_compose` 配合 `encode` 操作：
- 应用目标媒体配置文件（youtube_landscape、tiktok、instagram_reels 等）
- 双遍编码以保证质量

**目标文件大小：**
| 平台 | 最大时长 | 目标大小 |
|----------|-------------|-------------|
| Instagram Reels | 90 秒 | < 50 MB |
| TikTok | 10 分钟 | < 100 MB |
| YouTube Shorts | 60 秒 | < 40 MB |
| YouTube | 不限 | < 25 MB/分钟 |

如果输出超过目标，以较低比特率重新编码。一个 66 秒、76 MB 的 Instagram Reels 是不可接受的——它应该低于 30 MB。

```
video_compose.execute({
    "operation": "encode",
    "input_path": "<mixed_video>",
    "output_path": "<project>/renders/final.mp4",
    "media_profile": "instagram_reels",
    "video_bitrate": "4M",
    "audio_bitrate": "192k",
})
```

### 步骤 7: 视觉 QA

在宣布成功之前使用 `visual_qa` 验证输出：
```
visual_qa.execute({
    "operation": "review",
    "input_path": "<final_video>",
    "timestamps": [3.0, 10.0, 25.0, 50.0, 100.0, 170.0],
})
```
然后**读取每张提取的帧**进行验证：
- 字幕可见并位于底部（不在面部上）
- 面部增强已应用（皮肤看起来光滑，不过度处理）
- 过渡干净（过渡点无伪影）
- 展示卡片具有可读的排版

同时运行探针验证：
```
visual_qa.execute({
    "operation": "probe",
    "input_path": "<final_video>",
    "expected": {
        "width": 1080, "height": 1920,
        "has_audio": true,
        "pixel_format": "yuv420p"
    },
})
```

并检查音频电平：
```
visual_qa.execute({
    "operation": "audio_levels",
    "input_path": "<final_video>",
    "timestamps": [5.0, 50.0, 170.0],
})
```
验证：讲话段落的音量高于展示段落（确认音乐放置正确）。

### 步骤 8: 构建渲染报告

记录输出：路径、格式、分辨率、时长、文件大小、QA 结果。

### 步骤 9: 自我评估

| 标准 | 问题 |
|-----------|----------|
| **可播放性** | 视频是否能无错误播放？ |
| **质量** | 增强效果是否正确应用？ |
| **构图** | 如果重新构了图——面部居中吗？没有重要内容被裁剪？ |
| **音频** | 语音清晰、电平平衡吗？音乐仅在预期段落播放？ |
| **字幕** | 字幕在底部可见吗？不遮挡面部？逐词高亮正常工作？ |
| **过渡** | 过渡干净吗？类型正确（crossfade vs fadeblack）？ |
| **展示** | 展示卡片是否正确信箱格式处理、排版可读？ |

### 步骤 10: 提交

根据模式校验渲染报告，并通过检查点持久化。
