---
name: text-animations
description: Write、AddTextLetterByLetter、TypeWithCursor 文本动画
metadata:
  tags: text, write, typing, letter, cursor, animation
---

# 文本动画

专门为文本和方程设计的动画。

## Write

最常见的文本动画。模拟手写效果。

```python
from manim import *

class WriteExample(Scene):
    def construct(self):
        text = Text("Hello World")
        equation = MathTex(r"E = mc^2")

        self.play(Write(text))
        self.wait()
        self.play(Write(equation))
```

### Write 参数

```python
self.play(Write(
    text,
    run_time=2,           # 覆盖自动计算的时间
    rate_func=linear,     # 时间曲线
    reverse=False,        # 如果为 True，则反向书写
))
```

Write 会根据文本长度自动调整 `run_time`。

## AddTextLetterByLetter

逐字键入文本。

```python
class LetterByLetterExample(Scene):
    def construct(self):
        text = Text("Typing effect")

        self.play(AddTextLetterByLetter(
            text,
            time_per_char=0.1  # 打字速度
        ))
```

**注意：** 仅适用于 `Text`，不适用于 `MathTex`。

## RemoveTextLetterByLetter

AddTextLetterByLetter 的反向——逐字移除。

```python
class RemoveLetterByLetter(Scene):
    def construct(self):
        text = Text("Disappearing text")
        self.add(text)

        self.play(RemoveTextLetterByLetter(
            text,
            time_per_char=0.05
        ))
```

## TypeWithCursor

带可见光标的打字效果。

```python
class TypeWithCursorExample(Scene):
    def construct(self):
        text = Text("Typing with cursor")

        # 创建光标
        cursor = Rectangle(
            color=GREY_A,
            fill_color=GREY_A,
            fill_opacity=1.0,
            height=1.1,
            width=0.1,
        )

        self.play(TypeWithCursor(text, cursor))

        # 可选：打字后闪烁光标
        self.play(Blink(cursor, blinks=3))
```

### 光标自定义

```python
# 线形光标
cursor = Line(UP * 0.5, DOWN * 0.5, color=WHITE, stroke_width=2)

# 块状光标
cursor = Rectangle(width=0.5, height=1, fill_opacity=0.8, color=WHITE)

# 自定义光标位置
self.play(TypeWithCursor(
    text,
    cursor,
    buff=0.05,           # 文本和光标之间的间距
    keep_cursor_y=True,  # 保持光标高度一致
    leave_cursor_on=True # 动画后显示光标
))
```

## Blink（用于光标）

```python
class BlinkExample(Scene):
    def construct(self):
        cursor = Rectangle(height=1, width=0.1, fill_opacity=1)
        self.add(cursor)

        self.play(Blink(cursor, blinks=5, time_on=0.3, time_off=0.3))
```

## 逐词动画

使用 LaggedStart 实现逐词出现：

```python
class WordByWord(Scene):
    def construct(self):
        # 拆分为独立的 Text 对象
        words = VGroup(
            Text("Hello"),
            Text("World"),
            Text("!")
        ).arrange(RIGHT, buff=0.3)

        self.play(LaggedStart(
            *[Write(word) for word in words],
            lag_ratio=0.5
        ))
```

## 方程变换

在方程之间进行动画：

```python
class EquationTransform(Scene):
    def construct(self):
        eq1 = MathTex(r"a^2 + b^2 = c^2")
        eq2 = MathTex(r"c = \sqrt{a^2 + b^2}")

        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
```

## 高亮文本

```python
class HighlightText(Scene):
    def construct(self):
        text = Text("Important message")
        self.add(text)

        # Circumscribe（在周围绘制）
        self.play(Circumscribe(text, color=YELLOW))

        # Indicate（脉冲）
        self.play(Indicate(text, color=RED))

        # Flash（闪烁）
        self.play(Flash(text.get_center(), color=WHITE))
```

## 替换文本

```python
class ReplaceText(Scene):
    def construct(self):
        text1 = Text("Before")
        text2 = Text("After")

        self.play(Write(text1))
        self.wait()

        # 变换文本
        self.play(Transform(text1, text2))

        # 或替换变换
        self.play(ReplacementTransform(text1, text2))
```

## 彩色文本动画

```python
class ColoredTextAnimation(Scene):
    def construct(self):
        text = Text("Colorful")
        self.play(Write(text))

        # 每个字母的颜色变化动画
        self.play(LaggedStart(
            *[char.animate.set_color(random_bright_color()) for char in text],
            lag_ratio=0.1
        ))
```

## 最佳实践

1. **大多数文本使用 Write** - 自然且平滑
2. **"打字"效果使用 AddTextLetterByLetter** - 终端/代码美学
3. **交互感受使用 TypeWithCursor** - 适合教程
4. **方程使用 TransformMatchingTex** - 平滑的数学过渡
5. **调整 time_per_char 控制节奏** - 0.05-0.1 通常不错
6. **逐字效果只使用 Text（非 MathTex）** - API 限制
