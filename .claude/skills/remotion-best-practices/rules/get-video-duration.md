---
name: get-video-duration
description: 使用 Mediabunny 获取视频文件时长（秒）
metadata:
  tags: duration, video, length, time, seconds
---

# 使用 Mediabunny 获取视频时长

Mediabunny 可以提取视频文件的时长。它可在浏览器、Node.js 和 Bun 环境中使用。

## 获取视频时长

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getVideoDuration = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {
      getRetryDelay: () => null,
    }),
  });

  const durationInSeconds = await input.computeDuration();
  return durationInSeconds;
};
```

## 使用方法

```tsx
const duration = await getVideoDuration("https://remotion.media/video.mp4");
console.log(duration); // 例如 10.5（秒）
```

## 来自 public/ 目录的视频文件

确保将文件路径包裹在 `staticFile()` 中：

```tsx
import { staticFile } from "remotion";

const duration = await getVideoDuration(staticFile("video.mp4"));
```

## 在 Node.js 和 Bun 中

使用 `FileSource` 替代 `UrlSource`：

```tsx
import { Input, ALL_FORMATS, FileSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new FileSource(file), // 来自输入或拖放的文件对象
});

const durationInSeconds = await input.computeDuration();
```
