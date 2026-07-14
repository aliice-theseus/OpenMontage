---
name: captions
description: HeyGen 视频的自动生成字幕和副标题选项
---

# 视频字幕

HeyGen 可以自动为你的视频生成字幕，提高可访问性和参与度。

## 启用字幕

生成视频时可以启用字幕：

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
  // 字幕设置（可用性因套餐而异）
  caption: true,
};
```

## 字幕配置选项

```typescript
interface CaptionConfig {
  // 启用/禁用字幕
  enabled: boolean;

  // 字幕样式
  style?: {
    font_family?: string;
    font_size?: number;
    font_color?: string;
    background_color?: string;
    position?: "top" | "bottom";
  };

  // 字幕生成语言
  language?: string;
}
```

## 字幕样式

### 基本字幕

```typescript
const config = {
  video_inputs: [...],
  caption: true, // 启用默认样式
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
// 西班牙语视频带西班牙语字幕
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

对于视频翻译，你可以提供自己的 SRT：

```typescript
const translationConfig = {
  input_video_id: "original_video_id",
  output_languages: ["es-ES", "fr-FR"],
  srt_key: "path/to/custom.srt", // 自定义 SRT 文件
  srt_role: "input", // "input" 或 "output"
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

当底部空间被占用时：

```typescript
caption: {
  enabled: true,
  style: {
    position: "top"
  }
}
```

## 可访问性最佳实践

1. **始终启用字幕** - 提高对听障观众的友好度
2. **使用高对比度** - 白色文字配深色背景，或反之
3. **可读的字体大小** - 标准视频至少 24px，移动端更大
4. **不要遮挡重要内容** - 将字幕放置在远离关键视觉元素的位置
5. **同步时间** - 确保字幕与音频时间准确匹配

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

- 将字幕置于中央或上半部分
- 避免底部 20%（被 UI 元素遮挡）
- 移动端观看使用更大的字体

```typescript
const socialCaptions = {
  enabled: true,
  style: {
    font_size: 42,
    position: "top", // 避免底部 UI 元素
  },
};
```

### YouTube

- 标准底部字幕效果良好
- YouTube 也支持上传隐藏式字幕

### LinkedIn

- 强烈推荐使用字幕（许多人静音观看）
- 倾向于专业样式

## 限制

- 字幕样式可能因订阅等级而受限
- 一些高级字幕功能可能需要 Web 界面
- 多人说话的字幕检测可能有限
- 字幕准确度取决于音频质量和语音清晰度

## 与视频翻译集成

使用视频翻译时，字幕会自动处理：

```typescript
// 视频翻译包括字幕生成
const translationConfig = {
  input_video_id: "original_video_id",
  output_languages: ["es-ES"],
  // 字幕以目标语言生成
};
```

参见 [video-translation.md](video-translation.md) 了解更多详情。
