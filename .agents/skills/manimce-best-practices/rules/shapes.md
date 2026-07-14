---
name: shapes
description: Circle、Square、Rectangle、Polygon 和几何基本体
metadata:
  tags: shapes, circle, square, rectangle, polygon, geometry
---

# 几何形状

Manim 中的基本几何基本体。

## Circle

```python
from manim import *

class CircleExample(Scene):
    def construct(self):
        # 默认圆
        c1 = Circle()

        # 带参数
        c2 = Circle(
            radius=2,
            color=BLUE,
            fill_opacity=0.5,
            stroke_width=4
        )

        self.add(c1, c2)
```

### Circle 方法

```python
circle = Circle()

# 获取属性
circle.get_radius()
circle.get_center()

# 从点创建
Circle.from_three_points(p1, p2, p3)

# 包围另一个 mobject
triangle = Triangle()
circle = Circle().surround(triangle)  # 圆包围三角形
circle = Circle().surround(triangle, buffer_factor=1.5)  # 带边距
circle = Circle().surround(triangle, stretch=True)  # 拉伸以适应
```

## Ellipse

```python
class EllipseExample(Scene):
    def construct(self):
        ellipse = Ellipse(
            width=4,
            height=2,
            color=GREEN
        )
        self.add(ellipse)
```

## Square

```python
class SquareExample(Scene):
    def construct(self):
        # 默认正方形
        s1 = Square()

        # 带参数
        s2 = Square(
            side_length=2,
            color=RED,
            fill_opacity=0.8
        )

        self.add(s1, s2)
```

## Rectangle

```python
class RectangleExample(Scene):
    def construct(self):
        rect = Rectangle(
            width=4,
            height=2,
            color=YELLOW,
            fill_opacity=0.5
        )
        self.add(rect)
```

### RoundedRectangle

```python
class RoundedRectExample(Scene):
    def construct(self):
        rounded = RoundedRectangle(
            width=4,
            height=2,
            corner_radius=0.5,
            color=BLUE,
            fill_opacity=0.8
        )
        self.add(rounded)
```

## Triangle

```python
class TriangleExample(Scene):
    def construct(self):
        # 等边三角形
        tri = Triangle(color=PURPLE)

        # 自定义三角形（使用 Polygon）
        custom_tri = Polygon(
            ORIGIN, RIGHT * 2, UP * 3,
            color=GREEN
        )

        self.add(tri, custom_tri.shift(RIGHT * 3))
```

## Polygon

从顶点创建任意多边形。

```python
class PolygonExample(Scene):
    def construct(self):
        # 五边形
        pentagon = RegularPolygon(n=5, color=ORANGE)

        # 六边形
        hexagon = RegularPolygon(n=6, color=TEAL)

        # 自定义多边形
        custom = Polygon(
            [-2, -1, 0],
            [2, -1, 0],
            [2, 1, 0],
            [0, 2, 0],
            [-2, 1, 0],
            color=PINK
        )

        VGroup(pentagon, hexagon, custom).arrange(RIGHT, buff=1)
        self.add(pentagon, hexagon, custom)
```

## RegularPolygon

```python
class RegularPolygonExamples(Scene):
    def construct(self):
        shapes = VGroup(
            RegularPolygon(n=3),   # 三角形
            RegularPolygon(n=4),   # 正方形
            RegularPolygon(n=5),   # 五边形
            RegularPolygon(n=6),   # 六边形
            RegularPolygon(n=8),   # 八边形
        ).arrange(RIGHT)
        self.add(shapes)
```

## Star

```python
class StarExample(Scene):
    def construct(self):
        star = Star(
            n=5,                    # 顶点数
            outer_radius=2,
            inner_radius=1,         # 可选：未指定时自动计算
            density=2,              # 顶点连接方式（影响形状）
            color=YELLOW,
            fill_opacity=1
        )
        self.add(star)

        # 不同密度创建不同星形图案
        star_d2 = Star(7, outer_radius=2, density=2, color=RED)
        star_d3 = Star(7, outer_radius=2, density=3, color=PURPLE)
```

## RegularPolygram

通过密度连接顶点的星形。

```python
class PolygramExample(Scene):
    def construct(self):
        # 五角星形（5角星图案）
        pentagram = RegularPolygram(5, radius=2)
        self.add(pentagram)
```

## Annulus（圆环）

```python
class AnnulusExample(Scene):
    def construct(self):
        ring = Annulus(
            inner_radius=1,
            outer_radius=2,
            color=BLUE,
            fill_opacity=0.5
        )
        self.add(ring)
```

## Sector 和 Arc

```python
class SectorArcExample(Scene):
    def construct(self):
        # Sector（扇形）
        sector = Sector(
            radius=2,
            angle=PI/2,
            start_angle=0,
            color=RED,
            fill_opacity=0.8
        ).shift(LEFT * 2)

        # Arc（仅曲线）
        arc = Arc(
            radius=2,
            angle=PI/2,
            start_angle=PI,
            color=BLUE
        ).shift(RIGHT * 2)

        self.add(sector, arc)
```

## ArcBetweenPoints

```python
class ArcBetweenPointsExample(Scene):
    def construct(self):
        arc = ArcBetweenPoints(
            start=LEFT * 2,
            end=RIGHT * 2,
            angle=PI/2,  # 曲率
            color=GREEN
        )
        self.add(arc)
```

## Dot

```python
class DotExample(Scene):
    def construct(self):
        # 默认点
        d1 = Dot()

        # 自定义
        d2 = Dot(
            point=RIGHT * 2,
            radius=0.2,
            color=YELLOW
        )

        self.add(d1, d2)
```

## 常用形状操作

```python
shape = Square()

# 变换
shape.scale(2)
shape.rotate(PI/4)
shape.stretch(2, dim=0)  # 水平拉伸

# 样式
shape.set_fill(RED, opacity=0.5)
shape.set_stroke(WHITE, width=4)

# 定位
shape.move_to(ORIGIN)
shape.shift(UP * 2)
shape.next_to(other, RIGHT)
```

## 最佳实践

1. **规则形状使用 RegularPolygon** - 比手动 Polygon 更精确
2. **设置 fill_opacity 确保可见性** - 默认常为 0（透明）
3. **点使用 Dot** - 比小半径 Circle 更好
4. **UI 元素使用 RoundedRectangle** - 更精致的外观
5. **使用 VGroup 组合形状** - 用于复杂图形
