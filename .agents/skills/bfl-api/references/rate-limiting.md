---
name: rate-limiting
description: 理解和处理 BFL API 速率限制
---

# 速率限制

BFL API 实施速率限制以确保公平使用和系统稳定性。

## 当前限制

| 端点类别               | 并发请求数 |
| ---------------------- | ---------- |
| 标准（大多数模型）     | 24         |

**并发请求**指的是正在处理中的请求（已提交但尚未完成）。

## 速率限制头部

检查响应头中的速率限制状态：

```
X-RateLimit-Limit: 24
X-RateLimit-Remaining: 23
X-RateLimit-Reset: 1640000000
```

## HTTP 429 响应

当达到速率限制时，您会收到 HTTP 429：

```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many concurrent requests",
  "retry_after": 5
}
```

## 处理策略

### 1. 客户端侧跟踪

跟踪活动请求以保持在限制以下：

```python
from threading import Lock, Semaphore

class RateLimitedClient:
    def __init__(self, api_key, max_concurrent=24):
        self.api_key = api_key
        self.semaphore = Semaphore(max_concurrent)

    def generate(self, model, prompt, **kwargs):
        with self.semaphore:  # 达到限制时阻塞
            return self._make_request(model, prompt, **kwargs)

    def _make_request(self, model, prompt, **kwargs):
        # 提交请求
        response = requests.post(...)
        polling_url = response.json()["polling_url"]

        # 轮询直到完成（请求仍"活跃"）
        return self._poll(polling_url)
```

### 2. 带指数退避的重试

```python
import time

def request_with_retry(endpoint, payload, headers, max_retries=5):
    """在速率限制时自动重试的请求。"""
    for attempt in range(max_retries):
        response = requests.post(endpoint, json=payload, headers=headers)

        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 5))
            wait_time = retry_after * (2 ** attempt)  # 指数退避
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
            continue

        response.raise_for_status()
        return response

    raise Exception("Max retries exceeded due to rate limiting")
```

### 3. 基于队列的架构

适用于高吞吐量应用：

```python
from queue import Queue
from threading import Thread
import time

class RequestQueue:
    def __init__(self, api_key, max_concurrent=24):
        self.api_key = api_key
        self.queue = Queue()
        self.active = 0
        self.max_concurrent = max_concurrent
        self.lock = Lock()

        # 启动工作线程
        for _ in range(max_concurrent):
            worker = Thread(target=self._worker, daemon=True)
            worker.start()

    def submit(self, model, prompt, callback):
        """提交请求到队列。"""
        self.queue.put({
            'model': model,
            'prompt': prompt,
            'callback': callback
        })

    def _worker(self):
        """处理队列项。"""
        while True:
            item = self.queue.get()
            try:
                result = self._process(item)
                item['callback'](result, None)
            except Exception as e:
                item['callback'](None, e)
            finally:
                self.queue.task_done()

    def _process(self, item):
        # 发送请求并轮询
        ...

# 使用示例
queue = RequestQueue("your-api-key")

def handle_result(result, error):
    if error:
        print(f"Error: {error}")
    else:
        print(f"Generated: {result['sample']}")

queue.submit("flux-2-pro", "A sunset", handle_result)
```

### 4. 异步信号量

```python
import asyncio
import aiohttp

class AsyncRateLimitedClient:
    def __init__(self, api_key, max_concurrent=24):
        self.api_key = api_key
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.headers = {"x-key": api_key}

    async def generate(self, model, prompt):
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                # 提交
                async with session.post(
                    f"https://api.bfl.ai/v1/{model}",
                    headers=self.headers,
                    json={"prompt": prompt}
                ) as response:
                    data = await response.json()
                    polling_url = data["polling_url"]

                # 轮询直到完成
                while True:
                    async with session.get(
                        polling_url,
                        headers=self.headers
                    ) as response:
                        data = await response.json()
                        if data["status"] == "Ready":
                            return data["result"]
                        elif data["status"] == "Error":
                            raise Exception(data.get("error"))
                    await asyncio.sleep(2)

# 使用示例
async def main():
    client = AsyncRateLimitedClient("your-api-key")

    # 带速率限制生成 50 张图像
    prompts = [f"Image {i}" for i in range(50)]
    tasks = [client.generate("flux-2-pro", p) for p in prompts]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```

## 监控速率限制

```python
class RateLimitMonitor:
    def __init__(self):
        self.requests_made = 0
        self.rate_limit_hits = 0
        self.lock = Lock()

    def record_request(self, response):
        with self.lock:
            self.requests_made += 1
            if response.status_code == 429:
                self.rate_limit_hits += 1

    def get_stats(self):
        return {
            "total_requests": self.requests_made,
            "rate_limit_hits": self.rate_limit_hits,
            "hit_rate": self.rate_limit_hits / max(self.requests_made, 1)
        }
```

## 最佳实践

1. **跟踪活动请求** - 了解有多少正在处理中
2. **实现客户端侧限制** - 主动保持在限制以下
3. **使用信号量** - 限制并发的简洁方式
4. **高吞吐量时使用队列** - 流量高峰时缓冲请求
5. **监控头部** - 对剩余配额做出反应
6. **优雅降级** - 接近限制时排队或延迟
7. **不同端点不同限制** - 记住 Kontext Max 是 6，不是 24

## 区域分发

对于非常高的吞吐量，考虑跨区域分发：

```python
ENDPOINTS = [
    "https://api.bfl.ai",
    "https://api.eu.bfl.ai",
    "https://api.us.bfl.ai"
]

def get_endpoint():
    """轮询或最少负载选择。"""
    return random.choice(ENDPOINTS)
```

注意：在依赖此策略之前，请验证区域速率限制是否独立。
