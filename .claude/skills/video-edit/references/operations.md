# 操作参考

每个操作的详细 ffmpeg 配方。每个部分显示命令，解释关键标志，并列出常见变体。

---

## info

使用 ffprobe 获取视频文件的完整元数据。

```bash
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4
```

**关键标志：**
- `-v quiet` — 禁止横幅/日志噪音，仅输出请求的数据。
- `-print_format json` — 输出为 JSON（易于解析）。也支持 `csv`、`flat`、`ini`。
- `-show_format` — 容器级别信息：时长、比特率、格式名称、大小。
- `-show_streams` — 每个流的信息：编解码器、分辨率、帧率、采样率、通道数。

**变体：**
```bash
# 仅时长（秒，纯文本）
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 video.mp4

# 仅分辨率
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 video.mp4
```

---

## trim

使用流复制剪切视频片段（无需重新编码，非常快）。

```bash
ffmpeg -y -ss 00:00:30 -to 00:01:45 -i video.mp4 -c copy trimmed.mp4
```

**关键标志：**
- `-ss <time>` — 定位到起始位置。放在 `-i` 之前用于快速输入定位。
- `-to <time>` — 在此时间戳停止（绝对时间）。替代方案：`-t <duration>` 用于相对时长。
- `-c copy` — 无需重新编码复制流。速度快但仅在关键帧上剪切（可能差几帧）。

**时间戳** 支持 `HH:MM:SS`、`HH:MM:SS.mmm`、`MM:SS` 或原始秒数（`90`、`90.5`）。

**变体：**
```bash
# 按时长而非结束时间
ffmpeg -y -ss 00:00:30 -t 75 -i video.mp4 -c copy trimmed.mp4

# 帧精确裁剪（重新编码，较慢但精确）
ffmpeg -y -ss 00:00:30 -to 00:01:45 -i video.mp4 -c:v libx264 -c:a aac trimmed.mp4
```

---

## concat

将多个视频文件合并为单个文件。

```bash
# 步骤 1：创建拼接列表文件
printf "file '%s'\n" clip1.mp4 clip2.mp4 clip3.mp4 > list.txt

# 步骤 2：使用流复制拼接
ffmpeg -y -f concat -safe 0 -i list.txt -c copy joined.mp4
```

**关键标志：**
- `-f concat` — 使用 concat 分离器。
- `-safe 0` — 允许文件列表中的绝对路径。
- `-c copy` — 无需重新编码复制流。要求所有输入共享相同编解码器、分辨率和帧率。

**变体：**
```bash
# 重新编码以标准化不匹配的片段（较慢）
ffmpeg -y -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac joined.mp4

# 内联拼接无需文件（仅相同格式文件）
ffmpeg -y -i "concat:part1.ts|part2.ts" -c copy joined.ts
```

---

## resize

将视频调整为特定尺寸，同时保持宽高比并填充。

```bash
ffmpeg -y -i video.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:a copy resized.mp4
```

**关键标志：**
- `-vf` — 视频滤镜链。
- `scale=W:H:force_original_aspect_ratio=decrease` — 缩小以适配 WxH 内，保持宽高比。
- `pad=W:H:(ow-iw)/2:(oh-ih)/2:black` — 填充到精确 WxH，居中黑边。
- `-c:a copy` — 无需重新编码复制音频。

**变体：**
```bash
# 按宽度缩放，自动计算高度（保持宽高比）
ffmpeg -y -i video.mp4 -vf "scale=1280:-2" -c:a copy resized.mp4

# 按高度缩放，自动计算宽度
ffmpeg -y -i video.mp4 -vf "scale=-2:720" -c:a copy resized.mp4

# 自定义尺寸无填充（拉伸）
ffmpeg -y -i video.mp4 -vf "scale=1280:720" -c:a copy resized.mp4
```

---

## speed

同时改变视频和音频的播放速度。

```bash
# 2 倍快放
ffmpeg -y -i video.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" fast.mp4

# 半速（慢动作）
ffmpeg -y -i video.mp4 -filter:v "setpts=2.0*PTS" -filter:a "atempo=0.5" slow.mp4
```

**关键标志：**
- `-filter:v "setpts=N*PTS"` — 乘以展示时间戳。`0.5` = 2 倍快放，`2.0` = 半速。公式：`N = 1 / speed_factor`。
- `-filter:a "atempo=F"` — 调整音频速度。保持音调。仅支持 0.5 到 2.0 之间的值。

**对于 0.5-2.0 之外的因子**，链式使用多个 atempo 滤镜：
```bash
# 4 倍快放
ffmpeg -y -i video.mp4 -filter:v "setpts=0.25*PTS" -filter:a "atempo=2.0,atempo=2.0" fast4x.mp4

# 0.25 倍（极慢）
ffmpeg -y -i video.mp4 -filter:v "setpts=4.0*PTS" -filter:a "atempo=0.5,atempo=0.5" slow025x.mp4
```

---

## extract-audio

从视频文件中提取音轨。

```bash
ffmpeg -y -i video.mp4 -vn -acodec libmp3lame audio.mp3
```

**关键标志：**
- `-vn` — 禁用视频（仅音频输出）。
- `-acodec <codec>` — 使用的音频编解码器。

