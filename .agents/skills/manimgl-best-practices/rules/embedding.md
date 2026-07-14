# ManimGL 中的交互式嵌入

ManimGL 的 `self.embed()` 功能在场景执行期间将您放入交互式 IPython shell，使调试和实验变得非常强大。

## 基本用法

### 向场景添加 embed()

```python
from manimlib import *

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))

        # 在此处进入交互式 shell
        self.embed()

        # 退出 shell 后代码继续执行
        self.play(circle.animate.shift(RIGHT))
        self.wait()
```

### 使用 Embed 运行

```bash
# 运行场景——将在 embed() 处暂停
manimgl scene.py MyScene
```

## 交互式命令

### Shell 中可用

当 `self.embed()` 打开 IPython shell 时，您可以访问：

```python
# 场景方法（精简版——无需 'self.'）
play(animation)              # 播放动画
add(mobject)                 # 将 mobject 添加到场景
remove(mobject)              # 移除 mobject
wait(duration)               # 等待指定时间
clear()                      # 清除场景

# 相机/帧控制
frame                        # 访问相机帧
play(frame.animate.shift(RIGHT))

# construct() 中的所有局部变量
circle, square, text, etc.   # 您的 mobject

# 交互式相机
touch()                      # 进入触摸模式（按 'q' 退出）
                             # 按 'd' + 鼠标旋转
                             # 按 'z' + 滚轮缩放
                             # 按 'r' 重置

# 退出 shell 并继续
exit()                       # 继续场景执行
```

## 实际示例

### 调试动画

```python
class DebugScene(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.add(circle, square)

        # 这个动画有问题？
        self.play(circle.animate.move_to(square))

        # 交互式调试
        self.embed()

        # 在 shell 中：
        # >>> play(circle.animate.set_color(RED))
        # >>> circle.get_center()
        # >>> square.get_center()
```

### 实验定位

```python
class PositioningExperiment(Scene):
    def construct(self):
        shapes = VGroup(*[
            Circle(radius=0.5) for _ in range(5)
        ])

        # 交互式尝试不同排列
        self.add(shapes)
        self.embed()

        # 在 shell 中尝试：
        # >>> play(shapes.animate.arrange(RIGHT, buff=1))
        # >>> play(shapes.animate.arrange(DOWN, buff=0.5))
        # >>> play(shapes.animate.arrange_in_grid(rows=2))
```

### 颜色和样式探索

```python
class StyleExploration(Scene):
    def construct(self):
        text = Text("Experiment", font_size=72)
        self.add(text)
        self.embed()

        # 在 shell 中：
        # >>> play(text.animate.set_color(BLUE))
        # >>> text.set_backstroke(BLACK, width=10)
        # >>> play(text.animate.scale(2))
```

## 高级 embed() 用法

### 多个嵌入点

```python
class MultipleEmbeds(Scene):
    def construct(self):
        # 第一个检查点
        circle = Circle()
        self.play(ShowCreation(circle))
        self.embed()  # 第一次暂停

        # 第二个检查点
        square = Square()
        self.play(ShowCreation(square))
        self.embed()  # 第二次暂停

        # 第三个检查点
        self.play(FadeOut(VGroup(circle, square)))
        self.embed()  # 第三次暂停
```

### 条件嵌入

```python
class ConditionalEmbed(Scene):
    def construct(self):
        DEBUG = True

        circle = Circle()
        self.play(ShowCreation(circle))

        if DEBUG:
            self.embed()  # 仅在调试模式下嵌入

        self.play(circle.animate.shift(RIGHT))
```

## 使用 -se 标志

### 跳过并嵌入

`-se` 标志跳过到特定行并嵌入：

```python
class LargeScene(Scene):
    def construct(self):
        # 第 5 行
        circle = Circle()
        self.play(ShowCreation(circle))

        # 第 10 行
        square = Square()
        self.play(ShowCreation(square))

        # 第 15 行
        text = Text("Hello")
        self.play(Write(text))

        # 第 20 行
        self.play(FadeOut(VGroup(circle, square, text)))
```

```bash
# 直接跳到第 15 行并嵌入
manimgl scene.py LargeScene -se 15
```

## checkpoint_paste()

### 交互式代码执行

`checkpoint_paste()` 运行剪贴板中的代码：

```python
class CheckpointScene(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.embed()
```

```bash
# 运行场景
manimgl scene.py CheckpointScene
```

在 shell 中：

```python
# 先将此代码复制到剪贴板：
"""
square = Square()
play(ShowCreation(square))
play(square.animate.next_to(circle, RIGHT))
"""

# 然后在 shell 中：
>>> checkpoint_paste()              # 带动画运行
>>> checkpoint_paste(skip=True)     # 立即运行
>>> checkpoint_paste(record=True)   # 录制运行过程
```

## 保存和恢复状态

### save_state() 和 restore()

