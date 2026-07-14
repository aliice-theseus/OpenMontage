---
name: assets
description: Uploading images, videos, and audio for use in HeyGen video generation
---

# 资源上传和管理

HeyGen 允许您上传自定义资源（图片、视频、音频），用于视频生成，例如背景、说话照片源和自定义音频。

## 上传流程

资源上传是一个单步过程：将原始文件二进制数据直接 POST 到上传端点。Content-Type 头部必须与文件的 MIME 类型匹配。

## 上传资源

**端点：** `POST https://upload.heygen.com/v1/asset`

### 请求

| 头部 | 必填 | 描述 |
|--------|:--------:|-------------|
| `X-Api-Key` | ✓ | 您的 HeyGen API 密钥 |
| `Content-Type` | ✓ | 文件的 MIME 类型（例如 `image/jpeg`） |

请求体是原始二进制文件数据。不需要 JSON 或表单字段。

### 响应

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `code` | number | 状态码（`100` = 成功） |
| `data.id` | string | 用于视频生成的唯一资源 ID |
| `data.name` | string | 资源名称 |
| `data.file_type` | string | `image`、`video` 或 `audio` |
| `data.url` | string | 上传文件的可访问 URL |
| `data.image_key` | string \| null | 用于创建上传照片虚拟形象的键（仅图片） |
| `data.folder_id` | string | 文件夹 ID（不在文件夹中则为空） |
| `data.meta` | string \| null | 资源元数据 |
| `data.created_ts` | number | 创建的 Unix 时间戳 |

### curl

```bash
curl -X POST "https://upload.heygen.com/v1/asset" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: image/jpeg" \
  --data-binary '@./background.jpg'
```

### TypeScript

```typescript
import fs from "fs";
import path from "path";

interface AssetUploadResponse {
  code: number;
  data: {
    id: string;
    name: string;
    file_type: string;
    url: string;
    image_key: string | null;
    folder_id: string;
    meta: string | null;
    created_ts: number;
  };
  msg: string | null;
  message: string | null;
}

async function uploadAsset(filePath: string, contentType: string): Promise<AssetUploadResponse["data"]> {
  const resolvedPath = path.resolve(filePath);
  const fileBuffer = fs.readFileSync(resolvedPath);

  const response = await fetch("https://upload.heygen.com/v1/asset", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": contentType,
    },
    body: fileBuffer,
  });

  const json: AssetUploadResponse = await response.json();

  if (json.code !== 100) {
    throw new Error(json.message ?? "Upload failed");
  }

  return json.data;
}

// Usage
const asset = await uploadAsset("./background.jpg", "image/jpeg");
console.log(`Uploaded asset: ${asset.id}`);
console.log(`Asset URL: ${asset.url}`);
```

### TypeScript（使用流处理大文件）

```typescript
import fs from "fs";
import path from "path";
import { stat } from "fs/promises";

async function uploadLargeAsset(filePath: string, contentType: string): Promise<AssetUploadResponse["data"]> {
  const resolvedPath = path.resolve(filePath);
  const fileStats = await stat(resolvedPath);
  const fileStream = fs.createReadStream(resolvedPath);

  const response = await fetch("https://upload.heygen.com/v1/asset", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": contentType,
      "Content-Length": fileStats.size.toString(),
    },
    body: fileStream as any,
    // @ts-ignore - duplex is needed for streaming
    duplex: "half",
  });

  const json: AssetUploadResponse = await response.json();

  if (json.code !== 100) {
    throw new Error(json.message ?? "Upload failed");
  }

  return json.data;
}
```

### Python

```python
import requests
import os

def upload_asset(file_path: str, content_type: str) -> dict:
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://upload.heygen.com/v1/asset",
            headers={
                "X-Api-Key": os.environ["HEYGEN_API_KEY"],
                "Content-Type": content_type
            },
            data=f
        )

    data = response.json()
    if data.get("code") != 100:
        raise Exception(data.get("message", "Upload failed"))

    return data["data"]


# Usage
asset = upload_asset("./background.jpg", "image/jpeg")
print(f"Uploaded asset: {asset['id']}")
print(f"Asset URL: {asset['url']}")
```

## 支持的内容类型

| 类型 | Content-Type | 用例 |
|------|--------------|----------|
| JPEG | `image/jpeg` | 背景、说话照片 |
| PNG | `image/png` | 背景、叠加层 |
| MP4 | `video/mp4` | 视频背景 |
| WebM | `video/webm` | 视频背景 |
| MP3 | `audio/mpeg` | 自定义音频输入 |
| WAV | `audio/wav` | 自定义音频输入 |

## 从 URL 上传

如果您的资源已经托管在线：

```typescript
async function uploadFromUrl(sourceUrl: string, contentType: string): Promise<AssetUploadResponse["data"]> {
  // 1. Validate and download the file
  const url = new URL(sourceUrl);
  if (url.protocol !== "https:") {
    throw new Error("Only HTTPS URLs are supported");
  }
  const sourceResponse = await fetch(sourceUrl);
  const buffer = Buffer.from(await sourceResponse.arrayBuffer());

  // 2. Upload directly to HeyGen
  const response = await fetch("https://upload.heygen.com/v1/asset", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": contentType,
    },
    body: buffer,
  });

  const json: AssetUploadResponse = await response.json();

  if (json.code !== 100) {
    throw new Error(json.message ?? "Upload failed");
  }

  return json.data;
}
```

## 使用上传的资源

### 作为背景图片

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hello, this is a video with a custom background!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "image",
        url: asset.url,  // Use the URL from the upload response
      },
    },
  ],
};
```

### 作为说话照片源

```typescript
const talkingPhotoConfig = {
  video_inputs: [
    {
      character: {
        type: "talking_photo",
        talking_photo_id: asset.id,  // Use the ID from the upload response
      },
      voice: {
        type: "text",
        input_text: "Hello from my talking photo!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};
```

### 作为音频输入

```typescript
const audioConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "audio",
        audio_url: asset.url,  // Use the URL from the upload response
      },
    },
  ],
};
```

## 完整上传工作流程

```typescript
async function createVideoWithCustomBackground(
  backgroundPath: string,
  script: string
): Promise<string> {
  // 1. Upload background
  console.log("Uploading background...");
  const background = await uploadAsset(backgroundPath, "image/jpeg");

  // 2. Create video config
  const config = {
    video_inputs: [
      {
        character: {
          type: "avatar",
          avatar_id: "josh_lite3_20230714",
          avatar_style: "normal",
        },
        voice: {
          type: "text",
          input_text: script,
          voice_id: "1bd001e7e50f421d891986aad5158bc8",
        },
        background: {
          type: "image",
          url: background.url,
        },
      },
    ],
    dimension: { width: 1920, height: 1080 },
  };

  // 3. Generate video
  console.log("Generating video...");
  const response = await fetch("https://api.heygen.com/v2/video/generate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });

  const { data } = await response.json();
  return data.video_id;
}
```

## 资源限制

- **文件大小**：最大 10MB
- **图片尺寸**：建议匹配视频尺寸
- **音频时长**：应与预期视频长度匹配
- **保留期限**：资源可能在一段时间不活跃后被删除

## 最佳实践

1. **优化图片** - 上传前调整为匹配视频尺寸
2. **使用合适的格式** - 照片用 JPEG，带透明的图形用 PNG
3. **上传前验证** - 先在本地检查文件类型和大小
4. **处理上传错误** - 为失败的上传实现重试逻辑
5. **缓存资源 ID** - 在多个视频生成中重用资源
