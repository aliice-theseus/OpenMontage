---
name: video-download
description: |
  使用 yt-dlp 从 YouTube 及 1000+ 站点下载视频和音频。无需 API 密钥。
  在以下情况下使用：(1) 从 YouTube 或其他站点下载视频，(2) 从视频 URL 提取音频，
  (3) 从视频下载字幕/隐藏式字幕，(4) 在不下载的情况下获取视频元数据。
---

# 视频下载

使用 yt-dlp 直接从 URL 下载视频和音频。无需包装脚本。

## 前置条件

- **yt-dlp**：`brew install yt-dlp` 或 `pip install yt-dlp`
- **ffmpeg**：`brew install ffmpeg` 或 `apt install ffmpeg`（合并视频+音频流时需要）

定期更新 yt-dlp 以跟上站点变化：`yt-dlp -U` 或 `pip install -U yt-dlp`。

## 命令

### 下载最佳质量

```bash
yt-dlp "URL" -o "%(title)s.%(ext)s" --merge-output-format mp4
```

### 下载特定分辨率

```bash
# 720p
yt-dlp "URL" -f "bestvideo[height<=720]+bestaudio/best[height<=720]" --merge-output-format mp4

# 1080p
yt-dlp "URL" -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" --merge-output-format mp4
```

### 仅音频

```bash
yt-dlp "URL" -x --audio-format mp3 --audio-quality 0
```

### 下载字幕

```bash
# 下载带英文字幕的视频
yt-dlp "URL" --write-subs --sub-langs en --merge-output-format mp4

# 下载带多种字幕语言的视频
yt-dlp "URL" --write-subs --sub-langs "en,es,fr" --merge-output-format mp4

# 仅下载字幕（无视频）
yt-dlp "URL" --write-subs --sub-langs en --skip-download
```

### 获取元数据（不下载）

```bash
yt-dlp "URL" --dump-json --no-download
```

### 列出可用格式

```bash
yt-dlp "URL" -F
```

### 指定输出目录

```bash
yt-dlp "URL" -o "./downloads/%(title)s.%(ext)s" --merge-output-format mp4
```

## 质量预设

| 质量 | 格式标志 |
|---------|-------------|
| 最佳 | `-f "bestvideo+bestaudio/best"`（默认） |
| 1080p | `-f "bestvideo[height<=1080]+bestaudio/best[height<=1080]"` |
| 720p | `-f "bestvideo[height<=720]+bestaudio/best[height<=720]"` |
| 480p | `-f "bestvideo[height<=480]+bestaudio/best[height<=480]"` |
| 最差 | `-f "worstvideo+worstaudio/worst"` |

## 输出模板变量

`-o` 模板的常用变量：

| 变量 | 描述 |
|----------|-------------|
| `%(title)s` | 视频标题 |
| `%(ext)s` | 文件扩展名 |
| `%(id)s` | 视频 ID |
| `%(uploader)s` | 频道/上传者名称 |
| `%(upload_date)s` | 上传日期（YYYYMMDD） |
| `%(duration)s` | 时长（秒） |
| `%(resolution)s` | 视频分辨率 |

## 提示

- 始终使用 `--merge-output-format mp4` 以避免得到 `.webm` 或 `.mkv` 文件。
- 使用 `--no-download` 配合 `--dump-json` 进行仅元数据查询 — 不写入磁盘文件。
- 如果下载因 HTTP 错误失败，先更新 yt-dlp（`yt-dlp -U`）。
- 当不需要全分辨率时，使用 `-f "bestvideo[height<=720]+bestaudio"` 节省带宽。
- yt-dlp 自动处理速率限制和重试。
- `--dump-json` 输出包含 `title`、`duration`、`uploader`、`view_count`、`description`、`formats`、`subtitles` 等大量信息。

## 故障排除

- **"yt-dlp: command not found"**：安装它（`pip install yt-dlp`）并确保你的 PATH 包含 pip 的 bin 目录。
- **"ffmpeg: command not found"**：安装 ffmpeg。没有它，当视频和音频是分离流时（这在 YouTube 的 HD 视频中很常见），下载会失败。
- **下载失败或返回错误**：运行 `yt-dlp -U` 更新。站点经常变化，yt-dlp 定期发布修复。
