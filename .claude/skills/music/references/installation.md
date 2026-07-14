# 安装

## JavaScript / TypeScript

```bash
npm install @elevenlabs/elevenlabs-js
```

> **重要提示：** 始终使用 `@elevenlabs/elevenlabs-js`。旧的 `elevenlabs` npm 包（v1.x）已弃用，不应再使用。

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

// 选项 1：环境变量（推荐）
// 在环境中设置 ELEVENLABS_API_KEY
const client = new ElevenLabsClient();

// 选项 2：直接传入
const client = new ElevenLabsClient({ apiKey: "your-api-key" });
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

# 选项 2：直接传入
client = ElevenLabs(api_key="your-api-key")
```

## cURL / REST API

将 API 密钥设置为环境变量：

```bash
export ELEVENLABS_API_KEY="your-api-key"
```

通过 `xi-api-key` 头包含在请求中：

```bash
curl -X POST "https://api.elevenlabs.io/v1/music" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A chill lo-fi beat", "music_length_ms": 30000}'
```

## 获取 API 密钥

1. 在 [elevenlabs.io](https://elevenlabs.io) 注册
2. 前往 [API Keys](https://elevenlabs.io/app/settings/api-keys)
3. 点击 **Create API Key**
4. 复制并安全存储

或使用 `setup-api-key` 技能进行引导式设置。

**注意：** 音乐生成需要 ElevenLabs 付费计划。
