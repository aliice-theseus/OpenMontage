# 客户端实时流式传输

将音频从浏览器直接传输到 ElevenLabs 进行实时转录。

## 安装

```bash
# React
npm install @elevenlabs/react @elevenlabs/elevenlabs-js

# JavaScript
npm install @elevenlabs/client @elevenlabs/elevenlabs-js
```

> **警告：** 客户端包始终使用 `@elevenlabs/*` 命名空间。

## 令牌生成

客户端流式传输需要使用一次性令牌来保护您的 API 密钥。在后端生成令牌：

```typescript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

const elevenlabs = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY,
});

app.get("/scribe-token", yourAuthMiddleware, async (req, res) => {
  const token = await elevenlabs.tokens.singleUse.create("realtime_scribe");
  res.json(token);
});
```

**注意：** 一次性令牌在 15 分钟后过期。

## React 实现

```typescript
import { useScribe, CommitStrategy } from "@elevenlabs/react";

function TranscriptionComponent() {
  const [transcript, setTranscript] = useState("");

  const scribe = useScribe({
    modelId: "scribe_v2_realtime",
    commitStrategy: CommitStrategy.VAD, // 麦克风输入时静音自动提交
    onPartialTranscript: (data) => {
      // 用户说话时显示实时反馈
      console.log("部分：", data.text);
    },
    onCommittedTranscript: (data) => {
      // 此片段的最终转录
      setTranscript((prev) => prev + data.text);
    },
  });

  const startRecording = async () => {
    const tokenResponse = await fetch("/scribe-token");
    const { token } = await tokenResponse.json();

    await scribe.connect({
      token,
      microphone: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
      },
    });
  };

  const stopRecording = () => {
    scribe.disconnect();
  };

  return (
    <div>
      <div>状态：{scribe.status}</div>
      <button onClick={startRecording}>开始</button>
      <button onClick={stopRecording}>停止</button>
      <p>{transcript}</p>
    </div>
  );
}
```

> **重要：** 默认提交策略是 `CommitStrategy.MANUAL`，需要您显式调用 `scribe.commit()`。对于麦克风输入，始终设置 `CommitStrategy.VAD`，这样服务器在检测到静音时会自动提交。否则，已提交的转录永远不会触发，连接可能会断开。

### `scribe.status` 值

| 状态 | 含义 |
|--------|---------|
| `"disconnected"` | 无活动连接 |
| `"connecting"` | 正在建立连接 |
| `"connected"` | 已连接，准备接收音频 |
| `"transcribing"` | 正在处理语音（检测到音频或 VAD 提交时从 `"connected"` 转换） |
| `"error"` | 发生错误 |

> **重要：** 检查会话是否活跃时，始终检查 `"connected"` 和 `"transcribing"` 两种状态。语音处理期间状态会转换为 `"transcribing"`，因此仅检查 `"connected"` 会导致 UI 元素（按钮、波形、指示器）在会话中间错误重置。

```typescript
// 正确——处理两种活跃状态
const isListening = scribe.status === "connected" || scribe.status === "transcribing";

// 错误——VAD 提交时会闪烁/重置
const isListening = scribe.status === "connected";
```

## JavaScript 实现

```typescript
import { Scribe, RealtimeEvents } from "@elevenlabs/client";

async function startTranscription() {
  const tokenResponse = await fetch("/scribe-token");
  const { token } = await tokenResponse.json();

  const connection = Scribe.connect({
    token,
    modelId: "scribe_v2_realtime",
    includeTimestamps: true,
    microphone: {
      echoCancellation: true,
      noiseSuppression: true,
      autoGainControl: true,
    },
  });

  connection.on(RealtimeEvents.OPEN, () => {
    console.log("已连接");
  });

  connection.on(RealtimeEvents.PARTIAL_TRANSCRIPT, (data) => {
    console.log("部分：", data.text);
  });

  connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT, (data) => {
    console.log("已提交：", data.text);
  });

  connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT_WITH_TIMESTAMPS, (data) => {
    for (const word of data.words) {
      console.log(`${word.text}: ${word.start}s - ${word.end}s`);
    }
  });

  connection.on(RealtimeEvents.ERROR, (error) => {
    console.error("错误：", error);
  });

  connection.on(RealtimeEvents.CLOSE, () => {
    console.log("已断开连接");
  });

  return connection;
}
```

## 手动音频分块

对于文件上传或自定义音频源，编码为 PCM-16 并按块发送：

```typescript
const chunkSize = 4096;

for (let offset = 0; offset < pcmData.length; offset += chunkSize) {
  const chunk = pcmData.slice(offset, offset + chunkSize);
  const bytes = new Uint8Array(chunk.buffer);
  const base64 = btoa(String.fromCharCode(...bytes));

  scribe.sendAudio(base64);

  // 模拟实时流式传输
  await new Promise((resolve) => setTimeout(resolve, 50));
}

// 完成转录
scribe.commit();
```

## 麦克风选项

| 选项 | 描述 |
|--------|-------------|
| `echoCancellation` | 消除扬声器回声 |
| `noiseSuppression` | 过滤背景噪音 |
| `autoGainControl` | 标准化音量级别 |

## 安全

- 切勿将 API 密钥暴露给客户端
- 始终在后端生成一次性令牌
- 使用认证中间件保护令牌端点
