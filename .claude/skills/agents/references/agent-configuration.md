# 代理配置

配置会话 AI 代理的完整参考。

## 配置结构

```python
agent = client.conversational_ai.agents.create(
    name="我的代理",
    conversation_config={
        "agent": {
            "first_message": "你好！",
            "language": "en",
            "prompt": {           # LLM、系统提示词、工具和知识库
                "prompt": "你很有帮助。",
                "llm": "gemini-2.0-flash",
                "tools": [...],
                "built_in_tools": {...}
            }
        },
        "tts": {...},             # 语音和 TTS 模型设置
        "asr": {...},             # 语音识别设置
        "turn": {...},            # 轮流说话行为
        "conversation": {...},    # 时长、事件、监控
        "vad": {...},             # 语音活动检测配置
        "language_presets": {...}  # 特定语言覆盖
    },
    platform_settings={...}       # 认证、通话限制
)
```

## conversation_config

控制实时对话行为。

### agent

```python
conversation_config={
    "agent": {
        "first_message": "你好！今天有什么可以帮助你的？",
        "language": "en",
        "disable_first_message_interruptions": False,
        "prompt": {
            "prompt": "你是一个有用的助手。",
            "llm": "gemini-2.0-flash",
            "temperature": 0.7
        }
    }
}
```

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `first_message` | string | `""` | 对话开始时代理说的话 |
| `language` | string | `"en"` | ISO 639-1 语言代码（en、es、fr 等） |
| `disable_first_message_interruptions` | bool | `false` | 防止用户打断第一条消息 |
| `hinglish_mode` | bool | `false` | 启用且语言为印地语时，代理用 Hinglish 回应 |
| `dynamic_variables` | object | - | 包含 `dynamic_variable_placeholders` 键值对的配置 |
| `prompt` | object | - | LLM 配置（见下方 prompt 部分） |

### tts（文本转语音）

```python
conversation_config={
    "tts": {
        "voice_id": "JBFqnCBsd6RMkjVDRZzb",
        "model_id": "eleven_flash_v2_5",
        "stability": 0.5,
        "similarity_boost": 0.8,
        "speed": 1.0,
        "optimize_streaming_latency": 3,
        "expressive_mode": True
    }
}
```

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `voice_id` | string | `"cjVigY5qzO86Huf0OWal"` | 使用的音色 |
| `model_id` | string | - | TTS 模型（见下方） |
| `stability` | float | `0.5` | 0-1，越低越有表现力 |
| `similarity_boost` | float | `0.8` | 0-1，越高越接近原始语音 |
| `speed` | float | `1.0` | 0.7-1.2，语速倍数 |
| `optimize_streaming_latency` | int | - | 0-4，越高越快但质量越低 |
| `expressive_mode` | bool | `true` | 启用富有表现力的语音生成 |
| `agent_output_audio_format` | string | - | 输出音频编解码器格式 |
| `pronunciation_dictionary_locators` | array | - | 发音覆盖 |

**代理可用的 TTS 模型：**

| 模型 ID | 语言数 | 延迟 |
|----------|-----------|---------|
| `eleven_flash_v2_5` | 32 | 约75ms（推荐） |
| `eleven_flash_v2` | 英语 | 约75ms |
| `eleven_turbo_v2_5` | 32 | 约250-300ms |
| `eleven_turbo_v2` | 英语 | 约250-300ms |
| `eleven_multilingual_v2` | 29 | 标准 |
| `eleven_v3_conversational` | 70+ | 标准 |

### asr（自动语音识别）

```python
conversation_config={
    "asr": {
        "quality": "high",
        "keywords": ["ElevenLabs", "TechCorp"],
        "user_input_audio_format": "pcm_16000"
    }
}
```

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `quality` | string | `"high"` | 转录质量级别 |
| `provider` | string | `"elevenlabs"` | ASR 提供商（`elevenlabs` 或 `scribe_realtime`） |
| `keywords` | array | - | 提高识别准确率的词汇 |
| `user_input_audio_format` | string | - | 输入音频格式（例如 `pcm_16000`、`ulaw_8000`） |

### turn（轮流说话）

