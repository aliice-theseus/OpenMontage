# ManimGL 中的颜色

ManimGL 提供了广泛的颜色支持，包括内置颜色常量、渐变和颜色操作工具。

## 颜色常量

### 基本颜色

```python
# 三原色
RED, GREEN, BLUE
YELLOW, CYAN, MAGENTA

# 灰度
WHITE, GREY, GRAY, BLACK

# 常用颜色
ORANGE, PURPLE, PINK, BROWN
MAROON, TEAL, GOLD
```

### 颜色变体

ManimGL 提供带有字母后缀的颜色渐变：

```python
# 蓝色变体（最暗到最亮）
BLUE_E  # 最暗的蓝
BLUE_D
BLUE_C
BLUE_B
BLUE_A  # 最亮的蓝

# 其他颜色同理：
RED_E, RED_D, RED_C, RED_B, RED_A
GREEN_E, GREEN_D, GREEN_C, GREEN_B, GREEN_A
YELLOW_E, YELLOW_D, YELLOW_C, YELLOW_B, YELLOW_A
```

### 使用示例

```python
from manimlib import *

class ColorExample(Scene):
    def construct(self):
        # 用不同颜色变体创建圆
        circles = VGroup(*[
            Circle(radius=0.5, color=color)
            for color in [BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A]
        ])
        circles.arrange(RIGHT, buff=0.5)
        self.add(circles)
```

## 设置颜色

### 基本颜色设置

```python
# 创建时设置
circle = Circle(color=BLUE)

# 创建后设置
square = Square()
square.set_color(RED)

# 多个 mobject
group = VGroup(Circle(), Square(), Triangle())
group.set_color(GREEN)
```

### 动画化颜色变化

```python
class ColorAnimation(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        self.add(circle)

        # 动画化颜色变化
        self.play(circle.animate.set_color(RED))
        self.wait()

        # 再次变化
        self.play(circle.animate.set_color(YELLOW))
        self.wait()
```

## 渐变

### set_submobject_colors_by_gradient

```python
# 对子对象应用渐变
text = Text("Gradient Text")
text.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW)

# 多个对象的渐变
squares = VGroup(*[Square() for _ in range(10)])
squares.arrange(RIGHT)
squares.set_submobject_colors_by_gradient(RED, BLUE)
```

### 颜色插值

```python
from manimlib.utils.color import interpolate_color

# 创建两种颜色之间的中间色
mid_color = interpolate_color(RED, BLUE, 0.5)  # 紫色

# 通过代码创建渐变
n_colors = 10
gradient = [
    interpolate_color(RED, BLUE, alpha)
    for alpha in np.linspace(0, 1, n_colors)
]
```

## 高级颜色技巧

### set_color_by_code（GLSL）

ManimGL 允许使用 GLSL 代码进行动态着色：

```python
# 基于位置着色
square = Square()
square.set_color_by_code("""
    color.r = x;
    color.g = y;
    color.b = 1.0;
""")
```

### set_color_by_xyz_func

```python
# 基于3D位置着色
surface = Sphere(radius=2)
surface.set_color_by_xyz_func(
    glsl_snippet="float value = sqrt(x*x + y*y + z*z); return value;",
    min_value=0,
    max_value=5,
    colormap='viridis'
)
```

## 文本和 LaTeX 的颜色

### 文本部分着色

```python
# 为特定单词着色
text = Text(
    "Red, Green, and Blue",
    t2c={"Red": RED, "Green": GREEN, "Blue": BLUE}
)
```

### LaTeX 着色

```python
# 为数学符号着色
equation = Tex(
    R"E = mc^2",
    t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
)

# 按 tex 子字符串着色
formula = Tex(R"\int_0^1 x^2 dx")
formula.set_color_by_tex("x", BLUE)
formula.set_color_by_tex(R"\int", RED)
```

## RGB 和十六进制颜色

### 使用 RGB 值

```python
from manimlib.utils.color import rgb_to_color

# RGB 值（0-1 范围）
custom_color = rgb_to_color([0.5, 0.3, 0.8])
circle = Circle(color=custom_color)

# 从 0-255 范围的 RGB（转换为 0-1）
custom_color = rgb_to_color([128/255, 77/255, 204/255])
```

### 使用十六进制颜色

```python
from manimlib.utils.color import hex_to_rgb, rgb_to_color

# 十六进制颜色
hex_color = "#FF5733"
rgb = hex_to_rgb(hex_color)
color = rgb_to_color(rgb)

circle = Circle(color=color)
```

## 不透明度和透明

### 设置不透明度

