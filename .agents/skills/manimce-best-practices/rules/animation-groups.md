---
name: animation-groups
description: AnimationGroup、LaggedStart、Succession 用于复杂动画序列
metadata:
  tags: animationgroup, laggedstart, succession, lag_ratio, sequence
---

# 动画组

控制多个动画如何一起播放。

## AnimationGroup

以可控的时间播放多个动画。

```python
from manim import *

class AnimationGroupExample(Scene):
    def construct(self):
        circles = VGroup(*[Circle() for _ in range(5)]).arrange(RIGHT)

        # 所有动画同时播放（lag_ratio=0）
        self.play(AnimationGroup(
            *[Create(c) for c in circles],
            lag_ratio=0
        ))
```

### lag_ratio 参数

控制动画开始之间的延迟：
- `lag_ratio=0`：所有同时开始
- `lag_ratio=0.5`：每个在上一动画完成50%时开始
- `lag_ratio=1`：每个在上一动画完成时开始（顺序）

```python
class LagRatioDemo(Scene):
    def construct(self):
        squares = VGroup(*[Square() for _ in range(4)]).arrange(RIGHT)

        # 交错开始——每个在上一个完成25%时开始
        self.play(AnimationGroup(
            *[FadeIn(s) for s in squares],
            lag_ratio=0.25,
            run_time=2
        ))
```

## LaggedStart

便捷类，默认 `lag_ratio=0.05`（5%重叠）。

```python
class LaggedStartExample(Scene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(10)]).arrange(RIGHT)

        # 快速交错动画
        self.play(LaggedStart(
            *[GrowFromCenter(d) for d in dots],
            lag_ratio=0.1
        ))
```

### 常见 LaggedStart 模式

```python
# 交错淡入
self.play(LaggedStart(*[FadeIn(m) for m in mobjects], lag_ratio=0.2))

# 波浪效果
self.play(LaggedStart(
    *[m.animate.shift(UP * 0.5) for m in mobjects],
    lag_ratio=0.1
))

# 交错颜色变化
self.play(LaggedStart(
    *[m.animate.set_color(RED) for m in mobjects],
    lag_ratio=0.15
))
```

## Succession

一个接一个地播放动画（等同于 `lag_ratio=1`）。

```python
class SuccessionExample(Scene):
    def construct(self):
        circle = Circle().shift(LEFT * 2)
        square = Square()
        triangle = Triangle().shift(RIGHT * 2)

        # 动画按顺序播放
        self.play(Succession(
            Create(circle),
            Create(square),
            Create(triangle)
        ))
```

### Succession vs 多个 play() 调用

```python
# 以下两者等价：

# 使用 Succession
self.play(Succession(
    Create(circle),
    Create(square)
))

# 使用单独的 play 调用
self.play(Create(circle))
self.play(Create(square))
```

Succession 在您想将顺序动画视为一个整体时很有用。

## 组合组类型

```python
class CombinedExample(Scene):
    def construct(self):
        group1 = VGroup(*[Circle() for _ in range(3)]).arrange(RIGHT).shift(UP)
        group2 = VGroup(*[Square() for _ in range(3)]).arrange(RIGHT).shift(DOWN)

        # 第一组先交错出现，然后第二组
        self.play(Succession(
            LaggedStart(*[Create(c) for c in group1], lag_ratio=0.2),
            LaggedStart(*[Create(s) for s in group2], lag_ratio=0.2)
        ))
```

## LaggedStartMap

将动画应用于 mobject 的所有子对象，带交错时间。

```python
class LaggedStartMapExample(Scene):
    def construct(self):
        dots = VGroup(*[Dot(radius=0.16) for _ in range(35)]).arrange_in_grid(rows=5, cols=7)

        # 对所有点应用 FadeIn，带交错效果
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.1))
        self.wait(0.5)

        # 使用 LaggedStart 交错更改颜色
        self.play(LaggedStart(
            *[dot.animate.set_color(YELLOW) for dot in dots],
            lag_ratio=0.05
        ))
```

LaggedStartMap 更适合将相同动画应用于每个子对象。对于属性更改，请使用 LaggedStart 配合 `.animate`。

## 带 run_time 的 AnimationGroup

总的 `run_time` 根据 `lag_ratio` 在动画之间分配。

```python
self.play(AnimationGroup(
    *[Create(c) for c in circles],
    lag_ratio=0.5,
    run_time=4  # 总持续时间为4秒
))
```

## 实际示例

### 逐词出现文本

```python
class WordByWord(Scene):
    def construct(self):
        words = VGroup(
            Text("Hello"),
            Text("World"),
            Text("!")
        ).arrange(RIGHT)

        self.play(LaggedStart(
            *[Write(w) for w in words],
            lag_ratio=0.5
        ))
```

### 网格动画

```python
class GridAnimation(Scene):
    def construct(self):
        grid = VGroup(*[
            Square().scale(0.3)
            for _ in range(25)
        ]).arrange_in_grid(5, 5)

        # 对角线波浪效果
        self.play(LaggedStart(
            *[GrowFromCenter(s) for s in grid],
            lag_ratio=0.05
        ))
```

## 最佳实践

1. **使用 LaggedStart 提升视觉精致度** - 交错动画看起来更动态
2. **保持 lag_ratio 较小（0.05-0.2）** - 太高会感觉缓慢
3. **不同步骤使用 Succession** - 当动画在概念上分离时
4. **根据 lag_ratio 调整 run_time** - 更多项目可能需要更长的总时间