```python
conversation_config={
    "turn": {
        "turn_timeout": 7,
        "turn_eagerness": "normal",
        "silence_end_call_timeout": -1
    }
}
```

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `turn_timeout` | number | `7` | 重新接洽用户前的等待秒数 |
| `turn_eagerness` | string | `"normal"` | 代理回应的急切程度：`patient`、`normal` 或 `eager` |
| `silence_end_call_timeout` | number | `-1` | 结束通话前的静默秒数（-1 = 禁用） |
| `initial_wait_time` | number | - | 等待用户开始说话的秒数 |
| `spelling_patience` | string | `"auto"` | 实体检测耐心度：`auto` 或 `off` |
| `speculative_turn` | bool | `false` | 启用推测性轮流检测 |
| `soft_timeout_config` | object | - | 用户静默时配置消息（见下方） |

**soft_timeout_config：**

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `timeout_seconds` | number | `-1` | 软超时前的秒数（-1 = 禁用） |
| `message` | string | `"嗯...好吧。"` | 超时代理说的话 |
| `use_llm_generated_message` | bool | `false` | 让 LLM 生成超时消息 |

## prompt（嵌套在 conversation_config.agent 中）

配置 LLM 行为。此对象位于 `conversation_config.agent.prompt`：

```python
conversation_config={
    "agent": {
        "prompt": {
            "prompt": "你是一个有用的客户服务代理...",
            "llm": "gemini-2.0-flash",
            "temperature": 0.7,
            "max_tokens": 500,
            "tools": [...],
            "built_in_tools": {...},
            "knowledge_base": [...]
        }
    }
}
```

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `prompt` | string | `""` | 定义代理行为的系统提示词 |
| `llm` | string | - | 模型 ID（见下方 LLM 提供商） |
| `temperature` | float | `0` | 0-1，越高越有创意 |
| `max_tokens` | int | `-1` | LLM 响应的最大 token 数（-1 = 无限制） |
| `reasoning_effort` | string | - | 推理深度：`none`、`minimal`、`low`、`medium`、`high`（取决于模型） |
| `thinking_budget` | int | - | 推理模型的最大思考 token 数 |
| `tools` | array | - | Webhook 和客户端工具定义 |
| `built_in_tools` | object | - | 系统工具（end_call、transfer 等） |
| `tool_ids` | array | - | 对预配置工具的引用 |
| `knowledge_base` | array | - | 用于 RAG 的文档 |
| `custom_llm` | object | - | 自定义 LLM 端点配置 |
| `timezone` | string | - | IANA 时区（例如 `America/New_York`） |
| `backup_llm_config` | object | - | 备用 LLM 配置 |
| `cascade_timeout_seconds` | number | `8` | 级联到备用 LLM 前的秒数（2-15） |
| `mcp_server_ids` | array | - | 要连接的 MCP 服务器 ID |
| `native_mcp_server_ids` | array | - | 原生 MCP 服务器 ID |
| `ignore_default_personality` | bool | - | 跳过默认个性化指令 |

工作区环境变量让一个代理配置可以跨越多个部署。在服务端工具和 MCP 服务器 URL 中使用 `{{system_env__label}}`，在密钥支持的工具请求头中使用 `{ "env_var_label": "orders_api_key" }`，在 `auth_connection` 中使用 `{ "env_var_label": "orders_oauth" }` 以在运行时解析按环境的认证连接。

### LLM 提供商

| 提供商 | 模型 ID |
|----------|-----------|
| OpenAI | `gpt-5`、`gpt-5-mini`、`gpt-5-nano`、`gpt-4.1`、`gpt-4.1-mini`、`gpt-4.1-nano`、`gpt-4o`、`gpt-4o-mini`、`gpt-4-turbo` |
| Anthropic | `claude-sonnet-4-6`、`claude-sonnet-4-5`、`claude-sonnet-4`、`claude-haiku-4-5`、`claude-3-7-sonnet`、`claude-3-5-sonnet`、`claude-3-haiku` |
| Google | `gemini-3.1-flash-lite-preview`、`gemini-3-pro-preview`、`gemini-3-flash-preview`、`gemini-2.5-flash`、`gemini-2.5-flash-lite`、`gemini-2.0-flash`、`gemini-2.0-flash-lite` |
| ElevenLabs | `glm-45-air-fp8`、`qwen3-30b-a3b`、`gpt-oss-120b`（托管，超低延迟） |
| 自定义 | `custom-llm`（需要 custom_llm 配置） |

使用 `GET /v1/convai/llm/list` 查看当前模型目录，包括弃用状态、token/上下文限制和功能标志（如图像输入支持）。

### 自定义 LLM

