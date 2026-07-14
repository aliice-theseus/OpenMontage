# FFmpeg 参考

## 滤镜语法

### 视频滤镜（-vf）

```bash
# 用逗号链式组合滤镜
-vf "scale=1920:1080,fps=30,crop=1280:720"

# 带标签的复杂滤镜
-filter_complex "[0:v]scale=1920:1080[scaled];[scaled]fps=30[out]" -map "[out]"
```

### 常用视频滤镜

| 滤镜 | 语法 | 示例 |
|--------|--------|---------|
| scale | `scale=w:h` | `scale=1920:1080` 或 `scale=1280:-1`（自动高度） |
| crop | `crop=w:h:x:y` | `crop=1280:720:320:180` |
| fps | `fps=N` | `fps=30` |
| pad | `pad=w:h:x:y:color` | `pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black` |
| fade | `fade=t=in/out:st=N:d=N` | `fade=t=in:st=0:d=1` |
| setpts | `setpts=N*PTS` | `setpts=0.5*PTS`（2 倍速） |
| drawtext | `drawtext=text='Hi':fontsize=24` | 添加文本叠加 |
| overlay | `overlay=x:y` | 合并视频 |

### 常用音频滤镜（-af）

| 滤镜 | 语法 | 示例 |
|--------|--------|---------|
| volume | `volume=N` | `volume=1.5` 或 `volume=0.5` |
| afade | `afade=t=in/out:st=N:d=N` | `afade=t=in:st=0:d=1` |
| atempo | `atempo=N` | `atempo=2.0`（2 倍速，范围 0.5-2.0） |
| loudnorm | `loudnorm` | 标准化音频电平 |

## 编解码器选项

### 视频编解码器（-c:v）

| 编解码器 | 用途 | 说明 |
|-------|----------|-------|
| libx264 | 通用 H.264 | 最佳兼容性 |
| libx265 | H.265/HEVC | 更好的压缩，兼容性较低 |
| libvpx-vp9 | WebM | 适合网络使用 |
| prores | ProRes | 专业编辑 |
| copy | 流复制 | 无需重新编码，最快 |

### 音频编解码器（-c:a）

| 编解码器 | 用途 | 说明 |
|-------|----------|-------|
| aac | MP4 容器 | 兼容性最好 |
| libmp3lame | MP3 | 通用 |
| libvorbis | WebM/OGG | 开源 |
| pcm_s16le | WAV | 未压缩 |
| copy | 流复制 | 无需重新编码 |

## 质量设置

### x264/x265 的 CRF（恒定速率因子）

| CRF | 质量 | 用途 |
|-----|---------|----------|
| 0 | 无损 | 存档 |
| 17-18 | 视觉无损 | 母版 |
| 19-22 | 高质量 | 生产 |
| 23 | 默认 | 通用 |
| 24-27 | 中等 | 网络分发 |
| 28+ | 低 | 预览/草稿 |

### 预设（-preset）

更快的预设 = 更大的文件，更快的编码

`ultrafast` → `superfast` → `veryfast` → `faster` → `fast` → `medium` → `slow` → `slower` → `veryslow`

## 容器格式

| 格式 | 扩展名 | 最佳用途 |
|--------|-----------|----------|
| MP4 | .mp4 | 通用、网络、移动 |
| MOV | .mov | Apple 生态系统、ProRes |
| WebM | .webm | 网络（VP9） |
| MKV | .mkv | 存档、多流 |
| GIF | .gif | 短动画（无音频） |

## 输入/输出选项

### 输入选项（在 -i 之前）

| 选项 | 用途 | 示例 |
|--------|---------|---------|
| -ss | 定位到时间点 | `-ss 00:01:30` |
| -t | 时长限制 | `-t 00:00:30` |
| -r | 输入帧率 | `-r 30` |
| -f | 强制格式 | `-f gif` |

### 输出选项（在 -i 之后）

| 选项 | 用途 | 示例 |
|--------|---------|---------|
| -y | 覆盖输出 | `-y` |
| -n | 从不覆盖 | `-n` |
| -movflags faststart | 网络流式播放 | `-movflags faststart` |
| -pix_fmt | 像素格式 | `-pix_fmt yuv420p` |
| -an | 无音频 | `-an` |
| -vn | 无视频 | `-vn` |

## 实用模式

### 获取时长（秒）

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 input.mp4
```

### 获取分辨率

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 input.mp4
```

### 获取帧数

```bash
ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 input.mp4
```

### 创建缩略图

```bash
# 在指定时间点
ffmpeg -i input.mp4 -ss 00:00:05 -vframes 1 thumbnail.jpg

# 最佳质量
ffmpeg -i input.mp4 -ss 00:00:05 -vframes 1 -q:v 2 thumbnail.jpg
```

### 从视频创建 GIF

```bash
# 简单（大文件）
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1" output.gif

# 带调色板（更好质量，更小文件）
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

### 画中画

```bash
# 在角落叠加小视频
ffmpeg -i main.mp4 -i overlay.mp4 \
  -filter_complex "[1:v]scale=320:-1[pip];[0:v][pip]overlay=W-w-20:H-h-20" \
  -c:a copy output.mp4
```

### 并排视频

```bash
ffmpeg -i left.mp4 -i right.mp4 \
  -filter_complex "[0:v][1:v]hstack=inputs=2[v]" \
  -map "[v]" -c:v libx264 output.mp4
```

## Remotion 集成说明

- Remotion 使用 `<OffthreadVideo>`，支持大多数格式
- 首选 MP4 容器中的 H.264（libx264）
- 始终使用 `-movflags faststart` 以便网络播放
- 帧率匹配合成设置（通常 30fps）
- 分辨率应与合成匹配（通常 1920x1080）
