---
name: video-toolkit
description: 使用 claude-code-video-toolkit 自主创建专业视频 — AI 配音、图像生成、音乐、虚拟主播和 Remotion 渲染。
metadata:
  openclaw:
    emoji: "🎬"
    skillKey: "video-toolkit"
    os: ["darwin", "linux"]
    requires:
      bins: ["node", "python3", "ffmpeg", "npm"]
---

# 视频工具包

从文本需求创建专业的解说视频。该工具包使用云端 GPU（Modal 或 RunPod）上的开源 AI 模型进行配音、图像生成、音乐和虚拟主播动画。Remotion（React）处理合成和渲染。

## 关键：工具包路径

工具包位于固定路径。**在运行任何工具命令前，始终先 `cd` 到此目录。**

```bash
TOOLKIT=~/.openclaw/workspace/claude-code-video-toolkit
cd $TOOLKIT
```

**永远不要从项目目录内部运行工具命令。** 工具解析相对于工具包根目录的路径。

## 设置

### 步骤 1：检查当前状态

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/verify_setup.py
```

如果全部显示 `[x]`，跳到下面的"快速测试"。否则继续设置。

### 步骤 2：安装 Python 依赖

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
pip3 install --break-system-packages -r tools/requirements.txt
```

注意：在带有托管 Python（PEP 668）的 Debian/Ubuntu 上需要 `--break-system-packages`。在容器内安全。

### 步骤 3：配置云端 GPU 端点

工具包需要在 `.env` 中配置云端 GPU 端点 URL。检查 `.env` 是否存在并包含 Modal 端点：

```bash
cat ~/.openclaw/workspace/claude-code-video-toolkit/.env | grep MODAL
```

如果 Modal 端点已配置，你就准备好了。如果没有，**要求用户提供 Modal 端点 URL** 或设置 Modal：

```bash
pip3 install --break-system-packages modal
python3 -m modal setup   # 打开浏览器进行认证

# 部署每个工具 — 从输出中捕获端点 URL
cd ~/.openclaw/workspace/claude-code-video-toolkit
modal deploy docker/modal-qwen3-tts/app.py
modal deploy docker/modal-flux2/app.py
modal deploy docker/modal-music-gen/app.py
modal deploy docker/modal-sadtalker/app.py
modal deploy docker/modal-image-edit/app.py
modal deploy docker/modal-upscale/app.py
modal deploy docker/modal-propainter/app.py
modal deploy docker/modal-ltx2/app.py      # 需要：modal secret create huggingface-token HF_TOKEN=hf_...
```

**LTX-2 前提条件：** 在部署 LTX-2 之前，创建 HuggingFace 密钥并接受 [Gemma 3 许可](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized)：
```bash
modal secret create huggingface-token HF_TOKEN=hf_your_read_access_token
```

将每个 URL 添加到 `.env`：
```
MODAL_QWEN3_TTS_ENDPOINT_URL=https://...modal.run
MODAL_FLUX2_ENDPOINT_URL=https://...modal.run
...
```

### 步骤 4：验证和快速测试

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/verify_setup.py
```

所有工具应显示 `[x]`。然后运行快速测试确认 GPU 管线有效：

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/qwen3_tts.py --text "Hello, this is a test." --speaker Ryan --tone warm --output /tmp/video-toolkit-test.mp3 --cloud modal
```

---

## 创建视频

### 步骤 1：创建项目

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
cp -r templates/product-demo projects/PROJECT_NAME
cd projects/PROJECT_NAME
npm install
```

### 步骤 2：编写配置

编辑 `projects/PROJECT_NAME/src/config/demo-config.ts`：

（产品演示配置的完整 TypeScript 接口已保留）

场景类型：`title`、`problem`、`solution`、`demo`、`feature`、`stats`、`cta`。

### 步骤 3：编写配音脚本

创建 `projects/PROJECT_NAME/VOICEOVER-SCRIPT.md`。

### 步骤 4：生成资产

**关键：以下所有命令必须从工具包根目录运行，而非项目目录。**

#### 4a. 背景音乐
#### 4b. 配音（按场景）
#### 4c. 场景图像
#### 4d. 视频片段 — B-Roll 和动画背景（可选）
#### 4e. 虚拟主播解说（可选）
#### 4f. 图像编辑（可选）
#### 4g. 放大（可选）

（所有工具命令和用法与英文版保持一致）

### 步骤 5：同步时间

**在生成配音后始终执行此步骤。** 音频时长与估计值不同。

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
for f in projects/PROJECT_NAME/public/audio/scenes/*.mp3; do
  echo "$(basename $f): $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")s"
done
```

### 步骤 6：审查静止帧
### 步骤 7：渲染

## 合成模式

### 按场景音频、按场景虚拟主播 PiP、转场等完整内容已保留。

## 错误恢复

| 问题 | 解决方案 |
|---------|----------|
| 工具命令失败，报"No module named..." | 从工具包根目录运行 `pip3 install --break-system-packages -r tools/requirements.txt` |
| "MODAL_*_ENDPOINT_URL not configured" | 检查 `.env` 是否有端点 URL。运行 `python3 tools/verify_setup.py` |
| SadTalker 输出为方形/裁剪 | 你忘了 `--preprocess full`。用该标志重新运行 |
| 音频对场景来说太短/太长 | 重新运行步骤 5（同步时间）并更新配置 |
| `npm run render` 失败 | 确保你在项目目录中，而非工具包根目录。先运行 `npm install` |
| Remotion 中"Cannot find module" | 检查导入路径。自定义组件使用 `../../../lib/` 相对路径 |
| Modal 冷启动超时 | 空闲后的第一次调用需 30-120 秒。重试一次 — 第二次调用使用热 GPU |

## 成本估算（Modal）

（各工具成本表格已保留）

**一个 60 秒视频的总成本：** 约 $1-3，取决于场景和讲解片段数量。

Modal Starter 计划：每月 $30 免费计算。应用空闲时缩放到零。
