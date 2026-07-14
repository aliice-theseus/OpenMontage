---
name: api-key-setup
description: 如何获取和配置 BFL API 密钥
---

# API 密钥设置

> **重要：** 在尝试图像生成之前，请始终验证您的 API 密钥。密钥缺失或无效会导致"Not authenticated"错误。

## 快速验证

首先运行以下命令检查密钥是否已配置且有效：

```bash
# 检查密钥是否已设置
[ -z "$BFL_API_KEY" ] && echo "Error: BFL_API_KEY not set" || echo "OK: Key configured"
```

如果未设置，请按照以下步骤操作。

## 获取密钥

1. 前往 **https://dashboard.bfl.ai/get-started**
2. 点击 **"Create Key"**
3. 选择组织（如果有多个选项，请询问用户）
4. 复制密钥（以 `bfl_` 开头）

## 对于直接进行 API 调用的代理

当当前会话中未设置 `BFL_API_KEY` 时：

1. **检查现有的 `.env`**：
   ```bash
   grep BFL_API_KEY .env 2>/dev/null
   ```

2. **如果找到，导出它**：
   ```bash
   export BFL_API_KEY=$(grep BFL_API_KEY .env | cut -d '=' -f2)
   ```

3. **如果未找到，向用户询问**密钥：
   > "我需要一个 BFL API 密钥来生成图像。请：
   > 1. 前往 https://dashboard.bfl.ai/get-started
   > 2. 点击 'Create Key' 并复制它
   > 3. 在此粘贴"

4. **保存并导出**：
   ```bash
   echo 'BFL_API_KEY=bfl_provided_key' >> .env
   echo '.env' >> .gitignore
   export BFL_API_KEY=bfl_provided_key
   ```

现在 `$BFL_API_KEY` 可用于会话中的直接 curl/API 调用。
