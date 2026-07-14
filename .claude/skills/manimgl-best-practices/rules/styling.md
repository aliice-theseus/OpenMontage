# ManimGL 样式

ManimGL 为 mobject 提供全面的样式选项，包括填充、描边、不透明度和特殊效果。

## 填充属性

### 基本填充

```python
from manimlib import *

# 创建时设置填充
circle = Circle(fill_color=BLUE, fill_opacity=0.7)

# 创建后设置填充
square = Square()
square.set_fill(RED, opacity=0.5)
```

### 填充示例

```python
class FillExample(Scene):
    def construct(self):
        # 实心填充
        solid = Circle(radius=1)
        solid.set_fill(BLUE, opacity=1.0)

        # 透明填充
        transparent = Circle(radius=1)
        transparent.set_fill(GREEN, opacity=0.3)

        # 无填充（仅轮廓）
        outline = Circle(radius=1)
        outline.set_fill(opacity=0)
        outline.set_stroke(YELLOW, width=4)

        VGroup(solid, transparent, outline).arrange(RIGHT, buff=1)
        self.add(solid, transparent, outline)
```

## 描边属性

### 基本描边

```python
# 创建时设置描边
line = Line(stroke_color=WHITE, stroke_width=4)

# 创建后设置描边
circle = Circle()
circle.set_stroke(BLUE, width=3, opacity=0.8)
```

### 描边宽度

```python
# 不同描边宽度
thin = Circle().set_stroke(width=1)
medium = Circle().set_stroke(width=4)
thick = Circle().set_stroke(width=10)

VGroup(thin, medium, thick).arrange(RIGHT, buff=0.5)
```

### 描边在填充后方

```python
# 在填充后方绘制描边（用于边框效果）
shape = Circle(fill_color=BLUE, fill_opacity=0.8)
shape.set_stroke(WHITE, width=6, opacity=1, background=True)
```

## 背景描边（Backstroke）

`backstroke` 功能在文本或形状后方添加轮廓以提高可见性。

```python
# 带背景描边的文本（黑色轮廓）
text = Text("Readable Text", font_size=60)
text.set_backstroke(BLACK, width=5)

# 在复杂背景上效果很好
text.set_backstroke(BLACK, width=8, opacity=1.0)
```

### 背景描边示例

```python
class BackstrokeExample(Scene):
    def construct(self):
        # 创建复杂背景
        background = VGroup(*[
            Circle(radius=2 * np.random.random(), color=random_color())
            for _ in range(20)
        ])
        background.set_opacity(0.3)
        self.add(background)

        # 带背景描边的文本更加突出
        text = Text("Clear and Readable", font_size=72, color=WHITE)
        text.set_backstroke(BLACK, width=10)
        self.add(text)
```

## 不透明度控制

### 填充不透明度

```python
# 控制填充透明度
circle = Circle()
circle.set_fill_opacity(0.5)

# 动画化不透明度
self.play(circle.animate.set_fill_opacity(1.0))
```

### 描边不透明度

```python
# 控制描边透明度
square = Square()
square.set_stroke_opacity(0.7)
```

### 整体不透明度

```python
# 同时设置填充和描边不透明度
mobject = Circle()
mobject.set_opacity(0.5)  # 同时影响填充和描边
```

## 光泽（3D）

### 为 3D 对象添加光泽

```python
# 使对象有光泽/闪亮
sphere = Sphere(radius=2, color=BLUE)
sphere.set_gloss(0.8)  # 0（亚光）到 1（非常光泽）

# 获取光泽值
gloss_value = sphere.get_gloss()
```

## 阴影（3D）

### 添加阴影

```python
# 为 3D 对象添加阴影
cube = Cube(color=RED)
cube.set_shadow(0.6)  # 0（无阴影）到 1（强阴影）

# 获取阴影值
shadow_value = cube.get_shadow()
```

## 组合样式

### 完整的样式控制

```python
class CompleteStyling(Scene):
    def construct(self):
        shape = Circle(radius=2)

        # 设置所有属性
        shape.set_fill(BLUE, opacity=0.7)
        shape.set_stroke(WHITE, width=4, opacity=1.0)
        shape.set_backstroke(BLACK, width=6)

        self.add(shape)
```

## 样式匹配

### 从另一个 Mobject 匹配样式

```python
# 创建样式源
source = Circle()
source.set_fill(BLUE, opacity=0.7)
source.set_stroke(WHITE, width=3)

# 匹配样式
target = Square()
target.match_style(source)  # 复制所有样式

# 匹配特定属性
target2 = Triangle()
target2.match_fill(source)   # 仅复制填充
target2.match_stroke(source) # 仅复制描边
target2.match_color(source)  # 仅复制颜色
```

## 渐变和颜色过渡

### 渐变填充

```python
# 跨子对象的渐变
text = Text("Gradient")
text.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW)

# 用于带子对象的形状
squares = VGroup(*[Square() for _ in range(10)])
squares.arrange(RIGHT)
squares.set_submobject_colors_by_gradient(RED, PURPLE)
```

## 视觉效果

### 发光效果

