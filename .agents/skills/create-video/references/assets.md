---
name: assets
description: 上传图片、视频和音频用于 HeyGen 视频生成
---

# 资产上传和管理

HeyGen 允许你上传自定义资产（图片、视频、音频）用于视频生成，例如背景、说话照片源和自定义音频。

## 上传流程

资产上传是单步骤过程：直接将原始文件二进制 POST 到上传端点。Content-Type 头必须匹配文件的 MIME 类型。

## 上传资产

**端点：** `POST https://upload.heygen.com/v1/asset`

### 请求

| 头 | 必需 | 描述 |
|--------|:--------:|-------------|
| `X-Api-Key` | ✓ | 你的 HeyGen API 密钥 |
| `Content-Type` | ✓ | 文件的 MIME 类型（例如 `image/jpeg`） |

请求主体是原始二进制文件数据。不需要 JSON 或表单字段。

### 响应

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `code` | number | 状态码（`100` = 成功） |
| `data.id` | string | 用于视频生成的唯一资产 ID |
| `data.name` | string | 资产名称 |
| `data.file_type` | string | `image`、`video` 或 `audio` |
| `data.url` | string | 上传文件的可访问 URL |
| `data.image_key` | string \| null | 用于创建上传照片虚拟形象的关键（仅图片） |
| `data.folder_id` | string | 文件夹 ID（如果不在文件夹中则为空） |
| `data.meta` | string \| null | 资产元数据 |
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
    throw new Error(json.message ?? "上传失败");
  }

  return json.data;
}

// 用法
const asset = await uploadAsset("./background.jpg", "image/jpeg");
console.log(`已上传资产：${asset.id}`);
console.log(`资产 URL：${asset.url}`);
```

## 支持的内容类型

| 类型 | Content-Type | 用例 |
|------|--------------|----------|
| JPEG | `image/jpeg` | 背景、说话照片 |
| PNG | `image/png` | 背景、叠加 |
| MP4 | `video/mp4` | 视频背景 |
| WebM | `video/webm` | 视频背景 |
| MP3 | `audio/mpeg` | 自定义音频输入 |
| WAV | `audio/wav` | 自定义音频输入 |

## 使用上传资产

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
        input_text: "你好，这是一个带自定义背景的视频！",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "image",
        url: asset.url,  // 使用上传响应中的 URL
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
        talking_photo_id: asset.id,  // 使用上传响应中的 ID
      },
      voice: {
        type: "text",
        input_text: "你好，来自我的说话照片！",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};
```

## 资产限制

- **文件大小**：最大 10MB
- **图片尺寸**：建议匹配视频尺寸
- **音频时长**：应与预期视频长度匹配
- **保留**：资产可能在一段不活动时间后被删除

## 最佳实践

1. **优化图片** - 上传前调整大小以匹配视频尺寸
2. **使用适当格式** - 照片用 JPEG，带透明度的图形用 PNG
3. **上传前验证** - 先本地检查文件类型和大小
4. **处理上传错误** - 对失败的上传实现重试逻辑
5. **缓存资产 ID** - 跨多个视频生成重用资产
