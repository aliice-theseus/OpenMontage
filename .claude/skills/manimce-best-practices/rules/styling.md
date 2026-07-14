---
name: styling
description: 填充、描边、不透明度和 mobject 的视觉样式
metadata:
  tags: fill, stroke, opacity, style, width, appearance
---

# Mobject 样式

使用填充、描边和不透明度设置控制 mobject 的视觉外观。

## 填充属性

填充控制形状的内部区域。

```python
from manim import *

class FillExample(Scene):
    def construct(self):
        # 创建时设置填充
        circle = Circle(fill_color=BLUE, fill_opacity=0.8)

        # 创建后设置填充
        square = Square()
        square.set_fill(RED, opacity=0.5)

        self.add(circle, square)
```

### 填充方法
```python
mobject.set_fill(color=RED)                    # 仅颜色
mobject.set_fill(RED, opacity=0.5)             # 颜色和不透明度
mobject.set_fill(opacity=0.5)                  # 仅不透明度
mobject.set_fill_color(RED)                    # 仅颜色（替代写法）
mobject.set_fill_opacity(0.5)                  # 仅不透明度（替代写法）
```

## 描边属性

描边控制形状的轮廓/边框。

```python
class StrokeExample(Scene):
    def construct(self):
        # 创建时设置描边
        circle = Circle(stroke_color=BLUE, stroke_width=4)

        # 创建后设置描边
        square = Square()
        square.set_stroke(RED, width=8)

        self.add(circle, square)
```

### 描边方法
```python
mobject.set_stroke(color=RED)                  # 仅颜色
mobject.set_stroke(RED, width=4)               # 颜色和宽度
mobject.set_stroke(width=4)                    # 仅宽度
mobject.set_stroke(opacity=0.5)                # 仅不透明度
mobject.set_stroke_color(RED)                  # 仅颜色（替代写法）
mobject.set_stroke_width(4)                    # 仅宽度（替代写法）
mobject.set_stroke_opacity(0.5)                # 仅不透明度（替代写法）
```

### 描边宽度参考
```python
# 常用描边宽度
DEFAULT_STROKE_WIDTH = 4
thin = 1
normal = 4
thick = 8
very_thick = 12
```

## 组合样式

```python
class CombinedStyling(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE, opacity=0.5)
        square.set_stroke(YELLOW, width=6)
        self.add(square)
```

### 方法链式调用
```python
square = Square().set_fill(RED, 0.5).set_stroke(WHITE, 4)
```

## set_style 方法

一次设置多个样式属性：

```python
square = Square()
square.set_style(
    fill_color=BLUE,
    fill_opacity=0.5,
    stroke_color=WHITE,
    stroke_width=4,
    stroke_opacity=1
)
```

## 不透明度

控制 mobject 的透明度：

```python
# 整体不透明度
mobject.set_opacity(0.5)  # 影响填充和描边

# 分别设置不透明度
mobject.set_fill_opacity(0.8)
mobject.set_stroke_opacity(0.3)

# 淡出效果
mobject.fade(0.5)  # 0.5 = 50% 淡出（不透明度的反向）
```

## 背景矩形

在文本或其他 mobject 后添加背景：

```python
class BackgroundExample(Scene):
    def construct(self):
        text = Text("重要！")
        bg = BackgroundRectangle(text, fill_opacity=0.8, buff=0.1)
        group = VGroup(bg, text)
        self.add(group)
```

## 应用于子对象

```python
# 应用于所有子对象（family=True，默认）
group.set_fill(RED, opacity=0.5, family=True)

# 仅应用于父对象，不应用于子对象
group.set_fill(RED, opacity=0.5, family=False)
```

## 基于位置的样式

```python
class GradientFill(Scene):
    def construct(self):
        squares = VGroup(*[Square() for _ in range(5)]).arrange(RIGHT)

        for i, sq in enumerate(squares):
            opacity = (i + 1) / 5
            sq.set_fill(BLUE, opacity=opacity)

        self.add(squares)
```

## 复制样式

```python
# 从另一个 mobject 复制样式
source = Circle().set_fill(RED, 0.5).set_stroke(WHITE, 4)
target = Square()
target.match_style(source)  # 现在具有相同的填充和描边
```

## 最佳实践

1. **形状使用 fill_opacity** —— 完全不透明的填充可能遮挡其他元素
2. **描边宽度保持一致** —— 选择一个宽度并坚持使用
3. **填充和描边形成对比** —— 不同颜色有助于轮廓清晰
4. **使用 BackgroundRectangle 提高可读性** —— 在复杂背景上的文本后方
5. **链式调用保持代码简洁** —— 但过长时请换行
