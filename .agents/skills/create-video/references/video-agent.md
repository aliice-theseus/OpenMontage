---
name: video-agent
description: 使用 HeyGen Video Agent API 进行一次性提示视频生成
---

# Video Agent API

Video Agent API 从单个文本提示生成完整视频。与需要逐场景详细配置的标准视频生成 API 不同，Video Agent 自动处理脚本编写、虚拟形象选择、视觉、配音、节奏和字幕。

## MCP 工具（首选）

如果 HeyGen MCP 服务器已连接，使用 `mcp__heygen__generate_video_agent` 代替直接 API 调用：

```
工具：mcp__heygen__generate_video_agent
参数：
  prompt: "<来自 prompt-optimizer.md 的优化提示>"
  config:
    duration_sec: 90          # 可选，5-300
    avatar_id: "avatar_id"    # 可选，省略时代理选择
    orientation: "landscape"   # 可选，"landscape" 或 "portrait"
  files:                       # 可选
    - asset_id: "uploaded_asset_id"
```

然后使用返回的 `video_id` 通过 `mcp__heygen__get_video` 检查状态。

提示质量仍然是关键因素——无论你使用 MCP 还是直接 API，始终遵循 [prompt-optimizer.md](prompt-optimizer.md)。

## 何时使用 Video Agent vs 标准 API

| 用例 | 推荐 API |
|----------|-----------------|
| 从想法快速制作视频 | Video Agent |
| 精确控制场景、虚拟形象、时间 | 标准 v2/video/generate |
| 规模化自动内容生成 | Video Agent |
| 特定虚拟形象配合精确脚本 | 标准 v2/video/generate |
| 原型或草稿视频 | Video Agent |
| 品牌一致的生产视频 | 标准 v2/video/generate |

## 在调用此 API 之前

**必需步骤：** 在生成视频前使用 [prompt-optimizer.md](prompt-optimizer.md) 优化提示。平庸和专业结果之间的区别完全取决于提示质量。

快速清单：
1. 定义视觉风格（颜色、美学）——参见 [visual-styles.md](visual-styles.md)
2. 使用特定场景类型构建场景
3. 以约 150 词/分钟编写配音脚本
4. 为每个场景指定媒体类型（运动图形、素材、AI 生成）

## 直接 API 端点

```
POST https://api.heygen.com/v1/video_agent/generate
```

## 请求字段

| 字段 | 类型 | 必需 | 描述 |
|-------|------|:---:|-------------|
| `prompt` | string | ✓ | 描述所需视频的文本提示 |
| `config` | object | | 配置选项（见下文） |
| `files` | array | | 要在生成中引用的资源文件 |
| `callback_id` | string | | 用于跟踪的自定义 ID。**同时需要设置 `callback_url`** — 如果不需要 webhook，两者都省略 |
| `callback_url` | string | | 用于完成通知的 Webhook URL |

### Config 对象

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `duration_sec` | integer | 大致时长（秒），5-300 |
| `avatar_id` | string | 要使用的特定虚拟形象（可选——未提供时由代理选择） |
| `orientation` | string | `"portrait"` 或 `"landscape"` |

### Files 数组

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `asset_id` | string | 要引用的已上传文件的资产 ID |

## 响应格式

```json
{
  "error": null,
  "data": {
    "video_id": "abc123"
  }
}
```

## curl 示例

```bash
curl -X POST "https://api.heygen.com/v1/video_agent/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "为新的 AI 驱动日历应用创建一个 60 秒的产品演示视频。语气应专业但友好，面向忙碌的专业人士。突出智能日程安排功能和时区处理。"
  }'
```

## 示例

### 基础：仅提示

```typescript
const videoId = await generateWithVideoAgent(
  "为科技初创公司的新员工创建一个 30 秒的欢迎视频。保持活力和现代感。"
);
```

### 带时长和方向

```typescript
const videoId = await generateWithVideoAgent(
  "解释云计算对小型企业的好处。使用简单语言和现实世界的例子。",
  {
    duration_sec: 90,
    orientation: "landscape"
  }
);
```

### 带特定虚拟形象

```typescript
const videoId = await generateWithVideoAgent(
  "展示季度销售业绩。专业语气，数据聚焦。",
  {
    duration_sec: 120,
    avatar_id: "josh_lite3_20230714",
    orientation: "landscape"
  }
);
```

## 编写有效提示

参见 **[prompt-optimizer.md](prompt-optimizer.md)** 获取全面的提示编写指导。

提示优化器涵盖：
- 提示复杂度级别（基础 → 逐场景）
- 视觉风格分类和颜色指定
- 媒体类型选择（运动图形 vs 素材 vs AI 生成）
- 场景结构和时间计算
- 常见视频类型的即用模板

## 检查视频状态

Video Agent 返回一个 `video_id`——使用标准状态端点检查进度：

```typescript
// 与标准视频生成相同的轮询
const videoUrl = await waitForVideo(videoId);
```

参见 [video-status.md](video-status.md) 了解轮询实现。

## 限制

- 对精确脚本措辞的控制较少
- 如果未指定，虚拟形象选择可能变化
- 场景合成是自动化的
- 可能不符合精确的品牌指南
- 时长是近似值，不是精确值

## 最佳实践

1. **在提示中具体说明** - 更多细节 = 更好的结果
2. **指定时长** - 使用 `config.duration_sec` 控制长度
3. **如果需要，锁定虚拟形象** - 使用 `config.avatar_id` 保持一致性
4. **上传参考文件** - 帮助代理理解你的品牌/产品
5. **迭代提示** - 根据结果优化
6. **用于草稿** - Video Agent 非常适合在最终生产前快速迭代
