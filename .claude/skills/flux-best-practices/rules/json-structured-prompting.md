---
name: json-structured-prompting
description: 使用 JSON 格式进行复杂场景构图
---

# JSON 结构化提示

对于包含多个元素、空间关系或生产自动化的复杂场景，使用 JSON 结构化提示。

## 使用时机

- 多个角色具有不同属性
- 精确的空间定位
- 复杂场景构图
- 可重现的、基于模板的提示
- 程序化提示生成
- 带变量替换的生产工作流

## 基本结构

```json
{
  "scene": {
    "setting": "环境描述",
    "time": "一天中的时间/时期",
    "mood": "氛围质量"
  },
  "subjects": [
    {
      "type": "person/object/animal",
      "description": "详细描述",
      "position": "在画面中的位置",
      "action": "他们在做什么"
    }
  ],
  "style": {
    "medium": "摄影/绘画/插画",
    "technique": "具体风格细节",
    "reference": "艺术家或风格参考"
  },
  "technical": {
    "camera": "相机和镜头",
    "lighting": "灯光设置",
    "composition": "构图细节"
  },
  "colors": ["#hex1", "#hex2"]
}
```

## 单主体示例

```json
{
  "scene": {
    "setting": "带书架的家庭办公室",
    "time": "傍晚",
    "mood": "专注、宁静"
  },
  "subjects": [
    {
      "type": "person",
      "description": "30 多岁女性，深色卷发松散地扎成发髻，穿着休闲米色毛衣",
      "position": "坐在书桌前，画面中央",
      "action": "在笔记本电脑上打字，专注的浅笑"
    }
  ],
  "style": {
    "medium": "摄影",
    "technique": "生活方式编辑",
    "reference": "Kinfolk 杂志美学"
  },
  "technical": {
    "camera": "索尼 A7III 配 50mm f/1.8",
    "lighting": "左侧柔和的自然窗光",
    "composition": "中景，三分法"
  }
}
```

## 多角色场景

```json
{
  "scene": {
    "setting": "维多利亚时代客厅，带有华丽壁纸和古董家具",
    "time": "傍晚，烛光",
    "mood": "紧张、神秘"
  },
  "subjects": [
    {
      "id": "detective",
      "type": "person",
      "description": "50 多岁高个子男性，五官锐利，鬓角灰白，穿着棕色粗花呢西装",
      "position": "站在左中位置，面朝右",
      "action": "用放大镜检查一封信，专注投入"
    },
    {
      "id": "lady",
      "type": "person",
      "description": "40 多岁优雅女性，赤褐色头发盘成维多利亚式发髻，翠绿色晚礼服",
      "position": "坐在右侧躺椅上",
      "action": "紧张地观察侦探，紧握双手"
    },
    {
      "id": "butler",
      "type": "person",
      "description": "老年男性，穿着正式管家制服，表情坚忍",
      "position": "背景，靠近门口",
      "action": "立正站立，观察着"
    }
  ],
  "style": {
    "medium": "油画",
    "technique": "古典写实主义，戏剧性光线",
    "reference": "维多利亚叙事绘画，John Singer Sargent"
  },
  "technical": {
    "lighting": "温暖烛光为主光，透过窗户的冷月光为补光",
    "composition": "人物呈三角形排列，侦探在顶点"
  }
}
```

## 带颜色的产品场景

```json
{
  "scene": {
    "setting": "极简主义产品摄影工作室",
    "mood": "干净、高端、令人向往"
  },
  "subjects": [
    {
      "type": "product",
      "description": "充电盒中的时尚无线耳机",
      "position": "居中，略微倾斜",
      "details": "哑光表面，微妙的品牌标识"
    }
  ],
  "style": {
    "medium": "商业摄影",
    "technique": "高端产品拍摄",
    "reference": "Apple 产品摄影"
  },
  "technical": {
    "camera": "Phase One 配 120mm 微距镜头",
    "lighting": "上方大型柔光箱，下方微妙补光",
    "composition": "居中，主打产品拍摄"
  },
  "colors": {
    "product": "#1A1A2E",
    "accent": "#E94560",
    "background": "#FFFFFF"
  }
}
```

## 将 JSON 转换为自然语言

将 JSON 展平为流畅的散文作为实际提示：

### 从 JSON
```json
{
  "subjects": [
    {
      "type": "person",
      "description": "双手粗糙的老工匠",
      "position": "坐在工作台前",
      "action": "仔细雕刻木头"
    }
  ],
  "scene": { "setting": "传统工坊", "time": "早晨" },
  "technical": { "lighting": "来自右侧的自然窗光" }
}
```

### 转换为提示
```
一位双手粗糙的老工匠坐在他传统工坊的工作台前，
专注而精确地雕刻着木头。
早晨的自然光从右侧窗户流入，
照亮了散落在磨损表面上木屑和工具。
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
  "prompt_template": "{{PRODUCT_NAME}}（{{PRODUCT_COLOR}}色）的专业产品摄影，品牌色 {{BRAND_HEX_1}} 和 {{BRAND_HEX_2}} 装饰，{{BG_STYLE}} 背景，商业品质"
}
```

## 空间关系

定义清晰的空间关系：

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

1. **为引用使用 ID** - 主体交互时给它们分配 ID
2. **分离关注点** - 保持场景、主体、风格和技术参数分离
3. **保持一致** - 全程使用相同的术语
4. **包含所有细节** - 不要假设，指定一切
5. **展平以执行** - 在发送给模型前转换为自然语言
6. **版本化模板** - 跟踪模板版本以实现可重现性
