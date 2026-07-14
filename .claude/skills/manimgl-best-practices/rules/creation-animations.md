# ManimGL 中的创建动画

创建动画将 mobject 带入场景。ManimGL 提供了几种动画类来实现不同的创建效果。

## ShowCreation

**注意**：ManimGL 使用 `ShowCreation`，而不是 `Create`（ManimCE 中使用）。

### 基本用法

```python
from manimlib import *

class CreationExample(Scene):
    def construct(self):
        circle = Circle()

        # ShowCreation 绘制对象
        self.play(ShowCreation(circle))
        self.wait()
```

### 不同的 Mobject

```python
# 适用于任何 VMobject
self.play(ShowCreation(Circle()))
self.play(ShowCreation(Square()))
self.play(ShowCreation(Line(LEFT, RIGHT)))
self.play(ShowCreation(Text("Hello")))
```

### 反向创建

```python
# 取消创建（ShowCreation 的逆向）
circle = Circle()
self.add(circle)
self.play(ShowCreation(circle, reverse=True))  # 取消创建
```

## Write

`Write` 动画专门用于文本和 LaTeX。

### 书写文本

```python
# 逐字母书写文本
text = Text("Hello World", font_size=60)
self.play(Write(text))

# 书写 LaTeX
formula = Tex(R"\int_0^1 x^2 dx = \frac{1}{3}")
self.play(Write(formula))
```

### 书写速度

```python
# 使用 run_time 控制书写速度
text = Text("Fast", font_size=72)
self.play(Write(text), run_time=0.5)

text2 = Text("Slow", font_size=72)
self.play(Write(text2), run_time=3)
```

## FadeIn

淡入对象到视野中。

### 基本 FadeIn

```python
circle = Circle()
self.play(FadeIn(circle))
```

### FadeIn 带位移

```python
# 淡入时移动
text = Text("Appearing", font_size=60)
self.play(FadeIn(text, shift=UP))

# 从不同方向
self.play(FadeIn(circle, shift=DOWN))
self.play(FadeIn(square, shift=LEFT))
self.play(FadeIn(triangle, shift=RIGHT))
```

### FadeIn 带缩放

```python
# 淡入时缩放
circle = Circle()
self.play(FadeIn(circle, scale=0.5))  # 从半大开始

# 缩小同时淡入
square = Square()
self.play(FadeIn(square, scale=2))  # 从双倍大开始
```

## DrawBorderThenFill

先绘制边框，再填充形状。

```python
class DrawBorderExample(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE, opacity=0.7)
        square.set_stroke(WHITE, width=4)

        self.play(DrawBorderThenFill(square))
        self.wait()
```

## GrowFromCenter

从中心放大对象。

```python
circle = Circle()
self.play(GrowFromCenter(circle))

# 控制生长速度
square = Square()
self.play(GrowFromCenter(square), run_time=2)
```

## GrowFromEdge

从特定边缘放大对象。

```python
square = Square()

# 从不同边缘放大
self.play(GrowFromEdge(square, DOWN))
# 或：UP, DOWN, LEFT, RIGHT
```

## GrowFromPoint

从特定点放大对象。

```python
circle = Circle()
point = np.array([2, 2, 0])

self.play(GrowFromPoint(circle, point))
```

## SpinInFromNothing

旋转对象进入视野同时放大。

```python
star = Star()
self.play(SpinInFromNothing(star))
```

## AnimationGroup 用于多个创建

### 同时创建

```python
class MultipleCreations(Scene):
    def construct(self):
        shapes = VGroup(
            Circle().shift(LEFT * 2),
            Square(),
            Triangle().shift(RIGHT * 2)
        )

        # 同时创建所有
        self.play(*[ShowCreation(shape) for shape in shapes])
        self.wait()
```

### 顺序创建

```python
# 一个接一个
for shape in shapes:
    self.play(ShowCreation(shape))
    self.wait(0.2)
```

## LaggedStart

使用交错延迟创建对象。

```python
class LaggedCreation(Scene):
    def construct(self):
        circles = VGroup(*[
            Circle(radius=0.5).shift(i * RIGHT)
            for i in range(-3, 4)
        ])

        # 交错创建
        self.play(LaggedStart(
            *[ShowCreation(circle) for circle in circles],
            lag_ratio=0.2  # 每个之间的延迟
        ))
        self.wait()
```

## 创建动画对比

