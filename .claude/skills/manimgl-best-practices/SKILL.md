---
name: manimgl-best-practices
description: |
  触发条件：(1) 用户提到 "manimgl" 或 "ManimGL" 或 "3b1b manim"，(2) 代码包含 `from manimlib import *`，(3) 用户运行 `manimgl` CLI 命令，(4) 使用 InteractiveScene、self.frame、self.embed()、ShowCreation() 或 ManimGL 特定模式。

  ManimGL（Grant Sanderson 的 3Blue1Brown 版本）的最佳实践 — 基于 OpenGL 的动画引擎，支持交互式开发。涵盖 InteractiveScene、带 t2c 的 Tex、相机框架控制、交互模式（-se 标志）、3D 渲染和 checkpoint_paste() 工作流程。

  不适用于 Manim Community Edition（使用 `manim` 导入和 `manim` CLI）。
---

## 使用方法

阅读各规则文件以获取详细解释和代码示例：

### 核心概念
- [rules/scenes.md](rules/scenes.md) - InteractiveScene、场景类型和 construct 方法
- [rules/mobjects.md](rules/mobjects.md) - Mobject 类型、VMobject、组和定位
- [rules/animations.md](rules/animations.md) - 动画类、播放动画和时间控制

### 创建与变换
- [rules/creation-animations.md](rules/creation-animations.md) - ShowCreation、Write、FadeIn、DrawBorderThenFill
- [rules/transform-animations.md](rules/transform-animations.md) - Transform、ReplacementTransform、TransformMatchingTex
- [rules/animation-groups.md](rules/animation-groups.md) - LaggedStart、Succession、AnimationGroup

### 文本与数学
- [rules/tex.md](rules/tex.md) - Tex 类、原始字符串 R"..." 和 LaTeX 渲染
- [rules/text.md](rules/text.md) - Text mobject、字体和样式
- [rules/t2c.md](rules/t2c.md) - tex_to_color_map (t2c) 用于为数学表达式着色

### 样式与外观
- [rules/colors.md](rules/colors.md) - 颜色常量、渐变、RGB、十六进制、GLSL 着色
- [rules/styling.md](rules/styling.md) - 填充、描边、不透明度、背景描边、光泽、阴影

### 3D 与相机
- [rules/3d.md](rules/3d.md) - 3D 对象、曲面、球体、环面、参数曲面、光照
- [rules/camera.md](rules/camera.md) - frame.reorient()、欧拉角、fix_in_frame()、相机动画

### 交互式开发
- [rules/interactive.md](rules/interactive.md) - 使用 `-se` 标志的交互模式、checkpoint_paste()
- [rules/frame.md](rules/frame.md) - self.frame、相机控制、重新定向和缩放
- [rules/embedding.md](rules/embedding.md) - 用于 IPython 调试的 self.embed()、touch() 模式

### 配置与 CLI
- [rules/cli.md](rules/cli.md) - manimgl 命令、标志（-w、-o、-se、-l、-h）、渲染选项
- [rules/config.md](rules/config.md) - custom_config.yml、目录、相机设置、质量预设

## 工作示例

展示常见模式的完整、经过测试的示例文件：

- [examples/basic_animations.py](examples/basic_animations.py) - 基本形状、文本和动画
- [examples/math_visualization.py](examples/math_visualization.py) - LaTeX 方程和数学内容
- [examples/graph_plotting.py](examples/graph_plotting.py) - 坐标轴、函数和绘图
- [examples/3d_visualization.py](examples/3d_visualization.py) - 带相机控制和曲面的 3D 场景
- [examples/updater_patterns.py](examples/updater_patterns.py) - 使用更新器的动态动画

## 场景模板

复制并修改这些模板以开始新项目：

- [templates/basic_scene.py](templates/basic_scene.py) - 标准 2D 场景模板
- [templates/interactive_scene.py](templates/interactive_scene.py) - 带 self.embed() 的 InteractiveScene
- [templates/3d_scene.py](templates/3d_scene.py) - 带 frame.reorient() 的 3D 场景
- [templates/math_scene.py](templates/math_scene.py) - 数学推导和方程

## 快速参考

