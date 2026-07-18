# OpenMontage 图像提供商使用指南

> 如何在图像生成和素材提供商之间选择，以及如何有效使用每个提供商。
> 补充现有的 `image-gen-usage.md`（深度介绍 FLUX 提示词）。

## 提供商概览

### 生成提供商（AI 创建图像）

| 工具 | 提供商 | 费用 | 速度 | 最适合 |
|------|--------|------|------|--------|
| `flux_image` | FLUX 2 Pro 通过 fal.ai | 约$0.03-0.05 | 约5-10秒 | 照片级真实感，通用用途，主力 |
| `grok_image` | Grok Imagine Image (xAI) | $0.02/输出 + $0.002/输入编辑图像 | 约5-15秒 | 图像编辑、风格迁移、多图像合成 |
| `openai_image` | GPT Image 1 (OpenAI) | 约$0.01-0.17 | 约5-15秒 | 复杂指令、图像中的文字、多元素 |
| `recraft_image` | Recraft V4 通过 fal.ai | 约$0.04-0.25 | 约5-10秒 | Logo、SVG矢量、品牌资产、文字渲染（见下方注意事项） |
| `local_diffusion` | FLUX.1-schnell（本地默认） | 免费 | 取决于 GPU | 视频流程默认文生图、离线、隐私、LoRA |
| `image_gen` | 多（旧版，已弃用） | 不等 | 不等 | **已弃用** — 使用 `image_selector` 或按提供商工具 |

### 素材提供商（搜索和下载现有图像）

| 工具 | 提供商 | 费用 | 速度 | 最适合 |
|------|--------|------|------|--------|
| `pexels_image` | Pexels | 免费 | 约2-5秒 | 高质量摄影、颜色筛选 |
| `pixabay_image` | Pixabay | 免费 | 约2-5秒 | 大型库、分类筛选、插图 |

### 选择器

| 工具 | 用途 |
|------|------|
| `image_selector` | 根据偏好和可用性路由到最佳可用提供商 |

## 按场景类型的提供商选择

| 场景类型 | 主要提供商 | 原因 | 回退 |
|----------|-----------|------|------|
| **真实照片**（城市、自然、人物） | `pexels_image` | 真实的照片 > AI 的真实感 | `pixabay_image` → `flux_image` |
| **技术图表** | `diagram_gen` | 结构化、可编辑 | `flux_image` 配图表提示 |
| **抽象/概念插图** | `local_diffusion`（FLUX） | 视频流程统一默认、风格一致、支持 LoRA | 用户批准后可改用 `flux_image` |
| **现有图像的风格迁移/重绘** | `grok_image` | 原生编辑流程，强大的可提示变换 | `openai_image` |
| **多图像合并/合成** | `grok_image` | 可将多个源图像合成为一个场景 | `openai_image` |
| **Logo 或品牌资产** | `recraft_image` | SVG 支持，文字准确性 | `openai_image` |
| **带文字/标签的图像** | `openai_image` | 最佳文字渲染（GPT Image 1） | `recraft_image` |
| **复杂多元素构图** | `openai_image` | 最佳指令遵循 | `flux_image` |
| **主视觉图像（关键视觉）** | `local_diffusion`（FLUX） | 视频流程统一默认、可复现 | 用户批准后可改用其他提供商 |
| **缩略图** | `local_diffusion`（FLUX） | 与视频主视觉保持一致 | 用户批准后可改用其他提供商 |
| **预算/免费项目** | `pexels_image` 或 `pixabay_image` | 免费、即时 | `local_diffusion` |
| **离线/无网络** | `local_diffusion` | 无需网络 | — |

## 提供商特定注意事项

### Recraft V4 通过 fal.ai
- **`style` 参数会导致 422 错误**（截至2026年4月）。`style` 枚举值（`digital_illustration`、`realistic_image` 等）被 fal.ai 的 Recraft V4 端点拒绝。**解决方法：** 改为在提示文本中编码风格方向（例如，"牙齿横截面的数字插图"而非 `style="digital_illustration"`）。`image_size` 和 `colors` 参数正常工作。
- **精确商业名称的文字渲染不可靠。** Recraft（如所有 AI 图像模型）可能生成错误的文字。对于文字必须逐字准确（行动号召屏幕、商业名称、电话号码）的任何场景，使用 Remotion `text_card` 而非生成带文字的图像。

## 费用-质量权衡

```
生产路径：高级
├── 主视觉图像：local_diffusion / FLUX ($0.00/图)
├── 辅助视觉：local_diffusion / FLUX ($0.00/图)
├── 精确文字叠加：Remotion 原生文字 ($0.00)
├── B-roll 静态图：pexels_image ($0.00)
└── 10张图像 API 成本：$0.00

生产路径：标准
├── 全部生成：local_diffusion / FLUX ($0.00/图)
├── B-roll 静态图：pexels_image ($0.00)
└── 10张图像 API 成本：$0.00

生产路径：预算
├── 全部素材：pexels_image + pixabay_image ($0.00)
├── 图表：diagram_gen ($0.00)
└── 总计：$0.00

生产路径：离线
├── 全部生成：local_diffusion ($0.00)
├── 图表：diagram_gen ($0.00)
└── 总计：$0.00（但更慢、质量更低）
```

当任务从现有图像开始并应仅路由到支持编辑的提供商时，使用 `generation_mode="edit"`。

## 使用图像选择器

大多数视频文生图调用使用 `image_selector`；未指定提供商时会默认路由到本地 FLUX：

```python
# 选择器找到最佳可用提供商
result = image_selector.execute({
    "prompt": "现代化数据中心鸟瞰图",
    "preferred_provider": "local_diffusion",
    "output_path": "assets/images/scene-3.png"
})
```

省略 `preferred_provider` 时，纯文生图同样默认使用 `local_diffusion`。只有用户明确批准其他生成提供商时才覆盖。图库搜索应明确指定 `pexels` / `pixabay`，图像编辑和自定义 ComfyUI 工作流按能力自动路由。
使用 `allowed_providers` 限制为免费或本地选项：

```python
# 预算模式：仅免费提供商
result = image_selector.execute({
    "prompt": "服务器机房内部",
    "allowed_providers": ["pexels", "pixabay", "local_diffusion"],
    "output_path": "assets/images/scene-3.jpg"
})
```

## 跨混合源的一致性

在同一视频中混合素材和生成的图像时，视觉一致性是挑战。

### 策略：统一调色
在合成阶段将剧本调色 LUT 应用于素材和生成的图像。
这统一了外观。`color_grade` 增强工具处理此问题。

### 策略：匹配视觉身份，而非复制前缀
生成图像时，将剧本的情绪、调色板、纹理和媒介
调整为简短的场景特定锚点。搜索素材时，筛选相同的
情感和视觉品质：颜色、光照、环境、构图、时代
和纹理。将剧本作为一致性来源，而非要粘贴的脚本。

### 策略：避免在同一场景中混合风格
不要在同一个场景中对一个元素使用素材照片而对另一个元素使用 AI 插图。
保持每个场景内部一致 — 全部素材或全部生成。
