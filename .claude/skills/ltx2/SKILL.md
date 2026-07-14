---
name: ltx2
description: 使用 LTX-2.3 22B 进行 AI 视频生成 — 文生视频、图生视频片段，用于视频制作。在生成视频片段、将图片动画化、创建 B-roll、动画背景或运动内容时使用。触发词包括视频生成、图片动画化、B-roll、运动、视频片段、文生视频、图生视频。
---

# LTX-2.3 视频生成

使用 LTX-2.3 22B DiT 模型从文本提示或图片生成约 5 秒的视频片段。
运行在 Modal（A100-80GB）上。需在 `.env` 中配置 `MODAL_LTX2_ENDPOINT_URL`。

## 快速参考

```bash
# 文生视频
python3 tools/ltx2.py --prompt "A sunset over the ocean, golden light on waves, cinematic" --output sunset.mp4

# 图生视频（将静态图片动画化）
python3 tools/ltx2.py --prompt "Gentle camera drift, soft ambient motion" --input photo.jpg --output animated.mp4

# 自定义分辨率和时长
python3 tools/ltx2.py --prompt "..." --width 1024 --height 576 --num-frames 161 --output wide.mp4

# 快速模式（更少步骤，更快）
python3 tools/ltx2.py --prompt "..." --quality fast --output quick.mp4

# 可重现输出
python3 tools/ltx2.py --prompt "..." --seed 42 --output reproducible.mp4
```

## 参数

| 参数 | 默认值 | 描述 |
|-----------|---------|-------------|
| `--prompt` |（必填）| 视频的文本描述 |
| `--input` | - | 图生视频的输入图片 |
| `--width` | 768 | 视频宽度（可被 64 整除） |
| `--height` | 512 | 视频高度（可被 64 整除） |
| `--num-frames` | 121 | 帧数，必须满足 `(n-1) % 8 == 0` |
| `--fps` | 24 | 每秒帧数 |
| `--quality` | standard | `standard`（30 步）或 `fast`（15 步） |
| `--steps` | 30 | 直接覆盖推理步数 |
| `--seed` | 随机 | 用于可重现性的种子 |
| `--output` | 自动 | 输出文件路径 |
| `--negative-prompt` | 合理默认值 | 避免的内容 |

## 有效帧数

`(n - 1) % 8 == 0`: 25（约 1 秒）、49（约 2 秒）、73（约 3 秒）、97（约 4 秒）、**121（约 5 秒，默认）**、161（约 6.7 秒）、193（约 8 秒，最大实用值）。

## 常用分辨率

| 分辨率 | 比例 | 备注 |
|------------|-------|-------|
| 768x512 | 3:2 | 默认，良好平衡 |
| 512x512 | 1:1 | 方形，最快 |
| 1024x576 | 16:9 | 宽屏 |
| 576x1024 | 9:16 | 竖屏/垂直 |

## 提示指南

LTX-2 对电影化的描述响应良好。组合以下维度：

- **摄像机：**"缓慢前推"、"航拍镜头"、"跟拍"、"静态广角"
- **灯光：**"黄金时刻"、"电影化灯光"、"霓虹灯"、"柔和漫射光"
- **运动：**"延时摄影..."、"慢动作"、"轻柔摄像机漂移"、"逐渐过渡"
- **风格：**"35mm 胶片拍摄"、"纪录片风格"、"简洁极简美学"
- **反向提示：**始终隐式避免"最差质量、模糊、抖动、水印、文字、标志"

将提示控制在 200 词以内。具体描述场景。

### 优秀提示

```
# 氛围 b-roll
"Aerial drone shot slowly flying over turquoise ocean waves breaking on white sand, golden hour sunlight, cinematic"

# 产品/科技场景
"Close-up of hands typing on a mechanical keyboard, shallow depth of field, soft desk lamp lighting, cozy atmosphere"

# 抽象背景
"Dark moody abstract background with flowing blue light streaks, subtle geometric grid, bokeh particles floating, cinematic tech atmosphere"

# 动画肖像
"Professional headshot, subtle natural head movement, confident warm expression, studio lighting, shallow depth of field"

# 动画幻灯片/截图
"Gentle subtle particle effects floating across a presentation slide, soft ambient light shifts, very slight camera drift"
```

