---
name: video-toolkit
description: 使用 claude-code-video-toolkit 自主创建专业视频 — AI 配音、图片生成、音乐、虚拟主播和 Remotion 渲染。
metadata:
  openclaw:
    emoji: "🎬"
    skillKey: "video-toolkit"
    os: ["darwin", "linux"]
    requires:
      bins: ["node", "python3", "ffmpeg", "npm"]
---

# 视频工具包

根据文本简报创建专业的解说视频。该工具包使用云 GPU（Modal 或 RunPod）上的开源 AI 模型进行配音、图片生成、音乐和虚拟主播动画。Remotion（React）负责合成和渲染。

## 关键：工具包路径

工具包位于固定路径。**在运行任何工具命令前，始终先 `cd` 到此目录。**

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
```

**切勿在项目目录内运行工具命令。** 工具相对于工具包根目录解析路径。

## 设置

### 步骤 1：检查当前状态

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/verify_setup.py
```

如果所有内容都显示 `[x]`，跳到下面的"快速测试"。否则继续设置。

### 步骤 2：安装 Python 依赖

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
pip3 install --break-system-packages -r tools/requirements.txt
```

注意：Debian/Ubuntu 上使用受管理的 Python（PEP 668）时需要 `--break-system-packages`。在容器内是安全的。

### 步骤 3：配置云 GPU 端点

工具包需要在 `.env` 中配置云 GPU 端点 URL。检查 `.env` 是否存在并包含 Modal 端点：

```bash
cat ~/.openclaw/workspace/claude-code-video-toolkit/.env | grep MODAL
```

如果 Modal 端点已配置，你就准备好了。如果没有，**要求用户提供 Modal 端点 URL** 或设置 Modal：

```bash
pip3 install --break-system-packages modal
python3 -m modal setup   # 打开浏览器进行身份验证

# 部署各工具 — 从输出中捕获端点 URL
cd ~/.openclaw/workspace/claude-code-video-toolkit
modal deploy docker/modal-qwen3-tts/app.py
modal deploy docker/modal-flux2/app.py
modal deploy docker/modal-music-gen/app.py
modal deploy docker/modal-sadtalker/app.py
modal deploy docker/modal-image-edit/app.py
modal deploy docker/modal-upscale/app.py
modal deploy docker/modal-propainter/app.py
modal deploy docker/modal-ltx2/app.py      # 需要: modal secret create huggingface-token HF_TOKEN=hf_...
```

**LTX-2 前置条件：** 在部署 LTX-2 之前，创建 HuggingFace 密钥并接受 [Gemma 3 许可证](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized)：
```bash
modal secret create huggingface-token HF_TOKEN=hf_your_read_access_token
```

将每个 URL 添加到 `.env`：
```
MODAL_QWEN3_TTS_ENDPOINT_URL=https://...modal.run
MODAL_FLUX2_ENDPOINT_URL=https://...modal.run
MODAL_MUSIC_GEN_ENDPOINT_URL=https://...modal.run
MODAL_SADTALKER_ENDPOINT_URL=https://...modal.run
MODAL_IMAGE_EDIT_ENDPOINT_URL=https://...modal.run
MODAL_UPSCALE_ENDPOINT_URL=https://...modal.run
MODAL_DEWATERMARK_ENDPOINT_URL=https://...modal.run
MODAL_LTX2_ENDPOINT_URL=https://...modal.run
```

可选但推荐 — Cloudflare R2 用于可靠的文件传输：
```
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=video-toolkit
```

### 步骤 4：验证和快速测试

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/verify_setup.py
```

所有工具应显示 `[x]`。然后运行快速测试以确认 GPU 流水线正常工作：

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/qwen3_tts.py --text "Hello, this is a test." --speaker Ryan --tone warm --output /tmp/video-toolkit-test.mp3 --cloud modal
```

如果获得有效的 .mp3 文件，设置完成。如果失败，检查：
- `.env` 中有正确的 `MODAL_QWEN3_TTS_ENDPOINT_URL`
- 运行 `python3 tools/verify_setup.py --json` 并检查 `modal_tools` 缺少哪些端点

**成本：** Modal 包含每月 $30 的免费计算额度。一个典型的 60 秒视频成本为 $1-3。

---

## 创建视频

### 步骤 1：创建项目

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
cp -r templates/product-demo projects/PROJECT_NAME
cd projects/PROJECT_NAME
npm install
```

