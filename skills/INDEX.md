# OpenMontage — 技能索引

> 如需完整的代理入门指南，请参阅项目根目录下的 [`AGENT_GUIDE.md`](../AGENT_GUIDE.md)。

本文件列出了所有可用的第 2 层技能，并介绍了三层知识架构。

## 知识架构

```
第 1 层：tools/tool_registry.py          "存在哪些工具及其功能"
         tools/base_tool.py               每个工具声明：功能、层级、状态、
                                          依赖、成本和 agent_skills[]

         â†" agent_skills[] 指向 â†"

第 2 层：skills/                          "OpenMontage 如何使用这些工具"
         项目特定约定：                     流水线集成、产物映射、
         {core,creative,meta,pipelines}/   增强链顺序、质量检查清单

         â†" 引用底层技术于 â†"

第 3 层：.agents/skills/                  "技术本身的工作原理"
         通用 API 知识来自                 正确的导入路径、代码模式、
         skills.sh（47 个已安装技能）      约束条件、参数 — 技术无关
```

**代理如何使用此结构：**
1. 编排器查询第 1 层（`tool_registry.support_envelope()`）了解可用工具
2. 每个工具的 `agent_skills[]` 字段指明其依赖的第 3 层技能
3. 第 2 层技能（本目录）教导代理 OpenMontage 特定的约定
4. 第 3 层技能（`.agents/skills/`）提供通用 API 知识，按需加载

## 能力家族与工具发现

每个工具声明一个 `capability`（功能）和一个 `provider`（提供者）。注册表按能力对工具进行分组，以便代理能够发现特定任务的所有可用选项。

### 选择器/提供者模式

对于具有多个提供者的能力家族（TTS、视频生成），架构使用：
- **选择器工具**（`tts_selector`、`video_selector`、`image_selector`）— 根据需求、API 密钥可用性和成本路由到最佳可用提供者。选择器自动从注册表发现提供者。当用户未指定提供者时，代理应默认使用选择器。
- **提供者工具** — 直接调用特定的提供者。当用户明确请求某个提供者或选择器的路由不适用时，代理使用这些工具。

### 能力家族参考

