---
name: webhook-integration
description: Setting up webhooks for production BFL API integration
---

# Webhook 集成

对于生产工作负载，请使用 webhook 而非轮询来接收生成结果。

## 相比轮询的优势

- **减少 API 调用** - 无需重复轮询请求
- **即时通知** - 确切知道生成何时完成
- **更好的资源效率** - 不会在轮询上浪费计算资源
- **可扩展架构** - 事件驱动设计

## 设置

### 带 Webhook 的请求

在请求中包含 `webhook_url` 和可选的 `webhook_secret`：

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "美丽的山间日落",
    "webhook_url": "https://your-server.com/api/bfl-webhook",
    "webhook_secret": "your-secret-key-here"
  }'
```

### Webhook 载荷

生成完成时，BFL 向您的 webhook URL 发送 POST 请求：

```json
{
  "id": "gen_abc123xyz",
  "status": "Ready",
  "result": {
    "sample": "https://bfldeliveryprod.blob.core.windows.net/results/...",
    "prompt": "...",
    "seed": 1234567890
  },
  "timestamp": "2025-01-15T10:30:00Z"
}
```

失败时的载荷：

```json
{
  "id": "gen_abc123xyz",
  "status": "Error",
  "error": "content_policy_violation",
  "message": "提示词违反内容政策",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

## 安全

### 签名验证

当提供 `webhook_secret` 时，BFL 使用 HMAC-SHA256 对载荷进行签名：

```
X-BFL-Signature: sha256=<十六进制编码的签名>
```

### 验证实现

```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    """验证 webhook 是否来自 BFL。"""
    if not signature or not signature.startswith('sha256='):
        return False

    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    provided_signature = signature[7:]  # 移除 'sha256=' 前缀

    return hmac.compare_digest(expected_signature, provided_signature)
```

### 带验证的 Flask 处理器

```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import requests

app = Flask(__name__)
WEBHOOK_SECRET = "your-secret-key-here"

@app.route('/api/bfl-webhook', methods=['POST'])
def handle_webhook():
    # 验证签名
    signature = request.headers.get('X-BFL-Signature')
    if not verify_webhook_signature(request.data, signature, WEBHOOK_SECRET):
        return jsonify({'error': '签名无效'}), 401

    data = request.json

    if data['status'] == 'Ready':
        handle_completion(data)
    elif data['status'] == 'Error':
        handle_failure(data)

    return jsonify({'status': 'received'}), 200

def handle_completion(data):
    generation_id = data['id']
    result_url = data['result']['sample']

    # 立即下载图像（URL 在 10 分钟内过期）
    image_data = requests.get(result_url).content

    # 存储到您的存储系统
    store_image(generation_id, image_data)

    # 更新数据库
    update_generation_status(generation_id, 'completed')

    # 通知您的应用/用户
    notify_completion(generation_id)

def handle_failure(data):
    generation_id = data['id']
    error = data.get('error', '未知')

    # 记录失败
    log_generation_failure(generation_id, error)

    # 更新数据库
    update_generation_status(generation_id, 'failed', error)

    # 可能重试或通知
    handle_generation_error(generation_id, error)
```

### Express.js 处理器

```javascript
const express = require('express');
const crypto = require('crypto');
const axios = require('axios');

const app = express();
app.use(express.raw({ type: 'application/json' }));

const WEBHOOK_SECRET = 'your-secret-key-here';

function verifySignature(payload, signature, secret) {
  if (!signature || !signature.startsWith('sha256=')) {
    return false;
  }

  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

  const providedSignature = signature.slice(7);

  return crypto.timingSafeEqual(
    Buffer.from(expectedSignature),
    Buffer.from(providedSignature)
  );
}

app.post('/api/bfl-webhook', async (req, res) => {
  const signature = req.headers['x-bfl-signature'];

  if (!verifySignature(req.body, signature, WEBHOOK_SECRET)) {
    return res.status(401).json({ error: '签名无效' });
  }

  const data = JSON.parse(req.body);

  if (data.status === 'Ready') {
    // 下载图像（URL 在 10 分钟内过期）
    const imageResponse = await axios.get(data.result.sample, {
      responseType: 'arraybuffer'
    });

    // 存储图像
    await storeImage(data.id, imageResponse.data);
  }

  res.json({ status: 'received' });
});
```

## 要求

### 需要 HTTPS

生产环境中 Webhook URL **必须使用 HTTPS**。BFL 不会向 HTTP 端点发送 webhook。

### 响应要求

- 返回 2xx 状态码以确认收到
- 在 30 秒内响应
- 保持处理器快速 - 将繁重处理任务卸载

### 重试策略

BFL 会重试失败的 webhook 投递：

| 尝试 | 延迟 |
|---------|-------|
| 第 1 次重试 | 1 秒 |
| 第 2 次重试 | 5 秒 |
| 第 3 次重试 | 30 秒 |

3 次失败后，webhook 被放弃。如果至关重要，请回退到轮询。

## 幂等性

处理重复的 webhook 投递：

```python
from functools import lru_cache
import redis

redis_client = redis.Redis()

def is_duplicate_webhook(generation_id):
    """检查是否已处理过此 webhook。"""
    key = f"webhook:processed:{generation_id}"

    # 尝试使用 NX 设置（仅当不存在时）
    was_set = redis_client.set(key, "1", nx=True, ex=3600)  # 1 小时 TTL

    return not was_set  # 如果无法设置，则为重复

@app.route('/api/bfl-webhook', methods=['POST'])
def handle_webhook():
    # ... 签名验证 ...

    data = request.json
    generation_id = data['id']

    if is_duplicate_webhook(generation_id):
        return jsonify({'status': 'already_processed'}), 200

    # 处理 webhook...
```

## 混合方案

将 webhook 与轮询回退结合使用：

```python
class HybridClient:
    def __init__(self, api_key, webhook_url, webhook_secret):
        self.api_key = api_key
        self.webhook_url = webhook_url
        self.webhook_secret = webhook_secret
        self.pending = {}  # 跟踪待处理的生成

    def generate(self, prompt, timeout=300):
        """使用 webhook 生成，回退到轮询。"""
        response = self._submit(prompt)
        generation_id = response['id']
        polling_url = response['polling_url']

        # 等待 webhook（带超时）
        result = self._wait_for_webhook(generation_id, timeout=timeout)

        if result is None:
            # Webhook 未到达，回退到轮询
            result = self._poll(polling_url, timeout=60)

        return result

    def _submit(self, prompt):
        return requests.post(
            "https://api.bfl.ai/v1/flux-2-pro",
            headers={"x-key": self.api_key},
            json={
                "prompt": prompt,
                "webhook_url": self.webhook_url,
                "webhook_secret": self.webhook_secret
            }
        ).json()

    def receive_webhook(self, data):
        """由 webhook 处理器调用。"""
        generation_id = data['id']
        if generation_id in self.pending:
            self.pending[generation_id].set_result(data)
```

## 监控

跟踪 webhook 健康状态：

```python
import time

class WebhookMetrics:
    def __init__(self):
        self.received = 0
        self.processed = 0
        self.failed = 0
        self.avg_latency = 0

    def record_webhook(self, generation_id, submit_time):
        self.received += 1
        latency = time.time() - submit_time
        self.avg_latency = (self.avg_latency * (self.received - 1) + latency) / self.received

    def record_success(self):
        self.processed += 1

    def record_failure(self):
        self.failed += 1

    def get_stats(self):
        return {
            "received": self.received,
            "processed": self.processed,
            "failed": self.failed,
            "success_rate": self.processed / max(self.received, 1),
            "avg_latency_seconds": self.avg_latency
        }
```
