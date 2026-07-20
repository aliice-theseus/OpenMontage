# OpenMontage - 共享项目上下文

这是项目架构和约定的唯一真实来源。所有特定于平台的代理文件（CODEX.md, COPILOT.md）应指向此处，而不是重复这些内容。

## 身份定位

OpenMontage 是一个开源的、由 AI 编排的视频制作平台。

## 架构：指令驱动（代理优先）

AI 代理本身就是智能核心。Python 仅用于工具和持久化。其他一切——编排、创意决策、审查、阶段转换——都存在于代理遵循的指令中（YAML 清单 + Markdown 技能）。

```
代理读取管道清单 (YAML) → 读取阶段导演技能 (MD)
→ 使用工具 (Python BaseTool) → 自我审查 (元技能)
→ 检查点 (Python 工具) → 提交给人工审批
```

**没有 Python 编排器，没有 Python 审查器，没有 Python 处理器。** 代理驱动整个管道。

## 真实信息来源

- **代理指南与合约：** `AGENT_GUIDE.md`（工具清单、管道选择、阶段代理、协议）
- **技能索引：** `skills/INDEX.md`
- **工具注册表：** `tools/tool_registry.py`
- **管道清单：** `pipeline_defs/`
- **产物模式：** `schemas/artifacts/`
- **风格剧本：** `styles/*.yaml`（模式：`schemas/styles/playbook.schema.json`）
- **阶段导演技能：** `skills/pipelines/<pipeline>/<stage>-director.md`
- **元技能：** `skills/meta/*.md`（审查器、检查点协议、技能创建器）
- **架构深度解析：** `docs/ARCHITECTURE.md`

## 知识架构（三层）

```
第1层: tools/tool_registry.py     → "存在什么工具"（运行时能力、状态、成本）
第2层: skills/                    → "OpenMontage 如何使用它们"（项目约定）
第3层: .agents/skills/            → "技术如何工作"（通用 API 规则、skills.sh）
```

每个工具的 `agent_skills[]` 字段连接第1层 → 第3层。完整映射请参见 `skills/INDEX.md`。

## 关键模式

- **管道状态机：** `idea -> script -> scene_plan -> assets -> edit -> compose -> publish`
- **指令驱动阶段：** 每个阶段都有一个导演技能（MD）来教导代理如何执行
- **管道清单：** 声明式 YAML 定义阶段、技能、工具、审查重点、审批关卡
- **能力优先的工具设计：** 每个主要工具族应暴露一个选择器工具加上明确的提供商工具
  - 示例：`tts_selector` + `elevenlabs_tts` / `google_tts` / `openai_tts` / `piper_tts`
  - 示例：`video_selector` + `heygen_video` / `wan_video` / `hunyuan_video` / `ltx_video_local` / `ltx_video_modal` / `cogvideo_video`
- **风格剧本：** YAML 定义视觉语言、排版、运动、音频、资产生成约束
- **产物是规范的：** `brief`, `script`, `scene_plan`, `asset_manifest`, `edit_decisions`, `render_report`, `publish_log`
- **每个工具都继承自 `tools/base_tool.py`**（ToolContract）
- **检查点策略** 存在于管道清单中（每个阶段的 `human_approval_default`）+ `skills/meta/checkpoint-protocol.md`
- **审查器** 是一个元技能（`skills/meta/reviewer.md`），建议性质，最多2轮
- **成本追踪器**（`tools/cost_tracker.py`）管理预算：估算 -> 预留 -> 对账
- **规范产物** 根据 `schemas/artifacts/` 中的 JSON 模式进行验证

## 关键文件

