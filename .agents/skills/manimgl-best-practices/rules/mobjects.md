# ManimGL Mobjects

## Mobject 层次结构

```
Mobject（基类）
├── VMobject（向量化——最常用）
│   ├── VGroup
│   ├── Circle、Square、Rectangle、Line、Arrow
│   ├── Tex、Text、TexText
│   └── Axes、NumberPlane
├── Group（非向量化容器）
├── ImageMobject
├── Point
└── 3D对象（Surface、ParametricSurface等）
```

## 创建 Mobjects

```python
# 几何图形
circle = Circle(radius=1, color=BLUE)
square = Square(side_length=2)
rect = Rectangle(width=3, height=2)
line = Line(LEFT, RIGHT)
arrow = Arrow(ORIGIN, UP)

# 文本
text = Text("Hello")
math = Tex(R"\pi r^2")

# 组
group = VGroup(circle, square)
```

## 定位

```python
# 绝对位置
circle.move_to(ORIGIN)
circle.move_to(RIGHT * 2 + UP)

# 相对于屏幕边缘
circle.to_edge(UP)
circle.to_edge(LEFT, buff=1)
circle.to_corner(UL)

# 相对于其他 mobject
square.next_to(circle, RIGHT)
square.next_to(circle, DOWN, buff=0.5)

# 对齐
group.align_to(other, UP)
group.align_to(other, LEFT)

# 移动
circle.shift(RIGHT * 2)
circle.shift(UP + RIGHT)
```

## 样式

```python
# 填充
circle.set_fill(BLUE, opacity=0.5)

# 描边（轮廓）
circle.set_stroke(WHITE, width=2)
circle.set_stroke(color=RED, width=4, opacity=0.8)

# 同时设置
circle.set_style(
    fill_color=BLUE,
    fill_opacity=0.5,
    stroke_color=WHITE,
    stroke_width=2
)

# 颜色（同时影响填充和描边）
circle.set_color(RED)

# 背光描边（后方轮廓，提升可读性）
text.set_backstroke(BLACK, 5)
```

## VGroup

用于向量化 mobject 的容器：

```python
# 创建组
shapes = VGroup(circle, square, triangle)

# 排列
shapes.arrange(RIGHT, buff=0.5)
shapes.arrange(DOWN, aligned_edge=LEFT)
shapes.arrange_in_grid(rows=2, cols=3)

# 应用于所有元素
shapes.set_color(BLUE)
shapes.scale(0.5)
shapes.shift(UP)

# 访问元素
shapes[0]  # 第一个元素
shapes[-1]  # 最后一个元素
shapes[1:3]  # 切片
```

## Group vs VGroup

```python
# VGroup - 用于向量化 mobject（VMobject 子类）
vgroup = VGroup(Circle(), Square())

# Group - 用于任何 mobject，包括图像、3D等
group = Group(ImageMobject("photo.png"), Circle())
```

## 常用方法

| 方法 | 描述 |
|--------|-------------|
| `.move_to(point)` | 将中心移动到点 |
| `.shift(vector)` | 按向量移动 |
| `.scale(factor)` | 按比例缩放 |
| `.rotate(angle)` | 旋转角度（弧度） |
| `.next_to(mob, dir)` | 放置在另一个旁边 |
| `.align_to(mob, dir)` | 边缘对齐 |
| `.to_edge(dir)` | 移动到屏幕边缘 |
| `.to_corner(corner)` | 移动到屏幕角落 |
| `.get_center()` | 获取中心点 |
| `.get_width()` | 获取宽度 |
| `.get_height()` | 获取高度 |
| `.copy()` | 创建副本 |

## 生成目标

用于动画化到修改版本：

```python
circle.generate_target()
circle.target.shift(RIGHT * 2)
circle.target.scale(2)
circle.target.set_color(RED)

self.play(MoveToTarget(circle))
```

## 保存和恢复状态

```python
circle.save_state()
self.play(circle.animate.shift(RIGHT).scale(2))
# 之后...
self.play(Restore(circle))
```

## Updaters

动态行为：

```python
# 始终跟随另一个 mobject
label.add_updater(lambda m: m.next_to(dot, UP))

# 基于时间
circle.add_updater(lambda m, dt: m.rotate(dt))

# 基于值，配合 ValueTracker
tracker = ValueTracker(0)
circle.add_updater(
    lambda m: m.set_fill(opacity=tracker.get_value())
)
self.play(tracker.animate.set_value(1))
```

## 有用快捷方式

```python
# f_always 用于常见 updater 模式
label.f_always.next_to(dot, UP)

# always（函数形式）
always(label.next_to, dot, UP)
```
