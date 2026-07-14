---
name: setup-api-key
description: 引导用户完成 ElevenLabs API 密钥的设置，用于 ElevenLabs MCP 工具。当用户需要配置 ElevenLabs API 密钥、ElevenLabs 工具因缺少 API 密钥而失败，或用户提及需要访问 ElevenLabs 时使用。首先检查 ELEVENLABS_API_KEY 是否已配置且有效，仅在需要时运行完整设置。
license: MIT
compatibility: 需要互联网访问 elevenlabs.io 和 api.elevenlabs.io。
---

# ElevenLabs API 密钥设置

引导用户获取和配置 ElevenLabs API 密钥。

## 工作流

### 步骤 0：首先检查现有 API 密钥

在向用户索要密钥之前，检查现有的 `ELEVENLABS_API_KEY`：

1. 检查 `ELEVENLABS_API_KEY` 是否存在于当前环境中。
2. 如果环境中没有，检查 `.env` 中是否有 `ELEVENLABS_API_KEY=<value>`。
3. 如果找到现有密钥，**验证它**：
   ```
   GET https://api.elevenlabs.io/v1/user
   Header: xi-api-key: <existing-api-key>
   ```
4. **如果现有密钥验证成功：**
   - 告诉用户 ElevenLabs 已经配置并可正常工作
   - 跳过设置流程
   - 询问他们是否要替换/轮换密钥；如果不需要，停止
5. **如果现有密钥验证失败：**
   - 告诉用户现有密钥似乎无效或已过期
   - 继续到步骤 1

### 步骤 1：请求 API 密钥

告诉用户：

> 要设置 ElevenLabs，打开 API 密钥页面：https://elevenlabs.io/app/settings/api-keys
>
> （需要账户？先在 https://elevenlabs.io/app/sign-up 创建一个）
>
> 如果你还没有 API 密钥：
> 1. 点击"Create key"
> 2. 给它命名（或使用默认名称）
> 3. 为你的密钥设置权限。如果你提供的密钥"User"权限设置为"Read"，此技能会自动验证你的密钥是否有效
> 4. 点击"Create key"确认
> 5. **立即复制密钥** — 它只显示一次！
>
> 准备好后将你的 API 密钥粘贴在这里。

然后等待用户的下一条消息，该消息应包含 API 密钥。

### 步骤 2：验证和配置

一旦用户提供 API 密钥：

1. **验证密钥** 通过发起请求：
   ```
   GET https://api.elevenlabs.io/v1/user
   Header: xi-api-key: <the-api-key>
   ```

2. **如果验证失败：**
   - 告诉用户 API 密钥似乎无效
   - 请他们再试一次
   - 提醒他们 URL：https://elevenlabs.io/app/settings/api-keys
   - 如果第二次仍失败，显示错误并退出

3. **如果验证成功**，将 API 密钥保存到 `.env` 文件中：
   ```
   ELEVENLABS_API_KEY=<the-api-key>
   ```
   - 如果 `.env` 已有 `ELEVENLABS_API_KEY=...`，替换该行
   - 否则为 `ELEVENLABS_API_KEY` 添加新行

4. **确认成功：**
   > 完成！你的密钥已作为环境变量存储在 .env 中
   > 保管好密钥！不要与任何人分享！
