# ManimGL 中的 Tex 到颜色映射（t2c）

`t2c` 参数（tex_to_color_map）是一个强大的功能，用于为 LaTeX 表达式的特定部分着色。

## 基本 t2c 用法

### 为数学符号着色

```python
from manimlib import *

class T2CExample(Scene):
    def construct(self):
        # 为特定变量着色
        equation = Tex(
            R"E = mc^2",
            t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
        )
        self.add(equation)
```

### 为子串着色

```python
# 为公式的部分着色
formula = Tex(
    R"\int_0^1 x^2 \, dx = \frac{1}{3}",
    t2c={
        R"\int": BLUE,
        "x": GREEN,
        R"\frac{1}{3}": YELLOW
    }
)
```

## 高级 t2c 模式

### 为多个实例着色

```python
# 变量的所有实例都会着色
series = Tex(
    R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
    t2c={
        "n": BLUE,     # 为所有 'n' 着色
        R"\pi": RED,
        R"\sum": GREEN
    }
)
```

### 将 isolate 与 t2c 结合使用

```python
# 隔离特定部分以便单独控制
equation = Tex(
    R"a^2 + b^2 = c^2",
    isolate=["a", "b", "c", "^2"],
    t2c={
        "a": RED,
        "b": GREEN,
        "c": BLUE,
        "^2": YELLOW
    }
)
```

## 动态着色

### set_color_by_tex

```python
# 创建后着色
formula = Tex(R"f(x) = x^2 + 2x + 1")
formula.set_color_by_tex("x", BLUE)
formula.set_color_by_tex("f", GREEN)
formula.set_color_by_tex("1", YELLOW)
```

### 渐变着色

```python
# 为整个公式应用渐变
formula = Tex(R"\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}")
formula.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW)
```

## 文本着色（Text 类）

### Text 对象的 t2c

```python
# 为 Text 中的单词着色
text = Text(
    "The quick brown fox jumps",
    t2c={
        "quick": BLUE,
        "brown": ORANGE,
        "fox": GREEN
    }
)
```

### 多种样式选项

```python
# 组合 t2c、t2f、t2s、t2w
text = Text(
    "Different styles and colors",
    t2c={"Different": RED, "colors": BLUE},
    t2f={"styles": "Consolas"},
    t2s={"styles": ITALIC},
    t2w={"Different": BOLD}
)
```

## 复杂示例

### 带颜色编码的物理方程

```python
class ColoredPhysicsEquation(Scene):
    def construct(self):
        # 带颜色编码组件的麦克斯韦方程
        maxwell = Tex(
            R"\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}",
            t2c={
                R"\nabla": BLUE,
                R"\vec{E}": RED,
                R"\vec{B}": GREEN,
                "t": YELLOW
            }
        )
        self.play(Write(maxwell))
        self.wait()
```

### 逐步推导

```python
class ColoredDerivation(Scene):
    def construct(self):
        # 初始方程
        eq1 = Tex(
            R"(a + b)^2 = a^2 + 2ab + b^2",
            t2c={"a": BLUE, "b": GREEN}
        )

        # 展开形式
        eq2 = Tex(
            R"(a + b)^2 = (a + b)(a + b)",
            t2c={"a": BLUE, "b": GREEN}
        )

        # 展示变换
        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
```

### 高亮特定项

```python
class HighlightTerms(Scene):
    def construct(self):
        # 高亮判别式的二次公式
        formula = Tex(
            R"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            t2c={
                "x": WHITE,
                "b": BLUE,
                "a": GREEN,
                "c": YELLOW,
                R"b^2 - 4ac": RED  # 判别式为红色
            }
        )

        # 为判别式添加标签
        discriminant_label = Text("判别式", color=RED, font_size=30)
        discriminant_label.next_to(formula, DOWN)

        self.play(Write(formula))
        self.play(FadeIn(discriminant_label, shift=UP))
        self.wait()
```

## 为 LaTeX 运算符着色

```python
# 为不同的运算符类型着色
expression = Tex(
    R"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}",
    t2c={
        R"\int": BLUE,          # 积分号
        "e": GREEN,              # 指数
        R"\pi": RED,            # 圆周率
        "x": YELLOW,            # 变量
        "2": ORANGE             # 指数
    }
)
```

## 最佳实践

1. **使用原始字符串 R**：在 ManimGL 中始终使用 `R"..."` 表示 LaTeX 字符串
2. **先测试 isolate**：使用 `isolate=` 验证哪些部分可以独立着色
3. **一致的配色方案**：使用有意义的颜色（如变量用蓝色，常量用绿色）
4. **不要过度着色**：太多颜色可能分散注意力
5. **用颜色突出重点**：高亮希望观众关注的重要部分

## 常见模式

### 为数学创建配色方案

```python
MATH_COLORS = {
    "variables": BLUE,
    "constants": GREEN,
    "operators": YELLOW,
    "results": RED
}

equation = Tex(
    R"x^2 + y^2 = r^2",
    t2c={
        "x": MATH_COLORS["variables"],
        "y": MATH_COLORS["variables"],
        "r": MATH_COLORS["constants"]
    }
)
```

### 动画化颜色变化

```python
class AnimateColorChange(Scene):
    def construct(self):
        formula = Tex(R"f(x) = x^2")

        # 先使用一种颜色
        formula.set_color(BLUE)
        self.add(formula)
        self.wait()

        # 动画化到不同颜色
        self.play(formula.animate.set_color_by_tex("x", RED))
        self.wait()
```

## 故障排除

### 如果 t2c 不起作用：

1. 检查子串是否与 LaTeX 字符串中的内容完全匹配
2. 使用 `isolate=` 分离要着色的部分
3. 记住 LaTeX 中的空格是有意义的
4. 使用原始字符串 `R"..."` 而不是普通字符串

### 常见问题示例：

```python
# 如果空格不匹配，可能无效：
wrong = Tex(R"a+b", t2c={"a + b": RED})  # 不会匹配 "a+b"

# 这样可以：
right = Tex(R"a + b", t2c={"a": RED, "b": BLUE})
```