```python
# 透明圆
circle = Circle(color=BLUE, fill_opacity=0.5)

# 改变不透明度
circle.set_opacity(0.7)

# 填充 vs 描边不透明度
square = Square()
square.set_fill(BLUE, opacity=0.5)
square.set_stroke(WHITE, width=4, opacity=1.0)
```

## 颜色工具

### 从 Mobject 获取颜色

```python
circle = Circle(color=BLUE)

# 获取颜色
color = circle.get_color()

# 获取填充颜色
fill_color = circle.get_fill_color()

# 获取描边颜色
stroke_color = circle.get_stroke_color()
```

### 颜色匹配

```python
# 匹配另一个 mobject 的颜色
circle = Circle(color=BLUE)
square = Square()
square.match_color(circle)

# 匹配填充颜色
square.match_fill(circle)

# 匹配描边
square.match_stroke(circle)
```

## 配色方案

### 创建一致的颜色调色板

```python
# 定义配色方案
COLOR_SCHEME = {
    "background": "#1e1e1e",
    "primary": BLUE_C,
    "secondary": GREEN_C,
    "accent": YELLOW_C,
    "text": WHITE,
    "highlight": RED_C
}

# 在场景中使用
class StyledScene(Scene):
    def construct(self):
        title = Text("Title", color=COLOR_SCHEME["primary"])
        subtitle = Text("Subtitle", color=COLOR_SCHEME["secondary"])
        highlight = Circle(color=COLOR_SCHEME["accent"])

        self.add(title, subtitle, highlight)
```

### 3Blue1Brown 配色方案

```python
# Grant 的典型颜色
BLUE_3B1B = BLUE_C
GREEN_3B1B = GREEN_C
YELLOW_3B1B = YELLOW_C
RED_3B1B = RED_C

# 背景色
BACKGROUND_COLOR = "#0a0a0a"
```

## 光泽和视觉属性

### 添加光泽（用于3D）

```python
# 添加光泽效果
sphere = Sphere(radius=2, color=BLUE)
sphere.set_gloss(0.8)  # 0 到 1

# 获取光泽值
gloss = sphere.get_gloss()
```

### 阴影

```python
# 添加阴影（用于3D）
cube = Cube(color=RED)
cube.set_shadow(0.5)  # 0 到 1

# 获取阴影值
shadow = cube.get_shadow()
```

## 完整颜色示例

```python
class ComprehensiveColorExample(Scene):
    def construct(self):
        # 颜色变体展示
        blue_shades = VGroup(*[
            Circle(radius=0.4, color=color)
            for color in [BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A]
        ])
        blue_shades.arrange(RIGHT, buff=0.3)
        blue_shades.to_edge(UP, buff=1)

        # 渐变
        squares = VGroup(*[Square(side_length=0.6) for _ in range(8)])
        squares.arrange(RIGHT, buff=0.2)
        squares.set_submobject_colors_by_gradient(RED, YELLOW, GREEN, BLUE)

        # 自定义 RGB 颜色
        custom_circle = Circle(
            radius=1,
            color=rgb_to_color([0.8, 0.2, 0.6]),
            fill_opacity=0.7
        )
        custom_circle.shift(DOWN * 2)

        # 彩色文本
        text = Text(
            "Colorful Text",
            font_size=48,
            t2c={"Colorful": BLUE, "Text": GREEN}
        )
        text.next_to(custom_circle, UP, buff=0.5)

        # 添加所有内容
        self.play(
            FadeIn(blue_shades, lag_ratio=0.1),
            FadeIn(squares, lag_ratio=0.1),
            ShowCreation(custom_circle),
            Write(text)
        )
        self.wait()

        # 动画化颜色变化
        self.play(
            squares.animate.set_submobject_colors_by_gradient(PURPLE, ORANGE),
            custom_circle.animate.set_color(TEAL)
        )
        self.wait()
```

## 最佳实践

1. **使用命名常量**：优先使用 `BLUE` 而非 RGB 值，以获得更好的可读性
2. **一致的配色方案**：定义颜色调色板以获得连贯的视觉效果
3. **渐变用于强调**：使用渐变展示递进或关系
4. **透明度用于分层**：使用透明度展示重叠元素
5. **颜色可访问性**：确保足够的对比度以便可见
6. **t2c 用于 LaTeX**：为数学表达式着色以高亮重要部分
7. **不要过度使用**：过多的颜色可能分散注意力

## 常见模式

### 彩虹渐变

```python
def rainbow_gradient(mobjects):
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    VGroup(*mobjects).set_submobject_colors_by_gradient(*colors)
```

### 渐变为某种颜色的动画

```python
self.play(
    circle.animate.set_color(RED),
    run_time=2
)
```

### 颜色循环

```python
colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
for color in colors:
    self.play(circle.animate.set_color(color), run_time=0.5)
    self.wait(0.2)
```
