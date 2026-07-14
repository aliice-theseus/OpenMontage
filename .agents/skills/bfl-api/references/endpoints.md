---
name: endpoints
description: BFL API 完整端点文档
---

# BFL API 端点

所有 BFL FLUX API 端点的完整参考。

## 基础 URL

| 区域 | 端点 | 用途 |
|------|------|------|
| 全局 | `https://api.bfl.ai` | 默认，自动故障转移 |
| 欧盟 | `https://api.eu.bfl.ai` | GDPR 合规，欧盟数据驻留 |
| 美国 | `https://api.us.bfl.ai` | 美国数据驻留 |

**建议：** 除非有特定区域要求，否则使用全局端点（`api.bfl.ai`）。

## 认证

所有请求都需要在 `x-key` 头中提供 API 密钥：

```bash
x-key: YOUR_API_KEY
```

## FLUX.2 文本到图像和图像到图像端点

### FLUX.2 [klein] 4B

```
POST /v1/flux-2-klein-4b
```

最快生成，4B 参数。

### FLUX.2 [klein] 9B

```
POST /v1/flux-2-klein-9b
```

快速生成，质量更好，9B 参数。

### FLUX.2 [max]

```
POST /v1/flux-2-max
```

最高质量，支持基础搜索。

### FLUX.2 [pro]

```
POST /v1/flux-2-pro
```

生产环境平衡质量和速度。

### FLUX.2 [flex]

```
POST /v1/flux-2-flex
```

排版优化，可调节步数/引导尺度。

## FLUX.1 端点

### FLUX1.1 [pro]

```
POST /v1/flux-pro-1.1
```

文本到图像生成。

### FLUX.1 Kontext

```
POST /v1/flux-kontext
```

### FLUX.1 Kontext Max

```
POST /v1/flux-kontext-max
```

### FLUX.1 Fill

```
POST /v1/flux-fill
```

修复填充和物体移除——使用 FLUX.2 模型并通过特定提示风格可以实现修复填充和物体移除，性能更佳。

## 通用请求参数

### 文本到图像 (T2I)

| 参数                | 类型    | 必需 | 描述                                      |
| ------------------- | ------- | ---- | ----------------------------------------- |
| `prompt`            | string  | 是   | 文本描述（最多 32K tokens）                |
| `width`             | integer | 否   | 图像宽度（16 的倍数，最大 4MP 总面积）     |
| `height`            | integer | 否   | 图像高度（16 的倍数，最大 4MP 总面积）     |
| `seed`              | integer | 否   | 随机种子，用于可重现结果                  |
| `safety_tolerance`  | integer | 否   | 0（严格）到 5（宽松），默认 2              |
| `output_format`     | string  | 否   | "jpeg" 或 "png"，默认 "jpeg"               |
| `webhook_url`       | string  | 否   | 用于异步通知的 URL                        |
| `webhook_secret`    | string  | 否   | 用于 webhook 签名的密钥                    |

### 图像到图像 (I2I)

> **重要：** 所有 FLUX.2 模型（klein、pro、max、flex）都通过 `input_image` 参数支持图像到图像编辑。推荐使用 FLUX.2 而非 FLUX.1 Kontext 进行编辑。

> **推荐：直接使用 URL** - API 自动获取 URL，比下载并编码为 base64 更简单方便。URL 和 base64 都可用，但推荐在可用时使用 URL。

| 参数                               | 类型    | 必需 | 描述                                              |
| ---------------------------------- | ------- | ---- | ------------------------------------------------- |
| `prompt`                           | string  | 是   | 编辑指令                                          |
| `input_image`                      | string  | 是   | **URL（推荐）** 或 base64 - API 自动获取 URL      |
| `input_image_2` - `input_image_8`  | string  | 否   | 额外的参考 URL 或 base64                          |
| `width`                            | integer | 否   | 输出宽度                                          |
| `height`                           | integer | 否   | 输出高度                                          |

### FLUX.2 [flex] 专有

| 参数      | 类型    | 默认值 | 描述                     |
| --------- | ------- | ------ | ------------------------ |
| `steps`   | integer | 50     | 推理步数（1-50）         |
| `guidance`| float   | 4.5    | 引导尺度（1.5-10）       |

## 分辨率约束

- **最小：** 64x64 像素
- **最大：** 4MP 总面积（宽度 x 高度）
- **倍数：** 16（两个维度）

### 常用分辨率

| 宽高比         | 分辨率      | 百万像素  |
| -------------- | ----------- | --------- |
| 1:1（正方形）  | 1024x1024   | 1.05 MP   |
| 16:9（宽屏）   | 1920x1080   | 2.07 MP   |
| 9:16（竖屏）   | 1080x1920   | 2.07 MP   |
| 4:3（经典）    | 1536x1152   | 1.77 MP   |
| 2:1（全景）    | 2048x1024   | 2.10 MP   |

## 示例请求

### 基本 T2I 请求

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A serene mountain landscape at golden hour",
    "width": 1024,
    "height": 1024
  }'
```

### 响应

```json
{
  "id": "gen_abc123xyz",
  "polling_url": "https://api.bfl.ai/v1/get_result?id=gen_abc123xyz"
}
```

### 带所有选项的 T2I

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-max" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Professional headshot of a business executive",
    "width": 1024,
    "height": 1280,
    "seed": 42,
    "safety_tolerance": 2,
    "output_format": "png",
    "webhook_url": "https://your-server.com/webhook",
    "webhook_secret": "your-secret-key"
  }'
```

### I2I 请求（FLUX.2 - 推荐）

使用任何 FLUX.2 模型通过直接传递源图像 URL 来编辑图像：

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-klein-9b" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Change the floor color to light blue",
    "input_image": "https://example.com/room-photo.jpg"
  }'
```

如需更高质量的编辑，请使用 FLUX.2 [pro] 或 [max]：

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Change the background to a beach sunset",
    "input_image": "https://example.com/portrait.jpg"
  }'
```

### 多参考 I2I (FLUX.2)

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-max" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Person from image 1 wearing outfit from image 2 in setting from image 3",
    "input_image": "https://example.com/person.jpg",
    "input_image_2": "https://example.com/outfit.jpg",
    "input_image_3": "https://example.com/location.jpg"
  }'
```

### FLUX.2 [flex] 带自定义步数

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-flex" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A poster with text \"SUMMER SALE\" in bold typography",
    "steps": 50,
    "guidance": 7.0
  }'
```

## 轮询端点

### 获取结果

```
GET /v1/get_result?id={generation_id}
```

### 响应状态

```json
// 处理中
{ "status": "Pending" }

// 就绪
{
  "status": "Ready",
  "result": {
    "sample": "https://bfldeliveryprod.blob.core.windows.net/results/...",
    "prompt": "...",
    "seed": 1234567890
  }
}

// 错误
{
  "status": "Error",
  "error": "Error description"
}
```

## 错误响应

| 状态码 | 含义           | 操作               |
| ------ | -------------- | ------------------ |
| 400    | 错误请求       | 检查参数           |
| 401    | 未授权         | 验证 API 密钥      |
| 402    | 需要付款       | 添加积分           |
| 429    | 请求过多       | 实施退避策略       |
| 500    | 服务器错误     | 带退避重试         |
