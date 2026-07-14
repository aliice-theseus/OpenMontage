---
name: text
description: 文本 mobjects、字体和 Manim 中的文本样式
metadata:
  tags: text, font, typography, markup, paragraph
---

# Manim 中的文本

`Text` 类使用 Pango/Cairo 渲染文本，支持多种字体和样式。

## 基本文本

```python
from manim import *

class TextExample(Scene):
    def construct(self):
        text = Text("你好世界")
        self.play(Write(text))
```

## 文本参数

```python
text = Text(
    "你好世界",
    font_size=48,           # 字号（默认：48）
    color=BLUE,             # 文本颜色
    font="Arial",           # 字体系列
    weight=BOLD,            # NORMAL, BOLD 等
    slant=ITALIC,           # NORMAL, ITALIC, OBLIQUE
    line_spacing=1.5,       # 行间距
)
```

## 字号

```python
# 使用 font_size 参数
small = Text("小号", font_size=24)
medium = Text("中号", font_size=48)
large = Text("大号", font_size=72)

# 创建后使用 scale
text = Text("你好").scale(2)
```

## 自定义字体

```python
# 使用任何已安装的系统字体
text = Text("自定义字体", font="SimHei")
text = Text("等宽字体", font="Courier New")
text = Text("衬线字体", font="Times New Roman")
```

## 使用 MarkupText 进行文本样式

使用 Pango 标记语言在一个 Text 对象中实现混合样式：

```python
class MarkupExample(Scene):
    def construct(self):
        text = MarkupText(
            f'全部红色 <span fgcolor="{YELLOW}">除了这个</span>',
            color=RED
        )
        self.play(Write(text))
```

### 可用的标记标签

```python
# 粗体和斜体
text = MarkupText('<b>粗体</b> 和 <i>斜体</i>')

# 使用 fgcolor 设置颜色
text = MarkupText('<span fgcolor="yellow">黄色</span>')

# 下标和上标
text = MarkupText('H<sub>2</sub>O 和 x<sup>2</sup>')

# 字号
text = MarkupText('<big>大</big> 和 <small>小</small>')

# 下划线和删除线
text = MarkupText('<u>下划线</u> 和 <s>删除线</s>')

# 带颜色的双下划线
text = MarkupText('<span underline="double" underline_color="green">文本</span>')

# 等宽字体
text = MarkupText('输入 <tt>help</tt> 获取帮助')
```

### MarkupText 中的渐变

```python
# 全局渐变
text = MarkupText("漂亮的渐变", gradient=(BLUE, GREEN))

# 内联渐变
text = MarkupText(
    '漂亮的 <gradient from="RED" to="YELLOW">彩色</gradient> 文本'
)
```

### 转义特殊字符

```python
# 必须转义以下字符：
# > 为 &gt;
# < 为 &lt;
# & 为 &amp;
text = MarkupText("5 &gt; 3 且 2 &lt; 4")
```

## 多行文本

```python
# 使用 \n 换行
text = Text("第一行\n第二行\n第三行")

# 使用 Paragraph 获得更好控制
from manim import Paragraph

para = Paragraph(
    "这是一段较长的文本",
    "跨越了多行",
    "自动对齐",
    line_spacing=0.5
)
```

## 文本部分着色

```python
class ColoredText(Scene):
    def construct(self):
        text = Text("你好世界")
        text[0:2].set_color(RED)    # "你好" 红色
        text[2:4].set_color(BLUE)   # "世界" 蓝色
        self.play(Write(text))
```

## 渐变色文本

```python
text = Text("渐变文本")
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

# 遍历
for char in text:
    char.set_color(random_color())
```

## 文本定位

```python
# 标准定位方法都适用
text = Text("你好")
text.to_edge(UP)
text.to_corner(UL)
text.move_to(ORIGIN)
text.next_to(other_mobject, DOWN)
```

## 最佳实践

1. **常规文本使用 Text** —— 简单快速
2. **混合样式使用 MarkupText** —— 需要多种颜色/字重时
3. **数学公式使用 MathTex** —— Text 不渲染 LaTeX
4. **全局安装字体** —— Manim 使用系统字体
5. **保持 font_size 一致** —— 相关文本使用相同字号
