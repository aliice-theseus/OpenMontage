# OpenMontage 架构

> 最后更新：2026-03-28 | 源自代码探索，非先前文档。

OpenMontage 是一个**代理编排的视频制作平台**。LLM 编码助手（Claude Code、Cursor、Copilot 等）充当编排者——读取流水线清单、遵循技能说明、调用 Python 工具以及记录检查点状态。没有运行时的 Python 编排器；代理本身就是控制平面。

---

## 高层流程

```
用户提供主题/想法
        |
        v
代理读取流水线清单（YAML）
        |
        v
对于每个阶段：
   1. 代理读取阶段导演技能（Markdown）
   2. 代理通过工具注册表调用 Python 工具
   3. 代理写入带有工件的检查点（JSON）
   4. 代理使用元/审查者技能进行自我审查
   5. 人工审批关卡（如已配置）
        |
        v
最终视频输出
```

---

## 仓库布局

```
OpenMontage/
├── lib/                    # 核心运行时基础设施（Python）
│   ├── config_model.py     # Pydantic 配置：LLM、预算、检查点、输出、路径
│   ├── checkpoint.py       # 流水线状态持久化和阶段转换
│   ├── pipeline_loader.py  # YAML 清单加载和验证
│   ├── media_profiles.py   # 平台特定的渲染配置（YouTube、TikTok 等）
│   ├── env_loader.py       # .env 变量管理
│   └── providers/          # （为未来提供商抽象保留）
│
├── tools/                  # 57+ 个 Python 工具实现
│   ├── base_tool.py        # 抽象基类——工具契约
│   ├── tool_registry.py    # 自动发现的单例注册表
│   ├── cost_tracker.py     # 预算治理（估算 → 预留 → 对账）
│   ├── analysis/           # 转录、场景检测、帧采样、视频理解
│   ├── audio/              # TTS（ElevenLabs、OpenAI、Piper）、音乐生成、混音、增强
│   ├── avatar/             # 虚拟形象动画、唇形同步
│   ├── enhancement/        # 放大、背景移除、人脸增强/修复、调色
│   ├── graphics/           # 图像生成（FLUX、DALL-E、Recraft、本地扩散）、素材库、图表、代码片段、数学动画
│   ├── publishers/         # （保留）
│   ├── subtitle/           # 从时间戳生成 SRT/VTT
│   └── video/              # 13 个视频生成提供商、合成、拼接、裁剪
│
├── pipeline_defs/          # YAML 流水线清单
├── schemas/                # 用于验证的 JSON Schema 定义
│   ├── artifacts/          # 11 个工件模式（brief → publish_log）
│   ├── checkpoints/        # 检查点状态模式
│   ├── pipelines/          # 流水线清单模式
│   ├── styles/             # 风格剧本书模式
│   └── tools/              # 工具特定模式
│
├── skills/                 # 第 2 层：OpenMontage 特定的代理说明
│   ├── core/               # FFmpeg、Remotion、WhisperX、调色技能
│   ├── creative/           # 视频剪辑、增强、数据可视化、提示工程
│   ├── meta/               # 审查者、检查点协议、技能创建者
│   └── pipelines/          # 按流水线划分的阶段导演技能
│
├── .agents/skills/         # 第 3 层：外部技术技能（FFmpeg、HyperFrames、GSAP 等）
├── styles/                 # 视觉风格剧本书（YAML）+ 加载器
├── remotion-composer/      # Node.js/React——Remotion 视频合成渲染器
├── tests/                  # 契约测试、QA 集成测试、评估框架
├── docs/                   # 最佳实践指南、会话交接、审计
└── config.yaml             # 全局运行时配置
```

---

## 核心架构原则

### 1. 代理优先编排

**没有 Python 编排器**。LLM 代理：
- 读取流水线清单以了解阶段顺序
- 读取每个阶段导演技能的详细说明
- 调用工具、评估结果、做出创意决策
- 写入检查点以在阶段之间持久化状态

Python 仅提供**工具和持久化**。所有智能都在技能说明（Markdown）和流水线清单（YAML）中。

### 2. 运行时无 LLM API 密钥

OpenMontage 在运行时不会调用 LLM API。在用户 IDE 中运行的编码助手_就是_LLM。需要生成能力（图像、视频、TTS）的工具直接调用领域特定 API（ElevenLabs、HeyGen 等），而不是通用 LLM 端点。

### 3. 双提供商支持

每个能力必须同时支持**API 提供商**（云端，付费）和**本地/开源替代方案**（免费，需 GPU）。选择器模式通过路由到任何可用的方式强制执行此规则。

