---
name: get-audio-duration
description: 使用 Mediabunny 获取音频文件的时长（秒）
metadata:
  tags: duration, audio, length, time, seconds, mp3, wav
---

# 使用 Mediabunny 获取音频时长

Mediabunny 可以提取音频文件的时长。它适用于浏览器、Node.js 和 Bun 环境。

## 获取音频时长

```tsx title="get-audio-duration.ts"
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getAudioDuration = async (src: string) => {
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

## 用法

```tsx
const duration = await getAudioDuration("https://remotion.media/audio.mp3");
console.log(duration); // 例如 180.5（秒）
```

## 在 Remotion 中使用 staticFile

确保将文件路径包裹在 `staticFile()` 中：

```tsx
import { staticFile } from "remotion";

const duration = await getAudioDuration(staticFile("audio.mp3"));
```

## 在 Node.js 和 Bun 中

使用 `FileSource` 代替 `UrlSource`：

```tsx
import { Input, ALL_FORMATS, FileSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new FileSource(file), // 来自输入或拖放的文件对象
});
```
