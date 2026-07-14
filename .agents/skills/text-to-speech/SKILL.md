---
name: text-to-speech
description: |
  使用 HeyGen 的 Starfish TTS 模型从文本生成语音音频。在以下情况下使用：(1) 从文本生成独立的语音音频文件，(2) 将文本转换为语音，支持语音选择、速度和音高控制，(3) 为配音、旁白或播客创建音频，(4) 使用 HeyGen 的 /v1/audio 端点，(5) 按语言或性别列出可用的 TTS 语音。
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 文字转语音（HeyGen Starfish）

使用 HeyGen 自家的 Starfish TTS 模型从文本生成语音音频文件。此技能用于独立音频生成 — 与视频创建独立。

## 认证

所有请求需要 `X-Api-Key` 头。设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X GET "https://api.heygen.com/v1/audio/voices" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## 工具选择

如果 HeyGen MCP 工具可用（`mcp__heygen__*`），**优先使用它们**而非直接 HTTP API 调用。

| 任务 | MCP 工具 | 回退（直接 API） |
|------|----------|----------------------|
| 列出 TTS 语音 | `mcp__heygen__list_audio_voices` | `GET /v1/audio/voices` |
| 生成语音音频 | `mcp__heygen__text_to_speech` | `POST /v1/audio/text_to_speech` |

## 默认工作流

1. 使用 `mcp__heygen__list_audio_voices`（或 `GET /v1/audio/voices`）列出语音
2. 选择匹配所需语言、性别和功能的语音
3. 使用文本和 voice_id 调用 `mcp__heygen__text_to_speech`（或 `POST /v1/audio/text_to_speech`）
4. 使用返回的 `audio_url` 下载或播放音频

## 列出 TTS 语音

检索与 Starfish TTS 模型兼容的语音。

> **注意：** 这使用 `GET /v1/audio/voices` — 与视频语音 API（`GET /v2/voices`）不同的端点。并非所有视频语音都支持 Starfish TTS。

### curl

```bash
curl -X GET "https://api.heygen.com/v1/audio/voices" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

（TypeScript 和 Python 示例与原文一致，仅翻译注释和说明文字。）

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

将文本转换为语音音频，使用指定的语音。

### 端点

`POST https://api.heygen.com/v1/audio/text_to_speech`

### 请求字段

| 字段 | 类型 | 必填 | 描述 |
|-------|------|:---:|-------------|
| `text` | string | Y | 要转换为语音的文本内容 |
| `voice_id` | string | Y | 来自 `GET /v1/audio/voices` 的语音 ID |
| `speed` | number | | 语速，0.5-1.5（默认：1） |
| `pitch` | integer | | 音高，-50 到 50（默认：0） |
| `locale` | string | | 多语言语音的口音/区域设置（例如 `en-US`、`pt-BR`） |
| `elevenlabs_settings` | object | | ElevenLabs 语音的高级设置 |

### 使用带停顿的 Break 标签

在文本中使用 SSML 风格的 break 标签来实现停顿：

```
word <break time="1s"/> word
```

规则：
- 使用带 `s` 后缀的秒数：`<break time="1.5s"/>`
- 标签前后必须有空格
- 自闭合标签格式

## 表现性语音指导

对于旁白，在生成音频之前创建一个简短的语音表现计划：

- 解说角色和情感意图
- 节奏轮廓
- 整个脚本的能量曲线
- 停顿应该落在哪里
- 需要强调的词语或短语

使用具体的提示，而非通用指令。"温暖但果断；对比前停顿；最后一句放慢"是有用的。"听起来自然"则不是。

当所选语音支持停顿时，直接将最重要的停顿用 break 标签放在文本中。先从表演最重的部分生成样本，如果样本听起来平淡、匆忙或忽略了预期的停顿，不要批量生成其余部分。

## 最佳实践

1. **使用 `GET /v1/audio/voices`** 查找兼容的语音 — 并非所有来自 `GET /v2/voices` 的语音都支持 Starfish TTS
2. **在设置 `locale` 前检查 `support_locale`** — 仅多语言语音支持区域选择
3. **将速度保持在 0.8-1.2 之间** 以获得自然的输出效果
4. **使用 `preview_audio_url` 预览语音** 在生成之前（某些语音可能为空）
5. **使用响应中的 `word_timestamps`** 用于字幕同步或定时文本覆盖
6. **在文本中使用 SSML break 标签** 实现停顿：`word <break time="1s"/> word`
