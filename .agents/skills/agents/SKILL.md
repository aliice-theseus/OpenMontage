---
name: agents
description: 使用 ElevenLabs 构建语音 AI 代理。在创建语音助手、客服机器人、交互式语音角色或任何实时语音对话体验时使用。
license: MIT
compatibility: 需要互联网连接和 ElevenLabs API 密钥（ELEVENLABS_API_KEY）。
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs 代理平台

使用自然对话、多种 LLM 提供商、自定义工具和简单的 Web 嵌入构建语音 AI 代理。

> **设置：** 请参阅 [安装指南](references/installation.md) 了解 CLI 和 SDK 设置。

## CLI 快速入门

ElevenLabs CLI 是创建和管理代理的推荐方式：

```bash
# 安装 CLI 并进行身份验证
npm install -g @elevenlabs/cli
elevenlabs auth login

# 初始化项目并创建代理
elevenlabs agents init
elevenlabs agents add "My Assistant" --template complete

# 推送到 ElevenLabs 平台
elevenlabs agents push
```

**可用模板：** `complete`、`minimal`、`voice-only`、`text-only`、`customer-service`、`assistant`

### Python

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

agent = client.conversational_ai.agents.create(
    name="My Assistant",
    enable_versioning=True,
    conversation_config={
        "agent": {
            "first_message": "Hello! How can I help?",
            "language": "en",
            "prompt": {
                "prompt": "You are a helpful assistant. Be concise and friendly.",
                "llm": "gemini-2.0-flash",
                "temperature": 0.7
            }
        },
        "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb"}
    }
)
```

### JavaScript

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
const client = new ElevenLabsClient();

const agent = await client.conversationalAi.agents.create({
  name: "My Assistant",
  enableVersioning: true,
  conversationConfig: {
    agent: {
      firstMessage: "Hello! How can I help?",
      language: "en",
      prompt: {
        prompt: "You are a helpful assistant.",
        llm: "gemini-2.0-flash",
        temperature: 0.7
      }
    },
    tts: { voiceId: "JBFqnCBsd6RMkjVDRZzb" }
  }
});
```

### cURL

```bash
curl -X POST "https://api.elevenlabs.io/v1/convai/agents/create?enable_versioning=true" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"name": "My Assistant", "conversation_config": {"agent": {"first_message": "Hello!", "language": "en", "prompt": {"prompt": "You are helpful.", "llm": "gemini-2.0-flash"}}, "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb"}}}'
```

## 开始对话

**服务器端（Python）：** 获取客户端连接的有符号 URL：
```python
signed_url = client.conversational_ai.conversations.get_signed_url(
    agent_id="your-agent-id",
    environment="staging",
)
```

**客户端（JavaScript）：**
```javascript
import { Conversation } from "@elevenlabs/client";

const conversation = await Conversation.startSession({
  agentId: "your-agent-id",
  environment: "staging",
  onMessage: (msg) => console.log("Agent:", msg.message),
  onUserTranscript: (t) => console.log("User:", t.message),
  onError: (e) => console.error(e)
});
```

**React Hook：**
```typescript
import { useConversation } from "@elevenlabs/react";

const conversation = useConversation({ onMessage: (msg) => console.log(msg) });
// 从后端获取目标环境的有符号 URL，然后：
await conversation.startSession({ signedUrl: token });
```

## 配置

