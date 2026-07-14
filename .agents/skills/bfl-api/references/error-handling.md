---
name: error-handling
description: BFL API 错误码和恢复策略
---

# 错误处理

处理 BFL API 错误的综合指南。

## HTTP 状态码

| 编码 | 含义             | 原因                 | 操作               |
|------|------------------|----------------------|-------------------|
| 200  | 成功             | 请求成功             | 处理响应           |
| 400  | 错误请求         | 无效参数             | 检查请求格式       |
| 401  | 未授权           | 无效/缺失 API 密钥   | 验证凭据           |
| 402  | 需要付款         | 积分不足             | 向账户添加积分     |
| 403  | 禁止访问         | 访问被拒绝           | 检查权限           |
| 404  | 未找到           | 无效端点             | 验证 URL           |
| 429  | 请求过多         | 达到速率限制         | 实施退避策略       |
| 500  | 内部服务器错误   | 服务器问题           | 带退避重试         |
| 502  | 错误网关         | 网络问题             | 带退避重试         |
| 503  | 服务不可用       | 临时中断             | 带退避重试         |

## 错误响应格式

```json
{
  "error": "error_code",
  "message": "人类可读的描述",
  "details": {
    "field": "特定字段信息"
  }
}
```

## 常见错误及解决方案

### 认证错误 (401)

```json
{
  "error": "invalid_api_key",
  "message": "The provided API key is invalid or expired"
}
```

**解决方案：**
```python
def verify_api_key(api_key):
    if not api_key:
        raise ValueError("API key is required")
    if not api_key.startswith("bfl_"):
        raise ValueError("Invalid API key format")
```

### 积分不足 (402)

```json
{
  "error": "insufficient_credits",
  "message": "Your account does not have enough credits"
}
```

**解决方案：**
```python
def handle_payment_error(response):
    if response.status_code == 402:
        # 记录并告警
        logging.error("Insufficient credits - add funds")
        # 可选择暂停操作
        raise InsufficientCreditsError("Add credits to continue")
```

### 速率限制 (429)

```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many concurrent requests",
  "retry_after": 5
}
```

**解决方案：**
```python
def handle_rate_limit(response):
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 5))
        time.sleep(retry_after)
        return True  # 信号重试
    return False
```

### 验证错误 (400)

```json
{
  "error": "validation_error",
  "message": "Invalid request parameters",
  "details": {
    "width": "Must be a multiple of 16",
    "prompt": "Cannot be empty"
  }
}
```

**解决方案：**
```python
def validate_request(prompt, width, height):
    errors = []

    if not prompt or not prompt.strip():
        errors.append("Prompt cannot be empty")

    if width % 16 != 0:
        errors.append(f"Width {width} must be multiple of 16")

    if height % 16 != 0:
        errors.append(f"Height {height} must be multiple of 16")

    if width * height > 4_000_000:
        errors.append("Total pixels cannot exceed 4MP")

    if errors:
        raise ValidationError(errors)
```

### 生成失败

轮询过程中的失败：

```json
{
  "status": "Error",
  "error": "content_policy_violation",
  "message": "The prompt violated content policy"
}
```

**常见失败原因：**
- `content_policy_violation` - 提示词/图片被安全系统标记
- `generation_timeout` - 生成时间过长
- `internal_error` - 服务端问题
- `invalid_image` - 输入图片无法处理

## 重试策略

```python
import time
import random

class RetryableError(Exception):
    """可以重试的错误。"""
    pass

class NonRetryableError(Exception):
    """不应重试的错误。"""
    pass

def classify_error(status_code, error_code):
    """判断错误是否可重试。"""
    # 可重试
    if status_code in [429, 500, 502, 503]:
        return RetryableError

    # 不可重试
    if status_code in [400, 401, 402, 403]:
        return NonRetryableError

    # 生成失败
    if error_code in ['generation_timeout', 'internal_error']:
        return RetryableError

    if error_code in ['content_policy_violation', 'invalid_image']:
        return NonRetryableError

    return RetryableError  # 默认可重试

def make_request_with_retry(func, max_retries=3):
    """使用重试逻辑执行函数。"""
    last_exception = None

    for attempt in range(max_retries):
        try:
            return func()
        except RetryableError as e:
            last_exception = e
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time:.1f}s")
            time.sleep(wait_time)
        except NonRetryableError:
            raise  # 不重试

    raise last_exception
```

## 综合错误处理器

```python
import logging

class BFLError(Exception):
    """BFL API 错误的基础异常。"""
    def __init__(self, message, status_code=None, error_code=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)

class AuthenticationError(BFLError):
    """API 密钥或认证问题。"""
    pass

class InsufficientCreditsError(BFLError):
    """账户需要更多积分。"""
    pass

class RateLimitError(BFLError):
    """并发请求过多。"""
    def __init__(self, message, retry_after=5):
        super().__init__(message, 429, "rate_limit_exceeded")
        self.retry_after = retry_after

class ValidationError(BFLError):
    """无效的请求参数。"""
    pass

class GenerationError(BFLError):
    """生成失败。"""
    pass

def handle_response(response):
    """处理 API 响应并抛出相应的错误。"""
    if response.status_code == 200:
        return response.json()

    try:
        error_data = response.json()
    except:
        error_data = {"message": response.text}

    error_code = error_data.get("error", "unknown")
    message = error_data.get("message", "Unknown error")

    if response.status_code == 401:
        raise AuthenticationError(message, 401, error_code)

    if response.status_code == 402:
        raise InsufficientCreditsError(message, 402, error_code)

    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 5))
        raise RateLimitError(message, retry_after)

    if response.status_code == 400:
        raise ValidationError(message, 400, error_code)

    if response.status_code >= 500:
        raise BFLError(f"Server error: {message}", response.status_code, error_code)

    raise BFLError(message, response.status_code, error_code)
```

## 日志记录最佳实践

```python
import logging
import json

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log_request(endpoint, payload):
    logging.info(f"Request: POST {endpoint}")
    logging.debug(f"Payload: {json.dumps(payload, indent=2)}")

def log_error(error, context=None):
    logging.error(f"Error: {error}")
    if context:
        logging.error(f"Context: {context}")

def log_generation_failure(status, error, prompt):
    logging.warning(f"Generation failed: {error}")
    logging.debug(f"Failed prompt: {prompt[:100]}...")
```

## 断路器模式

用于生产系统：

```python
import time
from threading import Lock

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        self.lock = Lock()

    def record_success(self):
        with self.lock:
            self.failures = 0
            self.state = "closed"

    def record_failure(self):
        with self.lock:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "open"

    def can_proceed(self):
        with self.lock:
            if self.state == "closed":
                return True

            if self.state == "open":
                if time.time() - self.last_failure_time > self.reset_timeout:
                    self.state = "half-open"
                    return True
                return False

            # half-open: 允许一个请求测试
            return True
```
