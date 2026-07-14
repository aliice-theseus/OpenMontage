---
name: positioning
description: move_to、next_to、align_to、shift 和定位方法
metadata:
  tags: position, move_to, next_to, shift, align, layout
---

# Manim 中的定位

用于在场景中放置和移动 mobject 的方法。

## 坐标系

Manim 使用以下坐标系：
- 原点 (0, 0, 0) 位于屏幕中心
- X轴：左 (-) 到右 (+)
- Y轴：下 (-) 到上 (+)
- Z轴：内 (-) 到外 (+)（用于3D）

### 方向常量
```python
UP = np.array([0, 1, 0])
DOWN = np.array([0, -1, 0])
LEFT = np.array([-1, 0, 0])
RIGHT = np.array([1, 0, 0])
ORIGIN = np.array([0, 0, 0])

# 对角线
UL = UP + LEFT      # 左上
UR = UP + RIGHT     # 右上
DL = DOWN + LEFT    # 左下
DR = DOWN + RIGHT   # 右下
```

## move_to

移动到绝对位置。

```python
from manim import *

class MoveToExample(Scene):
    def construct(self):
        circle = Circle()

        # 移动到原点
        circle.move_to(ORIGIN)

        # 移动到指定坐标
        circle.move_to(RIGHT * 2 + UP * 1)

        # 移动到另一个 mobject 的位置
        square = Square().shift(LEFT * 2)
        circle.move_to(square)

        # 移动到另一个 mobject 的特定点
        circle.move_to(square.get_top())
```

## shift

相对于当前位置移动。

```python
class ShiftExample(Scene):
    def construct(self):
        circle = Circle()

        # 向一个方向移动
        circle.shift(RIGHT)
        circle.shift(UP * 2)

        # 向多个方向移动
        circle.shift(RIGHT * 2 + UP * 1)

        # 链式移动
        circle.shift(LEFT).shift(DOWN)
```

## next_to

相对于另一个 mobject 定位。

```python
class NextToExample(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        triangle = Triangle()

        # 将圆形放置在正方形的右侧
        circle.next_to(square, RIGHT)

        # 带间距缓冲区
        triangle.next_to(square, DOWN, buff=0.5)

        # 对齐到特定边缘
        circle.next_to(square, RIGHT, aligned_edge=UP)
```

### buff 参数
```python
# 默认间距
circle.next_to(square, RIGHT)  # 使用 DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

# 自定义间距
circle.next_to(square, RIGHT, buff=0)    # 无间隙
circle.next_to(square, RIGHT, buff=1)    # 1个单位间隙
circle.next_to(square, RIGHT, buff=0.5)  # 半单位间隙
```

## align_to

与另一个 mobject 的边缘对齐。

```python
class AlignToExample(Scene):
    def construct(self):
        square = Square().shift(LEFT)
        circle = Circle().shift(RIGHT)

        # 将圆形的左边缘与正方形的左边缘对齐
        circle.align_to(square, LEFT)

        # 对齐顶部
        circle.align_to(square, UP)

        # 对齐到某点
        circle.align_to(ORIGIN, DOWN)
```

## 边缘方法

定位到屏幕边缘。

```python
class EdgeExample(Scene):
    def construct(self):
        # 定位到屏幕边缘
        text1 = Text("Top").to_edge(UP)
        text2 = Text("Bottom").to_edge(DOWN)
        text3 = Text("Left").to_edge(LEFT)
        text4 = Text("Right").to_edge(RIGHT)

        # 带间距
        text5 = Text("Buffered").to_edge(UP, buff=1)
```

## 角落方法

定位到屏幕角落。

```python
class CornerExample(Scene):
    def construct(self):
        t1 = Text("UL").to_corner(UL)
        t2 = Text("UR").to_corner(UR)
        t3 = Text("DL").to_corner(DL)
        t4 = Text("DR").to_corner(DR)

        # 带间距
        t5 = Text("Buffered").to_corner(UL, buff=0.5)
```

## 居中

在屏幕或另一个 mobject 中居中。

```python
mobject.center()           # 在屏幕中居中
mobject.center_on(other)   # 在另一个 mobject 上居中（自定义辅助方法）
```

## 获取位置

```python
circle = Circle()

# 获取各种位置点
circle.get_center()        # 中心点
circle.get_top()           # 顶部边缘中心
circle.get_bottom()        # 底部边缘中心
circle.get_left()          # 左侧边缘中心
circle.get_right()         # 右侧边缘中心
circle.get_corner(UL)      # 左上角
circle.get_corner(DR)      # 右下角
circle.get_start()         # 路径起点
circle.get_end()           # 路径终点
```

## 动画定位

```python
class AnimatedPosition(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # 动画移动
        self.play(square.animate.shift(RIGHT * 2))
        self.play(square.animate.move_to(UP * 2))
        self.play(square.animate.to_edge(LEFT))
```

## 最佳实践

1. **相对定位使用 next_to** - 保持关系
2. **绝对定位使用 move_to** - 精确坐标
3. **相对调整使用 shift** - 快速微调
4. **屏幕定位使用 to_edge/to_corner** - 响应式布局
5. **调整 buff 控制视觉间距** - 不要让元素拥挤
