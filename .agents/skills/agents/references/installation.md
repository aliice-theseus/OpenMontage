# 安装

## CLI（推荐）

ElevenLabs CLI 是创建和管理代理的推荐方式：

```bash
npm install -g @elevenlabs/cli
# 或
pnpm add -g @elevenlabs/cli
# 或
yarn global add @elevenlabs/cli
```

需要 Node.js 16.0.0 或更高版本。

### 身份验证

```bash
elevenlabs auth login          # 使用 API 密钥进行身份验证
elevenlabs auth whoami         # 验证当前登录状态
elevenlabs auth logout         # 移除存储的凭据
```

API 密钥安全存储在 `~/.agents/api_keys.json` 中。

### 快速入门

```bash
# 初始化新项目
elevenlabs agents init

# 从模板创建代理
elevenlabs agents add "My Assistant" --template complete

# 推送到 ElevenLabs 平台
elevenlabs agents push
```

## JavaScript / TypeScript SDK

用于程序化访问和客户端集成：

```bash
npm install @elevenlabs/elevenlabs-js
```

> **重要：** 始终使用 `@elevenlabs/elevenlabs-js`。旧的 `elevenlabs` npm 包（v1.x）已弃用，不应再使用。

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

// 选项 1：环境变量（推荐）
// 在环境中设置 ELEVENLABS_API_KEY
const client = new ElevenLabsClient();

// 选项 2：直接传递
const client = new ElevenLabsClient({ apiKey: "your-api-key" });
```

### 从已弃用的包迁移

如果安装了旧包，请移除它们：

```bash
# 移除已弃用的包
npm uninstall elevenlabs

# 安装当前包
npm install @elevenlabs/elevenlabs-js

# 对于客户端/浏览器使用，还需安装：
npm install @elevenlabs/client  # 浏览器客户端
npm install @elevenlabs/react   # React hooks
```

**导入变更：**
```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { Conversation } from "@elevenlabs/client";
import { useConversation } from "@elevenlabs/react";
```

## Python

```bash
pip install elevenlabs
```

```python
from elevenlabs import ElevenLabs

# 选项 1：环境变量（推荐）
# 在环境中设置 ELEVENLABS_API_KEY
client = ElevenLabs()

# 选项 2：直接传递
client = ElevenLabs(api_key="your-api-key")
```

## cURL / REST API

将 API 密钥设置为环境变量：

```bash
export ELEVENLABS_API_KEY="your-api-key"
```

通过 `xi-api-key` 头在请求中包含：

```bash
curl -X POST "https://api.elevenlabs.io/v1/convai/agents/create" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Agent", "conversation_config": {"agent": {"prompt": {"prompt": "You are helpful.", "llm": "gemini-2.0-flash"}}, "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb"}}}'
```

## 获取 API 密钥

1. 在 [elevenlabs.io](https://elevenlabs.io) 注册
2. 前往 [API Keys](https://elevenlabs.io/app/settings/api-keys)
3. 点击 **Create API Key**
4. 复制并安全存储

或使用 `setup-api-key` 技能进行引导式设置。

## 环境变量

| 变量                | 描述                             |
|---------------------|----------------------------------|
| `ELEVENLABS_API_KEY` | 您的 ElevenLabs API 密钥（必需） |
