# 服务器端实时流式传输

在服务器上实时转录音频流，延迟极低。

## 安装

```bash
# Python
pip install elevenlabs python-dotenv pydub

# JavaScript
npm install @elevenlabs/elevenlabs-js dotenv
```

> **警告：** 不要使用 `npm install elevenlabs`——那是过时的 v1.x 包。始终使用 `@elevenlabs/elevenlabs-js`。

## 配置

将您的 API 密钥存储在 `.env` 文件中：

```
ELEVENLABS_API_KEY=<your_api_key_here>
```

## 从 URL 流式传输

### Python

```python
from dotenv import load_dotenv
import os
import asyncio
from elevenlabs import ElevenLabs
from elevenlabs import RealtimeEvents, RealtimeUrlOptions

load_dotenv()

async def main():
    elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    stop_event = asyncio.Event()

    connection = await elevenlabs.speech_to_text.realtime.connect(RealtimeUrlOptions(
        model_id="scribe_v2_realtime",
        url="https://npr-ice.streamguys1.com/live.mp3",
        include_timestamps=True,
    ))

    def on_partial_transcript(data):
        print(f"Partial: {data.get('text', '')}")

    def on_committed_transcript(data):
        print(f"Committed: {data.get('text', '')}")

    def on_error(error):
        print(f"Error: {error}")
        stop_event.set()

    def on_close():
        print("Connection closed")

    connection.on(RealtimeEvents.PARTIAL_TRANSCRIPT, on_partial_transcript)
    connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT, on_committed_transcript)
    connection.on(RealtimeEvents.ERROR, on_error)
    connection.on(RealtimeEvents.CLOSE, on_close)

    try:
        await stop_event.wait()
    except KeyboardInterrupt:
        print("\nStopping transcription...")
    finally:
        await connection.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript

```javascript
import "dotenv/config";
import { ElevenLabsClient, RealtimeEvents } from "@elevenlabs/elevenlabs-js";

const elevenlabs = new ElevenLabsClient();

const connection = await elevenlabs.speechToText.realtime.connect({
  modelId: "scribe_v2_realtime",
  url: "https://npr-ice.streamguys1.com/live.mp3",
  includeTimestamps: true,
});

connection.on(RealtimeEvents.PARTIAL_TRANSCRIPT, (transcript) => {
  console.log("Partial transcript", transcript);
});

connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT, (transcript) => {
  console.log("Committed transcript", transcript);
});

connection.on(RealtimeEvents.ERROR, (error) => {
  console.log("Error", error);
});

connection.on(RealtimeEvents.CLOSE, () => {
  console.log("Connection closed");
});
```

## 手动音频分块

对于本地文件或自定义音频流，转换为 PCM 格式并分块发送。

### Python

```python
import asyncio
import base64
import os
from dotenv import load_dotenv
from pathlib import Path
from elevenlabs import ElevenLabs
from elevenlabs import AudioFormat, CommitStrategy, RealtimeEvents, RealtimeAudioOptions
from pydub import AudioSegment

load_dotenv()

def load_and_convert_audio(audio_path: str | Path, target_sample_rate: int = 16000) -> bytes:
    if str(audio_path).lower().endswith('.pcm'):
        with open(audio_path, 'rb') as f:
            return f.read()

    audio = AudioSegment.from_file(audio_path)
    if audio.channels > 1:
        audio = audio.set_channels(1)
    if audio.frame_rate != target_sample_rate:
        audio = audio.set_frame_rate(target_sample_rate)
    audio = audio.set_sample_width(2)
    return audio.raw_data

