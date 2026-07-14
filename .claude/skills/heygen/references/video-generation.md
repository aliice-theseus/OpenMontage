---
name: video-generation
description: POST /v2/video/generate 工作流和 HeyGen 的多场景视频
---

# 视频生成

## 目录
- [视频输出格式](#视频输出格式)
- [基本视频生成](#基本视频生成)
- [请求字段](#请求字段)
- [视频配置选项](#视频配置选项)
- [多场景视频](#多场景视频)
- [使用不同角色类型](#使用不同角色类型)
- [语音输入类型](#语音输入类型)
- [完整工作流示例](#完整工作流示例)
- [错误处理](#错误处理)
- [脚本长度限制](#脚本长度限制)
- [在脚本中添加暂停](#在脚本中添加暂停)
- [测试模式](#测试模式)
- [生产级工作流](#生产级工作流)
- [透明背景视频（WebM）](#透明背景视频webm)
- [最佳实践](#最佳实践)

---

`/v2/video/generate` 端点是使用 HeyGen 创建 AI 头像视频的主要方式。

## 视频输出格式

| 端点 | 格式 | 使用场景 |
|----------|--------|----------|
| `/v2/video/generate` | MP4 | **标准** - 带背景的视频（最常用） |
| `/v1/video.webm` | WebM | 透明背景 - 仅在需要时使用 |

大多数情况使用带背景的 MP4。只有当你想看到头像*后面*的内容时才需要 WebM（例如，将头像叠加在屏幕录制上）。

## 基本视频生成

### curl

```bash
curl -X POST "https://api.heygen.com/v2/video/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_inputs": [
      {
        "character": {
          "type": "avatar",
          "avatar_id": "josh_lite3_20230714",
          "avatar_style": "normal"
        },
        "voice": {
          "type": "text",
          "input_text": "Hello! Welcome to HeyGen.",
          "voice_id": "1bd001e7e50f421d891986aad5158bc8"
        }
      }
    ],
    "dimension": {
      "width": 1920,
      "height": 1080
    }
  }'
```

## 请求字段

### 顶层字段

| 字段 | 类型 | 必需 | 描述 |
|-------|------|:---:|-------------|
| `video_inputs` | array | ✓ | 1-50 个视频输入对象的数组 |
| `dimension` | object | | 视频尺寸 `{width, height}` |
| `title` | string | | 用于组织的视频名称 |
| `test` | boolean | | 测试模式（带水印，不消耗积分） |
| `caption` | boolean | | 启用自动字幕 |
| `callback_id` | string | | 用于 webhook 追踪的自定义 ID |
| `callback_url` | string | | 完成通知的 URL |
| `folder_id` | string | | 存储文件夹 ID |

### video_inputs[].character 字段

| 字段 | 类型 | 必需 | 描述 |
|-------|------|:---:|-------------|
| `type` | string | ✓ | `"avatar"` 或 `"talking_photo"` |
| `avatar_id` | string | ✓* | 头像 ID（*type 为 "avatar" 时必需） |
| `talking_photo_id` | string | ✓* | 照片 ID（*type 为 "talking_photo" 时必需） |
| `avatar_style` | string | | `"normal"`, `"closeUp"` 或 `"circle"` |
| `scale` | number | | 头像缩放比例 |
| `offset` | object | | 位置偏移 `{x, y}` |

### video_inputs[].voice 字段

| 字段 | 类型 | 必需 | 描述 |
|-------|------|:---:|-------------|
| `type` | string | ✓ | `"text"`, `"audio"` 或 `"silence"` |
| `voice_id` | string | ✓* | 语音 ID（*type 为 "text" 时必需） |
| `input_text` | string | ✓* | 脚本文本（*type 为 "text" 时必需） |
| `audio_url` | string | ✓* | 音频 URL（*type 为 "audio" 时必需） |
| `duration` | number | ✓* | 时长秒数（*type 为 "silence" 时必需） |
| `speed` | number | | 语速 0.5-2.0（默认 1.0） |
| `pitch` | number | | 音高 -20 到 20（默认 0） |

### video_inputs[].background 字段

| 字段 | 类型 | 必需 | 描述 |
|-------|------|:---:|-------------|
| `type` | string | | `"color"`, `"image"` 或 `"video"` |
| `value` | string | | Hex 颜色（type 为 "color" 时） |
| `url` | string | | 图片/视频 URL（type 为 "image"/"video" 时） |
| `fit` | string | | `"cover"` 或 `"contain"` |

### TypeScript

```typescript
// 必需字段没有 '?' - 可选字段有 '?'
interface VideoInput {
  character: {
    type: "avatar" | "talking_photo";           // 必需
    avatar_id?: string;                         // type="avatar" 时必需
    talking_photo_id?: string;                  // type="talking_photo" 时必需
    avatar_style?: "normal" | "closeUp" | "circle";
    scale?: number;
    offset?: { x: number; y: number };
  };
  voice: {
    type: "text" | "audio" | "silence";         // 必需
    input_text?: string;                        // type="text" 时必需
    voice_id?: string;                          // type="text" 时必需
    audio_url?: string;                         // type="audio" 时必需
    duration?: number;                          // type="silence" 时必需
    speed?: number;
    pitch?: number;
  };
  background?: {
    type?: "color" | "image" | "video";
    value?: string;
    url?: string;
    fit?: "cover" | "contain";
  };
}

interface VideoGenerateRequest {
  video_inputs: VideoInput[];                   // 必需
  dimension?: { width: number; height: number };
  test?: boolean;
  title?: string;
  caption?: boolean;
  callback_id?: string;
  callback_url?: string;
  folder_id?: string;
}

interface VideoGenerateResponse {
  error: null | string;
  data: {
    video_id: string;
  };
}

async function generateVideo(config: VideoGenerateRequest): Promise<string> {
  const response = await fetch("https://api.heygen.com/v2/video/generate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });

  const json: VideoGenerateResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.video_id;
}
```

### Python

```python
import requests
import os

def generate_video(config: dict) -> str:
    response = requests.post(
        "https://api.heygen.com/v2/video/generate",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json"
        },
        json=config
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["video_id"]
```

## 视频配置选项

### 完整配置示例

```typescript
const fullConfig: VideoGenerateRequest = {
  // 测试模式（不消耗积分，输出带水印）
  test: false,

  // 视频标题（用于组织）
  title: "产品演示视频",

  // 视频尺寸
  dimension: {
    width: 1920,
    height: 1080,
  },

  // 视频场景/输入
  video_inputs: [
    {
      // 头像配置
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },

      // 语音配置
      voice: {
        type: "text",
        input_text: "欢迎来到我们的产品演示！",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
        speed: 1.0,
        pitch: 0,
      },

      // 背景配置
      background: {
        type: "color",
        value: "#FFFFFF",
      },
    },
  ],
};
```

## 多场景视频

创建包含多个场景的视频：

```typescript
const multiSceneConfig = {
  video_inputs: [
    // 场景 1：介绍
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "你好！今天我将向你展示三个关键功能。",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#1a1a2e",
      },
    },
    // 场景 2：功能 1
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "closeUp",
      },
      voice: {
        type: "text",
        input_text: "首先，让我们看看我们的仪表盘。",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "image",
        url: "https://example.com/dashboard-bg.jpg",
      },
    },
    // 场景 3：总结
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "感谢观看！今天就试试吧。",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#1a1a2e",
      },
    },
  ],
  dimension: { width: 1920, height: 1080 },
};
```

## 使用不同角色类型

### 头像

```typescript
{
  character: {
    type: "avatar",
    avatar_id: "josh_lite3_20230714",
    avatar_style: "normal"
  }
}
```

### 说话照片

```typescript
{
  character: {
    type: "talking_photo",
    talking_photo_id: "your_talking_photo_id"
  }
}
```

## 语音输入类型

### 文字转语音

```typescript
{
  voice: {
    type: "text",
    input_text: "你的脚本内容",
    voice_id: "1bd001e7e50f421d891986aad5158bc8",
    speed: 1.0,  // 0.5 - 2.0
    pitch: 0     // -20 到 20
  }
}
```

### 自定义音频

```typescript
{
  voice: {
    type: "audio",
    audio_url: "https://example.com/your-audio.mp3"
  }
}
```

## 完整工作流示例

```typescript
async function createVideo(script: string, avatarId: string, voiceId: string) {
  // 1. 生成视频
  console.log("开始视频生成...");
  const videoId = await generateVideo({
    video_inputs: [
      {
        character: {
          type: "avatar",
          avatar_id: avatarId,
          avatar_style: "normal",
        },
        voice: {
          type: "text",
          input_text: script,
          voice_id: voiceId,
        },
        background: {
          type: "color",
          value: "#FFFFFF",
        },
      },
    ],
    dimension: { width: 1920, height: 1080 },
  });

  console.log(`视频 ID: ${videoId}`);

  // 2. 轮询完成状态
  console.log("等待视频完成...");
  const videoUrl = await waitForVideo(videoId);

  console.log(`视频就绪: ${videoUrl}`);
  return videoUrl;
}

// 轮询辅助函数
async function waitForVideo(videoId: string): Promise<string> {
  const maxAttempts = 60;
  const pollInterval = 10000; // 10 秒

  for (let i = 0; i < maxAttempts; i++) {
    const response = await fetch(
      `https://api.heygen.com/v2/videos/${videoId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );

    const { data } = await response.json();

    if (data.status === "completed") {
      return data.video_url;
    } else if (data.status === "failed") {
      throw new Error(data.failure_message || "视频生成失败");
    }

    await new Promise((r) => setTimeout(r, pollInterval));
  }

  throw new Error("视频生成超时");
}
```

## 错误处理

```typescript
async function generateVideoSafe(config: VideoGenerateRequest) {
  try {
    const videoId = await generateVideo(config);
    return { success: true, videoId };
  } catch (error) {
    // 常见错误
    if (error.message.includes("quota")) {
      console.error("积分不足");
    } else if (error.message.includes("avatar")) {
      console.error("无效的头像 ID");
    } else if (error.message.includes("voice")) {
      console.error("无效的语音 ID");
    } else if (error.message.includes("script")) {
      console.error("脚本过长或无效");
    }

    return { success: false, error: error.message };
  }
}
```

## 脚本长度限制

| 套餐 | 最大字符数 |
|------|----------------|
| 免费 | ~500 |
| 创作者 | ~1,500 |
| 团队 | ~3,000 |
| 企业 | ~5,000+ |

## 在脚本中添加暂停

使用 `<break>` 标签在脚本中添加暂停：

```typescript
const script = "欢迎来到我们的演示。<break time=\"1s\"/> 让我展示功能。";
```

**格式：** `<break time="Xs"/>` 其中 X 是秒数（例如 `1s`, `1.5s`, `0.5s`）

**重要：** Break 标签必须在前后有空格。

参见 [voices.md](voices.md) 了解详细的 break 标签文档。

## 测试模式

在开发期间使用测试模式：

```typescript
const config = {
  test: true, // 水印输出，不消耗积分
  video_inputs: [...],
};
```

## 生产级工作流

使用头像默认语音（推荐）、适当超时和重试逻辑的完整示例：

```typescript
interface VideoGenerationResult {
  videoId: string;
  videoUrl: string;
  duration: number;
  avatarId: string;
  voiceId: string;
  avatarName: string;
}

async function generateAvatarVideo(
  script: string,
  options: {
    avatarId?: string; // 特定头像，或选择第一个可用
    width?: number;
    height?: number;
  } = {}
): Promise<VideoGenerationResult> {
  const { width = 1920, height = 1080 } = options;
  let { avatarId } = options;

  // 1. 如果未提供特定头像，列出可用头像
  if (!avatarId) {
    console.log("列出可用头像...");
    const listResponse = await fetch("https://api.heygen.com/v2/avatars", {
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    });
    const listData = await listResponse.json();

    if (!listData.data?.avatars?.length) {
      throw new Error("没有可用的头像");
    }
    avatarId = listData.data.avatars[0].avatar_id;
  }

  // 2. 获取头像详情，包括 default_voice_id
  console.log(`获取头像详情: ${avatarId}`);
  const detailsResponse = await fetch(
    `https://api.heygen.com/v2/avatar/${avatarId}/details`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );
  const { data: avatar } = await detailsResponse.json();

  if (!avatar.default_voice_id) {
    throw new Error(`头像 ${avatar.name} 没有默认语音 - 请手动选择语音`);
  }

  console.log(`使用头像: ${avatar.name}，默认语音: ${avatar.default_voice_id}`);

  // 3. 使用头像的默认语音生成视频
  const videoId = await generateVideo({
    video_inputs: [{
      character: {
        type: "avatar",
        avatar_id: avatar.id, // 来自详情响应
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: script,
        voice_id: avatar.default_voice_id, // 预先匹配的默认语音
        speed: 1.0,
      },
      background: {
        type: "color",
        value: "#1a1a2e",
      },
    }],
    dimension: { width, height },
  });

  console.log(`视频 ID: ${videoId}`);

  // 3. 等待完成（20 分钟超时 - 生成可能需要 15+ 分钟）
  console.log("等待视频生成（通常 5-15 分钟，可能更长）...");
  const result = await waitForVideo(
    videoId,
    process.env.HEYGEN_API_KEY!,
    (status, elapsed) => {
      console.log(`  [${Math.round(elapsed / 1000)}s] ${status}`);
    },
    1200000 // 20 分钟安全超时
  );

  return {
    videoId,
    videoUrl: result.video_url!,
    duration: result.duration!,
    avatarId: avatar.id,
    voiceId: avatar.default_voice_id,
    avatarName: avatar.name,
  };
}

// 使用示例 - 让它自动选择头像
const result = await generateAvatarVideo(
  "你好！欢迎来到我们的产品演示。"
);
console.log(`视频就绪: ${result.videoUrl}`);

// 或指定一个已知的 avatar_id
const result2 = await generateAvatarVideo(
  "你好！欢迎来到我们的产品演示。",
  { avatarId: "josh_lite3_20230714" }
);
```

## 透明背景视频（WebM）

**仅当需要透明度时**使用 WebM——即头像应叠加在其他视频内容上，并且你需要看到后面的内容。

**不需要 WebM 的情况：**
- 头像顶部叠加动态图形/文字
- 画中画带纯色背景
- 标准出镜视频

**需要 WebM 的情况：**
- 头像叠加在屏幕录制上
- 头像浮动在视频背景上
- 真正的 Alpha 通道合成

### WebM 请求字段

**注意：** WebM 端点（`/v1/video.webm`）使用与 `/v2/video/generate` 不同的结构。

| 字段 | 类型 | 必需 | 描述 |
|-------|------|:---:|-------------|
| `avatar_pose_id` | string | ✓ | 头像姿势 ID（从头像详情获取） |
| `avatar_style` | string | ✓ | 仅 `"normal"` 或 `"closeUp"`（无 circle） |
| `input_text` | string | ✓* | 脚本文本（*不使用 input_audio 时必需） |
| `voice_id` | string | ✓* | 语音 ID（*与 input_text 搭配使用时必需） |
| `input_audio` | string | ✓* | 音频 URL（*不使用 input_text 时必需） |
| `dimension` | object | | `{width, height}`（默认：1280x720） |

必须提供（`input_text` + `voice_id`）**或** `input_audio` 其中之一，但不能同时提供。

### curl

```bash
curl -X POST "https://api.heygen.com/v1/video.webm" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "avatar_pose_id": "josh_lite3_20230714",
    "avatar_style": "normal",
    "input_text": "Hello! This video has a transparent background.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "dimension": {
      "width": 1920,
      "height": 1080
    }
  }'
```

### TypeScript

```typescript
interface WebMVideoRequest {
  avatar_pose_id: string;                      // 必需
  avatar_style: "normal" | "closeUp";          // 必需（不支持 circle）
  input_text?: string;                         // 不使用 input_audio 时必需
  voice_id?: string;                           // 与 input_text 搭配时必需
  input_audio?: string;                        // 不使用 input_text 时必需
  dimension?: { width: number; height: number };
}

async function generateTransparentVideo(
  script: string,
  avatarPoseId: string,
  voiceId: string
): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/video.webm", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      avatar_pose_id: avatarPoseId,            // 必需
      avatar_style: "normal",                  // 必需："normal" 或 "closeUp"
      input_text: script,                      // 必需（与 voice_id 配套）
      voice_id: voiceId,                       // 必需（与 input_text 配套）
      dimension: { width: 1920, height: 1080 },
    }),
  });

  const { data } = await response.json();
  return data.video_id;
}
```

### 何时使用 WebM vs MP4

| 场景 | 格式 | 原因 |
|----------|--------|------|
| 头像顶部有叠加层 | **MP4** | 叠加层放在顶部，不需要透明度 |
| 标准出镜 | **MP4** | 更简单，兼容性更好 |
| Loom 风格（头像在屏幕录制上） | **WebM** + `normal`/`closeUp` | 需要透明度，后期裁剪为圆形 |
| 头像浮动在视频内容上 | **WebM** | 需要看到头像后面的内容 |

**注意：** WebM 仅支持 `normal` 和 `closeUp` 样式。WebM 不支持 Circle 样式——请在视频编辑器/Remotion 中应用圆形遮罩。

### WebM 示例：Loom 风格（头像在屏幕录制上）

使用 `normal` 或 `closeUp` 样式生成（WebM 不支持 circle）：

```typescript
// 生成带透明背景的头像
const videoId = await fetch("https://api.heygen.com/v1/video.webm", {
  method: "POST",
  headers: { "X-Api-Key": apiKey, "Content-Type": "application/json" },
  body: JSON.stringify({
    avatar_pose_id: avatarPoseId,              // 必需
    avatar_style: "closeUp",                   // 必需：仅 "normal" 或 "closeUp"
    input_text: script,                        // 必需（与 voice_id 配套）
    voice_id: voiceId,                         // 必需（与 input_text 配套）
    dimension: { width: 1920, height: 1080 },
  }),
}).then(r => r.json()).then(d => d.data.video_id);
```

在 Remotion 中应用圆形遮罩：

```tsx
import { Video, AbsoluteFill } from "remotion";

export const LoomStyleVideo: React.FC<{
  screenRecordingUrl: string;
  avatarWebmUrl: string;
}> = ({ screenRecordingUrl, avatarWebmUrl }) => {
  return (
    <AbsoluteFill>
      {/* 屏幕录制作为底层 */}
      <Video src={screenRecordingUrl} style={{ width: "100%", height: "100%" }} />

      {/* 在 CSS 中应用圆形遮罩的头像 */}
      <Video
        src={avatarWebmUrl}
        style={{
          position: "absolute",
          bottom: 20,
          left: 20,
          width: 150,
          height: 150,
          borderRadius: "50%", // 圆形遮罩
          overflow: "hidden",
          objectFit: "cover",
        }}
      />
    </AbsoluteFill>
  );
};
```

### 状态轮询说明

WebM 视频使用与 MP4 相同的状态端点：

```typescript
// 与常规视频相同的轮询方式
const status = await getVideoStatus(videoId);
// status.video_url 将是一个 .webm 文件
```

## 最佳实践

1. **在生成前预览头像** - 下载 `preview_image_url`，让用户在生成视频前看到头像的样子（参见 [avatars.md](avatars.md)）
2. **使用头像的默认语音** - 大多数头像有预先匹配的 `default_voice_id`，可以获得自然的效果（参见 [avatars.md](avatars.md)）
3. **备用方案：手动匹配性别** - 如果没有默认语音，确保头像和语音性别匹配（参见 [voices.md](voices.md)）
4. **验证输入** - 在生成前检查头像和语音 ID
5. **使用测试模式** - 在不消耗积分的情况下测试配置
6. **设置充足的超时时间** - 使用 15-20 分钟；生成通常需要 10-15 分钟，有时更长
7. **考虑异步模式** - 对于长视频，保存 video_id 稍后检查状态（参见 [video-status.md](video-status.md)）
8. **优雅处理错误** - 实现适当的错误处理
9. **监控进度** - 实现带进度反馈的轮询
10. **优化脚本** - 保持脚本简洁自然
11. **考虑尺寸** - 根据你的使用场景匹配尺寸（参见 [dimensions.md](dimensions.md)）
