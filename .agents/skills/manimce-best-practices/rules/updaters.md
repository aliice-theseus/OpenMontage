---
name: updaters
description: Updaters、ValueTracker 和动态动画
metadata:
  tags: updater, valuetracker, dynamic, always, add_updater
---

# Updaters 和动态动画

Updaters 允许 mobject 基于其他值或 mobject 自动更新。

## 基本 Updater

添加每帧运行的函数。

```python
from manim import *

class UpdaterExample(Scene):
    def construct(self):
        dot = Dot()
        label = Text("Follow me").next_to(dot, UP)

        # 标签始终跟随点
        label.add_updater(lambda m: m.next_to(dot, UP))

        self.add(dot, label)
        self.play(dot.animate.shift(RIGHT * 3), run_time=2)
        self.play(dot.animate.shift(DOWN * 2), run_time=2)
```

## Updater 语法

```python
# Lambda 函数
mobject.add_updater(lambda m: m.move_to(target.get_center()))

# 命名函数
def follow_target(mob):
    mob.next_to(target, RIGHT)

mobject.add_updater(follow_target)

# 带 dt（时间增量）参数
def time_based_update(mob, dt):
    mob.rotate(dt * PI)  # 基于已用时间旋转

mobject.add_updater(time_based_update)
```

## ValueTracker

存储数值的 mobject。非常适合动画化参数。

```python
class ValueTrackerExample(Scene):
    def construct(self):
        # 创建跟踪器
        tracker = ValueTracker(0)

        # 创建数字显示
        number = DecimalNumber(0, num_decimal_places=2)
        number.add_updater(lambda m: m.set_value(tracker.get_value()))

        # 创建随跟踪器增长的圆
        circle = Circle()
        circle.add_updater(lambda m: m.set_width(tracker.get_value()))

        self.add(number, circle)

        # 动画化跟踪器
        self.play(tracker.animate.set_value(4), run_time=3)
        self.play(tracker.animate.set_value(1), run_time=2)
```

### ValueTracker 操作

```python
tracker = ValueTracker(5)

# 获取和设置值
current = tracker.get_value()
tracker.set_value(10)

# 增加
tracker.increment_value(2.5)

# 算术运算符（直接操作，无动画）
tracker += 1
tracker -= 2
tracker *= 3
tracker /= 2

# 动画化更改
self.play(tracker.animate.set_value(100))
self.play(tracker.animate.increment_value(-50))
```

## 带 ValueTracker 的 DecimalNumber

显示变化的数字：

```python
class NumberDisplay(Scene):
    def construct(self):
        tracker = ValueTracker(0)

        number = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=True,
            font_size=72
        )
        number.add_updater(lambda m: m.set_value(tracker.get_value()))
        number.add_updater(lambda m: m.move_to(ORIGIN))

        self.add(number)
        self.play(tracker.animate.set_value(100), run_time=3)
```

## always_redraw

基于当前值每帧重新创建 mobject。

```python
class AlwaysRedrawExample(Scene):
    def construct(self):
        tracker = ValueTracker(1)

        # 始终连接两个点的线
        line = always_redraw(
            lambda: Line(
                LEFT * 2,
                RIGHT * 2 * tracker.get_value()
            )
        )

        self.add(line)
        self.play(tracker.animate.set_value(2), run_time=2)
        self.play(tracker.animate.set_value(0.5), run_time=2)
```

## 常见 Updater 模式

### 跟随另一个 Mobject
```python
follower.add_updater(lambda m: m.move_to(leader.get_center()))
follower.add_updater(lambda m: m.next_to(leader, RIGHT))
```

### 指向另一个 Mobject
```python
arrow = Arrow(ORIGIN, RIGHT)
arrow.add_updater(lambda m: m.put_start_and_end_on(
    start.get_center(),
    end.get_center()
))
```

### 连续旋转
```python
mobject.add_updater(lambda m, dt: m.rotate(dt * PI))
```

### 匹配属性
```python
# 匹配颜色
follower.add_updater(lambda m: m.set_color(leader.get_color()))

# 匹配带偏移的位置
follower.add_updater(lambda m: m.move_to(leader.get_center() + UP))
```

## 移除 Updaters

```python
# 移除特定 updater
mobject.remove_updater(updater_function)

# 移除所有 updater
mobject.clear_updaters()

# 临时暂停
mobject.suspend_updating()
mobject.resume_updating()
```

## Updaters 与动画

Updaters 在动画期间持续运行：

```python
class UpdaterDuringAnimation(Scene):
    def construct(self):
        dot = Dot()
        trail = TracedPath(dot.get_center, stroke_color=YELLOW)

        self.add(dot, trail)
        self.play(dot.animate.shift(RIGHT * 3 + UP * 2), run_time=3)
```

## TracedPath

用于绘制路径的内置 updater：

```python
class TracedPathExample(Scene):
    def construct(self):
        dot = Dot()
        path = TracedPath(dot.get_center, stroke_width=2, stroke_color=BLUE)

        self.add(dot, path)
        self.play(
            dot.animate.shift(RIGHT * 2),
            dot.animate.shift(UP * 2),
            run_time=3
        )
```

## 最佳实践

1. **动画参数使用 ValueTracker** - 简洁且可控
2. **复杂形状使用 always_redraw** - 当 updater 变得复杂时
3. **完成后清除 updater** - 防止性能问题
4. **保持 updater 函数简单** - 复杂逻辑可能降低渲染速度
5. **基于时间的动画使用 dt** - 帧率无关
