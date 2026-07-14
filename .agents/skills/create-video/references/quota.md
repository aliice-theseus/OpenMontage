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
console.log(`剩余积分：${data.remaining_quota}`);
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
print(f"剩余积分：{data['remaining_quota']}")
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
| 标准视频（1 分钟） | 约 1 积分/分钟 | 因分辨率而异 |
| 720p 视频 | 基础费率 | 标准质量 |
| 1080p 视频 | 约 1.5x 基础费率 | 更高质量 |
| 视频翻译 | 因视频长度而异 |
| 流式虚拟形象 | 按会话 | 实时使用 |

## 生成前配额检查

在生成视频前始终验证有足够配额：

```typescript
async function generateVideoWithQuotaCheck(videoConfig: VideoConfig) {
  // 先检查配额
  const quotaResponse = await fetch(
    "https://api.heygen.com/v2/user/remaining_quota",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const { data: quota } = await quotaResponse.json();

  // 估计所需积分（粗略估计：每分钟 1 积分）
  const estimatedMinutes = videoConfig.estimatedDuration / 60;
  const requiredCredits = Math.ceil(estimatedMinutes);

  if (quota.remaining_quota < requiredCredits) {
    throw new Error(
      `积分不足。需要 ${requiredCredits}，剩余 ${quota.remaining_quota}`
    );
  }

  // 继续生成视频
  return generateVideo(videoConfig);
}
```

## 常见积分问题错误处理

```typescript
async function handleQuotaError(error: any) {
  if (error.message.includes("quota") || error.message.includes("credit")) {
    console.error("配额超出。考虑：");
    console.error("1. 升级你的订阅");
    console.error("2. 等待配额重置");
    console.error("3. 购买额外积分");

    // 检查当前配额
    const quota = await getQuota();
    console.error(`当前剩余：${quota.remaining_quota}`);
  }

  throw error;
}
```

## 最佳实践

1. **使用前检查配额** - 在生成前始终验证有足够积分
2. **监控使用情况** - 定期记录配额使用情况
3. **设置警报** - 在配额低时收到通知
4. **开发时使用测试模式** - 避免在开发过程中消耗积分
5. **考虑订阅层级** - 不同层级有不同的配额分配