| 提供商    | 模型 |
|-----------|------|
| OpenAI    | `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo` |
| Anthropic | `claude-sonnet-4-6`, `claude-sonnet-4-5`, `claude-sonnet-4`, `claude-haiku-4-5`, `claude-3-7-sonnet`, `claude-3-5-sonnet`, `claude-3-haiku` |
| Google    | `gemini-3.1-flash-lite-preview`, `gemini-3-pro-preview`, `gemini-3-flash-preview`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-2.0-flash`, `gemini-2.0-flash-lite` |
| ElevenLabs | `glm-45-air-fp8`, `qwen3-30b-a3b`, `gpt-oss-120b` |
| 自定义    | `custom-llm`（自带端点） |

使用 `GET /v1/convai/llm/list` 查看当前模型目录，包括弃用状态、令牌/上下文限制以及图片输入支持等能力标志。

**热门语音：** `JBFqnCBsd6RMkjVDRZzb`（George）、`EXAVITQu4vr4xnSDxMaL`（Sarah）、`onwK4e9ZLuTAKqWW03F9`（Daniel）、`XB0fDUnXU5powFXDhCwa`（Charlotte）

**抢话程度：** `patient`（等待用户说完更长时间）、`normal` 或 `eager`（快速响应）

所有选项请参阅 [代理配置](references/agent-configuration.md)。

## 工具

通过 webhook、客户端或内置系统工具扩展代理。工具定义在 `conversation_config.agent.prompt` 内：

工作区环境变量可以解析每个环境下的服务器工具 URL、请求头和认证连接，运行时系统变量如 `{{system__conversation_history}}` 可在需要时将完整对话上下文传递到工具调用中。

```python
"prompt": {
    "prompt": "You are a helpful assistant that can check the weather.",
    "llm": "gemini-2.0-flash",
    "tools": [
        # Webhook：服务器端 API 调用
        {"type": "webhook", "name": "get_weather", "description": "Get weather",
         "api_schema": {"url": "https://api.example.com/weather", "method": "POST",
             "request_body_schema": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]}}},
        # Client：在浏览器中运行
        {"type": "client", "name": "show_product", "description": "Display a product",
         "parameters": {"type": "object", "properties": {"productId": {"type": "string"}}, "required": ["productId"]}}
    ],
    "built_in_tools": {
        "end_call": {},
        "transfer_to_number": {"transfers": [{"transfer_destination": {"type": "phone", "phone_number": "+1234567890"}, "condition": "User asks for human support"}]}
    }
}
```

**客户端工具**在浏览器中运行：
```javascript
clientTools: {
  show_product: async ({ productId }) => {
    document.getElementById("product").src = `/products/${productId}`;
    return { success: true };
  }
}
```

完整文档请参阅 [客户端工具参考](references/client-tools.md)。

## Widget 嵌入

```html
<elevenlabs-convai agent-id="your-agent-id"></elevenlabs-convai>
<script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
```

使用属性自定义：`avatar-image-url`、`action-text`、`start-call-text`、`end-call-text`。

所有选项请参阅 [Widget 嵌入参考](references/widget-embedding.md)。

## 外呼电话

通过 Twilio 集成使用代理拨打外呼电话：

### Python

```python
response = client.conversational_ai.twilio.outbound_call(
    agent_id="your-agent-id",
    agent_phone_number_id="your-phone-number-id",
    to_number="+1234567890",
    call_recording_enabled=True
)
print(f"Call initiated: {response.conversation_id}")
```

### JavaScript

```javascript
const response = await client.conversationalAi.twilio.outboundCall({
  agentId: "your-agent-id",
  agentPhoneNumberId: "your-phone-number-id",
  toNumber: "+1234567890",
  callRecordingEnabled: true,
});
```

### cURL

```bash
curl -X POST "https://api.elevenlabs.io/v1/convai/twilio/outbound-call" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"agent_id": "your-agent-id", "agent_phone_number_id": "your-phone-number-id", "to_number": "+1234567890", "call_recording_enabled": true}'
```

配置覆盖和动态变量请参阅 [外呼电话参考](references/outbound-calls.md)。

## 管理代理

### 使用 CLI（推荐）

```bash
# 列出代理并检查状态
elevenlabs agents list
elevenlabs agents status

# 从平台导入代理到本地配置
elevenlabs agents pull                      # 导入所有代理
elevenlabs agents pull --agent <agent-id>   # 导入指定代理

# 将本地更改推送到平台
elevenlabs agents push              # 上传配置
elevenlabs agents push --dry-run    # 先预览更改

# 添加工具
elevenlabs tools add-webhook "Weather API"
elevenlabs tools add-client "UI Tool"
```

### 项目结构

CLI 创建一个用于管理代理的项目结构：

```
your_project/
├── agents.json       # 代理定义
├── tools.json        # 工具配置
├── tests.json        # 测试配置
├── agent_configs/    # 单个代理配置
├── tool_configs/     # 单个工具配置
└── test_configs/     # 单个测试配置
```

### SDK 示例

```python
# 列出
agents = client.conversational_ai.agents.list()

# 获取
agent = client.conversational_ai.agents.get(agent_id="your-agent-id")

# 更新（部分 - 仅包含要更改的字段）
client.conversational_ai.agents.update(agent_id="your-agent-id", name="New Name")
client.conversational_ai.agents.update(agent_id="your-agent-id",
    conversation_config={
        "agent": {"prompt": {"prompt": "New instructions", "llm": "claude-sonnet-4"}}
    })

# 删除
client.conversational_ai.agents.delete(agent_id="your-agent-id")
```

所有配置选项和 SDK 示例请参阅 [代理配置](references/agent-configuration.md)。

## 错误处理

```python
try:
    agent = client.conversational_ai.agents.create(...)
except Exception as e:
    print(f"API error: {e}")
```

常见错误：**401**（无效密钥）、**404**（未找到）、**422**（无效配置）、**429**（速率限制）

## 参考文档

- [安装指南](references/installation.md) - SDK 设置和迁移
- [代理配置](references/agent-configuration.md) - 所有配置选项和 CRUD 示例
- [客户端工具](references/client-tools.md) - Webhook、客户端和系统工具
- [Widget 嵌入](references/widget-embedding.md) - 网站集成
- [外呼电话](references/outbound-calls.md) - Twilio 电话集成
