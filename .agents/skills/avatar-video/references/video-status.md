---
name: video-status
description: HeyGen 视频的轮询模式、状态类型和获取下载 URL
---

# 视频状态和轮询

生成视频后，您需要轮询状态直到视频完成。HeyGen 异步处理视频。

## MCP 工具（推荐）

如果 HeyGen MCP 服务器已连接，使用带 `videoId` 参数的 `mcp__heygen__get_video`。它在一次调用中返回状态、video_url、thumbnail_url、duration、title、gif_url、captioned_video_url 和其他元数据。

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
| `pending` | 视频已排队等待处理 |
| `processing` | 视频正在生成中 |
| `completed` | 视频已准备好下载 |
| `failed` | 视频生成失败 |

## 预期生成时间

视频生成通常需要 **5-15 分钟**，但在高峰期或脚本较长时可能超过 20 分钟。

| 因素 | 影响 |
|--------|--------|
| 脚本长度 | 较长的脚本 = 显著更长的处理时间 |
| 分辨率 | 1080p 比 720p 耗时更长 |
| 虚拟角色复杂度 | 某些虚拟角色渲染更快 |
| 队列负载 | 高峰时段可能导致 15-20+ 分钟等待 |
| 多个场景 | 每个场景增加处理时间 |

**建议：**
- 设置超时为 **15-20 分钟**（900,000-1,200,000 毫秒）以确保安全
- 对于超过 2 分钟语音的脚本，预计需要 15 分钟以上
- 对于长视频，考虑异步模式（保存 video_id，稍后检查）

## 响应格式

### 完成的视频

```json
{
  "error": null,
  "data": {
    "id": "abc123",
    "status": "completed",
    "video_url": "https://files.heygen.ai/video/abc123.mp4",
    "thumbnail_url": "https://files.heygen.ai/thumbnail/abc123.jpg",
    "duration": 45.2,
    "title": "My Video",
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

### 失败的视频

```json
{
  "error": null,
  "data": {
    "id": "abc123",
    "status": "failed",
    "failure_code": "script_too_long",
    "failure_message": "Script too long for selected avatar"
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
        throw new Error(status.failure_message || "Video generation failed");
      case "pending":
      case "processing":
        await new Promise((resolve) => setTimeout(resolve, pollIntervalMs));
        break;
    }
  }

  throw new Error("Video generation timed out");
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
        throw new Error(status.failure_message || "Video generation failed");
      default:
        await new Promise((resolve) => setTimeout(resolve, pollIntervalMs));
    }
  }

  throw new Error("Video generation timed out");
}

// 使用
const videoUrl = await waitForVideoWithProgress(
  videoId,
  (status, elapsed) => {
    console.log(`Status: ${status}, Elapsed: ${Math.round(elapsed / 1000)}s`);
  }
);
```

### Python 轮询

```python
import time
from typing import Optional, Callable

def wait_for_video(
    video_id: str,
    max_wait_seconds: int = 600,
    poll_interval: int = 5,
    on_progress: Optional[Callable[[str, int], None]] = None
) -> str:
    start_time = time.time()

    while time.time() - start_time < max_wait_seconds:
        elapsed = int(time.time() - start_time)
        status_data = get_video_status(video_id)
        status = status_data["status"]

        if on_progress:
            on_progress(status, elapsed)

        if status == "completed":
            return status_data["video_url"]
        elif status == "failed":
            raise Exception(status_data.get("failure_message", "Video generation failed"))

        time.sleep(poll_interval)

    raise Exception("Video generation timed out")


# 使用
def progress_callback(status: str, elapsed: int):
    print(f"Status: {status}, Elapsed: {elapsed}s")

video_url = wait_for_video(video_id, on_progress=progress_callback)
```

## 下载视频

视频完成后，下载它。**重要**：状态显示为"completed"后，视频 URL 可能不会立即可用。使用带退避的重试逻辑。

### TypeScript（带重试）

```typescript
import fs from "fs";
import path from "path";