**不要维护硬编码的工具列表。** 注册表是唯一的事实来源。在运行时查询：

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
```

在输出中查找的关键能力家族：

| 能力 | 选择器 | 发现机制 |
|---|---|---|---|
| `tts` | `tts_selector` | 自动发现所有 `capability="tts"` 工具 |
| `video_generation` | `video_selector` | 自动发现所有 `capability="video_generation"` 工具 |
| `image_generation` | `image_selector` | 自动发现所有 `capability="image_generation"` 工具 |
| `audio_processing` | — | 基于 FFmpeg 的本地工具 |
| `enhancement` | — | 混合提供者 |
| `analysis` | — | 混合提供者 |
| `character_animation` | — | 本地角色规格、SVG 骨架、姿态库、动作时间线、预览和 QA |
| `graphics` | — | 本地渲染工具 |
| `music_generation` | — | 单一提供者 |
| `subtitle` | — | 纯 Python |
| `avatar` | — | 本地 GPU 模型 |
| `video_post` | — | 基于 FFmpeg 的本地工具 |

### 添加新工具

1. 将工具放置在正确的能力文件夹中（或在 `tools/` 下创建新文件夹）
2. 在类定义中设置 `capability` 和 `provider`
3. 如果加入多提供者家族，现有选择器会自动发现它
4. 通过 `agent_skills[]` 附加相关的第 2 层和第 3 层技能
5. 注册表自动发现工具 — 无需手动注册
6. **无需更新其他文件** — 选择器、清单和指令均源自注册表

## 核心技能

| 技能 | 文件 | 触发条件 | 代理技能（第 3 层） |
|-------|------|---------|----------------------|
| FFmpeg | `core/ffmpeg.md` | 视频编码、滤镜、合成 | `ffmpeg`, `video-toolkit` |
| Remotion | `core/remotion.md` | 基于 React 的合成，第 3+ 阶段 | `remotion-best-practices`, `remotion` |
| HyperFrames | `core/hyperframes.md` | HTML/CSS/GSAP 合成运行时 — 动态排版、音乐视频、产品宣传片、网页捕获。供应商版本 v0.7.17（2026-06-27）。 | `hyperframes`（路由器）→ `hyperframes-core`（合约）, `hyperframes-creative`（调色板/排版/旁白）, `hyperframes-media`（TTS/BGM/SFX/字幕）, `hyperframes-animation`（所有动效）, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `motion-graphics`, `music-to-video`（节拍驱动）, `website-to-video`, `remotion-to-hyperframes`（迁移）, `gsap-core`, `gsap-timeline` |
| WhisperX | `core/whisperx.md` | 带词级时间戳的转写 | `speech-to-text` |
| 字幕同步 | `core/subtitle-sync.md` | 字幕时序与对齐 | `remotion-best-practices` |
| 调色 | `core/color-grading.md` | FFmpeg 色彩配置、LUT 工作流、无障碍 | `ffmpeg` |

## 创意技能

| 技能 | 文件 | 触发条件 | 代理技能（第 3 层） |
|-------|------|---------|----------------------|
| 视频剪辑 | `creative/video-editing.md` | 剪辑决策、节奏、韵律 | `ffmpeg`, `video-toolkit` |
| 增强策略 | `creative/enhancement-strategy.md` | 叠加放置与密度 | `ffmpeg` |
| 数据可视化 | `creative/data-visualization.md` | 图表类型选择、动画、标签放置 | `d3-viz`, `remotion-best-practices` |
| 视频拼接 | `creative/video-stitching.md` | 多片段组装、AI 片段链接、空间合成 | `ffmpeg`, `video-toolkit` |
| 视频生成提示 | `creative/video-gen-prompting.md` | 通用视频生成提示词汇表；**规范 5 维规格**（主体/运动/场景/空间/相机）；约 200 个摄影原语 | `ai-video-gen`, `ltx2`, `create-video` |
| â†³ Seedance 提示 | `creative/prompting/seedance-prompting.md` | **首选的付费默认值。** Seedance 2.0 8 组件结构、多镜头、唇形同步、参考转视频 | `seedance-2-0`, `ai-video-gen` |
| â†³ Grok 提示 | `creative/prompting/grok-prompting.md` | Grok 图像/视频提示、编辑流程、参考图像视频 | `grok-media` |
| â†³ Sora 提示 | `creative/prompting/sora-prompting.md` | Sora 2 结构化模板、高级字段 | `ai-video-gen` |
| â†³ VEO 提示 | `creative/prompting/veo-prompting.md` | VEO 3.1 14 组件结构、艺术运动 | `ai-video-gen` |
| â†³ LTX 提示 | `creative/prompting/ltx-prompting.md` | LTX-2 6 元素结构、音频提示 | `ltx2` |
| â†³ HunyuanVideo 提示 | `creative/prompting/hunyuan-prompting.md` | HunyuanVideo 公式、I2V 最佳实践 | â€" |
| 故事叙述 | `creative/storytelling.md` | 叙事结构、钩子、节奏、Mayer 原则 | â€" |
| 音效设计 | `creative/sound-design.md` | 音频闪避、LUFS 目标、SFX 时序、AI TTS 混音 | `elevenlabs` |
| 排版 | `creative/typography.md` | 字体选择、文字大小、安全区域、字幕样式 | â€" |
| ManimCE 使用 | `creative/manim-usage.md` | 场景合成、动画时序、色彩使用 | `manimce-best-practices` |
| 图像生成使用 | `creative/image-gen-usage.md` | 提示一致性、主视觉参考、批量策略 | `flux-best-practices`, `bfl-api` |
| 图像提供者使用 | `creative/image-provider-usage.md` | 提供者选择（FLUX/Grok/OpenAI/Recraft/图库）、成本-质量权衡 | `flux-best-practices`, `bfl-api`, `grok-media` |
| B-Roll 规划 | `creative/broll-planning.md` | 图库 vs 生成决策、查询构建、素材评估 | — |
| 图库素材使用 | `creative/stock-sourcing-usage.md` | Pexels/Pixabay 使用、参数、许可、集成 | — |
| 场景检测使用 | `creative/scene-detect-usage.md` | 阈值调优、算法选择、内容预设 | â€" |
| 图表生成使用 | `creative/diagram-gen-usage.md` | 复杂度限制、渐进式构建、主题 | `beautiful-mermaid` |
| 音乐生成使用 | `creative/music-gen-usage.md` | BPM 选择、提示工程、时长匹配 | `music`, `elevenlabs` |
| 背景移除 | `creative/bg-remove-usage.md` | 模型选择、Alpha 抠图、合成工作流 | â€" |
| 放大 | `creative/upscale-usage.md` | 缩放因子、模型选择、人脸感知放大 | â€" |
| 人脸修复 | `creative/face-restore-usage.md` | CodeFormer/GFPGAN 选择、保真度调优、vs face_enhance | â€" |
| 唇形同步 | `creative/lip-sync-usage.md` | Wav2Lip 模型选择、配音工作流、输入要求 | `faceswap` |
| 虚拟形象生成 | `creative/talking-head-gen-usage.md` | SadTalker/MuseTalk、照片转视频、表情调优 | `avatar-video` |
| 视频理解 | `creative/video-understand-usage.md` | 视觉 QA、质量门控、场景分类 | `video-understand` |

## 流水线类型技能

流水线类型技能为特定视频格式提供制作指导，独立于动画讲解或虚拟形象发言人的流水线。

| 技能 | 文件 | 使用时机 |
|-------|------|-------------|
| 短视频 | `creative/short-form.md` | TikTok、Reels、Shorts — 竖屏 9:16、60 秒以内 |
| 长视频 | `creative/long-form.md` | YouTube 10 分钟以上 — 章节、留存、结尾画面 |
| 屏幕录制 | `creative/screen-recording.md` | 代码讲解、教程、软件演示 |
| 动画流水线 | `creative/animation-pipeline.md` | 动态图形、缓动、转场、合成 |
| 角色动画流水线 | `pipelines/character-animation/` | 绑定本地卡通角色、姿态库、动作时间线、SVG/Canvas/Remotion/HyperFrames 渲染 |
| 影视感 | `creative/cinematic.md` | 宽银幕、电影节奏、分层音频、调色 |

## 流水线阶段导演技能

阶段导演技能指导代理如何执行每个流水线阶段。每个技能是一个详细的 markdown 文件，包含流程步骤、质量评分标准和自我评估准则。

### 动画讲解流水线（`pipelines/explainer/`）— v2.0

| 技能 | 文件 | 阶段 | 关键能力 |
|-------|------|-------|-----------------|
| **执行制片人** | `pipelines/explainer/executive-producer.md` | `all` | **8 阶段串行编排、质量门禁、跨阶段检查、退回** |
| **研究导演** | `pipelines/explainer/research-director.md` | `research` | **网络研究方法论、5 批搜索、景观/趋势/数据/受众/专家分析** |
| **提案导演** | `pipelines/explainer/proposal-director.md` | `proposal` | **基于研究的概念方案、制作计划、成本估算、审批关卡** |
| 剧本导演 | `pipelines/explainer/script-director.md` | `script` | 叙事架构、时间控制、增强提示、研究整合 |
| 场景导演 | `pipelines/explainer/scene-director.md` | `scene_plan` | 视觉规划、技术库、可行性 |
| 素材导演 | `pipelines/explainer/asset-director.md` | `assets` | TTS、图像生成、图表生成、音乐、预算 |
| 剪辑导演 | `pipelines/explainer/edit-director.md` | `edit` | 时间线组装、字幕、音频闪避 |
| 合成导演 | `pipelines/explainer/compose-director.md` | `compose` | FFmpeg/Remotion 渲染、音频混音 |
| 发布导演 | `pipelines/explainer/publish-director.md` | `publish` | SEO 元数据、章节、导出打包 |

> **注：** 旧的 `idea-director.md` 仍然存在供参考，但已被 v2.0 的研究 + 提案两阶段流程取代。虚拟形象发言人流水线继续使用其自己的 `idea-director`。

### 虚拟形象发言人流水线（`pipelines/talking-head/`）

| 技能 | 文件 | 阶段 | 关键能力 |
|-------|------|-------|-----------------|
| 创意导演 | `pipelines/talking-head/idea-director.md` | `idea` | 素材检查、内容评估 |
| 剧本导演 | `pipelines/talking-head/script-director.md` | `script` | 转录、段落分割 |
| 场景导演 | `pipelines/talking-head/scene-director.md` | `scene_plan` | 增强规划、叠加放置 |
| 素材导演 | `pipelines/talking-head/asset-director.md` | `assets` | 字幕生成、音频提取 |
| 剪辑导演 | `pipelines/talking-head/edit-director.md` | `edit` | 剪辑组装、字幕配置 |
| 合成导演 | `pipelines/talking-head/compose-director.md` | `compose` | 增强链、渲染 |
| 发布导演 | `pipelines/talking-head/publish-director.md` | `publish` | 元数据、导出打包 |

### 屏幕演示流水线（`pipelines/screen-demo/`）— v2.0

| 技能 | 文件 | 阶段 | 关键能力 |
|-------|------|-------|-----------------|
| **执行制片人** | `pipelines/screen-demo/executive-producer.md` | `all` | **7 阶段串行编排、可读性门禁、音频清晰度、节奏检查** |
| 创意导演 | `pipelines/screen-demo/idea-director.md` | `idea` | 工作流范围界定、UI 密度评估、输出形态选择 |
| 剧本导演 | `pipelines/screen-demo/script-director.md` | `script` | 动作映射、程序化叙述、速度规划 |
| 场景导演 | `pipelines/screen-demo/scene-director.md` | `scene_plan` | 裁剪规划、标注克制、宽高比可行性 |
| 素材导演 | `pipelines/screen-demo/asset-director.md` | `assets` | 字幕优先素材包、音频清理、可复用叠加层 |
| 剪辑导演 | `pipelines/screen-demo/edit-director.md` | `edit` | 紧凑时间线规划、速度注释、字幕区域控制 |
| 合成导演 | `pipelines/screen-demo/compose-director.md` | `compose` | 可读性优先渲染、清晰屏幕输出、验证 |
| 发布导演 | `pipelines/screen-demo/publish-director.md` | `publish` | 可搜索元数据、章节打包、缩略图概念 |

### 片段工厂流水线（`pipelines/clip-factory/`）— v2.0

| 技能 | 文件 | 阶段 | 关键能力 |
|-------|------|-------|-----------------|
| **执行制片人** | `pipelines/clip-factory/executive-producer.md` | `all` | **7 阶段串行编排、片段选择门禁、批次一致性、钩子放置** |
| 创意导演 | `pipelines/clip-factory/idea-director.md` | `idea` | 批次策略、片段家族、产出规划 |
| 剧本导演 | `pipelines/clip-factory/script-director.md` | `script` | 转录挖掘、排序、独立验证 |
| 场景导演 | `pipelines/clip-factory/scene-director.md` | `scene_plan` | 平台构图、安全区域、裁剪可行性规划 |
| 素材导演 | `pipelines/clip-factory/asset-director.md` | `assets` | 共享品牌包、重定基字幕、批次音频一致性 |
| 剪辑导演 | `pipelines/clip-factory/edit-director.md` | `edit` | 钩子优先微剪辑、系列一致性 |
| 合成导演 | `pipelines/clip-factory/compose-director.md` | `compose` | 多任务渲染、批次弹性、逐输出验证 |
| 发布导演 | `pipelines/clip-factory/publish-director.md` | `publish` | 发布顺序、平台文案、批次编目 |

### 播客再利用流水线（`pipelines/podcast-repurpose/`）— v2.0

| 技能 | 文件 | 阶段 | 关键能力 |
|-------|------|-------|-----------------|
| **执行制片人** | `pipelines/podcast-repurpose/executive-producer.md` | `all` | **7 阶段串行编排、音频保留门禁、片段质量、多交付物** |
| 创意导演 | `pipelines/podcast-repurpose/idea-director.md` | `idea` | 按源模式的交付物组合、实际长视频规划 |
| 剧本导演 | `pipelines/podcast-repurpose/script-director.md` | `script` | 带说话人标签的转录真相、亮点排序、章节映射 |
| 场景导演 | `pipelines/podcast-repurpose/scene-director.md` | `scene_plan` | 忠实于源的处理方案、音频图 vs 引言 vs 伴生视频规划 |
| 素材导演 | `pipelines/podcast-repurpose/asset-director.md` | `assets` | 字幕优先打包、说话人素材、可选题图 |
| 剪辑导演 | `pipelines/podcast-repurpose/edit-director.md` | `edit` | 钩子引导播客片段、引言停留时间、伴生视频简洁性 |
| 合成导演 | `pipelines/podcast-repurpose/compose-director.md` | `compose` | 音频优先渲染、交付物优先级排序 |
| 发布导演 | `pipelines/podcast-repurpose/publish-director.md` | `publish` | 剧集交叉链接、嘉宾署名、错开发布逻辑 |

### 电影感流水线（`pipelines/cinematic/`）— v2.0

| 技能 | 文件 | 阶段 | 关键能力 |
|-------|------|-------|-----------------|
| **执行制片人** | `pipelines/cinematic/executive-producer.md` | `all` | **7 阶段串行编排、情感节奏门禁、色彩一致性、音频动态** |
| 创意导演 | `pipelines/cinematic/idea-director.md` | `idea` | 情感弧线选择、源素材真相、交付形态规划 |
| 剧本导演 | `pipelines/cinematic/script-director.md` | `script` | 节拍映射、对话精选、标题卡克制 |
| 场景导演 | `pipelines/cinematic/scene-director.md` | `scene_plan` | 主镜头规划、揭示结构、转场限制 |
| 素材导演 | `pipelines/cinematic/asset-director.md` | `assets` | 源素材精选、辅助插入纪律、音乐/氛围规划 |
| 剪辑导演 | `pipelines/cinematic/edit-director.md` | `edit` | 情感优先节奏、揭示时机、音频驱动韵律 |
| 合成导演 | `pipelines/cinematic/compose-director.md` | `compose` | 调色与混音收尾、画面处理判断 |
| 发布导演 | `pipelines/cinematic/publish-director.md` | `publish` | 主视觉 vs 预告片打包、海报帧概念 |

### 动画流水线（`pipelines/animation/`）— v2.0

| 技能 | 文件 | 阶段 | 关键能力 |
|-------|------|-------|-----------------|
| **执行制片人** | `pipelines/animation/executive-producer.md` | `all` | **8 阶段串行编排、质量门禁、动效一致性、数学精度检查** |
| **研究导演** | `pipelines/animation/research-director.md` | `research` | **主题 + 动画技术研究、视觉参考扫描、模式知情角度** |
| **提案导演** | `pipelines/animation/proposal-director.md` | `proposal` | **动画模式选择（Manim/Remotion/AI/图表）、复用策略、成本估算、审批关卡** |
| 剧本导演 | `pipelines/animation/script-director.md` | `script` | 动画就绪节拍、文本克制、研究整合、模式感知写作 |
| 场景导演 | `pipelines/animation/scene-director.md` | `scene_plan` | 动态分镜规划、转场系统、工具路径映射 |
| 素材导演 | `pipelines/animation/asset-director.md` | `assets` | 确定性素材选择、可复用图案、可行性真相 |
| 剪辑导演 | `pipelines/animation/edit-director.md` | `edit` | 停留时间、错开规则、可读动效规划 |
| 合成导演 | `pipelines/animation/compose-director.md` | `compose` | 清晰渲染输出、时序完整性、安全区域检查 |
| 发布导演 | `pipelines/animation/publish-director.md` | `publish` | 动画模式打包、缩略图系统对齐 |

> **注：** 旧的 `idea-director.md` 仍然存在供参考，但已被 v2.0 的研究 + 提案两阶段流程取代。

### 混合流水线（`pipelines/hybrid/`）— v2.0

| 技能 | 文件 | 阶段 | 关键能力 |
|-------|------|-------|-----------------|
| **执行制片人** | `pipelines/hybrid/executive-producer.md` | `all` | **7 阶段串行编排、源素材/辅助平衡门禁、叠加密度、连贯性** |
| 创意导演 | `pipelines/hybrid/idea-director.md` | `idea` | 锚定媒介选择、辅助层规划、回退可见性 |
| 剧本导演 | `pipelines/hybrid/script-director.md` | `script` | 源素材 vs 辅助节拍映射、对话保留、辅助理由 |
| 场景导演 | `pipelines/hybrid/scene-director.md` | `scene_plan` | 源素材优先布局规则、叠加密度控制、变体安全规划 |
| 素材导演 | `pipelines/hybrid/asset-director.md` | `assets` | 共享辅助包、源素材 vs 生成素材追踪 |
| 剪辑导演 | `pipelines/hybrid/edit-director.md` | `edit` | 锚定剪辑优先工作流、分层辅助时机、可读变体 |
| 合成导演 | `pipelines/hybrid/compose-director.md` | `compose` | 源素材/辅助平衡检查、变体验证、连贯混音 |
| 发布导演 | `pipelines/hybrid/publish-director.md` | `publish` | 主视觉 vs 衍生打包、源素材混合元数据 |

### 虚拟形象发言人流水线（`pipelines/avatar-spokesperson/`）— v2.0

| 技能 | 文件 | 阶段 | 关键能力 |
|-------|------|-------|-----------------|
| **执行制片人** | `pipelines/avatar-spokesperson/executive-producer.md` | `all` | **7 阶段串行编排、唇形同步质量门禁、主讲人构图、CTA 落地** |
| 创意导演 | `pipelines/avatar-spokesperson/idea-director.md` | `idea` | 虚拟形象路径分类、CTA 范围界定、能力真相 |
| 剧本导演 | `pipelines/avatar-spokesperson/script-director.md` | `script` | 口播文案塑造、场景安全节奏、文本克制 |
| 场景导演 | `pipelines/avatar-spokesperson/scene-director.md` | `scene_plan` | 主讲人布局、背景纪律、变体真实感 |
| 素材导演 | `pipelines/avatar-spokesperson/asset-director.md` | `assets` | 虚拟形象路径锁定、旁白分辨率、最小辅助包 |
| 剪辑导演 | `pipelines/avatar-spokesperson/edit-director.md` | `edit` | 主讲人优先剪辑规划、叠加时机、CTA 落地 |
| 合成导演 | `pipelines/avatar-spokesperson/compose-director.md` | `compose` | 唇形同步验证、字幕安全构图、清晰渲染检查 |
| 发布导演 | `pipelines/avatar-spokesperson/publish-director.md` | `publish` | 受众导向打包、主讲人优先缩略图概念 |

### 本地化配音流水线（`pipelines/localization-dub/`）— v2.0

| 技能 | 文件 | 阶段 | 关键能力 |
|-------|------|-------|-----------------|
| **执行制片人** | `pipelines/localization-dub/executive-producer.md` | `all` | **7 阶段串行编排、翻译精度门禁、时序保留、逐语言环境 QA** |
| 创意导演 | `pipelines/localization-dub/idea-director.md` | `idea` | 范围定义、语言环境规划、术语表与评审捕获 |
| 剧本导演 | `pipelines/localization-dub/script-director.md` | `script` | 转录真相、翻译脚本打包、术语保留 |
| 场景导演 | `pipelines/localization-dub/scene-director.md` | `scene_plan` | 配音模式选择、时序风险映射、屏幕文字规划 |
| 素材导演 | `pipelines/localization-dub/asset-director.md` | `assets` | 字幕优先本地化包、配音音频生成、可选唇形同步 |
| 剪辑导演 | `pipelines/localization-dub/edit-director.md` | `edit` | 语言环境特定时间线、覆盖规划、时序调整 |
| 合成导演 | `pipelines/localization-dub/compose-director.md` | `compose` | 逐语言环境渲染、字幕适配检查、输出标记 |
| 发布导演 | `pipelines/localization-dub/publish-director.md` | `publish` | 语言环境打包、元数据精度、QA 注释保留 |

## 元技能

适用于所有流水线的跨领域技能：

| 技能 | 文件 | 用途 |
|-------|------|---------|
| 入职引导 | `meta/onboarding.md` | 首次交互问候、能力发现、入门提示 |
| 评审员 | `meta/reviewer.md` | 每个阶段后的自我评审协议 |
| 检查点协议 | `meta/checkpoint-protocol.md` | 何时/如何设置检查点并请求人工审批 |
| 技能创建器 | `meta/skill-creator.md` | 在流水线运行期间动态创建新技能 |
| 动画运行时选择器 | `meta/animation-runtime-selector.md` | 为每个场景选择渲染运行时 + 动画库 |
| 定制合成（Atelier） | `meta/bespoke-composition.md` | 从头开始手工编写合成（核心工作）— 无预制场景类型；路由从艺术指导 → 动效原则 → 引擎机制 → Atelier 渲染 |

## 样式手册

样式手册（`styles/*.yaml`）定义视觉语言、排版、动效、音频和素材生成约束。它们会通过 `schemas/styles/playbook.schema.json` 进行验证。

| 手册 | 类别 | 情绪 | 最适合 |
|----------|----------|------|----------|
| `clean-professional` | 动态图形 | 精致、可靠 | 企业、教育、SaaS |
| `flat-motion-graphics` | 动态图形 | 充满活力、大胆 | 社交媒体、TikTok、初创公司 |
| `minimalist-diagram` | 白板 | 专注、技术性 | 技术深度分析、架构 |

通过 `styles/playbook_loader.py` 加载：`load_playbook("clean-professional")`

## 已安装的代理技能（第 3 层）

所有代理技能位于 `.agents/skills/`，并通过 `npx skills add` 管理。
Claude Code 通过 `.claude/skills/` 中的符号链接访问。

| 类别 | 已安装技能 | 来源 |
|----------|-----------------|--------|
| **视频合成** | `remotion-best-practices`, `remotion`, `hyperframes`（路由器）, `hyperframes-core`, `hyperframes-creative`, `hyperframes-media`, `hyperframes-animation`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `motion-graphics`, `music-to-video`, `remotion-to-hyperframes`, `website-to-video` | `remotion-dev/skills`, `digitalsamba/claude-code-video-toolkit`, `heygen-com/hyperframes`（供应商版本 v0.7.17，见 `.agents/skills/hyperframes/PROVENANCE.md`） |
| **视频处理** | `ffmpeg`, `video-toolkit` | `digitalsamba/claude-code-video-toolkit` |
| **TTS 与音频** | `text-to-speech`, `speech-to-text`, `music`, `sound-effects`, `elevenlabs`, `agents`, `setup-api-key` | `elevenlabs/skills`, `digitalsamba/claude-code-video-toolkit` |
| **图像生成** | `flux-best-practices`, `bfl-api`, `grok-media` | `black-forest-labs/skills`, 本地 OpenMontage 技能 |
| **数学动画** | `manimce-best-practices`, `manimgl-best-practices`, `manim-composer` | `adithya-s-k/manim_skill` |
| **3D 图形** | `threejs-animation`, `threejs-fundamentals`, `threejs-geometry`, `threejs-interaction`, `threejs-lighting`, `threejs-loaders`, `threejs-materials`, `threejs-postprocessing`, `threejs-shaders`, `threejs-textures` | `cloudai-x/threejs-skills` |
| **图表** | `beautiful-mermaid`, `d3-viz` | `intellectronica/agent-skills`, `davila7/claude-code-templates` |
| **动画** | `framer-motion`, `lottie-bodymovin` | `pproenca/dot-skills`, `dylantarre/animation-principles` |
| **设计** | `tailwind-design-system`, `web-design-guidelines`, `vercel-react-best-practices`, `vercel-composition-patterns` | `wshobson/agents`, `vercel-labs/agent-skills` |
| **AI 视频（HeyGen）** | `heygen`, `avatar-video`, `create-video`, `faceswap`, `ai-video-gen`, `video-download`, `video-edit`, `video-translate`, `video-understand`, `visual-style` | `heygen-com/skills` |
| **AI 视频（高级）** | `seedance-2-0` — 首选的付费默认值（电影感、预告片、多镜头、唇形同步、同步音频）；通过 `seedance_video`（fal.ai）或 `heygen_video` 虚拟形象镜头访问 | 本地 OpenMontage 技能 |
| **基础设施** | `acestep`, `ltx2`, `playwright-recording` | `digitalsamba/claude-code-video-toolkit` |