```python
class CreationComparison(Scene):
    def construct(self):
        methods = [
            ("ShowCreation", ShowCreation),
            ("FadeIn", FadeIn),
            ("GrowFromCenter", GrowFromCenter),
            ("DrawBorderThenFill", DrawBorderThenFill),
        ]

        for name, AnimClass in methods:
            # 创建标签
            label = Text(name, font_size=30)
            label.to_edge(UP)

            # 创建形状
            square = Square()
            square.set_fill(BLUE, opacity=0.7)
            square.set_stroke(WHITE, width=3)

            # 展示动画
            self.play(Write(label))
            self.play(AnimClass(square))
            self.wait()
            self.play(FadeOut(VGroup(label, square)))
```

## 高级创建模式

### 部分创建

```python
# 只展示创建的一部分
line = Line(LEFT * 3, RIGHT * 3)
self.play(
    ShowCreation(line),
    rate_func=lambda t: smooth(t * 0.5)  # 只创建 50%
)
```

### 反向速率函数

```python
# 反向创建
circle = Circle()
self.play(
    ShowCreation(circle),
    rate_func=lambda t: 1 - smooth(t)  # 反向
)
```

### 带颜色变化的创建

```python
class ColoredCreation(Scene):
    def construct(self):
        line = Line(LEFT * 3, RIGHT * 3)
        line.set_color_by_gradient(BLUE, RED)

        self.play(ShowCreation(line), run_time=2)
        self.wait()
```

## 书写数学内容

### 书写方程

```python
class WriteEquation(Scene):
    def construct(self):
        equation = Tex(R"E = mc^2")
        equation.scale(2)

        self.play(Write(equation))
        self.wait()

        # 为部分着色
        equation.set_color_by_tex("E", BLUE)
        equation.set_color_by_tex("m", GREEN)
        equation.set_color_by_tex("c", YELLOW)
        self.wait()
```

### 书写多行内容

```python
class MultiLineWrite(Scene):
    def construct(self):
        lines = VGroup(
            Tex(R"a^2 + b^2 = c^2"),
            Tex(R"e^{i\pi} + 1 = 0"),
            Tex(R"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")
        )
        lines.arrange(DOWN, buff=0.5)

        # 逐行书写
        for line in lines:
            self.play(Write(line))
            self.wait(0.5)
```

## 最佳实践

1. **形状用 ShowCreation**：用于几何对象和路径
2. **文本用 Write**：用于 Text 和 Tex 对象
3. **组用 FadeIn**：适合同时引入多个对象
4. **序列用 LaggedStart**：营造视觉节奏
5. **时间一致**：相关对象保持相似的 run_time
6. **动画与内容匹配**：根据上下文使用合适的动画

## 常见模式

### 创建并高亮

```python
shape = Circle()
self.play(ShowCreation(shape))
self.play(shape.animate.set_color(YELLOW))
self.play(shape.animate.scale(1.5))
```

### 顺序文本出现

```python
title = Text("Title", font_size=72)
subtitle = Text("Subtitle", font_size=48)

self.play(Write(title))
self.wait(0.3)
self.play(FadeIn(subtitle, shift=UP))
```

### 网格创建

```python
grid = VGroup(*[
    Square(side_length=0.5).shift([i, j, 0])
    for i in range(-3, 4)
    for j in range(-2, 3)
])

self.play(LaggedStart(
    *[ShowCreation(square) for square in grid],
    lag_ratio=0.01
))
```

## 完整示例

```python
class ComprehensiveCreation(Scene):
    def construct(self):
        # 标题
        title = Text("Creation Animations", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

        # 使用不同动画创建形状
        circle = Circle(radius=1, color=BLUE)
        circle.shift(LEFT * 3)

        square = Square(side_length=2, color=GREEN)
        square.set_fill(GREEN, opacity=0.5)

        triangle = Triangle(color=YELLOW)
        triangle.shift(RIGHT * 3)

        # 交错创建
        self.play(
            ShowCreation(circle),
            FadeIn(square, scale=0.5),
            GrowFromCenter(triangle),
            run_time=2
        )
        self.wait()

        # 添加公式
        formula = Tex(R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}")
        formula.next_to(title, DOWN, buff=1)
        self.play(Write(formula))
        self.wait(2)

        # 清空场景
        self.play(FadeOut(VGroup(title, circle, square, triangle, formula)))
```
