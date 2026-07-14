---
name: mobjects
description: Manim 中的 Mobject 类型、VMobject 和 mobject 层次结构
metadata:
  tags: mobject, vmobject, group, submobjects, hierarchy
---

# Manim 中的 Mobjects

Mobject（数学对象）是 Manim 中所有可显示对象的基类。

## Mobject 层次结构

```
Mobject（基类）
├── VMobject（向量化 Mobject——最常用）
│   ├── Circle、Square、Rectangle、Polygon
│   ├── Line、Arrow、Vector
│   ├── Text、MathTex、Tex
│   ├── Axes、NumberPlane
│   └── VGroup
├── ImageMobject（用于图像）
├── PMobject（点云）
└── Group（用于非 VMobject 集合）
```

## VMobject（向量化 Mobject）

您使用的大多数形状都是 VMobject——它们由贝塞尔曲线定义。

```python
# 常用 VMobject
circle = Circle()
square = Square()
rect = Rectangle(width=4, height=2)
triangle = Triangle()
polygon = Polygon(ORIGIN, RIGHT, UP)
line = Line(LEFT, RIGHT)
arrow = Arrow(LEFT, RIGHT)
```

## 创建自定义 VMobject

```python
class CustomShape(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 使用 set_points_as_corners 或 set_points_smoothly 定义点
        self.set_points_as_corners([
            LEFT, UP, RIGHT, DOWN, LEFT
        ])
```

## Mobject 属性

### 位置和大小

```python
mobject.get_center()      # 返回中心点
mobject.get_width()       # 返回宽度
mobject.get_height()      # 返回高度
mobject.get_top()         # 顶部边缘中心点
mobject.get_bottom()      # 底部边缘中心点
mobject.get_left()        # 左侧边缘中心点
mobject.get_right()       # 右侧边缘中心点
```

### 边界框角落

```python
mobject.get_corner(UL)    # 左上角
mobject.get_corner(UR)    # 右上角
mobject.get_corner(DL)    # 左下角
mobject.get_corner(DR)    # 右下角
```

## 子对象

Mobject 可以包含其他 mobject 作为子对象。

```python
# 访问子对象
group = VGroup(Circle(), Square())
group.submobjects      # 子 mobject 列表
group[0]               # 第一个子对象（Circle）
group[1]               # 第二个子对象（Square）

# 遍历子对象
for mob in group:
    mob.set_color(RED)
```

## 复制 Mobjects

```python
# 创建副本
circle_copy = circle.copy()

# 复制并定位
circle_copy = circle.copy().shift(RIGHT * 2)
```

## 方法链式调用

大多数 mobject 方法返回 `self`，允许方法链式调用：

```python
circle = Circle().set_color(RED).shift(LEFT).scale(2)
```

## 最佳实践

1. **自定义形状使用 VMobject** - 更好的渲染和动画支持
2. **优先使用 VGroup 而非 Group** - VGroup 与大多数动画配合更好
3. **复用对象时使用 copy()** - 避免意外修改原始对象
4. **链式调用提升可读性** - 但如果太长，请换行
