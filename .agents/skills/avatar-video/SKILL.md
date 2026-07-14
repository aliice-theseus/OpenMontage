---
name: avatar-video
description: |
  使用 HeyGen 的 v2 API 创建 AI 虚拟角色视频，精确控制虚拟角色、声音、脚本、场景和背景。用于：(1) 为视频选择特定的虚拟角色和声音，(2) 为虚拟角色编写精确的脚本，(3) 构建每个场景具有不同背景的多场景视频，(4) 创建用于合成的透明 WebM 视频，(5) 使用会说话的照片作为视频主持人，(6) 将 HeyGen 虚拟角色与 Remotion 集成，(7) 按精确规格批量生成视频，(8) 精确控制的品牌一致性制作视频。
homepage: https://docs.heygen.com/reference/create-a-video
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 虚拟角色视频

创建 AI 虚拟角色视频，完全控制虚拟角色、声音、脚本、场景和背景。使用 HeyGen 的 `/v2/video/generate` API，按精确配置构建单场景或多场景视频。

## 身份验证

所有请求都需要 `X-Api-Key` 头部。设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X GET "https://api.heygen.com/v2/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## 工具选择

如果 HeyGen MCP 工具可用（`mcp__heygen__*`），**优先使用它们**，而非直接 HTTP API 调用 — 它们会自动处理身份验证和请求格式化。

| 任务 | MCP 工具 | 回退（直接 API） |
|------|----------|-----------------|
| 检查视频状态/获取 URL | `mcp__heygen__get_video` | `GET /v2/videos/{video_id}` |
| 列出账户视频 | `mcp__heygen__list_videos` | `GET /v2/videos` |
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v2/videos/{video_id}` |

视频生成（`POST /v2/video/generate`）和虚拟角色/声音列表通过直接 API 调用完成 — 参见下面的参考文件。

## 默认工作流

1. **列出虚拟角色** — `GET /v2/avatars` → 选择虚拟角色，预览，记下 `avatar_id` 和 `default_voice_id`。参见 [avatars.md](references/avatars.md)
2. **列出声音**（如需要）— `GET /v2/voices` → 选择与虚拟角色性别/语言匹配的声音。参见 [voices.md](references/voices.md)
3. **编写脚本** — 每个场景一个概念的脚本结构。参见 [scripts.md](references/scripts.md)
4. **生成视频** — `POST /v2/video/generate`，每场景设置虚拟角色、声音、脚本和背景。参见 [video-generation.md](references/video-generation.md)
5. **轮询完成** — `GET /v2/videos/{video_id}` 直到状态为 `completed`。参见 [video-status.md](references/video-status.md)

## 快速参考

| 任务 | 阅读 |
|------|------|
| 列出和预览虚拟角色 | [avatars.md](references/avatars.md) |
| 列出和选择声音 | [voices.md](references/voices.md) |
| 编写和结构化脚本 | [scripts.md](references/scripts.md) |
| 生成视频（单场景或多场景） | [video-generation.md](references/video-generation.md) |
| 添加自定义背景 | [backgrounds.md](references/backgrounds.md) |
| 添加字幕/副标题 | [captions.md](references/captions.md) |
| 添加文字覆盖层 | [text-overlays.md](references/text-overlays.md) |
| 创建透明 WebM 视频 | [video-generation.md](references/video-generation.md)（WebM 章节） |
| 使用模板 | [templates.md](references/templates.md) |
| 从照片创建虚拟角色 | [photo-avatars.md](references/photo-avatars.md) |
| 检查视频状态/下载 | [video-status.md](references/video-status.md) |
| 上传资产（图片、音频） | [assets.md](references/assets.md) |
| 与 Remotion 配合使用 | [remotion-integration.md](references/remotion-integration.md) |
| 设置 webhook | [webhooks.md](references/webhooks.md) |

## 何时使用此技能 vs 创建视频

此技能适用于**精确控制** — 您选择虚拟角色、编写精确脚本、配置每个场景。

如果用户只想**描述一个视频创意**并让 AI 处理其余部分（脚本、虚拟角色、视觉效果），请改用 **create-video** 技能。

| 用户说 | 创建视频技能 | 此技能 |
|--------|:----------:|:------:|
| "帮我制作一个关于 X 的视频" | ✓ | |
| "创建一个产品演示视频" | ✓ | |
| "我想要虚拟角色 Y 确切地说 Z" | | ✓ |
| "不同背景的多场景视频" | | ✓ |
| "用于合成的透明 WebM" | | ✓ |
| "为我的脚本使用这个特定的声音" | | ✓ |
| "按精确规格批量生成视频" | | ✓ |

## 参考文件

### 核心视频创建
- [references/avatars.md](references/avatars.md) — 列出虚拟角色、风格、avatar_id 选择
- [references/voices.md](references/voices.md) — 列出声音、区域设置、语速/音调
- [references/scripts.md](references/scripts.md) — 编写脚本、暂停、节奏
- [references/video-generation.md](references/video-generation.md) — POST /v2/video/generate 和多场景视频

### 视频定制
- [references/backgrounds.md](references/backgrounds.md) — 纯色、图片、视频背景
- [references/text-overlays.md](references/text-overlays.md) — 添加字体和位置控制的文字
- [references/captions.md](references/captions.md) — 自动生成的字幕和副标题

### 高级功能
- [references/templates.md](references/templates.md) — 模板列表和变量替换
- [references/photo-avatars.md](references/photo-avatars.md) — 从照片创建虚拟角色
- [references/webhooks.md](references/webhooks.md) — Webhook 端点和事件

### 集成
- [references/remotion-integration.md](references/remotion-integration.md) — 在 Remotion 合成中使用 HeyGen

### 基础
- [references/video-status.md](references/video-status.md) — 轮询模式和下载 URL
- [references/assets.md](references/assets.md) — 上传图片、视频、音频
- [references/dimensions.md](references/dimensions.md) — 分辨率和宽高比
- [references/quota.md](references/quota.md) — 积分系统和使用限制

## 最佳实践

1. **在生成前预览虚拟角色** — 下载 `preview_image_url`，让用户在确定前看到虚拟角色
2. **使用虚拟角色的默认声音** — 大多数虚拟角色有预先匹配的 `default_voice_id`，效果自然
3. **回退：手动匹配性别** — 如果没有默认声音，确保虚拟角色和声音性别匹配
4. **开发时使用测试模式** — 设置 `test: true` 避免消耗积分（输出将带水印）
5. **设置充裕的超时时间** — 视频生成通常需要 5-15 分钟，有时更长
6. **验证输入** — 在生成前检查虚拟角色和声音 ID 是否存在
