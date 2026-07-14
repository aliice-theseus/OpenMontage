---
name: speech-to-text
description: 使用 ElevenLabs Scribe v2 将音频转录为文本。在转换音频/视频为文本、生成字幕、转录会议或处理口语内容时使用。
license: MIT
compatibility: 需要互联网连接和 ElevenLabs API 密钥（ELEVENLABS_API_KEY）。
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs 语音转文本

使用 Scribe v2 将音频转录为文本——支持 90+ 种语言、说话人分离和词级时间戳。

> **设置：** 请参阅 [安装指南](references/installation.md)。对于 JavaScript，请仅使用 `@elevenlabs/*` 包。

## 快速入门

### Python

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

with open("audio.mp3", "rb") as audio_file:
    result = client.speech_to_text.convert(file=audio_file, model_id="scribe_v2")

print(result.text)
```

### JavaScript

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { createReadStream } from "fs";

const client = new ElevenLabsClient();
const result = await client.speechToText.convert({
  file: createReadStream("audio.mp3"),
  modelId: "scribe_v2",
});
console.log(result.text);
```

### cURL

```bash
curl -X POST "https://api.elevenlabs.io/v1/speech-to-text" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -F "file=@audio.mp3" -F "model_id=scribe_v2"
```

## 模型

| 模型 ID               | 描述                                     | 最佳用途                     |
|-----------------------|------------------------------------------|------------------------------|
| `scribe_v2`           | 最先进的准确度，90+ 种语言               | 批量转录、字幕、长音频       |
| `scribe_v2_realtime`  | 低延迟（约150ms）                        | 实时转录、语音代理           |

## 带时间戳的转录

词级时间戳包含类型分类和说话人识别：

```python
result = client.speech_to_text.convert(
    file=audio_file, model_id="scribe_v2", timestamps_granularity="word"
)

for word in result.words:
    print(f"{word.text}: {word.start}s - {word.end}s (type: {word.type})")

```

## 说话人分离

识别谁说了什么——模型为每个词标记说话人 ID，适用于会议、采访或任何多人音频：

```python
result = client.speech_to_text.convert(
    file=audio_file,
    model_id="scribe_v2",
    diarize=True
)

for word in result.words:
    print(f"[{word.speaker_id}] {word.text}")
```

## 关键词提示

帮助模型识别可能误听的特定词汇——产品名称、技术术语或非常规拼写（最多 100 个词）：

```python
result = client.speech_to_text.convert(
    file=audio_file,
    model_id="scribe_v2",
    keyterms=["ElevenLabs", "Scribe", "API"]
)
```

## 语言检测

自动检测，可附带语言提示：

```python
result = client.speech_to_text.convert(
    file=audio_file,
    model_id="scribe_v2",
    language_code="eng"  # ISO 639-1 或 ISO 639-3 代码
)

print(f"Detected: {result.language_code} ({result.language_probability:.0%})")
```

## 支持的格式

**音频：** MP3、WAV、M4A、FLAC、OGG、WebM、AAC、AIFF、Opus
**视频：** MP4、AVI、MKV、MOV、WMV、FLV、WebM、MPEG、3GPP

**限制：** 最大 3GB 文件大小，10 小时时长

## 响应格式

```json
{
  "text": "The full transcription text",
  "language_code": "eng",
  "language_probability": 0.98,
  "words": [
    {"text": "The", "start": 0.0, "end": 0.15, "type": "word", "speaker_id": "speaker_0"},
    {"text": " ", "start": 0.15, "end": 0.16, "type": "spacing", "speaker_id": "speaker_0"}
  ]
}
```

**词类型：**
- `word` - 实际说出的词
- `spacing` - 词之间的空白（用于精确定时）
- `audio_event` - 模型检测到的非语音声音（笑声、掌声、音乐等）

## 错误处理

```python
try:
    result = client.speech_to_text.convert(file=audio_file, model_id="scribe_v2")
except Exception as e:
    print(f"Transcription failed: {e}")
```

