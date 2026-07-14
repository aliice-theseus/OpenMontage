# 合成导演 - Clip Factory 流水线

## 使用时机

独立渲染每个剪辑和平台变体。此处的重要行为是一致性、批次弹性以及部分失败的清晰报告。

## 运行时路由（硬性约束 — 仅限 Remotion 或 FFmpeg）

此流水线在 HyperFrames 采用计划中被推迟到第一阶段。`edit_decisions.render_runtime` 必须是 `"remotion"`（默认）或 `"ffmpeg"`（纯拼接的剪辑任务，无合成）。**HyperFrames 在此处不是有效的运行时** — clip-factory 依赖 Remotion 的逐词字幕烧录，而 HyperFrames 的字幕对等功能已被推迟。

- 如果 `edit_decisions.render_runtime == "hyperframes"`，停止。重新打开 idea 阶段，让用户了解真实的约束条件，并用 `render_runtime_selection` 决策锁定 `remotion`，记录 `hyperframes` 为 `rejected_because: "caption-burn parity deferred on clip-factory"`。
- 根据 AGENT_GUIDE.md → "展示两种合成运行时（硬性规则）"：约束条件不是跳过对话的借口。用户仍然需要知道 HyperFrames 存在以及为什么在此处不可行。
- 将 `proposal_packet`/`brief` 传递给 `video_compose.execute()`，以便工具内的运行时切换检查端到端运行。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 制品验证 |
| 前置制品 | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | 剪辑编辑和资源 |
| 工具 | `video_trimmer`, `video_compose`, `audio_mixer`, `color_grade` | 渲染流水线 |
| 媒体配置 | `lib/media_profiles.py` | 平台目标 |

## 流程

### 1. 将每个输出视为独立任务

一个剪辑跨三个平台就是三个渲染任务。明确命名并追踪它们。

### 2. 复用可共享的内容

- 尽可能共享音频混音，
- 共享字幕样式，
- 共享覆盖层资源，
- 如果视频源需要，共享调色方案。

### 3. 优雅地处理失败

如果某个剪辑或某个平台变体失败：

- 清晰记录日志，
- 继续渲染批次的其他部分，
- 不阻塞已成功的导出。

### 4. 验证每个输出

每次渲染：

- 正确的时长，
- 正确的分辨率/宽高比，
- 无黑色开场帧，
- 钩子准时出现，
- 字幕正确渲染，
- 音频存在且一致。

### 5. 使用渲染报告元数据

推荐的元数据键：

- `job_index`
- `failed_jobs`
- `shared_intermediates`
- `platform_groupings`

## 常见陷阱

- 任务独立时却无理由地串行渲染。
- 将某个剪辑失败视为停止整批处理的理由。
- 让某个平台变体悄悄地使用了错误的构图或字幕区域。
