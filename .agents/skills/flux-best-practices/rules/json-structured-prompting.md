---
name: json-structured-prompting
description: 使用 JSON 格式进行复杂场景组合
---

# JSON 结构化提示词

对于具有多个元素、空间关系或生产自动化的复杂场景，使用 JSON 结构化提示词。

## 何时使用

- 多个具有不同属性的角色
- 精确的空间定位
- 复杂场景构图
- 可重现的、基于模板的提示词
- 程序化提示词生成
- 带有变量替换的生产工作流

## 基本结构

```json
{
  "scene": {
    "setting": "环境描述",
    "time": "时间/时期",
    "mood": "氛围质量"
  },
  "subjects": [
    {
      "type": "人物/物体/动物",
      "description": "详细描述",
      "position": "在画面中的位置",
      "action": "他们在做什么"
    }
  ],
  "style": {
    "medium": "摄影/绘画/插画",
    "technique": "特定风格细节",
    "reference": "艺术家或风格参考"
  },
  "technical": {
    "camera": "相机和镜头",
    "lighting": "灯光设置",
    "composition": "取景细节"
  },
  "colors": ["#hex1", "#hex2"]
}
```

## 单主体示例

```json
{
  "scene": {
    "setting": "带书架的家庭舒适办公室",
    "time": "傍晚",
    "mood": "专注、宁静"
  },
  "subjects": [
    {
      "type": "person",
      "description": "30 多岁女性，深色卷发松散盘起，穿着休闲奶油色毛衣",
      "position": "坐在桌前，画面中央",
      "action": "在笔记本电脑上打字，略带专注的微笑"
    }
  ],
  "style": {
    "medium": "photography",
    "technique": "lifestyle editorial",
    "reference": "kinfolk magazine aesthetic"
  },
  "technical": {
    "camera": "Sony A7III with 50mm f/1.8",
    "lighting": "左侧柔和的自然窗光",
    "composition": "中景，三分法"
  }
}
```

## 多角色场景

```json
{
  "scene": {
    "setting": "维多利亚时代客厅，华丽壁纸和古董家具",
    "time": "夜晚，烛光",
    "mood": "紧张，神秘"
  },
  "subjects": [
    {
      "id": "detective",
      "type": "person",
      "description": "50 多岁高个子男人，棱角分明，鬓角灰白，穿着棕色粗花呢西装",
      "position": "站左中，面向右",
      "action": "用放大镜检查信件，极度专注"
    },
    {
      "id": "lady",
      "type": "person",
      "description": "40 多岁优雅女性，赤褐色头发维多利亚式盘发，翠绿色晚礼服",
      "position": "坐在右侧躺椅上",
      "action": "紧握双手，带着隐藏的焦虑看着侦探"
    },
    {
      "id": "butler",
      "type": "person",
      "description": "年长男性，身着正式管家服，表情坚忍",
      "position": "背景，靠近门口",
      "action": "立正站立，观察"
    }
  ],
  "style": {
    "medium": "oil painting",
    "technique": "classical realism with dramatic lighting",
    "reference": "Victorian narrative painting, John Singer Sargent"
  },
  "technical": {
    "lighting": "温暖烛光为主光，窗外冷色月光为补光",
    "composition": "人物三角排列，侦探在顶点"
  }
}
```

## 带颜色的产品场景

```json
{
  "scene": {
    "setting": "极简产品摄影工作室",
    "mood": "干净、高级、有追求"
  },
  "subjects": [
    {
      "type": "product",
      "description": "充电盒中的时尚无线耳机",
      "position": "居中，略微倾斜",
      "details": "哑光饰面，微妙的品牌标识"
    }
  ],
  "style": {
    "medium": "商业摄影",
    "technique": "高端产品拍摄",
    "reference": "Apple 产品摄影"
  },
  "technical": {
    "camera": "Phase One with 120mm macro",
    "lighting": "上方大型柔光箱，下方微妙补光",
    "composition": "居中，主视觉产品拍摄"
  },
  "colors": {
    "product": "#1A1A2E",
    "accent": "#E94560",
    "background": "#FFFFFF"
  }
}
```

## 将 JSON 转换为自然语言

将 JSON 展平为流畅的散文作为实际提示词：

### 从 JSON
```json
{
  "subjects": [
    {
      "type": "person",
      "description": "双手饱经风霜的老工匠",
      "position": "坐在工作台前",
      "action": "仔细雕刻木头"
    }
  ],
  "scene": { "setting": "传统作坊", "time": "早晨" },
  "technical": { "lighting": "右侧自然窗光" }
}
```

### 转提示词
```
一位双手饱经风霜的老工匠坐在传统作坊的工作台前，
专注而精确地雕刻木头。早晨的自然光从右侧窗户射入，
照亮了散落在磨损表面的木屑和工具。
```

## 模板变量

使用 JSON 结构进行基于模板的生成：

```json
{
  "template": "product_hero",
  "variables": {
    "product_name": "{{PRODUCT_NAME}}",
    "product_color": "{{PRODUCT_COLOR}}",
    "brand_primary": "{{BRAND_HEX_1}}",
    "brand_secondary": "{{BRAND_HEX_2}}",
    "background_style": "{{BG_STYLE}}"
  },
  "prompt_template": "Professional product photography of {{PRODUCT_NAME}} in {{PRODUCT_COLOR}}, brand colors {{BRAND_HEX_1}} and {{BRAND_HEX_2}} accents, {{BG_STYLE}} background, commercial quality"
}
```

## 空间关系

定义明确的空间关系：

```json
{
  "composition": {
    "layout": "triangular",
    "focal_point": "center-left intersection",
    "depth_layers": [
      {
        "layer": "foreground",
        "elements": ["flowers in vase"],
        "focus": "soft blur"
      },
      {
        "layer": "midground",
        "elements": ["main subject"],
        "focus": "sharp"
      },
      {
        "layer": "background",
        "elements": ["window", "garden view"],
        "focus": "soft blur"
      }
    ]
  }
}
```

## 最佳实践

1. **使用 ID 做参考** - 主体交互时给它们分配 ID
2. **关注点分离** - 保持场景、主体、风格和技术参数独立
3. **保持一致性** - 在整个过程中使用相同的术语
4. **包含所有细节** - 不要假设，说明一切
5. **展平后执行** - 在发送给模型前转换为自然语言
6. **版本控制模板** - 跟踪模板版本以确保可重现性
