# 合成导演 - 电影化流水线

## 适用场景

渲染电影化作品，精心关注调色、音频动态和帧处理。这不是一个普通的导出步骤。

## 运行时路由（强制性第一步）

读取 `edit_decisions.render_runtime`。电影化工作路由到：

- **`render_runtime="remotion"`** — 视频主导的预告片默认使用 `CinematicRenderer`。在一个基于 React 的渲染通道中整合视频片段、转场和环境叠加层。
- **`render_runtime="hyperframes"`** — 用于动态标题卡片、HTML/GSAP 驱动的预告片或视觉语法基于 HTML/CSS 的启动片风格合成。参见 `skills/core/hyperframes.md`。渲染前必须通过 `hyperframes lint` 和 `hyperframes validate`。
- **`render_runtime="ffmpeg"`** — 简单的源视频拼接，无需合成。

`delivery_promise.motion_required=true` 意味着锁定的运行时是一个承诺。静默切换到其他运行时（包括 FFmpeg Ken Burns）是严重的治理违规。如果锁定的运行时失败，按照 AGENT_GUIDE.md > "Escalate Blockers Explicitly" 升级处理。

**将 `proposal_packet` 传递给 `video_compose.execute()`**，以便工具的 `runtime_swap_detected` 检查直接与 `proposal_packet.production_plan.render_runtime` 对比。没有它，工具内部的交换检查会被跳过，只有审阅者技能能发现偏差。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/render_report.schema.json` | 制品验证 |
| 前置产物 | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | 剪辑计划和媒体素材 |
| 工具 | `video_compose`, `audio_mixer`, `video_stitch`, `video_trimmer`, `color_grade`, `audio_enhance` | 渲染和后期处理 |
| 手册 | 当前风格手册 | 后期一致性 |

## 流程

### 0. 在渲染前检查硬性要求

如果已批准的简报或场景计划将动态效果作为硬性要求，请验证渲染路径仍然保留该承诺。

- 如果 Remotion 是必需的但不可用或失败，请立即停止并向用户报告问题。
- 对于动态主导的预告片、预告精简版或智能体视频，不要切换到仅有 FFmpeg 的静态图像降级方案。
- 除非用户明确批准该降级，否则不要将作品转换为动态分镜（animatic）。
- 如果渲染引擎发生实质性变化，在渲染前告知用户并解释原因。

**强制性的 Remotion 预检（当场景计划包含任何 Remotion 场景类型——标题卡片、统计卡片、动漫/英雄标题、结尾标签、叠加层时，每次渲染前运行）：**

```bash
python -c "
from tools.tool_registry import registry
registry.discover()
info = registry.get('video_compose').get_info()
print('Render engines:', info.get('render_engines'))
print('Remotion note:', info.get('remotion_note'))
"
```

如果 Remotion 不在可用的渲染引擎中，请停止并根据决策沟通契约向用户报告。未经批准不得替换为低保真度的渲染路径。

### 1. 有目的地使用帧处理

仅当有助于作品时才使用遮幅宽屏、24fps 意图或重度调色。不要因为流水线名称叫"电影化"就应用它们。

### 2. 保留音频动态

混音应允许：

- 安静时刻，
- 冲击时刻，
- 清晰的对话或旁白，
- 可控的音乐渐强。

### 3. 验证最终情绪

检查：

- 开场帧，
- 揭示节拍，
- 最终落地，
- 字幕可读性（如适用）。

### 4. 使用渲染元数据

推荐的元数据键：

- `frame_treatment`
- `grade_profile`
- `mix_notes`
- `variant_outputs`

## 常见陷阱

- 压平音频导致作品失去动态。
- 对需要每一个像素的素材应用遮幅宽屏。
- 让调色或锐化损坏人脸或文字。
- 静默地用低保真度的静态图像导出替换被阻塞的 Remotion 渲染。
