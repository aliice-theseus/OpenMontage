# 转录指南

关于 `transcribe` CLI 调用、`.en` 翻译非英语规则以及 whisper 模型选择，请参见 [`../transcribe.md`](../transcribe.md)。本文档涵盖在制作字幕时如何处理生成的转录结果：输入格式、强制性质量检查、清理代码、外部 API 备选。

## 支持的输入格式

CLI 自动检测并归一化以下格式：

| 格式 | 扩展名 | 来源 | 词语级？ |
| --------------------- | --------- | --------------------------------------------------------------------------- | ----------------- |
| whisper.cpp JSON | `.json` | `hyperframes init --video`、`hyperframes transcribe` | 是 |
| OpenAI Whisper API | `.json` | `openai.audio.transcriptions.create({ timestamp_granularities: ["word"] })` | 是 |
| SRT 字幕 | `.srt` | 视频编辑器、字幕工具、YouTube | 否（短语级） |
| VTT 字幕 | `.vtt` | 网页播放器、YouTube、转录服务 | 否（短语级） |
| 归一化词语数组 | `.json` | 任何工具预处理 | 是 |

**词语级时间戳产生更好的字幕。** SRT/VTT 提供短语级时序，虽然可用但无法实现逐词动画效果。

## 转录质量检查（强制性）

每次转录后，**在继续之前阅读转录结果并检查质量问题。** 糟糕的转录会产生无意义的字幕。切勿跳过此步骤。

### 需要检查的内容

| 信号 | 示例 | 原因 |
| ---------------------------- | -------------------------------------- | ---------------------------------------------------------------------------- |
| 音乐音符标记（`♪`、`�`） | `{ "text": "♪" }` 或 `{ "text": "�" }` | Whisper 检测到音乐，而非语音 |
| 乱码/无意义的词语 | "Do a chin"、"Get so gay"、"huh" | 模型听错歌词或背景噪音 |
| 长时间无词语的间隙 | 只有 `♪` 标记的 20+ 秒片段 | 乐器部分——可预期，但高比例意味着语音被遗漏 |
| 重复的填充词 | 很多 "huh"、"uh"、"oh" 条目 | 模型在音乐上产生幻觉 |
| 非常短的词语跨度 | `end - start < 0.05` 的词语 | 时间戳对齐不可靠 |

### 自动重试规则

**如果超过 20% 的条目是 `♪`/`�` 标记，或者转录结果包含明显的无意义词，转录失败。** 不要使用糟糕的转录继续。而是：

1. **如果原始使用了 `small.en` 或更小的模型，用 `medium.en` 重试：**
   ```bash
   npx hyperframes transcribe audio.mp3 --model medium.en
   ```
2. **如果 `medium.en` 也失败**（仍然 >20% 音乐标记或乱码），告知用户音频噪音太大，本地转录无法处理，并建议：
   - 手动提供 SRT/VTT 格式的歌词
   - 使用外部 API（OpenAI 或 Groq Whisper——见下文）
3. **在构建字幕前务必清理转录结果**——过滤掉 `♪`/`�` 标记以及 `text` 是单个非词语字符的条目。只有真正的词语才能进入字幕作品。

### 清理转录结果

转录后（即使使用好的模型），清除非词语条目：

```js
var raw = JSON.parse(transcriptJson);
var words = raw.filter(function (w) {
  if (!w.text || w.text.trim().length === 0) return false;
  if (/^[♪�\u266a\u266b\u266c\u266d\u266e\u266f]+$/.test(w.text)) return false;
  if (/^(huh|uh|um|ah|oh)$/i.test(w.text) && w.end - w.start < 0.1) return false;
  return true;
});
```

关于按内容类型选择模型的指导，请参见 [`../transcribe.md`](../transcribe.md) →「按内容类型选择模型」。

## 使用外部转录 API

为获得最佳准确性，使用外部 API 并导入结果：

**OpenAI Whisper API**（推荐用于高质量）：

```bash
# 生成带词语时间戳的结果，然后导入
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@audio.mp3 -F model=whisper-1 \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -o transcript-openai.json

npx hyperframes transcribe transcript-openai.json
```

**Groq Whisper API**（快速，提供免费层）：

```bash
curl https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file=@audio.mp3 -F model=whisper-large-v3 \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -o transcript-groq.json

npx hyperframes transcribe transcript-groq.json
```

## 如果没有转录结果

1. 检查项目根目录是否存在 `transcript.json`、`.srt` 或 `.vtt` 文件。
2. 如果没有找到，运行 [`../transcribe.md`](../transcribe.md)——从那里的「按内容类型选择模型」中选择起始模型。
3. 运行上面的质量检查。如果失败，用更大的模型重试或回退到手动歌词/外部 API。
