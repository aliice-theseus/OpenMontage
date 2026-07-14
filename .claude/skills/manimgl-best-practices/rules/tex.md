# ManimGL LaTeX（Tex 类）

## Tex 与 MathTex 的区别

**重要：** ManimGL 使用 `Tex` 类（而不是 ManimCE 的 `MathTex`）。

```python
# ManimGL - 使用带大写 R 原始字符串的 Tex
formula = Tex(R"\int_0^1 x^2 \, dx = \frac{1}{3}")

# 不要像 ManimCE 那样：
# formula = MathTex(r"\int...")  # 在 ManimGL 中错误
```

## 带大写 R 的原始字符串

始终使用大写 `R` 作为原始字符串，以避免转义问题：

```python
# 正确 — 大写 R
Tex(R"\frac{a}{b}")
Tex(R"\vec{v}")
Tex(R"\sum_{n=1}^{\infty}")

# 也可以用，但可读性较差
Tex("\\frac{a}{b}")
```

## 使用 t2c 进行颜色映射

使用 `t2c`（tex_to_color）参数为特定部分着色：

```python
equation = Tex(
    R"E = mc^2",
    t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
)
```

更复杂的着色：

```python
formula = Tex(
    R"\vec{F} = m\vec{a}",
    t2c={
        R"\vec{F}": BLUE,
        R"\vec{a}": RED,
        "m": GREEN,
    }
)
```

## set_color_by_tex

创建后为部分着色：

```python
formula = Tex(R"\sum_{n=1}^{\infty} \frac{1}{n^2}")
formula.set_color_by_tex("n", BLUE)
formula.set_color_by_tex(R"\infty", YELLOW)
```

## 隔离子串

获取公式的某些部分用于动画：

```python
formula = Tex(R"a^2 + b^2 = c^2")

# 通过索引访问
a_squared = formula[0]  # "a^2"

# 或使用 isolate 参数
formula = Tex(
    R"a^2", "+", R"b^2", "=", R"c^2",
)
# 现在 formula[0] 是 "a^2"，formula[1] 是 "+"，等等
```

## Text 与 Tex 的区别

```python
# 常规文本
text = Text("Hello World")

# LaTeX 数学
math = Tex(R"\pi \approx 3.14159")

# 混合（在数学上下文中使用 TexText）
mixed = TexText("The value of ", R"$\pi$", " is important")
```

## TexText

用于可能包含内联数学的文本：

```python
sentence = TexText(
    "The area is ", R"$\pi r^2$", ".",
    t2c={R"$\pi r^2$": YELLOW}
)
```

## 对齐方程

```python
equations = Tex(R"""
    \begin{align*}
    f(x) &= x^2 + 2x + 1 \\
    &= (x + 1)^2
    \end{align*}
""")
```

## 常用 LaTeX 符号

```python
# 希腊字母
Tex(R"\alpha, \beta, \gamma, \delta, \theta, \phi, \pi")

# 运算符
Tex(R"\sum, \prod, \int, \oint, \partial")

# 关系符
Tex(R"\leq, \geq, \neq, \approx, \equiv")

# 集合
Tex(R"\in, \subset, \cup, \cap, \emptyset")

# 箭头
Tex(R"\rightarrow, \leftarrow, \Rightarrow, \Leftrightarrow")

# 分数
Tex(R"\frac{a}{b}, \dfrac{a}{b}")

# 根号
Tex(R"\sqrt{x}, \sqrt[3]{x}")

# 矩阵
Tex(R"\begin{pmatrix} a & b \\ c & d \end{pmatrix}")
```

## 字体大小

```python
# 使用 font_size 参数
small = Tex(R"\pi", font_size=24)
large = Tex(R"\pi", font_size=72)

# 或创建后缩放
small.scale(1.5)
```

## 用于可读性的背景描边

当文本放在彩色背景上时：

```python
label = Tex(R"f(x)")
label.set_backstroke(BLACK, 5)  # 黑色轮廓
```

## 调试 LaTeX

如果 LaTeX 无法渲染：

1. 检查 LaTeX 安装中是否缺少必要的包
2. 先尝试更简单的表达式
3. 检查输出目录中的中间 `.tex` 文件
4. 在数学环境中使用 `\text{}` 表示常规文本