模板：`product-demo`（营销/解说）、`sprint-review`、`sprint-review-v2`（可组合场景）。

### 步骤 2：编写配置

编辑 `projects/PROJECT_NAME/src/config/demo-config.ts`：

```typescript
export const demoConfig: ProductDemoConfig = {
  product: {
    name: '我的产品',
    tagline: '一行概括产品功能',
    website: 'example.com',
  },
  scenes: [
    { type: 'title', durationSeconds: 9, content: { headline: '...', subheadline: '...' } },
    { type: 'problem', durationSeconds: 14, content: { headline: '...', problems: ['...', '...'] } },
    { type: 'solution', durationSeconds: 13, content: { headline: '...', highlights: ['...', '...'] } },
    { type: 'stats', durationSeconds: 12, content: { stats: [{value: '99%', label: '...'}, ...] } },
    { type: 'cta', durationSeconds: 10, content: { headline: '...', links: ['...'] } },
  ],
  audio: {
    backgroundMusicFile: 'audio/bg-music.mp3',
    backgroundMusicVolume: 0.12,
  },
};
```

场景类型：`title`、`problem`、`solution`、`demo`、`feature`、`stats`、`cta`。

**时长规则：** 将 `durationSeconds` 估算为 `ceil(word_count / 2.5) + 2`。在步骤 4 生成音频后需要调整。

### 步骤 3：编写配音脚本

创建 `projects/PROJECT_NAME/VOICEOVER-SCRIPT.md`：

```markdown
## 场景 1：标题（9 秒，约 17 词）
用 AI 构建视频。产品名称工具包让一切变得简单。

## 场景 2：问题（14 秒，约 30 词）
问题陈述写在这里。保持简洁有力、引起共鸣。
```

**每场景字数预算：** `(durationSeconds - 2) * 2.5` 词。减 2 考虑了 1 秒音频延迟 + 1 秒填充。

### 步骤 4：生成资源

**关键：以下所有命令必须从工具包根目录运行，而非项目目录。**

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
```

#### 4a. 背景音乐

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/music_gen.py \
  --preset corporate-bg \
  --duration 90 \
  --output projects/PROJECT_NAME/public/audio/bg-music.mp3 \
  --cloud modal
```

预设：`corporate-bg`、`upbeat-tech`、`ambient`、`dramatic`、`tension`、`hopeful`、`cta`、`lofi`。

#### 4b. 配音（按场景）

**每个场景生成一个 .mp3 文件。不要生成单个配音文件。**

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit

# 场景 01
python3 tools/qwen3_tts.py \
  --text "场景一的配音文本。" \
  --speaker Ryan --tone warm \
  --output projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --cloud modal

# 场景 02
python3 tools/qwen3_tts.py \
  --text "场景二的配音文本。" \
  --speaker Ryan --tone warm \
  --output projects/PROJECT_NAME/public/audio/scenes/02.mp3 \
  --cloud modal

# ... 为每个场景重复
```

**说话者：** `Ryan`、`Aiden`、`Vivian`、`Serena`、`Uncle_Fu`、`Dylan`、`Eric`、`Ono_Anna`、`Sohee`
**语气：** `neutral`、`warm`、`professional`、`excited`、`calm`、`serious`、`storyteller`、`tutorial`

对于声音克隆（需要参考录音）：
```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/qwen3_tts.py \
  --text "要说的文本" \
  --ref-audio assets/voices/reference.m4a \
  --ref-text "参考音频的准确转录" \
  --output projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --cloud modal
```

#### 4c. 场景图片

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/flux2.py \
  --prompt "Dark tech background with blue geometric grid, cinematic lighting" \
  --width 1920 --height 1080 \
  --output projects/PROJECT_NAME/public/images/title-bg.png \
  --cloud modal
```

