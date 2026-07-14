# 输出格式

## 结果 JSON

主脚本（`understand_video.py`）输出一个 JSON 对象到标准输出（或使用 `-o` 输出到文件），包含视频元数据、提取的帧路径和转录数据。

```json
{
  "video": "video.mp4",
  "duration": 18.076,
  "resolution": {
    "width": 1224,
    "height": 1080
  },
  "mode": "scene",
  "frames": [
    {
      "path": "/absolute/path/to/frames/frame_0001.jpg",
      "timestamp": 0.0,
      "timestamp_formatted": "00:00"
    },
    {
      "path": "/absolute/path/to/frames/frame_0002.jpg",
      "timestamp": 3.2,
      "timestamp_formatted": "00:03"
    }
  ],
  "frame_count": 12,
  "transcript": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "Hello and welcome to this video."
    },
    {
      "start": 2.8,
      "end": 5.1,
      "text": "Today we will discuss..."
    }
  ],
  "text": "Hello and welcome to this video. Today we will discuss...",
  "note": "Use the Read tool to view frame images for visual understanding."
}
```

## 顶层字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `video` | string | 原始视频文件名（基本名称） |
| `duration` | float | 视频时长（秒） |
| `resolution` | object | 视频分辨率，包含 `width` 和 `height` |
| `mode` | string | 使用的提取模式：`scene`、`keyframe` 或 `interval` |
| `frames` | array | 提取的帧对象数组 |
| `frame_count` | integer | 提取的帧数 |
| `transcript` | array 或 null | 转录段落数组，跳过转录时为 `null` |
| `text` | string 或 null | 完整转录文本字符串，跳过时为 `null` |
| `note` | string | 提示 Claude 如何使用帧图像的提示信息 |

## 帧对象

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `path` | string | 提取的 JPEG 帧的绝对路径 |
| `timestamp` | float | 从视频开始到该帧的时间戳（秒） |
| `timestamp_formatted` | string | 人类可读的时间戳，格式为 `MM:SS` 或 `HH:MM:SS` |

## 转录段落

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `start` | float | 段落开始时间（秒） |
| `end` | float | 段落结束时间（秒） |
| `text` | string | 此段落的转录文本 |

## 帧路径约定

帧被提取到视频文件旁边的目录：

```
video.mp4
video_frames/
  frame_0001.jpg
  frame_0002.jpg
  ...
```

目录名称为 `{video_stem}_frames`。JSON 输出中的所有帧路径都是绝对路径，适合直接与 Read 工具一起使用。

## 空值字段

- 当使用 `--no-transcribe` 或未安装 Whisper 时，`transcript` 和 `text` 为 `null`。
- 如果场景检测未找到场景，模式自动回退到 `interval`，`mode` 字段反映实际使用的模式。

## 与 Claude 一起使用

要直观检查视频内容，请在 `frames` 数组返回的帧路径上使用 Read 工具。Claude 可以直接查看 JPEG 图像并描述其内容。结合转录，这提供了无需任何云 API 的完整视频理解。
