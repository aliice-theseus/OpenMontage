---
name: setup-api-key
description: 指导用户设置 ElevenLabs API 密钥以使用 ElevenLabs MCP 工具。在用户需要配置 ElevenLabs API 密钥、ElevenLabs 工具因缺少 API 密钥而失败、或用户提到需要访问 ElevenLabs 时使用。首先检查 ELEVENLABS_API_KEY 是否已配置且有效，仅在需要时执行完整设置。
license: MIT
compatibility: 需要访问 elevenlabs.io 和 api.elevenlabs.io 的互联网连接。
---

# ElevenLabs API 密钥设置

指导用户获取和配置 ElevenLabs API 密钥。

## 工作流

### 步骤 0：首先检查现有的 API 密钥

在向用户索要密钥之前，检查是否已存在 `ELEVENLABS_API_KEY`：

1. 检查当前环境中是否存在 `ELEVENLABS_API_KEY`。
2. 如果不在环境中，检查 `.env` 中是否有 `ELEVENLABS_API_KEY=<value>`。
3. 如果找到现有密钥，**验证它**：
   ```
   GET https://api.elevenlabs.io/v1/user
   头: xi-api-key: <现有-api-key>
   ```
4. **如果现有密钥验证成功：**
   - 告诉用户 ElevenLabs 已配置并可正常使用
   - 跳过设置流程
   - 询问是否要更换/轮换密钥；如果不需要，则停止
5. **如果现有密钥验证失败：**
   - 告诉用户现有密钥似乎无效或已过期
   - 继续到步骤 1

### 步骤 1：请求 API 密钥

告诉用户：

> 要设置 ElevenLabs，请打开 API 密钥页面：https://elevenlabs.io/app/settings/api-keys
>
> （需要一个账号？先在 https://elevenlabs.io/app/sign-up 创建一个）
>
> 如果你还没有 API 密钥：
> 1. 点击"创建密钥"
> 2. 命名它（或使用默认名称）
> 3. 为你的密钥设置权限。如果你提供的密钥"用户"权限设置为"读取"，本技能会自动验证你的密钥是否有效
> 4. 点击"创建密钥"确认
> 5. **立即复制密钥** - 仅显示一次！
>
> 准备好后在此粘贴你的 API 密钥。

然后等待用户的下一条消息，其中应包含 API 密钥。

### 步骤 2：验证和配置

用户提供 API 密钥后：

1. **验证密钥** 通过发起请求：
   ```
   GET https://api.elevenlabs.io/v1/user
   头: xi-api-key: <api-key>
   ```

2. **如果验证失败：**
   - 告诉用户 API 密钥似乎无效
   - 请他们重试
   - 提醒他们 URL：https://elevenlabs.io/app/settings/api-keys
   - 如果再次失败，显示错误并退出

3. **如果验证成功**，将 API 密钥保存到 `.env` 文件中：
   ```
   ELEVENLABS_API_KEY=<api-key>
   ```
   - 如果 `.env` 已有 `ELEVENLABS_API_KEY=...`，替换该行
   - 否则为 `ELEVENLABS_API_KEY` 添加新行

4. **确认成功：**
   > 完成！你的密钥已作为环境变量存储在 .env 中
   > 请保管好密钥！不要与任何人分享！
