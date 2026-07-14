---
name: camera
description: MovingCameraScene（移动相机场景）、缩放、平移和相机操作
metadata:
  tags: camera, zoom, pan, frame, movingcamerascene, 3d
---

# 相机控制

通过相机操作控制观众看到的内容。

## MovingCameraScene

用于具有相机移动（缩放、平移）的 2D 场景。

```python
from manim import *

class CameraExample(MovingCameraScene):
    def construct(self):
        circle = Circle()
        square = Square().shift(RIGHT * 3)
        self.add(circle, square)

        # 访问相机帧
        # self.camera.frame 是可视区域
```

## 缩放

### 通过缩放帧进行缩放

```python
class ZoomExample(MovingCameraScene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(100)])
        dots.arrange_in_grid(10, 10, buff=0.3)
        self.add(dots)

        # 放大（使帧变小）
        self.play(self.camera.frame.animate.scale(0.5))
        self.wait()

        # 缩小（使帧变大）
        self.play(self.camera.frame.animate.scale(4))
```

### 缩放到指定宽度

```python
class ZoomToWidth(MovingCameraScene):
    def construct(self):
        text = Text("聚焦我！")
        self.add(text)

        # 缩放以适配文本（带间距）
        self.play(
            self.camera.frame.animate.set(width=text.width * 1.5)
        )
```

## 平移

### 移动相机到目标位置

```python
class PanExample(MovingCameraScene):
    def construct(self):
        c1 = Circle().shift(LEFT * 3)
        c2 = Circle().shift(RIGHT * 3)
        self.add(c1, c2)

        # 平移到第一个圆形
        self.play(self.camera.frame.animate.move_to(c1))
        self.wait()

        # 平移到第二个圆形
        self.play(self.camera.frame.animate.move_to(c2))
```

### 缩放和平移组合

```python
class ZoomAndPan(MovingCameraScene):
    def construct(self):
        square = Square().shift(LEFT * 2)
        triangle = Triangle().shift(RIGHT * 2)
        self.add(square, triangle)

        # 同时缩放和平移
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(square)
        )
        self.wait()

        # 移动到三角形（保持缩放状态）
        self.play(self.camera.frame.animate.move_to(triangle))
```

## 保存和恢复相机状态

```python
class SaveRestoreCamera(MovingCameraScene):
    def construct(self):
        circle = Circle()
        self.add(circle)

        # 保存当前状态
        self.camera.frame.save_state()

        # 进行更改
        self.play(self.camera.frame.animate.scale(0.3).move_to(circle))
        self.wait()

        # 恢复到保存的状态
        self.play(Restore(self.camera.frame))
```

## auto_zoom

自动缩放以适配 mobject。

```python
class AutoZoomExample(MovingCameraScene):
    def construct(self):
        squares = VGroup(*[
            Square().shift(RIGHT * i + UP * j)
            for i in range(-2, 3) for j in range(-2, 3)
        ])
        self.add(squares)

        # 缩放到适配指定 mobject
        self.play(self.camera.auto_zoom(squares[0]))
        self.wait()

        # 缩放到适配所有（带边距）
        self.play(self.camera.auto_zoom(squares, margin=1))
```

## 3D 相机（ThreeDScene）

```python
class ThreeDCameraExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Sphere()
        self.add(axes, sphere)

        # 设置初始相机方向
        self.set_camera_orientation(
            phi=75 * DEGREES,    # 与 z 轴的角度
            theta=-45 * DEGREES  # 绕 z 轴的角度
        )
```

### 动画化相机旋转

```python
class RotatingCamera(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.set_camera_orientation(phi=75 * DEGREES, theta=0)

        # 持续旋转
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
```

### 移动 3D 相机

```python
class Move3DCamera(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # 动画化相机移动
        self.move_camera(
            phi=45 * DEGREES,
            theta=45 * DEGREES,
            run_time=3
        )
```

## 相机背景

```python
class CameraBackground(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = BLUE_E

        circle = Circle()
        self.add(circle)
```

## 最佳实践

1. **缩放/平移使用 MovingCameraScene** —— 普通 Scene 的相机是静态的
2. **复杂移动前保存状态** —— 便于恢复
3. **动态内容使用 auto_zoom** —— 自动适配内容
4. **保持相机移动平滑** —— 不要让观众感到眩晕
5. **谨慎使用 3D 相机旋转** —— 可能会让人迷失方向
