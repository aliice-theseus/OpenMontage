---
name: polling-patterns
description: 为 BFL API 响应实现异步轮询
---

# 轮询模式

BFL API 使用异步生成。所有请求都返回一个 `polling_url` 用于状态检查。

## 基本流程

```
1. POST 请求到模型端点
   └─> 立即响应：{ "polling_url": "..." }

2. GET polling_url（重复直到完成）
   └─> { "status": "Pending" | "Ready" | "Error" }

3. 状态为 "Ready" 时，下载结果示例 URL
   └─> URL 在 10 分钟后过期
```

## 响应状态

| 状态      | 描述             | 操作             |
|-----------|------------------|------------------|
| `Pending` | 请求已排队/处理中 | 继续轮询         |
| `Ready`   | 生成完成         | 下载结果         |
| `Error`   | 生成错误         | 处理错误         |

## 轮询策略

### 简单固定间隔

```python
import time
import requests

def poll_fixed_interval(polling_url, headers, interval=2, timeout=120):
    """固定间隔的简单轮询。"""
    start_time = time.time()

    while time.time() - start_time < timeout:
        response = requests.get(polling_url, headers=headers)
        data = response.json()

        if data["status"] == "Ready":
            return data["result"]
        elif data["status"] == "Error":
            raise Exception(data.get("error", "Generation Error"))

        time.sleep(interval)

    raise TimeoutError("Polling timeout exceeded")
```

### 指数退避（推荐）

```python
import time
import random
import requests

def poll_with_backoff(polling_url, headers, max_attempts=30):
    """带指数退避和抖动的轮询。"""
    base_delay = 0.5  # 从 500ms 开始
    max_delay = 10    # 上限 10 秒

    for attempt in range(max_attempts):
        response = requests.get(polling_url, headers=headers)
        data = response.json()

        if data["status"] == "Ready":
            return data["result"]
        elif data["status"] == "Error":
            raise Exception(data.get("error", "Generation Error"))

        # 指数退避加抖动
        delay = min(base_delay * (2 ** attempt), max_delay)
        jitter = random.uniform(0, delay * 0.1)  # 10% 抖动
        time.sleep(delay + jitter)

    raise TimeoutError("Max polling attempts exceeded")
```

### 自适应轮询

```python
import time
import requests

def poll_adaptive(polling_url, headers, timeout=120):
    """根据状态调整的自适应轮询。"""
    start_time = time.time()
    delays = {
        "Pending": 2.0,      # 队列/处理中
        None: 1.5            # 未知/默认
    }

    while time.time() - start_time < timeout:
        response = requests.get(polling_url, headers=headers)
        data = response.json()

        status = data.get("status")

        if status == "Ready":
            return data["result"]
        elif status == "Error":
            raise Exception(data.get("error", "Generation Error"))

        delay = delays.get(status, delays[None])
        time.sleep(delay)

    raise TimeoutError("Polling timeout exceeded")
```

## 完整示例：提交并轮询

```python
import time
import requests

class BFLClient:
    def __init__(self, api_key, base_url="https://api.bfl.ai"):
        self.base_url = base_url
        self.headers = {
            "x-key": api_key,
            "Content-Type": "application/json"
        }

    def generate(self, model, prompt, **kwargs):
        """提交生成请求并轮询结果。"""
        # 提交请求
        endpoint = f"{self.base_url}/v1/{model}"
        payload = {"prompt": prompt, **kwargs}

        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()

        polling_url = response.json()["polling_url"]

        # 轮询结果
        return self._poll(polling_url)

    def _poll(self, polling_url, timeout=120):
        """轮询直到完成或超时。"""
        start = time.time()
        delay = 1.0

        while time.time() - start < timeout:
            response = requests.get(polling_url, headers=self.headers)
            data = response.json()

            if data["status"] == "Ready":
                return data["result"]
            elif data["status"] == "Error":
                raise Exception(data.get("error"))

            time.sleep(delay)
            delay = min(delay * 1.5, 5.0)  # 渐进退避

        raise TimeoutError("Generation timed out")

# 使用示例
client = BFLClient("your-api-key")
result = client.generate(
    model="flux-2-pro",
    prompt="A beautiful sunset over mountains"
)
print(f"Image URL: {result['sample']}")
```

## URL 过期

**关键：** 结果 URL 在 10 分钟后过期。请始终立即下载。

```python
def download_result(result_url, output_path):
    """在 URL 过期前下载结果图像。"""
    response = requests.get(result_url)
    response.raise_for_status()

    with open(output_path, 'wb') as f:
        f.write(response.content)

    return output_path
```

## 带轮询的批量处理

```python
import asyncio
import aiohttp

async def generate_batch(client, prompts, model="flux-2-pro"):
    """并发生成多张图像。"""
    async with aiohttp.ClientSession() as session:
        # 提交所有请求
        tasks = []
        for prompt in prompts:
            task = submit_and_poll(session, client, model, prompt)
            tasks.append(task)

        # 等待全部完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

async def submit_and_poll(session, client, model, prompt):
    """异步提交并轮询单张图像。"""
    # 提交
    async with session.post(
        f"{client.base_url}/v1/{model}",
        headers=client.headers,
        json={"prompt": prompt}
    ) as response:
        data = await response.json()
        polling_url = data["polling_url"]

    # 轮询
    while True:
        async with session.get(polling_url, headers=client.headers) as response:
            data = await response.json()

            if data["status"] == "Ready":
                return data["result"]
            elif data["status"] == "Error":
                raise Exception(data.get("error"))

        await asyncio.sleep(2)
```

## 最佳实践

1. **始终实现超时** - 永远不要无限轮询
2. **使用指数退避** - 减少服务器负载，处理拥塞
3. **添加抖动** - 防止轮询多个请求时的惊群效应
4. **处理所有状态值** - 包括意外状态
5. **立即下载** - URL 在 10 分钟后过期
6. **记录轮询尝试** - 有助于调试和监控
7. **遵守速率限制** - 在收到 429 响应时实施适当的退避
