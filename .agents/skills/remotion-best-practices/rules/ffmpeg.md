---
name: ffmpeg
description: 在 Remotion 中使用 FFmpeg 和 FFprobe
metadata:
  tags: ffmpeg, ffprobe, video, trimming
---

## Remotion 中的 FFmpeg

`ffmpeg` 和 `ffprobe` 无需安装。可通过 `bunx remotion ffmpeg` 和 `bunx remotion ffprobe` 使用：

```bash
bunx remotion ffmpeg -i input.mp4 output.mp3
bunx remotion ffprobe input.mp4
```

### 裁剪视频

你有 2 种裁剪视频的选项：

1. 使用 FFmpeg 命令行。你必须重新编码视频，以避免视频开头出现冻结帧。

```bash
# 从精确帧开始重新编码
bunx remotion ffmpeg -ss 00:00:05 -i public/input.mp4 -to 00:00:10 -c:v libx264 -c:a aac public/output.mp4
```

2. 使用 `<Video>` 组件的 `trimBefore` 和 `trimAfter` 属性。好处是非破坏性的，你可以随时更改裁剪设置。

```tsx
import { Video } from "@remotion/media";

<Video
  src={staticFile("video.mp4")}
  trimBefore={5 * fps}
  trimAfter={10 * fps}
/>;
```
