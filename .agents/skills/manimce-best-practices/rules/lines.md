---
name: lines
description: Line、Arrow、Vector、DashedLine 和连接器
metadata:
  tags: line, arrow, vector, dashedline, brace, connector
---

# 线和箭头

使用线和箭头连接点并显示关系。

## Line

两点之间的基本线。

```python
from manim import *

class LineExample(Scene):
    def construct(self):
        # 从两个点创建线
        line = Line(LEFT * 2, RIGHT * 2)

        # 带样式
        styled_line = Line(
            UP * 2, DOWN * 2,
            color=BLUE,
            stroke_width=4
        )

        self.add(line, styled_line)
```

### Line 属性

```python
line = Line(LEFT, RIGHT)

# 获取点
line.get_start()
line.get_end()
line.get_center()
line.get_length()
line.get_angle()

# 修改
line.put_start_and_end_on(new_start, new_end)
line.set_length(3)  # 保持方向，改变长度
```

## Arrow

带箭头的线。

```python
class ArrowExample(Scene):
    def construct(self):
        # 基本箭头
        arrow = Arrow(LEFT * 2, RIGHT * 2)

        # 带样式的箭头
        styled = Arrow(
            start=UP,
            end=DOWN,
            color=RED,
            stroke_width=6,
            tip_length=0.4,
            max_tip_length_to_length_ratio=0.5
        )

        self.add(arrow, styled)
```

### 箭头变体

```python
# 双头箭头
double = DoubleArrow(LEFT * 2, RIGHT * 2)

# 自定义箭头的箭头尖
arrow = Arrow(LEFT, RIGHT)
arrow.tip  # 访问箭头尖端 mobject
```

## Vector

从原点出发的箭头（适用于物理/数学）。

```python
class VectorExample(Scene):
    def construct(self):
        # 从原点出发的向量
        v1 = Vector([2, 1, 0], color=YELLOW)
        v2 = Vector([-1, 2, 0], color=GREEN)

        self.add(v1, v2)
```

## DashedLine

```python
class DashedLineExample(Scene):
    def construct(self):
        dashed = DashedLine(
            LEFT * 2, RIGHT * 2,
            dash_length=0.2,
            dashed_ratio=0.5,  # 实线部分与间隙的比例
            color=WHITE
        )
        self.add(dashed)
```

## TangentLine

在曲线上某点与曲线相切的线。

```python
class TangentLineExample(Scene):
    def construct(self):
        circle = Circle(radius=2)

        # 在特定点的切线（t 参数 0-1 沿曲线）
        tangent = TangentLine(circle, alpha=0.25, length=3, color=YELLOW)

        self.add(circle, tangent)
```

## Brace

用于高亮的花括号。

```python
class BraceExample(Scene):
    def construct(self):
        rect = Rectangle(width=4, height=1)

        # 矩形下方的花括号
        brace = Brace(rect, DOWN)

        # 带标签
        brace_text = brace.get_text("Width")

        # 替代：BraceLabel
        brace_label = BraceLabel(rect, "Width", DOWN)

        self.add(rect, brace, brace_text)
```

### Brace 方向

```python
brace_down = Brace(mobject, DOWN)
brace_up = Brace(mobject, UP)
brace_left = Brace(mobject, LEFT)
brace_right = Brace(mobject, RIGHT)
```

## CurvedArrow

两点之间的曲线箭头。

```python
class CurvedArrowExample(Scene):
    def construct(self):
        curved = CurvedArrow(
            start_point=LEFT * 2,
            end_point=RIGHT * 2,
            angle=PI/2  # 曲率
        )
        self.add(curved)
```

## Elbow

直角连接器。

```python
class ElbowExample(Scene):
    def construct(self):
        elbow = Elbow(width=2, angle=PI/2)
        self.add(elbow)
```

## NumberLine 刻度

```python
class TicksExample(Scene):
    def construct(self):
        line = NumberLine(x_range=[-3, 3, 1])
        self.add(line)
```

## 连接 Mobjects

### Mobjects 之间的线

```python
class ConnectMobjects(Scene):
    def construct(self):
        c1 = Circle().shift(LEFT * 2)
        c2 = Circle().shift(RIGHT * 2)

        # 连接中心的线
        line = Line(c1.get_center(), c2.get_center())

        # 边缘之间的箭头
        arrow = Arrow(
            c1.get_right(),  # c1 的右边缘
            c2.get_left(),   # c2 的左边缘
            buff=0.1         # 距边缘的小间隙
        )

        self.add(c1, c2, line, arrow)
```

### 带 Updater 的动态连接

```python
class DynamicLine(Scene):
    def construct(self):
        dot1 = Dot(LEFT * 2)
        dot2 = Dot(RIGHT * 2)

        # 跟随点的线
        line = always_redraw(lambda: Line(
            dot1.get_center(),
            dot2.get_center(),
            color=YELLOW
        ))

        self.add(dot1, dot2, line)
        self.play(dot1.animate.shift(UP * 2), run_time=2)
```

## 最佳实践

1. **方向使用 Arrow** - 比普通线更清晰
2. **物理/数学使用 Vector** - 语义上有意义
3. **标注尺寸使用 Brace** - 专业外观
4. **辅助线使用 DashedLine** - 与主要内容区分
5. **动态线使用 always_redraw** - 随移动端点更新
