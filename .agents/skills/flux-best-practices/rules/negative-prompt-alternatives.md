---
name: negative-prompt-alternatives
description: 负面提示词的正面替代方案
---

# 负面提示词替代方案

FLUX 不支持负面提示词。本指南为常见的负面提示词模式提供正面替代方案。

## 为什么没有负面提示词？

负面提示词实际上可能使模型更关注不需要的元素。相反，精确描述你**确实想要**的内容 — 这能提供更清晰的指导和更好的结果。

## 替换策略

对于任何不需要的元素：
1. 识别你不想要什么
2. 问："那里应该有什么？"
3. 描述正面替代方案

## 常见替换

### 人物/人群

| 不要说                     | 改用                          |
|---------------------------|-------------------------------|
| "no people"               | "empty"、"deserted"、"solitary"、"abandoned" |
| "no crowds"               | "quiet"、"peaceful"、"secluded"、"private" |
| "without background people" | "isolated subject"、"clean background"、"solo figure" |

**示例：**
```
差：海滩场景，没有人
好：黎明时分的空无一人的海滩，原始未触碰的沙子，孤独的海鸥
```

### 皮肤/外观

| 不要说               | 改用                               |
|---------------------|-----------------------------------|
| "no makeup"         | "natural skin"、"bare face"、"fresh-faced" |
| "no blemishes"      | "clear skin"、"smooth complexion"、"healthy glow" |
| "no wrinkles"       | "youthful skin"、"smooth features" |

**示例：**
```
差：女性肖像，不化妆，没有瑕疵
好：自然清透肌肤的女性肖像，容光焕发，健康光泽
```

### 配饰

| 不要说               | 改用                                     |
|---------------------|------------------------------------------|
| "no glasses"        | "visible eyes"、"unobstructed gaze"、"clear eye contact" |
| "no hat"            | "bare head"、"visible hair"、"uncovered head" |
| "no jewelry"        | "minimal accessories"、"understated"、"unadorned" |

**示例：**
```
差：男性肖像，不戴眼镜，不戴帽子
好：目光清澈直接的男性肖像，风中可见的发丝
```

### 颜色

| 不要说               | 改用                                         |
|---------------------|----------------------------------------------|
| "no color"          | "monochrome"、"black and white"、"grayscale" |
| "not colorful"      | "muted tones"、"subdued palette"、"desaturated" |
| "no bright colors"  | "neutral tones"、"earth tones"、"soft pastels" |

**示例：**
```
差：风景照，没有鲜艳颜色
好：柔和大地色调的风景，柔和的晨光，低饱和调色板
```

### 文字/水印

| 不要说               | 改用                                   |
|---------------------|----------------------------------------|
| "no text"           | "clean surfaces"、"unmarked"、"text-free" |
| "no watermark"      | "pristine image"、"clean composition" |
| "no logos"          | "unbranded"、"plain"、"logo-free surface" |

**示例：**
```
差：产品照，没有水印，没有文字
好：干净的产品摄影，原始无标记表面，极简无品牌设计
```

### 风格/时代

| 不要说               | 改用                                           |
|---------------------|------------------------------------------------|
| "not modern"        | "traditional"、"classical"、"vintage"、"historical" |
| "no CGI look"       | "photorealistic"、"authentic"、"natural"、"organic" |
| "not cartoonish"    | "realistic"、"lifelike"、"naturalistic" |

**示例：**
```
差：建筑设计，不现代，没有未来感元素
好：传统维多利亚式建筑，古典华丽细节，时代精准特征
```

### 质量/伪影

| 不要说               | 改用                                        |
|---------------------|---------------------------------------------|
| "no blur"           | "sharp focus"、"crisp details"、"tack-sharp" |
| "no noise"          | "clean image"、"smooth gradients"、"low ISO" |
| "no artifacts"      | "pristine quality"、"clean render"、"flawless" |

**示例：**
```
差：肖像，没有模糊，没有噪点
好：极致锐利的肖像，原始图像质量，平滑肤色，清晰细节
```

### 物体

| 不要说               | 改用                                         |
|---------------------|----------------------------------------------|
| "no cars"           | "pedestrian area"、"car-free zone"、"walking street" |
| "no buildings"      | "open landscape"、"natural scenery"、"wilderness" |
| "no furniture"      | "empty room"、"bare space"、"minimalist interior" |

**示例：**
```
差：街景，没有汽车，没有现代建筑
好：历史悠久的鹅卵石步行街，两旁是 19 世纪的传统石砌建筑
```

### 天气/环境

| 不要说               | 改用                                               |
|---------------------|----------------------------------------------------|
| "no rain"           | "clear sky"、"dry weather"、"sunny day"            |
| "no clouds"         | "clear blue sky"、"cloudless"、"perfect visibility" |
| "not dark"          | "well-lit"、"bright"、"daylight"、"illuminated"    |

**示例：**
```
差：户外肖像，没有雨，没有云，不暗
好：晴朗蓝天下的户外肖像，明亮阳光明媚的日子，完美的自然光线
```

### 构图

| 不要说               | 改用                                               |
|---------------------|----------------------------------------------------|
| "no distractions"   | "clean composition"、"focused framing"、"minimal elements" |
| "nothing in background" | "solid background"、"isolated subject"、"clean backdrop" |
| "no clutter"        | "organized"、"tidy"、"minimal"、"streamlined" |

**示例：**
```
差：产品照，没有干扰，背景什么都没有
好：产品在干净的白色无缝背景上，孤立主体，极简聚焦构图
```

## 复杂替换示例

### 原负面提示词重的提示
```
女性肖像，不戴眼镜，不化妆，没有皱纹，没有瑕疵，
没有鲜艳颜色，没有分散注意力的背景，没有刺眼的光线
```

### 正面改写
```
年轻女性的肖像，自然清透的肌肤，明亮的眼睛，
容光焕发，健康光泽，穿着柔和的大地色系，
柔和模糊的中性背景，轻柔漫射光形成柔和阴影
```

### 原负面提示词重的提示
```
风景照，没有人，没有建筑，没有电线杆，没有现代元素，
没有阴天，没有枯树
```

### 正面改写
```
原始的自然荒野景观，郁郁葱葱的绿色森林，清澈的蓝天，
未触及的自然风光延伸至地平线，只有鸟鸣和风声的宁静孤独，
金色阳光透过健康的树叶洒落
```

## 快速参考卡

| 不想要的     | 正面替代方案                    |
|------------|-------------------------------|
| 没有人     | Empty, solitary, deserted     |
| 不化妆     | Natural, fresh-faced, bare    |
| 没有文字   | Clean, unmarked, pristine     |
| 没有模糊   | Sharp, crisp, tack-sharp      |
| 不现代     | Traditional, vintage, classical |
| 不暗       | Bright, well-lit, luminous    |
| 不杂乱     | Minimal, clean, focused       |
| 不人工     | Natural, organic, authentic   |
