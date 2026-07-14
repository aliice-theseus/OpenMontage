# 转录

创建归一化的词语级时间戳。**始终显式指定 `--model`**——CLI 默认是 `small.en`，它会静默将非英语音频翻译为英语。

```bash
npx hyperframes transcribe audio.mp3  --model small.en             # 已知为英语
npx hyperframes transcribe video.mp4  --model small --language es  # 已知为西班牙语
npx hyperframes transcribe audio.mp3  --model small                # 未知语言（自动检测）
npx hyperframes transcribe subtitles.srt                           # 导入现有字幕
npx hyperframes transcribe subtitles.vtt
npx hyperframes transcribe openai-response.json
```

## 语言规则（不可协商）

`.en` 模型（`tiny.en` / `base.en` / `small.en` / `medium.en`）会将非英语音频**翻译**为英语。这会静默破坏原始语言。

1. **已知为英语** → `--model small.en`（或音乐/嘈杂音频使用 `medium.en`）
2. **已知为非英语** → `--model small --language <iso-code>`（不带 `.en` 后缀）
3. **未知语言** → `--model small`（whisper 自动检测）

**CLI 默认是 `small.en`**——不要依赖它；始终传递 `--model` 以明确选择。`--language` 还会从混合语言音频中过滤掉非目标语言片段。

## 模型大小

| 模型 | 大小 | 速度 | 使用场景 |
| ---------- | ------ | -------- | ------------------------------------- |
| `tiny` | 75 MB | 最快 | 快速预览、冒烟测试 |
| `base` | 142 MB | 快 | 短片、清晰的音频 |
| `small` | 466 MB | 中等 | 大多数多语言内容的默认选择 |
| `medium` | 1.5 GB | 慢 | 带人声的音乐、嘈杂音频 |
| `large-v3` | 3.1 GB | 最慢 | 生产质量 |

### 按内容类型选择模型

1. 静音/轻背景上的语音 → `small.en`
2. 音乐上的语音，或带人声的音乐 → 从 `medium.en` 开始
3. 制作好的音乐曲目（人声 + 完整伴奏）→ 从 `medium.en` 开始；可能需要手动歌词或外部 API（[`captions/transcript-handling.md`](captions/transcript-handling.md) →「使用外部转录 API」）
4. 多语言 → `medium` 或 `large-v3`（不带 `.en` 后缀），配合 `--language`

## 输出格式

作品消费一个扁平的词语对象数组。`id`（`w0`、`w1`……）在归一化过程中添加，用于字幕覆盖的稳定引用；向后兼容时可省略。

```json
[
  { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 },
  { "id": "w1", "text": "world.", "start": 0.6, "end": 1.2 }
]
```

关于强制性的字幕质量检查、重试规则以及 OpenAI/Groq Whisper API 导入路径，请参见 `captions/transcript-handling.md`。
