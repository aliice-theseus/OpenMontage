# 外呼电话

通过 Twilio 集成使用您的 ElevenLabs 代理拨打外呼电话。

## 先决条件

1. 已配置的 ElevenLabs 代理
2. 关联到您代理的 Twilio 电话号码（从 ElevenLabs 控制面板获取 `agent_phone_number_id`）
3. 您的 ElevenLabs API 密钥

## 基本用法

基本的 Python、JavaScript 和 cURL 示例请参阅 [主代理技能](../SKILL.md#outbound-calls)。

## 请求参数

| 参数                                  | 类型    | 必需 | 描述                                             |
|---------------------------------------|---------|------|--------------------------------------------------|
| `agent_id`                            | string  | 是   | 您的 ElevenLabs 代理 ID                          |
| `agent_phone_number_id`               | string  | 是   | 关联到您代理的 Twilio 电话号码 ID                |
| `to_number`                           | string  | 是   | 目标电话号码（E.164 格式）                       |
| `conversation_initiation_client_data` | object  | 否   | 为此通话覆盖对话设置                             |
| `call_recording_enabled`              | boolean | 否   | 是否让 Twilio 录制通话                           |
| `telephony_call_config`               | object  | 否   | 电话呼叫设置如响铃超时                          |

## 响应

```json
{
  "success": true,
  "message": "Call initiated successfully",
  "conversation_id": "conv_abc123",
  "callSid": "CA1234567890abcdef"
}
```

| 字段              | 类型    | 描述                             |
|-------------------|---------|----------------------------------|
| `success`         | boolean | 通话是否成功发起                 |
| `message`         | string  | 状态消息                         |
| `conversation_id` | string  | 用于跟踪的 ElevenLabs 对话 ID    |
| `callSid`         | string  | 用于参考的 Twilio 通话 SID       |

## 自定义通话

使用 `conversation_initiation_client_data` 覆盖特定通话的代理设置：

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
                "first_message": "Hello! This is a reminder about your appointment tomorrow.",
                "language": "en"
            },
            "tts": {
                "voice_id": "JBFqnCBsd6RMkjVDRZzb"
            }
        },
        "dynamic_variables": {
            "customer_name": "John",
            "appointment_time": "2:00 PM"
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
        firstMessage: "Hello! This is a reminder about your appointment tomorrow.",
        language: "en",
      },
      tts: {
        voiceId: "JBFqnCBsd6RMkjVDRZzb",
      },
    },
    dynamicVariables: {
      customer_name: "John",
      appointment_time: "2:00 PM",
    },
  },
});
```

## 配置覆盖

### 代理设置

| 选项           | 类型    | 描述                                   |
|----------------|---------|----------------------------------------|
| `first_message`| string  | 此通话的自定义问候语                   |
| `language`     | string  | 语言代码（如 "en"、"es"、"fr"）        |
| `prompt`       | object  | 覆盖代理提示和 LLM 设置                |

### TTS 设置

| 选项               | 类型    | 描述                     |
|--------------------|---------|--------------------------|
| `voice_id`         | string  | 此通话使用的语音 ID      |
| `stability`        | number  | 语音稳定性（0.0-1.0）   |
| `similarity_boost` | number  | 语音相似度提升（0.0-1.0）|
| `speed`            | number  | 语速倍数                 |

### 电话呼叫配置

| 选项                   | 类型    | 描述                                          |
|------------------------|---------|-----------------------------------------------|
| `ringing_timeout_secs` | integer | 响铃多久后放弃接通（默认：`60`）              |

### 动态变量

使用 `dynamic_variables` 将自定义数据传递给代理的提示。在代理提示中使用 `{{variable_name}}` 语法引用它们。

分配动态变量时，您可以使用 `sanitize` 选项在工具响应发送到 LLM 和转录之前移除敏感值，同时仍允许变量赋值：

| 字段       | 类型    | 默认值  | 描述                                                         |
|------------|---------|---------|--------------------------------------------------------------|
| `sanitize` | boolean | `false` | 如果为 true，在发送到 LLM/转录之前从工具响应中移除赋值值，但仍处理变量赋值 |

## 完整示例

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

# 拨打个性化外呼电话
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
                        "first_message": f"Hello {customer['name']}, this is a friendly reminder about your account."
                    }
                },
                "dynamic_variables": {
                    "customer_name": customer["name"],
                    "balance": customer["balance"]
                }
            }
        )
        print(f"Called {customer['name']}: {response.conversation_id}")
    except Exception as e:
        print(f"Failed to call {customer['name']}: {e}")
```
