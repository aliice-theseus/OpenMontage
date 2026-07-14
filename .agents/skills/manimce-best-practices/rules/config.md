---
name: config
description: 配置系统、manim.cfg 和设置
metadata:
  tags: config, configuration, settings, manim.cfg, options
---

# 配置

通过文件和代码配置 Manim 的行为。

## 配置层次结构

Manim 按以下顺序读取配置（优先级从高到低）：
1. 命令行参数（最高优先级）
2. 当前目录中的用户 `manim.cfg`
3. 用户的全局配置
4. 默认值（最低优先级）

## manim.cfg 文件

在项目目录中创建 `manim.cfg` 文件：

```ini
[CLI]
# 渲染后预览
preview = True

# 默认质量
quality = medium_quality

# 输出格式
format = mp4

# 帧率
frame_rate = 30

[output]
# 自定义输出目录
media_dir = ./media

# 保存最后一帧为 PNG
save_last_frame = False

[renderer]
# 背景颜色
background_color = BLACK

[style]
# 默认字体
font = Arial
```

## 常用配置选项

### CLI 部分

```ini
[CLI]
# 质量预设：low_quality, medium_quality, high_quality, production_quality, fourk_quality
quality = medium_quality

# 渲染后预览视频
preview = True

# 帧率
frame_rate = 30

# 输出格式：mp4, gif, mov, webm, png
format = mp4

# 透明背景
transparent = False

# 进度条：display, leave, none
progress_bar = display
```

### 渲染部分

```ini
[renderer]
# 背景颜色（十六进制或颜色名称）
background_color = #1e1e1e

# 渲染器类型：cairo, opengl
renderer = cairo
```

### 分辨率

```ini
[CLI]
# 帧尺寸
pixel_width = 1920
pixel_height = 1080
```

## 编程式配置

在 Python 代码中访问和修改配置：

```python
# 访问配置值
config.pixel_width  # 例如 1920
config.frame_rate  # 例如 30
config.background_color  # 例如 BLACK

# 修改配置（在创建场景之前）
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60
config.background_color = BLUE_E
```

### 在场景中

```python
class MyScene(Scene):
    def construct(self):
        # 访问帧尺寸
        width = config.frame_width
        height = config.frame_height

        # 创建匹配帧大小的矩形
        frame_rect = Rectangle(
            width=width,
            height=height,
            stroke_color=WHITE
        )
        self.add(frame_rect)
```

## 背景颜色

### 在配置文件中

```ini
[renderer]
background_color = BLACK
# 或十六进制颜色
background_color = #1a1a2e
```

### 在代码中

```python
class DarkBackground(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        # ... 场景的其余部分
```

## 输出目录结构

默认媒体目录结构：
```
media/
├── videos/
│   └── scene_file/
│       ├── 480p15/       # 低质量
│       ├── 720p30/       # 中等质量
│       ├── 1080p60/      # 高质量
│       └── 2160p60/      # 4K 质量
├── images/
│   └── scene_file/
│       └── SceneName.png
└── Tex/                  # LaTeX 缓存
```

### 自定义输出目录

```ini
[output]
media_dir = ./output
```

或通过 CLI：
```bash
manim --media_dir ./output file.py Scene
```

## TeX 配置

用于 LaTeX 渲染：

```ini
[tex]
# 自定义前言
preamble = \usepackage{amsmath}\usepackage{amssymb}

# TeX 编译器
tex_compiler = latex
```

## 缓存

```ini
[CLI]
# 禁用缓存（用于调试）
disable_caching = True

# 最大缓存文件数
max_files_cached = 100
```

## 查看当前配置

```bash
# 显示所有配置值
manim cfg show

# 显示特定部分
manim cfg show CLI

# 将当前配置写入文件
manim cfg write
```

## 项目特定配置

在项目根目录创建 `manim.cfg`：

```ini
[CLI]
quality = high_quality
preview = True
frame_rate = 60

[renderer]
background_color = #0d1117

[output]
media_dir = ./renders
```

## 插件

Manim 具有可扩展的插件系统：

```bash
# 列出已安装的插件
manim plugins -l

# 安装插件
pip install manim-pluginname
```

在 `manim.cfg` 中启用插件：

```ini
[CLI]
plugins = manim-pluginname
# 多个插件：
plugins = plugin1,plugin2
```

## 最佳实践

1. **使用 manim.cfg 设置项目默认值** - 团队间一致的设置
2. **开发期间保持低质量** - 更快的迭代
3. **在配置中设置 background_color** - 不在每个场景中设置
4. **使用自定义 media_dir** - 保持渲染输出有序
5. **将 manim.cfg 提交到版本控制** - 与协作者共享设置
