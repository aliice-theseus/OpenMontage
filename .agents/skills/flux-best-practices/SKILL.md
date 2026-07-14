---
name: flux-best-practices
description: BFL FLUX 图片生成模型综合指南。涵盖提示词编写、T2I、I2I、结构化 JSON、十六进制颜色、排版、多参考编辑以及 FLUX.2 和 FLUX.1 系列的模型特定最佳实践。
metadata:
  author: Black Forest Labs
  version: "1.0.0"
  tags: flux, bfl, image-generation, prompting, t2i, i2i
---

# FLUX 最佳实践

在为任何 BFL FLUX 模型生成提示词时使用此技能，以确保最佳图像质量和准确的提示词解释。

> **扩展参考：** 本目录中的 [`AGENTS.md`](AGENTS.md) 是长篇上游 FLUX 指南（来自 Black Forest Labs）。它是限定于此技能的补充参考资料 — `SKILL.md` 是可加载的入口点和权威来源。它不会覆盖或扩展仓库根目录的 `AGENTS.md` / `AGENT_GUIDE.md`。

## 何时使用

- 为 FLUX.2 或 FLUX.1 模型创建提示词
- 文生图（T2I）生成
- 使用 FLUX.2 模型进行图生图（I2I）编辑
- 使用 JSON 进行结构化场景生成
- 排版和文本渲染
- 多参考风格迁移
- 色彩准确的品牌素材生成

## 快速参考

### 提示词结构公式

```
[主体] + [动作/姿态] + [风格/媒介] + [环境/场景] + [光照] + [相机/技术参数]
```

### 模型选择

| 使用场景         | 推荐模型           | 说明                                      |
| --------------- | ----------------- | ----------------------------------------- |
| 最快生成         | FLUX.2 [klein]    | 4B 或 9B，亚秒级                            |
| 最高质量         | FLUX.2 [max]      | 最佳细节，grounding 搜索                    |
| 生产平衡         | FLUX.2 [pro]      | 质量 + 速度                                |
| 排版/文字        | FLUX.2 [flex]     | 最佳文本渲染                               |
| 本地/开发        | FLUX.2 [dev]      | 开放权重                                   |
| 图片编辑         | FLUX.2 [pro/max]  | 直接将图片 URL 传递给 input_image           |
| 图像修复         | FLUX.1 Fill       | 物体移除/补全                               |
| 上下文编辑       | FLUX.1 Kontext    | 较旧模型，推荐使用 FLUX.2                   |

### 关键规则

1. **无负面提示词** - FLUX 不支持负面提示词；描述你想要的内容
2. **要具体** - 模糊的提示词会产生平庸的结果
3. **使用自然语言** - 散文/叙述风格效果最佳
4. **指定光照** - 光照对质量影响最大
5. **引用文本** - 使用"引号"进行排版渲染
6. **十六进制颜色** - 使用 #RRGGBB 格式配合颜色描述

## 相关

有关 API 集成（端点、轮询、webhooks），请参见 **bfl-api** 技能。

## 规则参考

阅读各个规则文件以获取详细指导：

- [rules/core-principles.md](rules/core-principles.md) - 通用 FLUX 提示词原则
- [rules/flux2-models.md](rules/flux2-models.md) - FLUX.2 系列：klein、max、pro、flex、dev
- [rules/flux1-models.md](rules/flux1-models.md) - FLUX.1 系列：较旧的 FLUX.2 模型 - pro、Kontext、Fill
- [rules/t2i-prompting.md](rules/t2i-prompting.md) - 文生图提示词模式
- [rules/i2i-prompting.md](rules/i2i-prompting.md) - 使用 FLUX.2 进行图生图编辑
- [rules/json-structured-prompting.md](rules/json-structured-prompting.md) - 复杂场景组合
- [rules/hex-color-prompting.md](rules/hex-color-prompting.md) - 精确颜色指定
- [rules/typography-text.md](rules/typography-text.md) - 文本渲染和排版
- [rules/multi-reference-editing.md](rules/multi-reference-editing.md) - 多图片参考
- [rules/negative-prompt-alternatives.md](rules/negative-prompt-alternatives.md) - 正面替代方案
- [rules/model-selection-guide.md](rules/model-selection-guide.md) - 选择适合的模型

## 示例提示词

```
一个 70 多岁饱经风霜的渔夫，满脸深深的皱纹，花白的胡须，
穿着海军蓝绞花毛衣，站在他的木船舵位。
左侧的金色夕阳在他脸上勾勒出戏剧性的轮廓光。
使用哈苏相机配 85mm f/2.8 镜头拍摄，浅景深，
背景中港口的灯光形成柔和散景。柯达 Portra 400 色彩科学。
```