---

## 工具系统

### BaseTool 契约

所有工具都继承自 `BaseTool`（ABC）并声明：

| 字段 | 用途 |
|------|------|
| `name`, `version` | 身份标识 |
| `tier` | CORE、VOICE、ENHANCE、GENERATE、SOURCE、ANALYZE、PUBLISH |
| `capability` | 功能描述（例如 `tts`、`image_generation`、`video_post`） |
| `provider` | 服务提供商（例如 `elevenlabs`、`ffmpeg`、`selector`） |
| `runtime` | LOCAL、LOCAL_GPU、API、HYBRID |
| `stability` | EXPERIMENTAL、BETA、PRODUCTION |
| `dependencies` | 必需的二进制文件（`cmd:ffmpeg`）、环境变量（`env:ELEVENLABS_API_KEY`）、Python 包（`python:torch`） |
| `input_schema`, `output_schema` | 输入/输出的 JSON Schema |
| `fallback_tools` | 有序的回退链 |
| `agent_skills` | 链接到第 3 层知识技能 |
| `resource_profile` | CPU、RAM、VRAM、磁盘、网络要求 |
| `retry_policy` | 最大重试次数、退避策略 |

**必需方法：** `execute(inputs) -> ToolResult`

`ToolResult` 包含：`success`、`data`、`artifacts`（文件路径）、`error`、`cost_usd`、`duration_seconds`、`seed`、`model`。

### 工具注册表

`ToolRegistry` 是一个单例，通过 `pkgutil.walk_packages()` 自动发现所有 `BaseTool` 子类。无需手动注册。

关键查询：
- `get_by_capability("tts")`——所有 TTS 工具
- `get_by_provider("elevenlabs")`——所有 ElevenLabs 工具
- `get_available()`——依赖满足的工具
- `find_fallback("elevenlabs_tts")`——解析回退链
- `support_envelope()`——供代理使用的完整能力报告
- `gpu_required_tools()`、`network_required_tools()`

### 选择器模式

三个选择器工具抽象了多提供商能力：

| 选择器 | 能力 | 选择方式 |
|--------|------|---------|
| `tts_selector` | 文本转语音 | 根据任务匹配度、质量、控制力、可靠性、成本、延迟和连续性对发现的提供商进行排名 |
| `image_selector` | 图像生成 | 从实时注册表对发现的提供商进行排名；无硬编码的提供商顺序 |
| `video_selector` | 视频生成 | 从实时注册表对发现的提供商进行排名；显式提供时尊重用户偏好 |

选择器基于：用户偏好（显式设置时），然后根据可用提供商的评分排名进行路由。它们透明地在提供商之间适配输入模式。

### 按类别划分的工具清单

**分析（4 个）：** transcriber（WhisperX）、scene_detect、frame_sampler、video_understand（CLIP/BLIP-2）

**音频（8 个）：** elevenlabs_tts、google_tts、openai_tts、piper_tts、tts_selector、music_gen、audio_mixer、audio_enhance

**虚拟形象（2 个）：** talking_head（SadTalker/MuseTalk）、lip_sync（Wav2Lip）

**增强（5 个）：** upscale（Real-ESRGAN）、bg_remove（rembg/U2Net）、face_enhance、face_restore（CodeFormer/GFPGAN）、color_grade（FFmpeg LUTs）

**图形（11 个）：** grok_image、google_imagen、openai_image、local_diffusion、pexels_image、pixabay_image、image_selector、code_snippet、diagram_gen、math_animate（ManimCE）、image_gen（已弃用）

**字幕（1 个）：** subtitle_gen

**视频（15 个）：** grok_video、heygen_video、higgsfield_video、runway_video、wan_video、hunyuan_video、cogvideo_video、ltx_video_local、ltx_video_modal、pexels_video、pixabay_video、video_selector、video_compose（FFmpeg）、video_stitch、video_trimmer

---

## 流水线系统

### 流水线清单

每个流水线是 `pipeline_defs/` 中的一个 YAML 文件，定义：

```yaml
name: animated-explainer
version: "2.0"
category: generated          # talking_head | generated | hybrid | screen_recording | animation | cinematic | custom
default_checkpoint_policy: guided

orchestration:
  mode: executive-producer
  skill: pipelines/explainer/executive-producer
  budget_default_usd: 2.00
  max_revisions_per_stage: 3

compatible_playbooks:
  - clean-professional
  - flat-motion-graphics

stages:
  - name: research
    skill: pipelines/explainer/research-director
    produces: [research_brief]
    tools_available: []
    checkpoint_required: false
    human_approval_default: false
    review_focus: [...]
    success_criteria: [...]
  # ... 直到 publish
```

