# 实时事件参考

实时语音转文字流式传输中事件的完整参考。

## 发送事件（客户端 → 服务器）

### input_audio_chunk

发送音频数据进行转录。

```json
{
  "message_type": "input_audio_chunk",
  "audio_base_64": "<base64 编码的 pcm 音频>",
  "commit": false,
  "sample_rate": 16000
}
```

| 字段 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `message_type` | string | 是 | 始终为 `"input_audio_chunk"` |
| `audio_base_64` | string | 是 | Base64 编码的 PCM 音频数据 |
| `commit` | boolean | 是 | 是否在此块后提交 |
| `sample_rate` | number | 否 | 采样率，单位 Hz（8000-48000） |
| `previous_text` | string | 否 | 之前转录的上下文（仅第一个块，最多 50 个字符） |

### commit

最终确定当前转录片段。

```json
{
  "message_type": "commit"
}
```

## 接收事件（服务器 → 客户端）

所有接收的事件使用 `message_type` 作为鉴别字段。

### session_started

连接成功建立。

```json
{
  "message_type": "session_started",
  "session_id": "0b0a72b57fd743ebbed6555d44836cf2",
  "config": {
    "sample_rate": 16000,
    "audio_format": "pcm_16000",
    "language_code": "en",
    "model_id": "scribe_v2_realtime",
    "commit_strategy": "manual",
    "include_timestamps": true
  }
}
```

### partial_transcript

中间转录结果，随着音频处理而频繁更新。

```json
{
  "message_type": "partial_transcript",
  "text": "你好，你"
}
```

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `message_type` | string | `"partial_transcript"` |
| `text` | string | 当前部分转录 |

### committed_transcript

提交后的最终转录。

```json
{
  "message_type": "committed_transcript",
  "text": "你好，你今天怎么样？"
}
```

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `message_type` | string | `"committed_transcript"` |
| `text` | string | 最终确定的转录 |

### committed_transcript_with_timestamps

带词级计时的最终转录。当 `include_timestamps=true` 时在 `committed_transcript` 之后发送。

```json
{
  "message_type": "committed_transcript_with_timestamps",
  "text": "你好，你今天怎么样？",
  "language_code": "zh",
  "words": [
    {"text": "你好", "start": 0.0, "end": 0.32, "type": "word"},
    {"text": " ", "start": 0.32, "end": 0.35, "type": "spacing"},
    {"text": "你", "start": 0.40, "end": 0.55, "type": "word"}
  ]
}
```

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `message_type` | string | `"committed_transcript_with_timestamps"` |
| `text` | string | 完整转录文本 |
| `language_code` | string | 检测到的语言代码 |
| `words` | array | 词级计时数据 |
| `words[].text` | string | 词或标记 |
| `words[].start` | number | 开始时间（秒） |
| `words[].end` | number | 结束时间（秒） |
| `words[].type` | string | `"word"`、`"spacing"` 或 `"audio_event"` |
| `words[].speaker_id` | string | 说话人标识符（如果启用了说话人分离） |

## 错误事件

### error

发生错误时发送。

```json
{
  "message_type": "error",
  "error": "input_error"
}
```

### 错误码

| 码 | 描述 |
|------|-------------|
| `auth_error` | API 密钥或令牌无效 |
| `quota_exceeded` | 达到使用限制 |
| `input_error` | 不支持的音频格式或无效输入 |
| `rate_limited` | 请求过多 |
| `commit_throttled` | 提交发送过于频繁 |
| `session_time_limit_exceeded` | 会话超过最大持续时间 |
| `unaccepted_terms` | 未在仪表板中接受条款 |
| `resource_exhausted` | 服务器容量已满 |
| `queue_overflow` | 服务器队列容量已满 |
| `chunk_size_exceeded` | 音频块过大 |
| `insufficient_audio_activity` | 未检测到足够的语音 |
| `transcriber_error` | 内部处理错误 |

## 连接事件

### open

WebSocket 连接已建立（标准 WebSocket 事件，不是 JSON 消息）。

### close

WebSocket 连接已关闭（标准 WebSocket 关闭帧，含代码和原因）。

## 事件处理示例

### Python

Python SDK 抽象了网络协议。使用 SDK 的事件对象时，可以使用 `event.type`（而不是 `message_type`）：

```python
async for event in connection:
    if event.type == "session_started":
        print(f"会话：{event.session_id}")
    elif event.type == "partial_transcript":
        print(f"部分：{event.text}")
    elif event.type == "committed_transcript":
        print(f"最终：{event.text}")
    elif event.type == "committed_transcript_with_timestamps":
        for word in event.words:
            print(f"  {word.text}: {word.start}s - {word.end}s")
    elif event.type == "error":
        print(f"错误：{event.error}")
```

### JavaScript

JavaScript SDK 使用与 `message_type` 值匹配的事件名称：

```javascript
connection.on("session_started", (data) => {
  console.log("会话：", data.sessionId);
});

connection.on("partial_transcript", (data) => {
  console.log("部分：", data.text);
});

connection.on("committed_transcript", (data) => {
  console.log("最终：", data.text);
});

connection.on("committed_transcript_with_timestamps", (data) => {
  for (const word of data.words) {
    console.log(`  ${word.text}: ${word.start}s - ${word.end}s`);
  }
});

connection.on("error", (error) => {
  console.error("错误：", error);
});
```