async function downloadVideoWithRetry(
  videoUrl: string,
  outputPath = "./output/video.mp4",
  maxRetries = 5,
  initialDelayMs = 2000
): Promise<void> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch(videoUrl);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const arrayBuffer = await response.arrayBuffer();
      fs.writeFileSync(path.resolve(outputPath), Buffer.from(arrayBuffer));
      console.log(`Video downloaded to ${outputPath}`);
      return;
    } catch (error) {
      lastError = error as Error;
      const delay = initialDelayMs * Math.pow(2, attempt); // 指数退避
      console.log(`Download attempt ${attempt + 1} failed, retrying in ${delay}ms...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw new Error(`Failed to download after ${maxRetries} attempts: ${lastError?.message}`);
}
```

### Python（带重试）

```python
import requests
import time

def download_video_with_retry(
    video_url: str,
    output_path: str,
    max_retries: int = 5,
    initial_delay: float = 2.0
) -> None:
    last_error = None

    for attempt in range(max_retries):
        try:
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Video downloaded to {output_path}")
            return
        except Exception as e:
            last_error = e
            delay = initial_delay * (2 ** attempt)  # 指数退避
            print(f"Download attempt {attempt + 1} failed, retrying in {delay}s...")
            time.sleep(delay)

    raise Exception(f"Failed to download after {max_retries} attempts: {last_error}")
```

### 简单下载（无重试）

用于快速脚本，可手动重试：

```typescript
async function downloadVideo(videoUrl: string, outputPath = "./output/video.mp4") {
  const response = await fetch(videoUrl);
  if (!response.ok) {
    throw new Error(`Failed to download: ${response.status}`);
  }
  const arrayBuffer = await response.arrayBuffer();
  fs.writeFileSync(path.resolve(outputPath), Buffer.from(arrayBuffer));
}
```

## 完整工作流示例

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
  console.log(`Video ID: ${videoId}`);

  // 2. 轮询完成
  const videoUrl = await waitForVideoWithProgress(
    videoId,
    (status, elapsed) => {
      console.log(`[${Math.round(elapsed / 1000)}s] Status: ${status}`);
    }
  );

  // 3. 下载
  const outputPath = `./output/${videoId}.mp4`;
  await downloadVideo(videoUrl, outputPath);

  return outputPath;
}
```

## 可恢复的状态检查

对于长时间运行的生成，保存 video_id 并在稍后检查状态，而不是保持进程等待。

### 生成后保存状态

```typescript
interface PendingVideo {
  videoId: string;
  createdAt: string;
  script: string;
  avatarId: string;
  voiceId: string;
}

async function startVideoGeneration(config: VideoGenerateRequest): Promise<PendingVideo> {
  const videoId = await generateVideo(config);

  const pending: PendingVideo = {
    videoId,
    createdAt: new Date().toISOString(),
    script: config.video_inputs[0].voice.input_text!,
    avatarId: config.video_inputs[0].character.avatar_id!,
    voiceId: config.video_inputs[0].voice.voice_id!,
  };

  // 保存到文件，供稍后检索
  fs.writeFileSync("pending-video.json", JSON.stringify(pending, null, 2));
  console.log(`Video generation started. ID: ${videoId}`);
  console.log("Check status later with: checkVideoStatus()");

  return pending;
}
```

### 稍后检查状态

```typescript
async function checkVideoStatus(): Promise<void> {
  if (!fs.existsSync("pending-video.json")) {
    console.log("No pending video found");
    return;
  }

  const pending: PendingVideo = JSON.parse(
    fs.readFileSync("pending-video.json", "utf-8")
  );

  const elapsed = Date.now() - new Date(pending.createdAt).getTime();
  console.log(`Checking video ${pending.videoId} (started ${Math.round(elapsed / 60000)} min ago)...`);

  const status = await getVideoStatus(pending.videoId);

  switch (status.status) {
    case "completed":
      console.log(`Video ready: ${status.video_url}`);
      console.log(`Duration: ${status.duration}s`);
      // 清理待定文件
      fs.unlinkSync("pending-video.json");
      // 保存结果
      fs.writeFileSync("video-result.json", JSON.stringify({
        ...pending,
        videoUrl: status.video_url,
        thumbnailUrl: status.thumbnail_url,
        duration: status.duration,
        title: status.title,
        createdAt: status.created_at,
        completedAt: status.completed_at,
      }, null, 2));
      break;
    case "failed":
      console.error(`Video failed: ${status.failure_message}`);
      fs.unlinkSync("pending-video.json");
      break;
    default:
      console.log(`Status: ${status.status} - check again in a few minutes`);
  }
}
```

### CLI 友好模式

```typescript
// generate-video.ts - 开始生成并退出
async function main() {
  const pending = await startVideoGeneration(config);
  console.log(`\nVideo ID saved. Run 'npx tsx check-status.ts' to check progress.`);
  process.exit(0); // 立即退出，不等待
}

// check-status.ts - 检查并可选地等待
async function main() {
  const args = process.argv.slice(2);
  const shouldWait = args.includes("--wait");

  if (shouldWait) {
    // 轮询直到完成（20 分钟超时）
    const result = await waitForVideo(pending.videoId, apiKey, onProgress, 1200000);
    console.log(`Done: ${result.video_url}`);
  } else {
    // 仅检查一次并报告
    await checkVideoStatus();
  }
}
```

## 替代方案：使用 Webhooks

您可以使用 webhooks 在视频完成时接收通知，而不是轮询。参见 [webhooks.md](webhooks.md) 获取详情。Webhooks 适用于您不想维持轮询连接的生产系统。

## 最佳实践

1. **使用指数退避** — 为长时间运行的任务增加轮询间隔
2. **设置合理的超时时间** — 大多数视频在 10 分钟内完成
3. **优雅地处理失败** — 检查错误消息以获取可操作反馈
4. **考虑 webhooks** — 对于生产系统，webhooks 比轮询更高效
5. **缓存视频 URL** — 下载的视频 URL 在有限时间内有效
