---
name: text-overlays
description: 在 HeyGen 视频中添加带字体和定位的文字叠加
---

# 文字叠加

在 HeyGen 视频中添加文字叠加层，用于标题、字幕、下三分之一等屏幕文字元素。

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
  // 文字叠加配置（如果 API 套餐支持）
  // 注意：可用性因套餐而异
};
```

## 文字叠加配置

文字叠加通常支持以下属性：

```typescript
interface TextOverlay {
  text: string;
  x: number;          // X 位置（像素或百分比）
  y: number;          // Y 位置（像素或百分比）
  width?: number;     // 文本框宽度
  height?: number;    // 文本框高度
  font_family?: string;
  font_size?: number;
  font_color?: string;
  background_color?: string;
  text_align?: "left" | "center" | "right";
  duration?: {
    start: number;    // 开始时间（秒）
    end: number;      // 结束时间（秒）
  };
}
```

## 定位文字

### 坐标系统

- **原点**：左上角 (0, 0)
- **X 轴**：向右增加
- **Y 轴**：向下增加
- **单位**：通常为像素或视频尺寸的百分比

### 常见位置

对于 1920x1080 视频：

| 位置 | X | Y | 描述 |
|----------|---|---|-------------|
| 左上角 | 50 | 50 | 左上角 |
| 顶部居中 | 960 | 50 | 顶部中央 |
| 右上角 | 1870 | 50 | 右上角 |
| 居中 | 960 | 540 | 正中央 |
| 左下角 | 50 | 1030 | 下三分之一左侧 |
| 底部居中 | 960 | 1030 | 下三分之一居中 |

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

### 常见字体族

| 字体 | 样式 | 使用场景 |
|------|-------|----------|
| Arial | 无衬线 | 干净、通用 |
| Helvetica | 无衬线 | 现代、专业 |
| Times New Roman | 衬线 | 传统、正式 |
| Georgia | 衬线 | 优雅、可读性强 |
| Roboto | 无衬线 | 现代、数字 |
| Open Sans | 无衬线 | 友好、易访问 |

## 常见文字叠加模式

### 标题卡片

```typescript
const titleOverlay = {
  text: "产品演示",
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
  text: "访问 example.com",
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
    throw new Error(`未找到模板 "${templateName}"`);
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

## 文字叠加时序

将文字出现时间与脚本同步：

```typescript
// 带时间标记的脚本
const script = `
大家好，欢迎。 [0:00 - 0:03]
让我展示我们的功能。 [0:03 - 0:08]
首先，我们有分析功能。 [0:08 - 0:15]
今天就加入我们！ [0:15 - 0:20]
`;

// 匹配的文字叠加
const overlays = [
  {
    text: "欢迎",
    duration: { start: 0, end: 3 },
    ...titleStyle,
  },
  {
    text: "功能概述",
    duration: { start: 3, end: 8 },
    ...subtitleStyle,
  },
  {
    text: "分析仪表盘",
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

1. **可读性** - 使用足够的文字/背景对比度
2. **大小** - 确保文字在移动设备上也足够大
3. **时长** - 给观众足够的阅读时间（经验法则：至少 3 秒）
4. **定位** - 不要与头像的脸部重叠
5. **一致性** - 在整个视频中使用一致的字体和样式
6. **可访问性** - 考虑色盲友好的调色板

## 限制

- 文字叠加支持因订阅套餐而异
- 某些高级样式选项可能无法通过 API 使用
- 复杂动画可能需要后期制作工具
- 如需自动生成字幕，请参见 [captions.md](captions.md)
