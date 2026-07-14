# ManimGL 中的动画组

动画组允许您协调多个动画，同时、顺序或以交错时间运行它们。

## AnimationGroup

同时运行多个动画。

### 基本用法

```python
from manimlib import *

class GroupExample(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        circle.shift(LEFT * 2)
        square.shift(RIGHT * 2)

        # 同时运行两个动画
        self.play(AnimationGroup(
            ShowCreation(circle),
            ShowCreation(square)
        ))
        self.wait()
```

### 简写语法

```python
# 等同于 AnimationGroup
self.play(
    ShowCreation(circle),
    ShowCreation(square)
)
```

## LaggedStart

以交错延迟启动动画。

### 基本 LaggedStart

```python
class LaggedStartExample(Scene):
    def construct(self):
        circles = VGroup(*[
            Circle(radius=0.5).shift(i * RIGHT)
            for i in range(-3, 4)
        ])

        # 交错创建
        self.play(LaggedStart(
            *[ShowCreation(c) for c in circles],
            lag_ratio=0.2,  # 动画之间的延迟比例
            run_time=3
        ))
        self.wait()
```

### lag_ratio 参数

```python
# lag_ratio 控制延迟
# 0 = 全部同时（像 AnimationGroup）
# 1 = 完全顺序（像 Succession）
# 0.5 = 重叠动画

# 微妙重叠
self.play(LaggedStart(*animations, lag_ratio=0.1))

# 更明显的交错
self.play(LaggedStart(*animations, lag_ratio=0.5))

# 近乎顺序
self.play(LaggedStart(*animations, lag_ratio=0.9))
```

## Succession

一个接一个地运行动画。

```python
class SuccessionExample(Scene):
    def construct(self):
        shapes = VGroup(
            Circle().shift(LEFT * 2),
            Square(),
            Triangle().shift(RIGHT * 2)
        )

        # 一个接一个（无重叠）
        self.play(Succession(
            ShowCreation(shapes[0]),
            ShowCreation(shapes[1]),
            ShowCreation(shapes[2])
        ))
        self.wait()
```

### Succession vs 连续的 play() 调用

```python
# 使用 Succession（在一个 play 调用中完成全部）
self.play(Succession(
    animation1,
    animation2,
    animation3
))

# 等同于分开的 play 调用
self.play(animation1)
self.play(animation2)
self.play(animation3)
```

## 组合动画组

### 嵌套组

```python
class NestedGroups(Scene):
    def construct(self):
        # 顶行
        top = VGroup(*[Circle().shift(i*RIGHT) for i in range(-2, 3)])

        # 底行
        bottom = VGroup(*[Square().shift(i*RIGHT + 2*DOWN) for i in range(-2, 3)])

        # 每行内部交错，但两行同时出现
        self.play(
            LaggedStart(*[ShowCreation(c) for c in top], lag_ratio=0.2),
            LaggedStart(*[ShowCreation(s) for s in bottom], lag_ratio=0.2),
        )
        self.wait()
```

### 顺序组

```python
# 先第一组，然后第二组
self.play(Succession(
    LaggedStart(*[ShowCreation(t) for t in top], lag_ratio=0.2),
    LaggedStart(*[ShowCreation(b) for b in bottom], lag_ratio=0.2)
))
```

## LaggedStartMap

将动画构造函数应用于多个 mobject，带交错效果。

```python
class LaggedStartMapExample(Scene):
    def construct(self):
        dots = VGroup(*[
            Dot().shift(i * RIGHT + j * UP)
            for i in range(-3, 4)
            for j in range(-2, 3)
        ])

        # 对所有点应用 FadeIn，带交错效果
        self.play(LaggedStartMap(
            FadeIn, dots,
            lag_ratio=0.05
        ))
        self.wait()
```

## 时间控制

### 组的 run_time

```python
# 所有动画的总时间
self.play(LaggedStart(
    *animations,
    lag_ratio=0.2,
    run_time=5  # 总持续时间
))

# 每个动画的单独时间
self.play(LaggedStart(
    ShowCreation(circle, run_time=2),
    ShowCreation(square, run_time=1),
    lag_ratio=0.3
))
```

### 组的 rate_func

```python
# 将速率函数应用于整个组
self.play(
    LaggedStart(*animations, lag_ratio=0.2),
    rate_func=smooth
)

# 每个动画使用不同的速率函数
self.play(
    ShowCreation(circle, rate_func=linear),
    ShowCreation(square, rate_func=rush_into),
    ShowCreation(triangle, rate_func=rush_from)
)
```

## 实际示例

### 文本出现

```python
class TextReveal(Scene):
    def construct(self):
        title = Text("Animated Title", font_size=72)
        subtitle = Text("With smooth appearance", font_size=40)
        subtitle.next_to(title, DOWN)

        # 标题字母逐个出现
        self.play(LaggedStart(
            *[FadeIn(char, shift=UP) for char in title],
            lag_ratio=0.05
        ))
        self.wait(0.3)

        # 副标题淡入
        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait()
```

### 网格动画

