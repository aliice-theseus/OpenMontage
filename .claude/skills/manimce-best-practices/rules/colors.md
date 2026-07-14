---
name: colors
description: 颜色常量、渐变和 Manim 中的颜色操作
metadata:
  tags: color, colors, gradient, rgb, hex, palette
---

# Manim 中的颜色

Manim 提供预定义的颜色常量并支持自定义颜色。

## 颜色常量

### 主要颜色
```python
RED, GREEN, BLUE
YELLOW, ORANGE, PINK, PURPLE
WHITE, BLACK, GREY (或 GRAY)
```

### 颜色变体（色阶）
大多数颜色有从 `_A`（最浅）到 `_E`（最深）的变体：
```python
BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E
RED_A, RED_B, RED_C, RED_D, RED_E
GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E
GREY_A, GREY_B, GREY_C, GREY_D, GREY_E
```

### 常用命名颜色
```python
TEAL, TEAL_A, TEAL_B, TEAL_C, TEAL_D, TEAL_E
GOLD, GOLD_A, GOLD_B, GOLD_C, GOLD_D, GOLD_E
MAROON, MAROON_A, MAROON_B, MAROON_C, MAROON_D, MAROON_E
PURPLE, PURPLE_A, PURPLE_B, PURPLE_C, PURPLE_D, PURPLE_E
```

### 特殊颜色
```python
PURE_RED, PURE_GREEN, PURE_BLUE  # RGB 三原色
LIGHT_GREY, DARK_GREY
LIGHTER_GREY, DARKER_GREY
LIGHT_BROWN, DARK_BROWN
```

## 使用颜色

### 创建时设置颜色
```python
circle = Circle(color=RED)
square = Square(color=BLUE, fill_color=GREEN, fill_opacity=0.5)
text = Text("你好", color=YELLOW)
```

### 创建后设置颜色
```python
circle = Circle()
circle.set_color(RED)
```

## 十六进制颜色

```python
# 使用十六进制字符串
circle = Circle(color="#FF5733")
square = Square(color="#2ECC71")

# RGB 值（0-1 范围）
from manim import rgb_to_color
custom = rgb_to_color([0.5, 0.2, 0.8])
```

## 填充 vs 描边颜色

```python
square = Square()
square.set_fill(RED, opacity=0.8)      # 内部颜色
square.set_stroke(BLUE, width=4)       # 边框颜色
```

### 组合样式
```python
square = Square(
    color=BLUE,            # 同时设置填充和描边
    fill_opacity=0.5,      # 填充透明度
    stroke_width=4         # 边框厚度
)
```

## 渐变

### Mobject 上的颜色渐变
```python
text = Text("渐变")
text.set_color_by_gradient(RED, YELLOW, GREEN)
```

### 沿路径渐变
```python
line = Line(LEFT * 3, RIGHT * 3)
line.set_color_by_gradient(BLUE, GREEN, YELLOW)
```

## 颜色插值

在两个颜色之间创建颜色：

```python
from manim import interpolate_color

# 获取 RED 和 BLUE 中间的颜色
mid_color = interpolate_color(RED, BLUE, 0.5)

# 创建一系列颜色
colors = [interpolate_color(RED, BLUE, alpha) for alpha in np.linspace(0, 1, 10)]
```

## ManimColor 类

高级颜色操作，直接使用 ManimColor：

```python
from manim import ManimColor

# 从各种格式创建
color1 = ManimColor("#FF0000")           # 从十六进制
color2 = ManimColor((0.0, 1.0, 0.5))     # 从 RGB 浮点数（0-1）
color3 = ManimColor([255, 165, 0])       # 从 RGB 整数（0-255）

# 颜色操作方法
lighter = color1.lighter()               # 变浅版本
darker = color1.darker()                 # 变深版本
inverted = color1.invert()               # 反转颜色
with_alpha = color1.opacity(0.5)         # 50% 不透明度

# 格式转换
hex_str = color1.to_hex()                # 转十六进制字符串
rgb = color1.to_rgb()                    # 转 RGB 浮点数数组
hsv = color1.to_hsv()                    # 转 HSV 数组

# 插值
mixed = color1.interpolate(color2, 0.5)  # 混合两种颜色
```

## 不透明度

```python
# 设置不透明度（0 = 透明，1 = 不透明）
circle = Circle(fill_opacity=0.5, stroke_opacity=0.8)

# 修改不透明度
circle.set_opacity(0.5)         # 填充和描边同时
circle.set_fill_opacity(0.7)    # 仅填充
circle.set_stroke_opacity(0.3)  # 仅描边
```

## 按值着色

基于值对 mobject 着色（用于数据可视化）：

```python
class ColorByValue(Scene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(10)]).arrange(RIGHT)

        for i, dot in enumerate(dots):
            # 从蓝色（冷）到红色（热）着色
            dot.set_color(interpolate_color(BLUE, RED, i / 9))

        self.add(dots)
```

## 随机颜色

```python
from manim import random_color, random_bright_color

circle = Circle(color=random_color())
square = Square(color=random_bright_color())
```

## 用于动画的颜色列表

```python
class ColorCycle(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)

        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        for color in colors:
            self.play(circle.animate.set_color(color), run_time=0.5)
```

## 最佳实践

1. **使用颜色变体增加层次感** —— `BLUE_E` 用于阴影，`BLUE_A` 用于高亮
2. **保持颜色一致性** —— 相关概念使用相同颜色
3. **使用不透明度实现分层** —— 半透明填充展示重叠部分
4. **考虑色盲可访问性** —— 避免仅用红绿区分
5. **谨慎使用渐变** —— 过多会分散注意力
