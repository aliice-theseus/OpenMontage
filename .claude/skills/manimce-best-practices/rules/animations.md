---
name: animations
description: 动画类、播放动画和 Manim 中的动画时序
metadata:
  tags: animation, play, run_time, rate_func, animate
---

# Manim 中的动画

动画在时间上对 mobject 进行状态插值。通过 `self.play()` 播放。

## .animate 语法

最常见的动画方式是使用 `.animate` 属性：

```python
# 将正方形向右移动
self.play(square.animate.shift(RIGHT))

# 放大
self.play(circle.animate.scale(2))

# 改变颜色
self.play(text.animate.set_color(RED))

# 链式多个变化
self.play(square.animate.shift(RIGHT).rotate(PI/4).set_color(BLUE))
```

## 动画参数

### run_time
控制动画时长（秒），默认值为 1。

```python
self.play(Create(circle), run_time=2)  # 2 秒动画
self.play(Create(circle), run_time=0.5)  # 半秒
```

### rate_func
控制动画的时间曲线（缓动）。

```python
from manim import smooth, linear, there_and_back

self.play(square.animate.shift(RIGHT), rate_func=smooth)
self.play(square.animate.shift(RIGHT), rate_func=linear)
self.play(square.animate.shift(RIGHT), rate_func=there_and_back)
```

## 播放多个动画

### 同时播放

```python
# 所有同时播放
self.play(
    Create(circle),
    FadeIn(square),
    Write(text)
)
```

### 顺序播放

```python
# 一个接一个
self.play(Create(circle))
self.play(FadeIn(square))
self.play(Write(text))

# 或使用 Succession
self.play(Succession(
    Create(circle),
    FadeIn(square),
    Write(text)
))
```

## 常用动画类

### 创建动画
```python
Create(mobject)           # 逐步绘制 mobject
Write(text)               # 写入文本/公式
FadeIn(mobject)           # 从透明淡入
DrawBorderThenFill(mob)   # 先绘制轮廓，然后填充
GrowFromCenter(mobject)   # 从中心点生长
```

### 移除动画
```python
FadeOut(mobject)          # 淡出至透明
Uncreate(mobject)         # Create 的反向操作
ShrinkToCenter(mobject)   # 收缩到中心并消失
```

### 变形动画
```python
Transform(mob1, mob2)              # 将 mob1 形变为 mob2
ReplacementTransform(mob1, mob2)   # 用 mob2 替换 mob1
TransformFromCopy(mob1, mob2)      # 保留 mob1，创建 mob2
```

### 移动动画
```python
MoveToTarget(mobject)     # 移动到预设目标
Rotate(mobject, angle)    # 按角度旋转
Circumscribe(mobject)     # 用圆形引起注意
```

## 动画 vs 即时变化

```python
# 动画变化（可见过渡）
self.play(circle.animate.set_color(RED))

# 即时变化（无动画）
circle.set_color(RED)
self.add(circle)
```

## 最佳实践

1. **简单变换使用 .animate** —— 比显式 Animation 类更简洁
2. **保持 run_time 合理** —— 大多数动画 0.5-2 秒
3. **使用 rate_func 增加润色** —— `smooth` 通常比 `linear` 更好
4. **将相关动画分组** —— 概念相关时同时播放
