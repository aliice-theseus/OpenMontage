---
name: faceswap
description: |
  使用 AI 通过 HeyGen API 在视频中换脸。在以下情况下使用：(1) 用另一张脸替换视频中的脸，(2) 从源图片将脸换到目标视频上，(3) 通过换入某人的脸来创建个性化视频，(4) 使用 HeyGen 的 /v1/workflows/executions 端点进行换脸处理。
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 换脸（HeyGen API）

使用 GPU 加速的 AI 处理，将源图片中的脸换到目标视频中。源图片提供要换入的脸，目标视频接收新脸。

## 认证

所有请求都需要 `X-Api-Key` 头。设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workflow_type": "FaceswapNode", "input": {"source_image_url": "https://example.com/face.jpg", "target_video_url": "https://example.com/video.mp4"}}'
```

## 默认工作流

1. 调用 `POST /v1/workflows/executions`，使用 `workflow_type: "FaceswapNode"`、源脸部图片和目标视频
2. 在响应中收到 `execution_id`
3. 每 10 秒轮询 `GET /v1/workflows/executions/{id}`，直到状态为 `completed`
4. 使用输出中返回的 `video_url`

## 执行换脸

### 端点

`POST https://api.heygen.com/v1/workflows/executions`

### 请求字段

| 字段 | 类型 | 必填 | 描述 |
|-------|------|:---:|-------------|
| `workflow_type` | string | Y | 必须为 `"FaceswapNode"` |
| `input.source_image_url` | string | Y | 要换入的脸部图片 URL |
| `input.target_video_url` | string | Y | 要应用换脸的视频 URL |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "FaceswapNode",
    "input": {
      "source_image_url": "https://example.com/face-photo.jpg",
      "target_video_url": "https://example.com/original-video.mp4"
    }
  }'
```

### TypeScript

```typescript
interface FaceswapInput {
  source_image_url: string;
  target_video_url: string;
}

interface ExecuteResponse {
  data: {
    execution_id: string;
    status: "submitted";
  };
}

async function faceswap(input: FaceswapInput): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/workflows/executions", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      workflow_type: "FaceswapNode",
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

def faceswap(source_image_url: str, target_video_url: str) -> str:
    payload = {
        "workflow_type": "FaceswapNode",
        "input": {
            "source_image_url": source_image_url,
            "target_video_url": target_video_url,
        },
    }

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
    "execution_id": "node-gw-f1s2w3p4",
    "status": "submitted"
  }
}
```

## 检查状态

### 端点

`GET https://api.heygen.com/v1/workflows/executions/{execution_id}`

### curl

```bash
curl -X GET "https://api.heygen.com/v1/workflows/executions/node-gw-f1s2w3p4" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### 响应格式（已完成）

```json
{
  "data": {
    "execution_id": "node-gw-f1s2w3p4",
    "status": "completed",
    "output": {
      "video_url": "https://resource.heygen.ai/faceswap/output.mp4"
    }
  }
}
```

## 轮询完成

```typescript
async function faceswapAndWait(
  input: FaceswapInput,
  maxWaitMs = 600000,
  pollIntervalMs = 10000
): Promise<string> {
  const executionId = await faceswap(input);
  console.log(`已提交换脸: ${executionId}`);

  const startTime = Date.now();
  while (Date.now() - startTime < maxWaitMs) {
    const response = await fetch(
      `https://api.heygen.com/v1/workflows/executions/${executionId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );
    const { data } = await response.json();

    switch (data.status) {
      case "completed":
        return data.output.video_url;
      case "failed":
        throw new Error(data.error?.message || "换脸失败");
      case "not_found":
        throw new Error("工作流未找到");
      default:
        await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
  }

  throw new Error("换脸超时");
}
```

## 使用示例

### 基础换脸

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "FaceswapNode",
    "input": {
      "source_image_url": "https://example.com/headshot.jpg",
      "target_video_url": "https://example.com/presentation.mp4"
    }
  }'
```

### 与 Avatar 视频链式使用

先生成 Avatar 视频，然后换入自定义脸部：

```python
import time

# 步骤 1：生成 Avatar 视频
avatar_execution_id = requests.post(
    "https://api.heygen.com/v1/workflows/executions",
    headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"], "Content-Type": "application/json"},
    json={
        "workflow_type": "AvatarInferenceNode",
        "input": {
            "avatar": {"avatar_id": "Angela-inblackskirt-20220820"},
            "audio_list": [{"audio_url": "https://example.com/speech.mp3"}],
        },
    },
).json()["data"]["execution_id"]

# 步骤 2：等待 Avatar 视频完成
while True:
    status = requests.get(
        f"https://api.heygen.com/v1/workflows/executions/{avatar_execution_id}",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
    ).json()["data"]
    if status["status"] == "completed":
        avatar_video_url = status["output"]["video"]["video_url"]
        break
    time.sleep(10)

# 步骤 3：换入自定义脸部
faceswap_execution_id = faceswap(
    source_image_url="https://example.com/custom-face.jpg",
    target_video_url=avatar_video_url,
)
```

## 最佳实践

1. **使用清晰、正面的脸部照片** — 源图片应显示单张脸部，光线良好
2. **换脸是 GPU 密集型的** — 预计 1-3 分钟处理时间，每 10 秒轮询一次
3. **源图片质量很重要** — 更高分辨率的脸部照片产生更好的效果
4. **每张源图片一张脸** — 源图片应恰好包含一张要换入的脸
5. **适用于任何视频** — 目标视频可以是 Avatar 视频、录制品或任何包含可见脸部的视频
6. **与其他工作流链式使用** — 先生成 Avatar 视频，然后换入自定义脸部进行个性化