图片预设（使用 `--preset` 替代 `--prompt --width --height`）：
`title-bg`、`problem`、`solution`、`demo-bg`、`stats-bg`、`cta`、`thumbnail`、`portrait-bg`

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/flux2.py \
  --preset title-bg \
  --output projects/PROJECT_NAME/public/images/title-bg.png \
  --cloud modal
```

#### 4d. 视频片段 — B-Roll 和动画背景（可选）

生成 AI 视频片段，用于 b-roll 过渡、动画幻灯片背景或片头/片尾序列：

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit

# 从文本生成 b-roll 片段
python3 tools/ltx2.py \
  --prompt "Aerial drone shot over a European city at golden hour, cinematic wide angle" \
  --output projects/PROJECT_NAME/public/videos/broll-europe.mp4 \
  --cloud modal

# 动画化幻灯片/截图（图生视频）
python3 tools/ltx2.py \
  --prompt "Gentle particle effects, soft ambient light shifts, very slight camera drift" \
  --input projects/PROJECT_NAME/public/images/title-bg.png \
  --output projects/PROJECT_NAME/public/videos/animated-title.mp4 \
  --cloud modal

# 抽象片头/片尾背景
python3 tools/ltx2.py \
  --prompt "Dark moody abstract background with flowing blue light streaks, bokeh particles, cinematic" \
  --output projects/PROJECT_NAME/public/videos/intro-bg.mp4 \
  --cloud modal
```

在 Remotion 合成中使用 `<OffthreadVideo>`：
```tsx
<OffthreadVideo src={staticFile('videos/broll-europe.mp4')} />
```

**LTX-2 规则：**
- 每个片段最长约 8 秒（193 帧，24fps）。默认约 5 秒（121 帧）。
- 宽/高必须能被 64 整除。默认：768x512。
- 每个片段约 $0.20-0.25，生成时间约 2.5 分钟。
- 冷启动约 60-90 秒。后续片段在预热 GPU 上更快。
- 生成的音频仅为环境音 — 语音和音乐请使用配音/音乐工具。
- 约 30% 的生成结果可能包含训练数据伪影（标志/文字）。使用 `--seed` 重新运行以获取变化。

#### 4e. 虚拟主播（可选）

生成主持人肖像，然后为每个场景动画化片段：

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit

# 1. 生成肖像
python3 tools/flux2.py \
  --prompt "Professional presenter portrait, clean style, dark background, facing camera, upper body" \
  --width 1024 --height 576 \
  --output projects/PROJECT_NAME/public/images/presenter.png \
  --cloud modal

# 2. 生成每个场景的主播片段（每个场景一个，不是长视频）
python3 tools/sadtalker.py \
  --image projects/PROJECT_NAME/public/images/presenter.png \
  --audio projects/PROJECT_NAME/public/audio/scenes/01.mp3 \
  --preprocess full --still --expression-scale 0.8 \
  --output projects/PROJECT_NAME/public/narrator-01.mp4 \
  --cloud modal

# 为每个需要主播的场景重复
```

**SadTalker 规则 — 严格遵循：**
- **始终**使用 `--preprocess full`（默认的 `crop` 输出方形，宽高比错误）
- **始终**使用 `--still`（减少头部运动，看起来专业）
- **始终**生成每个场景的片段（每个 6-15 秒），**绝不**生成一个长视频
- 处理时间：Modal A10G 上每 10 秒音频约 3-4 分钟
- `--expression-scale 0.8` 保持表情微妙（范围 0.0-1.5）

#### 4e. 图片编辑（可选）

从现有图片创建场景变体：

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/image_edit.py \
  --input projects/PROJECT_NAME/public/images/title-bg.png \
  --prompt "Make it darker with red tones, more ominous" \
  --output projects/PROJECT_NAME/public/images/problem-bg.png \
  --cloud modal
```

#### 4f. 放大（可选）

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/upscale.py \
  --input projects/PROJECT_NAME/public/images/some-image.png \
  --output projects/PROJECT_NAME/public/images/some-image-4x.png \
  --scale 4 --cloud modal