```python
# 使用多层描边创建发光效果
def add_glow(mobject, color=YELLOW, radius=0.5):
    glow_layers = VGroup(*[
        mobject.copy().set_stroke(
            color,
            width=width,
            opacity=0.3 / (i + 1)
        )
        for i, width in enumerate(range(2, 20, 2))
    ])
    return VGroup(glow_layers, mobject)

# 用法
circle = Circle(color=BLUE)
glowing_circle = add_glow(circle)
```

### 霓虹效果

```python
def neon_style(mobject, color=BLUE):
    mobject.set_fill(color, opacity=0.2)
    mobject.set_stroke(color, width=3)
    mobject.set_backstroke(color, width=10, opacity=0.5)
    return mobject

# 用法
neon_text = neon_style(Text("NEON", font_size=90), BLUE)
```

## 样式预设

### 创建可复用样式

```python
# 定义样式函数
def outline_style(mobject):
    mobject.set_fill(opacity=0)
    mobject.set_stroke(WHITE, width=3)
    return mobject

def solid_style(mobject, color=BLUE):
    mobject.set_fill(color, opacity=1.0)
    mobject.set_stroke(color, width=0)
    return mobject

def glass_style(mobject, color=BLUE):
    mobject.set_fill(color, opacity=0.3)
    mobject.set_stroke(WHITE, width=2, opacity=0.8)
    mobject.set_gloss(0.9)
    return mobject

# 用法
circle1 = outline_style(Circle())
circle2 = solid_style(Circle(), RED)
circle3 = glass_style(Circle(), GREEN)
```

## 动画化样式

### 样式过渡

```python
class StyleAnimation(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE, opacity=0)
        square.set_stroke(WHITE, width=1)

        self.add(square)
        self.wait()

        # 动画化样式变化
        self.play(
            square.animate.set_fill(BLUE, opacity=0.7),
            square.animate.set_stroke(WHITE, width=5)
        )
        self.wait()

        # 改变颜色
        self.play(
            square.animate.set_fill(RED, opacity=0.9),
            square.animate.set_stroke(YELLOW, width=3)
        )
        self.wait()
```

## 完整样式示例

```python
class ComprehensiveStyleExample(Scene):
    def construct(self):
        # 不同样式方法
        shapes = VGroup()

        # 填充形状
        filled = Circle(radius=0.8)
        filled.set_fill(BLUE, opacity=0.8)
        filled.set_stroke(width=0)
        shapes.add(filled)

        # 轮廓形状
        outlined = Circle(radius=0.8)
        outlined.set_fill(opacity=0)
        outlined.set_stroke(WHITE, width=4)
        shapes.add(outlined)

        # 透明带边框
        transparent = Circle(radius=0.8)
        transparent.set_fill(GREEN, opacity=0.3)
        transparent.set_stroke(GREEN, width=3)
        shapes.add(transparent)

        # 带背景描边
        backstroke = Circle(radius=0.8)
        backstroke.set_fill(YELLOW, opacity=0.6)
        backstroke.set_stroke(WHITE, width=2)
        backstroke.set_backstroke(BLACK, width=5)
        shapes.add(backstroke)

        # 渐变（多个子对象）
        gradient_circles = VGroup(*[
            Circle(radius=0.15).shift(i * 0.3 * RIGHT)
            for i in range(-2, 3)
        ])
        gradient_circles.set_submobject_colors_by_gradient(RED, YELLOW)
        shapes.add(gradient_circles)

        # 排列并显示
        shapes.arrange(RIGHT, buff=1)
        self.play(LaggedStart(*[
            FadeIn(shape)
            for shape in shapes
        ], lag_ratio=0.2))
        self.wait()

        # 动画化样式过渡
        self.play(
            filled.animate.set_opacity(0.3),
            outlined.animate.set_stroke(YELLOW, width=8),
            transparent.animate.set_fill(RED, opacity=0.8)
        )
        self.wait()
```

## 最佳实践

1. **用透明度进行分层**：使用透明显示重叠元素
2. **用背景描边提高可读性**：在复杂背景上为文本添加背景描边
3. **一致的描边宽度**：使用一致的宽度维护视觉层级
4. **填充 vs 描边**：用填充表示区域，用描边表示边框
5. **用光泽增加真实感**：为 3D 对象添加光泽使其更逼真
6. **用样式匹配保持一致性**：使用样式匹配实现一致的外观
7. **用渐变表示流动**：使用渐变显示过渡或关系

## 常见模式

### 轮廓样式用于强调

```python
def emphasize(mobject):
    return mobject.set_stroke(YELLOW, width=8, opacity=1.0)
```

### 透明覆盖层

```python
def overlay(mobject, color=BLUE):
    return mobject.set_fill(color, opacity=0.2)
```

### 简洁 UI 样式

```python
def ui_style(mobject):
    mobject.set_fill(BLUE_C, opacity=0.9)
    mobject.set_stroke(WHITE, width=2)
    return mobject
```

### 高亮文本

```python
text = Text("Important", font_size=60)
text.set_fill(YELLOW, opacity=1.0)
text.set_backstroke(BLACK, width=8)
text.set_stroke(WHITE, width=1)
```
