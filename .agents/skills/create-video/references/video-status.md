---
name: video-status
description: HeyGen 视频的轮询模式、状态类型和获取下载 URL
---

# 视频状态和轮询

生成视频后，你需要轮询状态直到视频完成。HeyGen 异步处理视频。

## MCP 工具（首选）

如果 HeyGen MCP 服务器已连接，使用 `mcp__heygen__get_video` 并传入 `videoId` 参数。它一次调用返回状态、video_url、thumbnail_url、duration、title、gif_url、captioned_video_url 和其他元数据。

## 检查视频状态（直接 API）

### curl

```bash
curl -X GET "https://api.heygen.com/v2/videos/YOUR_VIDEO_ID" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface VideoStatusResponse {
  error: null | string;
  data: {
    id: string;
    status: "pending" | "processing" | "completed" | "failed";
    video_url?: string;
    thumbnail_url?: string;
    duration?: number;
    title?: string;
    created_at?: string;
    completed_at?: string;
    gif_url?: string;
    captioned_video_url?: string;
    subtitle_url?: string;
    folder_id?: string;
    output_language?: string;
    failure_code?: string;
    failure_message?: string;
  };
}

async function getVideoStatus(videoId: string): Promise<VideoStatusResponse["data"]> {
  const response = await fetch(
    `https://api.heygen.com/v2/videos/${videoId}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json: VideoStatusResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data;
}
```

### Python

```python
import requests
import os

def get_video_status(video_id: str) -> dict:
    response = requests.get(
        f"https://api.heygen.com/v2/videos/{video_id}",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]
```

## 视频状态类型

| 状态 | 描述 |
|--------|-------------|
| `pending` | 视频正在排队等待处理 |
| `processing` | 视频正在生成中 |
| `completed` | 视频已准备好下载 |
| `failed` | 视频生成失败 |

## 预计生成时间

视频生成通常需要 **5-15 分钟**，但在高峰负载或脚本较长时可能超过 20 分钟。

| 因素 | 影响 |
|--------|--------|
| 脚本长度 | 较长的脚本 = 显著更长的处理时间 |
| 分辨率 | 1080p 比 720p 耗时更长 |
| 虚拟形象复杂度 | 某些虚拟形象渲染更快 |
| 队列负载 | 高峰时段可能导致 15-20+ 分钟的等待 |
| 多场景 | 每个场景增加处理时间 |

**建议：**
- 将超时设置为 **15-20 分钟**（900,000-1,200,000 ms）以确保安全
- 对于超过 2 分钟语音的脚本，预计 15+ 分钟
- 对于长视频，考虑异步模式（保存 video_id，稍后检查）

## 响应格式

### 视频已完成

```json
{
  "error": null,
  "data": {
    "id": "abc123",
    "status": "completed",
    "video_url": "https://files.heygen.ai/video/abc123.mp4",
    "thumbnail_url": "https://files.heygen.ai/thumbnail/abc123.jpg",
    "duration": 45.2,
    "title": "我的视频",
    "created_at": "2024-01-15T10:30:00Z",
    "completed_at": "2024-01-15T10:38:00Z",
    "gif_url": "https://files.heygen.ai/gif/abc123.gif",
    "captioned_video_url": null,
    "subtitle_url": null,
    "folder_id": null,
    "output_language": "en"
  }
}
```

### 视频失败

```json
{
  "error": null,
  "data": {
    "id": "abc123",
    "status": "failed",
    "failure_code": "script_too_long",
    "failure_message": "脚本对所选虚拟形象太长"
  }
}
```

## 轮询实现

### 基本轮询

```typescript
async function waitForVideo(
  videoId: string,
  maxWaitMs = 600000, // 10 分钟
  pollIntervalMs = 5000 // 5 秒
): Promise<string> {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitMs) {
    const status = await getVideoStatus(videoId);

    switch (status.status) {
      case "completed":
        return status.video_url!;
      case "failed":
        throw new Error(status.failure_message || "视频生成失败");
      case "pending":
      case "processing":
        await new Promise((resolve) => setTimeout(resolve, pollIntervalMs));
        break;
    }
  }

  throw new Error("视频生成超时");
}
```

### 带进度回调的轮询

```typescript
type ProgressCallback = (status: string, elapsed: number) => void;

async function waitForVideoWithProgress(
  videoId: string,
  onProgress?: ProgressCallback,
  maxWaitMs = 600000,
  pollIntervalMs = 5000
): Promise<string> {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitMs) {
    const elapsed = Date.now() - startTime;
    const status = await getVideoStatus(videoId);

    onProgress?.(status.status, elapsed);

    switch (status.status) {
      case "completed":
        return status.video_url!;
      case "failed":
        throw new Error(status.failure_message || "视频生成失败");
      default:
        await new Promise((resolve) => setTimeout(resolve, pollIntervalMs));
    }
  }

  throw new Error("视频生成超时");
}
```

### 完整工作流示例

```typescript
async function generateAndDownloadVideo(config: VideoConfig): Promise<string> {
  // 1. 生成视频
  const generateResponse = await fetch(
    "https://api.heygen.com/v2/video/generate",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    }
  );

  const { data: generateData } = await generateResponse.json();
  const videoId = generateData.video_id;
  console.log(`视频 ID：${videoId}`);

  // 2. 轮询完成
  const videoUrl = await waitForVideoWithProgress(
    videoId,
    (status, elapsed) => {
      console.log(`[${Math.round(elapsed / 1000)}s] 状态：${status}`);
    }
  );

  // 3. 下载
  const outputPath = `./output/${videoId}.mp4`;
  await downloadVideo(videoUrl, outputPath);

  return outputPath;
}
```

## 最佳实践

1. **使用指数退避** - 增加长时间运行作业的轮询间隔
2. **设置合理超时** - 大多数视频在 10 分钟内完成
3. **优雅处理失败** - 检查错误消息以获取可操作的反馈
4. **考虑 webhook** - 对于生产系统，webhook 比轮询更高效
5. **缓存视频 URL** - 下载的视频 URL 有效时间有限
