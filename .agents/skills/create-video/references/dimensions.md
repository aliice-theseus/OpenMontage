---
name: dimensions
description: HeyGen 视频的分辨率选项（720p/1080p）和宽高比
---

# 视频尺寸和分辨率

HeyGen 支持各种视频尺寸和宽高比，以适应不同平台和用例。

## 标准分辨率

### 横屏（16:9）

| 分辨率 | 宽度 | 高度 | 用例 |
|------------|-------|--------|----------|
| 720p | 1280 | 720 | 标准质量，处理更快 |
| 1080p | 1920 | 1080 | 高质量，最常见 |

### 竖屏（9:16）

| 分辨率 | 宽度 | 高度 | 用例 |
|------------|-------|--------|----------|
| 720p | 720 | 1280 | 移动优先内容 |
| 1080p | 1080 | 1920 | 高质量竖版 |

### 方形（1:1）

| 分辨率 | 宽度 | 高度 | 用例 |
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

## 尺寸约束

- **最小**：任何边 128px
- **最大**：任何边 4096px
- **必须为偶数**：宽度和高度必须能被 2 整除

## 分辨率 vs 积分成本

较高分辨率可能消耗更多积分：

| 分辨率 | 相对成本 |
|------------|---------------|
| 720p | 基础费率 |
| 1080p | 约 1.5x 基础费率 |

考虑在草稿和测试时使用 720p，最终输出使用 1080p。
