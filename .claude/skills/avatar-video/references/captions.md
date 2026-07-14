---
name: captions
description: Auto-generated captions and subtitle options for HeyGen videos
---

# 视频字幕

HeyGen 可以自动为您的视频生成字幕，提高可访问性和参与度。

## 启用字幕

在生成视频时可以启用字幕：

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
        input_text: "Hello! This video will have automatic captions.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
  // Caption settings (availability varies by plan)
  caption: true,
};
```

## 字幕配置选项

```typescript
interface CaptionConfig {
  // Enable/disable captions
  enabled: boolean;

  // Caption style
  style?: {
    font_family?: string;
    font_size?: number;
    font_color?: string;
    background_color?: string;
    position?: "top" | "bottom";
  };

  // Language for caption generation
  language?: string;
}
```

## 字幕样式

### 基本字幕

```typescript
const config = {
  video_inputs: [...],
  caption: true, // Enable with default styling
};
```

### 带样式的字幕

```typescript
const config = {
  video_inputs: [...],
  caption: {
    enabled: true,
    style: {
      font_family: "Arial",
      font_size: 32,
      font_color: "#FFFFFF",
      background_color: "rgba(0, 0, 0, 0.7)",
      position: "bottom",
    },
  },
};
```

## 多语言字幕

对于不同语言的视频，字幕根据语音语言生成：

```typescript
// Spanish video with Spanish captions
const spanishConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "¡Hola! Este video tendrá subtítulos en español.",
        voice_id: "spanish_voice_id",
      },
    },
  ],
  caption: true,
};
```

## 使用 SRT 文件

### SRT 文件格式

标准 SRT 格式：

```srt
1
00:00:00,000 --> 00:00:03,000
Hello! This video will have

2
00:00:03,000 --> 00:00:06,000
automatic captions generated.

3
00:00:06,000 --> 00:00:09,000
They sync with the audio.
```

### 使用自定义 SRT

对于视频翻译，您可以提供自己的 SRT：

```typescript
const translationConfig = {
  input_video_id: "original_video_id",
  output_languages: ["es-ES", "fr-FR"],
  srt_key: "path/to/custom.srt", // Custom SRT file
  srt_role: "input", // "input" or "output"
};
```

## 字幕定位

### 底部（默认）

大多数视频的标准位置：

```typescript
caption: {
  enabled: true,
  style: {
    position: "bottom"
  }
}
```

### 顶部

适用于底部空间被占用的视频：

```typescript
caption: {
  enabled: true,
  style: {
    position: "top"
  }
}
```

## 无障碍最佳实践

1. **始终启用字幕** - 提高对聋哑/听障观众的可访问性
2. **使用高对比度** - 深色背景上的白色文字，或反之
3. **可读的字体大小** - 标准视频至少 24px，移动端更大
4. **不要遮盖重要内容** - 将字幕放置在关键视觉元素之外
5. **同步时间** - 确保字幕与音频时间精确匹配

## 字幕辅助函数

```typescript
interface CaptionStyle {
  font_family: string;
  font_size: number;
  font_color: string;
  background_color: string;
  position: "top" | "bottom";
}

const captionPresets: Record<string, CaptionStyle> = {
  default: {
    font_family: "Arial",
    font_size: 32,
    font_color: "#FFFFFF",
    background_color: "rgba(0, 0, 0, 0.7)",
    position: "bottom",
  },
  minimal: {
    font_family: "Arial",
    font_size: 28,
    font_color: "#FFFFFF",
    background_color: "transparent",
    position: "bottom",
  },
  bold: {
    font_family: "Arial",
    font_size: 36,
    font_color: "#FFFFFF",
    background_color: "rgba(0, 0, 0, 0.9)",
    position: "bottom",
  },
  branded: {
    font_family: "Roboto",
    font_size: 30,
    font_color: "#00D1FF",
    background_color: "rgba(26, 26, 46, 0.9)",
    position: "bottom",
  },
};

function createCaptionConfig(preset: keyof typeof captionPresets) {
  return {
    enabled: true,
    style: captionPresets[preset],
  };
}
```

## 社交媒体字幕注意事项

### TikTok / Instagram Reels

- 将字幕定位在中间或上部
- 避免底部 20%（被 UI 元素覆盖）
- 移动端观看时使用更大的字体大小

```typescript
const socialCaptions = {
  enabled: true,
  style: {
    font_size: 42,
    position: "top", // Avoid bottom UI elements
  },
};
```

### YouTube

- 标准底部字幕效果良好
- YouTube 也支持上传隐藏式字幕

### LinkedIn

- 强烈推荐使用字幕（许多人无声观看）
- 首选专业风格

## 限制

- 字幕样式可能因订阅等级而受限
- 某些高级字幕功能可能需要使用网页界面
- 多人说话的字幕检测可能受限
- 字幕准确性取决于音频质量和语音清晰度

## 与视频翻译集成

使用视频翻译时，字幕会自动处理：

```typescript
// Video translation includes caption generation
const translationConfig = {
  input_video_id: "original_video_id",
  output_languages: ["es-ES"],
  // Captions generated in target language
};
```

有关视频翻译的更多详细信息，请参阅 **video-translate** 技能。
