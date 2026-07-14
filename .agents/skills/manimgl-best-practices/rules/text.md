# ManimGL 中的文本

ManimGL 通过 `Text` 和 `TexText` 类提供了强大的文本渲染能力。

## Text 类

`Text` 类使用系统字体渲染文本，具有丰富的样式选项。

### 基本文本创建

```python
from manimlib import *

class TextExample(Scene):
    def construct(self):
        # 基本文本
        text = Text("Hello ManimGL")
        self.add(text)
```

### 字体自定义

```python
# 指定字体和大小
text = Text("Custom Font", font="Consolas", font_size=90)

# 不同部分使用不同字体
text = Text(
    "Mixed fonts example",
    t2f={"Mixed": "Consolas", "fonts": "Arial"}
)
```

### 文本着色

```python
# 为整个文本着色
text = Text("Colored Text", color=BLUE)

# 为特定单词着色
text = Text(
    "The quick brown fox",
    t2c={"quick": BLUE, "brown": ORANGE, "fox": GREEN}
)
```

### 文本样式

```python
# 倾斜（斜体）
text = Text(
    "Italic and bold text",
    t2s={"Italic": ITALIC},
    t2w={"bold": BOLD}
)

# 组合颜色、字体、倾斜和粗细
text = Text(
    "Fully styled text",
    font="Arial",
    font_size=48,
    t2c={"styled": RED},
    t2s={"styled": ITALIC},
    t2w={"text": BOLD},
    t2f={"text": "Consolas"}
)
```

## TexText 类

`TexText` 将 LaTeX 渲染与文本结合，适用于混合文本和数学。

### 基本 TexText

```python
# 带 LaTeX 支持的文本
text = TexText("The integral $\\int_0^1 x^2 dx$ equals $\\frac{1}{3}$")

# 带字体大小
text = TexText("Hello World", font_size=72)

# 隔离部分用于着色
text = TexText(
    "Einstein's $E = mc^2$",
    isolate=["E", "m", "c"]
)
text.set_color_by_tex("E", BLUE)
text.set_color_by_tex("m", GREEN)
text.set_color_by_tex("c", YELLOW)
```

## Text vs TexText

- **Text**：使用系统字体，不支持 LaTeX，更好的字体控制
- **TexText**：支持数学符号的 LaTeX，使用 LaTeX 的文本渲染

### 何时使用哪种

```python
# 自定义字体纯文本用 Text
title = Text("Machine Learning", font="Helvetica", font_size=60)

# 混合文本和内联数学用 TexText
description = TexText("The function $f(x) = x^2$ is convex")

# 纯数学表达式用 Tex
formula = Tex(R"\sum_{i=1}^n i = \frac{n(n+1)}{2}")
```

## 文本定位

```python
# 基本定位
text = Text("Top")
text.to_edge(UP)

# 排列多个文本
title = Text("Title")
subtitle = Text("Subtitle", font_size=36)
VGroup(title, subtitle).arrange(DOWN, buff=0.5)

# 设置宽度
text = Text("Long text that needs to fit")
text.set_width(FRAME_WIDTH - 1)
```

## 带背景的文本

```python
# 设置背光描边提升可读性
text = Text("With Background", font_size=60)
text.set_backstroke(BLACK, width=5)

# 手动背景矩形
from manimlib.mobject.svg.tex_mobject import BackgroundRectangle
text = Text("Text")
bg = BackgroundRectangle(text, color=BLACK, fill_opacity=0.8)
self.add(bg, text)
```

## 文本布局的 VGroup

```python
# 分组多个文本对象
line1 = Text("First line")
line2 = Text("Second line")
line3 = Text("Third line")

paragraph = VGroup(line1, line2, line3)
paragraph.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
paragraph.to_edge(LEFT)
```

## 完整示例

```python
class ComprehensiveTextExample(Scene):
    def construct(self):
        # 自定义字体标题
        title = Text(
            "Text Rendering in ManimGL",
            font="Arial",
            font_size=72,
            color=BLUE
        )
        title.to_edge(UP)

        # 混合样式的描述
        desc = Text(
            "Mix different fonts, colors, and styles",
            font="Helvetica",
            font_size=36,
            t2c={"fonts": RED, "colors": GREEN, "styles": YELLOW},
            t2w={"Mix": BOLD}
        )
        desc.next_to(title, DOWN, buff=0.5)

        # 使用 TexText 的数学描述
        math_desc = TexText(
            "For equations like $E = mc^2$, use Tex or TexText",
            font_size=30
        )
        math_desc.next_to(desc, DOWN, buff=1)

        # 带动画添加所有内容
        self.play(Write(title))
        self.play(FadeIn(desc, shift=DOWN))
        self.play(Write(math_desc))
        self.wait()
```

## 最佳实践

1. **字体可用性**：确保字体已安装在系统上
2. **使用 Text 制作 UI 元素**：更好地控制外观
3. **使用 TexText 处理混合内容**：当需要同时显示文本和数学时
4. **背光描边提高可见性**：在复杂背景上添加背光描边
5. **使用 VGroup 进行布局**：分组相关文本元素以便于定位
6. **t2c/t2f/t2s/t2w**：使用字典进行逐词样式设置

## 常见模式

### 创建带背景的文本标签

```python
def create_label(text_str, color=WHITE):
    label = Text(text_str, font_size=40, color=color)
    label.set_backstroke(BLACK, width=5)
    return label
```

### 带对齐的多行文本

```python
lines = [Text(line) for line in [
    "Line 1",
    "Longer line 2",
    "Line 3"
]]
paragraph = VGroup(*lines)
paragraph.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
```

### 高亮文本

```python
sentence = Text(
    "This word is highlighted",
    t2c={"highlighted": YELLOW},
    t2w={"highlighted": BOLD}
)
```
