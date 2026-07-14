---
name: flux-best-practices
description: BFL FLUX 图像生成模型的综合指南。涵盖提示工程、T2I、I2I、结构化 JSON、十六进制颜色、排版、多参考编辑以及 FLUX.2 和 FLUX.1 系列的模型特定最佳实践。
metadata:
  author: Black Forest Labs
  version: "1.0.0"
  tags: flux, bfl, image-generation, prompting, t2i, i2i
---

# FLUX 最佳实践

在为任何 BFL FLUX 模型生成提示时使用本技能，以确保最佳的图像质量和准确的提示理解。

> **扩展参考：** 本目录中的 [`AGENTS.md`](AGENTS.md) 是完整版上游 FLUX 指南（来自 Black Forest Labs）。它是本技能范围内的补充参考材料——`SKILL.md` 是可加载的入口点和权威文件。它不会覆盖或扩展仓库根目录的 `AGENTS.md` / `AGENT_GUIDE.md`。

## 使用时机

- 为 FLUX.2 或 FLUX.1 模型创建提示
- 文生图（T2I）生成
- 使用 FLUX.2 模型进行图生图（I2I）编辑
- 使用 JSON 进行结构化场景生成
- 排版和文本渲染
- 多参考风格迁移
- 色彩精确的品牌生成

## 快速参考

### 提示结构公式

```
[主体] + [动作/姿势] + [风格/媒介] + [环境/场景] + [光照] + [相机/技术参数]
```

### 模型选择

| 使用场景            | 推荐模型          | 备注                                  |
| ------------------- | ----------------- | -------------------------------------- |
| 最快生成            | FLUX.2 [klein]    | 4B 或 9B，亚秒级                       |
| 最高质量            | FLUX.2 [max]      | 最佳细节，支持实况搜索                 |
| 生产平衡            | FLUX.2 [pro]      | 质量 + 速度                            |
| 排版/文本           | FLUX.2 [flex]     | 最佳文本渲染                           |
| 本地/开发           | FLUX.2 [dev]      | 开放权重                               |
| 图像编辑            | FLUX.2 [pro/max]  | 直接将图像 URL 传递给 input_image      |
| 内补绘制            | FLUX.1 Fill       | 物体移除/区域补全                      |
| 上下文编辑          | FLUX.1 Kontext    | 旧版模型，推荐使用 FLUX.2              |

### 关键规则

1. **无负面提示** - FLUX 不支持负面提示；描述你想要的内容
2. **具体明确** - 模糊的提示会产生平庸的结果
3. **使用自然语言** - 散文/叙事风格效果最佳
4. **指定光照** - 光照对质量影响最大
5. **引号包裹文本** - 使用"引号文本"进行排版渲染
6. **十六进制颜色** - 使用 #RRGGBB 格式并附带颜色描述

## 相关

关于 API 集成（端点、轮询、Webhook），请参见 **bfl-api** 技能。

## 规则参考

阅读各规则文件以获取详细指导：

- [rules/core-principles.md](rules/core-principles.md) - 通用 FLUX 提示原则
- [rules/flux2-models.md](rules/flux2-models.md) - FLUX.2 系列：klein, max, pro, flex, dev
- [rules/flux1-models.md](rules/flux1-models.md) - FLUX.1 系列：FLUX.2 的上一代模型 - pro, Kontext, Fill
- [rules/t2i-prompting.md](rules/t2i-prompting.md) - 文生图提示模式
- [rules/i2i-prompting.md](rules/i2i-prompting.md) - 使用 FLUX.2 进行图生图编辑
- [rules/json-structured-prompting.md](rules/json-structured-prompting.md) - 复杂场景构图
- [rules/hex-color-prompting.md](rules/hex-color-prompting.md) - 精确颜色指定
- [rules/typography-text.md](rules/typography-text.md) - 文本渲染和排版
- [rules/multi-reference-editing.md](rules/multi-reference-editing.md) - 多图像参考
- [rules/negative-prompt-alternatives.md](rules/negative-prompt-alternatives.md) - 正面替代方案
- [rules/model-selection-guide.md](rules/model-selection-guide.md) - 选择合适的模型

## 示例提示

```
一位饱经风霜的 70 多岁渔民，满脸深皱纹，胡须花白，
身穿海军蓝针织毛衣，站在他的木船舵旁。
左侧金色黄昏的阳光在他的侧影上形成戏剧性的轮廓光。
使用哈苏相机配 85mm f/2.8 镜头拍摄，浅景深，背景中
港口灯光形成柔和的散景。柯达 Portra 400 色彩科学。
```