`custom_llm` 字段嵌套在 `conversation_config.agent.prompt` 内：

```python
conversation_config={
    "agent": {
        "prompt": {
            "prompt": "你很有帮助。",
            "llm": "custom-llm",
            "custom_llm": {
                "url": "https://your-llm-endpoint.com/v1/chat/completions",
                "model_id": "your-model-id",
                "api_key": {"secret_id": "your-secret-id"},
                "api_type": "chat_completions"  # 或 "responses"
            }
        }
    }
}
```

## platform_settings

安全、限制、摘要和小组件行为的平台级配置。

```python
platform_settings={
    "summary_language": "en",
    "widget": {
        "show_agent_status": True,
        "show_conversation_id": True
    },
    "auth": {
        "enable_auth": True,
        "allowlist": [{"hostname": "example.com"}]
    },
    "call_limits": {
        "agent_concurrency_limit": 10,
        "daily_limit": 100
    }
}
```

### 顶级字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `summary_language` | string | 对话分析输出的语言，如摘要、标题、评估理由和数据收集理由。如果省略，ElevenLabs 会从对话中推断。 |
| `widget` | object | 托管小组件和可分享页面配置。选定选项见下方小组件表格。 |
| `auth` | object | 代理访问的认证和来源限制 |
| `call_limits` | object | 并发和每日使用限制 |
| `guardrails` | object | 代理交互的内置安全和策略控制 |
| `privacy` | object | 录制、保留和对话历史编辑设置 |

### auth

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `enable_auth` | bool | 连接需要签名 URL/令牌 |
| `allowlist` | array | CORS 允许的来源 |
| `shareable_token` | string | 公共对话令牌 |

### call_limits

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `agent_concurrency_limit` | int | 最大同时对话数（默认：-1，无限制） |
| `daily_limit` | int | 每日最大对话数（默认：100000） |
| `bursting_enabled` | bool | 允许以 2 倍成本超出限制（默认：true） |

### guardrails

使用 `platform_settings.guardrails` 配置用户输入和代理行为的内置安全控制。以下字段涵盖当前模式中与代理配置最相关的部分。

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `version` | string | 护栏配置版本。使用 `"1"` 表示当前模式。 |
| `focus` | object | 保持代理在话题上并与配置任务保持一致。 |
| `prompt_injection` | object | 检测提示注入和指令覆盖尝试。 |
| `custom` | object | 配置用户定义的响应验证护栏。 |
| `content` | object | 配置按类别的内容审核护栏。 |

**focus / prompt_injection：**

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `is_enabled` | bool | 启用护栏。 |

**content：**

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `execution_mode` | string | 护栏执行模式：`streaming` 或 `blocking`。 |
| `config` | object | 内容审核的类别阈值设置。 |

**content.config：**

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `sexual` | object | 色情内容的阈值设置。 |
| `violence` | object | 暴力内容的阈值设置。 |
| `harassment` | object | 骚扰内容的阈值设置。 |
| `self_harm` | object | 自残内容的阈值设置。 |
| `profanity` | object | 脏话内容的阈值设置。 |
| `religion_or_politics` | object | 宗教或政治内容的阈值设置。 |
| `medical_and_legal_information` | object | 医疗或法律信息的阈值设置。 |

**content.config.\<category\>：**

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `is_enabled` | bool | 启用该类别的审核。 |
| `threshold` | number or string | 类别阈值为数字分数或 `low`、`medium`、`high` 之一。 |

阻挡性内容护栏和自定义护栏支持 `trigger_action`，它要么立即结束会话，要么重试响应。重试会移除被阻止的回复，将您的反馈作为系统消息注入，并重新生成最多 3 次，之后平台回退到结束会话。反馈模板可以使用 `{{trigger_reason}}` 和 `{{agent_message}}`。

### privacy

使用 `platform_settings.privacy` 控制录制、保留和编辑行为。编辑特定字段为：

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `conversation_history_redaction` | object | 从存储的转录、音频和分析中编辑已配置的实体类型。 |

**conversation_history_redaction：**

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `enabled` | bool | `false` | 是否启用对话历史编辑 |
| `entities` | array | - | 要编辑的实体类型。使用父类型如 `name` 或特定值如 `name.name_given`、`email_address`、`contact_number`、`dob` 和 `age`。 |

### widget

