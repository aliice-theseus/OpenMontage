---
name: agents
description: Build voice AI agents with ElevenLabs. Use when creating voice assistants, customer service bots, interactive voice characters, or any real-time voice conversation experience.
license: MIT
compatibility: Requires internet access and an ElevenLabs API key (ELEVENLABS_API_KEY).
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs 代理平台

构建具有自然对话、多 LLM 提供商、自定义工具和简易网页嵌入的语音 AI 代理。

> **设置：** 参见[安装指南](references/installation.md)了解 CLI 和 SDK 设置。

## CLI 快速开始

ElevenLabs CLI 是创建和管理代理的推荐方式：

```bash
# 安装 CLI 并认证
npm install -g @elevenlabs/cli
elevenlabs auth login

# 初始化项目并创建代理
elevenlabs agents init
elevenlabs agents add "我的助手" --template complete

# 推送到 ElevenLabs 平台
elevenlabs agents push
```

**可用模板：** `complete`、`minimal`、`voice-only`、`text-only`、`customer-service`、`assistant`

### Python

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

agent = client.conversational_ai.agents.create(
    name="我的助手",
    enable_versioning=True,
    conversation_config={
        "agent": {
            "first_message": "你好！有什么可以帮助你的？",
            "language": "en",
            "prompt": {
                "prompt": "你是一个有用的助手。保持简洁友好。",
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
  name: "我的助手",
  enableVersioning: true,
  conversationConfig: {
    agent: {
      firstMessage: "你好！有什么可以帮助你的？",
      language: "en",
      prompt: {
        prompt: "你是一个有用的助手。",
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
  -d '{"name": "我的助手", "conversation_config": {"agent": {"first_message": "你好！", "language": "en", "prompt": {"prompt": "你是有用的助手。", "llm": "gemini-2.0-flash"}}, "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb"}}}'
```

## 开始对话

**服务端（Python）：** 获取客户端连接的签名 URL：
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
  onMessage: (msg) => console.log("代理：", msg.message),
  onUserTranscript: (t) => console.log("用户：", t.message),
  onError: (e) => console.error(e)
});
```

**React Hook：**
```typescript
import { useConversation } from "@elevenlabs/react";

const conversation = useConversation({ onMessage: (msg) => console.log(msg) });
// 从后端获取目标环境的签名 URL，然后：
await conversation.startSession({ signedUrl: token });
```

## 配置

| 提供商 | 模型 |
|----------|--------|
| OpenAI | `gpt-5`、`gpt-5-mini`、`gpt-5-nano`、`gpt-4.1`、`gpt-4.1-mini`、`gpt-4.1-nano`、`gpt-4o`、`gpt-4o-mini`、`gpt-4-turbo` |
| Anthropic | `claude-sonnet-4-6`、`claude-sonnet-4-5`、`claude-sonnet-4`、`claude-haiku-4-5`、`claude-3-7-sonnet`、`claude-3-5-sonnet`、`claude-3-haiku` |
| Google | `gemini-3.1-flash-lite-preview`、`gemini-3-pro-preview`、`gemini-3-flash-preview`、`gemini-2.5-flash`、`gemini-2.5-flash-lite`、`gemini-2.0-flash`、`gemini-2.0-flash-lite` |
| ElevenLabs | `glm-45-air-fp8`、`qwen3-30b-a3b`、`gpt-oss-120b` |
| 自定义 | `custom-llm`（自带端点） |

使用 `GET /v1/convai/llm/list` 查看当前模型目录，包括弃用状态、token/上下文限制和功能标志（如图像输入支持）。

**热门音色：** `JBFqnCBsd6RMkjVDRZzb`（George）、`EXAVITQu4vr4xnSDxMaL`（Sarah）、`onwK4e9ZLuTAKqWW03F9`（Daniel）、`XB0fDUnXU5powFXDhCwa`（Charlotte）

**回应急切度：** `patient`（等待用户说完更久）、`normal` 或 `eager`（快速回应）

所有选项参见[代理配置](references/agent-configuration.md)。

## 工具

使用 webhook、客户端或内置系统工具扩展代理。工具在 `conversation_config.agent.prompt` 内定义：

工作区环境变量可以解析按环境区分的服务端工具 URL、请求头和认证连接，运行时系统变量（如 `{{system__conversation_history}}`）可在需要时将完整对话上下文传递到工具调用中。

```python
"prompt": {
    "prompt": "你是一个可以查询天气的有用助手。",
    "llm": "gemini-2.0-flash",
    "tools": [
        # Webhook：服务端 API 调用
        {"type": "webhook", "name": "get_weather", "description": "获取天气",
         "api_schema": {"url": "https://api.example.com/weather", "method": "POST",
             "request_body_schema": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]}}},
        # 客户端：在浏览器中运行
        {"type": "client", "name": "show_product", "description": "显示产品",
         "parameters": {"type": "object", "properties": {"productId": {"type": "string"}}, "required": ["productId"]}}
    ],
    "built_in_tools": {
        "end_call": {},
        "transfer_to_number": {"transfers": [{"transfer_destination": {"type": "phone", "phone_number": "+1234567890"}, "condition": "用户要求人工支持"}]}
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

完整文档参见[客户端工具参考](references/client-tools.md)。

## 小组件嵌入

```html
<elevenlabs-convai agent-id="your-agent-id"></elevenlabs-convai>
<script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
```

使用属性自定义：`avatar-image-url`、`action-text`、`start-call-text`、`end-call-text`。

所有选项参见[小组件嵌入参考](references/widget-embedding.md)。

## 外呼电话

通过 Twilio 集成使用您的代理进行外呼电话：

### Python

```python
response = client.conversational_ai.twilio.outbound_call(
    agent_id="your-agent-id",
    agent_phone_number_id="your-phone-number-id",
    to_number="+1234567890",
    call_recording_enabled=True
)
print(f"呼叫已发起：{response.conversation_id}")
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

配置覆盖和动态变量参见[外呼电话参考](references/outbound-calls.md)。

## 管理代理

### 使用 CLI（推荐）

```bash
# 列出代理并检查状态
elevenlabs agents list
elevenlabs agents status

# 从平台导入代理到本地配置
elevenlabs agents pull                      # 导入所有代理
elevenlabs agents pull --agent <agent-id>   # 导入特定代理

# 将本地更改推送到平台
elevenlabs agents push              # 上传配置
elevenlabs agents push --dry-run    # 先预览更改

# 添加工具
elevenlabs tools add-webhook "天气 API"
elevenlabs tools add-client "UI 工具"
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

# 更新（部分——仅包含要更改的字段）
client.conversational_ai.agents.update(agent_id="your-agent-id", name="新名称")
client.conversational_ai.agents.update(agent_id="your-agent-id",
    conversation_config={
        "agent": {"prompt": {"prompt": "新指令", "llm": "claude-sonnet-4"}}
    })

# 删除
client.conversational_ai.agents.delete(agent_id="your-agent-id")
```

所有配置选项和 SDK 示例参见[代理配置](references/agent-configuration.md)。

## 错误处理

```python
try:
    agent = client.conversational_ai.agents.create(...)
except Exception as e:
    print(f"API 错误：{e}")
```

常见错误：**401**（密钥无效）、**404**（未找到）、**422**（配置无效）、**429**（速率限制）

## 参考

- [安装指南](references/installation.md) - SDK 设置和迁移
- [代理配置](references/agent-configuration.md) - 所有配置选项和 CRUD 示例
- [客户端工具](references/client-tools.md) - Webhook、客户端和系统工具
- [小组件嵌入](references/widget-embedding.md) - 网站集成
- [外呼电话](references/outbound-calls.md) - Twilio 电话呼叫集成
