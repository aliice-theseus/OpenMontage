---
name: dimensions
description: Resolution options (720p/1080p) and aspect ratios for HeyGen videos
---

# 视频尺寸与分辨率

HeyGen 支持多种视频尺寸和宽高比，以适应不同平台和用例。

## 标准分辨率

### 横屏（16:9）

| 分辨率 | 宽度 | 高度 | 用途 |
|------------|-------|--------|----------|
| 720p | 1280 | 720 | 标准质量，处理速度更快 |
| 1080p | 1920 | 1080 | 高质量，最常用 |

### 竖屏（9:16）

| 分辨率 | 宽度 | 高度 | 用途 |
|------------|-------|--------|----------|
| 720p | 720 | 1280 | 移动优先内容 |
| 1080p | 1080 | 1920 | 高质量竖屏 |

### 方形（1:1）

| 分辨率 | 宽度 | 高度 | 用途 |
|------------|-------|--------|----------|
| 720p | 720 | 720 | 社交媒体帖子 |
| 1080p | 1080 | 1080 | 高质量方形 |

## 设置尺寸

### TypeScript

```typescript
// 横屏 1080p
const landscapeConfig = {
  video_inputs: [...],
  dimension: {
    width: 1920,
    height: 1080
  }
};

// 竖屏 1080p
const portraitConfig = {
  video_inputs: [...],
  dimension: {
    width: 1080,
    height: 1920
  }
};

// 方形 1080p
const squareConfig = {
  video_inputs: [...],
  dimension: {
    width: 1080,
    height: 1080
  }
};
```

### curl

```bash
# 横屏 1080p
curl -X POST "https://api.heygen.com/v2/video/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_inputs": [...],
    "dimension": {
      "width": 1920,
      "height": 1080
    }
  }'
```

## 尺寸辅助函数

```typescript
type AspectRatio = "16:9" | "9:16" | "1:1" | "4:3" | "4:5";
type Quality = "720p" | "1080p";

interface Dimensions {
  width: number;
  height: number;
}

function getDimensions(aspectRatio: AspectRatio, quality: Quality): Dimensions {
  const configs: Record<AspectRatio, Record<Quality, Dimensions>> = {
    "16:9": {
      "720p": { width: 1280, height: 720 },
      "1080p": { width: 1920, height: 1080 },
    },
    "9:16": {
      "720p": { width: 720, height: 1280 },
      "1080p": { width: 1080, height: 1920 },
    },
    "1:1": {
      "720p": { width: 720, height: 720 },
      "1080p": { width: 1080, height: 1080 },
    },
    "4:3": {
      "720p": { width: 960, height: 720 },
      "1080p": { width: 1440, height: 1080 },
    },
    "4:5": {
      "720p": { width: 576, height: 720 },
      "1080p": { width: 864, height: 1080 },
    },
  };

  return configs[aspectRatio][quality];
}

// 使用示例
const youTubeDimensions = getDimensions("16:9", "1080p");
const tikTokDimensions = getDimensions("9:16", "1080p");
const instagramDimensions = getDimensions("1:1", "1080p");
```

## 平台特定推荐

### YouTube

```typescript
const youtubeConfig = {
  video_inputs: [...],
  dimension: { width: 1920, height: 1080 }, // 16:9 横屏
};
```

### TikTok / Instagram Reels / YouTube Shorts

```typescript
const shortFormConfig = {
  video_inputs: [...],
  dimension: { width: 1080, height: 1920 }, // 9:16 竖屏
};
```

### Instagram 信息流帖子

```typescript
const instagramFeedConfig = {
  video_inputs: [...],
  dimension: { width: 1080, height: 1080 }, // 1:1 方形
};
```

### LinkedIn

```typescript
const linkedinConfig = {
  video_inputs: [...],
  dimension: { width: 1920, height: 1080 }, // 推荐 16:9 横屏
};
```

### Twitter/X

```typescript
const twitterConfig = {
  video_inputs: [...],
  dimension: { width: 1280, height: 720 }, // 16:9，常用 720p
};
```

## Avatar IV 尺寸

对于 Avatar IV（基于照片的虚拟形象），通过方向设置尺寸：

```typescript
type VideoOrientation = "portrait" | "landscape" | "square";

function getAvatarIVDimensions(orientation: VideoOrientation): Dimensions {
  switch (orientation) {
    case "portrait":
      return { width: 720, height: 1280 };
    case "landscape":
      return { width: 1280, height: 720 };
    case "square":
      return { width: 720, height: 720 };
  }
}
```

## 自定义尺寸

HeyGen 支持在限制范围内的自定义尺寸：

```typescript
const customConfig = {
  video_inputs: [...],
  dimension: {
    width: 1600,
    height: 900  // 自定义 16:9 非标准分辨率
  }
};
```

### 尺寸限制

- **最小值**：任意边不少于 128px
- **最大值**：任意边不超过 4096px
- **必须为偶数**：宽度和高度都必须能被 2 整除

```typescript
function validateDimensions(width: number, height: number): boolean {
  if (width < 128 || height < 128) {
    throw new Error("尺寸必须至少为 128px");
  }
  if (width > 4096 || height > 4096) {
    throw new Error("尺寸不能超过 4096px");
  }
  if (width % 2 !== 0 || height % 2 !== 0) {
    throw new Error("尺寸必须为偶数");
  }
  return true;
}
```

## 分辨率与积分消耗

更高的分辨率可能消耗更多积分：

| 分辨率 | 相对成本 |
|------------|---------------|
| 720p | 基础费率 |
| 1080p | 约基础费率的 1.5 倍 |

建议草稿和测试阶段使用 720p，最终输出使用 1080p。

## 背景注意事项

确保背景图片/视频的尺寸与视频尺寸匹配：

```typescript
// 适用于 1080p 横屏视频
const config = {
  video_inputs: [
    {
      character: {...},
      voice: {...},
      background: {
        type: "image",
        url: "https://example.com/1920x1080-background.jpg" // 匹配视频尺寸
      }
    }
  ],
  dimension: { width: 1920, height: 1080 }
};
```

## 创建视频配置工厂

```typescript
interface VideoConfigOptions {
  script: string;
  avatarId: string;
  voiceId: string;
  platform: "youtube" | "tiktok" | "instagram_feed" | "instagram_story" | "linkedin";
  quality?: "720p" | "1080p";
}

function createVideoConfig(options: VideoConfigOptions) {
  const platformDimensions: Record<string, Dimensions> = {
    youtube: { width: 1920, height: 1080 },
    tiktok: { width: 1080, height: 1920 },
    instagram_feed: { width: 1080, height: 1080 },
    instagram_story: { width: 1080, height: 1920 },
    linkedin: { width: 1920, height: 1080 },
  };

  const dimension = platformDimensions[options.platform];

  // 如果请求 720p，则按比例缩小
  if (options.quality === "720p") {
    dimension.width = Math.round((dimension.width * 720) / 1080);
    dimension.height = Math.round((dimension.height * 720) / 1080);
  }

  return {
    video_inputs: [
      {
        character: {
          type: "avatar",
          avatar_id: options.avatarId,
          avatar_style: "normal",
        },
        voice: {
          type: "text",
          input_text: options.script,
          voice_id: options.voiceId,
        },
      },
    ],
    dimension,
  };
}

// 使用示例
const tiktokVideo = createVideoConfig({
  script: "大家好！看看这个！",
  avatarId: "josh_lite3_20230714",
  voiceId: "1bd001e7e50f421d891986aad5158bc8",
  platform: "tiktok",
  quality: "1080p",
});
```
