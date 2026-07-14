# ElevenLabs API 参考

ElevenLabs 音频生成服务的详细 API 文档。

## 认证

```python
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
```

## 文本转语音模型

| 模型 ID | 描述 | 语言数 | 延迟 |
|----------|-------------|-----------|-------|
| `eleven_flash_v2_5` | 超低延迟流式传输 | 32 | ~75ms |
| `eleven_multilingual_v2` | 最高质量 | 32 | 标准 |
| `eleven_turbo_v2_5` | 快速，质量好 | 32 | 低 |
| `eleven_v3` | 最佳情感范围（alpha） | 32+ | 较高 |

## 语音设置

| 参数 | 范围 | 默认值 | 效果 |
|-----------|-------|---------|--------|
| `stability` | 0.0-1.0 | 0.5 | 越低越有表现力/变化 |
| `similarity_boost` | 0.0-1.0 | 0.75 | 越高越接近原声 |
| `style` | 0.0-1.0 | 0.0 | 风格夸张（v2 模型）|
| `speed` | 0.5-2.0 | 1.0 | 播放速度倍数 |

## 输出格式

| 格式代码 | 采样率 | 比特率 | 所需层级 |
|-------------|-------------|---------|---------------|
| `mp3_44100_128` | 44.1kHz | 128kbps | 免费（默认）|
| `mp3_44100_192` | 44.1kHz | 192kbps | Creator+ |
| `pcm_44100` | 44.1kHz | - | Pro+ |
| `ulaw_8000` | 8kHz | - | 免费（电话）|

## 长音频（拼接）

为多个生成之间的连续性：

```python
result1 = client.text_to_speech.convert_with_timestamps(
    text="First paragraph...",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2"
)
request_id_1 = result1.request_id

result2 = client.text_to_speech.convert(
    text="Second paragraph...",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    previous_request_ids=[request_id_1]
)
```

## 专业语音克隆 (PVC)

需要 Creator 计划+。创建一个微调模型（3-6 小时训练）。

**要求：**
- 至少 30 分钟，最佳 2-3 小时音频
- 推荐专业 XLR 麦克风
- 防喷罩，约 20cm 距离
- 峰值电平：-6dB 到 -3dB
- 一致的表演风格

**工作流：**

```python
# 1. 使用样本创建 PVC
pvc = client.voices.create_professional_voice_clone(
    name="My Pro Voice",
    files=["recording1.mp3", "recording2.mp3", ...],
)

# 2. 获取验证验证码
captcha = client.voices.get_pvc_verification_captcha(voice_id=pvc.voice_id)
# 朗读验证码文本并录制

# 3. 提交验证
client.voices.verify_pvc(
    voice_id=pvc.voice_id,
    recording=open("captcha_reading.mp3", "rb")
)

# 4. 开始训练
client.voices.start_pvc_training(voice_id=pvc.voice_id)
```

## 音效参数

| 参数 | 类型 | 必需 | 描述 |
|-----------|------|----------|-------------|
| `text` | string | 是 | 音效描述 |
| `duration_seconds` | float | 否 | 1-22 秒（省略时自动）|
| `prompt_influence` | float | 否 | 0.0-1.0（默认 0.3）|

**计费：** 100 字符/生成（自动）或 25 字符/秒（固定时长）

**示例提示：**
- 环境："Rain on a tin roof, steady and rhythmic"
- 动作："Sword being drawn from sheath, metallic ring"
- 机械："Old car engine struggling to start then roaring to life"

## 音乐参数

| 参数 | 类型 | 必需 | 描述 |
|-----------|------|----------|-------------|
| `prompt` | string | 是* | 自然语言音乐描述 |
| `composition_plan` | object | 是* | 详细创作结构 |
| `duration_ms` | int | 否 | 10000-300000（10秒-5分钟）|
| `instrumental` | bool | 否 | 强制器乐输出 |

*需要 `prompt` 或 `composition_plan` 之一，不能同时提供。

**有效的提示包括：**
1. 类型/风格："indie rock"、"lo-fi hip hop"、"orchestral"
2. 情绪："uplifting"、"melancholic"、"tense"
3. 乐器："acoustic guitar"、"synth pads"、"strings"
4. 节奏/能量："slow"、"upbeat"、"driving"
5. 场景："for a travel vlog"、"podcast intro"

## 按层级的速率限制

| 层级 | TTS 并发 | SFX 并发 | 音乐并发 |
|------|---------------|----------------|------------------|
| 免费 | 2 | 2 | 1 |
| Starter | 3 | 3 | 2 |
| Creator | 5 | 5 | 3 |
| Pro | 10 | 10 | 5 |
| Scale | 15 | 15 | 10 |

## 语音管理

```python
# 列出语音
voices = client.voices.get_all()
for voice in voices.voices:
    print(f"{voice.name}: {voice.voice_id}")

# 删除语音
client.voices.delete(voice_id="your_voice_id")
```

## 错误处理

```python
from elevenlabs.core.api_error import ApiError

try:
    audio = client.text_to_speech.convert(...)
except ApiError as e:
    if e.status_code == 429:
        print("Rate limited - wait and retry")
    elif e.status_code == 401:
        print("Invalid API key")
```

| 编码 | 含义 | 操作 |
|------|---------|--------|
| 401 | 无效的 API 密钥 | 检查 API 密钥 |
| 403 | 功能不可用 | 升级层级 |
| 422 | 无效参数 | 检查请求体 |
| 429 | 速率受限 | 等待重试 |