```python
class GridAnimation(Scene):
    def construct(self):
        grid = VGroup(*[
            Square(side_length=0.8).shift([i, j, 0])
            for i in range(-3, 4)
            for j in range(-2, 3)
        ])

        # 涟漪效果
        self.play(LaggedStart(
            *[ShowCreation(square) for square in grid],
            lag_ratio=0.02,
            run_time=4
        ))
        self.wait()
```

### 波浪效果

```python
class WaveEffect(Scene):
    def construct(self):
        dots = VGroup(*[
            Dot().shift(i * 0.5 * RIGHT)
            for i in range(-10, 11)
        ])

        # 上下起伏
        def wave_animation(dot, delay):
            return Succession(
                Wait(delay),
                dot.animate.shift(UP),
                dot.animate.shift(DOWN)
            )

        self.add(dots)
        self.play(*[
            wave_animation(dot, i * 0.1)
            for i, dot in enumerate(dots)
        ])
        self.wait()
```

### 级联效果

```python
class CascadeEffect(Scene):
    def construct(self):
        squares = VGroup(*[
            Square(side_length=1).shift(i * 1.5 * DOWN)
            for i in range(-2, 3)
        ])

        # 从上到下级联
        self.play(LaggedStart(
            *[
                AnimationGroup(
                    square.animate.shift(RIGHT * 3),
                    square.animate.set_color(random_color())
                )
                for square in squares
            ],
            lag_ratio=0.3
        ))
        self.wait()
```

## 同时变换

### 多对象变换

```python
class SimultaneousTransforms(Scene):
    def construct(self):
        shapes = VGroup(
            Circle().shift(LEFT * 3),
            Square().shift(LEFT),
            Triangle().shift(RIGHT),
            Star().shift(RIGHT * 3)
        )

        self.play(LaggedStart(
            *[ShowCreation(s) for s in shapes],
            lag_ratio=0.2
        ))
        self.wait()

        # 同时变换所有对象，不同目标
        targets = [
            Square().shift(LEFT * 3),
            Circle().shift(LEFT),
            Star().shift(RIGHT),
            Triangle().shift(RIGHT * 3)
        ]

        self.play(*[
            Transform(s, t)
            for s, t in zip(shapes, targets)
        ])
        self.wait()
```

## 最佳实践

1. **使用 LaggedStart 创造视觉节奏**：产生更动态的动画
2. **lag_ratio 调优**：
   - 0.1-0.3 用于微妙效果
   - 0.5 用于平衡重叠
   - 0.8-1.0 用于近乎顺序
3. **嵌套组**：组合实现复杂编排
4. **总 run_time**：在组上设置以确保一致的时间
5. **不要过度使用**：过多的交错动画可能分散注意力

## 常见模式

### 淡出所有内容

```python
# 交错淡出所有对象
self.play(LaggedStart(
    *[FadeOut(mob) for mob in self.mobjects],
    lag_ratio=0.1
))
```

### 构建复杂图形

```python
# 按顺序构建各部分
self.play(Succession(
    ShowCreation(axes),
    ShowCreation(graph),
    Write(labels),
    FadeIn(legend)
))
```

### 展示图表

```python
# 有节奏地展示组件
components = [background, main_shape, decorations, labels]
self.play(LaggedStart(
    *[FadeIn(c, scale=0.8) for c in components],
    lag_ratio=0.4
))
```

### 同步移动

```python
# 一起移动多个对象
objects = VGroup(circle, square, triangle)
self.play(*[
    obj.animate.shift(RIGHT * 2)
    for obj in objects
])
```

## 完整示例

```python
class ComprehensiveGrouping(Scene):
    def construct(self):
        # 标题
        title = Text("Animation Groups", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # 创建点阵
        dots = VGroup(*[
            Dot(color=interpolate_color(BLUE, RED, i/20))
            .shift([
                (i % 7 - 3) * 0.8,
                (i // 7 - 1.5) * 0.8,
                0
            ])
            for i in range(21)
        ])

        # 交错出现
        self.play(LaggedStart(
            *[FadeIn(dot, scale=0.5) for dot in dots],
            lag_ratio=0.05,
            run_time=3
        ))
        self.wait()

        # 同步颜色变化
        self.play(*[
            dot.animate.set_color(YELLOW)
            for dot in dots
        ])
        self.wait()

        # 级联消失
        self.play(LaggedStart(
            *[FadeOut(dot, shift=DOWN) for dot in dots],
            lag_ratio=0.05,
            run_time=2
        ))

        # 清理
        self.play(FadeOut(title))
        self.wait()
```

## 调试组

### 打印时间信息

```python
# 检查总持续时间
group = LaggedStart(*animations, lag_ratio=0.2)
print(f"Group duration: {group.get_run_time()}")

# 可视化时间
for i, anim in enumerate(animations):
    print(f"Animation {i}: starts at {i * 0.2 * group.get_run_time()}")
```

### 测试 lag_ratio 值

```python
# 尝试不同值以找到合适的感觉
for lag in [0.1, 0.3, 0.5, 0.7]:
    self.play(LaggedStart(*animations, lag_ratio=lag))
    self.wait()
```
