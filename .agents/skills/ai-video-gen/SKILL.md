---
name: ai-video-gen
description: |
  使用 HeyGen API 网关从文本提示生成 AI 视频。在以下情况下使用：(1) 从文本描述生成视频，(2) 为内容制作创建 AI 生成的视频片段，(3) 使用参考图片进行图生视频生成，(4) 在视频生成提供商（VEO、Kling、Sora、Runway、Seedance、MiniMax）之间选择。Seedance 2.0 另可通过火山引擎 Ark 直连（`seedance_video` 工具）。
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env_any:
        - HEYGEN_API_KEY
---

# 视频生成（多网关）

从文本提示生成 AI 视频。通过 HeyGen API 网关支持多个提供商；Seedance 2.0 另可通过火山引擎 Ark 直连。

| 网关 | 环境变量 | 提供商 | 工具 |
|---------|-------------|-----------|------|
| **HeyGen** | `HEYGEN_API_KEY` | VEO 3.1、Kling Pro、Sora v2、Runway Gen-4、Seedance Pro / Lite（1.x） | `heygen_video` |
| **火山引擎 Ark**（直连） | `ARK_API_KEY` | **Seedance 2.0**（标准 + 快速） | `seedance_video` |

**首选高级默认 — Seedance 2.0。** 当配置了 `ARK_API_KEY`（火山引擎 Ark 直连 `seedance_video`，或 HeyGen 的视频代理/头像拍摄路径）时，Seedance 2.0 是电影、预告片和高保真片段工作的首选默认模型。它是整个产品线中唯一具备**单通道原生同步音频、多镜头生成、导演级摄像机控制和引用对话的口型同步**的模型，并在 2026 年初的 Artificial Analysis Elo 排行榜上排名第一。仅在用户有特定原因（预算、提供商偏好、风格适配如 VEO 适合写实风景、Kling 适合特定动漫风格）时才切换它。有关权威的提示词和参数指南，请参见第 3 层 `seedance-2-0`。

**重要提示：** 始终使用 `video_selector` 而不是直接调用提供商工具。选择器会处理可用性检查、成本比较和自动回退，其评分引擎已经偏向于电影意图下的 Seedance 2.0。

## 认证

使用最能匹配用户可用提供商和成本/质量目标的已配置网关。

- **HeyGen：** 设置 `HEYGEN_API_KEY` 以访问多模型网关。
- **火山引擎 Ark（直连）：** 设置 `ARK_API_KEY` 以直连 Seedance 2.0。

在检查注册表和当前任务适配度之前，不要将任一网关描述为默认或首选。

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workflow_type": "GenerateVideoNode", "input": {"prompt": "A drone shot flying over a coastal city at sunset"}}'
```

## 默认工作流

1. 使用 `workflow_type: "GenerateVideoNode"` 和您的提示调用 `POST /v1/workflows/executions`
2. 在响应中收到一个 `execution_id`
3. 每 10 秒轮询 `GET /v1/workflows/executions/{id}` 直到状态为 `completed`
4. 使用输出中返回的 `video_url`

## 执行视频生成

### 端点

`POST https://api.heygen.com/v1/workflows/executions`

### 请求字段

| 字段 | 类型 | 必填 | 描述 |
|-------|------|:---:|-------------|
| `workflow_type` | string | Y | 必须为 `"GenerateVideoNode"` |
| `input.prompt` | string | Y | 要生成视频的文本描述 |
| `input.provider` | string | | 视频生成提供商（默认：`"veo_3_1"`）。见下方提供商列表。 |
| `input.aspect_ratio` | string | | 宽高比（默认：`"16:9"`）。常用值：`"16:9"`、`"9:16"`、`"1:1"` |
| `input.reference_image_url` | string | | 图生视频的参考图片 URL |
| `input.tail_image_url` | string | | 尾帧引导图片 URL |
| `input.config` | object | | 提供商特定的配置覆盖 |

### 提供商

| 提供商 | 值 | 描述 |
|----------|-------|-------------|
| VEO 3.1 | `"veo_3_1"` | Google VEO 3.1（默认，最高质量） |
| VEO 3.1 Fast | `"veo_3_1_fast"` | 更快的 VEO 3.1 变体 |
| VEO 3 | `"veo3"` | Google VEO 3 |
| VEO 3 Fast | `"veo3_fast"` | 更快的 VEO 3 变体 |
| VEO 2 | `"veo2"` | Google VEO 2 |
| Kling Pro | `"kling_pro"` | Kling Pro 模型 |
| Kling V2 | `"kling_v2"` | Kling V2 模型 |
| Sora V2 | `"sora_v2"` | OpenAI Sora V2 |
| Sora V2 Pro | `"sora_v2_pro"` | OpenAI Sora V2 Pro |
| Runway Gen-4 | `"runway_gen4"` | Runway Gen-4 |
| Seedance Lite | `"seedance_lite"` | Seedance Lite |
| Seedance Pro | `"seedance_pro"` | Seedance Pro |
| LTX Distilled | `"ltx_distilled"` | LTX Distilled（最快） |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "GenerateVideoNode",
    "input": {
      "prompt": "A drone shot flying over a coastal city at golden hour, cinematic lighting",
      "provider": "veo_3_1",
      "aspect_ratio": "16:9"
    }
  }'
