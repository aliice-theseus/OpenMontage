---
name: timing
description: 速率函数、缓动、run_time 和动画时间控制
metadata:
  tags: timing, rate_func, easing, smooth, linear, run_time
---

# 动画时间控制

使用时间参数控制动画的速度和感觉。

## run_time

控制动画的持续时间（秒）。

```python
from manim import *

class RunTimeExample(Scene):
    def construct(self):
        circle = Circle()

        # 默认（1秒）
        self.play(Create(circle))

        # 更长的动画
        self.play(circle.animate.shift(RIGHT), run_time=3)

        # 快速动画
        self.play(circle.animate.set_color(RED), run_time=0.5)
```

## 速率函数

速率函数控制动画随时间进展的方式（缓动）。

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

# 慢开始，快结束
rush_into

# 快开始，慢结束
rush_from

# 去并返回
there_and_back

# 去并返回，带停顿
there_and_back_with_pause

# 双重平滑（额外平滑）
double_smooth

# 保持不动（在 AnimationGroup 中用于延迟）
lingering
```

### 缓动函数（类似 CSS）

```python
# 缓入（慢开始）
ease_in_sine
ease_in_quad
ease_in_cubic
ease_in_expo
ease_in_circ
ease_in_back    # 开始时轻微过冲

# 缓出（慢结束）
ease_out_sine
ease_out_quad
ease_out_cubic
ease_out_expo
ease_out_circ
ease_out_back   # 结束时轻微过冲
ease_out_bounce # 弹跳结束

# 缓入-缓出（两端都慢）
ease_in_out_sine
ease_in_out_quad
ease_in_out_cubic
ease_in_out_expo
ease_in_out_circ
ease_in_out_back
```

## 视觉比较

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

动画向前然后反向。

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

创建自己的速率函数（t 从 0 到 1，返回进度 0 到 1）：

```python
def my_rate_func(t):
    # 二次缓动
    return t ** 2

self.play(
    circle.animate.shift(RIGHT),
    rate_func=my_rate_func
)
```

## wait() 时间

```python
# 等待默认时间（1秒）
self.wait()

# 等待指定时长
self.wait(2)    # 2秒
self.wait(0.5)  # 半秒
```

## 动画速度倍数

在 AnimationGroup 上使用 `run_time` 会影响所有子动画：

```python
self.play(AnimationGroup(
    Create(circle),
    Create(square),
    lag_ratio=0.5
), run_time=3)  # 总持续时间为3秒
```

## 最佳实践

1. **大多数动画使用 smooth** - 看起来自然
2. **恒定运动使用 linear** - 机械/精确移动
3. **俏皮效果使用 ease_out_bounce** - 吸引注意力
4. **保持 run_time 在 0.5-3 秒之间** - 保持观众注意力
5. **强调使用 there_and_back** - 临时展示某物
6. **rate_func 匹配内容** - 优雅用 smooth，有趣用 bouncy
