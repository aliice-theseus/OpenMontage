# ManimGL 中的相机和框架

ManimGL 的相机系统以 `CameraFrame` 为核心，可通过 `self.camera.frame` 访问。这提供了对 2D 和 3D 视角的强大控制。

## 访问相机框架

```python
from manimlib import *

class CameraExample(Scene):
    def construct(self):
        # 获取相机框架
        frame = self.camera.frame

        # frame 是一个 Mobject，因此拥有所有 Mobject 方法
        # move_to, shift, scale, rotate 等
```

## 2D 相机移动

### 基本移动

```python
# 平移相机
self.play(frame.animate.shift(RIGHT * 2))

# 移动到特定位置
self.play(frame.animate.move_to([3, 2, 0]))

# 缩放（变焦）
self.play(frame.animate.scale(0.5))  # 放大
self.play(frame.animate.scale(2))    # 缩小
```

### 跟随对象

```python
class FollowObject(Scene):
    def construct(self):
        frame = self.camera.frame
        dot = Dot(color=RED)

        # 相机跟随点
        frame.add_updater(lambda m: m.move_to(dot))

        # 移动点
        self.add(dot)
        self.play(dot.animate.shift(RIGHT * 5), run_time=3)
        self.play(dot.animate.shift(UP * 3), run_time=2)
        self.wait()
```

### 框架尺寸

```python
# 设置框架宽度/高度
frame.set_width(10)
frame.set_height(6)

# 动画化框架尺寸
self.play(frame.animate.set_width(20), run_time=2)
```

## 3D 相机方向

### reorient() 方法

`reorient()` 方法是在 ManimGL 中设置 3D 相机方向的主要方式。

```python
# 签名：
# frame.reorient(theta, phi, gamma=0, center=ORIGIN, height=8)

# 参数：
# - theta: 绕 z 轴旋转（方位角），角度制
# - phi: 与 z 轴的夹角（极角），角度制
# - gamma: 翻滚角，角度制（可选）
# - center: 相机观察的点（可选）
# - height: 框架高度（可选）

# 常见视角：
frame.reorient(0, 0)        # 前视图（XY 平面）
frame.reorient(20, 70)      # 类等轴视图
frame.reorient(0, 90)       # 俯视图（从上方看 XY 平面）
frame.reorient(90, 90)      # 侧视图（YZ 平面）
frame.reorient(45, 45)      # 对角视图
```

### 欧拉角

```python
# 单独设置角度
frame.set_theta(30 * DEGREES)
frame.set_phi(70 * DEGREES)
frame.set_gamma(0 * DEGREES)

# 全部同时设置
frame.set_euler_angles(
    theta=30 * DEGREES,
    phi=70 * DEGREES,
    gamma=0 * DEGREES
)

# 获取当前角度
theta = frame.get_theta()
phi = frame.get_phi()
gamma = frame.get_gamma()
```

### 增量旋转

```python
# 增加角度（用于动画）
frame.increment_theta(10 * DEGREES)
frame.increment_phi(5 * DEGREES)
frame.increment_gamma(2 * DEGREES)

# 动画化增量
self.play(frame.animate.increment_theta(90 * DEGREES))
```

## 动画化相机

### 简单的相机动画

```python
class AnimateCamera(Scene):
    def construct(self):
        frame = self.camera.frame

        cube = Cube()
        self.add(cube)

        # 重新定向到等轴视图
        self.play(frame.animate.reorient(20, 70), run_time=2)
        self.wait()

        # 围绕对象旋转
        self.play(frame.animate.increment_theta(360 * DEGREES), run_time=8)
        self.wait()
```

### 连续相机运动

```python
class ContinuousRotation(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        sphere = Sphere(radius=2, color=BLUE)
        self.add(sphere)

        # 添加连续旋转更新器
        frame.add_updater(lambda m, dt: m.increment_theta(20 * dt))

        # 让它旋转 10 秒
        self.wait(10)

        # 停止旋转
        frame.clear_updaters()
        self.wait()
```

### 相机放大/缩小

```python
class ZoomEffect(Scene):
    def construct(self):
        frame = self.camera.frame

        objects = VGroup(*[Square() for _ in range(5)])
        objects.arrange(RIGHT, buff=1)
        self.add(objects)

        # 缩小以看到所有对象
        self.play(frame.animate.set_width(20), run_time=2)
        self.wait()

        # 放大到第一个对象
        self.play(
            frame.animate.set_width(2).move_to(objects[0]),
            run_time=2
        )
        self.wait()
```

## 在框架中固定 Mobject

### fix_in_frame() 方法

在相机移动时保持 2D 元素固定在屏幕空间。

```python
class FixedInFrame(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        # 3D 对象随相机移动
        cube = Cube(color=BLUE)
        self.add(cube)

        # 2D 标签保持固定
        title = Text("Rotating Cube", font_size=60)
        title.to_edge(UP)
        title.fix_in_frame()  # 固定到屏幕空间
        self.add(title)

        # 旋转相机 - 立方体旋转，标题保持固定
        self.play(frame.animate.reorient(60, 80), run_time=3)
        self.wait()
```

### 多个固定元素