### 可用流水线

| 流水线 | 类别 | 描述 |
|--------|------|------|
| `animated-explainer` | generated | AI 制作的讲解视频，含研究、旁白、视觉、音乐 |
| `animation` | animation | 运动图形、动态文字 |
| `avatar-spokesperson` | talking_head | 虚拟形象驱动的演讲者视频 |
| `character-animation` | animation | 带 SVG 骨骼、姿势库、GSAP 时间线和 HyperFrames 渲染的本地绑定卡通角色 |
| `cinematic` | cinematic | 预告片、宣传片、情绪驱动的剪辑 |
| `clip-factory` | custom | 从长源批量生成短视频片段 |
| `hybrid` | hybrid | 源素材 + AI 生成的辅助视觉 |
| `localization-dub` | custom | 对现有视频进行字幕、配音和翻译 |
| `podcast-repurpose` | hybrid | 播客精彩片段转视频 |
| `screen-demo` | screen_recording | 软件屏幕录制和操作演示 |
| `talking-head` | talking_head | 素材主导的演讲者视频 |
| `framework-smoke` | custom | 用于框架验证的最小冒烟测试 |

### 标准阶段推进

大多数制作流水线遵循标准的 8 阶段流程：

```
research → proposal → script → scene_plan → assets → edit → compose → publish
```

每个阶段：
1. 有一个**阶段导演技能**（供代理使用的 Markdown 说明）
2. 声明 **tools_available**（代理可以调用哪些工具）
3. **产生**一个或多个规范工件
4. 有 **review_focus** 标准和 **success_criteria**
5. 可以在继续之前要求**人工审批**

专门的流水线可能会插入领域特定的阶段。例如，`character-animation` 在 `scene_plan` 之前添加了 `character_design` 和 `rig_plan`，然后在 `projects/<project-name>/renders/final.mp4` 输出 HyperFrames 工作区和最终交付物。

---

## 检查点系统

检查点将流水线状态作为 JSON 持久化在项目的 `pipeline/` 目录中。

```json
{
  "version": "1.0",
  "project_id": "my-video",
  "stage": "script",
  "status": "completed",
  "timestamp": "2026-03-28T10:00:00Z",
  "checkpoint_policy": "guided",
  "human_approval_required": false,
  "human_approved": true,
  "artifacts": { "script": { ... } },
  "review": { ... },
  "cost_snapshot": { ... }
}
```

**状态值：** `pending` | `in_progress` | `awaiting_human` | `completed` | `failed`

**检查点策略：**
- `guided`——在关键创意阶段设置检查点，机械阶段自动推进
- `manual_all`——每个阶段都需要人工审批
- `auto_noncreative`——除非阶段是创意性的（资源、剪辑），否则自动推进

**函数：** `write_checkpoint()`、`read_checkpoint()`、`get_latest_checkpoint()`、`get_completed_stages()`、`get_next_stage()`

### 规范工件（11 种类型，全部经过 JSON Schema 验证）

| 工件 | 阶段 | 包含内容 |
|------|------|---------|
| `research_brief` | research | 领域分析、数据点、受众洞察、角度 |
| `proposal_packet` | proposal | 概念选项、制作计划、成本估算、审批关卡 |
| `brief` | idea | 标题、钩子、关键点、语调、风格、平台、时长 |
| `script` | script | 带增强提示、发音指南的时间戳段落 |
| `scene_plan` | scene_plan | 带类型、描述、时长的场景定义 |
| `asset_manifest` | assets | 生成的资源，含路径、来源工具、场景关联 |
| `edit_decisions` | edit | 带有入/出时点的剪辑决策 |
| `render_report` | compose | 输出元数据（格式、分辨率、时长） |
| `publish_log` | publish | 平台发布条目，含状态 |
| `review` | （任意） | 审查者反馈和批准记录 |
| `cost_log` | （任意） | 预算跟踪条目 |

---

## 预算治理

`CostTracker` 在整个流水线中执行支出控制。

### 生命周期

```
estimate(tool, operation, $) → entry_id
        |
reserve(entry_id)          # 锁定预算
        |
reconcile(entry_id, $)     # 记录实际支出
```

### 预算模式

| 模式 | 行为 |
|------|------|
| `observe` | 跟踪成本，不强制执行 |
| `warn` | 超支时记录警告，允许执行 |
| `cap` | 拒绝超过剩余预算的操作 |

