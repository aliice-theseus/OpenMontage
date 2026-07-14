---
name: timing
description: 速率函数、缓动函数、run_time 和动画时序控制
metadata:
  tags: timing, rate_func, easing, smooth, linear, run_time
---

# 动画时序

通过时序参数控制动画的速度和感觉。

## run_time

控制动画持续的时间（秒）。

```python
from manim import *

class RunTimeExample(Scene):
    def construct(self):
        circle = Circle()

        # 默认（1 秒）
        self.play(Create(circle))

        # 较长的动画
        self.play(circle.animate.shift(RIGHT), run_time=3)

        # 快速动画
        self.play(circle.animate.set_color(RED), run_time=0.5)
```

## 速率函数

速率函数控制动画随时间推进的方式（缓动）。

### 使用速率函数

```python
self.play(
    circle.animate.shift(RIGHT),
    rate_func=smooth
)
```

### 常用速率函数

```python
# 平滑开始和结束（大多数动画的默认值）
smooth

# 恒定速度
linear

# 开始慢，结束快
rush_into

# 开始快，结束慢
rush_from

# 去并返回
there_and_back

# 去并返回（带停顿）
there_and_back_with_pause

# 双重平滑（超平滑）
double_smooth

# 原地不动（在 AnimationGroup 中用于延迟效果）
lingering
```

### 缓动函数（类似 CSS）

```python
# Ease in（开始慢）
ease_in_sine
ease_in_quad
ease_in_cubic
ease_in_expo
ease_in_circ
ease_in_back    # 开始时有轻微过冲

# Ease out（结束慢）
ease_out_sine
ease_out_quad
ease_out_cubic
ease_out_expo
ease_out_circ
ease_out_back   # 结束时有轻微过冲
ease_out_bounce # 弹跳式结束

# Ease in-out（两端都慢）
ease_in_out_sine
ease_in_out_quad
ease_in_out_cubic
ease_in_out_expo
ease_in_out_circ
ease_in_out_back
```

## 可视化对比

```python
class RateFuncComparison(Scene):
    def construct(self):
        funcs = [linear, smooth, rush_into, rush_from, there_and_back]
        names = ["linear", "smooth", "rush_into", "rush_from", "there_and_back"]

        dots = VGroup()
        labels = VGroup()

        for i, (func, name) in enumerate(zip(funcs, names)):
            dot = Dot().shift(LEFT * 4 + DOWN * i)
            label = Text(name, font_size=24).next_to(dot, LEFT)
            dots.add(dot)
            labels.add(label)

        self.add(dots, labels)

        self.play(*[
            dot.animate(rate_func=func).shift(RIGHT * 8)
            for dot, func in zip(dots, funcs)
        ], run_time=3)
```

## 组合 run_time 和 rate_func

```python
self.play(
    square.animate.shift(RIGHT * 3),
    run_time=2,
    rate_func=ease_out_bounce
)
```

## there_and_back

动画先前进再反向。

```python
class ThereAndBackExample(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # 向右移动然后回到起点
        self.play(
            square.animate.shift(RIGHT * 2),
            rate_func=there_and_back,
            run_time=2
        )
```

## 自定义速率函数

创建自己的速率函数（接收 t 从 0 到 1，返回进度 0 到 1）：

```python
def my_rate_func(t):
    # 二次缓动
    return t ** 2

self.play(
    circle.animate.shift(RIGHT),
    rate_func=my_rate_func
)
```

## wait() 时序

```python
# 等待默认时间（1 秒）
self.wait()

# 等待指定时长
self.wait(2)    # 2 秒
self.wait(0.5)  # 半秒
```

## 动画速度倍率

在 AnimationGroup 上使用 `run_time` 影响所有子动画：

```python
self.play(AnimationGroup(
    Create(circle),
    Create(square),
    lag_ratio=0.5
), run_time=3)  # 总时长 3 秒
```

## 最佳实践

1. **大多数动画使用 smooth** —— 看起来很自然
2. **恒定运动使用 linear** —— 机械/精确移动
3. **趣味效果使用 ease_out_bounce** —— 吸引注意力
4. **保持 run_time 在 0.5-3 秒之间** —— 保持观众注意力
5. **强调使用 there_and_back** —— 临时展示内容
6. **匹配 rate_func 到内容** —— 优雅用 smooth，有趣用弹跳
