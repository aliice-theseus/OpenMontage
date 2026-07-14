---
name: grouping
description: VGroup、Group、arrange 和布局模式
metadata:
  tags: vgroup, group, arrange, layout, grid, submobjects
---

# 分组 Mobjects

将多个 mobject 组织成组以便集体操作。

## VGroup

VGroup（矢量化组）用于分组 VMobjects。最常用。

```python
from manim import *

class VGroupExample(Scene):
    def construct(self):
        # 创建组
        group = VGroup(
            Circle(),
            Square(),
            Triangle()
        )

        # 操作应用于所有成员
        group.set_color(RED)
        group.shift(UP)

        self.add(group)
```

## Group

Group 用于混合不同类型的 mobject（VMobjects、ImageMobjects 等）。

```python
class GroupExample(Scene):
    def construct(self):
        # 混合不同类型
        text = Text("你好")
        group = Group(
            Circle(),
            text
        )
        self.add(group)
```

## 创建 Groups

```python
# 从单个 mobjects
group = VGroup(circle, square, triangle)

# 从列表
shapes = [Circle(), Square(), Triangle()]
group = VGroup(*shapes)

# 使用列表推导式
group = VGroup(*[Circle() for _ in range(5)])

# 空组，稍后添加
group = VGroup()
group.add(Circle())
group.add(Square())
```

## arrange

将 mobjects 排列成一行。

```python
class ArrangeExample(Scene):
    def construct(self):
        # 水平排列（默认）
        row = VGroup(*[Circle().scale(0.3) for _ in range(5)])
        row.arrange(RIGHT, buff=0.5).shift(UP * 2)

        # 垂直排列
        column = VGroup(*[Square().scale(0.3) for _ in range(4)])
        column.arrange(DOWN, buff=0.5).shift(LEFT * 2)

        # 自定义间距
        spaced = VGroup(*[Triangle().scale(0.3) for _ in range(3)])
        spaced.arrange(RIGHT, buff=1).shift(DOWN * 2)

        self.add(row, column, spaced)
```

### 方向选项
```python
group.arrange(RIGHT)      # 从左到右
group.arrange(LEFT)       # 从右到左
group.arrange(UP)         # 从下到上
group.arrange(DOWN)       # 从上到下
```

## arrange_in_grid

以网格模式排列。

```python
class GridExample(Scene):
    def construct(self):
        # 自动网格
        grid = VGroup(*[Square().scale(0.3) for _ in range(20)])
        grid.arrange_in_grid()

        # 指定行列
        grid = VGroup(*[Circle().scale(0.2) for _ in range(12)])
        grid.arrange_in_grid(rows=3, cols=4)

        # 带间距
        grid.arrange_in_grid(rows=3, cols=4, buff=0.5)

        self.add(grid)
```

## 访问组成员

```python
group = VGroup(Circle(), Square(), Triangle())

# 按索引
first = group[0]          # Circle
second = group[1]         # Square
last = group[-1]          # Triangle

# 切片
first_two = group[0:2]    # 包含 Circle 和 Square 的 VGroup

# 遍历
for mob in group:
    mob.set_color(random_color())

# 长度
num_items = len(group)
```

## 修改 Groups

```python
group = VGroup(Circle(), Square())

# 添加 mobjects
group.add(Triangle())
group.add(Star(), Pentagon())

# 移除 mobjects
group.remove(circle)

# 在指定位置插入
group.insert(0, new_mobject)

# 子对象列表
group.submobjects  # 所有子元素的列表
```

## 组变换

```python
group = VGroup(Circle(), Square(), Triangle()).arrange(RIGHT)

# 所有变换应用于整个组
group.shift(UP * 2)
group.scale(0.5)
group.rotate(PI / 4)
group.set_color(BLUE)

# 但可以针对单个对象
group[0].set_color(RED)  # 仅圆形
```

## 嵌套组

```python
class NestedGroups(Scene):
    def construct(self):
        # 创建子组
        row1 = VGroup(*[Circle() for _ in range(3)]).arrange(RIGHT)
        row2 = VGroup(*[Square() for _ in range(3)]).arrange(RIGHT)
        row3 = VGroup(*[Triangle() for _ in range(3)]).arrange(RIGHT)

        # 组的组
        all_rows = VGroup(row1, row2, row3).arrange(DOWN)

        self.add(all_rows)
```

## 有用的 Group 方法

```python
group = VGroup(Circle(), Square(), Triangle())

# 获取包围盒信息
group.get_center()
group.get_width()
group.get_height()

# 设置整个组的位置
group.move_to(ORIGIN)
group.to_edge(LEFT)

# 复制整个组
group_copy = group.copy()

# 匹配另一个组的布局
group1.match_height(group2)
group1.match_width(group2)
```

## 最佳实践

1. **VMobjects 使用 VGroup** —— 更好的性能和兼容性
2. **创建后使用 arrange** —— 不要单独定位再分组
3. **语义化命名组** —— `equation_parts` 而不是 `group1`
4. **使用嵌套组构建结构** —— 行中包含列等
5. **需要时复制组** —— 避免意外修改