```python
class StateManagement(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.add(circle, square)

        # 保存当前状态
        self.save_state()

        # 进行更改
        self.play(circle.animate.shift(RIGHT * 3))
        self.play(square.animate.shift(LEFT * 3))

        self.embed()

        # 在 shell 中：
        # >>> restore()  # 恢复到保存的状态
```

## 交互式 3D 探索

### touch() 模式

```python
class Interactive3D(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(20, 70)

        # 创建 3D 对象
        sphere = Sphere(radius=2, color=BLUE)
        self.add(sphere)

        self.embed()

        # 在 shell 中：
        # >>> touch()
        # 现在您可以：
        # - 按 'd' 并移动鼠标旋转
        # - 按 'z' 并滚动缩放
        # - 按 'r' 重置相机
        # - 按 'q' 退出触摸模式
```

## 调试模式

### 检查 Mobject 属性

```python
class InspectProperties(Scene):
    def construct(self):
        circle = Circle(radius=2, color=BLUE)
        circle.shift(RIGHT * 3)
        self.add(circle)
        self.embed()

        # 在 shell 中：
        # >>> circle.get_center()
        # >>> circle.get_color()
        # >>> circle.get_width()
        # >>> circle.get_height()
        # >>> circle.get_all_points()
```

### 测试动画时间

```python
class TimingTest(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.embed()

        # 在 shell 中测试不同时间：
        # >>> play(circle.animate.shift(RIGHT), run_time=0.5)
        # >>> play(circle.animate.shift(LEFT), run_time=2)
        # >>> play(circle.animate.shift(UP), run_time=1, rate_func=smooth)
```

### 迭代式构建复杂场景

```python
class IterativeBuilding(Scene):
    def construct(self):
        self.embed()

        # 在 shell 中构建整个场景：
        # >>> title = Text("My Animation")
        # >>> title.to_edge(UP)
        # >>> add(title)
        #
        # >>> circles = VGroup(*[Circle(radius=0.5) for _ in range(5)])
        # >>> circles.arrange(RIGHT, buff=0.5)
        # >>> play(LaggedStart(*[ShowCreation(c) for c in circles], lag_ratio=0.2))
        #
        # >>> formula = Tex(R"E = mc^2")
        # >>> formula.next_to(circles, DOWN, buff=1)
        # >>> play(Write(formula))
```

## 最佳实践

1. **用于调试**：当动画不如预期时添加 `self.embed()`
2. **自由实验**：在 shell 中尝试不同方法，然后再添加到代码中
3. **实验前 save_state()**：搞砸时容易恢复
4. **大型场景使用 -se**：跳转到问题区域，而不是观看整个动画
5. **迭代使用 checkpoint_paste()**：快速测试代码片段
6. **3D 使用 touch()**：找到正确相机角度的必备工具
7. **最终渲染前移除 embed()**：别忘了移除调试用的 embed

## 常见模式

### 快速实验模式

```python
# 在问题点添加
self.embed()

# 在 shell 中测试修复
play(mobject.animate.scale(2))  # 测试不同值

# 如果有效，添加到代码
# exit()
```

### 交互式开发模式

```python
# 从最小设置开始
class Scene(Scene):
    def construct(self):
        self.embed()

# 在 shell 中构建所有内容
# 将成功的命令复制回代码
```

### 3D 相机设置模式

```python
# 进入 3D 场景
frame.reorient(20, 70)
add(sphere)
self.embed()

# 找到完美角度
touch()  # 用鼠标旋转
# 完成后按 'q'
# 检查 frame.get_theta()、frame.get_phi()
# 将这些值添加到代码中
```

## 故障排除

### embed() 不起作用

- 确保使用 `manimgl` 命令运行
- 检查 IPython 是否已安装
- 确认 embed() 点之前没有语法错误

### 无法访问变量

- 变量必须在 `self.embed()` 之前定义
- 使用 `locals()` 或 `globals()` 检查可用变量

### Shell 立即退出

- 除非要继续，否则不要调用 `exit()`
- 按 Ctrl+D 退出并继续
- 使用 `quit()` 或 `exit()` 关闭 shell

## 示例：完整的交互式开发

```python
class InteractiveDevelopment(Scene):
    def construct(self):
        # 以 embed 开始
        self.embed()

        # 在 shell 中构建所有内容：
        """
        # 创建标题
        title = Text("Interactive Development", font_size=60)
        title.to_edge(UP)
        play(Write(title))

        # 创建内容
        circle = Circle(radius=1.5, color=BLUE)
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(WHITE, width=3)
        play(ShowCreation(circle))

        # 添加标签
        label = Text("Circle", font_size=36)
        label.next_to(circle, DOWN)
        play(FadeIn(label, shift=UP))

        # 动画
        play(
            circle.animate.shift(RIGHT * 2),
            label.animate.shift(RIGHT * 2)
        )

        wait(2)

        # 满意后，将这全部代码复制到 construct 方法中
        exit()
        """
```

这使 ManimGL 在快速原型设计和调试方面变得极其强大！
