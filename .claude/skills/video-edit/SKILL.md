---
name: video-edit
description: |
  使用 ffmpeg 在本地编辑视频。支持裁剪、拼接、调整大小、变速、叠加、提取音频、压缩和格式转换。
  适用场景：(1) 裁剪或剪切视频片段，(2) 拼接多个片段，(3) 为社交媒体平台调整视频大小，
  (4) 提取或替换音频，(5) 压缩视频，(6) 转换视频格式，(7) 获取视频信息。
---

# 视频编辑

通过直接运行 ffmpeg/ffprobe 在本地编辑视频。无需包装脚本。

## 前提条件

安装 ffmpeg（包含 ffprobe）：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install -y ffmpeg

# 验证
ffmpeg -version && ffprobe -version
```

## 快速参考

### 获取视频信息

```bash
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4
```

### 裁剪

```bash
ffmpeg -y -ss 00:00:30 -to 00:01:45 -i video.mp4 -c copy trimmed.mp4
```

### 拼接片段

```bash
# 1. 创建文件列表
printf "file '%s'\n" clip1.mp4 clip2.mp4 clip3.mp4 > list.txt

# 2. 使用流复制拼接
ffmpeg -y -f concat -safe 0 -i list.txt -c copy joined.mp4
```

### 为平台调整大小

```bash
ffmpeg -y -i video.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:a copy tiktok.mp4
```

### 改变速度

```bash
# 2 倍快放
ffmpeg -y -i video.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" fast.mp4

# 0.5 倍（慢动作）
ffmpeg -y -i video.mp4 -filter:v "setpts=2.0*PTS" -filter:a "atempo=0.5" slow.mp4
```

### 提取音频

```bash
ffmpeg -y -i video.mp4 -vn -acodec libmp3lame audio.mp3
```

### 替换音频

```bash
ffmpeg -y -i video.mp4 -i audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest output.mp4
```

### 压缩

```bash
ffmpeg -y -i video.mp4 -crf 23 -preset medium -c:a copy compressed.mp4
```

### 转换格式

```bash
ffmpeg -y -i video.mov output.mp4
```

### 添加图片叠加

```bash
# 右上角标志
ffmpeg -y -i video.mp4 -i logo.png \
  -filter_complex "overlay=W-w-10:10" -c:a copy watermarked.mp4
```

## 平台预设

| 平台 | 分辨率 | 缩放 + 填充滤镜 |
|------------|-------------|-------------------------------------------------------------------------------------------------------|
| TikTok | 1080 x 1920 | `scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black` |
| YouTube | 1920 x 1080 | `scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black` |
| Instagram | 1080 x 1350 | `scale=1080:1350:force_original_aspect_ratio=decrease,pad=1080:1350:(ow-iw)/2:(oh-ih)/2:black` |
| 正方形 | 1080 x 1080 | `scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black` |
| Twitter/X | 1920 x 1080 | `scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black` |

使用以下命令配合该滤镜：`ffmpeg -y -i input.mp4 -vf "<filter>" -c:a copy output.mp4`

## 技巧

- 始终使用 `-y` 覆盖输出而不提示。
- 只需剪切/拼接时使用 `-c copy`（无需重新编码，非常快）。
- CRF 越低 = 质量越好，文件越大。典型范围 18-28；23 是默认值。
- 详细配方和标志说明，请参见 `references/operations.md`。
