---
name: api-key-setup
description: How to obtain and configure a BFL API key
---

# API 密钥设置

> **重要：** 在尝试生成图像之前，请务必验证您的 API 密钥。缺少或无效的密钥会导致"未认证"错误。

## 快速验证

首先运行以下命令检查密钥是否已配置且有效：

```bash
# 检查密钥是否已设置
[ -z "$BFL_API_KEY" ] && echo "错误：BFL_API_KEY 未设置" || echo "正常：密钥已配置"
```

如果未设置，请按照以下步骤操作。

## 获取密钥

1. 访问 **https://dashboard.bfl.ai/get-started**
2. 点击 **"创建密钥"**
3. 选择组织（如果有多个选项，请询问用户）
4. 复制密钥（以 `bfl_` 开头）

## 供进行直接 API 调用的代理使用

当当前会话中未设置 `BFL_API_KEY` 时：

1. **检查是否已存在 `.env`**：
   ```bash
   grep BFL_API_KEY .env 2>/dev/null
   ```

2. **如果找到，导出它**：
   ```bash
   export BFL_API_KEY=$(grep BFL_API_KEY .env | cut -d '=' -f2)
   ```

3. **如果未找到，询问用户**提供密钥：
   > "我需要一个 BFL API 密钥来生成图像。请：
   > 1. 访问 https://dashboard.bfl.ai/get-started
   > 2. 点击'创建密钥'并复制
   > 3. 粘贴到这里"

4. **保存并导出**：
   ```bash
   echo 'BFL_API_KEY=bfl_provided_key' >> .env
   echo '.env' >> .gitignore
   export BFL_API_KEY=bfl_provided_key
   ```

现在 `$BFL_API_KEY` 可在会话中用于直接 curl/API 调用。
