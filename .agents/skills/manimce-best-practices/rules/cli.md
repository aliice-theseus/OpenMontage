---
name: cli
description: 命令行界面、渲染选项和质量标志
metadata:
  tags: cli, render, quality, preview, command, terminal
---

# Manim CLI

用于渲染场景的 `manim` 命令行界面。

## 基本用法

```bash
# 渲染场景
manim file.py SceneName

# 带预览（渲染后打开视频）
manim -p file.py SceneName

# 低质量预览（快速）
manim -pql file.py SceneName
```

## 质量标志

适用于不同用例的质量预设：

```bash
# 低质量：854x480, 15fps（快速测试）
manim -ql file.py SceneName

# 中等质量：1280x720, 30fps
manim -qm file.py SceneName

# 高质量：1920x1080, 60fps
manim -qh file.py SceneName

# 2K 质量：2560x1440, 60fps
manim -qp file.py SceneName

# 4K 质量：3840x2160, 60fps
manim -qk file.py SceneName
```

### 常见组合

```bash
# 预览 + 低质量（开发工作流）
manim -pql file.py SceneName

# 预览 + 高质量（最终检查）
manim -pqh file.py SceneName
```

## 预览标志

```bash
# -p：渲染后打开视频
manim -p file.py SceneName

# 无 -p：仅渲染（不自动打开）
manim file.py SceneName
```

## 渲染多个场景

```bash
# 渲染文件中的所有场景
manim -a file.py

# 渲染指定场景
manim file.py Scene1 Scene2 Scene3
```

## 输出选项

### 仅保存最后一帧

```bash
# -s：仅将最后一帧保存为 PNG
manim -s file.py SceneName

# 带质量
manim -sql file.py SceneName
```

### 输出格式

```bash
# GIF 输出
manim --format gif file.py SceneName

# PNG 序列
manim --format png file.py SceneName

# WebM（默认为 MP4）
manim --format webm file.py SceneName
```

### 自定义输出目录

```bash
manim -o custom_name file.py SceneName
manim --media_dir /path/to/output file.py SceneName
```

## 帧控制

```bash
# 从特定动画编号开始
manim -n 5 file.py SceneName

# 渲染动画 3 到 7 帧
manim -n 3,7 file.py SceneName
```

## 分辨率和帧率

```bash
# 自定义分辨率
manim -r 1920,1080 file.py SceneName

# 自定义帧率
manim --fps 24 file.py SceneName

# 同时设置
manim -r 1280,720 --fps 30 file.py SceneName
```

## 透明背景

```bash
# 使用透明背景渲染
manim -t file.py SceneName
```

## 渲染器选择

```bash
# Cairo 渲染器（默认，2D）
manim --renderer cairo file.py SceneName

# OpenGL 渲染器（3D，更快预览）
manim --renderer opengl file.py SceneName
```

## 其他有用标志

```bash
# 详细输出
manim -v DEBUG file.py SceneName

# 安静模式
manim -v WARNING file.py SceneName

# 显示进度条
manim --progress_bar display file.py SceneName

# 禁用缓存
manim --disable_caching file.py SceneName

# 即使无动画也写入视频
manim --write_to_movie file.py SceneName
```

## 帮助

```bash
# 显示所有选项
manim --help

# 显示渲染命令选项
manim render --help
```

## 其他命令

```bash
# 检查安装和依赖
manim checkhealth

# 初始化新项目
manim init

# 显示配置值
manim cfg show

# 将当前配置写入文件
manim cfg write

# 列出已安装的插件
manim plugins -l
```

## Jupyter Notebook 支持

在 Jupyter notebook 中使用 `%%manim` 单元格魔术命令：

```python
%%manim -qm -v WARNING MyScene
class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

标志用法与 CLI 相同（`-qm`、`-ql` 等）。

## 典型开发工作流

```bash
# 1. 快速预览开发
manim -pql scene.py MyScene

# 2. 中等质量检查
manim -pqm scene.py MyScene

# 3. 最终高质量渲染
manim -qh scene.py MyScene

# 4. 创建 GIF 用于分享
manim --format gif -qm scene.py MyScene
```

## 最佳实践

1. **开发使用 -pql** - 快速迭代周期
2. **最终输出使用 -qh** - 良好质量，合理渲染时间
3. **缩略图使用 -s** - 快速最后一帧捕获
4. **谨慎使用 -a** - 渲染所有内容，可能很慢
5. **演示使用 --format gif** - 易于分享和嵌入
