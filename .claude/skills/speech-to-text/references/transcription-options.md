# 转录选项

## 请求参数

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `file` | file | 是 | 要转录的音频或视频文件 |
| `model_id` | string | 是 | `scribe_v2`（或旧版 `scribe_v1`）用于批量转录 |
| `language_code` | string | 否 | 语言提示（ISO 639-1 或 ISO 639-3，例如 `en` 或 `eng`） |
| `timestamps_granularity` | string | 否 | `none`、`word` 或 `character`（默认：`word`） |
| `diarize` | boolean | 否 | 启用说话人分离（默认：`false`；最多 32 个说话人） |
| `num_speakers` | integer | 否 | 要检测的最大说话人数（批量最多 32 个） |
| `diarization_threshold` | number | 否 | 调整说话人分离灵敏度（默认：约0.22；仅在 `diarize=true` 且未设置 `num_speakers` 时） |
| `keyterms` | array | 否 | 影响转录倾向的术语（最多 100 个；每个 ≤50 字符，≤5 个词） |
| `tag_audio_events` | boolean | 否 | 检测非语音声音如笑声、掌声（默认：`true`） |
| `entity_detection` | string or array | 否 | 检测实体（例如 `pii`、`phi`、`pci`、`offensive_language`） |
| `no_verbatim` | boolean | 否 | 如果为 `true`，移除填充词、错误开头和非语音声音（`scribe_v2` 支持） |
| `use_multi_channel` | boolean | 否 | 将多声道音频拆分为单独的转录（默认：`false`；最多 5 声道，最长 1 小时） |
| `cloud_storage_url` | string | 否 | 要转录的 HTTPS URL，替代上传文件（最大 2GB） |
| `webhook` | boolean | 否 | 异步处理并将结果发送到 webhook（默认：`false`） |
| `webhook_id` | string | 否 | 目标特定 webhook（仅在 `webhook=true` 时） |
| `webhook_metadata` | string or object | 否 | 包含在 webhook 响应中的自定义元数据（最大 16KB） |
| `temperature` | double | 否 | 输出随机性（0.0-2.0）；默认值因模型而异 |
| `seed` | integer | 否 | 确定性输出（0-2147483647）；相同种子 = 相同结果 |
| `additional_formats` | array | 否 | 将转录导出为 `docx`、`html`、`pdf`、`srt`、`txt` 或 `segmented_json` |
| `file_format` | string | 否 | `pcm_s16le_16`（较低延迟）或 `other`（默认） |
| `enable_logging` | boolean | 否 | 设为 `false` 为零保留模式（仅企业；默认：`true`） |

## Python 示例

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

with open("audio.mp3", "rb") as audio_file:
    result = client.speech_to_text.convert(
        file=audio_file,
        model_id="scribe_v2",
        language_code="eng",
        timestamps_granularity="word",
        diarize=True,
        keyterms=["ElevenLabs", "Scribe"]
    )
```

## JavaScript 示例

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { createReadStream } from "fs";

const client = new ElevenLabsClient();

const result = await client.speechToText.convert({
  file: createReadStream("audio.mp3"),
  modelId: "scribe_v2",
  languageCode: "eng",
  timestampsGranularity: "word",
  diarize: true,
  keyterms: ["ElevenLabs", "Scribe"],
});
```

## cURL 示例

```bash
curl -X POST "https://api.elevenlabs.io/v1/speech-to-text" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "file=@audio.mp3" \
  -F "model_id=scribe_v2" \
  -F "language_code=eng" \
  -F "timestamps_granularity=word" \
  -F "diarize=true"
```

## 响应结构

```json
{
  "text": "来自音频文件的完整转录文本。",
  "language_code": "eng",
  "language_probability": 0.98,
  "words": [
    {
      "text": "The",
      "start": 0.0,
      "end": 0.15,
      "type": "word",
      "speaker_id": "speaker_0"
    },
    {
      "text": " ",
      "start": 0.15,
      "end": 0.16,
      "type": "spacing",
      "speaker_id": "speaker_0"
    }
  ]
}
```