```

### TypeScript

```typescript
interface GenerateVideoInput {
  prompt: string;
  provider?: string;
  aspect_ratio?: string;
  reference_image_url?: string;
  tail_image_url?: string;
  config?: Record<string, any>;
}

interface ExecuteResponse {
  data: {
    execution_id: string;
    status: "submitted";
  };
}

async function generateVideo(input: GenerateVideoInput): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/workflows/executions", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      workflow_type: "GenerateVideoNode",
      input,
    }),
  });

  const json: ExecuteResponse = await response.json();
  return json.data.execution_id;
}
```

### Python

```python
import requests
import os

def generate_video(
    prompt: str,
    provider: str = "veo_3_1",
    aspect_ratio: str = "16:9",
    reference_image_url: str | None = None,
    tail_image_url: str | None = None,
) -> str:
    payload = {
        "workflow_type": "GenerateVideoNode",
        "input": {
            "prompt": prompt,
            "provider": provider,
            "aspect_ratio": aspect_ratio,
        },
    }

    if reference_image_url:
        payload["input"]["reference_image_url"] = reference_image_url
    if tail_image_url:
        payload["input"]["tail_image_url"] = tail_image_url

    response = requests.post(
        "https://api.heygen.com/v1/workflows/executions",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json=payload,
    )

    data = response.json()
    return data["data"]["execution_id"]
```

### 响应格式

```json
{
  "data": {
    "execution_id": "node-gw-v1d2e3o4",
    "status": "submitted"
  }
}
```

## 检查状态

### 端点

`GET https://api.heygen.com/v1/workflows/executions/{execution_id}`

### curl

```bash
curl -X GET "https://api.heygen.com/v1/workflows/executions/node-gw-v1d2e3o4" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### 响应格式（已完成）

```json
{
  "data": {
    "execution_id": "node-gw-v1d2e3o4",
    "status": "completed",
    "output": {
      "video": {
        "video_url": "https://resource.heygen.ai/generated/video.mp4",
        "video_id": "abc123"
      },
      "asset_id": "asset-xyz789"
    }
  }
}
```

## 轮询等待完成

```typescript
async function generateVideoAndWait(
  input: GenerateVideoInput,
  maxWaitMs = 600000,
  pollIntervalMs = 10000
): Promise<{ video_url: string; video_id: string; asset_id: string }> {
  const executionId = await generateVideo(input);
  console.log(`已提交视频生成：${executionId}`);

  const startTime = Date.now();
  while (Date.now() - startTime < maxWaitMs) {
    const response = await fetch(
      `https://api.heygen.com/v1/workflows/executions/${executionId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );
    const { data } = await response.json();

    switch (data.status) {
      case "completed":
        return {
          video_url: data.output.video.video_url,
          video_id: data.output.video.video_id,
          asset_id: data.output.asset_id,
        };
      case "failed":
        throw new Error(data.error?.message || "视频生成失败");
      case "not_found":
        throw new Error("工作流未找到");
      default:
        await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
  }

  throw new Error("视频生成超时");
}
```

## 使用示例

### 简单的文字转视频

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "GenerateVideoNode",
    "input": {
      "prompt": "A person walking through a sunlit park, shallow depth of field"
    }
  }'
```

### 图生视频

```json
{
  "workflow_type": "GenerateVideoNode",
  "input": {
    "prompt": "Animate this product photo with a slow zoom and soft particle effects",
    "reference_image_url": "https://example.com/product-photo.png",
    "provider": "kling_pro"
  }
}
```

### 社交媒体竖屏格式

```json
{
  "workflow_type": "GenerateVideoNode",
  "input": {
    "prompt": "A trendy coffee shop interior, camera slowly panning across the counter",
    "aspect_ratio": "9:16",
    "provider": "veo_3_1"
  }
}
```

### 使用 LTX 快速生成

```json
{
  "workflow_type": "GenerateVideoNode",
  "input": {
    "prompt": "Abstract colorful shapes morphing and flowing",
    "provider": "ltx_distilled"
  }
}
```

## 最佳实践

1. **在提示词中要描述详细** — 包含摄像机运动、光照、风格和情绪细节
2. **默认使用 Seedance 2.0（通过 `seedance_video`）进行电影和运动导向的工作**，当已设置 `ARK_API_KEY` 时 — 单通道同步音频、多镜头、口型同步、导演级摄像机。当用户特别想要 Google 或 OpenAI 的运动角色时使用 VEO 3.1 / Sora V2 Pro；仅在速度是硬约束时使用 `ltx_distilled` 或 `veo3_fast`
3. **使用参考图片** 进行图生视频 — 非常适合动画化产品照片或静态图像
4. **视频生成是最慢的工作流** — 允许最多 5 分钟，每 10 秒轮询一次
5. **宽高比很重要** — 社交媒体故事/短视频用 `9:16`，横屏用 `16:9`，方形用 `1:1`
6. **输出包含 `asset_id`** — 用它来在其他 HeyGen 工作流中引用生成的视频
7. **输出 URL 是临时的** — 及时下载或保存生成的视频
