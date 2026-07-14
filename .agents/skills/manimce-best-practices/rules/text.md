---
name: text
description: Manim 中的 Text mobject、字体和文本样式
metadata:
  tags: text, font, typography, markup, paragraph
---

# Manim 中的文本

`Text` 类使用 Pango/Cairo 渲染文本，支持各种字体和样式。

## 基本文本

```python
from manim import *

class TextExample(Scene):
    def construct(self):
        text = Text("Hello World")
        self.play(Write(text))
```

## 文本参数

```python
text = Text(
    "Hello World",
    font_size=48,           # 大小（默认：48）
    color=BLUE,             # 文本颜色
    font="Arial",           # 字体系列
    weight=BOLD,            # NORMAL、BOLD 等
    slant=ITALIC,           # NORMAL、ITALIC、OBLIQUE
    line_spacing=1.5,       # 行间距
)
```

## 字体大小

```python
# 使用 font_size 参数
small = Text("Small", font_size=24)
medium = Text("Medium", font_size=48)
large = Text("Large", font_size=72)

# 创建后使用 scale
text = Text("Hello").scale(2)
```

## 自定义字体

```python
# 使用任何已安装的系统字体
text = Text("Custom Font", font="Comic Sans MS")
text = Text("Monospace", font="Courier New")
text = Text("Serif", font="Times New Roman")
```

## 使用 MarkupText 的文本样式

使用 Pango 标记在单个 Text 对象中实现混合样式：

```python
class MarkupExample(Scene):
    def construct(self):
        text = MarkupText(
            f'all in red <span fgcolor="{YELLOW}">except this</span>',
            color=RED
        )
        self.play(Write(text))
```

### 可用的标记标签

```python
# 粗体和斜体
text = MarkupText('<b>Bold</b> and <i>Italic</i>')

# 使用 fgcolor 指定颜色
text = MarkupText('<span fgcolor="yellow">Yellow</span>')

# 下标和上标
text = MarkupText('H<sub>2</sub>O and x<sup>2</sup>')

# 字体大小
text = MarkupText('<big>Big</big> and <small>small</small>')

# 下划线和删除线
text = MarkupText('<u>Underline</u> and <s>Strike</s>')

# 带颜色的双下划线
text = MarkupText('<span underline="double" underline_color="green">text</span>')

# 等宽字体
text = MarkupText('type <tt>help</tt> for help')
```

### MarkupText 中的渐变

```python
# 全局渐变
text = MarkupText("nice gradient", gradient=(BLUE, GREEN))

# 内联渐变
text = MarkupText(
    'nice <gradient from="RED" to="YELLOW">colored</gradient> text'
)
```

### 转义特殊字符

```python
# 必须转义以下字符：
# > 转义为 &gt;
# < 转义为 &lt;
# & 转义为 &amp;
text = MarkupText("5 &gt; 3 and 2 &lt; 4")
```

## 多行文本

```python
# 使用 \n 换行
text = Text("Line 1\nLine 2\nLine 3")

# 使用 Paragraph 获得更好控制
from manim import Paragraph

para = Paragraph(
    "This is a longer text",
    "that spans multiple lines",
    "with automatic alignment",
    line_spacing=0.5
)
```

## 文本部分着色

```python
class ColoredText(Scene):
    def construct(self):
        text = Text("Hello World")
        text[0:5].set_color(RED)    # "Hello" 用红色
        text[6:11].set_color(BLUE)  # "World" 用蓝色
        self.play(Write(text))
```

## 带渐变的文本

```python
text = Text("Gradient Text")
text.set_color_by_gradient(RED, YELLOW, GREEN)
```

## 访问字符

```python
text = Text("ABCDE")

# 单个字符
text[0]  # 'A'
text[1]  # 'B'

# 切片
text[0:3]  # 'ABC'
text[-1]   # 'E'

# 迭代
for char in text:
    char.set_color(random_color())
```

## 文本定位

```python
# 标准定位方法有效
text = Text("Hello")
text.to_edge(UP)
text.to_corner(UL)
text.move_to(ORIGIN)
text.next_to(other_mobject, DOWN)
```

## 最佳实践

1. **常规文本使用 Text** - 简单且快速
2. **混合样式使用 MarkupText** - 当需要多种颜色/粗细时
3. **数学内容使用 MathTex** - Text 不渲染 LaTeX
4. **系统范围安装字体** - Manim 使用系统字体
5. **保持 font_size 一致** - 相关文本使用相同大小
