# ManimGL 动画

## 动画系统概述

ManimGL 的动画系统建立在 `Animation` 基类之上。专用的子类处理创建、变换和指示效果。

## 播放动画

```python
# 单个动画
self.play(ShowCreation(circle))

# 同时播放多个动画
self.play(
    ShowCreation(circle),
    Write(text),
)

# 带 run_time
self.play(ShowCreation(circle), run_time=2)

# 带速率函数
self.play(ShowCreation(circle), rate_func=smooth)
```

## 创建动画

| 动画 | 描述 |
|-----------|-------------|
| `ShowCreation` | 绘制 VMobject 的路径（不是 ManimCE 中的 `Create`） |
| `Write` | 书写文本或 LaTeX |
| `DrawBorderThenFill` | 先绘制轮廓然后填充 |
| `FadeIn` | 淡入，可选方向 |
| `FadeOut` | 淡出，可选方向 |
| `GrowFromCenter` | 从中心缩放放大 |
| `GrowFromPoint` | 从一个点缩放放大 |
| `GrowArrow` | 专门用于箭头 |

```python
# ShowCreation 用于路径
self.play(ShowCreation(circle))

# Write 用于文本
self.play(Write(Tex(R"\pi")))

# FadeIn 带方向
self.play(FadeIn(square, shift=UP))
```

## 变换动画

| 动画 | 描述 |
|-----------|-------------|
| `Transform` | 将一个 mobject 变形为另一个（修改原始对象） |
| `ReplacementTransform` | 用目标替换源 |
| `TransformMatchingShapes` | 匹配相似形状 |
| `TransformMatchingTex` | 匹配 LaTeX 部分 |
| `FadeTransform` | 变换时淡出 |
| `MoveToTarget` | 移动到 mobject 的 `.target` |

```python
# Transform（修改 circle，变成 square）
self.play(Transform(circle, square))

# ReplacementTransform（移除 circle，添加 square）
self.play(ReplacementTransform(circle, square))

# 使用 .target
circle.generate_target()
circle.target.shift(RIGHT * 2)
circle.target.set_color(RED)
self.play(MoveToTarget(circle))
```

## 指示动画

| 动画 | 描述 |
|-----------|-------------|
| `Indicate` | 闪烁/脉冲以吸引注意 |
| `ShowPassingFlash` | 沿路径闪光 |
| `Flash` | 光爆发 |
| `Circumscribe` | 在周围绘制圆/矩形 |
| `Wiggle` | 摆动 mobject |
| `FlashAround` | 对象周围闪光效果 |

```python
self.play(Indicate(important_text))
self.play(FlashAround(equation, run_time=2))
```

## 移动动画

```python
# 使用 .animate 语法
self.play(circle.animate.shift(RIGHT * 2))
self.play(circle.animate.scale(2).set_color(RED))

# 旋转
self.play(Rotate(square, PI/2))
self.play(Rotate(square, 90 * DEGREES))  # 同上

# MoveAlongPath
path = Line(LEFT, RIGHT)
self.play(MoveAlongPath(dot, path))
```

## LaggedStart 和 Groups

```python
# 交错动画
self.play(LaggedStart(
    *[ShowCreation(mob) for mob in mobjects],
    lag_ratio=0.2
))

# AnimationGroup 用于同时播放
self.play(AnimationGroup(
    ShowCreation(circle),
    Write(text),
    lag_ratio=0  # 同时
))

# Succession 用于顺序播放
self.play(Succession(
    ShowCreation(circle),
    Write(text),
))
```

## 动画参数

所有动画的通用参数：

| 参数 | 描述 |
|-----------|-------------|
| `run_time` | 持续时间（秒） |
| `rate_func` | 缓动函数（smooth、linear 等） |
| `lag_ratio` | 组动画的交错比例 |
| `remover` | 动画后移除 mobject |
| `introducer` | 动画开始时添加 mobject |

```python
self.play(
    ShowCreation(circle),
    run_time=3,
    rate_func=there_and_back,
)
```

## 速率函数

常用速率函数：
- `smooth` - 默认平滑缓动
- `linear` - 恒定速度
- `rush_into` - 快开始，慢结束
- `rush_from` - 慢开始，快结束
- `there_and_back` - 去并返回
- `double_smooth` - 额外平滑

## 等待

```python
self.wait()       # 默认暂停
self.wait(2)      # 2秒暂停
self.wait(0.5)    # 半秒
```
