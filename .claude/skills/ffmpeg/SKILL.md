---
name: ffmpeg
description: 使用 FFmpeg 进行视频和音频处理。适用于格式转换、调整大小、压缩、音频提取和为 Remotion 准备素材。触发场景包括将 GIF 转换为 MP4、调整视频大小、提取音频、压缩文件或任何媒体转换任务。
---

# 视频制作中的 FFmpeg

FFmpeg 是视频/音频处理的基本工具。本技能涵盖 Remotion 视频项目的常见操作。

## 快速参考

### GIF 转 MP4（Remotion 兼容）

```bash
ffmpeg -i input.gif -movflags faststart -pix_fmt yuv420p \
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4
```

**为什么使用这些标志：**
- `-movflags faststart` - 将元数据移到文件开头，便于网络流式播放
- `-pix_fmt yuv420p` - 确保与大多数播放器兼容
- `scale=trunc(...)` - 强制为偶数尺寸（大多数编解码器要求）

### 调整视频大小

```bash
# 调整为 1920x1080（保持宽高比，添加黑边）
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4

# 调整为 1920x1080（裁剪填充）
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" output.mp4

# 按宽度缩放，高度自动
ffmpeg -i input.mp4 -vf "scale=1280:-2" output.mp4
```

### 压缩视频

```bash
# 良好质量，较小文件（CRF 23 是默认值，越低质量越好）
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4

# 网络预览的激进压缩
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k output.mp4

# 目标文件大小（例如 60s 视频约 10MB = 约 1.3Mbps）
ffmpeg -i input.mp4 -c:v libx264 -b:v 1300k -c:a aac -b:a 128k output.mp4
```

### 提取音频

```bash
# 提取为 MP3
ffmpeg -i input.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3

# 提取为 AAC
ffmpeg -i input.mp4 -vn -acodec aac -b:a 192k output.m4a

# 提取为 WAV（未压缩）
ffmpeg -i input.mp4 -vn output.wav
```

### 转换音频格式

```bash
# M4A 转 MP3（用于 ElevenLabs 语音样本）
ffmpeg -i input.m4a -codec:a libmp3lame -qscale:a 2 output.mp3

# WAV 转 MP3
ffmpeg -i input.wav -codec:a libmp3lame -b:a 192k output.mp3

# 调整音量
ffmpeg -i input.mp3 -filter:a "volume=1.5" output.mp3
```

### 裁剪/剪切视频

```bash
# 从时间戳开始裁剪指定时长（推荐 - 可靠）
ffmpeg -i input.mp4 -ss 00:00:30 -t 00:00:15 -c:v libx264 -c:a aac output.mp4

# 从时间戳到时间戳裁剪
ffmpeg -i input.mp4 -ss 00:00:30 -to 00:00:45 -c:v libx264 -c:a aac output.mp4

# 流复制（更快，但可能在剪切点丢失帧）
# 仅当源具有频繁的关键帧时使用
ffmpeg -i input.mp4 -ss 00:00:30 -t 00:00:15 -c copy output.mp4
```

**注意：** 建议对裁剪进行重新编码。流复制（`-c copy`）如果查找点不与关键帧对齐，可能会静默丢弃视频。

### 加速/减速

```bash
# 2 倍速（视频和音频）
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" output.mp4

# 0.5 倍速（慢动作）
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" output.mp4

# 仅视频（无音频）
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -an output.mp4
```

### 拼接视频

```bash
# 创建文件列表
echo "file 'clip1.mp4'" > list.txt
echo "file 'clip2.mp4'" >> list.txt
echo "file 'clip3.mp4'" >> list.txt

# 拼接（相同编解码器/分辨率）
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# 带重新编码的拼接（不同源文件）
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
```

### 添加淡入/淡出

```bash
# 前 1 秒淡入，后 1 秒淡出（30fps 视频）
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=9:d=1" -c:a copy output.mp4

# 音频淡入淡出
ffmpeg -i input.mp4 -af "afade=t=in:st=0:d=1,afade=t=out:st=9:d=1" -c:v copy output.mp4
```

### 获取视频信息

```bash
# 时长、分辨率、编解码器信息
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4

# 完整信息
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

## Remotion 特定模式

### 为 Remotion 调整视频速度

**何时使用 FFmpeg vs Remotion playbackRate：**

| 场景 | 使用 FFmpeg | 使用 Remotion |
|----------|------------|--------------|
| 恒定速度（1.5x、2x） | 两者都行 | ✅ 更简单 |
| 极端速度（>4x 或 <0.25x） | ✅ 更可靠 | 可能有问题 |
| 变速（随时间加速） | ✅ 预处理 | 需要复杂变通方案 |
| 需要完美的音频同步 | ✅ 有保证 | 通常可以 |
| 演示需要适配画外音时长 | ✅ 预先计算 | 运行时调整 |

**Remotion 限制：** `playbackRate` 必须恒定。如 `playbackRate={interpolate(frame, [0, 100], [1, 5])}` 这样的动态插值无法正确工作，因为 Remotion 独立评估每帧。

```bash
# 加速演示以适配场景（例如 60s 演示放入 20s = 3 倍速）
ffmpeg -i demo-raw.mp4 \
  -filter_complex "[0:v]setpts=0.333*PTS[v];[0:a]atempo=3.0[a]" \
  -map "[v]" -map "[a]" \
  public/demos/demo-fast.mp4