### 控制措施
- **总预算**（默认：¥10.00）
- **预留保留**（默认：10%）——作为安全余量保留
- **单次操作审批阈值**（默认：¥0.50）——超过此金额时暂停以获取审批
- **新增付费工具审批**——首次使用任何付费工具需要确认
- 按项目持久化到 `cost_log.json`

---

## 3 层知识架构

```
第 3 层：.agents/skills/          外部技术知识（47 个技能）
         "技术如何工作"                FFmpeg、ElevenLabs API、FLUX、Remotion、Three.js 等
              ^
              | agent_skills[] 引用
              |
第 2 层：skills/                   OpenMontage 约定
         "此项目如何使用该技术"          流水线集成、质量检查清单、工件映射
              ^
              | 阶段技能引用
              |
第 1 层：tools/ + pipeline_defs/   可执行能力 + 编排定义
         "存在什么以及何时使用"         BaseTool 契约、流水线清单
```

每个工具的 `agent_skills[]` 字段将第 1 层链接到第 2 层和第 3 层。例如：
- `video_compose.agent_skills = ["remotion-best-practices", "remotion", "ffmpeg"]`
- `tts_selector.agent_skills = ["text-to-speech", "elevenlabs", "openai-docs"]`

---

## 配置

### config.yaml

```yaml
llm:
  provider: anthropic
  temperature: 0.7
  max_tokens: 4096

budget:
  mode: warn
  total_usd: 10.00
  reserve_pct: 0.10
  single_action_approval_usd: 0.50

checkpoint:
  policy: guided
  storage_dir: pipeline

output:
  default_format: mp4
  default_codec: libx264
  default_audio_codec: aac
  default_resolution: 1920x1080
  default_fps: 30
  default_crf: 23

paths:
  pipeline_dir: pipeline
  library_dir: library
  styles_dir: styles
  skills_dir: skills
  output_dir: output
```

所有配置均通过 `lib/config_model.py` 中的 Pydantic 模型进行验证。

### 环境变量（.env）

| 变量 | 使用者 | 用途 |
|------|--------|------|
| `ELEVENLABS_API_KEY` | elevenlabs_tts, music_gen | TTS、音乐、音效 |
| `OPENAI_API_KEY` | openai_tts, openai_image | TTS 回退、DALL-E 3 |
| `XAI_API_KEY` | grok_image, grok_video | Grok 图像编辑/生成、Grok 视频生成 |

| `HEYGEN_API_KEY` | heygen_video | 多提供商视频生成 |
| `PEXELS_API_KEY` | pexels_image, pexels_video | 素材库媒体 |
| `PIXABAY_API_KEY` | pixabay_image, pixabay_video | 素材库媒体 |
| `GOOGLE_API_KEY` | google_imagen, google_tts | Google Imagen 图像、Google Cloud TTS |
| `RUNWAY_API_KEY` | runway_video | Runway Gen-3/Gen-4 直连 |
| `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` | higgsfield_video | Higgsfield 多模型视频 |
| `MODAL_LTX2_ENDPOINT_URL` | ltx_video_modal | 自托管 LTX-2 |
| `VIDEO_GEN_LOCAL_ENABLED` | 本地视频工具 | 启用本地 GPU 生成 |
| `VIDEO_GEN_LOCAL_MODEL` | wan, hunyuan, ltx, cogvideo | 选择本地模型 |

---

## 视觉风格系统

`styles/` 中的风格剧本书定义了流水线的视觉语言：

- `clean-professional.yaml`——企业级、精致外观
- `flat-motion-graphics.yaml`——现代扁平设计
- `minimalist-diagram.yaml`——技术性、极简图表

由 `styles/playbook_loader.py` 加载。每个流水线在其清单中声明 `compatible_playbooks`。针对 `schemas/styles/playbook.schema.json` 进行验证。

---

## 媒体配置

`lib/media_profiles.py` 中平台特定的渲染配置：

| 配置 | 分辨率 | 宽高比 | 说明 |
|------|--------|--------|------|
| `youtube_landscape` | 1920x1080 | 16:9 | 标准 YouTube |
| `youtube_4k` | 3840x2160 | 16:9 | 4K YouTube |
| `youtube_shorts` | 1080x1920 | 9:16 | 最长 60 秒 |
| `instagram_reels` | 1080x1920 | 9:16 | 最长 90 秒 |
| `instagram_feed` | 1080x1080 | 1:1 | 方形 |
| `tiktok` | 1080x1920 | 9:16 | 竖屏 |
| `linkedin` | 1920x1080 | 16:9 | 横屏 |
| `cinematic` | 2560x1080 | 21:9 | 超宽屏 |

