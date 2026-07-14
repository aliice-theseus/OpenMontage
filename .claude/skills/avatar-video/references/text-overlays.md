---
name: text-overlays
description: Adding text overlays with fonts and positioning to HeyGen videos
---

# 文字叠加

向 HeyGen 视频添加文字叠加，用于标题、字幕、下三分之一等屏幕文字元素。

## 基本文字叠加

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
        input_text: "Welcome to our presentation!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#1a1a2e",
      },
    },
  ],
  // Text overlay configuration (if supported in your API tier)
  // Note: Availability varies by plan
};
```

## 文字叠加配置

文字叠加通常支持以下属性：

```typescript
interface TextOverlay {
  text: string;
  x: number;          // X position (pixels or percentage)
  y: number;          // Y position (pixels or percentage)
  width?: number;     // Text box width
  height?: number;    // Text box height
  font_family?: string;
  font_size?: number;
  font_color?: string;
  background_color?: string;
  text_align?: "left" | "center" | "right";
  duration?: {
    start: number;    // Start time in seconds
    end: number;      // End time in seconds
  };
}
```

## 定位文字

### 坐标系

- **原点**：左上角 (0, 0)
- **X 轴**：向右增加
- **Y 轴**：向下增加
- **单位**：通常为像素或视频尺寸的百分比

### 常用位置

对于 1920x1080 的视频：

| 位置 | X | Y | 描述 |
|----------|---|---|-------------|
| 左上 | 50 | 50 | 左上角 |
| 顶部居中 | 960 | 50 | 顶部中央 |
| 右上 | 1870 | 50 | 右上角 |
| 居中 | 960 | 540 | 正中央 |
| 左下 | 50 | 1030 | 下三分之一左侧 |
| 底部居中 | 960 | 1030 | 下三分之一中央 |

### 位置辅助函数

```typescript
interface Position {
  x: number;
  y: number;
}

function getTextPosition(
  location: "top-left" | "top-center" | "top-right" | "center" | "bottom-left" | "bottom-center" | "bottom-right",
  videoWidth: number,
  videoHeight: number,
  padding: number = 50
): Position {
  const positions: Record<string, Position> = {
    "top-left": { x: padding, y: padding },
    "top-center": { x: videoWidth / 2, y: padding },
    "top-right": { x: videoWidth - padding, y: padding },
    "center": { x: videoWidth / 2, y: videoHeight / 2 },
    "bottom-left": { x: padding, y: videoHeight - padding },
    "bottom-center": { x: videoWidth / 2, y: videoHeight - padding },
    "bottom-right": { x: videoWidth - padding, y: videoHeight - padding },
  };

  return positions[location];
}
```

## 字体样式

### 可用字体属性

```typescript
const textStyle = {
  font_family: "Arial",
  font_size: 48,
  font_color: "#FFFFFF",
  font_weight: "bold",
  background_color: "rgba(0, 0, 0, 0.5)",
  text_align: "center",
};
```

### 常用字体族

| 字体 | 风格 | 用例 |
|------|-------|----------|
| Arial | 无衬线 | 干净、通用 |
| Helvetica | 无衬线 | 现代、专业 |
| Times New Roman | 衬线 | 传统、正式 |
| Georgia | 衬线 | 优雅、易读 |
| Roboto | 无衬线 | 现代、数字化 |
| Open Sans | 无衬线 | 友好、易访问 |

## 常见文字叠加模式

### 标题卡片

```typescript
const titleOverlay = {
  text: "Product Demo",
  x: 960,
  y: 540,
  font_family: "Arial",
  font_size: 72,
  font_color: "#FFFFFF",
  text_align: "center",
  duration: {
    start: 0,
    end: 3,
  },
};
```

### 下三分之一（姓名/头衔）

```typescript
const lowerThirdOverlay = {
  text: "John Smith\nCEO, Company Inc.",
  x: 100,
  y: 900,
  font_family: "Arial",
  font_size: 36,
  font_color: "#FFFFFF",
  background_color: "rgba(0, 102, 204, 0.9)",
  text_align: "left",
  duration: {
    start: 2,
    end: 8,
  },
};
```

### 行动号召

```typescript
const ctaOverlay = {
  text: "Visit example.com",
  x: 960,
  y: 1000,
  font_family: "Arial",
  font_size: 42,
  font_color: "#FFD700",
  text_align: "center",
  duration: {
    start: 25,
    end: 30,
  },
};
```

## 创建文字叠加模板

```typescript
interface TextOverlayTemplate {
  name: string;
  style: Partial<TextOverlay>;
}

const templates: TextOverlayTemplate[] = [
  {
    name: "title",
    style: {
      font_family: "Arial",
      font_size: 72,
      font_color: "#FFFFFF",
      text_align: "center",
    },
  },
  {
    name: "subtitle",
    style: {
      font_family: "Arial",
      font_size: 42,
      font_color: "#CCCCCC",
      text_align: "center",
    },
  },
  {
    name: "lower-third",
    style: {
      font_family: "Arial",
      font_size: 36,
      font_color: "#FFFFFF",
      background_color: "rgba(0, 0, 0, 0.7)",
      text_align: "left",
    },
  },
  {
    name: "caption",
    style: {
      font_family: "Arial",
      font_size: 32,
      font_color: "#FFFFFF",
      background_color: "rgba(0, 0, 0, 0.5)",
      text_align: "center",
    },
  },
];

function createTextOverlay(
  text: string,
  templateName: string,
  position: Position,
  duration?: { start: number; end: number }
): TextOverlay {
  const template = templates.find((t) => t.name === templateName);

  if (!template) {
    throw new Error(`Template "${templateName}" not found`);
  }

  return {
    text,
    x: position.x,
    y: position.y,
    ...template.style,
    duration,
  };
}
```

## 文字叠加的时间控制

将文字出现与脚本同步：

```typescript
// Script with timing markers
const script = `
Hello and welcome. [0:00 - 0:03]
Let me show you our features. [0:03 - 0:08]
First, we have analytics. [0:08 - 0:15]
Get started today! [0:15 - 0:20]
`;

// Matching text overlays
const overlays = [
  {
    text: "Welcome",
    duration: { start: 0, end: 3 },
    ...titleStyle,
  },
  {
    text: "Feature Overview",
    duration: { start: 3, end: 8 },
    ...subtitleStyle,
  },
  {
    text: "Analytics Dashboard",
    duration: { start: 8, end: 15 },
    ...lowerThirdStyle,
  },
  {
    text: "www.example.com",
    duration: { start: 15, end: 20 },
    ...ctaStyle,
  },
];
```

## 最佳实践

1. **可读性** - 在文字和背景之间使用足够的对比度
2. **大小** - 确保文字在移动设备上足够大以便阅读
3. **时长** - 给观众足够的阅读时间（经验法则：至少 3 秒）
4. **定位** - 不要与虚拟形象的面部重叠
5. **一致性** - 全程使用一致的字体和样式
6. **无障碍** - 考虑对色盲友好的配色方案

## 限制

- 文字叠加支持因订阅等级而异
- 某些高级样式选项可能无法通过 API 使用
- 复杂的动画可能需要后期制作工具
- 有关自动生成字幕，请参阅 [captions.md](captions.md)
