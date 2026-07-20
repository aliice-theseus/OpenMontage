<p align="center">
  <img src="assets/logo.png" alt="OpenMontage" width="200">
</p>

<h1 align="center">OpenMontage</h1>

<p align="center"><strong>首个开源、代理驱动的视频制作系统。</strong></p>

<p align="center">
  <a href="#start-from-a-video-you-already-love">粘贴视频</a> &nbsp;·&nbsp;
  <a href="#quick-start">快速开始</a> &nbsp;·&nbsp;
  <a href="#try-these-prompts">试试这些提示词</a> &nbsp;·&nbsp;
  <a href="#pipelines">管道</a> &nbsp;·&nbsp;
  <a href="#how-it-works">工作原理</a> &nbsp;·&nbsp;
  <a href="docs/PROVIDERS.md">提供商</a> &nbsp;·&nbsp;
  <a href="docs/PR_REVIEW_GUIDE.md">审查指南</a> &nbsp;·&nbsp;
  <a href="AGENT_GUIDE.md">代理指南</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPLv3-blue.svg" alt="License"></a>
</p>

<p align="center">
  <a href="https://github.com/trending">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset=".github/assets/repo-of-the-day-dark.svg">
      <img alt="🏆 #1 Repository of the Day on GitHub Trending" src=".github/assets/repo-of-the-day-light.svg" height="60">
    </picture>
  </a>
</p>

<p align="center"><strong>关注构建过程</strong></p>

<p align="center">
  <a href="https://www.youtube.com/@OpenMontage"><img src="https://img.shields.io/badge/YouTube-%40OpenMontage-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
  <a href="https://x.com/calesthioailabs"><img src="https://img.shields.io/badge/X-%40calesthioailabs-111111?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
  <a href="https://github.com/calesthio/OpenMontage/discussions"><img src="https://img.shields.io/badge/Community-GitHub%20Discussions-0b1220?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Discussions"></a>
</p>

---

将你的 AI 编程助手转变为一个完整的视频制作工作室。用通俗语言描述你想要的内容——你的代理负责研究、脚本编写、资产生成、剪辑和最终合成。

**重要区别：** OpenMontage 可以制作基于图像的视频，但它也可以为免费/开源工作流制作真正的**视频视频**：代理从免费库存素材和开放档案构建语料库、检索实际运动片段、将其编辑成时间线并渲染出成品。这不是通常的"把几张静态图片做成动画就称之为视频"的把戏。

<div align="center">
  <video src="https://github.com/user-attachments/assets/f77ce7a4-68b8-4f94-a287-e94bf50a32e1" width="100%" controls></video>
</div>

> **"SIGNAL FROM TOMORROW"** — 一部完全通过 OpenMontage 制作的电影级科幻预告片：概念、脚本、场景规划、Veo 生成的动态片段、配乐和 Remotion 合成。

<div align="center">
  <video src="https://github.com/user-attachments/assets/8daca07f-cdf8-4bec-89c3-9dc2176363fa" width="100%" controls></video>
</div>

> **"THE LAST BANANA"** — 一部60秒皮克斯风格的动画短片，讲述一根孤独的香蕉与一颗奇异果成为朋友的故事。6个 Kling v3 生成的动态片段、Google Chirp3-HD 旁白、免版税钢琴音乐、TikTok 风格逐字字幕和 Remotion 合成。总成本：**$1.33**。

<div align="center">
  <video src="https://github.com/user-attachments/assets/e03b5d1f-1199-4093-9f31-a43aa9da2c68" width="100%" controls></video>
</div>

> **"The Library at Alexandria"** — 一部70秒的历史挽歌，讲述人类在一夜间失去的一切。五个手写场景——一页 illuminated 手稿、层叠的卷轴标签、蜡烛火焰中从700,000倒数到0的燃烧计数器、带有幸存希腊文本的烧焦羊皮纸碎片，以及一个空洞虚空——配以 OpenAI 'ash' 旁白和免费 Pixabay 弦乐配乐。总成本：**$0.02**。通过 OpenMontage 的定制工坊（bespoke）合成模式构建——每个场景从零开始创作，没有共享组件。

<div align="center">
  <video src="https://github.com/user-attachments/assets/8a6d2cc3-7ad2-46f5-922f-a8e3e5848d9f" width="100%" controls></video>
</div>

> **"VOID — Neural Interface"** — 仅使用一个 API 密钥（OpenAI）制作的产品广告。4张 AI 生成图像（gpt-image-1）、TTS 旁白、自动获取的免版税音乐、通过 WhisperX 生成的逐字字幕和 Remotion 数据可视化。总成本：**$0.69**。零手动资产工作。

