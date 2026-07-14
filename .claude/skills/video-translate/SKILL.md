---
name: video-translate
description: |
  使用 HeyGen 将现有视频翻译和配音成多种语言。在以下情况下使用：(1) 将视频翻译成另一种语言，(2) 对视频内容进行配音并保持唇形同步，(3) 创建现有视频的多语言版本，(4) 仅音频翻译，无需唇形同步，(5) 使用 HeyGen 的 /v2/video_translate 端点。
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 视频翻译（HeyGen）

将现有视频翻译和配音成多种语言，保持唇形同步和自然的语音模式。提供视频 URL 或 HeyGen 视频 ID — 无需先在 HeyGen 上创建视频。

## 认证

所有请求都需要 `X-Api-Key` 头。设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X POST "https://api.heygen.com/v2/video_translate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://example.com/video.mp4", "output_language": "es-ES"}'
```

## 默认工作流

1. 提供视频 URL 或 HeyGen 视频 ID
2. 使用目标语言调用 `POST /v2/video_translate`
3. 轮询 `GET /v2/video_translate/{translate_id}` 直到状态为 `completed`
4. 从返回的 URL 下载翻译后的视频

## 创建翻译任务

### 请求字段

| 字段 | 类型 | 必填 | 描述 |
|-------|------|:---:|-------------|
| `video_url` | string | Y* | 要翻译的视频 URL（*或 `video_id`） |
| `video_id` | string | Y* | HeyGen 视频 ID（*或 `video_url`） |
| `output_language` | string | Y | 目标语言代码（例如 `"es-ES"`） |
| `title` | string | | 翻译视频的名称 |
| `translate_audio_only` | boolean | | 仅音频，无需唇形同步（更快） |
| `speaker_num` | number | | 视频中说话者数量 |
| `callback_id` | string | | 用于 webhook 跟踪的自定义 ID |
| `callback_url` | string | | 完成通知的 URL |

**必须提供 `video_url` 或 `video_id` 其中之一。**

### curl

```bash
curl -X POST "https://api.heygen.com/v2/video_translate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://example.com/original-video.mp4",
    "output_language": "es-ES",
    "title": "西班牙语版本"
  }'
```

### TypeScript

```typescript
interface VideoTranslateRequest {
  video_url?: string;
  video_id?: string;
  output_language: string;
  title?: string;
  translate_audio_only?: boolean;
  speaker_num?: number;
  callback_id?: string;
  callback_url?: string;
}

interface VideoTranslateResponse {
  error: null | string;
  data: {
    video_translate_id: string;
  };
}