async def main():
    elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    transcription_complete = asyncio.Event()

    connection = await elevenlabs.speech_to_text.realtime.connect(RealtimeAudioOptions(
        model_id="scribe_v2_realtime",
        audio_format=AudioFormat.PCM_16000,
        sample_rate=16000,
        commit_strategy=CommitStrategy.MANUAL,
        include_timestamps=True,
    ))

    def on_session_started(data):
        print(f"Session started: {data}")
        asyncio.create_task(send_audio())

    def on_partial_transcript(data):
        transcript = data.get('text', '')
        if transcript:
            print(f"Partial: {transcript}")

    def on_committed_transcript(data):
        transcript = data.get('text', '')
        print(f"\nCommitted transcript: {transcript}")

    def on_committed_transcript_with_timestamps(data):
        print(f"Timestamps: {data.get('words', '')}")
        transcription_complete.set()

    def on_error(error):
        print(f"Error: {error}")
        transcription_complete.set()

    def on_close():
        print("Connection closed")
        transcription_complete.set()

    connection.on(RealtimeEvents.SESSION_STARTED, on_session_started)
    connection.on(RealtimeEvents.PARTIAL_TRANSCRIPT, on_partial_transcript)
    connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT, on_committed_transcript)
    connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT_WITH_TIMESTAMPS, on_committed_transcript_with_timestamps)
    connection.on(RealtimeEvents.ERROR, on_error)
    connection.on(RealtimeEvents.CLOSE, on_close)

    async def send_audio():
        audio_file_path = Path("audio.mp3")
        audio_data = load_and_convert_audio(audio_file_path)
        chunk_size = 32000  # 16kHz 下 1 秒音频
        chunks = [audio_data[i:i + chunk_size] for i in range(0, len(audio_data), chunk_size)]

        for i, chunk in enumerate(chunks):
            chunk_base64 = base64.b64encode(chunk).decode('utf-8')
            await connection.send({"audio_base_64": chunk_base64, "sample_rate": 16000})

            if i < len(chunks) - 1:
                await asyncio.sleep(1)

        await asyncio.sleep(0.5)
        await connection.commit()

    try:
        await transcription_complete.wait()
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await connection.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript

```javascript
import "dotenv/config";
import * as fs from "node:fs";
import { ElevenLabsClient, RealtimeEvents, AudioFormat } from "@elevenlabs/elevenlabs-js";

const elevenlabs = new ElevenLabsClient();

const connection = await elevenlabs.speechToText.realtime.connect({
  modelId: "scribe_v2_realtime",
  audioFormat: AudioFormat.PCM_16000,
  sampleRate: 16000,
  includeTimestamps: true,
});

connection.on(RealtimeEvents.SESSION_STARTED, (data) => {
  console.log("Session started", data);
  sendAudio();
});

connection.on(RealtimeEvents.PARTIAL_TRANSCRIPT, (transcript) => {
  console.log("Partial transcript", transcript);
});

connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT, (transcript) => {
  console.log("Committed transcript", transcript);
});

connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT_WITH_TIMESTAMPS, (transcript) => {
  console.log("Committed with timestamps", transcript);
});

connection.on(RealtimeEvents.ERROR, (error) => {
  console.log("Error", error);
});

connection.on(RealtimeEvents.CLOSE, () => {
  console.log("Connection closed");
});

async function sendAudio() {
  const pcmFilePath = "audio.pcm";
  const chunkSize = 32000;
  const audioBuffer = fs.readFileSync(pcmFilePath);
  const chunks: Buffer[] = [];

  for (let i = 0; i < audioBuffer.length; i += chunkSize) {
    const chunk = audioBuffer.subarray(i, i + chunkSize);
    chunks.push(chunk);
  }

  for (let i = 0; i < chunks.length; i++) {
    const chunk = chunks[i];
    const chunkBase64 = chunk.toString("base64");

    connection.send({
      audioBase64: chunkBase64,
      sampleRate: 16000,
    });

    if (i < chunks.length - 1) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  }

  await new Promise((resolve) => setTimeout(resolve, 500));
  connection.commit();
}
```

## 直接 WebSocket 连接

用于无法使用 SDK 的情况：

```
wss://api.elevenlabs.io/v1/speech-to-text/realtime?model_id=scribe_v2_realtime
```

### 消息格式

```json
{
  "message_type": "input_audio_chunk",
  "audio_base_64": "<base64-encoded-audio>",
  "commit": false,
  "sample_rate": 16000
}
```

### 提交消息

```json
{
  "message_type": "commit"
}
```

## 音频要求

| 参数        | 值                     |
|-------------|------------------------|
| 格式        | PCM 16 位              |
| 采样率      | 16000 Hz（推荐）       |
| 声道        | 单声道                 |
| 块大小      | 32,000 字节 = 1 秒     |

支持的采样率：8kHz 到 48kHz
