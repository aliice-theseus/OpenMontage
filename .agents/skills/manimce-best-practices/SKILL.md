---
name: manimce-best-practices
description: |
  触发条件：(1) 用户提及"manim"或"Manim Community"或"ManimCE"，(2) 代码包含`from manim import *`，(3) 用户运行`manim` CLI命令，(4) 使用Scene、MathTex、Create()或ManimCE特有类。

  Manim社区版最佳实践 - 社区维护的Python动画引擎。涵盖Scene结构、动画、LaTeX/MathTex、使用ThreeDScene的3D、相机控制、样式和CLI使用。

  不适用于ManimGL/3b1b版本（使用`manimlib`导入和`manimgl` CLI）。
---

## 使用方法

阅读各个规则文件以获取详细解释和代码示例：

### 核心概念
- [rules/scenes.md](rules/scenes.md) - Scene结构、construct方法和场景类型
- [rules/mobjects.md](rules/mobjects.md) - Mobject类型、VMobject、Groups和定位
- [rules/animations.md](rules/animations.md) - 动画类、播放动画和时间控制

### 创建与变换
- [rules/creation-animations.md](rules/creation-animations.md) - Create、Write、FadeIn、DrawBorderThenFill
- [rules/transform-animations.md](rules/transform-animations.md) - Transform、ReplacementTransform、变形
- [rules/animation-groups.md](rules/animation-groups.md) - AnimationGroup、LaggedStart、Succession

### 文本与数学
- [rules/text.md](rules/text.md) - Text mobject、字体和样式
- [rules/latex.md](rules/latex.md) - MathTex、Tex、LaTeX渲染和公式着色
- [rules/text-animations.md](rules/text-animations.md) - Write、AddTextLetterByLetter、TypeWithCursor

### 样式与外观
- [rules/colors.md](rules/colors.md) - 颜色常量、渐变和颜色操作
- [rules/styling.md](rules/styling.md) - 填充、描边、不透明度和视觉属性

### 定位与布局
- [rules/positioning.md](rules/positioning.md) - move_to、next_to、align_to、shift方法
- [rules/grouping.md](rules/grouping.md) - VGroup、Group、arrange和布局模式

### 坐标系与绘图
- [rules/axes.md](rules/axes.md) - Axes、NumberPlane、坐标系
- [rules/graphing.md](rules/graphing.md) - 绘制函数、参数曲线
- [rules/3d.md](rules/3d.md) - ThreeDScene、3D坐标轴、曲面、相机朝向

### 动画控制
- [rules/timing.md](rules/timing.md) - 速率函数、缓动、run_time、lag_ratio
- [rules/updaters.md](rules/updaters.md) - Updaters、ValueTracker、动态动画
- [rules/camera.md](rules/camera.md) - MovingCameraScene、缩放、平移、帧操作

### 配置与CLI
- [rules/cli.md](rules/cli.md) - 命令行界面、渲染选项、质量标志
- [rules/config.md](rules/config.md) - 配置系统、manim.cfg、设置

### 形状与几何
- [rules/shapes.md](rules/shapes.md) - Circle、Square、Rectangle、Polygon和几何基本体
- [rules/lines.md](rules/lines.md) - Line、Arrow、Vector、DashedLine和连接器

## 工作示例

完整、经过测试的示例文件，展示常见模式：

- [examples/basic_animations.py](examples/basic_animations.py) - 形状创建、文本、交错动画、路径移动
- [examples/math_visualization.py](examples/math_visualization.py) - LaTeX方程、颜色编码数学、推导
- [examples/updater_patterns.py](examples/updater_patterns.py) - ValueTracker、动态动画、物理仿真
- [examples/graph_plotting.py](examples/graph_plotting.py) - 坐标轴、函数、面积、黎曼和、极坐标图
- [examples/3d_visualization.py](examples/3d_visualization.py) - ThreeDScene、曲面、3D相机、参数曲线

## 场景模板

复制并修改这些模板以开始新项目：

- [templates/basic_scene.py](templates/basic_scene.py) - 标准2D场景模板
- [templates/camera_scene.py](templates/camera_scene.py) - 带缩放/平移的MovingCameraScene
- [templates/threed_scene.py](templates/threed_scene.py) - 带曲面和相机旋转的3D场景

## 快速参考

### 基本场景结构
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # 创建mobject
        circle = Circle()

        # 添加到场景（静态）
        self.add(circle)

        # 或动画
        self.play(Create(circle))

        # 等待
        self.wait(1)
```

### 渲染命令
```bash
# 基本渲染带预览
manim -pql scene.py MyScene

# 质量标志：-ql（低）、-qm（中）、-qh（高）、-qk（4k）
manim -pqh scene.py MyScene
```

### 与3b1b/ManimGL的主要区别

| 特性 | Manim社区版 | 3b1b/ManimGL |
|---------|-----------------|--------------|
| 导入 | `from manim import *` | `from manimlib import *` |
| CLI | `manim` | `manimgl` |
| 数学文本 | `MathTex(r"\pi")` | `Tex(R"\pi")` |
| 场景 | `Scene` | `InteractiveScene` |
| 包 | `manim` (PyPI) | `manimgl` (PyPI) |

### Jupyter Notebook 支持

使用 `%%manim` 单元格魔术命令：

```python
%%manim -qm MyScene
class MyScene(Scene):
    def construct(self):
        self.play(Create(Circle()))
```

### 常见陷阱

1. **版本混淆** - 确保使用 `manim`（社区版），不是 `manimgl`（3b1b版本）
2. **检查导入** - `from manim import *` 是 ManimCE；`from manimlib import *` 是 ManimGL
3. **过时的教程** - 视频教程可能已过时；优先参考官方文档
4. **manimpango 问题** - 如果文本渲染失败，请检查 manimpango 安装要求
5. **Windows 的 PATH 问题** - 如果找不到 `manim` 命令，使用 `python -m manim` 或检查 PATH

### 安装

```bash
# 安装 Manim 社区版
pip install manim

# 检查安装
manim checkhealth
```

### 有用命令

```bash
manim -pql scene.py Scene    # 低质量预览（开发用）
manim -pqh scene.py Scene    # 高质量预览
manim --format gif scene.py  # 输出为 GIF
manim checkhealth            # 验证安装
manim plugins -l             # 列出插件
```
