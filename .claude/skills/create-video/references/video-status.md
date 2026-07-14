---
name: video-status
description: Polling patterns, status types, and retrieving download URLs for HeyGen videos
---

# 视频状态与轮询

生成视频后，您需要轮询状态直到视频完成。HeyGen 异步处理视频。

## MCP 工具（首选）

如果已连接 HeyGen MCP 服务器，请使用带 `videoId` 参数的 `mcp__heygen__get_video`。它一次调用即返回状态、video_url、thumbnail_url、时长、标题、gif_url、captioned_video_url 和其他元数据。

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
| `completed` | 视频已就绪，可下载 |
| `failed` | 视频生成失败 |

## 预期生成时间

视频生成通常需要 **5-15 分钟**，但在高峰时段或较长脚本可能超过 20 分钟。

| 因素 | 影响 |
|--------|--------|
| 脚本长度 | 更长脚本 = 显著更长的处理时间 |
| 分辨率 | 1080p 比 720p 耗时更长 |
| 虚拟形象复杂度 | 某些虚拟形象渲染更快 |
| 队列负载 | 高峰时段可能导致 15-20+ 分钟等待 |
| 多场景 | 每个场景增加处理时间 |

**建议**：
- 将超时设置为 **15-20 分钟**（900,000-1,200,000 毫秒）以确保安全
- 对于超过 2 分钟语音的脚本，预计 15 分钟以上
- 对于长视频，考虑异步模式（保存 video_id，稍后检查）

## 响应格式

### 完成视频

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

### 失败视频

```json
{
  "error": null,
  "data": {
    "id": "abc123",
    "status": "failed",
    "failure_code": "script_too_long",
    "failure_message": "脚本对所选虚拟形象来说过长"
  }
}
```

## 轮询实现

### 基础轮询

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

// 使用示例
const videoUrl = await waitForVideoWithProgress(
  videoId,
  (status, elapsed) => {
    console.log(`状态：${status}，已用时：${Math.round(elapsed / 1000)} 秒`);
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
            raise Exception(status_data.get("failure_message", "视频生成失败"))

        time.sleep(poll_interval)

    raise Exception("视频生成超时")


# 使用示例
def progress_callback(status: str, elapsed: int):
    print(f"状态：{status}，已用时：{elapsed} 秒")

video_url = wait_for_video(video_id, on_progress=progress_callback)
```

## 下载视频

视频完成后，进行下载。**重要提示**：状态显示 "completed" 后，视频 URL 可能不会立即可用。请使用带退避的重试逻辑。

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
      console.log(`视频已下载到 ${outputPath}`);
      return;
    } catch (error) {
      lastError = error as Error;
      const delay = initialDelayMs * Math.pow(2, attempt); // 指数退避
      console.log(`下载尝试 ${attempt + 1} 失败，${delay} 毫秒后重试...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw new Error(`重试 ${maxRetries} 次后下载失败：${lastError?.message}`);
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

            print(f"视频已下载到 {output_path}")
            return
        except Exception as e:
            last_error = e
            delay = initial_delay * (2 ** attempt)  # 指数退避
            print(f"下载尝试 {attempt + 1} 失败，{delay} 秒后重试...")
            time.sleep(delay)

    raise Exception(f"重试 {max_retries} 次后下载失败：{last_error}")
```

### 简单下载（无重试）

适用于快速脚本，您可以手动重试：

```typescript
async function downloadVideo(videoUrl: string, outputPath = "./output/video.mp4") {
  const response = await fetch(videoUrl);
  if (!response.ok) {
    throw new Error(`下载失败：${response.status}`);
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
  console.log(`视频 ID：${videoId}`);

  // 2. 轮询完成
  const videoUrl = await waitForVideoWithProgress(
    videoId,
    (status, elapsed) => {
      console.log(`[${Math.round(elapsed / 1000)} 秒] 状态：${status}`);
    }
  );

  // 3. 下载
  const outputPath = `./output/${videoId}.mp4`;
  await downloadVideo(videoUrl, outputPath);

  return outputPath;
}
```

## 可恢复的状态检查

对于长时间运行的生成任务，保存 video_id 并稍后检查状态，而不是让进程持续等待。

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

  // 保存到文件以便稍后检索
  fs.writeFileSync("pending-video.json", JSON.stringify(pending, null, 2));
  console.log(`视频生成已开始。ID：${videoId}`);
  console.log("稍后使用 checkVideoStatus() 检查状态。");

  return pending;
}
```

### 稍后检查状态

```typescript
async function checkVideoStatus(): Promise<void> {
  if (!fs.existsSync("pending-video.json")) {
    console.log("未找到待处理的视频");
    return;
  }

  const pending: PendingVideo = JSON.parse(
    fs.readFileSync("pending-video.json", "utf-8")
  );

  const elapsed = Date.now() - new Date(pending.createdAt).getTime();
  console.log(`正在检查视频 ${pending.videoId}（开始于 ${Math.round(elapsed / 60000)} 分钟前）...`);

  const status = await getVideoStatus(pending.videoId);

  switch (status.status) {
    case "completed":
      console.log(`视频就绪：${status.video_url}`);
      console.log(`时长：${status.duration} 秒`);
      // 清理待处理文件
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
      console.error(`视频失败：${status.failure_message}`);
      fs.unlinkSync("pending-video.json");
      break;
    default:
      console.log(`状态：${status.status} - 几分钟后再次检查`);
  }
}
```

### CLI 友好模式

```typescript
// generate-video.ts - 开始生成并退出
async function main() {
  const pending = await startVideoGeneration(config);
  console.log(`\n视频 ID 已保存。运行 'npx tsx check-status.ts' 检查进度。`);
  process.exit(0); // 立即退出，无需等待
}

// check-status.ts - 检查并可选择等待
async function main() {
  const args = process.argv.slice(2);
  const shouldWait = args.includes("--wait");

  if (shouldWait) {
    // 轮询直到完成（20 分钟超时）
    const result = await waitForVideo(pending.videoId, apiKey, onProgress, 1200000);
    console.log(`完成：${result.video_url}`);
  } else {
    // 仅检查一次并报告
    await checkVideoStatus();
  }
}
```

## 替代方案：使用 Webhook

您可以不使用轮询，而是使用 webhook 在视频完成时接收通知。详情参见 [webhooks.md](webhooks.md)。Webhook 是生产系统的理想选择，无需维护轮询连接。

## 最佳实践

1. **使用指数退避** - 对长时间运行的任务增加轮询间隔
2. **设置合理的超时时间** - 大多数视频在 10 分钟内完成
3. **优雅处理失败** - 检查错误信息以获取可操作的反馈
4. **考虑 webhook** - 对生产系统，webhook 比轮询更高效
5. **缓存视频 URL** - 下载后的视频 URL 有效期有限
