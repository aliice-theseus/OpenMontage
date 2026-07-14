---
name: music
description: 使用 ElevenLabs Music API 生成音乐。适用于创建器乐曲目、带歌词的歌曲、背景音乐、广告曲或任何 AI 生成的音乐作品。支持基于提示词生成、用于精细控制的作曲方案以及带有元数据的详细输出。
license: MIT
compatibility: 需要互联网访问和 ElevenLabs API 密钥（ELEVENLABS_API_KEY）。
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs 音乐生成

通过文本提示词生成音乐 - 支持器乐曲目、带歌词的歌曲以及通过作曲方案进行精细控制。

> **设置：** 请参阅[安装指南](references/installation.md)。对于 JavaScript，仅使用 `@elevenlabs/*` 包。

## 快速开始

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
| `music.compose` | 根据提示词或作曲方案生成音频 |
| `music.composition_plan.create` | 生成结构化方案以实现精细控制 |
| `music.compose_detailed` | 生成音频 + 作曲方案 + 元数据 |
| `music.upload` | 上传音频文件用于后续补全工作流，并可选择提取作曲方案 |

详见 [API 参考](references/api_reference.md) 了解完整参数详情。

`music.upload` 仅对拥有补全功能访问权限的企业客户可用。

## 作曲方案

如需精细控制，先生成作曲方案，修改后再作曲：

```python
plan = client.music.composition_plan.create(
    prompt="An epic orchestral piece building to a climax",
    music_length_ms=60000
)

# 查看/修改风格和段落
print(plan.positiveGlobalStyles)  # 例如 ["orchestral", "epic", "cinematic"]

audio = client.music.compose(
    composition_plan=plan,
    music_length_ms=60000
)
```

## 内容限制

- 不能引用特定艺术家、乐队或受版权保护的歌词
- `bad_prompt` 错误包含 `prompt_suggestion`，提供替代措辞
- `bad_composition_plan` 错误包含 `composition_plan_suggestion`

## 错误处理

```python
try:
    audio = client.music.compose(prompt="...", music_length_ms=30000)
except Exception as e:
    print(f"API error: {e}")
```

常见错误：401（密钥无效）、422（参数无效）、429（频率限制）。

## 参考资料

- [安装指南](references/installation.md)
- [API 参考](references/api_reference.md)
