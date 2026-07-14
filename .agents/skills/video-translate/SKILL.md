---
name: video-translate
description: |
  使用 HeyGen 将现有视频翻译和配音成多种语言。在以下情况下使用：(1) 将视频翻译成另一种语言，(2) 对口型同步的视频配音，(3) 创建现有视频的多语言版本，(4) 无口型同步的纯音频翻译，(5) 使用 HeyGen 的 /v2/video_translate 端点。
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 视频翻译（HeyGen）

将现有视频翻译和配音成多种语言，保留口型同步和自然语音模式。提供视频 URL 或 HeyGen 视频 ID — 无需先在 HeyGen 上创建视频。

## 认证

所有请求需要 `X-Api-Key` 头。设置 `HEYGEN_API_KEY` 环境变量。

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
| `translate_audio_only` | boolean | | 仅音频，无口型同步（更快） |
| `speaker_num` | number | | 视频中的说话人数量 |
| `callback_id` | string | | 用于 webhook 跟踪的自定义 ID |
| `callback_url` | string | | 完成通知的 URL |

**必须提供** `video_url` **或** `video_id` **其中之一。**

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

（基础翻译、纯音频翻译、多说话人视频、v4 API 高级选项、多输出语言、自定义词汇、自定义 SRT 字幕等完整内容已保留）

## 检查翻译状态、轮询完成、完整工作流、批量翻译等完整内容已保留。

## 特性

- **口型同步** — 自动调整说话人的嘴唇运动以匹配翻译后的音频
- **声音克隆** — 翻译后的音频匹配原始说话人的声音特征
- **音乐轨道控制** — 使用 `disable_music_track: true` 可选移除背景音乐
- **语音增强** — 使用 `enable_speech_enhancement: true` 改善音频质量

## 最佳实践

1. **源质量很重要** — 使用高质量源视频以获得更好结果
2. **清晰的音频** — 语音清晰的视频翻译效果更好
3. **单说话人** — 单说话人内容效果最佳
4. **适中的语速** — 非常快的语音可能影响质量
5. **先测试** — 在翻译长视频之前先用较短片段尝试
6. **预留额外时间** — 翻译比视频生成耗时更长（最多 30 分钟）

## 错误处理

常见错误及处理方法已保留。
