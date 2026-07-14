# ManimGL 帧（相机）控制

## CameraFrame

在 ManimGL 中，相机控制通过 `self.camera.frame` 完成（CameraFrame 是一个 Mobject）：

```python
frame = self.camera.frame

# 设置 3D 朝向的欧拉角
frame.set_euler_angles(
    theta=-30 * DEGREES,
    phi=70 * DEGREES,
)
```

**注意：** 在 InteractiveScene 中，您也可以使用 `self.frame` 作为快捷方式。

## CameraFrame 方法（来自官方文档）

CameraFrame 继承标准 Mobject 方法，外加以下特定方法：

- `.to_default_state()` - 重置相机
- `.set_euler_angles(theta, phi, gamma)` - 设置所有角度
- `.set_theta(theta)` - 水平旋转
- `.set_phi(phi)` - 垂直旋转
- `.set_gamma(gamma)` - 滚动
- `.increment_theta(dtheta)` - 增加 theta
- `.increment_phi(dphi)` - 增加 phi
- `.increment_gamma(dgamma)` - 增加 gamma

还继承了：`.shift()`、`.scale()`、`.move_to()`

```python
# 向下看 45 度，旋转 30 度
self.frame.reorient(45, -30, 0, ORIGIN, 8)

# 动画化重定向
self.play(
    self.frame.animate.reorient(60, -45, 0, (1, 0, 0), 10),
    run_time=3
)
```

## 常见相机操作

### 缩放

```python
# 放大（高度越小 = 越近）
self.play(self.frame.animate.set_height(4))

# 缩小
self.play(self.frame.animate.set_height(12))
```

### 平移

```python
# 移动相机中心
self.play(self.frame.animate.move_to(RIGHT * 3))

# 移动相机
self.play(self.frame.animate.shift(UP * 2))
```

### 组合移动

```python
self.play(
    self.frame.animate.reorient(50, -40, 0, (2, 1, 0), 6).set_anim_args(run_time=3)
)
```

## fix_in_frame()

在 3D 相机移动期间保持 mobject 固定在屏幕空间：

```python
title = Text("My Title")
title.to_edge(UP)
title.fix_in_frame()  # 在 mobject 上调用，而不是场景！

self.add(title)

# 相机移动时标题保持固定
self.play(self.frame.animate.reorient(60, -45, 0))
```

**与 ManimCE 的关键区别：** 在 ManimCE 中调用 `self.add_fixed_in_frame_mobjects(title)`。在 ManimGL 中调用 `title.fix_in_frame()`。

## set_floor_plane()

为 3D 场景设置地平面方向：

```python
self.set_floor_plane("xz")  # y 向上，xz 是地面
self.set_floor_plane("xy")  # z 向上，xy 是地面（默认）
```

## 帧动画语法

```python
# 使用 set_anim_args 链式调用设置 run_time
self.play(
    self.frame.animate.reorient(45, -30, 0, ORIGIN, 8).set_anim_args(run_time=2)
)

# 多个帧操作
self.play(
    self.frame.animate.shift(RIGHT * 2).set_height(6),
    run_time=1.5
)
```

## 背景矩形

对于带 3D 相机移动的场景，添加背景：

```python
background = FullScreenRectangle()
background.set_fill(BLACK, 1)
background.fix_in_frame()
self.add(background)
```

## 完整 3D 示例

```python
class Camera3DDemo(InteractiveScene):
    def construct(self):
        # 背景
        bg = FullScreenRectangle()
        bg.set_fill(GREY_E, 1)
        bg.fix_in_frame()
        self.add(bg)

        # 固定在帧中的标题
        title = Text("3D Demo")
        title.to_edge(UP)
        title.fix_in_frame()
        self.add(title)

        # 3D 内容
        cube = Cube(side_length=2)
        cube.set_color(BLUE)
        self.add(cube)

        # 动画化相机
        self.play(
            self.frame.animate.reorient(60, -45, 0, ORIGIN, 8),
            run_time=3
        )

        # 绕物体旋转
        self.play(
            self.frame.animate.reorient(60, 45, 0),
            run_time=4
        )
```
