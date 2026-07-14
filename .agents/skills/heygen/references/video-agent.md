---
name: video-agent
description: 使用 HeyGen Video Agent API 进行一次性提示视频生成
---

# Video Agent API

Video Agent API 从单个文本提示生成完整视频。与需要逐场景详细配置的标准视频生成 API 不同，Video Agent 会自动处理脚本编写、虚拟角色选择、视觉效果、配音、节奏和字幕。

## MCP 工具（推荐）

如果 HeyGen MCP 服务器已连接，使用 `mcp__heygen__generate_video_agent` 代替直接 API 调用：

```
Tool: mcp__heygen__generate_video_agent
Parameters:
  prompt: "<来自 prompt-optimizer.md 的优化提示>"
  config:
    duration_sec: 90          # 可选，5-300
    avatar_id: "avatar_id"    # 可选，省略时由 agent 选择
    orientation: "landscape"   # 可选，"landscape" 或 "portrait"
  files:                       # 可选
    - asset_id: "uploaded_asset_id"
```

然后使用返回的 `video_id` 通过 `mcp__heygen__get_video` 检查状态。

提示质量仍然是关键因素——无论您使用 MCP 还是直接 API，始终遵循 [prompt-optimizer.md](prompt-optimizer.md) 的指导。

## 何时使用 Video Agent vs 标准 API

| 使用场景 | 推荐 API |
|----------|-----------------|
| 从想法快速生成视频 | Video Agent |
| 精确控制场景、虚拟角色、时间 | 标准 v2/video/generate |
| 大规模自动内容生成 | Video Agent |
| 带精确脚本的特定虚拟角色 | 标准 v2/video/generate |
| 原型或草稿视频 | Video Agent |
| 品牌一致的生产视频 | 标准 v2/video/generate |

## 在调用此 API 之前

**必需步骤：** 使用 [prompt-optimizer.md](prompt-optimizer.md) 优化您的提示，然后再生成视频。平庸和专业结果之间的差距完全取决于提示质量。

快速检查清单：
1. 定义视觉风格（颜色、美学）——详见 [visual-styles.md](visual-styles.md)
2. 使用特定场景类型构建场景结构
3. 按约150字/分钟编写配音脚本
4. 为每个场景指定媒体类型（动态图形、素材、AI生成）

## 直接 API 端点

```
POST https://api.heygen.com/v1/video_agent/generate
```

## 请求字段

| 字段 | 类型 | 必需 | 描述 |
|-------|------|:---:|-------------|
| `prompt` | string | ✓ | 描述您想要视频的文本提示 |
| `config` | object | | 配置选项（见下文） |
| `files` | array | | 在生成中引用的资产文件 |
| `callback_id` | string | | 用于跟踪的自定义 ID。**需要同时设置 `callback_url`**——如果不需要 webhook，两者都省略 |
| `callback_url` | string | | 完成通知的 Webhook URL |

### Config 对象

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `duration_sec` | integer | 大致时长（秒），5-300 |
| `avatar_id` | string | 要使用的特定虚拟角色（可选——如未提供，agent 选择） |
| `orientation` | string | `"portrait"` 或 `"landscape"` |

### Files 数组

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `asset_id` | string | 要引用的已上传文件的资产 ID |

## 响应格式

```json
{
  "error": null,
  "data": {
    "video_id": "abc123"
  }
}
```

## curl 示例

```bash
curl -X POST "https://api.heygen.com/v1/video_agent/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 60-second product demo video for a new AI-powered calendar app. The tone should be professional but friendly, targeting busy professionals. Highlight the smart scheduling feature and time zone handling."
  }'
```

## TypeScript

```typescript
interface VideoAgentConfig {
  duration_sec?: number;      // 5-300 秒
  avatar_id?: string;         // 可选：特定虚拟角色
  orientation?: "portrait" | "landscape";
}

interface VideoAgentFile {
  asset_id: string;
}

interface VideoAgentRequest {
  prompt: string;             // 必需
  config?: VideoAgentConfig;
  files?: VideoAgentFile[];
  callback_id?: string;       // 设置时需要 callback_url
  callback_url?: string;
}

interface VideoAgentResponse {
  error: string | null;
  data: {
    video_id: string;
  };
}

async function generateWithVideoAgent(
  prompt: string,
  config?: VideoAgentConfig
): Promise<string> {
  const request: VideoAgentRequest = { prompt };

  if (config) {
    request.config = config;
  }

  const response = await fetch(
    "https://api.heygen.com/v1/video_agent/generate",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  const json: VideoAgentResponse = await response.json();

  if (json.error) {
    throw new Error(`Video Agent failed: ${json.error}`);
  }

  return json.data.video_id;
}
```

