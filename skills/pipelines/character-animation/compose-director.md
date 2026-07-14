# 合成导演 - 角色动画管线

## 目标

渲染已批准的角色动画并证明其已通过审阅。

## 运行时路由

首先读取 `edit_decisions.render_runtime`。它必须与提案中锁定的运行时一致，除非 `render_runtime_selection` 决策明确更改了它。

- `remotion`：将资源部署到 `remotion-composer/public`，构建合成 JSON，通过 `video_compose` 渲染。
- `hyperframes`：实例化一个 HyperFrames 工作区，让 `video_compose` 委托给 `hyperframes_compose`。`hyperframes lint` 和 `validate` 必须通过。
- `ffmpeg`：仅用于后期处理或简单的视频组装；不足以独立完成角色表演。

## 审阅工作流

1. 运行 `character_rig_renderer` 以生成或刷新 HyperFrames 包。浏览器预览仅是 QA/调试产物，而非渲染路径。
2. 验证渲染器是否输出了 HyperFrames `workspace_path`、合成 HTML、`asset_manifest` 和 `edit_decisions.render_runtime: "hyperframes"` 交接信息。
3. 运行 `character_animation_reviewer` 对骨架、姿态、时间线和预览进行检查。
4. 通过 `video_compose` 使用渲染器交接信息或已批准的 Remotion/HyperFrames 包渲染最终视频。交付路径为 `projects/<project-name>/renders/final.mp4`，遵循标准 OpenMontage 项目约定。
5. 运行标准的 `final_review`：ffprobe、帧采样、视觉抽查、音频抽查、承诺保留检查。

## 浏览器 QA

当 Playwright 可用时：

- 打开预览，
- 捕获开头/中间/结尾帧，
- 检查控制台错误，
- 验证角色可见，
- 比较帧差异以确保运动存在。

当 Playwright 不可用时，使用静态产物检查和 FFmpeg 帧采样，并报告可信度降低。

## 质量门槛

当 `character_qa_report.status` 为 `revise` 或 `fail` 时，不得将输出呈现为完成状态。
