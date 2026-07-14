# 合成导演 - 纪录片蒙太奇流水线

## 使用时机

时间线已存在。每个剪辑都有入/出点，过渡已选择，音乐基底已锁定。你现在必须渲染作品并应用基调平滑处理（统一的裁切 + LUT + 音频混音），使混合年代的语料库感觉像一部电影。

输出是一个单独的 mp4 加上一个 `render_report` 工件。

## 运行时路由（硬约束）

本流水线当前**需要** `render_runtime="remotion"`。尾标堆栈（ProRes 4444 叠加合成到最终场景上，或 concat 回退）依赖于 Remotion 的 `CinematicRenderer` 合成及其保留 alpha 的渲染路径。HyperFrames 的尾标对等功能明确属于 Wave 3 / 推迟工作（参见 `skills/core/hyperframes.md` → "Phase 1 中哪些保持 Remotion 独占"）。

- 如果 `edit_decisions.render_runtime` 不是 `remotion`，停止。这是一个**关键治理违规**。向用户展示冲突，将决策路由回提案以重新锁定 `render_runtime="remotion"`，在 decision_log 中记录 `render_runtime_selection` 修正，然后继续。
- 永远不要通过重写 edit_decisions 中的 render_runtime 来悄悄继续。纪录片承诺（运动驱动、情绪驱动、统一调色）由 Remotion 堆栈维护，而这个承诺是用户批准的。
- 将 `proposal_packet` 传递给 `video_compose.execute()`，以便工具内的 `runtime_swap_detected` 检查能主动确认运行时从头到尾保持 `remotion`。在本流水线上跳过此检查意味着你忘记传递提案工件。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/render_report.schema.json` | 工件验证 |
| 前置工件 | `state.artifacts["edit"]["edit_decisions"]` | 剪辑、过渡、音乐、元数据提示 |
| 前置工件 | `state.artifacts["assets"]["asset_manifest"]` | 文件路径、时长、提供者 |
| 工具 | `video_compose`（Remotion 优先 + FFmpeg 回退） | 主要渲染引擎 |
| 工具 | `audio_mixer` | 音乐淡入淡出、静音窗口、L-cut |
| 工具（可选） | `color_grade` | 跨混合年代剪辑的统一 LUT |
| 工具（可选） | `video_trimmer`、`video_stitch` | 需要时的底层辅助工具 |

## 思维模型

大多数流水线将合成视为一个枯燥的导出步骤。对于纪录片蒙太奇，它是一个创意步骤：调色和混音将来自完全不同来源的素材调和成一部作品的最后一次处理。

有三件事必须在这里完成，不能提前：

1. **统一宽高比和信箱模式。** Pexels 1920x1080、Prelinger 640x480 4:3、NASA 1280x720 都需要落在一个画布上。
2. **统一色彩调色。** 在整条时间线上应用一个统一的 LUT，这是让 1962 年的家庭影片与 2023 年的厨房片段相邻而不显突兀的关键。
3. **音频混音。** 音乐电平、静音窗口、L-cut 环境音延续、最终淡出 — 在拥有时间线的情况下一次性完成。

## 流程

### 0. 硬性需求检查

读取 `brief` 和 `edit_decisions.metadata` 中的任何硬性需求。如果概要要求"无旁白"但旁白轨道以某种方式出现在剪辑中，**停止**并询问。不要在违反合同的情况下渲染。

同时确认 `edit_decisions.renderer_family` 锁定为 `documentary-montage`，并且所选渲染引擎保留了该决策。对于此仓库的治理模型，`video_compose` 在 `operation="render"` 时是 Remotion 优先的，即使是素材主导的作品。

- 如果 Remotion 可用，使用正常的 `render` 路径并保持已批准的渲染器家族。
- 如果 Remotion 不可用，不要悄悄降级到 FFmpeg。在切换引擎之前上报并获得批准。

### 1. 确定画布

读取 `brief.target_platform`：

| 目标平台 | 画布 | 信箱模式 |
|--------|--------|-----------|
| `social_short`（Instagram/TikTok） | 1080x1920（9:16） | 顶部/底部裁切；每个剪辑居中锚定 |
| `youtube` / `generic` | 1920x1080（16:9） | 无；可选择 2.35:1 顶部/底部黑条以获得电影感 |
| `linkedin` | 1920x1080（16:9） | 无 |

时间线上的每个剪辑必须缩放/裁切到该画布。对于 `social_short`，这通常意味着对 16:9 素材进行中心裁切。对于 `youtube` 并带有电影感 2.35:1 黑条处理，在 1920x1080 画布上添加 140px 顶部和底部黑色填充。

将此提交到 `render_report.metadata.canvas` 和 `render_report.metadata.letterbox`。

### 2. 为 `video_compose` 构建串联计划

剪辑工件给你一个带有入/出点、过渡和来源 asset_id 的剪辑列表。遍历 asset_manifest 将每个 asset_id 解析为真实文件路径。然后构建渲染计划。

对于如此简单的流水线，最清晰的路径是：

```python
video_compose.execute({
    "operation": "render",
    "output_path": "projects/<name>/renders/final.mp4",
    "edit_decisions": edit_decisions_with_renderer_family,
    "asset_manifest": asset_manifest,
})
```

确切的字段名来自渲染时的实时 `video_compose` 模式 — 在写调用之前，如果可用，先查阅工具的 `agent_skills`。不要发明参数。

`edit_decisions_with_renderer_family` 意味着正常的编辑工件，其中 `renderer_family = "documentary-montage"` 保持不变。

### 3. 通过 LUT 而非逐剪辑应用调色

读取 `edit_decisions.metadata.grade_profile`。映射到 LUT 文件：

| 配置 | LUT | 适合 |
|---------|-----|-------|
| `warm_film_100` | 复古胶片温暖感，轻微提亮 | 挽歌式、梦幻式 |
| `cool_archive_60` | 冷色高光、压暗暗部 | 紧迫式、诙谐式 |
| `neutral_doc_20` | 几乎不可察觉的中性平衡 | 敬畏式 |
| `bleach_bypass_80` | 去饱和、高对比度 | 诙谐式、纪录片式硬朗 |

如果配置不在样式库中，使用 `neutral_doc_20` 并在 `warnings` 中注明。不要尝试自动调色 — LUT 是整个基调平滑处理的关键。

在合成级别应用 LUT，而不是逐剪辑。一个 LUT，一条时间线，一个一致的观感。这就是让 1962 年的 Prelinger 剪辑和 2023 年的 Pexels 剪辑感觉像同一部电影的原因。

### 4. 在合成中一次性混音音频

编辑工件已经决定了音量、淡入淡出、静音窗口和 L-cut 音效层。你的任务是忠实执行它们：

- 音乐基底音量 `edit_decisions.audio.music.volume`（默认 0.7）。
- 按 `fade_in_seconds` 淡入，按 `fade_out_seconds` 淡出。
- 静音窗口 = 在窗口持续时间内衰减到 0.0，以 0.2 秒的保持时间渐回。
- L-cut 音效层 = 以 0.5-0.7 音量混音，在音乐下方。
- 除非 `edit_decisions.audio.narration` 中明确存在旁白，否则没有旁白。

**音乐是强制要求的。** 如果剪辑没有音乐条目，检查概要：

- `brief.metadata.music_plan.source == "none"` 附带 `opt_out_reason` → 用户明确选择不使用。渲染静音并在 `render_report.warnings` 中注明。
- 其他情况 → **停止。** 这是合同违规。在渲染前向用户上报。在音乐强制要求的概要上渲染静音是本流水线中最响亮的失败模式。

不要添加环境噪音"来填补空白"。

### 4b. 通过 Remotion 渲染尾标

尾标通过 Remotion **单独**渲染，与 FFmpeg 主体分开。这使两个渲染引擎（FFmpeg 负责素材，Remotion 负责排版）保持清晰分离。合成方法取决于 `brief.metadata.end_tag_plan.mode`。

读取 `brief.metadata.end_tag_plan`：

```json
{
  "text": "WE BUILT BOTH WITH THE SAME HANDS.",
  "palette": "warm_ivory_on_black",
  "duration_seconds": 5.5,
  "render_engine": "remotion",
  "component": "EndTag",
  "mode": "overlay"
}
```

#### 路径 A — 叠加模式（默认）

标签在主体素材的最后场景上淡入。这是默认模式，产生更电影感的结果 — 排版出现在现场素材之上，而不是切换到黑卡。

**执行方法：**

1. 通过 FFmpeg 合成主体（剪辑 + LUT + 音乐 + 静音窗口）。保存为 `projects/<name>/renders/body.mp4`。注意主体 fps。
2. 计算 `durationInFrames = round(duration_seconds × body_fps)`。
3. 通过 Remotion CLI 渲染带 alpha 的尾标：
   ```bash
   npx remotion render src/index.tsx EndTagOverlay \
     projects/<name>/renders/end_tag_overlay.mov \
     --codec=prores --prores-profile=4444 \
     --pixel-format=yuva444p10le --image-format=png \
     --props='{"text":"...","palette":"...","overlay":true,
               "fadeInSeconds":1.0,"holdSeconds":3.0,"fadeOutSeconds":1.5}'
   ```
   使用 `overlay: true` 的 `EndTagOverlay` 合成。这将生成带有真实 alpha 通道的 ProRes 4444 MOV（pix_fmt=yuva444p12le）。画布必须与主体画布匹配。
4. 计算叠加偏移：
   - 如果存在，读取 `edit_decisions.end_tag.offset_seconds`。
   - 否则自动计算：`offset = body_duration - tag_duration`。标签的淡出应与主体的关闭淡出对齐。
5. 通过 FFmpeg overlay 和 `-itsoffset` 合成：
   ```bash
   ffmpeg -y \
     -i body.mp4 \
     -itsoffset {offset} -i end_tag_overlay.mov \
     -filter_complex "[0:v][1:v]overlay=0:0:format=auto:eof_action=pass[v]" \
     -map "[v]" -map "0:a" \
     -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
     -c:a aac -b:a 192k \
     projects/<name>/renders/final.mp4
   ```
   `eof_action=pass` 意味着主体视频在叠加结束后继续。叠加自身的 alpha 处理淡入/停留/淡出。

**验证：** 从叠加区域提取一帧（例如 `offset + 2s`）并确认文字在素材上可见，而不是在黑色上。如果帧显示文字后面有黑色背景，则 alpha 通道丢失 — 使用 `--image-format=png` 重新渲染。

#### 路径 B — 拼接模式

经典尾卡：在主体后附加不透明黑卡。仅在 `end_tag_plan.mode == "concat"` 时使用。

**执行方法：**

1. 如上合成主体。
2. 渲染尾标为不透明 MP4：
   ```bash
   npx remotion render src/index.tsx EndTag \
     projects/<name>/renders/end_tag.mp4 \
     --props='{"text":"...","palette":"...","durationInFrames":132}'
   ```
   （5.5 秒在 24fps 下 = 132 帧）。画布必须与主体画布匹配。
3. 拼接主体 + 尾标：
   ```bash
   ffmpeg -f concat -safe 0 -i list.txt -c copy final.mp4
   ```
   如果编码器不匹配则重新编码。

#### 通用规则（两种模式）

**尾标是强制要求的。** 跳过它的唯一方式是用户明确选择不使用，记录为 `end_tag_plan: null` 并附带 `end_tag_opt_out_reason`。如果概要中有尾标计划但你跳过了渲染，那是合同违规。在最终确定前停止并上报。

在 `render_report` 中记录：
- `end_tag_rendered: true | false`
- `end_tag_mode: "overlay" | "concat"`
- `end_tag_path: "projects/<name>/renders/end_tag_overlay.mov"`（或 `.mp4` 用于 concat）
- `end_tag_offset_seconds: <number>`（仅叠加模式）
- `end_tag_text: "..."`（用于审计追踪）

如果概要说"不要音乐"且剪辑正确没有音乐条目且 `music_plan.source == "none"` 带有 opt-out 原因，渲染静音。不要添加环境噪音"来填补空白"。

### 5. 以纪录片规格渲染

纪录片蒙太奇的推荐编码器设置：

| 字段 | 值 | 原因 |
|-------|-------|-----|
| 编码器 | `libx264`（H.264） | 通用、小巧 |
| 像素格式 | `yuv420p` | 通用兼容性 |
| CRF | `18` | 最终交付物视觉无损 |
| FPS | `24` | 电影感。不要将 24 升频到 30。 |
| 音频编码器 | `aac` | 通用 |
| 音频比特率 | `192k` | 音乐基底友好 |

如果源剪辑是 30fps 而画布是 24fps，让渲染管道均匀丢帧 — 不要混合。混合来源素材上的运动插值看起来很糟糕。

### 6. 渲染后验证

渲染成功后，实际探测输出文件并检查：

- **时长。** 应在 `sum(out - in for cut in cuts) + 淡入/淡出` 的 ±0.5 秒内。
- **分辨率。** 应与画布匹配。
- **音频存在。** 如果计划中有音乐，输出必须有音频流。如果计划静音，确认。
- **第一帧和最后一帧。** 打开文件，跳转到 0 秒和 duration-0.1 秒。第一帧应为淡入。最后一帧应为黑色（或正在淡出到黑色）。
- **静音窗口。** 跳转到静音窗口开始。音频电平应在波形中明显下降。

在 `render_report.verification_notes` 中记录验证。

### 7. 输出渲染报告

```json
{
  "version": "1.0",
  "outputs": [
    {
      "path": "projects/<name>/renders/final.mp4",
      "format": "mp4",
      "codec": "h264",
      "audio_codec": "aac",
      "resolution": "1920x1080",
      "fps": 24,
      "duration_seconds": 89.8,
      "file_size_bytes": 18234112,
      "platform_target": "youtube"
    }
  ],
  "render_time_seconds": 42.3,
  "warnings": [],
  "verification_notes": [
    "时长在计划值的 +0.2 秒内",
    "第一帧为指定的黑色淡入",
    "静音窗口 54-56 秒已确认（音乐 -60dB）",
    "最后一帧在 89.0 秒淡出到黑色"
  ],
  "render_grammar": "documentary-montage",
  "metadata": {
    "pipeline": "documentary-montage",
    "canvas": { "width": 1920, "height": 1080 },
    "letterbox": "2.35:1",
    "lut": "warm_film_100",
    "music_present": true
  }
}
```

### 8. 质量门

- 输出文件存在且可播放。
- 时长在 `brief.duration_seconds` 的 ±1 秒内（主体 + 尾标合计）。
- 分辨率与 `target_platform` 画布匹配。
- LUT 已应用（或记录警告）。
- **音乐存在**，除非 `brief.metadata.music_plan.source == "none"` 带有明确的 opt-out 原因。
- **尾标 MP4 已渲染并拼接**，除非 `brief.metadata.end_tag_plan` 为 null 带有明确的 opt-out 原因。最终 MP4 的最后一帧必须是该情况下的尾标卡片。
- 第一帧和最后一帧已验证。
- 静音窗口（如有）已在波形中验证。
- 没有未经概要批准的旁白。
- `render_report.warnings` 列出每一次替代。
- `render_report.metadata.music_mixed = true` 且 `render_report.metadata.end_tag_rendered = true`（或记录了明确的 opt-out）。

## 常见陷阱

- **让混合年代的剪辑未加调色就渲染。** 作品看起来会像互联网剪辑的 PowerPoint 幻灯片。LUT 是不可协商的。
- **通过升频而不是信箱模式来匹配画布。** Prelinger 640x480 升频到 1920x1080 看起来像素化和错误。用信箱黑条居中它，或者将方形裁切作为一种设计选择。
- **添加旁白或环境音效"来填补空白"。** 重大变更，需要用户批准。
- **逐剪辑调色。** 整个作品一个 LUT。不要尝试单独平衡每个剪辑 — 花费 10 倍的时间，使基调更不一致，而不是更多。
- **悄悄降级到 FFmpeg。** 如果 Remotion 被阻止而你路由到 FFmpeg 却没有上报，你就改变了批准的渲染路径。在渲染前停止并上报该降级。
- **在渲染时覆盖编辑决策。** 如果你发现在渲染调用中调整音量、淡入淡出或修剪，你就是在合成过程中编辑。回到剪辑阶段，修复决策，重新输出工件，然后重新渲染。
- **跳过验证。** 一个"成功"但实际上是静音、或淡出错误、或剪掉了最后英雄帧的渲染，比失败更糟糕。打开文件。

## 当渲染失败时

如果 `video_compose` 返回错误：

1. 根据决策沟通合同检查错误类别（认证/提供者/工具缺陷/计划质量）。
2. 如果是路径错误，验证资产清单中的每个 asset_id → 路径解析。一个文件缺失就会导致整个渲染失败。
3. 如果是编码器错误，输入剪辑可能包含不常见的容器（Archive.org 有时提供 Matroska）。先尝试通过 `video_trimmer` 运行每个输入以标准化为 mp4/h264。
4. 如果是内存或超时错误，将渲染分成两半，最后用 `video_stitch` 合并。
5. 在切换到低保真路径之前向用户上报。本流水线是素材主导的，没有生成静态图片的回退方案。
