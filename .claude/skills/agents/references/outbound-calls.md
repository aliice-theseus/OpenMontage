# 外呼电话

通过 Twilio 集成使用您的 ElevenLabs 代理进行外呼电话。

## 前提条件

1. 一个已配置的 ElevenLabs 代理
2. 一个链接到代理的 Twilio 电话号码（从 ElevenLabs 仪表板获取 `agent_phone_number_id`）
3. 您的 ElevenLabs API 密钥

## 基本用法

基本的 Python、JavaScript 和 cURL 示例请参见[主代理技能](../SKILL.md#outbound-calls)。

## 请求参数

| 参数 | 类型 | 必填 | 描述 |
|-----------|------|----------|-------------|
| `agent_id` | string | 是 | 您的 ElevenLabs 代理 ID |
| `agent_phone_number_id` | string | 是 | 链接到代理的 Twilio 电话号码 ID |
| `to_number` | string | 是 | 目标电话号码（E.164 格式） |
| `conversation_initiation_client_data` | object | 否 | 覆盖此次呼叫的对话设置 |
| `call_recording_enabled` | boolean | 否 | 是否让 Twilio 录制通话 |
| `telephony_call_config` | object | 否 | 电话呼叫设置，如响铃超时 |

## 响应

```json
{
  "success": true,
  "message": "呼叫已成功发起",
  "conversation_id": "conv_abc123",
  "callSid": "CA1234567890abcdef"
}
```

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `success` | boolean | 呼叫是否成功发起 |
| `message` | string | 状态消息 |
| `conversation_id` | string | ElevenLabs 对话 ID，用于跟踪 |
| `callSid` | string | Twilio 呼叫 SID，供参考 |

## 自定义呼叫

使用 `conversation_initiation_client_data` 覆盖特定呼叫的代理设置：

### Python

```python
response = client.conversational_ai.twilio.outbound_call(
    agent_id="your-agent-id",
    agent_phone_number_id="your-phone-number-id",
    to_number="+1234567890",
    call_recording_enabled=True,
    conversation_initiation_client_data={
        "conversation_config_override": {
            "agent": {
                "first_message": "你好！这是关于您明天预约的提醒。",
                "language": "en"
            },
            "tts": {
                "voice_id": "JBFqnCBsd6RMkjVDRZzb"
            }
        },
        "dynamic_variables": {
            "customer_name": "张三",
            "appointment_time": "下午 2:00"
        }
    }
)
```

### JavaScript

```javascript
const response = await client.conversationalAi.twilio.outboundCall({
  agentId: "your-agent-id",
  agentPhoneNumberId: "your-phone-number-id",
  toNumber: "+1234567890",
  callRecordingEnabled: true,
  conversationInitiationClientData: {
    conversationConfigOverride: {
      agent: {
        firstMessage: "你好！这是关于您明天预约的提醒。",
        language: "en",
      },
      tts: {
        voiceId: "JBFqnCBsd6RMkjVDRZzb",
      },
    },
    dynamicVariables: {
      customer_name: "张三",
      appointment_time: "下午 2:00",
    },
  },
});
```

## 配置覆盖

### 代理设置

| 选项 | 类型 | 描述 |
|--------|------|-------------|
| `first_message` | string | 此次呼叫的自定义问候语 |
| `language` | string | 语言代码（例如 "en"、"es"、"fr"） |
| `prompt` | object | 覆盖代理提示词和 LLM 设置 |

### TTS 设置

| 选项 | 类型 | 描述 |
|--------|------|-------------|
| `voice_id` | string | 此次呼叫使用的音色 ID |
| `stability` | number | 语音稳定性（0.0-1.0） |
| `similarity_boost` | number | 语音相似度增强（0.0-1.0） |
| `speed` | number | 语速倍数 |

### 电话呼叫配置

| 选项 | 类型 | 描述 |
|--------|------|-------------|
| `ringing_timeout_secs` | integer | 响铃多久后放弃（默认：`60`） |

### 动态变量

使用 `dynamic_variables` 将自定义数据传递给代理的提示词。在代理的提示词中使用 `{{variable_name}}` 语法引用它们。

分配动态变量时，您可以使用 `sanitize` 选项，在工具响应发送到 LLM 和转录文本之前移除敏感值，同时仍然允许变量赋值：

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `sanitize` | boolean | `false` | 如果为 true，该赋值在发送到 LLM/转录文本之前从工具响应中移除，但变量赋值仍会被处理 |

## 完整示例

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

# 发起个性化外呼
customers = [
    {"name": "Alice", "phone": "+1234567890", "balance": "$150.00"},
    {"name": "Bob", "phone": "+0987654321", "balance": "$75.50"},
]

for customer in customers:
    try:
        response = client.conversational_ai.twilio.outbound_call(
            agent_id="payment-reminder-agent",
            agent_phone_number_id="your-phone-number-id",
            to_number=customer["phone"],
            call_recording_enabled=True,
            conversation_initiation_client_data={
                "conversation_config_override": {
                    "agent": {
                        "first_message": f"你好 {customer['name']}，这是关于您账户的友好提醒。"
                    }
                },
                "dynamic_variables": {
                    "customer_name": customer["name"],
                    "balance": customer["balance"]
                }
            }
        )
        print(f"已呼叫 {customer['name']}：{response.conversation_id}")
    except Exception as e:
        print(f"呼叫 {customer['name']} 失败：{e}")
```