### 基本场景结构
```python
from manimlib import *

class MyScene(InteractiveScene):
    def construct(self):
        # 创建 mobject
        circle = Circle()

        # 添加到场景（静态）
        self.add(circle)

        # 或动画
        self.play(ShowCreation(circle))  # 注意：ShowCreation，不是 Create

        # 等待
        self.wait(1)
```

### 渲染命令
```bash
# 渲染并预览
manimgl scene.py MyScene

# 交互模式 — 在第 15 行进入 shell
manimgl scene.py MyScene -se 15

# 写入文件
manimgl scene.py MyScene -w

# 低质量测试
manimgl scene.py MyScene -l
```

### 与 ManimCE 的关键区别

| 功能 | ManimGL (3b1b) | Manim Community |
|---------|----------------|-----------------|
| 导入 | `from manimlib import *` | `from manim import *` |
| CLI | `manimgl` | `manim` |
| 数学文本 | `Tex(R"\pi")` | `MathTex(r"\pi")` |
| 场景 | `InteractiveScene` | `Scene` |
| 创建动画 | `ShowCreation` | `Create` |
| 相机 | `self.frame` | `self.camera.frame` |
| 固定在框架 | `mob.fix_in_frame()` | `self.add_fixed_in_frame_mobjects(mob)` |
| 包 | `manimgl` (PyPI) | `manim` (PyPI) |

### 交互式开发工作流程

ManimGL 的杀手级功能是交互式开发：

```bash
# 从第 20 行开始，状态保留
manimgl scene.py MyScene -se 20
```

在交互模式中：
```python
# 复制代码到剪贴板，然后运行：
checkpoint_paste()           # 带动画运行
checkpoint_paste(skip=True)  # 立即运行（无动画）
checkpoint_paste(record=True) # 运行时录制
```

### 相机控制（self.frame）

```python
# 获取相机框架
frame = self.frame

# 3D 重新定向（phi, theta, gamma, center, height）
frame.reorient(45, -30, 0, ORIGIN, 8)

# 动画化相机移动
self.play(frame.animate.reorient(60, -45, 0))

# 在 3D 移动期间将 mobject 固定在屏幕空间
title.fix_in_frame()
```

### 带 Tex 类的 LaTeX

```python
# 使用大写 R 的原始字符串
formula = Tex(R"\int_0^1 x^2 \, dx = \frac{1}{3}")

# 使用 t2c 进行颜色映射
equation = Tex(
    R"E = mc^2",
    t2c={"E": BLUE, "m": GREEN, "c": YELLOW}
)

# 隔离子串用于动画
formula = Tex(R"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}")
formula.set_color_by_tex("n", BLUE)
```

### 常见模式

#### 用于调试的嵌入
```python
def construct(self):
    circle = Circle()
    self.play(ShowCreation(circle))
    self.embed()  # 在此处进入 IPython shell
```

#### 设置 3D 地平面
```python
self.set_floor_plane("xz")  # 使 xy 成为观察平面
```

#### 文本可读性的背景描边
```python
text = Text("Label")
text.set_backstroke(BLACK, 5)  # 文本后方的黑色轮廓
```

### 安装

```bash
# 安装 ManimGL
pip install manimgl

# 检查安装
manimgl --version
```

### 应避免的常见陷阱

1. **版本混淆** - 确保使用 `manimgl`，而不是 `manim`（社区版）
2. **ShowCreation 与 Create** - ManimGL 使用 `ShowCreation`，不是 `Create`
3. **Tex 与 MathTex** - ManimGL 使用带大写 R 原始字符串的 `Tex`
4. **self.frame 与 self.camera.frame** - ManimGL 直接使用 `self.frame`
5. **fix_in_frame()** - 在 mobject 上调用，而不是在场景上
6. **交互模式** - 使用 `-se` 标志进行交互式开发

## 许可与署名

本技能包含改编自 [3Blue1Brown 的视频仓库](https://github.com/3b1b/videos)（Grant Sanderson 创作）的示例代码。

**许可协议：** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

- **要求署名** - 同时注明 3Blue1Brown 和改编者
- **非商业用途** - 不可用于商业目的
- **相同方式共享** - 衍生作品必须使用相同许可协议

详见 [LICENSE.txt](LICENSE.txt)。
