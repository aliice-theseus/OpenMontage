# ManimGL 配置

ManimGL 使用 `custom_config.yml` 文件进行配置。这些文件控制目录、相机设置、窗口属性等。

## 配置文件位置

### 默认位置

ManimGL 按此顺序查找 `custom_config.yml`：

1. 当前目录
2. 父目录（递归向上到项目根目录）
3. ManimGL 安装目录

```
my_project/
├── custom_config.yml      # 项目级配置
├── scenes/
│   ├── custom_config.yml  # 场景级配置（覆盖项目配置）
│   └── scene.py
└── manimlib/              # ManimGL 安装
```

### 多个配置

```bash
# 使用特定配置文件
manimgl scene.py MyScene --config_file /path/to/config.yml

# 带多个配置的项目结构
project/
├── custom_config.yml          # 项目默认配置
├── experiments/
│   ├── custom_config.yml      # 实验覆盖配置
│   └── test_scene.py
└── final/
    ├── custom_config.yml      # 高质量设置
    └── final_scene.py
```

## 基本配置

### 最小化 custom_config.yml

```yaml
# 目录
directories:
  output: "./media/videos"
  raster_images: "./media/images"
  vector_images: "./media/svg"
  sounds: "./media/sounds"
  data: "./media/data"

# 窗口配置
window_config:
  size: "default"  # 或 "fullscreen"

# 相机设置
camera_config:
  pixel_height: 1080
  pixel_width: 1920
  frame_rate: 60
```

## 详细配置选项

### 目录配置

```yaml
directories:
  # 渲染视频保存位置
  output: "/path/to/output/videos"

  # 临时文件存放位置
  temporary_storage: "/tmp/manim"

  # 图像资源
  raster_images: "./assets/images"
  vector_images: "./assets/svg"

  # 音频资源
  sounds: "./assets/audio"

  # 数据文件
  data: "./assets/data"

  # LaTeX 模板
  tex_templates: "./assets/tex_templates"

  # 字体目录
  fonts: "./assets/fonts"
```

### 相机配置

```yaml
camera_config:
  # 分辨率
  pixel_width: 1920
  pixel_height: 1080

  # 帧率
  frame_rate: 60

  # 背景颜色
  background_color: "#000000"

  # 帧设置
  frame_height: 8.0
  frame_width: 14.222222222222221  # 16:9 宽高比

  # 质量预设
  # 这些会覆盖 pixel_width、pixel_height、frame_rate
  quality:
    low:
      pixel_width: 854
      pixel_height: 480
      frame_rate: 15
    medium:
      pixel_width: 1280
      pixel_height: 720
      frame_rate: 30
    high:
      pixel_width: 1920
      pixel_height: 1080
      frame_rate: 60
    ultra_high:
      pixel_width: 3840
      pixel_height: 2160
      frame_rate: 60
```

### 窗口配置

```yaml
window_config:
  # 窗口大小："default"、"fullscreen" 或 [width, height]
  size: "default"
  # size: "fullscreen"
  # size: [1280, 720]

  # 窗口在屏幕上的位置
  position: "UR"  # 右上角
  # 选项：UL、UR、DL、DR、TOP、BOTTOM、LEFT、RIGHT、CENTER

  # 显示显示器编号（用于多显示器设置）
  monitor: 0

  # 窗口标题
  window_title: "ManimGL Preview"

  # 在标题中显示文件名
  show_file_name_in_title: true
```

### 样式配置

```yaml
style:
  # 默认颜色常量
  background_color: "#000000"

  # 字体设置
  font: "Consolas"
  tex_font: "Latin Modern Math"

  # 默认描边宽度
  stroke_width: 4

  # 默认动画运行时间
  default_animation_run_time: 1.0
```

### 通用导入配置

```yaml
# 自动导入常用模块
universal_import_line: |
  from manimlib import *
  import numpy as np
  import itertools as it
```

## 质量预设

### 命令行覆盖

```bash
# 使用低质量预设
manimgl scene.py MyScene -l

# 使用中等质量
manimgl scene.py MyScene -m

# 使用高质量
manimgl scene.py MyScene -h

# 使用 4K 质量
manimgl scene.py MyScene --uhd
```

### 自定义质量预设

```yaml
camera_config:
  quality:
    custom:
      pixel_width: 2560
      pixel_height: 1440
      frame_rate: 120
```

## LaTeX 配置

### TeX 配置

