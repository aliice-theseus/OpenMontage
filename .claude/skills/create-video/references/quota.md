---
name: quota
description: Credit system, usage limits, and checking remaining quota for HeyGen
---

# HeyGen 配额与积分

HeyGen 使用基于积分的系统进行视频生成。了解配额管理有助于防止视频生成请求失败。

## 查看剩余配额

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
console.log(`剩余积分: ${data.remaining_quota}`);
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
print(f"剩余积分: {data['remaining_quota']}")
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
| 标准视频（1 分钟） | 约每分钟 1 积分 | 因分辨率而异 |
| 720p 视频 | 基础费率 | 标准质量 |
| 1080p 视频 | 约基础费率的 1.5 倍 | 更高质量 |
| 视频翻译 | 视情况而定 | 取决于视频长度 |
| 流式虚拟形象 | 按会话计费 | 实时使用 |

## 生成前配额检查

在生成视频前务必验证配额是否充足：

```typescript
async function generateVideoWithQuotaCheck(videoConfig: VideoConfig) {
  // 先检查配额
  const quotaResponse = await fetch(
    "https://api.heygen.com/v2/user/remaining_quota",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const { data: quota } = await quotaResponse.json();

  // 估算所需积分（粗略估计：每分钟 1 积分）
  const estimatedMinutes = videoConfig.estimatedDuration / 60;
  const requiredCredits = Math.ceil(estimatedMinutes);

  if (quota.remaining_quota < requiredCredits) {
    throw new Error(
      `积分不足。需要 ${requiredCredits}，仅有 ${quota.remaining_quota}`
    );
  }

  // 继续生成视频
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
    剩余: data.remaining_quota,
    已用: data.used_quota,
    使用百分比: (
      (data.used_quota / (data.remaining_quota + data.used_quota)) *
      100
    ).toFixed(1),
  });
}
```

### 2. 设置告警

```typescript
const QUOTA_WARNING_THRESHOLD = 50;

async function checkQuotaWithAlert() {
  const response = await fetch(
    "https://api.heygen.com/v2/user/remaining_quota",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const { data } = await response.json();

  if (data.remaining_quota < QUOTA_WARNING_THRESHOLD) {
    // 发送告警（邮件、Slack 等）
    await sendAlert(`HeyGen 配额不足：仅剩 ${data.remaining_quota} 积分`);
  }

  return data;
}
```

### 3. 开发时使用测试模式

在可用时，使用测试模式避免在开发过程中消耗积分：

```typescript
const videoConfig = {
  test: true, // 开发时使用测试模式
  video_inputs: [...],
};

// 测试视频可能有水印但不消耗积分
```

## 订阅层级

不同的订阅层级有不同的配额分配和功能：

| 层级 | 功能 |
|------|----------|
| 免费 | 有限积分，基础功能 |
| 创作者 | 更多积分，标准虚拟形象 |
| 团队 | 更高限制，团队协作 |
| 企业 | 自定义限制，API 访问，优先支持 |

API 访问通常需要企业版或更高级别。

## 配额问题的错误处理

```typescript
async function handleQuotaError(error: any) {
  if (error.message.includes("quota") || error.message.includes("credit")) {
    console.error("配额超限。可考虑：");
    console.error("1. 升级您的订阅");
    console.error("2. 等待配额重置");
    console.error("3. 购买额外积分");

    // 检查当前配额
    const quota = await getQuota();
    console.error(`当前剩余：${quota.remaining_quota}`);
  }

  throw error;
}
```
