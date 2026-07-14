---
name: video-understand
description: |
  使用 ffmpeg 帧提取和 Whisper 转录在本地理解视频内容。无需 API 密钥。
  适用场景：(1) 了解视频内容，(2) 本地转录视频音频，
  (3) 提取关键帧进行视觉分析，(4) 无需 API 密钥获取视频内容。
---

# video-understand

使用 ffmpeg 进行帧提取，使用 Whisper 进行转录，在本地理解视频内容。完全离线，无需 API 密钥。

## 前提条件

- `ffmpeg` + `ffprobe`（必需）：`brew install ffmpeg`
- `openai-whisper`（可选，用于转录）：`pip install openai-whisper`

## 命令

```bash
# 场景检测 + 转录（默认）
python3 skills/video-understand/scripts/understand_video.py video.mp4

# 关键帧提取
python3 skills/video-understand/scripts/understand_video.py video.mp4 -m keyframe

# 固定间隔提取
python3 skills/video-understand/scripts/understand_video.py video.mp4 -m interval

# 限制提取帧数
python3 skills/video-understand/scripts/understand_video.py video.mp4 --max-frames 10

# 使用更大的 Whisper 模型
python3 skills/video-understand/scripts/understand_video.py video.mp4 --whisper-model small

# 仅提取帧，跳过转录
python3 skills/video-understand/scripts/understand_video.py video.mp4 --no-transcribe

# 安静模式（仅 JSON，无进度信息）
python3 skills/video-understand/scripts/understand_video.py video.mp4 -q

# 输出到文件
python3 skills/video-understand/scripts/understand_video.py video.mp4 -o result.json
```

## CLI 选项

| 标志 | 描述 |
|------|-------------|
| `video` | 输入视频文件（位置参数，必填） |
| `-m, --mode` | 提取模式：`scene`（默认）、`keyframe`、`interval` |
| `--max-frames` | 最大保留帧数（默认：20） |
| `--whisper-model` | Whisper 模型大小：tiny、base、small、medium、large（默认：base） |
| `--no-transcribe` | 跳过音频转录，仅提取帧 |
| `-o, --output` | 将结果 JSON 写入文件而非标准输出 |
| `-q, --quiet` | 抑制进度信息，仅输出 JSON |

## 提取模式

| 模式 | 工作原理 | 最佳用途 |
|------|-------------|----------|
| `scene` | 通过 ffmpeg `select='gt(scene,0.3)'` 检测场景变化 | 大多数视频，多样化内容 |
| `keyframe` | 提取 I 帧（编解码器关键帧） | 具有自然关键帧放置的编码视频 |
| `interval` | 基于时长和最大帧数的均匀间隔帧 | 固定采样，可预测输出 |

如果 `scene` 模式未检测到场景变化，会自动回退到 `interval` 模式。

## 输出

脚本输出 JSON 到标准输出（或使用 `-o` 输出到文件）。详见 `references/output-format.md` 了解完整模式。

```json
{
  "video": "video.mp4",
  "duration": 18.076,
  "resolution": {"width": 1224, "height": 1080},
  "mode": "scene",
  "frames": [
    {"path": "/abs/path/frame_0001.jpg", "timestamp": 0.0, "timestamp_formatted": "00:00"}
  ],
  "frame_count": 12,
  "transcript": [
    {"start": 0.0, "end": 2.5, "text": "Hello and welcome..."}
  ],
  "text": "Full transcript...",
  "note": "Use the Read tool to view frame images for visual understanding."
}
```

使用 Read 工具查看帧图像路径，以直观检查提取的帧。

## 参考资料

- `references/output-format.md` -- 完整 JSON 输出模式文档
