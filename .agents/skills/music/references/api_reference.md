# Music API 参考

## 目录

- [compose](#compose)
- [composition_plan.create](#composition_plancreate)
- [compose_detailed](#compose_detailed)
- [upload](#upload)
- [错误处理](#error-handling)

## compose

从文本提示生成音乐。返回音频流。

### 参数

| 参数 | 类型 | 必需 | 描述 |
|-----------|------|----------|-------------|
| `prompt` | string | 是* | 所需音乐的描述 |
| `composition_plan` | object | 是* | 预定义的创作计划（替代提示） |
| `music_length_ms` | integer | 否 | 时长（毫秒），3000-600000，使用 `prompt` 时；如果省略，模型自行选择 |
| `model_id` | string | 否 | 默认为 `music_v1` |
| `force_instrumental` | boolean | 否 | 保证纯器乐输出（仅提示模式） |
| `respect_sections_durations` | boolean | 否 | 强制每个创作计划章节的精确 `duration_ms` |

*提供 `prompt` 或 `composition_plan` 之一，不能同时提供。

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

### 使用创作计划

```python
plan = client.music.composition_plan.create(
    prompt="A jazz ballad with piano and saxophone",
    music_length_ms=60000
)

# 根据需要修改计划
audio = client.music.compose(
    composition_plan=plan,
    music_length_ms=60000
)
```

## composition_plan.create

从提示生成结构化创作计划，以便在生成音频之前进行精细控制。

### 参数

| 参数 | 类型 | 必需 | 描述 |
|-----------|------|----------|-------------|
| `prompt` | string | 是 | 音乐描述 |
| `music_length_ms` | integer | 是 | 时长（毫秒） |

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

# 检查和修改计划
print(plan.positiveGlobalStyles)
for section in plan.sections:
    print(f"{section.name}: {section.duration_ms}ms")
```

## compose_detailed

生成音乐的同时返回创作计划和元数据以及音频。

### 返回

| 字段 | 描述 |
|-------|-------------|
| `json` | 创作计划 + 歌曲元数据（包含歌词，如果适用） |
| `filename` | 输出文件标识符 |
| `audio` | 音频字节 |

### Python

```python
result = client.music.compose_detailed(
    prompt="A pop song about summer adventures",
    music_length_ms=120000
)

# 访问创作计划和元数据
print(result.json)

# 保存音频
with open(result.filename, "wb") as f:
    f.write(result.audio)
```

## upload

上传音乐文件用于后续修复工作流。此端点仅对有权访问修复功能的企业客户可用。

### 参数

| 参数 | 类型 | 必需 | 描述 |
|-----------|------|----------|-------------|
| `file` | file | 是 | 要上传的音频文件 |
| `extract_composition_plan` | boolean | 否 | 如果为 `true`，响应包含提取的创作计划，并且可能需要更长时间返回 |

### 返回

| 字段 | 描述 |
|-------|-------------|
| `song_id` | 上传歌曲的唯一标识符 |
| `composition_plan` | 提取的创作计划，如果未启用 `extract_composition_plan` 则为 `null` |

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

当提示引用受版权保护的材料（特定艺术家、乐队或受版权保护的歌词）时发生。错误响应包含带有替代措辞的 `prompt_suggestion`。

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

当创作计划包含受版权保护的风格时返回。错误包含带有更正后风格的 `composition_plan_suggestion`。对于有害内容不提供建议。

### 常见 HTTP 错误

| 编码 | 含义 |
|------|---------|
| 401 | 无效的 API 密钥 |
| 422 | 无效参数 |
| 429 | 超出速率限制 |
