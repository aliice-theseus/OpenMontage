---
name: quota
description: HeyGen 的积分系统、使用限制和检查剩余配额
---

# HeyGen 配额和积分

HeyGen 使用基于积分的系统进行视频生成。了解配额管理有助于防止视频生成请求失败。

## 检查剩余配额

### curl

```bash
curl -X GET "https://api.heygen.com/v2/user/remaining_quota" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface QuotaResponse {
  error: null | string;
  data: {
    remaining_quota: number;
    used_quota: number;
  };
}

const response = await fetch("https://api.heygen.com/v2/user/remaining_quota", {
  headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
});

const { data }: QuotaResponse = await response.json();
console.log(`Remaining credits: ${data.remaining_quota}`);
```

### Python

```python
import requests
import os

response = requests.get(
    "https://api.heygen.com/v2/user/remaining_quota",
    headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
)

data = response.json()["data"]
print(f"Remaining credits: {data['remaining_quota']}")
```

## 响应格式

```json
{
  "error": null,
  "data": {
    "remaining_quota": 450,
    "used_quota": 50
  }
}
```

## 积分消耗

不同操作消耗不同数量的积分：

| 操作 | 积分成本 | 说明 |
|-----------|-------------|-------|
| 标准视频（1分钟） | 约每分钟 1 积分 | 因分辨率而异 |
| 720p 视频 | 基准费率 | 标准质量 |
| 1080p 视频 | 约 1.5 倍基准费率 | 更高质量 |
| 视频翻译 | 不定 | 取决于视频长度 |
| 流媒体虚拟角色 | 按会话 | 实时使用 |

## 生成前配额检查

在生成视频前始终验证是否有充足配额：

```typescript
async function generateVideoWithQuotaCheck(videoConfig: VideoConfig) {
  // 先检查配额
  const quotaResponse = await fetch(
    "https://api.heygen.com/v2/user/remaining_quota",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const { data: quota } = await quotaResponse.json();

  // 估算所需积分（粗略估算：每分钟 1 积分）
  const estimatedMinutes = videoConfig.estimatedDuration / 60;
  const requiredCredits = Math.ceil(estimatedMinutes);

  if (quota.remaining_quota < requiredCredits) {
    throw new Error(
      `Insufficient credits. Need ${requiredCredits}, have ${quota.remaining_quota}`
    );
  }

  // 继续视频生成
  return generateVideo(videoConfig);
}
```

## 配额管理最佳实践

### 1. 定期监控使用情况

```typescript
async function logQuotaUsage() {
  const response = await fetch(
    "https://api.heygen.com/v2/user/remaining_quota",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const { data } = await response.json();

  console.log({
    remaining: data.remaining_quota,
    used: data.used_quota,
    percentUsed: (
      (data.used_quota / (data.remaining_quota + data.used_quota)) *
      100
    ).toFixed(1),
  });
}
```

### 2. 设置警报

```typescript
const QUOTA_WARNING_THRESHOLD = 50;

async function checkQuotaWithAlert() {
  const response = await fetch(
    "https://api.heygen.com/v2/user/remaining_quota",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const { data } = await response.json();

  if (data.remaining_quota < QUOTA_WARNING_THRESHOLD) {
    // 发送警报（邮件、Slack 等）
    await sendAlert(`Low HeyGen quota: ${data.remaining_quota} credits remaining`);
  }

  return data;
}
```

### 3. 开发时使用测试模式

可用时，使用测试模式避免在开发期间消耗积分：

```typescript
const videoConfig = {
  test: true, // 开发期间使用测试模式
  video_inputs: [...],
};

// 测试视频可能有水印但不消耗积分
```

## 订阅层级

不同订阅层级有不同的配额分配和功能：

| 层级 | 功能 |
|------|----------|
| 免费 | 有限积分，基本功能 |
| 创作者 | 更多积分，标准虚拟角色 |
| 团队 | 更高限制，团队协作 |
| 企业 | 自定义限制，API 访问，优先支持 |

API 访问通常需要企业层级或更高。

## 配额问题的错误处理

```typescript
async function handleQuotaError(error: any) {
  if (error.message.includes("quota") || error.message.includes("credit")) {
    console.error("Quota exceeded. Consider:");
    console.error("1. Upgrading your subscription");
    console.error("2. Waiting for quota reset");
    console.error("3. Purchasing additional credits");

    // 检查当前配额
    const quota = await getQuota();
    console.error(`Current remaining: ${quota.remaining_quota}`);
  }

  throw error;
}
```