| 文件 | 用途 |
|------|---------|
| `config.yaml` | 全局配置 |
| `lib/config_model.py` | 运行时配置加载器（Pydantic） |
| `lib/checkpoint.py` | 检查点写入器/读取器 |
| `lib/pipeline_loader.py` | 管道清单加载器 + 辅助工具 |
| `lib/media_profiles.py` | 平台特定的渲染配置文件 |
| `styles/playbook_loader.py` | 风格剧本加载器 + 验证器 + 设计智能（颜色/字体/无障碍） |
| `tools/base_tool.py` | ToolContract 基类 |
| `tools/tool_registry.py` | 工具发现和报告 |
| `tools/cost_tracker.py` | 预算治理 |
| `tools/video/video_stitch.py` | 多片段组装（拼接、空间布局、验证、预览） |
| `tools/video/video_compose.py` | 运行时感知的合成编排器 — 根据 `edit_decisions.render_runtime` 路由到 Remotion / HyperFrames / FFmpeg |
| `tools/video/hyperframes_compose.py` | HyperFrames 运行时 — 工作区实例化、`hyperframes lint`/`validate`/`render`、FFmpeg 基础检查 |
| `tools/character/character_animation.py` | 本地角色动画工具 — 角色规格、SVG 骨架方案、姿势库、动作时间线、HyperFrames 包和 QA 报告 |
| `lib/hyperframes_style_bridge.py` | 剧本 → CSS 自定义属性 + 用于 HyperFrames 工作区的 `DESIGN.md` 桥梁 |
| `remotion-composer/src/components/` | 8 个 Remotion 组件（TextCard, StatCard, ProgressBar, CalloutBox, ComparisonCard + charts/） |
| `.agents/skills/hyperframes*/` | 供应商 HyperFrames 第3层技能（创作合约、CLI、注册表、网站转视频） |
| `skills/core/hyperframes.md` | 第2层 — OpenMontage 何时选择 HyperFrames 与 Remotion，产物 → 工作区映射 |
| `schemas/styles/playbook.schema.json` | 带有设计令牌的剧本模式 v2（chart_palette, scale_system, weight_matrix, color_rules） |
| `tests/qa/` | 逐个工具输出检查的质量验证测试脚本 |

## 可用管道

| 管道 | 清单文件 | 类型 |
|----------|----------|------|
| `talking-head` | `pipeline_defs/talking-head.yaml` | 基于素材 |
| `animated-explainer` | `pipeline_defs/animated-explainer.yaml` | AI 生成 |
| `screen-demo` | `pipeline_defs/screen-demo.yaml` | 屏幕录制 |
| `clip-factory` | `pipeline_defs/clip-factory.yaml` | 短视频批量提取 |
| `podcast-repurpose` | `pipeline_defs/podcast-repurpose.yaml` | 播客二次利用 |
| `cinematic` | `pipeline_defs/cinematic.yaml` | 电影级剪辑 |
| `documentary-montage` | `pipeline_defs/documentary-montage.yaml` | 检索优先的纪录片蒙太奇 |
| `animation` | `pipeline_defs/animation.yaml` | 动画优先 |
| `character-animation` | `pipeline_defs/character-animation.yaml` | 本地骨骼角色动画 |
| `hybrid` | `pipeline_defs/hybrid.yaml` | 素材加辅助视觉混合 |
| `avatar-spokesperson` | `pipeline_defs/avatar-spokesperson.yaml` | 虚拟形象主持人 |
| `localization-dub` | `pipeline_defs/localization-dub.yaml` | 本地化和配音 |
| `framework-smoke` | `pipeline_defs/framework-smoke.yaml` | 测试工具 |

## 构建新管道时

1. 在 `pipeline_defs/` 中创建 YAML 清单（由 `pipeline_manifest.schema.json` 验证）
2. 在 `skills/pipelines/<pipeline-name>/` 中创建阶段导演技能（7个技能：从 idea 到 publish）
3. 在清单中引用元技能（审查器、检查点协议）
4. 向清单添加兼容的剧本
5. 在 `tests/contracts/` 中添加合约测试

## 构建新工具时

1. 继承 `tools/base_tool.py` 中的 `BaseTool`
2. 将工具放入正确的能力包中（`tools/audio/`, `tools/video/`, `tools/enhancement/`, `tools/analysis/`, `tools/graphics/`, `tools/avatar/`, `tools/subtitle/`）
3. 优先使用选择器加提供商的模式：
   - 一个能力路由工具方便代理使用
   - 每个真实提供商/运行时路径对应一个具体工具
4. 设置所有合约字段（name, version, tier, capability, provider, supports, fallback_tools, agent_skills 等）
5. 实现返回 `ToolResult` 的 `execute()` 方法
6. 通过 `tools/tool_registry.py` 进行发现；不依赖临时导入
7. 如果工具有复杂的 I/O，在 `schemas/tools/` 中添加 JSON 模式
8. 仅在运行时路径正确后添加测试