**音频编解码器映射：**

| 格式 | 编解码器标志 |
|--------|------------------|
| mp3 | `libmp3lame` |
| wav | `pcm_s16le` |
| aac | `aac` |
| flac | `flac` |

**变体：**
```bash
# 提取为 WAV（无损）
ffmpeg -y -i video.mp4 -vn -acodec pcm_s16le audio.wav

# 提取为 AAC
ffmpeg -y -i video.mp4 -vn -acodec aac audio.aac

# 原样复制音频编解码器（最快，保持原始格式）
ffmpeg -y -i video.mp4 -vn -acodec copy audio.aac
```

---

## replace-audio

用不同的音频文件替换视频的音轨。

```bash
ffmpeg -y -i video.mp4 -i audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest output.mp4
```

**关键标志：**
- `-i video.mp4 -i audio.mp3` — 两个输入：视频（索引 0）和音频（索引 1）。
- `-c:v copy` — 无需重新编码复制视频流。
- `-map 0:v:0` — 从第一个输入取视频。
- `-map 1:a:0` — 从第二个输入取音频。
- `-shortest` — 当较短的输入结束时停止。

**变体：**
```bash
# 完全移除音频（静音视频）
ffmpeg -y -i video.mp4 -c:v copy -an silent.mp4

# 混合原始音频和新音频（叠加，非替换）
ffmpeg -y -i video.mp4 -i music.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy mixed.mp4
```

---

## overlay

在视频顶部添加图片叠加（水印、标志）。

```bash
# 右下角（10px 间距）
ffmpeg -y -i video.mp4 -i logo.png \
  -filter_complex "overlay=W-w-10:H-h-10" -c:a copy watermarked.mp4
```

**关键标志：**
- `-filter_complex "overlay=X:Y"` — 将叠加图片定位在坐标 X,Y。
- `-c:a copy` — 无需重新编码复制音频。

**位置表达式：**

| 位置 | 表达式 |
|--------------|-------------------------|
| 左上角 | `overlay=10:10` |
| 右上角 | `overlay=W-w-10:10` |
| 左下角 | `overlay=10:H-h-10` |
| 右下角 | `overlay=W-w-10:H-h-10` |
| 居中 | `overlay=(W-w)/2:(H-h)/2` |

`W`/`H` = 视频尺寸，`w`/`h` = 叠加图片尺寸。

**变体：**
```bash
# 带透明度（半透明水印）
ffmpeg -y -i video.mp4 -i logo.png \
  -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.5[ovr];[0:v][ovr]overlay=W-w-10:10" \
  -c:a copy watermarked.mp4

# 仅在时间段内叠加（从 5s 到 15s 显示）
ffmpeg -y -i video.mp4 -i logo.png \
  -filter_complex "overlay=10:10:enable='between(t,5,15)'" -c:a copy watermarked.mp4
```

---

## compress

减小视频文件大小。

### 基于 CRF（简单，推荐）

```bash
ffmpeg -y -i video.mp4 -crf 23 -preset medium -c:a copy compressed.mp4
```

**关键标志：**
- `-crf <int>` — 恒定速率因子。越低 = 质量越好，文件越大。0 = 无损，18 = 视觉无损，23 = 默认，28 = 更小/更低质量。
- `-preset <speed>` — 编码速度/压缩权衡：`ultrafast`、`superfast`、`veryfast`、`faster`、`fast`、`medium`、`slow`、`slower`、`veryslow`。越慢 = 相同质量下文件越小。
- `-c:a copy` — 原样复制音频。

### 目标文件大小

要达到特定文件大小，计算所需的视频比特率：

```bash
# 公式：video_bitrate = (target_MB * 8 * 1024) / duration_seconds - audio_bitrate
# 示例：25MB 目标，120s 视频，128kbps 音频
# video_bitrate = (25 * 8 * 1024) / 120 - 128 = 1578 kbps

ffmpeg -y -i video.mp4 \
  -b:v 1578k -maxrate 1578k -bufsize 3156k \
  -c:a aac -b:a 128k \
  compressed.mp4
```

**变体：**
```bash
# 激进压缩（更小，更低质量）
ffmpeg -y -i video.mp4 -crf 28 -preset slow -c:a copy small.mp4

# 高质量（更大文件）
ffmpeg -y -i video.mp4 -crf 18 -preset slow -c:a copy hq.mp4
```

---

## convert

将视频转换为不同容器格式。

```bash
ffmpeg -y -i video.mov output.mp4
```

ffmpeg 从文件扩展名推断输出格式。对于大多数转换，这已经足够。

**支持的格式：** mp4、mov、avi、mkv、webm、gif。

### GIF 转换（高质量，双通道调色板）

```bash
# 步骤 1：生成优化调色板
ffmpeg -y -i video.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" palette.png

# 步骤 2：使用调色板生成高质量 GIF
ffmpeg -y -i video.mp4 -i palette.png \
  -filter_complex "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif

# 清理
rm palette.png
```

**变体：**
```bash
# 快速 GIF（较低质量，单通道）
ffmpeg -y -i video.mp4 -vf "fps=10,scale=320:-1" output.gif

# 转换为 WebM（VP9）
ffmpeg -y -i video.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm
```
