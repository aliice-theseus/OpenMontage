---
name: latex
description: Manim 中的 MathTex、Tex、LaTeX 渲染和方程样式
metadata:
  tags: latex, mathtex, tex, equation, formula, math
---

# Manim 中的 LaTeX

Manim 使用 LaTeX 渲染数学表达式和格式化文本。

## MathTex vs Tex

- **MathTex**：自动将内容包裹在数学模式中（`align*` 环境）
- **Tex**：原始 LaTeX——由您控制模式

```python
from manim import *

class LaTeXComparison(Scene):
    def construct(self):
        # MathTex - 自动数学模式
        math = MathTex(r"E = mc^2")

        # Tex - 需要显式数学定界符
        tex = Tex(r"$E = mc^2$")

        # 两者渲染结果相同
        VGroup(math, tex).arrange(DOWN)
        self.add(math, tex)
```

## 基本 MathTex

```python
class MathTexExample(Scene):
    def construct(self):
        # 简单方程
        eq1 = MathTex(r"x^2 + y^2 = z^2")

        # 分数
        eq2 = MathTex(r"\frac{a}{b}")

        # 平方根
        eq3 = MathTex(r"\sqrt{2}")

        # 希腊字母
        eq4 = MathTex(r"\alpha + \beta = \gamma")

        # 积分
        eq5 = MathTex(r"\int_0^\infty e^{-x} dx")

        # 求和
        eq6 = MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n^2}")

        equations = VGroup(eq1, eq2, eq3, eq4, eq5, eq6).arrange_in_grid(2, 3)
        self.add(equations)
```

## 方程部分着色

### 使用 set_color_by_tex

```python
class ColoredEquation(Scene):
    def construct(self):
        eq = MathTex(r"e^{i\pi} + 1 = 0")
        eq.set_color_by_tex("e", RED)
        eq.set_color_by_tex(r"\pi", BLUE)
        eq.set_color_by_tex("i", GREEN)
        self.add(eq)
```

### 使用 substrings_to_isolate

为精确保留着色，先隔离子字符串：

```python
class IsolatedColoring(Scene):
    def construct(self):
        eq = MathTex(
            r"e^x = x^0 + x^1 + \frac{1}{2}x^2 + \cdots",
            substrings_to_isolate=["x"]
        )
        eq.set_color_by_tex("x", YELLOW)
        self.add(eq)
```

### 使用 index_labels 进行调试

```python
class DebugLabels(Scene):
    def construct(self):
        eq = MathTex(r"\frac{a}{b}")
        # 添加索引标签以查看哪部分是哪个索引
        self.add(index_labels(eq[0]))
        self.add(eq)
```

### 直接索引

```python
eq = MathTex(r"a + b = c")
eq[0][0].set_color(RED)   # 'a'
eq[0][2].set_color(BLUE)  # 'b'
eq[0][4].set_color(GREEN) # 'c'
```

## 多部分方程

将方程拆分为多个部分以便单独控制：

```python
class MultiPartEquation(Scene):
    def construct(self):
        eq = MathTex("a", "^2", "+", "b", "^2", "=", "c", "^2")

        eq[0].set_color(RED)    # a
        eq[3].set_color(BLUE)   # b
        eq[6].set_color(GREEN)  # c

        self.play(Write(eq))
```

## 文本与数学混合（Tex）

```python
class MixedContent(Scene):
    def construct(self):
        # 混合文本和数学
        tex = Tex(r"The area is $A = \pi r^2$")
        self.play(Write(tex))
```

## 自定义 LaTeX 宏包

```python
class CustomPackage(Scene):
    def construct(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{mathrsfs}")

        eq = Tex(
            r"$\mathscr{L}$",
            tex_template=template
        )
        self.add(eq)
```

## 方程对齐

```python
class AlignedEquations(Scene):
    def construct(self):
        eqs = MathTex(
            r"a &= b + c \\",
            r"d &= e + f + g \\",
            r"h &= i"
        )
        self.add(eqs)
```

## 常用 LaTeX 符号

```python
# 希腊字母
MathTex(r"\alpha \beta \gamma \delta \epsilon")
MathTex(r"\Gamma \Delta \Theta \Lambda \Pi")

# 运算符
MathTex(r"\times \div \pm \mp \cdot")

# 关系符
MathTex(r"\leq \geq \neq \approx \equiv")

# 箭头
MathTex(r"\rightarrow \leftarrow \Rightarrow \Leftrightarrow")

# 集合
MathTex(r"\in \notin \subset \supset \cup \cap")

# 微积分
MathTex(r"\int \iint \oint \partial \nabla")
```

## 字体大小

```python
# 使用 font_size 参数
eq = MathTex(r"E = mc^2", font_size=72)

# 使用 scale
eq = MathTex(r"E = mc^2").scale(2)
```

## 最佳实践

1. **使用原始字符串** - 始终使用 `r"..."` 表示 LaTeX
2. **纯数学使用 MathTex** - 比添加 `$...$` 更简单
3. **混合内容使用 Tex** - 当组合文本和数学时
4. **拆分以便动画控制** - 将要单独动画化的部分分开
5. **使用 substrings_to_isolate** - 可靠地为重复元素着色