```yaml
tex_config:
  # TeX 编译器
  tex_compiler: "latex"  # 或 "xelatex"、"lualatex"

  # TeX 模板
  tex_template: "tex_template.tex"

  # 附加宏包
  tex_packages:
    - "amsmath"
    - "amssymb"
    - "mathtools"

  # 文本到 LaTeX 映射
  text_to_replace: {
    # 常用符号的替换
    "pi": "\\pi",
    "alpha": "\\alpha"
  }
```

## 项目级配置

### 开发配置（快速迭代）

```yaml
# dev_config.yml
directories:
  output: "./output/dev"

camera_config:
  pixel_height: 480
  pixel_width: 854
  frame_rate: 15

window_config:
  size: [1280, 720]
  position: "UR"
```

用法：

```bash
manimgl scene.py MyScene --config_file dev_config.yml
```

### 生产配置（高质量）

```yaml
# prod_config.yml
directories:
  output: "./output/final"

camera_config:
  pixel_height: 2160
  pixel_width: 3840
  frame_rate: 60

style:
  default_animation_run_time: 1.5
```

## 运行时配置覆盖

### 命令行覆盖

```bash
# 覆盖单个值
manimgl scene.py MyScene --config camera_config.frame_rate=30

# 覆盖多个值
manimgl scene.py MyScene \
  --config camera_config.frame_rate=30 \
  --config camera_config.pixel_width=1280 \
  --config camera_config.pixel_height=720

# 覆盖输出目录
manimgl scene.py MyScene --config directories.output=/tmp/manim_output
```

## 完整示例配置

### 完整的 custom_config.yml

```yaml
# 目录配置
directories:
  output: "./media/videos"
  temporary_storage: "/tmp/manim"
  raster_images: "./assets/images"
  vector_images: "./assets/svg"
  sounds: "./assets/audio"
  data: "./assets/data"
  tex_templates: "./assets/tex"
  fonts: "./assets/fonts"

# 相机配置
camera_config:
  pixel_width: 1920
  pixel_height: 1080
  frame_rate: 60
  background_color: "#0a0a0a"
  frame_height: 8.0
  frame_width: 14.222222222222221

# 窗口配置
window_config:
  size: "default"
  position: "UR"
  monitor: 0
  window_title: "ManimGL Preview"
  show_file_name_in_title: true

# 样式配置
style:
  background_color: "#0a0a0a"
  font: "Consolas"
  tex_font: "Latin Modern Math"
  stroke_width: 4
  default_animation_run_time: 1.0

# TeX 配置
tex_config:
  tex_compiler: "latex"
  tex_template: "tex_template.tex"
  tex_packages:
    - "amsmath"
    - "amssymb"
    - "mathtools"
    - "physics"

# 通用导入
universal_import_line: |
  from manimlib import *
  import numpy as np
  import itertools as it
  import random

# 日志
log_level: "INFO"  # DEBUG、INFO、WARNING、ERROR
```

## 最佳实践

1. **分离开发和生成配置**：为开发和最终渲染使用不同的配置
2. **项目级配置**：将 `custom_config.yml` 放在项目根目录
3. **测试时覆盖**：使用 `--config` 标志进行临时更改
4. **版本控制**：将 `custom_config.yml` 提交到 git
5. **记录自定义设置**：添加注释解释非标准值
6. **一致路径**：使用相对路径以便于移植
7. **质量预设**：使用内置质量标志（-l、-m、-h）代替手动分辨率更改

## 常见配置

### YouTube 视频（1080p）

```yaml
camera_config:
  pixel_width: 1920
  pixel_height: 1080
  frame_rate: 60
  background_color: "#000000"
```

### 快速测试

```yaml
camera_config:
  pixel_width: 854
  pixel_height: 480
  frame_rate: 15
```

### 4K 生产

```yaml
camera_config:
  pixel_width: 3840
  pixel_height: 2160
  frame_rate: 60
```

### 竖屏视频（TikTok/Shorts）

```yaml
camera_config:
  pixel_width: 1080
  pixel_height: 1920
  frame_rate: 60
  frame_height: 14.222222222222221
  frame_width: 8.0
```

## 故障排除

### 配置未加载

```bash
# 检查正在使用哪个配置
manimgl scene.py MyScene --verbose

# 显式指定配置
manimgl scene.py MyScene --config_file ./custom_config.yml
```

### 无效配置

- 确保 YAML 语法正确（缩进、冒号等）
- 检查配置键中的拼写错误
- 验证路径存在且可访问
- 路径含空格时使用引号

### 性能问题

```yaml
# 为测试降低质量
camera_config:
  pixel_width: 854
  pixel_height: 480
  frame_rate: 15

# 使用 SSD 上的临时存储
directories:
  temporary_storage: "/path/to/fast/storage"
```
