---
name: manimce-best-practices
description: |
  触发条件：(1) 用户提到 "manim" 或 "Manim Community" 或 "ManimCE"，(2) 代码包含 `from manim import *`，(3) 用户运行 `manim` CLI 命令，(4) 使用 Scene、MathTex、Create() 或 ManimCE 特定类。

  Manim Community Edition 最佳实践——社区维护的 Python 动画引擎。涵盖场景结构、动画、LaTeX/MathTex、使用 ThreeDScene 的 3D 动画、相机控制、样式和 CLI 使用。

  不适用于 ManimGL/3b1b 版本（使用 `manimlib` 导入和 `manimgl` CLI）。
---

## 如何使用

阅读各个规则文件以获取详细解释和代码示例：

### 核心概念
- [rules/scenes.md](rules/scenes.md) —— 场景结构、construct 方法和场景类型
- [rules/mobjects.md](rules/mobjects.md) —— Mobject 类型、VMobject、Groups 和定位
- [rules/animations.md](rules/animations.md) —— 动画类、播放动画和时序

### 创建与变形
- [rules/creation-animations.md](rules/creation-animations.md) —— Create、Write、FadeIn、DrawBorderThenFill
- [rules/transform-animations.md](rules/transform-animations.md) —— Transform、ReplacementTransform、形变
- [rules/animation-groups.md](rules/animation-groups.md) —— AnimationGroup、LaggedStart、Succession

### 文本与数学
- [rules/text.md](rules/text.md) —— 文本 mobjects、字体和样式
- [rules/latex.md](rules/latex.md) —— MathTex、Tex、LaTeX 渲染和公式着色
- [rules/text-animations.md](rules/text-animations.md) —— Write、AddTextLetterByLetter、TypeWithCursor

### 样式与外观
- [rules/colors.md](rules/colors.md) —— 颜色常量、渐变和颜色操作
- [rules/styling.md](rules/styling.md) —— 填充、描边、不透明度和视觉属性

### 定位与布局
- [rules/positioning.md](rules/positioning.md) —— move_to、next_to、align_to、shift 方法
- [rules/grouping.md](rules/grouping.md) —— VGroup、Group、arrange 和布局模式

### 坐标系统与绘图
- [rules/axes.md](rules/axes.md) —— Axes、NumberPlane、坐标系统
- [rules/graphing.md](rules/graphing.md) —— 绘制函数、参数曲线
- [rules/3d.md](rules/3d.md) —— ThreeDScene、3D 坐标轴、曲面、相机方向

### 动画控制
- [rules/timing.md](rules/timing.md) —— 速率函数、缓动、run_time、lag_ratio
- [rules/updaters.md](rules/updaters.md) —— Updaters、ValueTracker、动态动画
- [rules/camera.md](rules/camera.md) —— MovingCameraScene、缩放、平移、帧操作

### 配置与 CLI
- [rules/cli.md](rules/cli.md) —— 命令行界面、渲染选项、质量标志
- [rules/config.md](rules/config.md) —— 配置系统、manim.cfg、设置

### 形状与几何
- [rules/shapes.md](rules/shapes.md) —— Circle、Square、Rectangle、Polygon 和几何图元
- [rules/lines.md](rules/lines.md) —— Line、Arrow、Vector、DashedLine 和连接器

## 工作示例

完整、经过测试的示例文件，展示常见模式：

- [examples/basic_animations.py](examples/basic_animations.py) —— 形状创建、文本、错位动画、路径移动
- [examples/math_visualization.py](examples/math_visualization.py) —— LaTeX 公式、彩色数学、推导过程
- [examples/updater_patterns.py](examples/updater_patterns.py) —— ValueTracker、动态动画、物理模拟
- [examples/graph_plotting.py](examples/graph_plotting.py) —— 坐标轴、函数、面积、黎曼和、极坐标图
- [examples/3d_visualization.py](examples/3d_visualization.py) —— ThreeDScene、曲面、3D 相机、参数曲线

## 场景模板

复制并修改这些模板以开始新项目：

- [templates/basic_scene.py](templates/basic_scene.py) —— 标准 2D 场景模板
- [templates/camera_scene.py](templates/camera_scene.py) —— 带缩放/平移的 MovingCameraScene
- [templates/threed_scene.py](templates/threed_scene.py) —— 带曲面和相机旋转的 3D 场景

## 快速参考

### 基本场景结构
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # 创建 mobjects
        circle = Circle()

        # 添加到场景（静态）
        self.add(circle)

        # 或动画化
        self.play(Create(circle))

        # 等待
        self.wait(1)
```

### 渲染命令
```bash
# 带预览的基本渲染
manim -pql scene.py MyScene

# 质量标志：-ql（低）、-qm（中）、-qh（高）、-qk（4K）
manim -pqh scene.py MyScene
```

### 与 3b1b/ManimGL 的主要区别

| 功能 | Manim Community | 3b1b/ManimGL |
|---------|-----------------|--------------|
| 导入 | `from manim import *` | `from manimlib import *` |
| CLI | `manim` | `manimgl` |
| 数学文本 | `MathTex(r"\pi")` | `Tex(R"\pi")` |
| 场景 | `Scene` | `InteractiveScene` |
| 包 | `manim`（PyPI） | `manimgl`（PyPI） |

### Jupyter Notebook 支持

使用 `%%manim` 单元格魔法：

```python
%%manim -qm MyScene
class MyScene(Scene):
    def construct(self):
        self.play(Create(Circle()))
```

### 常见陷阱

1. **版本混淆** —— 确保使用 `manim`（Community），而不是 `manimgl`（3b1b 版本）
2. **检查导入** —— `from manim import *` 是 ManimCE；`from manimlib import *` 是 ManimGL
3. **过时的教程** —— 视频教程可能已过时；优先参考官方文档
4. **manimpango 问题** —— 如果文本渲染失败，检查 manimpango 安装要求
5. **Windows PATH 问题** —— 如果找不到 `manim` 命令，使用 `python -m manim` 或检查 PATH

### 安装

```bash
# 安装 Manim Community
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
