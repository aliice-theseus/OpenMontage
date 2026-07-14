---
name: music
description: 使用 ElevenLabs Music API 生成音乐。在创建器乐音轨、带歌词的歌曲、背景音乐、广告歌或任何 AI 生成的音乐作品时使用。支持基于提示的生成、用于精细控制的创作计划以及带元数据的详细输出。
license: MIT
compatibility: 需要互联网连接和 ElevenLabs API 密钥（ELEVENLABS_API_KEY）。
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs 音乐生成

从文本提示生成音乐——支持器乐音轨、带歌词的歌曲以及通过创作计划进行精细控制。

> **设置：** 请参阅 [安装指南](references/installation.md)。对于 JavaScript，请仅使用 `@elevenlabs/*` 包。

## 快速入门

### Python

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

audio = client.music.compose(
    prompt="A chill lo-fi hip hop beat with jazzy piano chords",
    music_length_ms=30000
)

with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### JavaScript

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { createWriteStream } from "fs";

const client = new ElevenLabsClient();
const audio = await client.music.compose({
  prompt: "A chill lo-fi hip hop beat with jazzy piano chords",
  musicLengthMs: 30000,
});
audio.pipe(createWriteStream("output.mp3"));
```

### cURL

```bash
curl -X POST "https://api.elevenlabs.io/v1/music" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"prompt": "A chill lo-fi beat", "music_length_ms": 30000}' --output output.mp3
```

## 方法

| 方法 | 描述 |
|--------|-------------|
| `music.compose` | 从提示或创作计划生成音频 |
| `music.composition_plan.create` | 生成结构化计划以实现精细控制 |
| `music.compose_detailed` | 生成音频 + 创作计划 + 元数据 |
| `music.upload` | 上传音频文件用于后续修复工作流，并可选择提取其创作计划 |

完整参数详情请参阅 [API 参考](references/api_reference.md)。

`music.upload` 仅对有权访问修复功能的企业客户可用。

## 创作计划

为实现精细控制，先生成创作计划，修改它，然后创作：

```python
plan = client.music.composition_plan.create(
    prompt="An epic orchestral piece building to a climax",
    music_length_ms=60000
)

# 检查/修改风格和章节
print(plan.positiveGlobalStyles)  # 例如 ["orchestral", "epic", "cinematic"]

audio = client.music.compose(
    composition_plan=plan,
    music_length_ms=60000
)
```

## 内容限制

- 不能引用特定艺术家、乐队或受版权保护的歌词
- `bad_prompt` 错误包含带有替代措辞的 `prompt_suggestion`
- `bad_composition_plan` 错误包含 `composition_plan_suggestion`

## 错误处理

```python
try:
    audio = client.music.compose(prompt="...", music_length_ms=30000)
except Exception as e:
    print(f"API error: {e}")
```

常见错误：401（无效密钥）、422（无效参数）、429（速率限制）。

## 参考文档

- [安装指南](references/installation.md)
- [API 参考](references/api_reference.md)