## 响应字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `text` | string | 完整转录文本 |
| `language_code` | string | 检测到的语言（ISO 639-1 或 ISO 639-3） |
| `language_probability` | float | 检测置信度（0-1） |
| `words` | array | 词级时间戳（如果请求） |
| `words[].text` | string | 转录的词或空格 |
| `words[].start` | float | 开始时间（秒） |
| `words[].end` | float | 结束时间（秒） |
| `words[].type` | string | `word`、`spacing` 或 `audio_event` |
| `words[].speaker_id` | string | 说话人标识符（如果启用了说话人分离） |
| `transcription_id` | string | 此转录的唯一标识符 |
| `additional_formats` | array | 导出的转录格式（如果请求） |
| `entities` | array | 检测到的实体，含文本、类型和字符偏移量（如果启用 entity_detection） |

## 支持的语言（90+）

常用语言（ISO 639-3 代码）：

| 代码 | 语言 | 代码 | 语言 |
|------|----------|------|----------|
| `eng` | 英语 | `jpn` | 日语 |
| `spa` | 西班牙语 | `kor` | 韩语 |
| `fra` | 法语 | `zho` | 中文 |
| `deu` | 德语 | `ara` | 阿拉伯语 |
| `ita` | 意大利语 | `hin` | 印地语 |
| `por` | 葡萄牙语 | `tur` | 土耳其语 |
| `nld` | 荷兰语 | `swe` | 瑞典语 |
| `pol` | 波兰语 | `dan` | 丹麦语 |
| `rus` | 俄语 | `fin` | 芬兰语 |

完整列表：南非荷兰语、阿姆哈拉语、亚美尼亚语、阿塞拜疆语、白俄罗斯语、孟加拉语、波斯尼亚语、保加利亚语、缅甸语、粤语、加泰罗尼亚语、宿务语、克罗地亚语、捷克语、爱沙尼亚语、菲律宾语、格鲁吉亚语、希腊语、古吉拉特语、豪萨语、希伯来语、匈牙利语、冰岛语、印度尼西亚语、爱尔兰语、爪哇语、卡纳达语、哈萨克语、高棉语、吉尔吉斯语、老挝语、拉脱维亚语、立陶宛语、卢森堡语、马其顿语、马来语、马拉雅拉姆语、马耳他语、毛利语、马拉地语、蒙古语、尼泊尔语、挪威语、奥里亚语、普什图语、波斯语、旁遮普语、罗马尼亚语、塞尔维亚语、绍纳语、信德语、斯洛伐克语、斯洛文尼亚语、索马里语、斯瓦希里语、泰米尔语、塔吉克语、泰卢固语、泰语、乌克兰语、乌尔都语、乌兹别克语、越南语、威尔士语、沃洛夫语、科萨语、约鲁巴语、祖鲁语。

## 格式要求

**音频：** MP3、WAV、M4A、FLAC、OGG、WebM、AAC、AIFF、Opus
**视频：** MP4、AVI、MKV、MOV、WMV、FLV、WebM、MPEG、3GPP

**限制：**
- 最大文件大小：3GB（文件上传）或 2GB（云存储 URL）
- 最长时长：10 小时（标准）或 1 小时（多声道模式）

## 使用案例

### 带说话人的字幕生成

```python
result = client.speech_to_text.convert(
    file=audio_file,
    model_id="scribe_v2",
    timestamps_granularity="word",
    diarize=True
)

# 生成带说话人标签的 SRT
for i, word in enumerate(result.words, 1):
    if word.type == "word":
        print(f"[{word.speaker_id}] {word.text} ({word.start:.2f}s)")
```

### 带自定义术语的会议转录

```python
with open("meeting.mp3", "rb") as f:
    result = client.speech_to_text.convert(
        file=f,
        model_id="scribe_v2",
        diarize=True,
        keyterms=["Q4 预测", "收入目标", "ACME 公司"]
    )

# 按说话人分组
current_speaker = None
for word in result.words:
    if word.type == "word":
        if word.speaker_id != current_speaker:
            current_speaker = word.speaker_id
            print(f"\n[{current_speaker}]:", end=" ")
        print(word.text, end="")
```
