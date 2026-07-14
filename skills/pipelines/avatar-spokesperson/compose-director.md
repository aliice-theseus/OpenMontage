# 合成总监 - 虚拟形象发言人管线

## 使用时机

渲染最终的发言人输出。标准很简单：主持人必须看起来稳定，语音必须清晰，字幕或辅助卡片不能拥挤画面。

## 运行时路由（硬性约束 — 仅限 Remotion）

Phase 1 从 HyperFrames 延迟处理。`edit_decisions.render_runtime` 必须为 `"remotion"`。此管线依赖 Remotion 的 `TalkingHead` 合成组件和 `remotion_caption_burn` — 两者在 Phase 1 中均未与 HyperFrames 实现功能对等。

- 如果 `edit_decisions.render_runtime == "hyperframes"`，停止。重新打开 idea 阶段并暴露该约束。静默改写是治理违规。
- 根据 AGENT_GUIDE.md → "展示两种合成运行时（硬性规则）"：锁定 remotion 不是跳过对话的借口。用户有权知道 HyperFrames 作为运行时的存在，以及为什么它不适用于 avatar-spokesperson。记录 `render_runtime_selection` 决策，hyperframes 设为 `rejected_because: "TalkingHead + caption parity deferred on avatar-spokesperson"`。
- 将 `proposal_packet`/`brief` 传递给 `video_compose.execute()` 以实现在工具内检测运行时切换。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/render_report.schema.json` | 工件验证 |
| 前置工件 | `state.artifacts["edit"]["edit_decisions"]`、`state.artifacts["assets"]["asset_manifest"]` | 要渲染的内容 |
| 工具 | `video_compose`、`audio_mixer`、`video_stitch`、`audio_enhance` | 渲染和音频后期处理 |
| 剧本 | 当前风格剧本 | 排版和布局规则 |

## 流程

### 1. 先渲染主角版本

在衍生版本之前，优先制作一个强力的母版。合成内容包括：

- 主持人视频，
- 字幕，
- 下方三分之一，
- CTA 卡片，
- 混合旁白。

### 2. 保持画面整洁

字幕和 CTA 的放置比花哨的转场更重要。确保面部和嘴部区域不被遮挡。

### 3. 验证口型时序和音频

如果虚拟形象路径使用了唇形同步或音频驱动说话头像，请检查：

- 口型时序，
- 面部伪影，
- 长段落的漂移，
- 音频清晰度。

### 4. 验证每个输出

在以下位置记录重要发现：

- `render_report.verification_notes`
- `render_report.warnings`
- `render_report.metadata.variant_notes`

### 5. 质量门禁

- 输出文件有效，
- 语音清晰，
- 字幕保持可读，
- 主持人保持视觉稳定。

## 常见陷阱

- 让字幕遮挡下巴或嘴部区域。
- 未抽查漂移就发布长段唇形同步渲染。
- 制作切掉主持人或 CTA 的衍生裁切版本。