```

### 步骤 5：同步时间

**生成配音后始终执行此步骤。** 音频时长与估算值不同。

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
for f in projects/PROJECT_NAME/public/audio/scenes/*.mp3; do
  echo "$(basename $f): $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")s"
done
```

更新 `demo-config.ts` 中每个场景的 `durationSeconds` 为：`ceil(实际音频时长 + 2)`。

示例：如果 `01.mp3` 为 6.8 秒，设置场景 1 的 `durationSeconds` 为 `9`（ceil(6.8 + 2) = 9）。

### 步骤 6：审查静态帧

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit/projects/PROJECT_NAME
npx remotion still src/index.ts ProductDemo --frame=100 --output=/tmp/review-scene1.png
npx remotion still src/index.ts ProductDemo --frame=400 --output=/tmp/review-scene2.png
```

检查：文字截断、动画时间、主播画中画定位、背景对比度。

### 步骤 7：渲染

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit/projects/PROJECT_NAME
npm run render
```

**输出：** `out/ProductDemo.mp4`

---

## 合成模式

### 按场景音频

使用带 1 秒延迟的按场景音频（`from={30}` = 30 帧 = 30fps 下的 1 秒）：

```tsx
<Sequence from={30}>
  <Audio src={staticFile('audio/scenes/01.mp3')} volume={1} />
</Sequence>
```

### 按场景主播画中画

```tsx
<Sequence from={30}>
  <OffthreadVideo
    src={staticFile('narrator-01.mp4')}
    style={{ width: 320, height: 180, objectFit: 'cover' }}
    muted
  />
</Sequence>
```

**始终使用 `<OffthreadVideo>`，绝不使用 `<video>`。** Remotion 需要自己的组件来实现帧精确渲染。

### 转场

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { glitch } from '../../../lib/transitions/presentations/glitch';
import { lightLeak } from '../../../lib/transitions/presentations/light-leak';
```

**绝不从 `lib/transitions` 索引文件导入** — 直接从 `lib/transitions/presentations/` 导入自定义转场。

---

## 错误恢复

| 问题 | 解决方案 |
|---------|----------|
| 工具命令失败提示"没有名为...的模块" | 从工具包根目录运行 `pip3 install --break-system-packages -r tools/requirements.txt` |
| "未配置 MODAL_*_ENDPOINT_URL" | 检查 `.env` 是否有端点 URL。运行 `python3 tools/verify_setup.py` |
| SadTalker 输出为方形/裁剪 | 你忘了 `--preprocess full`。使用该标志重新运行 |
| 音频对场景来说太短/太长 | 重新执行步骤 5（同步时间）并更新配置 |
| `npm run render` 失败 | 确保你在项目目录中，而非工具包根目录。先运行 `npm install` |
| Remotion 中"找不到模块" | 检查导入路径。自定义组件使用 `../../../lib/` 相对路径 |
| Modal 冷启动超时 | 空闲后的首次调用需要 30-120 秒。重试一次 — 第二次调用使用预热 GPU |

---

## 成本估算（Modal）

| 工具 | 典型成本 | 备注 |
|------|-------------|-------|
| Qwen3-TTS | 约 $0.01/场景 | 预热 GPU 上每场景约 20 秒 |
| FLUX.2 | 约 $0.01/图片 | 预热约 3 秒，冷启动约 30 秒 |
| ACE-Step | 约 $0.02-0.05 | 取决于时长 |
| SadTalker | 约 $0.05-0.20/场景 | 每 10 秒音频约 3-4 分钟 |
| Qwen-Edit | 约 $0.03-0.15 | 冷启动约 8 分钟（25GB 模型） |
| RealESRGAN | 约 $0.005/图片 | 非常快 |
| LTX-2.3 | 约 $0.20-0.25/片段 | 每 5 秒片段约 2.5 分钟，A100-80GB |

**60 秒视频总计：** 约 $1-3，取决于场景和主播片段数量。

Modal 入门计划：每月 $30 免费计算额度。应用空闲时自动缩放到零。