使用 `platform_settings.widget` 配置托管小组件和可分享页面默认值。关于客户端嵌入属性，参见小组件嵌入参考。

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `dismissible` | bool | `false` | 用户是否可以关闭小组件 |
| `show_agent_status` | bool | `false` | 工具运行时是否显示工作中的、完成或错误状态 |
| `show_conversation_id` | bool | `true` | 断开连接后是否显示对话 ID |
| `strip_audio_tags` | bool | `true` | 是否从消息中移除音频标记 |
| `syntax_highlight_theme` | string | 自动 | 代码块语法高亮主题（`light` 或 `dark`）；省略则让小组件自动检测 |

### conversation（在 conversation_config 内）

| 字段 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `max_duration_seconds` | int | `600` | 最大对话时长 |
| `text_only` | bool | `false` | 纯文本模式（避免音频计费） |
| `monitoring_enabled` | bool | `false` | 启用实时 WebSocket 监控 |

## 其他顶级字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `tags` | array | 用于过滤的分类标签（例如 `["production"]`、`["test"]`） |
| `workflow` | object | 对话流定义和工具交互序列 |

## 知识库 / RAG

知识库在 `conversation_config.agent.prompt` 内配置：

```python
agent = client.conversational_ai.agents.create(
    name="支持代理",
    conversation_config={
        "agent": {
            "prompt": {
                "prompt": "你是一个支持代理。使用知识库回答问题。",
                "llm": "gemini-2.0-flash",
                "knowledge_base": [
                    {"type": "file", "id": "doc-id", "name": "产品指南", "usage_mode": "auto"}
                ],
                "rag": {
                    "enabled": True,
                    "embedding_model": "qwen3_embedding_4b",
                    "max_documents_length": 50000,
                    "max_retrieved_rag_chunks_count": 20
                }
            }
        },
        "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb"}
    }
)
```

`rag.embedding_model` 支持 `e5_mistral_7b_instruct`、`multilingual_e5_large_instruct` 和 `qwen3_embedding_4b`。

## CRUD 操作

### 使用 CLI（推荐）

```bash
# 初始化项目
elevenlabs agents init

# 从模板创建代理
elevenlabs agents add "我的代理" --template complete
elevenlabs agents add "支持机器人" --template customer-service

# 列出代理
elevenlabs agents list

# 检查状态
elevenlabs agents status

# 将本地更改推送到平台
elevenlabs agents push
elevenlabs agents push --dry-run    # 先预览更改

# 从平台导入代理
elevenlabs agents pull                      # 导入所有
elevenlabs agents pull --agent <agent-id>   # 导入特定代理
elevenlabs agents pull --update             # 覆盖本地配置

# 查看可用模板
elevenlabs agents templates list
elevenlabs agents templates show <template-name>

# 添加工具
elevenlabs tools add-webhook "API 工具"
elevenlabs tools add-client "UI 工具"

# 生成小组件代码
elevenlabs agents widget <agent-id>
```

### SDK：列出代理

```python
agents = client.conversational_ai.agents.list()
for agent in agents.agents:
    print(f"{agent.name}: {agent.agent_id}")
```

```javascript
const agents = await client.conversationalAi.agents.list();
```

```bash
curl -X GET "https://api.elevenlabs.io/v1/convai/agents" -H "xi-api-key: $ELEVENLABS_API_KEY"
```

### SDK：获取代理

```python
agent = client.conversational_ai.agents.get(agent_id="your-agent-id")
```

```javascript
const agent = await client.conversationalAi.agents.get("your-agent-id");
```

```bash
curl -X GET "https://api.elevenlabs.io/v1/convai/agents/your-agent-id" -H "xi-api-key: $ELEVENLABS_API_KEY"
```

### SDK：更新代理

仅包含要更改的字段。其他所有设置保持不变。

**Python：**
```python
# 更新名称
client.conversational_ai.agents.update(agent_id="id", name="新名称")

# 更新 TTS 音色
client.conversational_ai.agents.update(agent_id="id", conversation_config={
    "tts": {"voice_id": "EXAVITQu4vr4xnSDxMaL", "model_id": "eleven_flash_v2_5"}
})

# 更新提示词/LLM（嵌套在 agent 中）
client.conversational_ai.agents.update(agent_id="id", conversation_config={
    "agent": {"prompt": {"prompt": "新指令。", "llm": "claude-sonnet-4", "temperature": 0.8}}
})

# 更新第一条消息
client.conversational_ai.agents.update(agent_id="id", conversation_config={
    "agent": {"first_message": "欢迎回来！"}
})

# 更新平台设置
client.conversational_ai.agents.update(agent_id="id", platform_settings={
    "auth": {"enable_auth": True, "allowlist": [{"hostname": "myapp.com"}]}
})
```

