# Grok 提示指南

当选择的提供商是 `grok_image` 或 `grok_video` 时使用此指南。

## 何时选择 Grok

- 需要编辑现有图像而非从头生成
- 需要将多个源图像合并为一个输出
- 需要受参考图像影响的短视频，但不锁定第一帧
- 想要一个提供商同时用于图像和视频生成，提示语言相似

## Grok 图像

### 最佳提示结构

```
[主体] + [动作或变化] + [环境] + [一个风格锚点] + [光照]
```

### 编辑提示

对于图像编辑，直接描述预期的变换：

- "Render this as a pencil sketch with detailed shading."
- "Replace the plain t-shirt with a dark green bomber jacket."
- "Combine these two people into the same sunny park scene."

除非保留至关重要，否则不要过度指定每个未改变的细节。

### 多图像合成

告诉 Grok 如何组合输入：

- 谁来自哪个源
- 什么应该保持分开
- 最终场景发生在哪里

示例：

```
Place the person from image 1 and the person from image 2 on the same subway platform at dusk,
standing shoulder to shoulder, cinematic sodium-vapor lighting, realistic photography.
```

## Grok 视频

### 最佳提示结构

```
[镜头] + [相机运动] + [主体] + [主要运动节拍] + [环境] + [光照] + [基调]
```

### 参考图像视频

Grok 支持使用类似 `<IMAGE_1>` 的占位符引用源图像的提示。当需要身份、服装或产品一致性时使用。

示例：

```
Medium full shot, slow push-in. The model from <IMAGE_1> walks onto a clean white runway wearing
the jacket from <IMAGE_2>. Soft studio lighting, premium fashion campaign, confident expression.
```

### 图生视频 vs 参考生视频

- 源图像应作为开场帧时，使用图生视频。
- 源图像应影响内容但不冻结构图时，使用参考生视频。

## 常见错误

- 将 Grok 参考图像视为严格的故事板。它们是影响输入，而非精确帧锁定。
- 在一个片段请求中写入多个场景变化。
- 将太多风格标签与过少的场景信息结合。
- 使用模糊的编辑提示如"make it better"而非命名变化。

## OpenMontage 指导

- 对于图像编辑或合成，优先选择 `grok_image` 而非选择器的默认主力工具。
- 对于参考条件视频，当简报依赖于从输入图像中携带人物、服装或产品进入运动时，优先选择 `grok_video`。
- 如果交付物是无参考约束的纯电影运动，在锁定提供商前比较 Grok 与 Runway、Veo 和 Kling。