# 慢动作强调效果（0.5 倍速）
ffmpeg -i action.mp4 \
  -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" \
  -map "[v]" -map "[a]" \
  public/demos/action-slow.mp4

# 仅加速视频（无音频，常见于屏幕录制）
ffmpeg -i demo.mp4 -filter:v "setpts=0.5*PTS" -an public/demos/demo-2x.mp4

# 延时效果（10 倍速，丢弃音频）
ffmpeg -i long-demo.mp4 -filter:v "setpts=0.1*PTS" -an public/demos/timelapse.mp4
```

**计算速度系数：**
- 将 X 秒视频适配到 Y 秒场景：`speed = X / Y`
- setpts 乘数 = `1 / speed`（例如 3 倍速 = setpts=0.333*PTS）
- atempo 值 = `speed`（例如 3 倍速 = atempo=3.0）

**极端速度（音频 >2x）：** 链式 atempo 滤镜（每个限制在 0.5-2.0 范围内）：
```bash
# 4 倍速音频
-filter_complex "[0:a]atempo=2.0,atempo=2.0[a]"

# 8 倍速音频
-filter_complex "[0:a]atempo=2.0,atempo=2.0,atempo=2.0[a]"
```

### 准备用于 Remotion 的演示录制

```bash
# 标准 1080p、30fps、Remotion 就绪
ffmpeg -i raw-recording.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 192k \
  -movflags faststart \
  public/demos/demo.mp4
```

### 屏幕录制转为 Remotion 素材

```bash
# 来自 iPhone/iPad 录制（通常 60fps，可变分辨率）
ffmpeg -i iphone-recording.mov \
  -vf "scale=1920:-2,fps=30" \
  -c:v libx264 -crf 20 \
  -an \
  public/demos/mobile-demo.mp4
