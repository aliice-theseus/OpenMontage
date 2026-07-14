# ManimGL 命令行界面

ManimGL 使用 `manimgl` 命令渲染场景。它提供了适用于不同工作流的强大标志。

## 基本用法

### 运行场景

```bash
# 基本语法
manimgl scene_file.py SceneName

# 示例
manimgl my_animation.py SquareToCircle
```

### 自动选择场景

```bash
# 如果文件中只有一个场景，它将自动运行
manimgl my_animation.py

# 如果有多个场景，将显示菜单供选择
manimgl my_animations.py
```

## 常用标志

### 写入文件

```bash
# 写入文件（无预览）
manimgl scene.py MyScene -w

# 写入并打开文件
manimgl scene.py MyScene -o

# 仅显示最后一帧
manimgl scene.py MyScene -s

# 将最后一帧保存为图像并显示
manimgl scene.py MyScene -so
```

### 交互模式

```bash
# 跳到第 15 行并进入交互模式
manimgl scene.py MyScene -se 15

# 在指定行进入交互模式
manimgl scene.py MyScene --skip_animations --embed 20
```

### 显示选项

```bash
# 全屏窗口
manimgl scene.py MyScene -f

# 自定义窗口大小
manimgl scene.py MyScene --resolution 1920,1080

# 隐藏进度条
manimgl scene.py MyScene --quiet
```

## 质量和分辨率

### 分辨率预设

```bash
# 低质量（用于测试）
manimgl scene.py MyScene -l

# 中等质量
manimgl scene.py MyScene -m

# 高质量（1080p）
manimgl scene.py MyScene -h

# 4K 质量
manimgl scene.py MyScene --uhd

# 自定义分辨率
manimgl scene.py MyScene --resolution 2560,1440
```

### 帧率

```bash
# 设置帧率（默认为 60）
manimgl scene.py MyScene --frame_rate 30

# 较低帧率以加快渲染速度
manimgl scene.py MyScene --frame_rate 15
```

## 高级标志

### 跳到特定动画

```bash
# 跳到第 n 个动画
manimgl scene.py MyScene -n 5

# 跳过动画（即时模式）
manimgl scene.py MyScene --skip_animations
```

### 输出选项

```bash
# 指定输出文件
manimgl scene.py MyScene -o output.mp4

# 保存为 GIF
manimgl scene.py MyScene --format gif

# 透明背景
manimgl scene.py MyScene --transparent
```

### 配置

```bash
# 使用自定义配置文件
manimgl scene.py MyScene --config_file custom_config.yml

# 设置特定配置值
manimgl scene.py MyScene --config camera_config.frame_rate=30
```

## 交互式开发

### -se 标志

`-se`（跳过并嵌入）标志是 ManimGL 的杀手级功能：

```bash
# 在第 15 行进入交互式 shell
manimgl scene.py MyScene -se 15
```

在交互式 shell 中：

```python
# 使用精简命令（无需 self.）
play(circle.animate.shift(RIGHT))
add(Square())
remove(circle)
wait(2)

# 将代码复制到剪贴板，然后：
checkpoint_paste()              # 带动画运行
checkpoint_paste(skip=True)     # 立即运行
checkpoint_paste(record=True)   # 录制运行过程

# 交互式相机控制
touch()  # 按 'd' + 鼠标旋转，'z' + 滚轮缩放

# 退出
exit()
```

## 文件组织

### 从不同目录运行

```bash
# 从与 manimlib/ 相同的目录
manimgl project/scene.py MyScene

# 使用绝对路径
manimgl /full/path/to/scene.py MyScene

# 使用相对路径
manimgl ../other_project/scene.py MyScene
```

## 组合标志

### 常见组合

```bash
# 高质量，写入并打开
manimgl scene.py MyScene -h -o

# 低质量，全屏，用于测试
manimgl scene.py MyScene -l -f

# 跳过动画，仅最后一帧
manimgl scene.py MyScene -s --skip_animations

# 在第 20 行交互，低质量
manimgl scene.py MyScene -l -se 20

# 保存为 GIF，高质量
manimgl scene.py MyScene -h --format gif -o
```

## 工作流示例

### 开发工作流

