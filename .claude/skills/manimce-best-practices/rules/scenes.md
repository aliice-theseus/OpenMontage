---
name: scenes
description: 场景结构、construct 方法和 Manim 中的场景类型
metadata:
  tags: scene, construct, setup, render, ThreeDScene, MovingCameraScene
---

# Manim 中的场景

Scene 是所有动画发生的画布。每个 Manim 动画都在 Scene 类中定义。

## 基本场景结构

所有动画代码都位于 Scene 子类的 `construct()` 方法中。

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.wait(1)
```

## 场景生命周期方法

### construct()
定义动画的主要方法。渲染时自动调用。

### setup()
在 `construct()` 之前调用。用于应在动画逻辑之前进行的初始化。

```python
class MyScene(Scene):
    def setup(self):
        self.camera.background_color = BLUE_E

    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

## 场景方法

### 添加和移除对象

```python
# 无动画添加（即时）
self.add(mobject)
self.add(mobject1, mobject2, mobject3)

# 无动画移除
self.remove(mobject)

# 清除所有 mobjects
self.clear()
```

### 播放动画

```python
# 播放单个动画
self.play(Create(circle))

# 同时播放多个动画
self.play(Create(circle), FadeIn(square))

# 带 run_time
self.play(Create(circle), run_time=2)
```

### 等待

```python
# 等待 1 秒（默认）
self.wait()

# 等待指定时长
self.wait(2)
```

## 场景类型

### Scene（默认）
适用于大多数动画的标准 2D 场景。

### ThreeDScene
用于具有相机方向控制的 3D 动画。

```python
class My3DScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes()
        sphere = Sphere()
        self.add(axes, sphere)
```

### MovingCameraScene
用于需要相机移动（缩放、平移）的动画。

```python
class ZoomScene(MovingCameraScene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.play(self.camera.frame.animate.scale(0.5).move_to(circle))
```

## 一个文件中的多个场景

渲染指定场景：
```bash
manim -pql file.py Scene1
```

渲染所有场景：
```bash
manim -pql -a file.py
```
