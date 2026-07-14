---
name: avatar-video
description: |
  Create AI avatar videos with precise control over avatars, voices, scripts, scenes, and backgrounds using HeyGen's v2 API. Use when: (1) Choosing a specific avatar and voice for a video, (2) Writing exact scripts for an avatar to speak, (3) Building multi-scene videos with different backgrounds per scene, (4) Creating transparent WebM videos for compositing, (5) Using talking photos as video presenters, (6) Integrating HeyGen avatars with Remotion, (7) Batch video generation with exact specs, (8) Brand-consistent production videos with precise control.
homepage: https://docs.heygen.com/reference/create-a-video
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Avatar 视频

使用 HeyGen 的 `/v2/video/generate` API 创建 AI 虚拟形象视频，完全控制虚拟形象、语音、脚本、场景和背景。可构建精确配置的单场景或多场景视频。

## 身份认证

所有请求都需要 `X-Api-Key` 请求头。请设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X GET "https://api.heygen.com/v2/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## 工具选择

如果 HeyGen MCP 工具可用（`mcp__heygen__*`），**优先使用它们**而不是直接调用 HTTP API——它们会自动处理身份认证和请求格式化。

| 任务 | MCP 工具 | 回退方式（直接 API） |
|------|----------|----------------------|
| 检查视频状态 / 获取 URL | `mcp__heygen__get_video` | `GET /v2/videos/{video_id}` |
| 列出账户视频 | `mcp__heygen__list_videos` | `GET /v2/videos` |
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v2/videos/{video_id}` |

视频生成（`POST /v2/video/generate`）和虚拟形象/语音列表通过直接 API 调用完成——请参阅下面的参考文件。

## 默认工作流程

1. **列出虚拟形象** — `GET /v2/avatars` → 选择虚拟形象，预览它，记下 `avatar_id` 和 `default_voice_id`。详见 [avatars.md](references/avatars.md)
2. **列出语音**（如果需要） — `GET /v2/voices` → 选择与虚拟形象性别/语言匹配的语音。详见 [voices.md](references/voices.md)
3. **编写脚本** — 按每个场景一个概念来组织场景结构。详见 [scripts.md](references/scripts.md)
4. **生成视频** — `POST /v2/video/generate`，为每个场景配置虚拟形象、语音、脚本和背景。详见 [video-generation.md](references/video-generation.md)
5. **轮询完成状态** — `GET /v2/videos/{video_id}` 直到状态为 `completed`。详见 [video-status.md](references/video-status.md)

## 快速参考

| 任务 | 参考文档 |
|------|------|
| 列出和预览虚拟形象 | [avatars.md](references/avatars.md) |
| 列出和选择语音 | [voices.md](references/voices.md) |
| 编写和组织脚本 | [scripts.md](references/scripts.md) |
| 生成视频（单场景或多场景） | [video-generation.md](references/video-generation.md) |
| 添加自定义背景 | [backgrounds.md](references/backgrounds.md) |
| 添加字幕 | [captions.md](references/captions.md) |
| 添加文字叠加 | [text-overlays.md](references/text-overlays.md) |
| 创建透明 WebM 视频 | [video-generation.md](references/video-generation.md)（WebM 章节） |
| 使用模板 | [templates.md](references/templates.md) |
| 从照片创建虚拟形象 | [photo-avatars.md](references/photo-avatars.md) |
| 检查视频状态 / 下载 | [video-status.md](references/video-status.md) |
| 上传资源（图片、音频） | [assets.md](references/assets.md) |
| 与 Remotion 结合使用 | [remotion-integration.md](references/remotion-integration.md) |
| 设置 Webhook | [webhooks.md](references/webhooks.md) |

## 何时使用此技能 vs 创建视频

此技能适用于**精确控制**——您选择虚拟形象、编写确切的脚本、配置每个场景。

如果用户只想**描述一个视频创意**，让 AI 处理其余部分（脚本、虚拟形象、视觉效果），请使用 **create-video** 技能。

| 用户需求 | create-video 技能 | 此技能 |
|-----------|:------------------:|:----------:|
| "帮我做一个关于 X 的视频" | ✓ | |
| "创建一个产品演示" | ✓ | |
| "我要虚拟形象 Y 准确地说 Z" | | ✓ |
| "不同背景的多场景视频" | | ✓ |
| "用于合成的透明 WebM" | | ✓ |
| "为我的脚本使用这个特定的语音" | | ✓ |
| "按精确规格批量生成视频" | | ✓ |

## 参考文件

### 核心视频创建
- [references/avatars.md](references/avatars.md) - 列出虚拟形象、样式、avatar_id 选择
- [references/voices.md](references/voices.md) - 列出语音、语言区域、速度/音调
- [references/scripts.md](references/scripts.md) - 编写脚本、暂停、节奏
- [references/video-generation.md](references/video-generation.md) - POST /v2/video/generate 和多场景视频

### 视频自定义
- [references/backgrounds.md](references/backgrounds.md) - 纯色、图片、视频背景
- [references/text-overlays.md](references/text-overlays.md) - 添加带字体和定位的文字
- [references/captions.md](references/captions.md) - 自动生成的字幕

### 高级功能
- [references/templates.md](references/templates.md) - 模板列表和变量替换
- [references/photo-avatars.md](references/photo-avatars.md) - 从照片创建虚拟形象
- [references/webhooks.md](references/webhooks.md) - Webhook 端点和事件

### 集成
- [references/remotion-integration.md](references/remotion-integration.md) - 在 Remotion 合成中使用 HeyGen

### 基础
- [references/video-status.md](references/video-status.md) - 轮询模式和下载 URL
- [references/assets.md](references/assets.md) - 上传图片、视频、音频
- [references/dimensions.md](references/dimensions.md) - 分辨率和宽高比
- [references/quota.md](references/quota.md) - 信用系统和用量限制

## 最佳实践

1. **生成前预览虚拟形象** — 下载 `preview_image_url`，使用户在提交前可以看到虚拟形象
2. **使用虚拟形象的默认语音** — 大多数虚拟形象都有预先匹配的 `default_voice_id`，以获得自然效果
3. **回退方案：手动匹配性别** — 如果没有默认语音，确保虚拟形象和语音的性别匹配
4. **开发时使用测试模式** — 设置 `test: true` 以避免消耗积分（输出将带有水印）
5. **设置充裕的超时时间** — 视频生成通常需要 5-15 分钟，有时更长
6. **验证输入** — 在生成前检查虚拟形象和语音 ID 是否存在
