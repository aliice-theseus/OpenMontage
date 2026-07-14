---
name: creation-animations
description: Create、Write、FadeIn、DrawBorderThenFill 和其他创建动画
metadata:
  tags: create, write, fadein, fadeout, grow, shrink, uncreate
---

# 创建动画

将 mobject 引入场景的动画。

## Create

沿路径逐步绘制 VMobject。

```python
from manim import *

class CreateExample(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

最适合：几何形状、线条、箭头。

## Write

模拟手写效果。最适合文本和方程。

```python
class WriteExample(Scene):
    def construct(self):
        text = Text("Hello World")
        equation = MathTex(r"E = mc^2")

        self.play(Write(text))
        self.wait()
        self.play(Write(equation))
```

Write 会根据文本长度自动设置适当的时间。

## DrawBorderThenFill

先绘制轮廓，然后填充形状。

```python
class DrawBorderExample(Scene):
    def construct(self):
        square = Square(fill_opacity=0.8, color=BLUE)
        self.play(DrawBorderThenFill(square))
```

最适合：带有填充且希望先强调轮廓的形状。

## FadeIn / FadeOut

简单的不透明度过渡。

```python
class FadeExample(Scene):
    def construct(self):
        circle = Circle()

        # 淡入
        self.play(FadeIn(circle))
        self.wait()

        # 淡出
        self.play(FadeOut(circle))
```

### 方向性淡入淡出

```python
# 从某个方向淡入
self.play(FadeIn(square, shift=UP))      # 向上移动时淡入
self.play(FadeIn(square, shift=LEFT))    # 从右侧淡入

# 向某个方向淡出
self.play(FadeOut(square, shift=DOWN))   # 向下移动时淡出
```

### 缩放淡入淡出

```python
self.play(FadeIn(circle, scale=0.5))   # 生长时淡入
self.play(FadeOut(circle, scale=2))    # 收缩时淡出
```

## GrowFromCenter / ShrinkToCenter

```python
class GrowExample(Scene):
    def construct(self):
        circle = Circle()

        self.play(GrowFromCenter(circle))
        self.wait()
        self.play(ShrinkToCenter(circle))
```

## GrowFromPoint

从指定点生长。

```python
self.play(GrowFromPoint(circle, ORIGIN))
self.play(GrowFromPoint(circle, LEFT * 3))
```

## GrowFromEdge

从指定边缘生长。

```python
self.play(GrowFromEdge(square, LEFT))   # 从左侧边缘生长
self.play(GrowFromEdge(square, DOWN))   # 从底部边缘生长
```

## SpinInFromNothing

对象旋转进入视野的同时生长。

```python
self.play(SpinInFromNothing(circle))
```

## Uncreate

Create 的反向——擦除 mobject。

```python
self.play(Create(circle))
self.wait()
self.play(Uncreate(circle))  # 反向擦除
```

## AddTextLetterByLetter

逐字键入文本。

```python
class TypingExample(Scene):
    def construct(self):
        text = Text("Hello World")
        self.play(AddTextLetterByLetter(text, time_per_char=0.1))
```

注意：仅适用于 `Text`，不适用于 `MathTex`。

## 最佳实践

1. **文本使用 Write** - 看起来比 Create 更自然
2. **形状使用 Create** - 干净的逐步绘制
3. **快速引入使用 FadeIn** - 当绘制不重要时
4. **移除方式匹配创建方式** - 如果用 Create，就用 Uncreate；如果用 FadeIn，就用 FadeOut
