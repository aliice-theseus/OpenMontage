# ManimGL 场景

## 场景类型

ManimGL 提供几种场景类型：

### InteractiveScene（推荐）

大多数开发使用的默认场景。支持使用 `-se` 标志的交互模式。

```python
from manimlib import *

class MyScene(InteractiveScene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))
        self.wait()
```

### Scene（基类）

没有交互功能的基本场景：

```python
class BasicScene(Scene):
    def construct(self):
        self.play(Write(Text("Hello")))
```

### ThreeDScene

用于带有正确相机设置的 3D 动画：

```python
from manimlib import *

class My3DScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)
        self.camera.frame.reorient(-45*DEGREES, 75*DEGREES)
```

## construct 方法

所有场景逻辑放在 `construct()` 中：

```python
class MyScene(InteractiveScene):
    def construct(self):
        # 1. 创建 mobject
        circle = Circle(color=BLUE)
        square = Square(color=RED)

        # 2. 定位它们
        circle.shift(LEFT * 2)
        square.shift(RIGHT * 2)

        # 3. 动画
        self.play(ShowCreation(circle), ShowCreation(square))

        # 4. 等待观看
        self.wait(2)
```

## 添加 vs 播放

```python
# 静态添加（立即显示，无动画）
self.add(circle)

# 动画添加
self.play(ShowCreation(circle))
self.play(FadeIn(square))
```

## 场景方法

| 方法 | 描述 |
|--------|-------------|
| `self.play(*anims)` | 播放动画 |
| `self.wait(t)` | 等待 t 秒 |
| `self.add(*mobs)` | 立即添加 mobject |
| `self.remove(*mobs)` | 移除 mobject |
| `self.clear()` | 清空所有 mobject |
| `self.embed()` | 进入 IPython shell |

## 交互模式

使用 `-se` 标志在特定行进入：

```bash
manimgl scene.py MyScene -se 15
```

在 shell 中：
```python
checkpoint_paste()           # 使用动画运行剪贴板代码
checkpoint_paste(skip=True)  # 立即运行
checkpoint_paste(record=True) # 运行时录制
```

## 类属性

将场景配置定义为类属性：

```python
class MyScene(InteractiveScene):
    camera_class = ThreeDCamera  # 使用 3D 相机
    random_seed = 42             # 用于可重复性

    def construct(self):
        ...
```
