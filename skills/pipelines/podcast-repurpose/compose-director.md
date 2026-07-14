# 合成导演 - 播客二次利用流水线

## 何时使用

渲染播客衍生的输出，以音频保真度作为最高优先级。视觉效果需要支持讲话内容，而非与之竞争。

## 运行时路由（硬性约束 — 仅限 Remotion 或 FFmpeg）

Phase 1 推迟了 HyperFrames 支持。`edit_decisions.render_runtime` 必须是 `"remotion"`（用于 audiogram、合成输出）或 `"ffmpeg"`（用于纯音频主导的片段导出）。HyperFrames 的字幕烧录同等功能已被推迟，播客输出依赖于 Remotion 的逐词字幕栈。

- 如果 `edit_decisions.render_runtime == "hyperframes"`，停止。重新打开 idea 阶段并向用户展示约束条件。切勿静默重写运行时。
- 根据 AGENT_GUIDE.md → "展示两种合成运行时（硬性规则）"：告知用户 HyperFrames 存在以及为何在此流水线上不可行，而非静默锁定 remotion。记录一个 `render_runtime_selection` 决策，其中 hyperframes 的 `rejected_because: "caption-burn parity deferred on podcast-repurpose"`。
- 将 `proposal_packet`/`brief` 传递给 `video_compose.execute()` 以进行端到端的运行时切换检测。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact 验证 |
| 前置 artifacts | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | 输出计划和素材路径 |
| 工具 | `video_compose`, `audio_mixer` | 渲染和混音控制 |
| Playbook | 活动样式 playbook | 品牌一致性 |

## 流程

### 1. 优先渲染最高价值的输出

优先级顺序：

1. 短视频精彩片段
2. 引用主导的片段
3. 可选的长格式伴随视频

这样可以确保最可发布的素材优先可用。

### 2. 保持音频质量

- 避免不必要的重新编码，
- 保持语音清晰稳定，
- 谨慎使用音乐，仅在不与讲话竞争时使用，
- 渲染后验证字幕同步。

### 3. 尊重平台尺寸

- `9:16` 用于短视频社交媒体
- `1:1` 用于引用主导或 Feed 安全片段
- `16:9` 用于长格式 YouTube 伴随输出

### 4. 验证每个交付物

- 正确的时长，
- 正确的宽高比，
- 可读的字幕，
- 准确的说话人归属，
- 稳定的音频，
- 一致的品牌处理。

### 5. 使用渲染报告 Metadata

推荐的 metadata 键：

- `deliverable_groups`
- `audio_notes`
- `subtitle_checks`
- `failed_outputs`

## 常见陷阱

- 让视觉处理方案降低音频质量。
- 先渲染完整的伴随视频，延迟最重要的片段。
- 忘记一个简单可读的片段胜过技术复杂但令人困惑的片段。
