---
name: create-video
description: |
  通过 HeyGen 的 Video Agent 从文本提示创建视频。在以下情况下使用：(1) 根据描述或想法创建视频，(2) 从提示生成讲解、演示或营销视频，(3) 无需指定精确的虚拟形象、语音或场景即可制作视频，(4) 快速视频原型或草稿，(5) 一次性提示到视频的生成，(6) 用户说「给我做个视频」或「创建一个关于 X 的视频」。
homepage: https://docs.heygen.com/reference/generate-video-agent
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 创建视频

从文本提示生成完整视频。描述你想要的内容，AI 会自动处理脚本编写、虚拟形象选择、视觉、配音、节奏和字幕。

## 认证

所有请求都需要 `X-Api-Key` 头。设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X POST "https://api.heygen.com/v1/video_agent/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "创建一个 60 秒的产品演示视频。"}'
```

## 工具选择

如果 HeyGen MCP 工具可用（`mcp__heygen__*`），**优先使用它们**而不是直接 HTTP API 调用——它们会自动处理认证和请求格式化。

| 任务 | MCP 工具 | 备选（直接 API） |
|------|----------|----------------------|
| 从提示生成视频 | `mcp__heygen__generate_video_agent` | `POST /v1/video_agent/generate` |
| 检查视频状态 / 获取 URL | `mcp__heygen__get_video` | `GET /v2/videos/{video_id}` |
| 列出账户视频 | `mcp__heygen__list_videos` | `GET /v2/videos` |
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v2/videos/{video_id}` |

如果没有 HeyGen MCP 工具可用，请按参考文件中的文档使用直接 HTTP API 调用。

## 默认工作流

始终使用 [prompt-optimizer.md](references/prompt-optimizer.md) 指南来构建带有场景、时间和视觉风格的提示。

**使用 MCP 工具：**
1. 使用 [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) 编写优化后的提示
2. 调用 `mcp__heygen__generate_video_agent`，传入提示和配置（duration_sec、orientation、avatar_id）
3. 调用 `mcp__heygen__get_video`，传入返回的 video_id 以轮询状态并获取下载 URL

**没有 MCP 工具（直接 API）：**
1. 使用 [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) 编写优化后的提示
2. `POST /v1/video_agent/generate`——参见 [video-agent.md](references/video-agent.md)
3. `GET /v2/videos/<id>`——参见 [video-status.md](references/video-status.md)

## 快速参考

| 任务 | MCP 工具 | 阅读 |
|------|----------|------|
| 从提示生成视频 | `mcp__heygen__generate_video_agent` | [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) → [video-agent.md](references/video-agent.md) |
| 检查视频状态 / 获取下载 URL | `mcp__heygen__get_video` | [video-status.md](references/video-status.md) |
| 上传参考文件用于提示 | — | [assets.md](references/assets.md) |

## 何时使用此技能 vs 虚拟形象视频

此技能用于**基于提示的视频创建**——描述你想要的内容，AI 处理其余部分。

如果用户需要**精确控制**特定的虚拟形象、确切的脚本、每个场景的语音/背景配置或多场景合成，请改用 **avatar-video** 技能。

| 用户说 | 此技能 | 虚拟形象视频技能 |
|-----------|:----------:|:------------------:|
| 「给我做个关于 X 的视频」 | ✓ | |
| 「创建一个产品演示」 | ✓ | |
| 「我想要虚拟形象 Y 准确说出 Z」 | | ✓ |
| 「不同背景的多场景视频」 | | ✓ |
| 「用于合成的透明 WebM」 | | ✓ |

## 参考文件

### 核心工作流
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - 编写有效提示（核心工作流 + 规则）
- [references/visual-styles.md](references/visual-styles.md) - 20 个命名的视觉风格及完整规格
- [references/prompt-examples.md](references/prompt-examples.md) - 完整生产提示示例 + 即用模板
- [references/video-agent.md](references/video-agent.md) - Video Agent API 端点详情

### 基础
- [references/video-status.md](references/video-status.md) - 轮询模式和下载 URL
- [references/webhooks.md](references/webhooks.md) - Webhook 端点和事件
- [references/assets.md](references/assets.md) - 上传图片、视频、音频作为参考
- [references/dimensions.md](references/dimensions.md) - 分辨率和宽高比
- [references/quota.md](references/quota.md) - 积分系统和用量限制

## 最佳实践

1. **优化你的提示**——平庸和专业结果之间的区别完全取决于提示质量。始终使用提示优化器
2. **指定时长**——使用 `config.duration_sec` 来控制长度
3. **如果需要，锁定虚拟形象**——使用 `config.avatar_id` 保持视频间的一致性
4. **上传参考文件**——帮助代理理解你的品牌/产品
5. **在提示上迭代**——根据结果进行优化；Video Agent 非常适合快速迭代