每个配置指定编码、音频编码、CRF、像素格式、最大文件大小、最大时长和字幕格式。`ffmpeg_output_args(profile)` 生成对应的 FFmpeg 标志。

---

## 合成运行时

OpenMontage 拥有多运行时合成层。三个引擎位于 `video_compose` 之后，在提案时选择并在 `edit_decisions.render_runtime` 中锁定：

### Remotion（基于 React）

`remotion-composer/` 中的独立 Node.js/React 子项目，使用 [Remotion](https://www.remotion.dev/)。

- **React 18** + **Remotion 4.0** + **TypeScript 5.3**
- 处理现有的场景组件栈（`text_card`、`stat_card`、图表、字幕、`TalkingHead`、`CinematicRenderer`）
- 脚本：`start`（工作室）、`build`（渲染）、`upgrade`

### HyperFrames（HTML/CSS/GSAP）

通过 `npx hyperframes` 使用（无需检出单体仓库）。运行时要求：Node.js ≥ 22、FFmpeg、`npx`。

- 处理动态文字、产品宣传视频、发布预告片、网站转视频、注册表块和 SVG/GSAP 角色骨骼
- 驱动程序：`tools/video/hyperframes_compose.py` 在 `projects/<name>/hyperframes/` 下实例化工作区，然后运行 `lint → validate → render`
- 第 3 层技能位于 `.agents/skills/hyperframes*/`；第 2 层指南位于 `skills/core/hyperframes.md`
- `character-animation` 流水线使用 HyperFrames 作为制作渲染包。浏览器预览仅是 QA/调试工件，而非渲染路径。

### FFmpeg（回退/简单剪辑）

- 在不需要合成时处理纯拼接/裁剪
- 也处理作为后期操作的字幕烧录

`video_compose` 读取 `edit_decisions.render_runtime` 并通过 `_render_via_hyperframes`、`_remotion_render` 或 `_render_via_ffmpeg` 进行分发。禁止静默运行时切换——当所选运行时不可用时，工具返回结构化的阻碍信息。参见 `AGENT_GUIDE.md` → "合成运行时（video_compose 内部）"和 `skills/core/hyperframes.md` 以获取完整决策矩阵。

---

## 测试架构

```
tests/
├── contracts/              # 阶段 0-3：工具契约验证、模式检查、注册表测试
├── qa/                     # 集成测试：TTS、图像生成、音乐、音频混音、视频合成/拼接、端到端
├── eval/                   # 用于回归测试的金色场景重放框架
├── pipelines/              # 流水线级别测试
├── tools/                  # 单个工具测试
└── styles/                 # 风格剧本书测试
```

**契约测试**验证每个工具都满足 `BaseTool` 契约：身份字段、模式、依赖声明、继承。

**QA 测试**调用真实工具（使用真实 API/二进制文件）并检查输出质量。

**评估框架**（`tests/eval/replay_harness/`）使用基于容差的比较重放金色场景，用于随机性输出。

---

## 系统依赖

**必需的：**
- Python >= 3.10
- FFmpeg（被约 15 个工具使用）

**可选的（扩展能力）：**
- Node.js（用于 Remotion 合成器）
- GPU + CUDA（用于本地视频/图像生成）
- Piper（离线 TTS）
- ManimCE（数学动画）
- Mermaid CLI（图表生成）

**Python 包：** pyyaml、pydantic、jsonschema、python-dotenv（核心）；pytest、pytest-asyncio（开发）；torch、torchvision、torchaudio（GPU）

---

## 关键设计决策

1. **无运行时编排器**——LLM 代理读取 YAML + Markdown 并驱动一切。这使得系统可调试（只需阅读技能）且与模型无关。

2. **基于检查点的恢复**——任何阶段都可以失败，流水线从最后一个检查点恢复。无需重新运行已完成的阶段。

3. **模式验证的工件**——在写入检查点之前，每个阶段输出都针对 JSON Schema 进行验证。防止垃圾信息传播。

4. **预算作为一等概念**——执行前成本估算、预算预留和对账。代理不能静默超支。

5. **选择器模式而非硬编码提供商**——能力优雅降级。缺少 API 密钥？选择器会回退到下一个提供商或本地替代方案。

6. **智能在技能而非代码中**——创意决策、质量检查清单、审查标准和提示模板存在于 Markdown 技能中，而非 Python 中。这意味着代理的行为可以通过编辑文本文件而非代码来调整。
