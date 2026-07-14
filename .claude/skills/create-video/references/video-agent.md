---
name: video-agent
description: One-shot prompt video generation with HeyGen Video Agent API
---

# Video Agent API

Video Agent API 从单个文本提示词生成完整视频。与需要逐场景详细配置的标准视频生成 API 不同，Video Agent 自动处理脚本编写、虚拟形象选择、视觉效果、配音、节奏和字幕。

## MCP 工具（首选）

如果已连接 HeyGen MCP 服务器，请使用 `mcp__heygen__generate_video_agent` 代替直接 API 调用：

```
工具：mcp__heygen__generate_video_agent
参数：
  prompt: "<来自 prompt-optimizer.md 的优化提示词>"
  config:
    duration_sec: 90          # 可选，5-300
    avatar_id: "avatar_id"    # 可选，省略则由 AI 选择
    orientation: "landscape"   # 可选，"landscape" 或 "portrait"
  files:                       # 可选
    - asset_id: "uploaded_asset_id"
```

然后使用返回的 `video_id` 通过 `mcp__heygen__get_video` 检查状态。

提示词质量仍然是关键因素——无论使用 MCP 还是直接 API，都要遵循 [prompt-optimizer.md](prompt-optimizer.md) 的指南。

## 何时使用 Video Agent vs 标准 API

| 使用场景 | 推荐 API |
|----------|-----------------|
| 从创意快速生成视频 | Video Agent |
| 精确控制场景、虚拟形象、时间 | 标准 v2/video/generate |
| 大规模自动化内容生成 | Video Agent |
| 特定虚拟形象配合精确脚本 | 标准 v2/video/generate |
| 原型或草稿视频 | Video Agent |
| 品牌一致的生产级视频 | 标准 v2/video/generate |

## 在调用此 API 之前

**必要步骤：** 在生成视频前使用 [prompt-optimizer.md](prompt-optimizer.md) 优化提示词。平庸与专业效果之间的差距完全取决于提示词质量。

快速检查清单：
1. 定义视觉风格（颜色、美学）——参见 [visual-styles.md](visual-styles.md)
2. 使用特定场景类型构建场景结构
3. 以约 150 字/分钟的速度编写画外音脚本
4. 为每个场景指定媒体类型（动态图形、素材、AI 生成）

## 直接 API 端点

```
POST https://api.heygen.com/v1/video_agent/generate
```

## 请求字段

| 字段 | 类型 | 必填 | 描述 |
|-------|------|:---:|-------------|
| `prompt` | string | ✓ | 描述所需视频的文本提示词 |
| `config` | object | | 配置选项（见下方） |
| `files` | array | | 生成中需引用的资产文件 |
| `callback_id` | string | | 用于跟踪的自定义 ID。**同时需要设置 `callback_url`** — 不需要 webhook 时省略两者 |
| `callback_url` | string | | 完成通知的 Webhook URL |

### Config 对象

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `duration_sec` | integer | 大致时长，单位秒（5-300） |
| `avatar_id` | string | 要使用的特定虚拟形象（可选——未提供则由 AI 选择） |
| `orientation` | string | `"portrait"` 或 `"landscape"` |

### Files 数组

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `asset_id` | string | 要引用的上传文件的资产 ID |

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
    "prompt": "为一个新的 AI 驱动日历应用创建一段 60 秒的产品演示视频。语气专业但友好，面向忙碌的职场人士。突出智能排程功能和时区处理。"
  }'
```

## TypeScript

```typescript
interface VideoAgentConfig {
  duration_sec?: number;      // 5-300 秒
  avatar_id?: string;         // 可选：特定虚拟形象
  orientation?: "portrait" | "landscape";
}

interface VideoAgentFile {
  asset_id: string;
}

interface VideoAgentRequest {
  prompt: string;             // 必填
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
    throw new Error(`Video Agent 失败：${json.error}`);
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
        raise Exception(f"Video Agent 失败：{data['error']}")

    return data["data"]["video_id"]
```

## 示例

### 基础：仅提示词

```typescript
const videoId = await generateWithVideoAgent(
  为科技创业公司的新员工创建一段 30 秒的欢迎视频。保持活力和现代感。"
);
```

### 带时长和方向

```typescript
const videoId = await generateWithVideoAgent(
  "解释云计算对小型企业的好处。使用通俗语言和实际案例。",
  {
    duration_sec: 90,
    orientation: "landscape"
  }
);
```

### 带特定虚拟形象

```typescript
const videoId = await generateWithVideoAgent(
  "展示季度销售业绩。专业语气，数据导向。",
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
// 1. 上传参考资料（参见 assets.md）
const logoAssetId = await uploadFile("./company-logo.png", "image/png");
const productImageId = await uploadFile("./product-screenshot.png", "image/png");

// 2. 使用参考文件生成视频
const response = await fetch(
  "https://api.heygen.com/v1/video_agent/generate",
  {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: "创建一个展示我们新仪表板功能的产品演示视频。使用上传的截图作为视觉参考。",
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

## 编写高效提示词

参见 **[prompt-optimizer.md](prompt-optimizer.md)** 获取全面的提示词编写指南。

提示词优化器涵盖以下内容：
- 提示词复杂度级别（基础 → 逐场景）
- 视觉风格分类和颜色规范
- 媒体类型选择（动态图形 vs 素材 vs AI 生成）
- 场景结构和时间计算
- 常见视频类型的即用模板

## 检查视频状态

Video Agent 返回一个 `video_id`——使用标准状态端点检查进度：

```typescript
// 与标准视频生成相同的轮询方式
const videoUrl = await waitForVideo(videoId);
```

轮询实现参见 [video-status.md](video-status.md)。

## 对比：Video Agent vs 标准 API

### Video Agent 请求
```typescript
// 简单：描述您想要的内容
const videoId = await generateWithVideoAgent(
  "创建一个 60 秒的教程，介绍如何设置双因素认证。专业语气，分步讲解。"
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
        input_text: "欢迎收看本教程，了解双因素认证...",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#1a1a2e",
      },
    },
    // ... 每个步骤的更多场景
  ],
  dimension: { width: 1920, height: 1080 },
});
```

## 局限性

- 对确切脚本措辞的控制较少
- 虚拟形象选择可能因未指定而变化
- 场景组成是自动化的
- 可能无法精确匹配品牌指南
- 时长是近似值，非精确值

## 最佳实践

1. **提示词要具体** - 更多细节 = 更好的结果
2. **指定时长** - 使用 `config.duration_sec` 获得可预测长度
3. **必要时锁定虚拟形象** - 使用 `config.avatar_id` 保持一致性
4. **上传参考文件** - 帮助 AI 理解您的品牌/产品
5. **迭代优化提示词** - 根据结果进行调整
6. **用于草稿** - Video Agent 非常适合在最终制作前快速迭代
