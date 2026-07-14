---
name: webhooks
description: Registering webhook endpoints and event types for HeyGen
---

# Webhook

Webhook 允许 HeyGen 在事件发生时通知您的应用程序，例如视频完成。这比轮询状态更新更高效。

## 概述

Webhook 不是重复检查视频状态，而是将通知推送到您的服务器，当：
- 视频生成完成
- 视频生成失败
- 翻译完成
- 虚拟形象训练完成
- 其他异步操作完成

## 设置 Webhook 端点

您的 webhook 端点应：
1. 接受 POST 请求
2. 快速返回 200 状态
3. 异步处理事件

### Express.js 示例

```typescript
import express from "express";
import crypto from "crypto";

const app = express();
app.use(express.json());

// Webhook endpoint
app.post("/webhook/heygen", async (req, res) => {
  // Acknowledge receipt immediately
  res.status(200).send("OK");

  // Process event asynchronously
  processWebhookEvent(req.body).catch(console.error);
});

async function processWebhookEvent(event: HeyGenWebhookEvent) {
  console.log(`Received event: ${event.event_type}`);

  switch (event.event_type) {
    case "avatar_video.success":
      await handleVideoSuccess(event);
      break;
    case "avatar_video.fail":
      await handleVideoFailure(event);
      break;
    case "video_translate.success":
      await handleTranslationSuccess(event);
      break;
    default:
      console.log(`Unknown event type: ${event.event_type}`);
  }
}

app.listen(3000, () => {
  console.log("Webhook server running on port 3000");
});
```

### Python Flask 示例

```python
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

@app.route("/webhook/heygen", methods=["POST"])
def heygen_webhook():
    event = request.json

    # Acknowledge immediately
    response = jsonify({"status": "received"})

    # Process asynchronously
    thread = threading.Thread(
        target=process_webhook_event,
        args=(event,)
    )
    thread.start()

    return response, 200

def process_webhook_event(event):
    event_type = event.get("event_type")
    print(f"Received event: {event_type}")

    if event_type == "avatar_video.success":
        handle_video_success(event)
    elif event_type == "avatar_video.fail":
        handle_video_failure(event)
    elif event_type == "video_translate.success":
        handle_translation_success(event)

if __name__ == "__main__":
    app.run(port=3000)
```

## Webhook 事件类型

| 事件类型 | 描述 |
|------------|-------------|
| `avatar_video.success` | 视频生成完成 |
| `avatar_video.fail` | 视频生成失败 |
| `video_translate.success` | 翻译完成 |
| `video_translate.fail` | 翻译失败 |
| `instant_avatar.success` | 即时虚拟形象已创建 |
| `instant_avatar.fail` | 即时虚拟形象创建失败 |

## 事件负载结构

### 视频成功事件

```typescript
interface VideoSuccessEvent {
  event_type: "avatar_video.success";
  event_data: {
    video_id: string;
    video_url: string;
    thumbnail_url: string;
    duration: number;
    callback_id?: string;
  };
}
```

```json
{
  "event_type": "avatar_video.success",
  "event_data": {
    "video_id": "abc123",
    "video_url": "https://files.heygen.ai/video/abc123.mp4",
    "thumbnail_url": "https://files.heygen.ai/thumbnail/abc123.jpg",
    "duration": 45.2,
    "callback_id": "your_custom_id"
  }
}
```

### 视频失败事件

```typescript
interface VideoFailureEvent {
  event_type: "avatar_video.fail";
  event_data: {
    video_id: string;
    error: string;
    callback_id?: string;
  };
}
```

```json
{
  "event_type": "avatar_video.fail",
  "event_data": {
    "video_id": "abc123",
    "error": "Script too long for selected avatar",
    "callback_id": "your_custom_id"
  }
}
```

## 注册 Webhook URL

通过 HeyGen 仪表板或 API 配置您的 webhook URL：

### 请求字段

| 字段 | 类型 | 必填 | 描述 |
|-------|------|:---:|-------------|
| `url` | string | ✓ | 您的 webhook 端点 URL |
| `events` | array | ✓ | 要订阅的事件类型 |
| `secret` | string | | 用于签名验证的共享密钥 |

### 通过 API

```bash
curl -X POST "https://api.heygen.com/v1/webhook/endpoint.add" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-domain.com/webhook/heygen",
    "events": ["avatar_video.success", "avatar_video.fail"]
  }'
```