async function translateVideo(config: VideoTranslateRequest): Promise<string> {
  const response = await fetch("https://api.heygen.com/v2/video_translate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });

  const json: VideoTranslateResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.video_translate_id;
}
```

### Python

```python
import requests
import os

def translate_video(config: dict) -> str:
    response = requests.post(
        "https://api.heygen.com/v2/video_translate",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json"
        },
        json=config
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["video_translate_id"]
```

## 支持的语言

| 语言 | 代码 | 备注 |
|----------|------|-------|
| 英语（美国） | en-US | 默认源语言 |
| 西班牙语（西班牙） | es-ES | 欧洲西班牙语 |
| 西班牙语（墨西哥） | es-MX | 拉丁美洲 |
| 法语 | fr-FR | 标准法语 |
| 德语 | de-DE | 标准德语 |
| 意大利语 | it-IT | 标准意大利语 |
| 葡萄牙语（巴西） | pt-BR | 巴西葡萄牙语 |
| 日语 | ja-JP | 标准日语 |
| 韩语 | ko-KR | 标准韩语 |
| 中文（普通话） | zh-CN | 简体中文 |
| 印地语 | hi-IN | 标准印地语 |
| 阿拉伯语 | ar-SA | 现代标准阿拉伯语 |

## 翻译选项

### 基本翻译（带唇形同步）

```typescript
const config = {
  video_url: "https://example.com/original.mp4",
  output_language: "es-ES",
  title: "西班牙语翻译",
};
```

### 仅音频翻译（更快，无唇形同步）

```typescript
const config = {
  video_url: "https://example.com/original.mp4",
  output_language: "es-ES",
  translate_audio_only: true,
};
```

### 多说话者视频

```typescript
const config = {
  video_url: "https://example.com/interview.mp4",
  output_language: "fr-FR",
  speaker_num: 2,
};
```

## 高级选项（v4 API）

如需对翻译进行更多控制：

```typescript
interface VideoTranslateV4Request {
  input_video_id?: string;
  google_url?: string;
  output_languages: string[];        // 单次调用多种语言
  name: string;
  srt_key?: string;                  // 自定义 SRT 字幕
  instruction?: string;
  vocabulary?: string[];             // 按原样保留的术语
  brand_voice_id?: string;
  speaker_num?: number;
  keep_the_same_format?: boolean;
  input_language?: string;
  enable_video_stretching?: boolean;
  disable_music_track?: boolean;
  enable_speech_enhancement?: boolean;
  srt_role?: "input" | "output";
  translate_audio_only?: boolean;
}
```

### 多种输出语言

```typescript
const config = {
  input_video_id: "original_video_id",
  output_languages: ["es-ES", "fr-FR", "de-DE"],
  name: "多语言翻译",
};
```

### 自定义词汇表（保留特定术语）

```typescript
const config = {
  video_url: "https://example.com/product-demo.mp4",
  output_language: "ja-JP",
  vocabulary: ["SuperWidget", "Pro Max", "TechCorp"],
};
```

### 自定义 SRT 字幕

```typescript
const config = {
  video_url: "https://example.com/video.mp4",
  output_language: "es-ES",
  srt_key: "path/to/custom-subtitles.srt",
  srt_role: "input",
};
```

## 检查翻译状态

### curl

```bash
curl -X GET "https://api.heygen.com/v2/video_translate/{translate_id}" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface TranslateStatusResponse {
  error: null | string;
  data: {
    id: string;
    status: "pending" | "processing" | "completed" | "failed";
    video_url?: string;
    message?: string;
  };
}

async function getTranslateStatus(translateId: string): Promise<TranslateStatusResponse["data"]> {
  const response = await fetch(
    `https://api.heygen.com/v2/video_translate/${translateId}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json: TranslateStatusResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data;
}
```

## 轮询完成

翻译比标准视频生成耗时更长 — 最多等待 30 分钟。

```typescript
async function waitForTranslation(
  translateId: string,
  maxWaitMs = 1800000,
  pollIntervalMs = 30000
): Promise<string> {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitMs) {
    const status = await getTranslateStatus(translateId);

    switch (status.status) {
      case "completed":
        return status.video_url!;
      case "failed":
        throw new Error(status.message || "翻译失败");
      default:
        console.log(`状态: ${status.status}...`);
        await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
  }

  throw new Error("翻译超时");
}
```

## 完整工作流

```typescript
async function translateAndDownload(
  videoUrl: string,
  targetLanguage: string
): Promise<string> {
  console.log(`开始翻译到 ${targetLanguage}...`);
  const translateId = await translateVideo({
    video_url: videoUrl,
    output_language: targetLanguage,
  });
  console.log(`翻译 ID: ${translateId}`);

  console.log("正在处理翻译...");
  const translatedVideoUrl = await waitForTranslation(translateId);
  console.log(`翻译完成: ${translatedVideoUrl}`);

  return translatedVideoUrl;
}

const spanishVideo = await translateAndDownload(
  "https://example.com/my-video.mp4",
  "es-ES"
);
```

## 批量翻译

并行翻译成多种语言：

```typescript
async function translateToMultipleLanguages(
  sourceVideoUrl: string,
  targetLanguages: string[]
): Promise<Record<string, string>> {
  const results: Record<string, string> = {};

  const translatePromises = targetLanguages.map(async (lang) => {
    const translateId = await translateVideo({
      video_url: sourceVideoUrl,
      output_language: lang,
    });
    return { lang, translateId };
  });

  const translationJobs = await Promise.all(translatePromises);

  for (const job of translationJobs) {
    try {
      const videoUrl = await waitForTranslation(job.translateId);
      results[job.lang] = videoUrl;
    } catch (error) {
      results[job.lang] = `错误: ${error.message}`;
    }
  }

  return results;
}

const translations = await translateToMultipleLanguages(
  "https://example.com/original.mp4",
  ["es-ES", "fr-FR", "de-DE", "ja-JP"]
);
```

## 功能特点

- **唇形同步** — 自动调整说话者的嘴唇运动以匹配翻译后的音频
- **声音克隆** — 翻译后的音频匹配原始说话者的声音特征
- **音乐轨道控制** — 可选择通过 `disable_music_track: true` 移除背景音乐
- **语音增强** — 通过 `enable_speech_enhancement: true` 提高音频质量

## 最佳实践

1. **源质量很重要** — 使用高质量源视频以获得更好效果
2. **清晰音频** — 语音清晰的视频翻译效果更好
3. **单说话者** — 单说话者内容效果最佳
4. **适中语速** — 非常快速的语音可能影响质量
5. **先测试** — 在翻译长视频前先用较短视频片段尝试
6. **预留额外时间** — 翻译比视频生成耗时更长（最多 30 分钟）

## 错误处理

常见错误及其处理方式：

```typescript
async function safeTranslate(
  videoUrl: string,
  targetLanguage: string
): Promise<{ success: boolean; result?: string; error?: string }> {
  try {
    const url = await translateAndDownload(videoUrl, targetLanguage);
    return { success: true, result: url };
  } catch (error) {
    if (error.message.includes("quota")) {
      return { success: false, error: "积分不足" };
    }
    if (error.message.includes("duration")) {
      return { success: false, error: "视频太长" };
    }
    if (error.message.includes("format")) {
      return { success: false, error: "不支持的视频格式" };
    }
    return { success: false, error: error.message };
  }
}
```
