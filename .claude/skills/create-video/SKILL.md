---
name: create-video
description: |
  Create videos from a text prompt using HeyGen's Video Agent. Use when: (1) Creating a video from a description or idea, (2) Generating explainer, demo, or marketing videos from a prompt, (3) Making a video without specifying exact avatars, voices, or scenes, (4) Quick video prototyping or drafts, (5) One-shot prompt-to-video generation, (6) User says "make me a video" or "create a video about X".
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

从文本提示生成完整视频。描述您想要的内容，AI 会自动处理脚本编写、虚拟形象选择、视觉效果、配音、节奏和字幕。

## 认证

所有请求都需要 `X-Api-Key` 请求头。请设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X POST "https://api.heygen.com/v1/video_agent/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "创建一段60秒的产品演示视频。"}'
```

## 工具选择

如果有 HeyGen MCP 工具可用（`mcp__heygen__*`），**优先使用它们**而非直接 HTTP API 调用——它们会自动处理认证和请求格式化。

| 任务 | MCP 工具 | 回退方案（直接 API） |
|------|----------|----------------------|
| 从提示词生成视频 | `mcp__heygen__generate_video_agent` | `POST /v1/video_agent/generate` |
| 检查视频状态/获取 URL | `mcp__heygen__get_video` | `GET /v2/videos/{video_id}` |
| 列出账户视频 | `mcp__heygen__list_videos` | `GET /v2/videos` |
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v2/videos/{video_id}` |

如果没有 HeyGen MCP 工具可用，则按照参考文件中记录的方案使用直接 HTTP API 调用。

## 默认工作流程

始终使用 [prompt-optimizer.md](references/prompt-optimizer.md) 的指南来构建包含场景、时间和视觉风格的提示词。

**使用 MCP 工具：**
1. 使用 [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) 编写优化后的提示词
2. 使用提示词和配置（duration_sec、orientation、avatar_id）调用 `mcp__heygen__generate_video_agent`
3. 使用返回的 video_id 调用 `mcp__heygen__get_video` 轮询状态并获取下载 URL

**不使用 MCP 工具（直接 API）：**
1. 使用 [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) 编写优化后的提示词
2. `POST /v1/video_agent/generate` — 参见 [video-agent.md](references/video-agent.md)
3. `GET /v2/videos/<id>` — 参见 [video-status.md](references/video-status.md)

## 快速参考

| 任务 | MCP 工具 | 参考文档 |
|------|----------|------|
| 从提示词生成视频 | `mcp__heygen__generate_video_agent` | [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) → [video-agent.md](references/video-agent.md) |
| 检查视频状态/获取下载 URL | `mcp__heygen__get_video` | [video-status.md](references/video-status.md) |
| 上传提示词的参考文件 | — | [assets.md](references/assets.md) |

## 何时使用此技能 vs Avatar Video

此技能适用于**基于提示词的视频创建**——描述您想要的内容，AI 负责其余部分。

如果用户需要**精确控制**特定虚拟形象、精确脚本、逐场景语音/背景配置或多场景组合，请改用 **avatar-video** 技能。

| 用户表述 | 此技能 | Avatar Video 技能 |
|-----------|:----------:|:------------------:|
| "帮我做一个关于 X 的视频" | ✓ | |
| "创建一个产品演示" | ✓ | |
| "我想要虚拟形象 Y 精确地说 Z" | | ✓ |
| "多场景不同背景的视频" | | ✓ |
| "用于合成的透明 WebM" | | ✓ |

## 参考文件

### 核心工作流
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - 编写有效的提示词（核心工作流 + 规则）
- [references/visual-styles.md](references/visual-styles.md) - 20 种命名视觉风格的完整规格
- [references/prompt-examples.md](references/prompt-examples.md) - 完整生产级提示词示例 + 即用模板
- [references/video-agent.md](references/video-agent.md) - Video Agent API 端点详情

### 基础
- [references/video-status.md](references/video-status.md) - 轮询模式和下载 URL
- [references/webhooks.md](references/webhooks.md) - Webhook 端点和事件
- [references/assets.md](references/assets.md) - 上传图片、视频、音频作为参考
- [references/dimensions.md](references/dimensions.md) - 分辨率和宽高比
- [references/quota.md](references/quota.md) - 积分系统和用量限制

## 最佳实践

1. **优化提示词** — 平庸与专业效果之间的差距完全取决于提示词质量。始终使用提示词优化器
2. **指定时长** — 使用 `config.duration_sec` 获得可预测的视频长度
3. **必要时锁定虚拟形象** — 使用 `config.avatar_id` 确保视频间的一致性
4. **上传参考文件** — 帮助 AI 理解您的品牌/产品
5. **迭代优化提示词** — 根据结果进行调整；Video Agent 非常适合快速迭代
