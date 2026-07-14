---
name: text-to-speech
description: |
  使用 HeyGen 的 Starfish TTS 模型从文本生成语音音频。在以下情况下使用：(1) 从文本生成独立的语音音频文件，(2) 将文本转换为语音，支持声音选择、速度和音调控制，(3) 为配音、旁白或播客创建音频，(4) 使用 HeyGen 的 /v1/audio 端点，(5) 按语言或性别列出可用的 TTS 声音。
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 文本转语音（HeyGen Starfish）

使用 HeyGen 自研的 Starfish TTS 模型从文本生成语音音频文件。本技能用于独立音频生成 — 与视频创作分开。

## 认证

所有请求都需要 `X-Api-Key` 头。设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X GET "https://api.heygen.com/v1/audio/voices" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## 工具选择

如果 HeyGen MCP 工具可用（`mcp__heygen__*`），**优先使用它们**而非直接 HTTP API 调用。

| 任务 | MCP 工具 | 回退（直接 API） |
|------|----------|----------------------|
| 列出 TTS 声音 | `mcp__heygen__list_audio_voices` | `GET /v1/audio/voices` |
| 生成语音音频 | `mcp__heygen__text_to_speech` | `POST /v1/audio/text_to_speech` |

## 默认工作流

1. 使用 `mcp__heygen__list_audio_voices`（或 `GET /v1/audio/voices`）列出声音
2. 选择匹配所需语言、性别和功能的声音
3. 使用文本和 voice_id 调用 `mcp__heygen__text_to_speech`（或 `POST /v1/audio/text_to_speech`）
4. 使用返回的 `audio_url` 下载或播放音频

## 列出 TTS 声音

检索与 Starfish TTS 模型兼容的声音。

> **注意：** 这使用 `GET /v1/audio/voices` — 与视频声音 API（`GET /v2/voices`）不同的端点。并非所有视频声音都支持 Starfish TTS。

### curl

```bash
curl -X GET "https://api.heygen.com/v1/audio/voices" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface TTSVoice {
  voice_id: string;
  language: string;
  gender: "female" | "male" | "unknown";
  name: string;
  preview_audio_url: string | null;
  support_pause: boolean;
  support_locale: boolean;
  type: string;
}

interface TTSVoicesResponse {
  error: null | string;
  data: {
    voices: TTSVoice[];
  };
}

async function listTTSVoices(): Promise<TTSVoice[]> {
  const response = await fetch("https://api.heygen.com/v1/audio/voices", {
    headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
  });

  const json: TTSVoicesResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.voices;
}
```

### Python

```python
import requests
import os

def list_tts_voices() -> list:
    response = requests.get(
        "https://api.heygen.com/v1/audio/voices",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["voices"]
```

### 响应格式

```json
{
  "error": null,
  "data": {
    "voices": [
      {
        "voice_id": "f38a635bee7a4d1f9b0a654a31d050d2",
        "name": "Chill Brian",
        "language": "English",
        "gender": "male",
        "preview_audio_url": "https://resource.heygen.ai/text_to_speech/WpSDQvmLGXEqXZVZQiVeg6.mp3",
        "support_pause": true,
        "support_locale": false,
        "type": "public"
      }
    ]
  }
}
```

## 生成语音音频

使用指定的声音将文本转换为语音音频。

### 端点

`POST https://api.heygen.com/v1/audio/text_to_speech`

### 请求字段

| 字段 | 类型 | 必填 | 描述 |
|-------|------|:---:|-------------|
| `text` | string | Y | 要转换为语音的文本内容 |
| `voice_id` | string | Y | 来自 `GET /v1/audio/voices` 的声音 ID |
| `speed` | number | | 语速，0.5-1.5（默认：1） |
| `pitch` | integer | | 音调，-50 到 50（默认：0） |
| `locale` | string | | 多语言声音的口音/区域设置（例如 `en-US`、`pt-BR`） |
| `elevenlabs_settings` | object | | ElevenLabs 声音的高级设置 |

### ElevenLabs 设置（可选）

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `model` | string | 模型选择（`eleven_v3`、`eleven_turbo_v2_5` 等） |
| `similarity_boost` | number | 声音相似度，0.0-1.0 |
| `stability` | number | 输出一致性，0.0-1.0 |
| `style` | number | 风格强度，0.0-1.0 |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/audio/text_to_speech" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello! Welcome to our product demo.",
    "voice_id": "YOUR_VOICE_ID",
    "speed": 1.0
  }'
