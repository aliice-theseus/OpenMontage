# 输出格式

## 结果 JSON

主脚本（`understand_video.py`）输出一个 JSON 对象到 stdout（或使用 `-o` 到文件），包含视频元数据、提取的帧路径和转录数据。

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
  "note": "使用 Read 工具查看帧图像以进行视觉理解。"
}
```

## 顶层字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `video` | string | 原始视频文件名（基本名称）|
| `duration` | float | 视频时长（秒）|
| `resolution` | object | 视频分辨率，包含 `width` 和 `height` |
| `mode` | string | 使用的提取模式：`scene`、`keyframe` 或 `interval` |
| `frames` | array | 提取的帧对象数组 |
| `frame_count` | integer | 提取的帧数 |
| `transcript` | array 或 null | 转录片段数组，如果跳过转录则为 `null` |
| `text` | string 或 null | 完整转录为单个字符串，如果跳过则为 `null` |
| `note` | string | 关于如何使用帧图像的提示 |

## 帧对象

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `path` | string | 提取的 JPEG 帧的绝对路径 |
| `timestamp` | float | 从视频开始的帧时间戳（秒）|
| `timestamp_formatted` | string | 人类可读的时间戳，格式为 `MM:SS` 或 `HH:MM:SS` |

## 转录片段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `start` | float | 片段开始时间（秒）|
| `end` | float | 片段结束时间（秒）|
| `text` | string | 此片段的转录文本 |

## 帧路径约定

帧提取到视频文件旁边的目录：

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
- 如果场景检测未找到场景，模式自动回退到 `interval`，并且 `mode` 字段反映实际使用的模式。

## 与 Claude 一起使用

要视觉检查视频内容，使用 Read 工具读取 `frames` 数组中返回的帧路径。Claude 可以直接查看 JPEG 图像并描述其内容。结合转录，无需任何云 API 即可提供完整的视频理解。