```bash
# 1. 初步测试（低质量，快速）
manimgl scene.py MyScene -l

# 2. 在特定点交互式调试
manimgl scene.py MyScene -l -se 25

# 3. 检查最后一帧
manimgl scene.py MyScene -s

# 4. 最终渲染（高质量，保存并打开）
manimgl scene.py MyScene -h -o
```

### 快速预览工作流

```bash
# 立即显示最后一帧
manimgl scene.py MyScene -s

# 如果看起来不错，渲染完整动画
manimgl scene.py MyScene -o
```

### 批量渲染

```bash
# 渲染多个场景
for scene in Scene1 Scene2 Scene3; do
    manimgl scenes.py $scene -h -w
done
```

## 调试标志

### 详细输出

```bash
# 显示详细输出
manimgl scene.py MyScene --verbose

# 显示所有调试信息
manimgl scene.py MyScene --debug
```

### 性能分析

```bash
# 显示性能统计
manimgl scene.py MyScene --profile

# 详细时间信息
manimgl scene.py MyScene --timing
```

## 配置覆盖

### 临时配置更改

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

## 帮助和信息

### 获取帮助

```bash
# 显示所有可用标志
manimgl --help

# 显示版本
manimgl --version

# 列出文件中的场景而不运行
manimgl scene.py --list_scenes
```

## 完整 CLI 参考

### 所有主要标志

```bash
# 质量/分辨率
-l, --low_quality           # 480p, 15fps
-m, --medium_quality        # 720p, 30fps
-h, --high_quality          # 1080p, 60fps
--uhd                       # 4K, 60fps
--resolution WIDTHxHEIGHT   # 自定义分辨率

# 输出
-w, --write_file            # 写入文件
-o, --open                  # 写入并打开
-s, --show_last_frame       # 显示最后一帧
--format FORMAT             # 输出格式（mp4, gif, png）
--transparent               # 透明背景

# 播放
-f, --fullscreen            # 全屏窗口
-n NUM, --skip_to NUM       # 跳到动画编号
--skip_animations           # 跳过所有动画

# 交互
-e, --embed                 # 进入 IPython shell
--skip_animations --embed   # 结束时交互（跳过动画）
-se LINE, --skip_and_embed  # 在指定行号交互

# 配置
--config_file FILE          # 自定义配置文件
--config KEY=VALUE          # 覆盖配置值

# 调试
--verbose                   # 详细输出
--debug                     # 调试模式
--quiet                     # 最小化输出
--profile                   # 性能分析

# 其他
--version                   # 显示版本
--help                      # 显示帮助
--list_scenes               # 列出文件中的场景
```

## 最佳实践

1. **开发时使用 -l**：低质量快速迭代
2. **调试时使用 -se**：在问题点使用交互模式
3. **快速检查使用 -s**：在完整渲染前验证最后一帧
4. **最终发布使用 -h -o**：准备好时使用高质量输出
5. **明智地组合标志**：`-l -f` 用于全屏测试
6. **自定义配置**：为不同项目使用不同配置
7. **脚本化常用命令**：为频繁任务创建 shell 别名

## 常用别名

添加到 `.bashrc` 或 `.zshrc`：

```bash
# 快速预览
alias mgl='manimgl -l'

# 最终渲染
alias mgf='manimgl -h -o'

# 交互式调试
alias mgd='manimgl -l -se'

# 显示最后一帧
alias mgs='manimgl -s'
```

## 故障排除

### 常见问题

```bash
# 场景未找到
manimgl scene.py  # 如果不指定，列出所有场景

# 找不到 manimlib
# 确保在包含 manimlib/ 的目录中，或使用完整路径

# 窗口不显示
# 检查 custom_config.yml 中的 window_config

# 性能不佳
# 使用 -l 标志，降低 frame_rate 或分辨率
```

## 示例命令

```bash
# 简单预览
manimgl examples/basic_animations.py SquareToCircle

# 高质量渲染
manimgl examples/basic_animations.py SquareToCircle -h -o

# 在第 30 行交互式调试
manimgl examples/basic_animations.py SquareToCircle -se 30

# 保存为 GIF
manimgl examples/basic_animations.py SquareToCircle --format gif -o

# 自定义分辨率
manimgl examples/basic_animations.py SquareToCircle --resolution 2560,1440

# 跳到第 5 个动画并显示
manimgl examples/basic_animations.py SquareToCircle -n 5

# 全屏，低质量，用于测试
manimgl examples/basic_animations.py SquareToCircle -l -f
```