```

### 批量转换 GIF

```bash
for f in assets/*.gif; do
  ffmpeg -i "$f" -movflags faststart -pix_fmt yuv420p \
    -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
    "public/demos/$(basename "$f" .gif).mp4"
done
```

## 常见问题

### "Height not divisible by 2"
添加缩放滤镜：`-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`

### 视频在浏览器中无法播放
使用：`-movflags faststart -pix_fmt yuv420p -c:v libx264`

### 速度变化后音画不同步
使用带 atempo 的 filter_complex：`-filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]"`

### 文件太大
增加 CRF（23→28）或降低分辨率

## 质量指南

| 用途 | CRF | 预设 | 说明 |
|----------|-----|--------|-------|
| 存档/母版 | 18 | slow | 最佳质量，大文件 |
| 生产 | 20-22 | medium | 良好平衡 |
| 网络/预览 | 23-25 | fast | 较小文件 |
| 草稿/快速 | 28+ | veryfast | 快速编码 |

## 按平台输出优化

Remotion 渲染视频后（通常输出到 `out/video.mp4`），使用 FFmpeg 针对每个分发平台进行优化。

### 工作流程集成

```
Remotion 渲染（母版）     FFmpeg 优化          平台上传
       ↓                       ↓                     ↓
   out/video.mp4  ────────→  out/video-youtube.mp4  ───→  YouTube
                   ────────→  out/video-twitter.mp4  ───→  Twitter/X
                   ────────→  out/video-linkedin.mp4 ───→  LinkedIn
                   ────────→  out/video-web.mp4      ───→  网站嵌入
```

### YouTube（推荐设置）

YouTube 会重新编码所有内容，因此上传高质量源：

```bash
# YouTube 优化（1080p）
ffmpeg -i out/video.mp4 \
  -c:v libx264 -preset slow -crf 18 \
  -profile:v high -level 4.0 \
  -bf 2 -g 30 \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart \
  out/video-youtube.mp4

# YouTube Shorts（竖屏 1080x1920）
ffmpeg -i out/video.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -crf 18 -c:a aac -b:a 192k \
  out/video-shorts.mp4
```

### Twitter/X

Twitter 有严格限制：最长 140s、512MB、1920x1200：

```bash
# Twitter 优化（目标 15MB 以下以便快速上传）
ffmpeg -i out/video.mp4 \
  -c:v libx264 -preset medium -crf 24 \
  -profile:v main -level 3.1 \
  -vf "scale='min(1280,iw)':'min(720,ih)':force_original_aspect_ratio=decrease" \
  -c:a aac -b:a 128k -ar 44100 \
  -movflags +faststart \
  -fs 15M \
  out/video-twitter.mp4

# 检查文件大小和时长
ffprobe -v error -show_entries format=duration,size -of csv=p=0 out/video-twitter.mp4
```

### LinkedIn

LinkedIn 偏好带 AAC 音频的 MP4，最长 10 分钟：

```bash
# LinkedIn 优化
ffmpeg -i out/video.mp4 \
  -c:v libx264 -preset medium -crf 22 \
  -profile:v main \
  -vf "scale='min(1920,iw)':'min(1080,ih)':force_original_aspect_ratio=decrease" \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart \
  out/video-linkedin.mp4
```

### 网站/嵌入（针对快速加载优化）

```bash
# Web 优化 MP4（小文件，渐进式加载）
ffmpeg -i out/video.mp4 \
  -c:v libx264 -preset medium -crf 26 \
  -profile:v baseline -level 3.0 \
  -vf "scale=1280:720" \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  out/video-web.mp4

# WebM 替代方案（更好的压缩，更广泛的浏览器支持）
ffmpeg -i out/video.mp4 \
  -c:v libvpx-vp9 -crf 30 -b:v 0 \
  -vf "scale=1280:720" \
  -c:a libopus -b:a 128k \
  -deadline good \
  out/video-web.webm
```

### GIF（用于预览/缩略图）

```bash
# 高质量 GIF（前 5 秒）
ffmpeg -i out/video.mp4 -t 5 \
  -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  out/preview.gif

# 小文件 GIF
ffmpeg -i out/video.mp4 -t 3 \
  -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  out/preview-small.gif
```

### 平台要求快速参考

| 平台 | 最大分辨率 | 最大大小 | 最长时长 | 音频 |
|----------|---------------|----------|--------------|-------|
| YouTube | 8K | 256GB | 12 小时 | AAC 48kHz |
| Twitter/X | 1920x1200 | 512MB | 140s | AAC 44.1kHz |
| LinkedIn | 4096x2304 | 5GB | 10 分钟 | AAC 48kHz |
| Instagram Feed | 1080x1350 | 4GB | 60s | AAC 48kHz |
| Instagram Reels | 1080x1920 | 4GB | 90s | AAC 48kHz |
| TikTok | 1080x1920 | 287MB | 10 分钟 | AAC |

### 所有平台批量导出

```bash
#!/bin/bash
# 保存为：export-all-platforms.sh
INPUT="out/video.mp4"

# YouTube（高质量）
ffmpeg -i "$INPUT" -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k -movflags +faststart \
  out/video-youtube.mp4

# Twitter（压缩）
ffmpeg -i "$INPUT" -c:v libx264 -crf 24 \
  -vf "scale='min(1280,iw)':'-2'" \
  -c:a aac -b:a 128k -movflags +faststart \
  out/video-twitter.mp4

# LinkedIn
ffmpeg -i "$INPUT" -c:v libx264 -crf 22 \
  -c:a aac -b:a 192k -movflags +faststart \
  out/video-linkedin.mp4

# Web 嵌入（小）
ffmpeg -i "$INPUT" -c:v libx264 -crf 26 \
  -vf "scale=1280:720" \
  -c:a aac -b:a 128k -movflags +faststart \
  out/video-web.mp4

echo "已导出："
ls -lh out/video-*.mp4
```

## 错误处理

处理视频时的常见错误和修复：

```bash
# 检查 FFmpeg 是否成功
ffmpeg -i input.mp4 -c:v libx264 output.mp4 && echo "Success" || echo "Failed: check input file"

# 验证输出文件是否可播放
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 output.mp4

# 获取详细错误信息
ffmpeg -v error -i input.mp4 -f null - 2>&1 | head -20
```

### 处理常见失败

| 错误 | 原因 | 修复 |
|-------|-------|-----|
| "No such file" | 输入路径错误 | 检查路径，对空格使用引号 |
| "Invalid data" | 输入文件损坏 | 重新下载或重新录制源文件 |
| "height not divisible by 2" | 奇数尺寸 | 添加带 trunc 的缩放滤镜 |
| "encoder not found" | 缺少编解码器 | 安装带完整编解码器的 FFmpeg |
| 输出 0 字节 | 静默失败 | 检查完整 ffmpeg 输出中的错误 |

---

## 反馈与贡献

如果此技能缺少信息或可以改进：

- **缺少某个命令？** 描述您需要的内容
- **发现错误？** 请告知问题所在
- **想要贡献？** 我可以帮助您：
  1. 用改进更新此技能
  2. 向 github.com/digitalsamba/claude-code-video-toolkit 创建 PR

只需说"improve this skill"，我将引导您更新 `.claude/skills/ffmpeg/SKILL.md`。
