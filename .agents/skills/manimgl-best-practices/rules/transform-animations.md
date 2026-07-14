# ManimGL 中的变换动画

变换动画将一个 mobject 变形为另一个，或对 mobject 属性进行动画化更改。

## Transform

基本的 `Transform` 将某个 mobject 改变为看起来像另一个。

### 基本 Transform

```python
from manimlib import *

class BasicTransform(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        self.play(ShowCreation(square))
        self.wait()

        # 将正方形变换为圆形
        self.play(Transform(square, circle))
        self.wait()

        # 注意：变换后，square 看起来像 circle
        # 但它仍然是 square 对象
```

### 关键洞察

在 `Transform(A, B)` 之后：
- 对象 A 保留在场景中
- 对象 A 现在看起来像 B
- 对象 B 未被添加到场景中

## ReplacementTransform

`ReplacementTransform` 用目标替换源。

```python
class ReplacementTransformExample(Scene):
    def construct(self):
        square = Square(color=BLUE)
        circle = Circle(color=RED)

        self.play(ShowCreation(square))
        self.wait()

        # 用圆形替换正方形
        self.play(ReplacementTransform(square, circle))
        self.wait()

        # 之后，场景中保留的是 circle，而不是 square
```

### 何时使用哪种

```python
# 使用 Transform 当：
# - 你想保持同一个 mobject 引用
square.transform_into_circle = lambda: Transform(square, Circle())

# 使用 ReplacementTransform 当：
# - 你想要交换对象
# - 目标对象应该保留
self.play(ReplacementTransform(old_text, new_text))
```

## TransformMatchingTex

通过匹配子字符串来变形 LaTeX 表达式。

```python
class TexTransformExample(Scene):
    def construct(self):
        eq1 = Tex(R"a^2 + b^2 = c^2")
        eq2 = Tex(R"a^2 = c^2 - b^2")

        self.play(Write(eq1))
        self.wait()

        # 匹配部分平滑变换
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
```

### 带颜色映射

```python
class ColoredTexTransform(Scene):
    def construct(self):
        # 设置带颜色的方程
        eq1 = Tex(
            R"(a + b)^2 = a^2 + 2ab + b^2",
            t2c={"a": BLUE, "b": GREEN}
        )
        eq2 = Tex(
            R"(a + b)^2 = (a + b)(a + b)",
            t2c={"a": BLUE, "b": GREEN}
        )

        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
```

### 使用 isolate 参数

```python
# 隔离特定部分以获得更好的匹配
eq1 = Tex(
    R"x^2 + 2x + 1",
    isolate=["x", "^2", "+", "1", "2"]
)
eq2 = Tex(
    R"(x + 1)^2",
    isolate=["x", "^2", "+", "1", "(", ")"]
)

self.play(Write(eq1))
self.wait()
self.play(TransformMatchingTex(eq1, eq2))
```

### 带键映射

```python
# 映射特定子字符串
eq1 = Tex(R"x^2 + y^2 = r^2")
eq2 = Tex(R"a^2 + b^2 = c^2")

self.play(Write(eq1))
self.wait()
self.play(TransformMatchingTex(
    eq1, eq2,
    key_map={
        "x": "a",
        "y": "b",
        "r": "c"
    }
))
```

## TransformMatchingShapes

通过匹配相似形状来变形对象。

```python
class ShapeTransform(Scene):
    def construct(self):
        # 源组
        source = VGroup(
            Circle(radius=0.5, color=BLUE),
            Square(side_length=1, color=GREEN),
            Triangle(color=YELLOW)
        )
        source.arrange(RIGHT, buff=0.5)

        # 目标组
        target = VGroup(
            Circle(radius=1, color=RED),
            Square(side_length=0.5, color=PURPLE),
            Triangle(color=ORANGE)
        )
        target.arrange(DOWN, buff=0.5)

        self.play(ShowCreation(source))
        self.wait()
        self.play(TransformMatchingShapes(source, target))
        self.wait()
```

## MoveToTarget

为 mobject 设置目标状态并进行动画化。

```python
class MoveToTargetExample(Scene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))

        # 设置目标状态
        circle.generate_target()
        circle.target.shift(RIGHT * 3)
        circle.target.scale(2)
        circle.target.set_color(YELLOW)

        # 动画化到目标
        self.play(MoveToTarget(circle))
        self.wait()
```

### 多个目标

```python
# 设置多个带目标的 mobject
square = Square()
triangle = Triangle()

square.generate_target()
square.target.shift(LEFT * 2)

triangle.generate_target()
triangle.target.shift(RIGHT * 2)

self.play(
    MoveToTarget(square),
    MoveToTarget(triangle)
)
```

## FadeTransform

在两个对象之间交叉淡出。

```python
class FadeTransformExample(Scene):
    def construct(self):
        text1 = Text("Hello", font_size=72)
        text2 = Text("World", font_size=72)

        self.play(Write(text1))
        self.wait()

        # 平滑交叉淡出
        self.play(FadeTransform(text1, text2))
        self.wait()
```

## Rotate

旋转 mobject。

```python
# 按角度旋转
square = Square()
self.play(Rotate(square, PI / 2))  # 90度

# 绕某点旋转
self.play(Rotate(square, PI, about_point=ORIGIN))

# 绕轴旋转（用于3D）
self.play(Rotate(cube, PI, axis=RIGHT))
```

