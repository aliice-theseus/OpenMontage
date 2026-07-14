---
name: backgrounds
description: HeyGen 视频的纯色、图片和视频背景
---

# 视频背景

HeyGen 支持多种背景类型，用于自定义头像视频的外观。

## 背景类型

| 类型 | 描述 |
|------|-------------|
| `color` | 纯色背景 |
| `image` | 静态图片背景 |
| `video` | 循环视频背景 |

## 纯色背景

最简单的选项——使用纯色：

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
        input_text: "Hello with a colored background!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#FFFFFF", // 白色背景
      },
    },
  ],
};
```

### 常见颜色值

| 颜色 | Hex 值 | 使用场景 |
|-------|-----------|----------|
| 白色 | `#FFFFFF` | 干净、专业 |
| 黑色 | `#000000` | 戏剧化、电影感 |
| 蓝色 | `#0066CC` | 企业、可信赖 |
| 绿色 | `#00FF00` | 色度键（用于合成） |
| 灰色 | `#808080` | 中性、现代 |

### 使用透明/绿幕

用于后期制作中的合成：

```typescript
background: {
  type: "color",
  value: "#00FF00", // 绿幕
}
```

## 图片背景

使用静态图片作为背景：

### 从 URL

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
        input_text: "Check out this custom background!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "image",
        url: "https://example.com/my-background.jpg",
      },
    },
  ],
};
```

### 从已上传的资源

首先上传图片，然后使用资源 URL：

```typescript
// 1. 上传图片
const assetId = await uploadFile("./background.jpg", "image/jpeg");

// 2. 在视频配置中使用
const videoConfig = {
  video_inputs: [
    {
      character: {...},
      voice: {...},
      background: {
        type: "image",
        url: `https://files.heygen.ai/asset/${assetId}`,
      },
    },
  ],
};
```

### 图片要求

- **格式**：JPEG、PNG
- **建议尺寸**：匹配视频尺寸（例如 1080p 为 1920x1080）
- **宽高比**：应与视频宽高比匹配
- **文件大小**：建议 10MB 以下

## 视频背景

使用循环视频作为背景：

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
        input_text: "Dynamic video background!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "video",
        url: "https://example.com/background-loop.mp4",
      },
    },
  ],
};
```

### 视频要求

- **格式**：MP4（建议使用 H.264 编码）
- **循环**：如果视频比头像内容短，会自动循环
- **音频**：背景视频的音频通常会被静音
- **文件大小**：建议 100MB 以下

## 每个场景不同背景

为每个场景使用不同的背景：

```typescript
const multiBackgroundConfig = {
  video_inputs: [
    // 场景 1：办公室背景
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Let me start with an introduction.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "image",
        url: "https://example.com/office-bg.jpg",
      },
    },
    // 场景 2：产品展示
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "closeUp",
      },
      voice: {
        type: "text",
        input_text: "Now let me show you our product.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "image",
        url: "https://example.com/product-bg.jpg",
      },
    },
    // 场景 3：行动号召
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Get started today!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#1a1a2e",
      },
    },
  ],
};
```

## 背景辅助函数

### TypeScript

```typescript
type BackgroundType = "color" | "image" | "video";

interface Background {
  type: BackgroundType;
  value?: string;
  url?: string;
}

function createColorBackground(hexColor: string): Background {
  return { type: "color", value: hexColor };
}

function createImageBackground(imageUrl: string): Background {
  return { type: "image", url: imageUrl };
}

function createVideoBackground(videoUrl: string): Background {
  return { type: "video", url: videoUrl };
}

// 预设背景
const backgrounds = {
  white: createColorBackground("#FFFFFF"),
  black: createColorBackground("#000000"),
  greenScreen: createColorBackground("#00FF00"),
  corporate: createColorBackground("#0066CC"),
};
```

## 最佳实践

1. **匹配尺寸** - 背景应与视频尺寸匹配
2. **考虑头像位置** - 为头像显示留出空间
3. **使用对比色** - 确保头像在背景上可见
4. **优化文件大小** - 压缩图片/视频以加快处理速度
5. **测试绿幕** - 用于专业的后期制作工作流
6. **保持背景简洁** - 避免在头像后面放置分散注意力的元素

## 常见问题

### 背景不显示

```typescript
// 错误：缺少 url/value
background: {
  type: "image"
}

// 正确
background: {
  type: "image",
  url: "https://example.com/bg.jpg"
}
```

### 宽高比不匹配

如果你的背景与视频尺寸不匹配，可能会被裁剪或拉伸。始终将背景宽高比与视频尺寸匹配：

```typescript
// 对于 1920x1080 视频
// 使用 1920x1080 背景图片

// 对于 1080x1920 竖屏视频
// 使用 1080x1920 背景图片
```

### 视频背景音频

背景视频的音频通常会被静音，以避免与头像的声音冲突。如果你需要背景音乐，请在后期制作中添加为单独的音频轨道。
