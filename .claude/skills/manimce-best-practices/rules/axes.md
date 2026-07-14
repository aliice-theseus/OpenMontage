---
name: axes
description: 坐标轴（Axes）、数平面（NumberPlane）和 Manim 中的坐标系统
metadata:
  tags: axes, numberplane, coordinate, grid, numberline
---

# 坐标系统

创建用于数学可视化的坐标轴、网格和数轴。

## Axes（坐标轴）

基本的 2D 坐标轴。

```python
from manim import *

class AxesExample(Scene):
    def construct(self):
        # 默认坐标轴
        axes = Axes()
        self.add(axes)
```

### 自定义坐标轴

```python
class CustomAxes(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-5, 5, 1],      # [最小值, 最大值, 步长]
            y_range=[-3, 3, 1],
            x_length=10,              # 屏幕上的物理长度
            y_length=6,
            axis_config={
                "color": BLUE,
                "include_tip": True,
                "include_numbers": True,
            },
            x_axis_config={
                "numbers_to_include": [-4, -2, 0, 2, 4],
            },
            y_axis_config={
                "numbers_to_include": [-2, 0, 2],
            },
        )
        self.add(axes)
```

### 添加标签

```python
class AxesLabels(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 3])

        # 添加轴标签
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        # 自定义标签
        x_label = axes.get_x_axis_label(MathTex(r"\theta"))
        y_label = axes.get_y_axis_label(MathTex(r"f(\theta)"))

        self.add(axes, x_label, y_label)
```

## NumberPlane（数平面）

带坐标轴的网格 —— 显示坐标线。

```python
class NumberPlaneExample(Scene):
    def construct(self):
        # 默认平面
        plane = NumberPlane()
        self.add(plane)
```

### 自定义 NumberPlane

```python
class CustomPlane(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={
                "color": WHITE,
            },
        )
        self.add(plane)
```

## ComplexPlane（复平面）

用于可视化复数。

```python
class ComplexPlaneExample(Scene):
    def construct(self):
        plane = ComplexPlane()

        # 绘制复数点
        z = complex(2, 1)  # 2 + i
        dot = Dot(plane.n2p(z), color=YELLOW)
        label = MathTex("2+i").next_to(dot, UR)

        self.add(plane, dot, label)
```

## NumberLine（数轴）

单条坐标轴线。

```python
class NumberLineExample(Scene):
    def construct(self):
        line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
            include_tip=True,
        )
        self.add(line)
```

## 坐标转换

```python
class CoordinateConversion(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 3])

        # 坐标转换为屏幕位置
        point = axes.c2p(2, 1)  # coords_to_point：(2, 1) -> 屏幕位置

        # 屏幕位置转换为坐标
        coords = axes.p2c(point)  # point_to_coords：屏幕 -> (x, y)

        dot = Dot(point, color=RED)
        self.add(axes, dot)
```

### 简写方法

```python
axes = Axes()

# c2p = coords_to_point
axes.c2p(x, y)

# p2c = point_to_coords
axes.p2c(point)

# i2gp = input_to_graph_point（用于图形）
axes.i2gp(x, graph)

# 用于 NumberPlane/ComplexPlane
plane.n2p(complex_number)  # number_to_point
plane.p2n(point)           # point_to_number
```

## ThreeDAxes（3D 坐标轴）

用于 3D 可视化。

```python
class ThreeDAxesExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            z_length=6,
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)
```

## 绘制点

```python
class PlotPoints(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-3, 3])

        points = [(1, 2), (-2, 1), (3, -1), (0, 2)]
        dots = VGroup(*[
            Dot(axes.c2p(x, y), color=YELLOW)
            for x, y in points
        ])

        self.add(axes, dots)
```

## 最佳实践

1. **设置合适的范围** —— 不要包含不必要的空白区域
2. **使 x_length/y_length 与范围比例匹配** —— 防止变形
3. **变换使用 NumberPlane** —— 网格清晰展示变形效果
4. **所有坐标工作使用 c2p** —— 不要手动转换
5. **谨慎包含数字** —— 太多数字会显得杂乱
