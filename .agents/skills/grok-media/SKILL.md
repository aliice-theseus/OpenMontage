---
name: grok-media
description: xAI Grok 图像和视频生成指南，涵盖认证、端点、提示词结构、图像编辑、参考图像视频和异步轮询。
metadata:
  author: OpenMontage
  version: "1.0.0"
  tags: xai, grok, image-generation, video-generation, media
---

# Grok Media

在 OpenMontage 中使用 xAI 媒体模型时使用此技能。

## 模型

- `grok-imagine-image` 用于图像生成和图像编辑
- `grok-imagine-video` 用于文字转视频、图像转视频和参考图像视频

## 认证

- 环境变量：`XAI_API_KEY`
- 基础 URL：`https://api.x.ai/v1`
- 请求头：`Authorization: Bearer $XAI_API_KEY`

## 图像 API

### 文字转图像

- 端点：`POST /images/generations`
- 核心字段：
  - `model`
  - `prompt`
  - `n`
  - `aspect_ratio`
  - `resolution`

### 图像编辑

- 端点：`POST /images/edits`
- 单张源图像使用 `image`
- 多图像合成使用 `images`
- 每张源图像可以是：
  - 一个公开的 HTTPS URL
  - 一个 base64 数据 URI

### 图像提示词

- Grok 对直接的自然语言响应良好
- 对于编辑，仅描述预期的变化，其余内容隐式保留
- 对于多图像合并，明确说明每张源图像的贡献方式
- 优先使用一个强大的场景描述，而非冗长的风格堆叠

## 视频 API

### 生成

- 端点：`POST /videos/generations`
- 轮询端点：`GET /videos/{request_id}`
- 成功状态：`status == "done"`
- 需显式处理的失败状态：`failed`、`expired`

### 模式

- 文字转视频：
  - 仅提示词生成
- 图像转视频：
  - 使用 `image: {"url": ...}`
  - 这将锚定起始帧
- 参考转视频：
  - 使用 `reference_images: [{"url": ...}, ...]`
  - 这会影响视频中出现的人物/内容，而不锁定第一帧
  - 提示词可以使用占位符 `<IMAGE_1>`、`<IMAGE_2>` 引用输入

### 视频约束

- Grok 视频最适合作为短格式生成
- 当前输出分辨率为 `480p` 和 `720p`
- 参考图像视频支持多张图像，适用于产品植入、服装迁移和身份一致性
- 及时下载输出；提供商 URL 可能是临时的

## 定价

- `grok-imagine-image`：每张生成图像 `$0.02`
- `grok-imagine-image` 编辑/合成：每张输入图像追加 `$0.002`
- `grok-imagine-video`：
  - `480p`：每秒 `$0.05`
  - `720p`：每秒 `$0.07`
- `grok-imagine-video` 图像条件请求：每张输入图像追加 `$0.002`

## Grok 特有提示词指导

### 图像

- 以主体、动作、场景开头
- 添加一个风格锚点，而不是五个
- 对于编辑：
  - 描述期望的修改
  - 通过省略而非编写冗长的保留列表来保持图像其他部分稳定

### 视频

- 保持提示词场景本地化：一个镜头、一个主要运动思路、一个情感节拍
- 对于参考条件视频，明确地将源图像映射到角色：
  - 来自 `<IMAGE_1>` 的人物
  - 来自 `<IMAGE_2>` 的外套
  - 来自 `<IMAGE_3>` 的产品
- 镜头和节奏语言有帮助：
  - slow push-in（慢推）
  - handheld follow（手持跟拍）
  - locked-off medium shot（固定中景）
  - high-energy whip pan transition（高能量快速摇摄转场）

## 适合场景

- 图像风格迁移
- 多源图像合成
- 参考条件短视频
- 产品导向的动态片段
- 角色一致场景（无需硬锁定第一帧）

## 不适合场景

- 长格式片段生成
- 高度依赖确定性种子
- 包含多个场景变化的过度复杂提示词

## 故障处理

- 如果生成提交成功但轮询超时，将其作为提供商/运行时问题展示
- 如果请求失败，在错误信息中保留端点、模式和提示词摘要
- 在未获用户批准的情况下，不要在选定 xAI 后静默地替换为其他提供商
