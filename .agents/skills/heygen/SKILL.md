---
name: heygen
description: |
  [已弃用] 请使用 `create-video` 进行基于提示的视频生成，或使用 `avatar-video` 进行精确的虚拟角色/场景控制。此遗留技能将两种工作流合并——较新的专注技能提供更清晰的指导。
homepage: https://docs.heygen.com/reference/generate-video-agent
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# HeyGen API（已弃用）

> **此技能已弃用。** 请改用专注技能：
> - **`create-video`** —— 从文本提示生成视频（Video Agent API）
> - **`avatar-video`** —— 使用特定虚拟角色、声音、脚本和场景构建视频（v2 API）

此技能保留以便向后兼容，但将在未来版本中移除。

---

用于生成AI虚拟角色说话头视频、讲解视频和演示文稿的API。

## 工具选择

如果 HeyGen MCP 工具可用（`mcp__heygen__*`），**优先使用它们**而非直接 HTTP API 调用——它们会自动处理身份验证和请求格式。

| 任务 | MCP 工具 | 回退方案（直接 API） |
|------|----------|----------------------|
| 从提示生成视频 | `mcp__heygen__generate_video_agent` | `POST /v1/video_agent/generate` |
| 检查视频状态/获取URL | `mcp__heygen__get_video` | `GET /v2/videos/{video_id}` |
| 列出账户视频 | `mcp__heygen__list_videos` | `GET /v2/videos` |
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v2/videos/{video_id}` |

如果没有可用的 HeyGen MCP 工具，请按照参考文件中的说明，使用 `X-Api-Key: $HEYGEN_API_KEY` 头进行直接 HTTP API 调用。

## 默认工作流

**优先使用 Video Agent** 处理大多数视频请求。
始终使用 [prompt-optimizer.md](references/prompt-optimizer.md) 指南来构建包含场景、时间和视觉样式的提示。

**使用 MCP 工具：**
1. 使用 [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) 编写优化提示
2. 调用 `mcp__heygen__generate_video_agent` 并传入提示和配置（duration_sec、orientation、avatar_id）
3. 调用 `mcp__heygen__get_video` 并传入返回的 video_id 来轮询状态并获取下载 URL

**没有 MCP 工具（直接 API）：**
1. 使用 [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) 编写优化提示
2. `POST /v1/video_agent/generate` —— 详见 [video-agent.md](references/video-agent.md)
3. `GET /v2/videos/<id>` —— 详见 [video-status.md](references/video-status.md)

仅在用户明确需要以下情况时使用 v2/video/generate：
- 无需 AI 修改的精确脚本
- 特定 voice_id 选择
- 每个场景不同的虚拟角色/背景
- 精确的每个场景时间控制
- 具有精确规格的编程/批量生成

## 快速参考

| 任务 | MCP 工具 | 阅读 |
|------|----------|------|
| 从提示生成视频（简单） | `mcp__heygen__generate_video_agent` | [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) → [video-agent.md](references/video-agent.md) |
| 精确控制生成视频 | — | [video-generation.md](references/video-generation.md)、[avatars.md](references/avatars.md)、[voices.md](references/voices.md) |
| 检查视频状态/获取下载 URL | `mcp__heygen__get_video` | [video-status.md](references/video-status.md) |
| 添加字幕或文本叠加 | — | [captions.md](references/captions.md)、[text-overlays.md](references/text-overlays.md) |
| 用于合成的透明视频 | — | [video-generation.md](references/video-generation.md)（WebM 部分） |
| 与 Remotion 配合使用 | — | [remotion-integration.md](references/remotion-integration.md) |

## 参考文件

### 基础
- [references/authentication.md](references/authentication.md) - API 密钥设置和 X-Api-Key 头
- [references/quota.md](references/quota.md) - 积分系统和使用限制
- [references/video-status.md](references/video-status.md) - 轮询模式和下载 URL
- [references/assets.md](references/assets.md) - 上传图像、视频、音频

### 核心视频创建
- [references/avatars.md](references/avatars.md) - 列出虚拟角色、样式、avatar_id 选择
- [references/voices.md](references/voices.md) - 列出声音、语言区域、速度/音调
- [references/scripts.md](references/scripts.md) - 编写脚本、暂停、节奏
- [references/video-generation.md](references/video-generation.md) - POST /v2/video/generate 和多场景视频
- [references/video-agent.md](references/video-agent.md) - 一次性提示视频生成
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - 编写有效的 Video Agent 提示（核心工作流 + 规则）
- [references/visual-styles.md](references/visual-styles.md) - 20种命名视觉样式及完整规格
- [references/prompt-examples.md](references/prompt-examples.md) - 完整生产提示示例 + 即用模板
- [references/dimensions.md](references/dimensions.md) - 分辨率和宽高比

### 视频自定义
- [references/backgrounds.md](references/backgrounds.md) - 纯色、图像、视频背景
- [references/text-overlays.md](references/text-overlays.md) - 使用字体和定位添加文本
- [references/captions.md](references/captions.md) - 自动生成字幕

### 高级功能
- [references/templates.md](references/templates.md) - 模板列表和变量替换
- [references/photo-avatars.md](references/photo-avatars.md) - 从照片创建虚拟角色
- [references/webhooks.md](references/webhooks.md) - Webhook 端点和事件

### 集成
- [references/remotion-integration.md](references/remotion-integration.md) - 在 Remotion 合成中使用 HeyGen
