---
name: doubao-tts
description: 使用火山引擎豆包语音合成 2.0（Doubao Speech 2.0）生成普通话和多语言旁白。在创建中文配音时、用户偏好豆包/火山引擎 TTS 时、或旁白需要字符级时间戳元数据用于字幕时使用。
---

# 豆包 TTS

需要在 `.env` 中设置 `DOUBAO_SPEECH_API_KEY`。
设置 `DOUBAO_SPEECH_VOICE_TYPE` 作为默认语音，或向工具传递 `voice_id`。

## 当前 API

使用新控制台 API Key 流程：

```text
X-Api-Key: ${DOUBAO_SPEECH_API_KEY}
X-Api-Resource-Id: seed-tts-2.0
```

不要在新控制台 API Key 中使用 `X-Api-App-Id` 和 `X-Api-Access-Key`。如果 API 返回 `load grant: requested grant not found`，可能是密钥类型或认证头错误。

对于长篇视频旁白，优先使用异步端点：

```text
POST https://openspeech.bytedance.com/api/v3/tts/submit
POST https://openspeech.bytedance.com/api/v3/tts/query
```

这会返回 `audio_url` 以及可用于构建字幕的 `sentences[].words[]` 时间元数据。

## OpenMontage 用法

使用 TTS 选择器生成：

```python
from tools.audio.tts_selector import TTSSelector

result = TTSSelector().execute({
    "preferred_provider": "doubao",
    "text": "如果 AI 真的会改变未来，普通人到底该怎么参与？",
    "voice_id": "zh_female_vv_uranus_bigtts",
    "output_path": "projects/my-video/assets/audio/narration.mp3",
    "speech_rate": 0,
    "enable_timestamp": True,
})
```

或直接调用提供商：

```python
from tools.audio.doubao_tts import DoubaoTTS

result = DoubaoTTS().execute({
    "text": "短样本试听文本。",
    "voice_id": "zh_female_vv_uranus_bigtts",
    "output_path": "projects/my-video/assets/audio/doubao_sample.mp3",
})
```

提供商会写入：

- `output_path`：下载的音频文件
- `metadata_path`：完整查询响应 JSON，默认为 `<output_path>.json`

## 推荐工作流

1. 在完整付费旁白前，先生成一个 10-15 秒的样本。
2. 询问用户认可语音的自然度、口音和速度。
3. 仅在获得认可后生成完整旁白。
4. 保留查询 JSON。它是字幕时间的权威来源。
5. 从 `sentences[].words[]` 构建字幕，而不是从估计的文本长度。
6. 在应用时间戳前，按中文语义短语对字幕进行分组。不要仅按固定字符数分割；它会破坏诸如"在不押单个公司的情况下"或"可能会被慢慢稀释"这样的短语，影响理解。
7. 让视频时长跟随认可后的语音节奏，除非用户明确要求匹配先前的运行时长度。

## 参数

- `voice_id`：豆包 `speaker` / 语音类型。默认为 `DOUBAO_SPEECH_VOICE_TYPE`。
- `resource_id`：豆包语音 2.0 音色使用 `seed-tts-2.0`。
- `speech_rate`：`0` 为正常，`100` 为 2 倍速，`-50` 为 0.5 倍速。
- `sample_rate`：默认为 `24000`。
- `enable_timestamp`：默认为 `true`。
- `return_usage`：默认为 `true`，在可用时请求使用量元数据。

默认不传递 `additions.explicit_language`。某些端点/密钥组合会拒绝 `zh-cn` 并返回 `unsupported additions explicit language zh-cn`。

对于平缓的中文解说，从 `speech_rate: 0` 开始。如果结果对于已认可的格式太长，在重新生成完整旁白之前，先用 `speech_rate: 25` 或 `50` 制作一个短的对比样本。如果用户偏好豆包的自然节奏，不要为了匹配先前提供商的时长而加速。

## 故障排除

- `load grant: requested grant not found`：密钥类型错误或认证头错误。新控制台 API Key 使用 `X-Api-Key`。
- `speaker permission denied`：语音 ID 错误或未对所选资源授权。
- `quota exceeded`：配额、终身字符数或并发数超限。
- 缺少时间戳：确认 `enable_timestamp: true`，保留查询 JSON，并确认所选端点返回了 `sentences`。

## 安全

绝不将 API 密钥打印或写入日志、元数据、补丁或项目制品中。`.env.example` 应仅包含空的变量名。