```python
class MultipleFixed(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(30, 70)

        # 3D 内容
        surface = Sphere(radius=2, color=BLUE, opacity=0.7)
        self.add(surface)

        # 固定的 UI 元素
        title = Text("3D Visualization", font_size=48)
        title.to_edge(UP)
        title.fix_in_frame()

        subtitle = Text("Interactive Camera", font_size=30, color=GREY)
        subtitle.next_to(title, DOWN)
        subtitle.fix_in_frame()

        controls = Text("Press 'd' to rotate", font_size=24)
        controls.to_corner(DL)
        controls.fix_in_frame()

        self.add(title, subtitle, controls)

        # 旋转相机
        self.play(frame.animate.increment_theta(180 * DEGREES), run_time=6)
```

## 重置相机

```python
# 重置为默认状态
frame.to_default_state()

# 动画化重置
self.play(frame.animate.to_default_state())
```

## 相机中心

```python
# 设置相机注视点
frame.set_center([2, 3, 0])

# 动画化中心变化
self.play(frame.animate.set_center([0, 0, 2]))

# 获取当前中心
center = frame.get_center()
```

## 高级相机模式

### 轨道相机围绕对象

```python
class OrbitCamera(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(30, 70)

        # 中心对象
        torus = Torus(r1=2, r2=0.5, color=YELLOW)
        self.add(torus)

        # 轨道 360 度
        self.play(
            frame.animate.increment_theta(360 * DEGREES),
            run_time=10,
            rate_func=linear
        )
```

### 相机沿路径移动

```python
class CameraPath(Scene):
    def construct(self):
        frame = self.camera.frame

        # 创建路径
        path = Circle(radius=5)
        self.add(path)

        # 要跟随的点
        dot = Dot(color=RED)
        dot.move_to(path.point_from_proportion(0))

        # 相机跟随点
        frame.add_updater(lambda m: m.move_to(dot))

        # 沿路径移动点
        self.play(
            MoveAlongPath(dot, path),
            run_time=8,
            rate_func=linear
        )
```

### 多个相机位置

```python
class CameraTour(Scene):
    def construct(self):
        frame = self.camera.frame

        # 创建场景
        objects = VGroup(
            Square(side_length=2, color=RED).shift(LEFT * 3),
            Circle(radius=1, color=BLUE),
            Triangle(color=GREEN).shift(RIGHT * 3)
        )
        self.add(objects)

        # 浏览每个对象
        for obj in objects:
            self.play(
                frame.animate.set_width(3).move_to(obj),
                run_time=2
            )
            self.wait()

        # 返回全景
        self.play(
            frame.animate.set_width(14).move_to(ORIGIN),
            run_time=2
        )
```

### 带更新器的动态相机

```python
class DynamicCamera(Scene):
    def construct(self):
        frame = self.camera.frame

        # 移动的对象
        dot = Dot(color=RED)

        # 相机追踪并根据距离原点距离缩放
        def update_frame(frame):
            frame.move_to(dot)
            dist = np.linalg.norm(dot.get_center())
            frame.set_width(max(8, dist * 2))

        frame.add_updater(update_frame)

        # 移动点
        self.add(dot)
        self.play(dot.animate.shift(RIGHT * 5 + UP * 3), run_time=4)
        self.play(dot.animate.shift(LEFT * 8 + DOWN * 2), run_time=4)
        self.wait()
```

## 光源

### 访问和移动光源

```python
class LightControl(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        # 获取光源
        light = self.camera.light_source

        # 创建 3D 对象
        sphere = Sphere(radius=2, color=BLUE)
        sphere.set_gloss(0.8)
        self.add(sphere)

        # 显示光源位置（用于调试）
        light_indicator = Dot(color=YELLOW)
        light_indicator.add_updater(lambda m: m.move_to(light.get_center()))
        self.add(light_indicator)

        # 移动光源
        self.play(light.animate.move_to([5, 5, 5]), run_time=2)
        self.wait()
        self.play(light.animate.move_to([-5, -5, 5]), run_time=2)
        self.wait()
```

## 最佳实践

1. **存储框架引用**：开始时使用 `frame = self.camera.frame`
2. **3D 中使用 reorient()**：比单独设置角度更简洁
3. **UI 使用 fix_in_frame()**：保持标签和标题可读
4. **平滑过渡**：相机移动使用适当的 run_time
5. **rate_func=linear**：用于连续旋转
6. **to_default_state()**：需要时重置相机
7. **使用更新器进行跟随**：使用 updater 追踪移动对象

## 常见模式

### 缩放和平移

```python
def zoom_to(self, mobject, scale_factor=1.5):
    frame = self.camera.frame
    self.play(
        frame.animate
            .set_width(mobject.get_width() * scale_factor)
            .move_to(mobject),
        run_time=2
    )
```

### 360 度展示

```python
def showcase_3d(self, mobject):
    frame = self.camera.frame
    frame.reorient(20, 70)
    self.play(
        frame.animate.increment_theta(360 * DEGREES),
        run_time=8,
        rate_func=linear
    )
```

### 画中画效果

```python
# 小窗口相机视图
small_frame = self.camera.frame.copy()
small_frame.set_width(4)
small_frame.to_corner(UR, buff=0.5)
small_frame.fix_in_frame()
```
