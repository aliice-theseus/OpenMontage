# 方程变换 - 参考指南

**示例文件**：`examples/equation_transforms.py`

## 用户查询场景

本示例解决如下查询：
- "展示逐步方程推导"
- "动画化二次公式推导"
- "高亮方程的部分"
- "展示带颜色追踪的变量替换"
- "添加花括号解释方程部分"

## 场景思考过程（3b1b 风格）

### 1. 核心概念
**数学推导**：当项被颜色编码且变换被平滑动画化时，逐步方程操作更清晰。

### 2. 技术实现

#### 使用 t2c 进行颜色编码
```python
eq = Tex(
    r"ax^2 + bx + c = 0",
    t2c={"a": RED, "b": GREEN, "c": BLUE, "x": YELLOW}
)
```

#### 平滑方程变换
```python
eq1 = Tex(r"ax^2 + bx + c = 0", t2c=colors)
eq2 = Tex(r"x^2 + \frac{b}{a}x + \frac{c}{a} = 0", t2c=colors)
self.play(TransformMatchingTex(eq1.copy(), eq2))
```

**关键理解**：`TransformMatchingTex` 匹配方程之间的字符并平滑变形。

#### 使用 SurroundingRectangle 高亮
```python
part = eq[r"a^2"]  # 通过 tex 字符串选择
rect = SurroundingRectangle(part, color=RED, buff=0.05)
self.play(ShowCreation(rect))
```

#### 花括号注释
```python
brace = Brace(eq["F"], UP, color=BLUE)
label = brace.get_text("Force", font_size=30)
self.play(GrowFromCenter(brace), FadeIn(label, UP))
```

### 3. 场景变体

| 场景 | 用途 |
|-------|---------|
| `QuadraticFormula` | 带步骤标签的完整推导 |
| `HighlightAndTransform` | 高亮 + 视觉证明 |
| `BraceAnnotations` | F=ma 带标注部分 |
| `ColorCodedSubstitution` | 带追踪的 u 替换 |

## 关键模式

### 模式：步骤标签
```python
step_label = Text("Divide by a", font_size=24, color=GREY)
step_label.next_to(eq2, LEFT, buff=0.5)
self.play(FadeIn(step_label, LEFT))
```

### 模式：最终答案框
```python
final = Tex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
box = SurroundingRectangle(final, color=GOLD, buff=0.2)
self.play(ShowCreation(box))
```

### 模式：选择方程部分
```python
# 通过 tex 子串
eq["x^2"]  # 返回匹配 "x^2" 的子对象
eq[r"\frac{b}{a}"]  # LaTeX 命令也可行

# 通过索引
eq[0]  # 第一个字符/组
```

## 运行命令

```bash
manimgl equation_transforms.py QuadraticFormula -w
manimgl equation_transforms.py HighlightAndTransform -w
manimgl equation_transforms.py BraceAnnotations -w
manimgl equation_transforms.py ColorCodedSubstitution -w
```
