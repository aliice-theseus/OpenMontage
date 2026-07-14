---
name: graphing
description: 绘制函数、参数曲线和数据可视化
metadata:
  tags: plot, graph, function, parametric, curve, data
---

# 绘制函数

绘制数学函数和曲线。

## 在坐标轴上绘制函数

```python
from manim import *

class BasicPlot(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 8])

        # 绘制函数
        graph = axes.plot(lambda x: x**2, color=BLUE)

        self.add(axes, graph)
```

## plot() 参数

```python
class PlotParameters(Scene):
    def construct(self):
        axes = Axes(x_range=[-5, 5], y_range=[-2, 2])

        graph = axes.plot(
            lambda x: np.sin(x),
            x_range=[-PI, PI],    # 限制定义域
            color=YELLOW,
            stroke_width=4,
        )

        self.add(axes, graph)
```

## 多个函数

```python
class MultiplePlots(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 10])

        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED)
        quad_graph = axes.plot(lambda x: x**2, color=GREEN)

        self.add(axes, sin_graph, cos_graph, quad_graph)
```

## 为图形添加标签

```python
class GraphLabels(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 10])
        graph = axes.plot(lambda x: x**2, color=BLUE)

        # 为图形添加标签
        label = axes.get_graph_label(
            graph,
            label=MathTex("y = x^2"),
            x_val=2,
            direction=UR
        )

        self.add(axes, graph, label)
```

## 参数曲线

绘制由参数方程定义的曲线。

```python
class ParametricExample(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-3, 3])

        # 圆形：x = cos(t), y = sin(t)
        curve = axes.plot_parametric_curve(
            lambda t: np.array([np.cos(t), np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=YELLOW
        )

        self.add(axes, curve)
```

### 参数曲线示例

```python
# 利萨如图形
curve = axes.plot_parametric_curve(
    lambda t: np.array([np.sin(3*t), np.sin(2*t), 0]),
    t_range=[0, 2*PI],
)

# 螺旋线
curve = axes.plot_parametric_curve(
    lambda t: np.array([t*np.cos(t), t*np.sin(t), 0]),
    t_range=[0, 4*PI],
)

# 心形线
curve = axes.plot_parametric_curve(
    lambda t: np.array([
        16 * np.sin(t)**3,
        13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t),
        0
    ]) / 10,
    t_range=[0, 2*PI],
)
```

## ParametricFunction（独立使用）

无需坐标轴创建参数曲线：

```python
class StandaloneParametric(Scene):
    def construct(self):
        curve = ParametricFunction(
            lambda t: np.array([np.cos(t), np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=BLUE
        )
        self.add(curve)
```

## 曲线下面积

```python
class AreaUnderCurve(Scene):
    def construct(self):
        axes = Axes(x_range=[-1, 5], y_range=[-1, 10])
        graph = axes.plot(lambda x: x**2, x_range=[0, 3], color=BLUE)

        # 阴影区域（曲线下面积）
        area = axes.get_area(
            graph,
            x_range=[0, 2],
            color=BLUE,
            opacity=0.5
        )

        self.add(axes, graph, area)
```

## 黎曼矩形

```python
class RiemannRectangles(Scene):
    def construct(self):
        axes = Axes(x_range=[-1, 5], y_range=[-1, 10])
        graph = axes.plot(lambda x: x**2, color=BLUE)

        rects = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 3],
            dx=0.5,
            color=YELLOW,
            stroke_width=1
        )

        self.add(axes, graph, rects)
```

## 动画化绘图

```python
class AnimatedGraph(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 2])
        self.add(axes)

        graph = axes.plot(lambda x: np.sin(x), color=BLUE)

        # 动画绘制图形
        self.play(Create(graph), run_time=3)
```

## 图形上的移动点

```python
class MovingPointOnGraph(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3], y_range=[-2, 2])
        graph = axes.plot(lambda x: np.sin(x), color=BLUE)

        # 跟随图形的点
        x_tracker = ValueTracker(-3)

        dot = always_redraw(lambda: Dot(
            axes.i2gp(x_tracker.get_value(), graph),
            color=YELLOW
        ))

        self.add(axes, graph, dot)
        self.play(x_tracker.animate.set_value(3), run_time=4)
```

## 3D 曲面图

```python
class SurfacePlot(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        surface = axes.plot_surface(
            lambda u, v: np.sin(u) * np.cos(v),
            u_range=[-PI, PI],
            v_range=[-PI, PI],
            colorscale=[BLUE, GREEN, YELLOW],
        )

        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(axes, surface)
```

## 最佳实践

1. **在 plot 上设置 x_range 处理间断点** —— 避免绘制未定义区域
2. **使用 get_graph_label 增加清晰度** —— 在图形上标注函数
3. **图形颜色与概念匹配** —— 一致的颜色编码
4. **使用 i2gp 获取图形上的点** —— 自动处理坐标转换
5. **动画绘制图形** —— 比静态展示更吸引人