## Rotating（连续旋转）

创建连续旋转。

```python
# 连续旋转
square = Square()
self.play(Rotating(square, radians=2*PI, run_time=4))

# 带 updater 的无限旋转
square.add_updater(lambda m, dt: m.rotate(0.1 * dt))
self.wait(10)
```

## ScaleInPlace

在不改变中心位置的情况下缩放。

```python
circle = Circle()
self.play(ScaleInPlace(circle, 2))  # 放大一倍

# 绕某点缩放
self.play(ScaleInPlace(circle, 0.5, about_point=RIGHT))
```

## ApplyMethod

对任何 mobject 方法进行动画化。

```python
# 使用 .animate 语法（推荐）
self.play(circle.animate.shift(RIGHT))
self.play(circle.animate.scale(2))
self.play(circle.animate.set_color(BLUE))

# 旧语法（仍然有效）
self.play(ApplyMethod(circle.shift, RIGHT))
self.play(ApplyMethod(circle.scale, 2))
```

## 复杂变换

### apply_complex_function

使用复数运算进行变换。

```python
class ComplexTransform(Scene):
    def construct(self):
        plane = ComplexPlane()
        plane.add_coordinate_labels(font_size=20)

        # 在复平面上创建形状
        circle = Circle(radius=1, color=BLUE)

        self.add(plane, circle)
        self.wait()

        # 应用复函数（例如 z^2）
        self.play(
            circle.animate.apply_complex_function(lambda z: z**2),
            run_time=3
        )
        self.wait()
```

### apply_function

使用任意函数进行变换。

```python
# 应用自定义变换
grid = NumberPlane()

def wavy_transform(point):
    x, y, z = point
    return np.array([
        x,
        y + 0.5 * np.sin(2 * x),
        z
    ])

self.play(
    grid.animate.apply_function(wavy_transform),
    run_time=3
)
```

## 变换序列

### 多步骤变换

```python
class TransformSequence(Scene):
    def construct(self):
        shapes = [
            Square(color=BLUE),
            Circle(color=GREEN),
            Triangle(color=YELLOW),
            Star(color=RED)
        ]

        current = shapes[0]
        self.play(ShowCreation(current))

        # 逐个变换每个形状
        for next_shape in shapes[1:]:
            self.play(ReplacementTransform(current, next_shape))
            current = next_shape
            self.wait(0.3)
```

### 推导变换

```python
class DerivationTransform(Scene):
    def construct(self):
        # 数学推导
        steps = [
            Tex(R"x^2 - 4 = 0"),
            Tex(R"x^2 = 4"),
            Tex(R"x = \pm 2"),
        ]

        current = steps[0]
        self.play(Write(current))
        self.wait()

        for next_step in steps[1:]:
            next_step.move_to(current)
            self.play(TransformMatchingTex(current.copy(), next_step))
            current = next_step
            self.wait()
```

## 最佳实践

1. **Transform vs ReplacementTransform**：
   - 使用 `Transform` 保持对象引用
   - 使用 `ReplacementTransform` 交换对象

2. **TransformMatchingTex**：
   - 使用 `isolate=` 控制匹配
   - 使用 `key_map=` 进行显式映射
   - 颜色一致性确保平滑过渡

3. **时间控制**：
   - 复杂变换使用更长的 `run_time`
   - 时间匹配内容的重要性

4. **.animate 语法**：
   - 简单变换的首选
   - 更可读且简洁

5. **路径弧度**：
   - 添加 `path_arc=90*DEGREES` 实现曲线变换路径

## 常见模式

### 方程操作

```python
eq = Tex(R"2x + 4 = 10")
self.play(Write(eq))

eq2 = Tex(R"2x = 6")
eq2.move_to(eq)
self.play(TransformMatchingTex(eq.copy(), eq2))

eq3 = Tex(R"x = 3")
eq3.move_to(eq2)
self.play(TransformMatchingTex(eq2.copy(), eq3))
```

### 形状变形

```python
shape = Circle()
self.play(ShowCreation(shape))

for new_shape in [Square(), Triangle(), Star(), Circle()]:
    self.play(Transform(shape, new_shape))
    self.wait(0.5)
```

### 文本替换

```python
text1 = Text("Before")
self.play(Write(text1))

text2 = Text("After")
text2.move_to(text1)
self.play(FadeTransform(text1, text2))
```

## 完整示例

```python
class ComprehensiveTransform(Scene):
    def construct(self):
        # 标题
        title = Text("Transformations", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))

        # 形状变换
        shape = Square(color=BLUE)
        self.play(ShowCreation(shape))
        self.wait()

        self.play(Transform(shape, Circle(color=GREEN)))
        self.wait()

        self.play(Transform(shape, Triangle(color=YELLOW)))
        self.wait()

        # 数学变换
        eq1 = Tex(R"a^2 + b^2 = c^2")
        eq1.next_to(title, DOWN, buff=1)
        self.play(
            FadeOut(shape),
            Write(eq1)
        )
        self.wait()

        eq2 = Tex(R"c = \sqrt{a^2 + b^2}")
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        self.wait()

        # 清理
        self.play(FadeOut(VGroup(title, eq2)))
```