**JavaScript：**
```javascript
await client.conversationalAi.agents.update("id", { name: "新名称" });
await client.conversationalAi.agents.update("id", {
  conversationConfig: { tts: { voiceId: "EXAVITQu4vr4xnSDxMaL" } }
});
await client.conversationalAi.agents.update("id", {
  conversationConfig: { agent: { prompt: { prompt: "新指令。", llm: "claude-sonnet-4" } } }
});
```

**cURL：**
```bash
curl -X PATCH "https://api.elevenlabs.io/v1/convai/agents/your-agent-id" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"name": "新名称"}'
```

#### 可更新字段

| 部分 | 字段 |
|---------|--------|
| 根级别 | `name`、`tags` |
| `conversation_config.agent` | `first_message`、`language`、`disable_first_message_interruptions`、`dynamic_variables` |
| `conversation_config.agent.prompt` | `prompt`、`llm`、`temperature`、`max_tokens`、`reasoning_effort`、`tools`、`built_in_tools`、`knowledge_base`、`custom_llm`、`timezone` |
| `conversation_config.tts` | `voice_id`、`model_id`、`stability`、`similarity_boost`、`speed`、`optimize_streaming_latency`、`expressive_mode` |
| `conversation_config.asr` | `quality`、`provider`、`keywords`、`user_input_audio_format` |
| `conversation_config.turn` | `turn_timeout`、`turn_eagerness`、`silence_end_call_timeout`、`soft_timeout_config` |
| `conversation_config.conversation` | `max_duration_seconds`、`text_only`、`monitoring_enabled` |
| `platform_settings` | `summary_language`、`guardrails`、`privacy` |
| `platform_settings.widget` | `dismissible`、`show_agent_status`、`show_conversation_id`、`strip_audio_tags`、`syntax_highlight_theme` |
| `platform_settings.auth` | `enable_auth`、`allowlist` |
| `platform_settings.call_limits` | `agent_concurrency_limit`、`daily_limit`、`bursting_enabled` |

### SDK：删除代理

```python
client.conversational_ai.agents.delete(agent_id="your-agent-id")
```

```javascript
await client.conversationalAi.agents.delete("your-agent-id");
```

```bash
curl -X DELETE "https://api.elevenlabs.io/v1/convai/agents/your-agent-id" -H "xi-api-key: $ELEVENLABS_API_KEY"
```

## CI/CD 集成

在部署流水线中使用 CLI：

```bash
# 将 API 密钥设置为环境变量
export ELEVENLABS_API_KEY="your-api-key"

# 推送更改（非交互式）
elevenlabs agents push
```

## 示例配置

### 客户支持代理

```python
agent = client.conversational_ai.agents.create(
    name="支持代理",
    conversation_config={
        "agent": {
            "first_message": "您好！感谢致电 TechCorp 支持。",
            "language": "en",
            "prompt": {
                "prompt": "你是一个客户支持代理。要有帮助、专业、简洁。",
                "llm": "gemini-2.0-flash",
                "temperature": 0.5,
                "built_in_tools": {
                    "end_call": {},
                    "transfer_to_number": {
                        "transfers": [{"transfer_destination": {"type": "phone", "phone_number": "+1234567890"}, "condition": "用户要求人工支持"}]
                    }
                }
            }
        },
        "tts": {"voice_id": "XB0fDUnXU5powFXDhCwa", "model_id": "eleven_flash_v2_5"},
        "turn": {"turn_eagerness": "normal", "turn_timeout": 7},
        "conversation": {"max_duration_seconds": 900}
    }
)
```

### 低延迟助手

```python
agent = client.conversational_ai.agents.create(
    name="快速助手",
    conversation_config={
        "agent": {
            "first_message": "嘿！你需要什么？",
            "prompt": {
                "prompt": "快速高效的助手。简洁的回答。",
                "llm": "gemini-2.0-flash",
                "temperature": 0.3,
                "max_tokens": 100
            }
        },
        "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb", "model_id": "eleven_flash_v2_5", "optimize_streaming_latency": 4},
        "turn": {"turn_eagerness": "eager", "turn_timeout": 3}
    }
)
```
