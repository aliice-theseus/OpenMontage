---
name: bfl-api
description: BFL FLUX API integration guide covering endpoints, async polling patterns, rate limiting, error handling, webhooks, and regional endpoints with Python and TypeScript code examples.
metadata:
  author: Black Forest Labs
  version: "1.0.0"
  tags: flux, bfl, api, integration, webhooks, rate-limiting
---

# BFL API 集成指南

在将 BFL FLUX API 集成到应用程序中用于图像生成、编辑和处理时使用此技能。

## 首先：检查 API 密钥

**在生成图像之前，请验证您的 API 密钥已设置：**

```bash
echo $BFL_API_KEY
```

如果为空或看到"未认证"错误，请参阅下方的 [API 密钥设置](#api-key-setup)。

## 重要提示：图像 URL 10 分钟后过期

API 返回的结果 URL 是临时的。生成完成后请立即下载图像——不要存储或缓存 URL 本身。

## 使用场景

- 设置 BFL API 客户端
- 实现异步轮询模式
- 处理速率限制和错误
- 为生产环境配置 webhook
- 选择区域端点
- 构建生产级集成

## 快速参考

### 基础端点

| 区域 | 端点 | 用途 |
| ------ | ----------------------- | --------------------------- |
| 全球 | `https://api.bfl.ai` | 默认，自动故障转移 |
| 欧盟 | `https://api.eu.bfl.ai` | GDPR 合规 |
| 美国 | `https://api.us.bfl.ai` | 美国数据驻留 |

### 模型端点与定价

> **积分定价：** 1 积分 = 0.01 美元。FLUX.2 使用基于百万像素的定价（成本随分辨率增加而增加）。

#### FLUX.2 模型

| 模型 | 路径 | 首 MP | +MP | 1MP T2I | 1MP I2I | 最适合 |
| ----------------- | --------------------- | ------ | ---- | ------- | ------- | ---------------------------------- |
| FLUX.2 [klein] 4B | `/v1/flux-2-klein-4b` | 1.4c | 0.1c | $0.014 | $0.015 | 实时、高容量 |
| FLUX.2 [klein] 9B | `/v1/flux-2-klein-9b` | 1.5c | 0.2c | $0.015 | $0.017 | 质量/速度平衡 |
| FLUX.2 [pro] | `/v1/flux-2-pro` | 3c | 1.5c | $0.03 | $0.045 | 生产环境，快速周转 |
| FLUX.2 [max] | `/v1/flux-2-max` | 7c | 3c | $0.07 | $0.10 | 最高质量 |
| FLUX.2 [flex] | `/v1/flux-2-flex` | 5c | 5c | $0.05 | $0.10 | 排版，可调控制 |
| FLUX.2 [dev] | - | - | - | 免费 | 免费 | 本地开发（非商业） |

> **定价公式：** `(firstMP + (outputMP-1) * mpPrice) + (inputMP * mpPrice)` 单位：美分

#### FLUX.1 模型

| 模型 | 路径 | 每张图像价格 | 最适合 |
| -------------------- | ------------------------ | ----------- | ----------------------------- |
| FLUX.1 Kontext [pro] | `/v1/flux-kontext` | $0.04 | 带上下文的图像编辑 |
| FLUX.1 Kontext [max] | `/v1/flux-kontext-max` | $0.08 | 最高质量编辑 |
| FLUX1.1 [pro] | `/v1/flux-pro-1.1` | $0.04 | 标准 T2I，快速可靠 |
| FLUX1.1 [pro] Ultra | `/v1/flux-pro-1.1-ultra` | $0.06 | 超高分辨率 |
| FLUX1.1 [pro] Raw | `/v1/flux-pro-1.1-raw` | $0.06 | 自然摄影感 |
| FLUX.1 Fill [pro] | `/v1/flux-pro-1.0-fill` | $0.05 | 内补绘制 |

> **提示：** 所有 FLUX.2 模型都通过 `input_image` 参数支持图像编辑——无需单独的编辑端点。使用 [bfl.ai/pricing](https://bfl.ai/pricing) 计算器查看不同分辨率的精确成本。

### 图像编辑输入

**推荐：直接使用 URL** - 比 base64 更简单方便。

**单图像编辑：**

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "将背景改为日落",
    "input_image": "https://example.com/photo.jpg"
  }'
```

**多参考编辑：**

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "图片 1 中的人物出现在图片 2 的环境中",
    "input_image": "https://example.com/person.jpg",
    "input_image_2": "https://example.com/background.jpg"
  }'
```

API 会自动获取 URL。URL 和 base64 均可使用，但推荐在可用时使用 URL。

### 多参考 I2I

FLUX.2 模型支持多张输入图像，用于组合元素、风格迁移和角色一致性：

| 模型 | 最大参考数 |
| --------------------- | -------------- |
| FLUX.2 [klein] | 4 张图像 |
| FLUX.2 [pro/max/flex] | 8 张图像 |

**参数：** `input_image`、`input_image_2`、`input_image_3`、... `input_image_8`

**提示词模式：** 在提示词中按编号引用图像：

- "图片 1 中的主体在图片 2 的环境中"
- "将图片 2 的风格应用到图片 1 的场景中"
- "图片 1 中的人穿着图片 2 的服装，摆出图片 3 的姿势"

> 关于详细的多参考模式（角色一致性、风格迁移、姿势引导），请参见 `flux-best-practices/rules/multi-reference-editing.md`

### 速率限制

| 层级 | 并发请求数 |
| ------------------------- | ------------------- |
| 标准（大多数端点） | 24 |

### 轮询 vs Webhook

| 方式 | 何时使用 |
| ------------ | ------------------------------------------------------------------------------------ |
| **轮询** | 脚本、CLI 工具、本地开发、单次请求、简单集成 |
| **Webhook** | 生产应用、高容量、服务器到服务器、需要即时通知时 |

**从轮询开始**——它更简单且适用于任何场景。当需要扩展或希望使用事件驱动架构时切换到 webhook。

### 关键行为

- **轮询**：响应中包含 `polling_url` 用于异步结果
- **URL 过期**：结果 URL 在 10 分钟后过期
- **Webhook 支持**：为生产工作负载配置 `webhook_url`

## API 密钥设置

**必需**：使用 API 前必须设置 `BFL_API_KEY` 环境变量。

### 快速检查

```bash
echo $BFL_API_KEY
```

### 如果未设置

1. **获取密钥**：访问 https://dashboard.bfl.ai/get-started → 点击 **"创建密钥"** → 选择组织
2. **保存到 `.env`**（推荐持久化）：
   ```bash
   echo 'BFL_API_KEY=bfl_your_key_here' >> .env
   echo '.env' >> .gitignore  # 不要提交密钥
   ```

详细设置说明参见 [references/api-key-setup.md](references/api-key-setup.md)。

## 认证

```bash
x-key: YOUR_API_KEY
```

## 基本请求流程

```
1. POST 请求到模型端点
   └─> 响应：{ "polling_url": "..." }

2. GET polling_url（重复直到完成）
   └─> 响应：{ "status": "Pending" | "Ready" | "Error", ... }

3. 状态为 Ready 时，下载结果 URL
   └─> URL 在 10 分钟后过期——请立即下载
```

## 相关

- **提示词最佳实践**（T2I、I2I、排版、颜色）：请参阅 **flux-best-practices** 技能
- **多参考模式**（角色一致性、风格迁移、姿势引导）：请参阅 `flux-best-practices/rules/multi-reference-editing.md`

## 参考

- [references/api-key-setup.md](references/api-key-setup.md) - **API 密钥创建与配置**
- [references/endpoints.md](references/endpoints.md) - 完整端点文档
- [references/polling-patterns.md](references/polling-patterns.md) - 异步轮询实现
- [references/rate-limiting.md](references/rate-limiting.md) - 速率限制处理策略
- [references/error-handling.md](references/error-handling.md) - 错误码与恢复
- [references/webhook-integration.md](references/webhook-integration.md) - Webhook 设置与安全

### 代码示例

> **注意：** 默认推荐使用 cURL 示例，因为它们无需 Python 或 Node.js 即可通用。在构建生产应用时使用语言特定客户端。

- [references/code-examples/curl-examples.sh](references/code-examples/curl-examples.sh) - **cURL 示例（推荐）**
- [references/code-examples/python-client.py](references/code-examples/python-client.py) - Python 客户端
- [references/code-examples/typescript-client.ts](references/code-examples/typescript-client.ts) - TypeScript 客户端

## 快速开始示例

### 1. 提交生成请求

```bash
curl -s -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "日落时分宁静的山景", "width": 1024, "height": 1024}'
```

响应：

```json
{ "id": "abc123", "polling_url": "https://api.bfl.ai/v1/get_result?id=abc123" }
```

### 2. 轮询结果

```bash
curl -s "POLLING_URL" -H "x-key: $BFL_API_KEY"
```

就绪时的响应：

```json
{ "status": "Ready", "result": { "sample": "https://...", "seed": 1234 } }
```

### 3. 下载图像

```bash
curl -s -o output.png "IMAGE_URL"
```

> **提示：** 结果 URL 在 10 分钟后过期。状态变为 `Ready` 后请立即下载。

### 4. 多参考示例

组合来自多张图像的元素：

```bash
curl -s -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "图片 1 中的猫坐在图片 2 的舒适房间里",
    "input_image": "https://example.com/cat.jpg",
    "input_image_2": "https://example.com/room.jpg",
    "width": 1024,
    "height": 1024
  }'
```

在提示词中按编号引用图像。参见[多参考 I2I](#multi-reference-i2i)了解限制和模式。
