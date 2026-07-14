---
name: animation-groups
description: AnimationGroup（动画组）、LaggedStart（延时启动）、Succession（顺序播放）用于复杂动画序列
metadata:
  tags: animationgroup, laggedstart, succession, lag_ratio, sequence
---

# 动画组

控制多个动画如何一起播放。

## AnimationGroup

以受控的时序播放多个动画。

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
- `lag_ratio=0.5`：每个在前一个完成 50% 时开始
- `lag_ratio=1`：每个在前一个完成时开始（顺序播放）

```python
class LagRatioDemo(Scene):
    def construct(self):
        squares = VGroup(*[Square() for _ in range(4)]).arrange(RIGHT)

        # 错开开始——每个在前一个完成 25% 时开始
        self.play(AnimationGroup(
            *[FadeIn(s) for s in squares],
            lag_ratio=0.25,
            run_time=2
        ))
```

## LaggedStart

便捷类，默认 `lag_ratio=0.05`（5% 重叠）。

```python
class LaggedStartExample(Scene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(10)]).arrange(RIGHT)

        # 快速错开动画
        self.play(LaggedStart(
            *[GrowFromCenter(d) for d in dots],
            lag_ratio=0.1
        ))
```

### 常用 LaggedStart 模式

```python
# 错开淡入
self.play(LaggedStart(*[FadeIn(m) for m in mobjects], lag_ratio=0.2))

# 波浪效果
self.play(LaggedStart(
    *[m.animate.shift(UP * 0.5) for m in mobjects],
    lag_ratio=0.1
))

# 错开颜色变化
self.play(LaggedStart(
    *[m.animate.set_color(RED) for m in mobjects],
    lag_ratio=0.15
))
```

## Succession

一个接一个地播放动画（相当于 `lag_ratio=1`）。

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
# 以下是等效的：

# 使用 Succession
self.play(Succession(
    Create(circle),
    Create(square)
))

# 使用单独的 play 调用
self.play(Create(circle))
self.play(Create(square))
```

当你想将顺序动画视为一个整体时，Succession 非常有用。

## 组合组类型

```python
class CombinedExample(Scene):
    def construct(self):
        group1 = VGroup(*[Circle() for _ in range(3)]).arrange(RIGHT).shift(UP)
        group2 = VGroup(*[Square() for _ in range(3)]).arrange(RIGHT).shift(DOWN)

        # 第一组错开出现，然后是第二组
        self.play(Succession(
            LaggedStart(*[Create(c) for c in group1], lag_ratio=0.2),
            LaggedStart(*[Create(s) for s in group2], lag_ratio=0.2)
        ))
```

## LaggedStartMap

将动画应用于 mobject 的所有子对象，带错开时序。

```python
class LaggedStartMapExample(Scene):
    def construct(self):
        dots = VGroup(*[Dot(radius=0.16) for _ in range(35)]).arrange_in_grid(rows=5, cols=7)

        # 将 FadeIn 应用于所有点，带错开
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.1))
        self.wait(0.5)

        # 使用 LaggedStart 错开改变颜色
        self.play(LaggedStart(
            *[dot.animate.set_color(YELLOW) for dot in dots],
            lag_ratio=0.05
        ))
```

LaggedStartMap 更简洁，适合对每个子对象应用相同的动画。对于属性变化，使用带 `.animate` 的 LaggedStart。

## AnimationGroup 与 run_time

总的 `run_time` 根据 `lag_ratio` 分布在动画之间。

```python
self.play(AnimationGroup(
    *[Create(c) for c in circles],
    lag_ratio=0.5,
    run_time=4  # 总时长为 4 秒
))
```

## 实用示例

### 逐词文本出现

```python
class WordByWord(Scene):
    def construct(self):
        words = VGroup(
            Text("你好"),
            Text("世界"),
            Text("！")
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

1. **使用 LaggedStart 增加视觉润色** —— 错开动画看起来更动感
2. **保持 lag_ratio 较小（0.05-0.2）** —— 太大感觉缓慢
3. **不同步骤使用 Succession** —— 当动画在概念上是分开的时
4. **根据 lag_ratio 调整 run_time** —— 更多项目可能需要更长的总时间