## Python

```python
import requests
import os
from typing import Optional

def generate_with_video_agent(
    prompt: str,
    duration_sec: Optional[int] = None,
    avatar_id: Optional[str] = None,
    orientation: Optional[str] = None
) -> str:
    request_body = {"prompt": prompt}

    config = {}
    if duration_sec:
        config["duration_sec"] = duration_sec
    if avatar_id:
        config["avatar_id"] = avatar_id
    if orientation:
        config["orientation"] = orientation

    if config:
        request_body["config"] = config

    response = requests.post(
        "https://api.heygen.com/v1/video_agent/generate",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json"
        },
        json=request_body
    )

    data = response.json()
    if data.get("error"):
        raise Exception(f"Video Agent failed: {data['error']}")

    return data["data"]["video_id"]
```

## 示例

### 基本：仅提示

```typescript
const videoId = await generateWithVideoAgent(
  "Create a 30-second welcome video for new employees at a tech startup. Keep it energetic and modern."
);
```

### 带时长和方向

```typescript
const videoId = await generateWithVideoAgent(
  "Explain the benefits of cloud computing for small businesses. Use simple language and real-world examples.",
  {
    duration_sec: 90,
    orientation: "landscape"
  }
);
```

### 带特定虚拟角色

```typescript
const videoId = await generateWithVideoAgent(
  "Present quarterly sales results. Professional tone, data-focused.",
  {
    duration_sec: 120,
    avatar_id: "josh_lite3_20230714",
    orientation: "landscape"
  }
);
```

### 带参考文件

先上传资产，然后引用它们：

```typescript
// 1. 上传参考资料（详见 assets.md）
const logoAssetId = await uploadFile("./company-logo.png", "image/png");
const productImageId = await uploadFile("./product-screenshot.png", "image/png");

// 2. 使用引用生成视频
const response = await fetch(
  "https://api.heygen.com/v1/video_agent/generate",
  {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: "Create a product demo video showcasing our new dashboard feature. Use the uploaded screenshots as visual references.",
      config: {
        duration_sec: 60,
        orientation: "landscape"
      },
      files: [
        { asset_id: logoAssetId },
        { asset_id: productImageId }
      ]
    }),
  }
);
```

## 编写有效提示

详见 **[prompt-optimizer.md](prompt-optimizer.md)** 获取全面的提示编写指南。

提示优化器涵盖：
- 提示复杂度级别（基本 → 逐场景）
- 视觉样式分类和颜色规范
- 媒体类型选择（动态图形 vs 素材 vs AI 生成）
- 场景结构和时间计算
- 常见视频类型的即用模板

## 检查视频状态

Video Agent 返回一个 `video_id`——使用标准状态端点检查进度：

```typescript
// 与标准视频生成相同的轮询
const videoUrl = await waitForVideo(videoId);
```

详见 [video-status.md](video-status.md) 了解轮询实现。

## 对比：Video Agent vs 标准 API

### Video Agent 请求
```typescript
// 简单：描述您想要的
const videoId = await generateWithVideoAgent(
  "Create a 60-second tutorial on setting up two-factor authentication. Professional tone, step-by-step."
);
```

### 等效的标准 API 请求
```typescript
// 复杂：指定每个细节
const videoId = await generateVideo({
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Welcome to this tutorial on two-factor authentication...",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#1a1a2e",
      },
    },
    // ... 每个步骤更多场景
  ],
  dimension: { width: 1920, height: 1080 },
});
```

## 限制

- 对精确脚本措辞的控制较少
- 如未指定，虚拟角色选择可能有所不同
- 场景合成是自动化的
- 可能不符合精确的品牌指南
- 时长是近似值，不是精确值

## 最佳实践

1. **提示中要具体** - 更多细节 = 更好结果
2. **指定时长** - 使用 `config.duration_sec` 获得可预测的长度
3. **需要时锁定虚拟角色** - 使用 `config.avatar_id` 保持一致
4. **上传参考文件** - 帮助 agent 理解您的品牌/产品
5. **迭代提示** - 根据结果优化
6. **用于草稿** - Video Agent 非常适合在最终生产前快速迭代