```

### TypeScript

```typescript
interface TTSRequest {
  text: string;
  voice_id: string;
  speed?: number;
  pitch?: number;
  locale?: string;
  elevenlabs_settings?: {
    model?: string;
    similarity_boost?: number;
    stability?: number;
    style?: number;
  };
}

interface WordTimestamp {
  word: string;
  start: number;
  end: number;
}

interface TTSResponse {
  error: null | string;
  data: {
    audio_url: string;
    duration: number;
    request_id: string;
    word_timestamps: WordTimestamp[];
  };
}

async function textToSpeech(request: TTSRequest): Promise<TTSResponse["data"]> {
  const response = await fetch(
    "https://api.heygen.com/v1/audio/text_to_speech",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  const json: TTSResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data;
}
```

### Python

```python
import requests
import os

def text_to_speech(
    text: str,
    voice_id: str,
    speed: float = 1.0,
    pitch: int = 0,
    locale: str | None = None,
) -> dict:
    payload = {
        "text": text,
        "voice_id": voice_id,
        "speed": speed,
        "pitch": pitch,
    }

    if locale:
        payload["locale"] = locale

    response = requests.post(
        "https://api.heygen.com/v1/audio/text_to_speech",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json=payload,
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]
```

### 响应格式

```json
{
  "error": null,
  "data": {
    "audio_url": "https://resource2.heygen.ai/text_to_speech/.../id=365d46bb.wav",
    "duration": 5.526,
    "request_id": "p38QJ52hfgNlsYKZZmd9",
    "word_timestamps": [
      { "word": "<start>", "start": 0.0, "end": 0.0 },
      { "word": "Hey", "start": 0.079, "end": 0.219 },
      { "word": "there,", "start": 0.239, "end": 0.459 },
      { "word": "<end>", "start": 5.526, "end": 5.526 }
    ]
  }
}
```

## 使用示例

### 基础 TTS

```typescript
const result = await textToSpeech({
  text: "Welcome to our quarterly earnings call.",
  voice_id: "YOUR_VOICE_ID",
});

console.log(`音频 URL: ${result.audio_url}`);
console.log(`时长: ${result.duration}s`);
```

### 调整速度

```typescript
const result = await textToSpeech({
  text: "We're thrilled to announce our newest feature!",
  voice_id: "YOUR_VOICE_ID",
  speed: 1.1,
});
```

### 多语言声音的区域设置

```typescript
const result = await textToSpeech({
  text: "Bem-vindo ao nosso produto.",
  voice_id: "MULTILINGUAL_VOICE_ID",
  locale: "pt-BR",
});
```

### 找到声音并生成音频

```typescript
async function generateSpeech(text: string, language: string): Promise<string> {
  const voices = await listTTSVoices();
  const voice = voices.find(
    (v) => v.language.toLowerCase().includes(language.toLowerCase())
  );

  if (!voice) {
    throw new Error(`未找到语言 ${language} 的 TTS 声音`);
  }

  const result = await textToSpeech({
    text,
    voice_id: voice.voice_id,
  });

  return result.audio_url;
}

const audioUrl = await generateSpeech("Hello and welcome!", "english");
```

## 使用 Break 标签暂停

在文本中使用 SSML 风格的 break 标签来添加暂停：

```
word <break time="1s"/> word
```

规则：
- 使用带 `s` 后缀的秒数：`<break time="1.5s"/>`
- 标签前后必须有空格
- 自闭合标签格式

## 表达性语音指导

对于配音，在生成音频前创建简短的语音表演计划：

- 讲述者角色和情感意图
- 节奏轮廓
- 脚本中的能量曲线
- 暂停应落在哪里
- 需要强调的词语或短语

使用具体提示，而非泛泛指示。"温暖但果断；对比前暂停；最后一句话放慢速度"是有用的。"听起来自然"则不是。

当所选声音支持暂停时，将最重要的暂停直接用 break 标签放在文本中。先从表演最重的部分生成一个样本，如果样本听起来平淡、急促或忽略预期的暂停，则不要批量生成其余部分。

## 最佳实践

1. **使用 `GET /v1/audio/voices`** 查找兼容的声音 — 并非来自 `GET /v2/voices` 的所有声音都支持 Starfish TTS
2. **在设置 `locale` 前检查 `support_locale`** — 只有多语言声音支持区域选择
3. **将速度保持在 0.8-1.2 之间** 以获得自然听感的输出
4. **在生成前使用 `preview_audio_url` 预览声音**（某些声音可能为 null）
5. **使用响应中的 `word_timestamps`** 进行字幕同步或定时文字叠加
6. **在文本中使用 SSML break 标签** 添加暂停：`word <break time="1s"/> word`