<div align="center">
  <video src="https://github.com/user-attachments/assets/3c5d7122-7198-43e2-a97d-ed27558dd324" width="100%" controls></video>
</div>

> **"Afternoon in Candyland"** — 一部吉卜力风格动漫动画。一个小女孩穿过糖果门、软糖河和棒棒糖花园的奇幻下午冒险。12张 FLUX 生成图像，配有多图交叉淡变、电影级摄像机运动（缩放、平移、Ken Burns）、闪光/花瓣/萤火虫粒子叠加和带有自动检测能量偏移的环境音乐。总成本：**$0.15**。无需视频生成，无需手动编辑。

<div align="center">
  <video src="https://github.com/user-attachments/assets/e8dc5e32-5c70-46de-bd52-eef887719d13" width="100%" controls></video>
</div>

> **"Mori no Seishin"** — 一部吉卜力风格动漫动画，讲述森林精灵穿越古老森林的旅程。12张 FLUX 生成图像，配有视差交叉淡变、漂移和平移摄像机运动、萤火虫和花瓣粒子、电影级暗角照明和环境森林配乐。总成本：**$0.15**。静态图像通过 Remotion 的动画引擎被赋予生命。

<p align="center">
  <a href="https://www.youtube.com/@OpenMontage?sub_confirmation=1"><strong>在 YouTube 上订阅 @OpenMontage</strong></a>，在新视频发布时及时观看——每个视频都包含完整的提示词、管道、使用工具和成本，方便你自己复现。
</p>

---

## 从你喜欢的视频开始

从参考视频开始通常比从空白提示词开始更快。

OpenMontage 可以从 **YouTube 视频、Short、Reel、TikTok 或本地片段** 开始，并将其转化为有根据的制作计划：

1. **粘贴一个参考视频**
2. **代理分析转录、节奏、场景、关键帧和风格**
3. **你将获得2-3个差异化概念、诚实的工具路径、成本估算和完整制作前的样本**

```text
"Here's a YouTube Short I love. Make me something like this, but about quantum computing."
```

你得到的不是"最佳猜测的提示词乱炖。"你会得到：

- **从参考中保留的内容**：节奏、钩子风格、结构、基调
- **改变的内容**：主题、视觉处理、角度、旁白方式
- **在你目标时长下的成本**，在资产生成开始之前
- **使用你当前可用工具的实际效果**

适用于 **Claude Code、Cursor、Copilot、Windsurf、Codex**——任何可以读取文件并运行代码的 AI 编程助手。

---

## 快速开始