### TypeScript

```typescript
interface WebhookConfig {
  url: string;                                 // Required
  events: string[];                            // Required
  secret?: string;
}

async function registerWebhook(config: WebhookConfig): Promise<void> {
  const response = await fetch("https://api.heygen.com/v1/webhook/endpoint.add", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });

  const json = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }
}
```

## 使用回调 ID

使用回调 ID 跟踪哪个视频触发了 webhook：

### 在视频生成中包含回调 ID

```typescript
const videoConfig = {
  video_inputs: [...],
  callback_id: "order_12345", // Your custom identifier
};
```

### 在 Webhook 中处理

```typescript
async function handleVideoSuccess(event: VideoSuccessEvent) {
  const { video_id, video_url, callback_id } = event.event_data;

  if (callback_id) {
    // Look up your original request
    const order = await getOrderByCallbackId(callback_id);
    await updateOrderWithVideo(order.id, video_url);
  }
}
```

## Webhook 安全

### 验证 Webhook 签名

如果 HeyGen 提供签名验证：

```typescript
import crypto from "crypto";

function verifyWebhookSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const expectedSignature = crypto
    .createHmac("sha256", secret)
    .update(payload)
    .digest("hex");

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}

// In your webhook handler
app.post("/webhook/heygen", (req, res) => {
  const signature = req.headers["x-heygen-signature"] as string;
  const payload = JSON.stringify(req.body);

  if (!verifyWebhookSignature(payload, signature, WEBHOOK_SECRET)) {
    return res.status(401).send("Invalid signature");
  }

  // Process event...
});
```

### 验证事件来源

```typescript
function isValidHeygenEvent(event: any): boolean {
  // Check required fields
  if (!event.event_type || !event.event_data) {
    return false;
  }

  // Check event type is known
  const validEventTypes = [
    "avatar_video.success",
    "avatar_video.fail",
    "video_translate.success",
    "video_translate.fail",
  ];

  return validEventTypes.includes(event.event_type);
}
```

## 处理 Webhook 失败

实现重试逻辑和错误处理：

```typescript
async function processWebhookEvent(event: HeyGenWebhookEvent) {
  const maxRetries = 3;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      await handleEvent(event);
      return;
    } catch (error) {
      console.error(`Attempt ${attempt} failed:`, error);

      if (attempt < maxRetries) {
        // Exponential backoff
        await new Promise((r) => setTimeout(r, Math.pow(2, attempt) * 1000));
      }
    }
  }

  // Store failed event for manual review
  await storeFailedEvent(event);
}
```

## Webhook 与轮询对比

| 方面 | Webhook | 轮询 |
|--------|---------|---------|
| 延迟 | 即时 | 取决于间隔 |
| 效率 | 高（推送） | 低（重复请求） |
| 复杂性 | 需要端点 | 实现更简单 |
| 可靠性 | 需要重试处理 | 保证送达 |
| 成本 | API 使用量较低 | API 使用量较高 |

## 测试 Webhook

### 使用 ngrok 本地开发

```bash
# Start ngrok tunnel
ngrok http 3000

# Use ngrok URL as webhook endpoint
# https://abc123.ngrok.io/webhook/heygen
```

### Webhook 测试工具

```typescript
// Test webhook locally
async function simulateWebhook(event: HeyGenWebhookEvent) {
  const response = await fetch("http://localhost:3000/webhook/heygen", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });

  console.log(`Response: ${response.status}`);
}

// Simulate success event
await simulateWebhook({
  event_type: "avatar_video.success",
  event_data: {
    video_id: "test_123",
    video_url: "https://example.com/test.mp4",
    thumbnail_url: "https://example.com/test.jpg",
    duration: 30,
    callback_id: "test_callback",
  },
});
```

## 最佳实践

1. **快速响应** - 在 5 秒内返回 200，异步处理
2. **处理重复** - 同一事件可能多次发送
3. **实现重试** - 处理临时处理失败
4. **记录一切** - 存储 webhook 负载以便调试
5. **使用回调 ID** - 通过系统跟踪请求
6. **保护端点** - 验证签名，使用 HTTPS
7. **监控健康** - 跟踪 webhook 成功率
8. **队列处理** - 对繁重处理使用任务队列