### 差劲提示

```
# 太模糊
"A cool video"

# 太多竞争性创意
"A cat riding a skateboard while juggling fire on the moon during a thunderstorm"

# 描述文字/UI（模型无法可靠渲染文字）
"A website showing the text 'Welcome to our platform'"
```

## 视频制作用例

### B-Roll 片段
生成氛围感的 5 秒片段，用于解说场景之间的过渡：
```bash
python3 tools/ltx2.py --prompt "Futuristic holographic interface, glowing data visualizations, clean workspace, cinematic" --output broll_tech.mp4
python3 tools/ltx2.py --prompt "Aerial view of European city at golden hour, modern architecture" --output broll_europe.mp4
```

### 动画幻灯片背景
输入幻灯片截图并添加微妙的运动：
```bash
python3 tools/ltx2.py --prompt "Gentle particle effects, soft ambient light shifts, very slight camera drift" --input slide.png --output animated_slide.mp4
```

### 动画肖像
让静态头像生动起来：
```bash
python3 tools/ltx2.py --prompt "Subtle natural head movement, warm expression, professional lighting" --input headshot.png --output animated_portrait.mp4
```

### 品牌片头/片尾
为标题卡片生成抽象动态背景：
```bash
python3 tools/ltx2.py --prompt "Dark moody background with flowing blue and coral light streaks, bokeh particles, cinematic tech atmosphere, no text" --output intro_bg.mp4
```

### 与其他工具结合

LTX-2 生成原始片段。与工具包中的其他工具结合使用：

| 工作流 | 工具 |
|----------|-------|
| 生成片段 → 放大 | `ltx2.py` → `upscale.py` |
| 生成片段 → 添加到 Remotion | `ltx2.py` → 在合成中用作 `<OffthreadVideo>` |
| 生成图片 → 动画化 | `flux2.py` → `ltx2.py --input` |
| 生成片段 → 提取音频 | `ltx2.py` → `ffmpeg -i clip.mp4 -vn audio.wav` |
| 生成片段 → 添加配音 | `ltx2.py` → 与 `qwen3_tts.py` 输出混音 |

## 技术细节

- **模型：** LTX-2.3 22B DiT（Lightricks），bf16
- **GPU：** Modal 上的 A100-80GB（约 $4.68/小时）
- **推理：** 每个片段约 2.5 分钟（768x512，121 帧，30 步）
- **成本：** 每个 5 秒片段约 $0.20-0.25
- **冷启动：** 约 60-90 秒（加载约 55GB 权重）
- **输出：** H.264 MP4，带同步环境音频（24fps）
- **最大时长：** 每个片段约 8 秒（193 帧）

### 已知限制

- **训练数据伪影：** 约 30% 的生成结果可能包含训练数据中的不需要的标志/文字。使用不同的 `--seed` 重新运行。
- **文字渲染：** 无法可靠地在视频中生成可读文字。请改用 Remotion 叠加层。
- **最大时长：** 每个片段约 8 秒。长内容需要拼接。
- **音频：** 生成的音频仅为环境/氛围音。语音和音乐请使用配音/音乐工具。
- **许可证：** 社区许可证 — 收入低于 $10M 免费使用，以上需要商业许可证。

## 设置

```bash
# 1. 创建 HuggingFace 的 Modal 密钥（一次性）
modal secret create huggingface-token HF_TOKEN=hf_your_token

# 2. 部署（下载约 55GB 权重，约需 10 分钟）
modal deploy docker/modal-ltx2/app.py

# 3. 保存端点 URL 到 .env
echo "MODAL_LTX2_ENDPOINT_URL=https://yourname--video-toolkit-ltx2-ltx2-generate.modal.run" >> .env

# 4. 测试
python3 tools/ltx2.py --prompt "A candle flickering on a dark table, cinematic" --output test.mp4
```

**重要提示：** HuggingFace 令牌需要读取访问权限。部署前请接受 [Gemma 3 许可证](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized)。未经认证的下载会受到严格的速率限制。