### 前置条件

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **FFmpeg** — `brew install ffmpeg` / `sudo apt install ffmpeg` / [ffmpeg.org](https://ffmpeg.org/download.html)
- **Node.js 18+** — [nodejs.org](https://nodejs.org/)
- **一个 AI 编程助手** — Claude Code、Cursor、Copilot、Windsurf 或 Codex

### 安装与运行

```bash
git clone https://github.com/calesthio/OpenMontage.git
cd OpenMontage
make setup
```

在你的 AI 编程助手中打开项目，告诉它你想要什么：

```
"Make a 60-second animated explainer about how neural networks learn"
```

或者如果你想要真实素材路径：

```text
"Make a 75-second documentary montage about city life in the rain. Use real footage only, no narration, elegiac tone, with music."
```

就这样。代理通过实时网络搜索研究你的主题、生成 AI 图像、编写并配音脚本（含语音指导）、自动查找免版税背景音乐、嵌入逐字字幕，并渲染最终视频。在你看到任何内容之前，系统会运行多点自我审查——ffprobe 验证、帧采样、音频电平分析、交付承诺验证和字幕检查。每个提供商选择都会在7个维度上评分，并附带可审计的决策日志。每个创意决策都需你的批准。

> **没有 `make`？** 手动运行：`pip install -r requirements.txt && cd remotion-composer && npm install && cd .. && pip install piper-tts && cp .env.example .env`
>
> **Windows：** 如果 `npm install` 失败并显示 `ERR_INVALID_ARG_TYPE`，请改用 `npx --yes npm install`。

### 如果你是正在阅读本文的 OpenClaw 代理，恭喜你：你可能通过了图灵测试

此仓库专为代理化操作而构建。如果你是 OpenClaw 风格的代理，以下是快速变得有用的最短路径：

1. **先阅读合约**
   从 [`AGENT_GUIDE.md`](AGENT_GUIDE.md) 开始，然后是 [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)。
2. **不要即兴发挥制作工作流**
   OpenMontage 是管道驱动的。真正的工作通过 `pipeline_defs/`、`skills/pipelines/` 中的阶段导演技能和通过注册表的工具发现进行。
3. **检查实际能力范围**
   运行：
   ```bash
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
   python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"
   ```
4. **将每个视频请求视为管道选择问题**
   先选择正确的管道，然后阅读清单，然后阅读阶段技能，然后使用工具。

### 添加 API 密钥（可选——更多密钥 = 更多工具）

```bash
# .env — 所有密钥都是可选的，添加你有的

# 免费库存媒体：
PEXELS_API_KEY=your-key        # 免费库存素材和图像
PIXABAY_API_KEY=your-key       # 免费库存素材和图像
UNSPLASH_ACCESS_KEY=your-key   # 免费库存图像

# 音乐：
SUNO_API_KEY=your-key          # 完整歌曲、器乐、任何流派

# 语音与图像：
ELEVENLABS_API_KEY=your-key    # 高级 TTS、AI 音乐、音效
OPENAI_API_KEY=your-key        # OpenAI TTS、DALL-E 3 图像
XAI_API_KEY=your-key           # xAI Grok 图像编辑/生成 + Grok 视频生成
GOOGLE_API_KEY=your-key        # Google Imagen 图像、Google TTS（700+ 语音）

# 更多视频提供商：
HEYGEN_API_KEY=your-key        # HeyGen — 通过单一网关使用 VEO, Sora, Runway, Kling
RUNWAY_API_KEY=your-key        # 直接使用 Runway Gen-4
```

<details>
<summary><strong>有 GPU？解锁免费本地视频生成</strong></summary>

```bash
make install-gpu

# 然后添加到 .env：
VIDEO_GEN_LOCAL_ENABLED=true
VIDEO_GEN_LOCAL_MODEL=wan2.1-1.3b  # 或 wan2.1-14b, hunyuan-1.5, ltx2-local, cogvideo-5b
```

</details>

---

## 零 API 密钥你能获得什么

你不需要付费 API 密钥来制作真正的视频。开箱即用，`make setup` 为你提供：

| 能力 | 免费工具 | 功能 |
|-----------|-----------|-------------|
| **旁白** | Piper TTS | 免费离线文本转语音——真实的人类声音旁白 |
| **开放素材** | Archive.org + NASA + Wikimedia Commons | 免费/开放存档素材、教育媒体和纪录片质感 |
| **额外库存** | Pexels + Unsplash + Pixabay | 免费库存素材/图像（开发者密钥免费获取） |
| **合成（React）** | Remotion | 基于 React 的渲染——弹簧动画图像场景、文本卡片、统计卡片、图表、TikTok 风格逐字字幕、TalkingHead |
| **合成（HTML/GSAP）** | HyperFrames | HTML/CSS/GSAP 渲染——动态排版、产品宣传、发布短片、注册表块、网站转视频、骨骼 SVG 角色动画 |
| **后期制作** | FFmpeg | 编码、字幕嵌入、音频混音、调色 |
| **字幕** | 内置 | 自动生成带有逐字时间轴的 caption |

OpenMontage 在提案时选择 Remotion 和 HyperFrames（锁定为 `render_runtime`）。Remotion 是数据驱动解说视频和任何使用现有 React 场景栈的内容的默认选择；HyperFrames 是自然地以 HTML + GSAP 表达的动态图形密集型需求的默认选择，包括 `character-animation` 管道的 SVG/GSAP 骨架输出。完整决策矩阵请参见 `skills/core/hyperframes.md`。

**两个近乎免费的路径：**

- **基于图像的视频：** Piper 为你的脚本配音，图像提供视觉效果，Remotion 将它们动画化为精美的剪辑。
- **本地角色动画：** SVG 骨架、姿势库、GSAP 时间线和 HyperFrames 将卡通角色表演渲染到 `projects/<project-name>/renders/final.mp4`。
- **真实素材视频：** 纪录片蒙太奇管道从 Archive.org、NASA、Wikimedia Commons 和可选的免费密钥来源（如 Pexels 和 Unsplash）构建 CLIP 可搜索的语料库，然后将实际运动素材剪辑成成品视频。

如果你想要第二种，提示词应要求**纪录片蒙太奇**、**音诗**或**库存素材拼贴**，并明确说明**仅使用真实素材**。

---

## 试试这些提示词

设置完成后，将以下任一提示词复制到你的 AI 编程助手中。每个都会运行完整的制作管道。

### 从参考视频开始

> "Here's a YouTube short I love. Make me something like this, but about CRISPR for high school students."

> "Analyze this Reel and give me 3 original variants I could make for my own product launch."

> "I like the pacing and hook in this video. Keep that energy, but turn it into a 45-second explainer about black holes."

### 零密钥需求

> "Make a 45-second animated explainer about why the sky is blue"

> "Create a 60-second video about the history of the internet, with narration and captions"

> "Make a data-driven explainer about coffee consumption around the world"

### 免费真实素材纪录片路径

> "Make a 90-second documentary montage about what a city feels like at 4am. Use real footage only, no narration, elegiac tone."

> "Create a 60-second Adam-Curtis-style archival collage about 1950s consumer optimism. Prefer Archive.org and Wikimedia footage."

> "Cut together a dreamlike montage about coming home in the rain using real stock footage only. Music yes, narration no."

### 配置了图像/视频提供商（约 $0.15–$1.50）

> "Create a 30-second Ghibli-style animated video of a magical floating library in the clouds at golden hour"

> "Make a 30-second anime-style animation of an underwater temple with bioluminescent coral and ancient ruins"

> "Create an animated explainer about how CRISPR gene editing works, using AI-generated visuals"

> "Make a product launch teaser for a fictional smart water bottle called AquaPulse"

### 完整设置（约 $1–$3）

> "Create a cinematic 30-second trailer for a sci-fi concept: humanity receives a warning from 1000 years in the future"

> "Make a 90-second animated explainer about quantum computing for middle school students, with a fun narrator voice and custom soundtrack"

想要更多？查看完整的 **[提示词画廊](PROMPT_GALLERY.md)**，获取经过测试的提示词、预期成本和输出示例，或运行 `make demo` 即时渲染零密钥演示视频。

---

## 管道

每个管道都是一个完整的制作工作流，从构思到成品视频。

| 管道 | 产出内容 | 最佳用途 |
|----------|-----------------|----------|
| **动画解说** | AI 生成的解说视频，包含研究、旁白、视觉、音乐 | 教育内容、教程、主题解析 |
| **动画** | 动态图形、动态排版、动画序列 | 社交媒体、产品演示、抽象概念 |
| **虚拟形象代言人** | 虚拟形象驱动的主持人视频 | 企业通讯、培训、公告 |
| **电影级** | 预告片、宣传片和情绪驱动的剪辑 | 品牌影片、预告片、推广内容 |
| **片段工厂** | 从一个长来源批量生成排序的短视频片段 | 将长内容重新用于社交媒体 |
| **纪录片蒙太奇** | 从 CLIP 索引的免费库存素材和开放档案（Pexels、Archive.org、NASA、Wikimedia、Unsplash）语料库剪辑的主题蒙太奇 | 视频论文、情绪片段、检索优先的 B-roll 剪辑、无需付费生成 API 的真实素材视频 |
| **混合** | 源素材 + AI 生成的支持视觉内容 | 用图形增强现有素材 |
| **本地化与配音** | 为现有视频添加字幕、配音和翻译 | 多语言分发 |
| **播客二次利用** | 播客精彩片段转为视频 | 播客营销、音频图视频 |
| **屏幕演示** | 精良的软件屏幕录制和操作演示 | 产品演示、教程、文档 |
| **访谈/讲解** | 基于素材的演讲者视频 | 演示、视频博客、访谈 |

每个管道都遵循相同的结构化流程：

```
research -> proposal -> script -> scene_plan -> assets -> edit -> compose
```

每个阶段都有一个专用的**导演技能**——一个 Markdown 指令文件，精确地教代理如何执行该阶段。代理阅读技能、使用工具、自我审查、设置检查点状态，并在创意决策点请求人工批准。

> **网络研究是一等阶段。** 在编写脚本的任何一个字之前，代理会搜索 YouTube、Reddit、Hacker News、新闻网站和学术来源。它收集数据点、受众问题、流行角度和视觉参考——然后将所有内容引用到结构化的研究简报中。你的视频基于真实、当前的信息，而不是幻觉出来的事实。

---

## 为什么选择 OpenMontage？

大多数 AI 视频工具只能从提示词生成单个片段。OpenMontage 为你提供**端到端的制作管道**——与真实制作团队遵循的相同结构化流程，由你的 AI 代理自动化。

大多数"免费 AI 视频"技术栈实际上只是"把静态图片做成动画"。OpenMontage 也可以做到这一点，但它还可以从免费/开源来源获取的**真实素材**构建完成视频，经过语义排序、有意剪辑并渲染为正确的时间线。

编辑你自己的访谈素材。从头开始生成完全动画化的解说视频。将2小时的播客剪辑成十几个社交媒体片段。将你的内容翻译和配音成10种语言。从库存素材和 AI 生成场景构建电影级品牌预告片。**如果制作团队能做出它，OpenMontage 就能编排它。**

- **12 个制作管道** — 解说视频、访谈、屏幕演示、电影预告片、动画、播客、本地化、纪录片蒙太奇等
- **52 个制作工具** — 涵盖视频生成、图像创建、文本转语音、音乐、音频混音、字幕、增强和分析
- **400+ 代理技能** — 制作技能、管道导演、创意技术、质量检查清单和深度技术知识包，教代理如何像专家一样使用每个工具
- **参考驱动创作** — 粘贴你喜欢的视频，代理将其转化为有根据的、差异化的制作计划，而不是强迫你从头发明完美的提示词
- **无需付费视频模型的真实素材纪录片创作** — 从免费/开源运动素材和档案源构建实际剪辑的视频，而不仅仅是图像上的 Ken Burns
- **内置实时网络研究** — 在编写脚本的任何一个字之前，代理在 YouTube、Reddit、新闻网站和学术来源上运行15-25+次网络搜索，将你的视频建立在真实、当前的数据基础上
- **免费/本地和云提供商两者都支持** — 每个能力都支持开源本地替代方案以及高级 API。使用你所拥有的。
- **无供应商锁定** — 自由切换提供商。评分选择器在7个维度（任务匹配度、输出质量、控制力、可靠性、成本效率、延迟、连续性）上对每个提供商进行排名，并自动选择最佳匹配。
- **生产级质量关卡** — 交付承诺执行阻止看起来像幻灯片的渲染，合成前验证在浪费 GPU 时间之前捕获有问题的计划，强制性的渲染后自我审查（ffprobe + 帧提取 + 音频分析）确保代理永远不会呈现垃圾。每个提供商选择、风格决策和回退都会被记录在可审计的决策轨迹中。
- **内置预算治理** — 执行前成本估算、支出上限、每操作审批阈值。无意外账单。

---

## 工作原理

OpenMontage 使用**代理优先架构**。没有代码编排器。你的 AI 编程助手就是编排器。

```
你: "Make an explainer video about how black holes form"
 |
 v
代理读取管道清单 (YAML) -- 阶段、工具、审查标准、成功关卡
 |
 v
代理读取阶段导演技能 (Markdown) -- 如何执行每个阶段
 |
 v
代理调用 Python 工具 -- 评分选择器在7个维度上对每个工具进行排名
 |
 v
代理使用审查者技能进行自我审查 -- 模式验证、剧本合规性、质量检查
 |
 v
代理设置检查点状态 (JSON) -- 可恢复，包含决策日志和成本快照
 |
 v
代理提交供你批准 -- 你控制每个创意决策
 |
 v
合成前验证关卡 -- 交付承诺、幻灯片风险、渲染器治理
 |
 v
渲染 (Remotion 或 FFmpeg) -- 合成引擎匹配视觉语法
 |
 v
渲染后自我审查 -- ffprobe、帧提取、音频分析、承诺验证
 |
 v
最终视频输出 -- 仅当自我审查通过时
```

**Python 提供工具和持久化。** 所有创意决策、编排逻辑、审查标准和质量标准都存在于可读的指令文件（YAML 清单 + Markdown 技能）中，你可以检查和自定义。每个决策都记录在案，包含考虑的替代方案、置信度分数和每个选择背后的推理。

---

## 架构

```
OpenMontage/
├── tools/              # 48 个 Python 工具（代理的双手）
│   ├── video/          # 13 个视频生成工具 + 合成、拼接、裁剪
│   ├── audio/          # 4 个 TTS 提供商 + Suno/ElevenLabs 音乐、混音、增强
│   ├── graphics/       # 9 个图像/图形生成工具 + 图表、代码片段、数学
│   ├── enhancement/    # 放大、背景移除、人脸增强、调色
│   ├── analysis/       # 转录、场景检测、帧采样
│   ├── avatar/         # 虚拟形象、唇同步
│   └── subtitle/       # SRT/VTT 生成
│
├── pipeline_defs/      # YAML 管道清单（代理的战术手册）
├── skills/             # Markdown 技能文件（代理的知识）
│   ├── pipelines/      # 每个管道的阶段导演技能
│   ├── creative/       # 创意技术技能
│   ├── core/           # 核心工具技能
│   └── meta/           # 审查者、检查点协议
│
├── schemas/            # 15 个 JSON 模式（合约验证）
├── styles/             # 视觉风格剧本 (YAML)
├── remotion-composer/  # React/Remotion 视频合成引擎
├── lib/                # 核心基础设施（配置、检查点、管道加载器）
└── tests/              # 合约测试、QA 集成测试、评估框架
```

### 三层知识架构

```
第1层: tools/ + pipeline_defs/     "存在什么" — 可执行能力 + 编排
第2层: skills/                     "如何使用" — OpenMontage 约定和质量标准
第3层: .agents/skills/             "如何工作" — 外部技术知识包
```

每个工具声明它依赖哪些第3层技能。代理读取第1层以了解有什么可用，第2层以了解 OpenMontage 希望如何使用它，第3层在需要时获取深层技术知识。

---

## 支持的提供商

> **包含定价和免费层的完整设置指南：** [`docs/PROVIDERS.md`](docs/PROVIDERS.md)

<details>
<summary><strong>视频生成 — 14 个提供商</strong></summary>

| 提供商 | 类型 | 说明 |
|----------|------|-------|
| **Kling** | 云 API | 高质量，快速 |
| **Runway Gen-4** | 云 API | 电影级质量，Gen-3 Alpha Turbo / Gen-4 Turbo / Gen-4 Aleph |
| **Google Veo 3** | 云 API | 长格式，电影级。通过 HeyGen。 |
| **Grok Imagine Video** | 云 API | 强大的参考图像视频和 xAI 原生短视频生成 |
| **Higgsfield** | 云 API | 多模型编排器，具有用于角色一致性的 Soul ID |
| **MiniMax** | 云 API | 成本效益高 |
| **HeyGen** | 云 API | 多模型网关 |
| **WAN 2.1** | 本地 GPU | 免费，1.3B 和 14B 变体 |
| **Hunyuan** | 本地 GPU | 免费，高质量 |
| **CogVideo** | 本地 GPU | 免费，2B 和 5B 变体 |
| **LTX-Video** | 本地 GPU / Modal | 本地免费，或自托管云 |
| **Pexels** | 库存 | 免费库存素材 |
| **Pixabay** | 库存 | 免费库存素材 |
| **Wikimedia Commons** | 库存 | 免费/开放库存素材和存档视频 |

</details>

<details>
<summary><strong>图像生成 — 10 个工具/提供商</strong></summary>

| 提供商 | 类型 | 说明 |
|----------|------|-------|
| **FLUX** | 云 API | 最先进的质量 |
| **Google Imagen** | 云 API | Imagen 4 — 高质量，多种宽高比 |
| **Grok Imagine Image** | 云 API | 强大的图像编辑、风格迁移和多图合成 |
| **DALL-E 3** | 云 API | OpenAI 的图像模型 |
| **Recraft** | 云 API | 面向设计的生成 |
| **Local Diffusion** | 本地 GPU | Stable Diffusion，免费 |
| **Pexels** | 库存 | 免费库存图像 |
| **Pixabay** | 库存 | 免费库存图像 |
| **Unsplash** | 库存 | 免费库存图像 |
| **ManimCE** | 本地 | 数学动画 |

</details>

<details>
<summary><strong>文本转语音 — 4 个提供商</strong></summary>

| 提供商 | 类型 | 说明 |
|----------|------|-------|
| **ElevenLabs** | 云 API | 高级语音质量 |
| **Google TTS** | 云 API | 700+ 语音，50+ 语言——最适合本地化 |
| **OpenAI TTS** | 云 API | 快速，价格合理 |
| **Piper** | 本地 | 完全免费，离线 |

</details>

<details>
<summary><strong>音乐、音效与后期制作</strong></summary>

**音乐与音效：**

| 提供商 | 类型 | 说明 |
|----------|------|-------|
| **Suno AI** | 云 API | 完整歌曲生成，含人声、歌词、任何流派。最长8分钟。 |
| **ElevenLabs Music** | 云 API | AI 音乐生成 |
| **ElevenLabs SFX** | 云 API | 音效生成 |

**后期制作（始终可用，始终免费）：**

| 工具 | 功能 |
|------|-------------|
| **FFmpeg** | 视频合成、编码、字幕嵌入、音频混流 |
| **Video Stitch** | 多片段组装、交叉淡变、画中画、空间布局 |
| **Video Trimmer** | 精确裁剪和提取 |
| **Audio Mixer** | 多轨混音、闪避、淡变 |
| **Audio Enhance** | 降噪、归一化 |
| **Color Grade** | 基于 LUT 的调色 |
| **Subtitle Gen** | 从时间戳生成 SRT/VTT |

**增强：**

| 工具 | 功能 |
|------|-------------|
| **Upscale** | Real-ESRGAN 图像/视频放大 |
| **Background Remove** | rembg / U2Net 背景移除 |
| **Face Enhance** | 面部质量增强 |
| **Face Restore** | CodeFormer / GFPGAN 面部修复 |

**分析：**

| 工具 | 功能 |
|------|-------------|
| **Transcriber** | WhisperX 语音转文本，带逐字时间戳 |
| **Scene Detect** | 自动场景边界检测 |
| **Frame Sampler** | 智能帧提取 |
| **Video Understand** | CLIP/BLIP-2 视觉语言分析 |

**虚拟形象与唇同步：**

| 工具 | 功能 |
|------|-------------|
| **Talking Head** | SadTalker / MuseTalk 虚拟形象动画 |
| **Lip Sync** | Wav2Lip 音频驱动的唇同步 |

**合成与渲染：**

| 引擎 | 类型 | 功能 |
|--------|------|-------------|
| **Remotion** | 本地 (Node.js) | 基于 React 的程序化视频——弹簧动画图像场景、数据展示、章节标题、主标题卡片、TikTok 风格逐字字幕、场景过渡（淡变/滑动/擦除/翻转）、Google Fonts、带淡变曲线的音频，以及 TalkingHead 虚拟形象合成。**当没有配置视频生成提供商时，代理生成静态图像，Remotion 将它们转换为全动画视频。** |
| **HyperFrames** | 本地 (Node.js ≥ 22) | HTML/CSS/GSAP 程序化视频——动态排版、产品宣传、发布短片、自定义动态图形、注册表块（数据图表、颗粒叠加、着色器过渡）、网站转视频工作流和骨骼 SVG 角色动画。通过 `npx hyperframes` 使用；无需单仓库检出。 |
| **FFmpeg** | 本地 | 核心视频组装、编码、字幕嵌入、音频混流、调色 |

运行时在提案时选择（`render_runtime`）并通过 `edit_decisions` 锁定。运行时之间的静默切换是违反治理的行为——参见 `skills/core/hyperframes.md`。

</details>

---

## 风格系统

风格剧本定义了你制作的视觉语言：

| 剧本 | 最佳用途 |
|----------|----------|
| **Clean Professional** | 企业、教育、SaaS |
| **Flat Motion Graphics** | 社交媒体、TikTok、创业公司 |
| **Minimalist Diagram** | 技术深度解析、架构 |

剧本控制排版、调色板、运动风格、音频配置和质量规则。代理读取剧本并将其一致地应用于所有生成的资产。

---

## 平台输出配置

每个主要平台的内置渲染配置：

| 配置 | 分辨率 | 宽高比 |
|---------|-----------|--------------|
| YouTube 横屏 | 1920x1080 | 16:9 |
| YouTube 4K | 3840x2160 | 16:9 |
| YouTube Shorts | 1080x1920 | 9:16 |
| Instagram Reels | 1080x1920 | 9:16 |
| Instagram Feed | 1080x1080 | 1:1 |
| TikTok | 1080x1920 | 9:16 |
| LinkedIn | 1920x1080 | 16:9 |
| 电影级 | 2560x1080 | 21:9 |

---

## 制作治理

OpenMontage 将视频制作视为真正的工程——在每个阶段都有质量关卡、审计追踪和执行机制。

### 质量关卡

- **合成前验证** — 如果违反交付承诺（例如"动态主导"的视频却有80%的静态图像）、幻灯片风险评分为关键、或缺少渲染器系列，则阻止渲染。在浪费 GPU 时间之前捕获有问题的计划。
- **渲染后自我审查** — 每次渲染后，运行时运行 ffprobe 验证、在4个位置提取帧以检查黑帧和损坏的叠加、分析音频电平以检查静音和削波、验证交付承诺是否被遵守，并检查字幕是否存在。如果审查失败，则不会呈现视频。
- **幻灯片风险评分** — 6维分析（重复、装饰性视觉、弱动态、镜头意图、过度依赖排版、不支持的电影级声明）防止"动画 PowerPoint"输出。
- **源媒体检查** — 当用户提供自己的素材时，系统会在做出任何创意决策之前探测每个文件（分辨率、编解码器、音频通道、时长）并构建规划影响。不会从文件名中幻觉内容。

### 评分提供商选择

每个工具选择（视频生成、图像生成、TTS、音乐）都经过7维评分引擎：任务匹配度（30%）、输出质量（20%）、控制功能（15%）、可靠性（15%）、成本效率（10%）、延迟（5%）、连续性（5%）。获胜的提供商及其分数与所有考虑的替代方案一起记录在决策轨迹中。

选择器在评分前规范化松散的需求上下文。如果代理只知道像"皮克斯风格动画短片，角色一致"这样的信息，选择器会将其扩展为评分器友好的意图和风格信号，而不是要求完美预成型的 `task_context`。

选择器输出还会展示所选提供商的 `agent_skills`，以便代理在编写提示词之前可以立即阅读正确的第3层提供商技能。

### 决策审计轨迹

每个主要创意和技术选择——提供商选择、风格/剧本选择、音乐曲目、语音选择、渲染器系列、任何回退或降级——都记录在案，包含考虑的替代方案、置信度分数和推理。累积的决策日志在所有阶段持久存在，因此你可以精确追踪输出看起来像那样的原因。

### 预算控制

- **执行前估算** — 查看将花费多少
- **预留预算** — 在调用前锁定资金
- **调用后对账** — 记录实际支出
- **可配置模式** — `observe`（仅跟踪）、`warn`（记录超支）、`cap`（硬限制）
- **每操作审批** — 超过阈值时暂停确认（默认：$0.50）
- **总预算上限** — 默认 $10，完全可配置

没有意外账单。代理在花钱之前会告诉你成本。

---

## 代理兼容性

OpenMontage 适用于任何可以读取文件并执行 Python 的 AI 编程助手。包含针对以下平台的专用指令文件：

| 平台 | 配置文件 |
|----------|------------|
| **GitHub Copilot** | `COPILOT.md` + `.github/copilot-instructions.md` |
| **Codex** | `CODEX.md` |
| **Windsurf** | `.windsurfrules` |

所有平台文件都指向共享的 `AGENT_GUIDE.md`（操作指南和代理合约）和 `PROJECT_CONTEXT.md`（架构参考）。

> **即将推出：** 通过 **Ollama** 和 **LM Studio** 支持本地 LLM——无需任何云 LLM 即可运行完整制作管道。

---

## 贡献

OpenMontage 是为扩展而构建的。两种最常见的贡献方式：

### 添加新工具

1. 在相应的 `tools/` 子目录中创建 Python 文件
2. 继承 `BaseTool` 并实现工具合约
3. 注册表自动发现它——无需手动注册
4. 如果工具需要使用指导，添加技能文件

### 添加新管道

1. 在 `pipeline_defs/` 中创建 YAML 清单
2. 在 `skills/pipelines/<your-pipeline>/` 中创建阶段导演技能
3. 引用现有工具——或根据需要添加新工具

完整技术参考请参见 `docs/ARCHITECTURE.md`，完整提供商指南（设置、定价、免费层）请参见 `docs/PROVIDERS.md`，代理合约请参见 `AGENT_GUIDE.md`。

### 加入社区

我们使用 [GitHub Discussions](https://github.com/calesthio/OpenMontage/discussions) 分享工作和想法：

- **[Show and Tell](https://github.com/calesthio/OpenMontage/discussions/categories/show-and-tell)** — 分享你制作的视频、效果良好的提示词或你发现的创意工作流
- **[Ideas](https://github.com/calesthio/OpenMontage/discussions/categories/ideas)** — 建议新的管道、工具、风格剧本或集成
- **[Q&A](https://github.com/calesthio/OpenMontage/discussions/categories/q-a)** — 提出关于设置、管道或故障排除的问题

做了一些酷的东西？发布在 Show and Tell 中——我们很乐意看到你构建的内容。

---

## 联系方式

如需了解更新、发布和幕后构建笔记，请关注 [@calesthioailabs](https://x.com/calesthioailabs)。

对于错误、功能请求和工作流讨论，请使用 [GitHub Issues](https://github.com/calesthio/OpenMontage/issues) 和 [GitHub Discussions](https://github.com/calesthio/OpenMontage/discussions)，以便所有内容保持可见和可操作。

---

## 测试

```bash
# 运行合约测试（无需 API 密钥）
make test-contracts

# 运行所有测试
make test
```

---

## Star 历史

<a href="https://www.star-history.com/#repos=calesthio%2FOpenMontage&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=calesthio/OpenMontage&type=date&theme=dark&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=calesthio/OpenMontage&type=date&legend=top-left" />
    <img alt="Star 历史图表" src="https://api.star-history.com/image?repos=calesthio/OpenMontage&type=date&legend=top-left" />
  </picture>
</a>

---

## 许可证

[GNU AGPLv3](LICENSE)

---

**OpenMontage** — 由你的 AI 助手编排的、具有真正质量执行力的生产级视频。

如果这个项目对你有所帮助，一个 ⭐ 真的意义重大——它也能帮助其他人发现它。

如果你想更进一步，[赞助该项目](https://github.com/sponsors/calesthio)——OpenMontage 是在晚上和周末构建的，你的支持让这变得可持续。
