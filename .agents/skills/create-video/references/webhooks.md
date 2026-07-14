---
name: webhooks
description: 注册 webhook 端点和事件类型用于 HeyGen
---

# Webhooks

Webhook 允许 HeyGen 在事件发生时通知你的应用程序，例如视频完成。这比轮询状态更新更高效。

## 概述

无需反复检查视频状态，webhook 会在以下情况下推送通知到你的服务器：
- 视频生成完成
- 视频生成失败
- 翻译完成
- 虚拟形象训练完成
- 其他异步操作完成

## 设置 Webhook 端点

你的 webhook 端点应：
1. 接受 POST 请求
2. 快速返回 200 状态
3. 异步处理事件

### Express.js 示例

```typescript
import express from "express";
import crypto from "crypto";

const app = express();
app.use(express.json());

// Webhook 端点
app.post("/webhook/heygen", async (req, res) => {
  // 立即确认收到
  res.status(200).send("OK");

  // 异步处理事件
  processWebhookEvent(req.body).catch(console.error);
});

async function processWebhookEvent(event: HeyGenWebhookEvent) {
  console.log(`收到事件：${event.event_type}`);

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
      console.log(`未知事件类型：${event.event_type}`);
  }
}

app.listen(3000, () => {
  console.log("Webhook 服务器运行在端口 3000");
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

    # 立即确认
    response = jsonify({"status": "received"})

    # 异步处理
    thread = threading.Thread(
        target=process_webhook_event,
        args=(event,)
    )
    thread.start()

    return response, 200

def process_webhook_event(event):
    event_type = event.get("event_type")
    print(f"收到事件：{event_type}")

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
| `instant_avatar.success` | 即时虚拟形象创建成功 |
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
    "error": "脚本对所选虚拟形象太长",
    "callback_id": "your_custom_id"
  }
}
```

## 注册 Webhook URL

通过 HeyGen 仪表板或 API 配置你的 webhook URL：

### 请求字段

| 字段 | 类型 | 必需 | 描述 |
|-------|------|:---:|-------------|
| `url` | string | ✓ | 你的 webhook 端点 URL |
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
  url: string;                                 // 必需
  events: string[];                            // 必需
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
  callback_id: "order_12345", // 你的自定义标识符
};
```

### 在 Webhook 中处理

```typescript
async function handleVideoSuccess(event: VideoSuccessEvent) {
  const { video_id, video_url, callback_id } = event.event_data;

  if (callback_id) {
    // 查找你的原始请求
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

// 在你的 webhook 处理器中
app.post("/webhook/heygen", (req, res) => {
  const signature = req.headers["x-heygen-signature"] as string;
  const payload = JSON.stringify(req.body);

  if (!verifyWebhookSignature(payload, signature, WEBHOOK_SECRET)) {
    return res.status(401).send("签名无效");
  }

  // 处理事件...
});
```

### 验证事件来源

```typescript
function isValidHeygenEvent(event: any): boolean {
  // 检查必填字段
  if (!event.event_type || !event.event_data) {
    return false;
  }

  // 检查事件类型是否已知
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
      console.error(`尝试 ${attempt} 失败：`, error);

      if (attempt < maxRetries) {
        // 指数退避
        await new Promise((r) => setTimeout(r, Math.pow(2, attempt) * 1000));
      }
    }
  }

  // 存储失败事件以便人工审查
  await storeFailedEvent(event);
}
```

## Webhook vs 轮询对比

| 方面 | Webhook | 轮询 |
|--------|---------|---------|
| 延迟 | 即时 | 取决于间隔 |
| 效率 | 高（推送） | 低（重复请求） |
| 复杂性 | 需要端点 | 实现更简单 |
| 可靠性 | 需要重试处理 | 保证送达 |
| 成本 | 较低的 API 使用量 | 较高的 API 使用量 |

## 测试 Webhook

### 使用 ngrok 进行本地开发

```bash
# 启动 ngrok 隧道
ngrok http 3000

# 使用 ngrok URL 作为 webhook 端点
# https://abc123.ngrok.io/webhook/heygen
```

### Webhook 测试工具

```typescript
// 本地测试 webhook
async function simulateWebhook(event: HeyGenWebhookEvent) {
  const response = await fetch("http://localhost:3000/webhook/heygen", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });

  console.log(`响应：${response.status}`);
}

// 模拟成功事件
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
2. **处理重复** - 同一事件可能发送多次
3. **实现重试** - 处理临时处理失败
4. **记录一切** - 存储 webhook 负载用于调试
5. **使用回调 ID** - 通过系统跟踪请求
6. **保护端点安全** - 验证签名，使用 HTTPS
7. **监控健康** - 跟踪 webhook 成功率
8. **队列处理** - 对繁重处理使用作业队列