常见错误：
- **401**：无效的 API 密钥
- **422**：无效参数
- **429**：超出速率限制

## 跟踪成本

通过 `request-id` 响应头监控使用情况：

```python
response = client.speech_to_text.convert.with_raw_response(file=audio_file, model_id="scribe_v2")
result = response.parse()
print(f"Request ID: {response.headers.get('request-id')}")
```

## 实时流式传输

对于超低延迟（约150ms）的实时转录，请使用实时 API。实时 API 产生两种类型的转录：

- **部分转录 (Partial transcripts)**：处理音频时频繁更新的中间结果——用于实时反馈（如用户说话时显示文本）
- **已提交转录 (Committed transcripts)**：提交后的最终稳定结果——用作应用程序的真实数据源

"提交"告诉模型最终确定当前片段。您可以手动提交（例如用户暂停时）或使用语音活动检测 (VAD) 在静音时自动提交。

### Python（服务器端）

```python
import asyncio
from elevenlabs import ElevenLabs

client = ElevenLabs()

async def transcribe_realtime():
    async with client.speech_to_text.realtime.connect(
        model_id="scribe_v2_realtime",
        include_timestamps=True,
    ) as connection:
        await connection.stream_url("https://example.com/audio.mp3")

        async for event in connection:
            if event.type == "partial_transcript":
                print(f"Partial: {event.text}")
            elif event.type == "committed_transcript":
                print(f"Final: {event.text}")

asyncio.run(transcribe_realtime())
```

### JavaScript（客户端，使用 React）

```typescript
import { useScribe, CommitStrategy } from "@elevenlabs/react";

function TranscriptionComponent() {
  const [transcript, setTranscript] = useState("");

  const scribe = useScribe({
    modelId: "scribe_v2_realtime",
    commitStrategy: CommitStrategy.VAD, // 麦克风输入时在静音处自动提交
    onPartialTranscript: (data) => console.log("Partial:", data.text),
    onCommittedTranscript: (data) => setTranscript((prev) => prev + data.text),
  });

  const start = async () => {
    // 从后端获取令牌（切勿将 API 密钥暴露给客户端）
    const { token } = await fetch("/scribe-token").then((r) => r.json());

    await scribe.connect({
      token,
      microphone: { echoCancellation: true, noiseSuppression: true },
    });
  };

  return <button onClick={start}>Start Recording</button>;
}
```

### 提交策略

| 策略    | 描述                                               |
|---------|----------------------------------------------------|
| **手动** | 您在准备好时调用 `commit()`——用于文件处理或控制音频片段时 |
| **VAD** | 语音活动检测在检测到静音时自动提交——用于实时麦克风输入 |

```typescript
// React：在 hook 上设置 commitStrategy（推荐用于麦克风输入）
import { useScribe, CommitStrategy } from "@elevenlabs/react";

const scribe = useScribe({
  modelId: "scribe_v2_realtime",
  commitStrategy: CommitStrategy.VAD,
  // 可选的 VAD 调优：
  vadSilenceThresholdSecs: 1.5,
  vadThreshold: 0.4,
});
```

```javascript
// JavaScript 客户端：在 connect 时传递 vad 配置
const connection = await client.speechToText.realtime.connect({
  modelId: "scribe_v2_realtime",
  vad: {
    silenceThresholdSecs: 1.5,
    threshold: 0.4,
  },
});
```

### 事件类型

| 事件                                  | 描述               |
|---------------------------------------|--------------------|
| `partial_transcript`                  | 实时中间结果       |
| `committed_transcript`                | 提交后的最终结果   |
| `committed_transcript_with_timestamps`| 带词级时间的最终结果 |
| `error`                               | 发生错误           |

完整文档请参阅实时参考。

## 参考文档

- [安装指南](references/installation.md)
- [转录选项](references/transcription-options.md)
- [实时客户端流式传输](references/realtime-client-side.md)
- [实时服务器端流式传输](references/realtime-server-side.md)
- [提交策略](references/realtime-commit-strategies.md)
- [实时事件参考](references/realtime-events.md)
