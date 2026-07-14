# 音乐 API 参考

## 目录

- [compose](#compose)
- [composition_plan.create](#composition_plancreate)
- [compose_detailed](#compose_detailed)
- [upload](#upload)
- [错误处理](#error-handling)

## compose

根据文本提示词生成音乐。返回音频流。

### 参数

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `prompt` | string | 是* | 所需音乐的描述 |
| `composition_plan` | object | 是* | 预定义的作曲方案（替代 prompt） |
| `music_length_ms` | integer | 否 | 持续时间（毫秒），范围 3,000–600,000；使用 `prompt` 时若省略则由模型选择 |
| `model_id` | string | 否 | 默认为 `music_v1` |
| `force_instrumental` | boolean | 否 | 确保输出为纯器乐（仅提示词模式） |
| `respect_sections_durations` | boolean | 否 | 强制遵循作曲方案中每个段落的精确 `duration_ms` |

*提供 `prompt` 或 `composition_plan` 其中之一，不能同时提供。

### Python

```python
audio = client.music.compose(
    prompt="An upbeat electronic track with synth leads",
    music_length_ms=30000
)

with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### JavaScript

```javascript
const audio = await client.music.compose({
  prompt: "An upbeat electronic track with synth leads",
  musicLengthMs: 30000,
});

const writeStream = createWriteStream("output.mp3");
audio.pipe(writeStream);
```

### 使用作曲方案

```python
plan = client.music.composition_plan.create(
    prompt="A jazz ballad with piano and saxophone",
    music_length_ms=60000
)

# 根据需要修改方案
audio = client.music.compose(
    composition_plan=plan,
    music_length_ms=60000
)
```

## composition_plan.create

根据提示词生成结构化作曲方案，以便在生成音频前进行精细控制。

### 参数

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `prompt` | string | 是 | 音乐描述 |
| `music_length_ms` | integer | 是 | 持续时间（毫秒） |

### 响应结构

```json
{
  "positiveGlobalStyles": ["jazz", "smooth", "warm"],
  "negativeGlobalStyles": ["aggressive", "distorted"],
  "sections": [
    {
      "name": "Intro",
      "localStyles": ["soft", "building"],
      "duration_ms": 15000,
      "lines": [
        { "text": "Instrumental intro", "type": "instrumental" }
      ]
    }
  ]
}
```

### Python

```python
plan = client.music.composition_plan.create(
    prompt="A peaceful ambient track with nature sounds",
    music_length_ms=60000
)

# 查看和修改方案
print(plan.positiveGlobalStyles)
for section in plan.sections:
    print(f"{section.name}: {section.duration_ms}ms")
```

## compose_detailed

生成音乐的同时返回作曲方案和元数据以及音频。

### 返回值

| 字段 | 描述 |
|-------|-------------|
| `json` | 作曲方案 + 歌曲元数据（如适用，包含歌词） |
| `filename` | 输出文件标识符 |
| `audio` | 音频字节 |

### Python

```python
result = client.music.compose_detailed(
    prompt="A pop song about summer adventures",
    music_length_ms=120000
)

# 访问作曲方案和元数据
print(result.json)

# 保存音频
with open(result.filename, "wb") as f:
    f.write(result.audio)
```

## upload

上传音乐文件用于后续补全工作流。此端点仅对拥有补全功能访问权限的企业客户可用。

### 参数

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `file` | file | 是 | 要上传的音频文件 |
| `extract_composition_plan` | boolean | 否 | 如果为 `true`，响应中包含提取的作曲方案，可能返回更慢 |

### 返回值

| 字段 | 描述 |
|-------|-------------|
| `song_id` | 上传歌曲的唯一标识符 |
| `composition_plan` | 提取的作曲方案，未启用 `extract_composition_plan` 时为 `null` |

### Python

```python
client.music.upload(
    file="example_file",
)
```

### cURL

```bash
curl -X POST "https://api.elevenlabs.io/v1/music/upload" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "file=@<file1>"
```

## 错误处理

### bad_prompt

当提示词引用受版权保护的内容（特定艺术家、乐队或受版权保护的歌词）时发生。错误响应包含 `prompt_suggestion`，提供替代措辞。

```python
try:
    audio = client.music.compose(
        prompt="A song like Beatles",
        music_length_ms=30000
    )
except Exception as e:
    print(f"Request failed: {e}")
```

### bad_composition_plan

当作曲方案包含受版权保护的风格时返回。错误包含 `composition_plan_suggestion` 和纠正后的风格。对于有害内容不提供建议。

### 常见 HTTP 错误

| 状态码 | 含义 |
|------|---------|
| 401 | API 密钥无效 |
| 422 | 参数无效 |
| 429 | 超过频率限制 |
