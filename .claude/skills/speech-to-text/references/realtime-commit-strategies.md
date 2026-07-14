# 转录与提交策略

控制实时流式传输中转录何时以及如何最终确定。

## 为什么提交很重要

在实时转录中，模型随着更多音频到达而不断改进其理解。听起来像"their"的词在听到更多上下文后可能变成"there"或"they're"。**提交**机制让您决定何时"锁定"转录。

## 转录类型

| 类型 | 描述 |
|------|-------------|
| **部分** | 随着音频处理而频繁更新的中间"最佳猜测"结果。用于实时反馈（用户说话时显示文本），但不要保存这些——它们可能会改变。 |
| **已提交** | 提交发生后获得的最终稳定结果。用作应用程序的真实来源——它们不会改变。 |
| **带时间戳的已提交** | 与已提交相同，但包含用于字幕、卡拉OK或唇形同步的词级计时数据。 |

## 手动提交（默认）

您显式控制转录片段何时最终确定。

### Python

```python
async with client.speech_to_text.realtime.connect(
    model_id="scribe_v2_realtime",
) as connection:
    # 发送音频
    await connection.send({
        "audio_base_64": audio_base_64,
        "sample_rate": 16000,
    })

    # 准备就绪时提交（例如，语音暂停、句子结束）
    await connection.commit()
```

### JavaScript

```javascript
const connection = await client.speechToText.realtime.connect({
  modelId: "scribe_v2_realtime",
});

// 发送音频
connection.send({
  audioBase64: audioBase64,
  sampleRate: 16000,
});

// 准备就绪时提交
connection.commit();
```

### 最佳实践

- **每 20-30 秒提交一次**以获得最佳性能
- **在静音期间**或逻辑断点处（句子结束、说话人切换）提交
- **在 90 秒时自动提交**如果未发送手动提交

### 提供上下文

在第一个音频块中发送之前的文本以帮助模型：

```python
await connection.send({
    "audio_base_64": first_chunk,
    "sample_rate": 16000,
    "previous_text": "正如我刚才说的，"  # 保持在 50 个字符以内
})
```

这有助于：
- 在重新连接后继续对话
- 提供上下文以获得更好的准确性
- 处理句子片段

## 语音活动检测（VAD）

VAD 监听静音并在说话人停顿时自动提交。这会创建与人们实际说话方式匹配的自然转录片段——在句子和想法之间停顿。推荐用于实时麦克风输入。

### 配置

#### React（`useScribe`）

```typescript
import { useScribe, CommitStrategy } from "@elevenlabs/react";

const scribe = useScribe({
  modelId: "scribe_v2_realtime",
  commitStrategy: CommitStrategy.VAD,
  // 可选 VAD 调优：
  vadSilenceThresholdSecs: 1.5,    // 提交前的静音时长
  vadThreshold: 0.4,               // 语音检测灵敏度（0-1）
  minSpeechDurationMs: 100,        // 所需最小语音长度
  minSilenceDurationMs: 100,       // 所需最小静音长度
});
```

> **重要：** 默认是 `CommitStrategy.MANUAL`。对于麦克风输入，始终设置 `CommitStrategy.VAD`——否则，已提交的转录永远不会触发，连接可能会断开。

#### JavaScript 客户端

```javascript
const connection = await client.speechToText.realtime.connect({
  modelId: "scribe_v2_realtime",
  vad: {
    silenceThresholdSecs: 1.5,    // 提交前的静音时长
    threshold: 0.4,               // 语音检测灵敏度（0-1）
    minSpeechDurationMs: 100,     // 所需最小语音长度
    minSilenceDurationMs: 100,    // 所需最小静音长度
  },
});
```

### 参数

| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `silenceThresholdSecs` | 自动提交前的静音秒数 | 1.5 |
| `threshold` | 语音检测灵敏度（越低越灵敏） | 0.4 |
| `minSpeechDurationMs` | 忽略短于此值的语音 | 100 |
| `minSilenceDurationMs` | 忽略短于此值的静音 | 100 |

### 何时使用 VAD

- 实时麦克风输入
- 对话应用程序
- 倾向于自然语音边界时
- 客户端实现

### 何时使用手动提交

- 处理音频文件
- 已知的片段边界
- 对计时有最大控制需求
- 服务端批处理

## 支持的音频格式

| 格式 | 采样率 | 说明 |
|--------|-------------|-------|
| PCM 16 位 | 16kHz | 推荐，最佳平衡 |
| PCM 16 位 | 8kHz - 48kHz | 支持范围 |
| μ-law 8 位 | 8kHz | 电话兼容性 |
