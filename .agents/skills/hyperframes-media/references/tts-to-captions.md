# TTS → 字幕

当没有录制的配音时，生成一个并获取词语级字幕时间。根据使用的 TTS 提供商不同，有两种路径：

## 路径 A — HeyGen（单次调用，无需 Whisper）

HeyGen 在与音频相同的响应中返回词语时间戳。传递 `--words` 即可完成：

```bash
npx hyperframes tts script.txt --provider heygen --output narration.wav --words narration.words.json
```

`narration.words.json` 已经是字幕流水线消费的 `[{ id, text, start, end }]` 格式——无需单独的转写步骤。

## 路径 B — ElevenLabs / Kokoro（TTS → Whisper）

这些提供商不返回词语数据。先生成音频，然后转写：

```bash
npx hyperframes tts script.txt --voice af_heart --output narration.wav
npx hyperframes transcribe narration.wav --model small.en   # 语音 af_heart 是美式英语
```

Whisper 从生成的音频中提取精确的词语边界，因此字幕时序与朗读匹配，无需手动调整。将 `--model` 与语音的语言匹配（对于 `a`/`b` 前缀使用 `small.en`，否则使用 `small --language <code>`）。然后通过 `captions/` 中的字幕参考资料消费 `transcript.json`。
