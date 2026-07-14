# 合成导演 - 本地化配音流水线

## 使用时机

渲染本地化输出。质量标准是可理解性、时序连贯性和每个语言包的清晰版本标签。

## 运行时路由（硬性约束 — 仅限 Remotion 或 FFmpeg）

第一阶段从 HyperFrames 推迟。`edit_decisions.render_runtime` 必须为 `"remotion"` 或 `"ffmpeg"`。本地化依赖于 Remotion 的字幕栈（按地区字幕烧录），当配音带唇形同步时，还依赖于 Remotion TalkingHead 流水线。HyperFrames 在第一阶段对两者均无对等功能。

- 如果 `edit_decisions.render_runtime == "hyperframes"`，停止。重新打开 idea 阶段并呈现约束条件 — 不要默默重写运行时。
- 根据 AGENT_GUIDE.md → "呈现两种合成运行时（硬性规则）"：流水线的约束条件并不能跳过与用户的沟通。向用户说明约束条件，让他们知道 HyperFrames 存在但在此处不可用。记录一个 `render_runtime_selection` 决策，其中 hyperframes 的 `rejected_because: "caption + lip-sync parity deferred on localization-dub"`。
- 将 `proposal_packet`/`brief` 传递给 `video_compose.execute()` 以实现端到端运行时切换检测。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/render_report.schema.json` | 工件验证 |
| 前置工件 | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | 按地区渲染指令 |
| 工具 | `video_compose`、`audio_mixer`、`video_trimmer`、`audio_enhance` | 最终渲染和音频后期 |
| 剧本 | 活跃的风格剧本 | 字幕位置和输出质量 |

## 流程

### 1. 按地区渲染

将每种目标语言视为一组独立的交付物。确保名称和输出目录明确。

### 2. 预期时序调整

预留以下情况的空间：

- 字幕重排
- 配音音频时长偏差
- 较长的行动号召（CTA）停留时间
- 可选的修剪或覆盖段落

### 3. 验证每个地区

在以下位置记录重要发现：

- `render_report.verification_notes`
- `render_report.warnings`
- `render_report.metadata.locale_notes`

检查：

- 可理解性
- 字幕适配
- 明显的同步偏差
- 版本标签

### 4. 质量门禁

- 每个地区的输出都存在
- 配音和字幕时序可接受
- 标签和文件名无歧义
- 警告得以保留

## 常见陷阱

- 将所有地区视为时序一致来渲染
- 翻译后忘记重新检查字幕行长度
- 命名输出时隐藏了地区或处理模式信息
