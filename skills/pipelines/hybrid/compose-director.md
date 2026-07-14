# 合成导演 - 混合流水线

## 使用时机

渲染混合项目，使源素材、支持图形和音频在所有输出中保持连贯。

## 运行时路由（必选的第一步）

读取 `edit_decisions.render_runtime`。混合工作通常使用 Remotion，因为源素材 + React 支持叠加层可以在一次渲染中干净地合成：

- **`render_runtime="remotion"`** — 默认。源素材通过 `<OffthreadVideo>`，支持图形作为 React 组件，一次渲染完成。
- **`render_runtime="hyperframes"`** — 仅当支持层为 HTML/GSAP 原生内容（例如动态文本标注、注册块）时选择。源素材仍可通过 `<video class="clip">` 方式使用，但会失去部分 Remotion 组件栈的能力。详见 `skills/core/hyperframes.md`。
- **`render_runtime="ffmpeg"`** — 在此流水线中很少使用；表示无生成支持层。

静默切换运行时是 CRITICAL 级别的治理违规。在替换之前，请按照 AGENT_GUIDE.md 上报阻塞问题。

**将 `proposal_packet` 传递给 `video_compose.execute()`**，以便工具内部的运行时切换检测直接针对提案进行检查，而非被 `skipped`。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 产物验证 |
| 前置产物 | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | 剪辑逻辑和支持素材 |
| 工具 | `video_compose`, `audio_mixer`, `video_stitch`, `video_trimmer`, `color_grade`, `audio_enhance` | 最终组装和润色 |
| Playbook | 当前样式 playbook | 输出一致性 |

## 流程

### 1. 验证源素材与支持素材的平衡

最终渲染应看起来仍像是一个带支持素材的源主导视频，而不是不相关系统的拼贴。

### 2. 检查变体完整性

对于每个输出变体，验证：

- 裁切安全性，
- 文本安全性，
- 字幕可读性，
- 音频一致性。

### 3. 保持音频连贯

源对话、旁白、音乐和音效应感觉像一个混音，而非互相争抢空间的独立层。

### 4. 使用渲染元数据

推荐的元数据键：

- `variant_outputs`
- `balance_checks`
- `subtitle_checks`
- `audio_notes`

## 常见陷阱

- 主剪版本良好，平台变体却出问题。
- 支持图形在竖屏导出中被裁剪。
- 源素材与生成部分的音频响度不一致。

