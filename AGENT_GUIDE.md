# OpenMontage - 代理指南

从这里开始。这是 OpenMontage 的完整操作指南和代理合约。

有关架构、关键文件和约定，请参见 [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)。

## 首次交互 — 上手引导

当用户的第一条消息模糊、试探性或询问你能做什么时（"帮我做个视频"、"你能做什么？"、"帮我创建点什么"、"我想做内容"），请在执行任何其他操作**之前**先阅读上手引导技能：

**阅读：** `skills/meta/onboarding.md`

该技能教会你如何运行探索、分类用户的设置、用通俗语言介绍能力，并提供针对其可用工具量身定制的入门提示词。目标：在60秒内让用户从"好奇"到"开始制作视频"。

**跳过上手引导** 当用户带着具体、可操作的请求到来时（例如，"制作一个关于黑洞的60秒解说视频"）。直接进入第零条规则。

## 参考视频入口

当用户提供**视频 URL 或本地视频文件作为灵感**时——例如：

- "你能做一个像这样的视频吗？"
- "我喜欢这个 YouTube Short。给我做点类似的。"
- "把这个 Reel 作为参考。"

——**不要**将其视为普通的网络搜索或提示词编写请求。

这是 OpenMontage 中的一等工作流。

### 必需行为

1. **阅读：** `skills/meta/video-reference-analyst.md`
2. **运行参考分析工作流**，使用本地分析工具（`video_analyzer`、转录提取、场景检测、帧采样）
3. **生成关于参考视频的有根据的总结**，包括：
   - 内容
   - 节奏
   - 结构
   - 风格
   - 是什么让它奏效
4. **然后**运行正常的能力审计和管道选择
5. 为用户版本提供 **2-3个差异化概念**——不是照搬

### 重要区别

- **参考驱动请求：** "make me something like this" -> 使用 `video-reference-analyst.md`
- **源素材请求：** "edit this footage" / "cut this into clips" -> 使用 `source_media_review` 和相应的素材主导管道

如果模型错过这个区别，它通常会退回到简单的搜索加猜测。这对 OpenMontage 来说是不正确的。

## 第零条规则 — 所有制作必须经过管道

**每个视频制作请求必须经过管道系统。没有例外。**

当用户要求制作、创建、生成任何视频内容——预告片、解说、片段、动画或任何其他视频时，代理必须：

1. **识别管道。** 将请求与 `pipeline_defs/` 中的一个管道匹配。如果不清楚，询问用户。
2. **读取管道清单。** `pipeline_defs/<pipeline>.yaml`——了解阶段、工具和质量关卡。
3. **运行预检。** 通过注册表发现可用工具。呈现能力菜单。
4. **逐阶段执行。** 对于每个阶段，在该阶段做任何工作**之前**，先阅读阶段导演技能（`skills/pipelines/<pipeline>/<stage>-director.md`）。
5. **在调用工具前阅读第3层技能。** 在使用任何带有 `agent_skills` 字段的工具之前，阅读 `.agents/skills/` 中引用的技能。这些包含提供商特定的提示指导、参数优化和质量技术，能显著改善输出。

**不要：**
- 编写临时 Python 脚本直接调用工具
- 跳过管道直接进行 API 调用
- 在未阅读阶段导演技能之前生成资产
- 在不检查其第3层技能以获取提示指导的情况下使用工具
- 绕过预检、检查点或审查

智能在于技能，而不是临时编写的代码。一个阅读了导演技能和第3层知识的代理将比一个使用通用提示词直接调用工具的代理产生显著更好的输出。

## OpenMontage 是什么

OpenMontage 是一个指令驱动的视频制作系统。AI 代理**就是**智能核心——它阅读指令（管道清单 + 阶段导演技能 + 元技能）并使用工具驱动管道。

```
代理读取管道清单 (YAML) -> 读取阶段导演技能 (MD)
-> 使用工具 (Python BaseTool 子类) -> 自我审查 (元技能)
-> 检查点 (Python 工具) -> 提交给人工审批
```

**Python = 工具 + 持久化。** Python 代码中没有编排逻辑、创意决策、审查逻辑或检查点策略。代理在指令指导下做出这些决策。

核心循环：

1. 选择一个管道。
2. 运行预检。
3. 从注册表发现真实工具。
4. 向用户展示概念、工具计划、制作计划和成本。
5. 逐阶段执行，带有检查点。

## 决策沟通合约

对于任何有意义的制作决策，代理必须在行动前沟通决策。用户绝不应在事后推断选择了哪个提供商、模型或渲染路径。

### 执行前宣布

在任何付费或重要的生成调用之前，说明：

- 确切的工具名称，
- 提供商，
- 模型或提供商变体，
- 选择它的原因，
- 是样品运行还是批量运行。

### 重大变更前询问

代理必须在更改任何重大制作选择之前询问用户，包括：

- 切换提供商，
- 切换模型系列或提供商变体，
- 从视频主导切换到静态图像主导的处理方式，
- 当改变输出特性时切换合成引擎，
- 放弃旁白、音乐或其他已批准的创意元素，
- 从样品模式切换到批量模式。

在已批准的提供商/模型路径内的细微提示优化不需要单独批准，除非它们实质性地改变了创意方向。

### Present Both Composition Runtimes (HARD RULE) / 同时呈现两种合成运行时

当 Remotion 和 HyperFrames 在机器上都可用时（检查 `video_compose.get_info()["render_engines"]`），代理**必须向用户呈现两个选项**，然后在提案阶段锁定 `render_runtime`。代理可以推荐其中一个并提供理由——但即使管道清单或导演技能建议了一个，也禁止默默选择"默认"。

Never silently choose a default composition runtime when both are available.

呈现内容必须包括每个运行时的以下信息：

1. 一句通俗语言描述它**对于这个特定需求**最擅长什么。
2. 一句诚实的权衡说明（为什么它可能不是这里的最佳选择）。
3. 代理的推荐及其理由，与需求的 delivery_promise 和视觉方法相关联。

然后等待用户明确批准后再继续。将完整的备选列表——两个运行时加上任何适用的"ffmpeg"选项——记录为 `decision_log` 中 `render_runtime_selection` 决策的 `options_considered`。当两者都可用时，决策日志条目中只考虑了一个运行时，这是一个**关键**审查发现。

例外：如果机器上只有一个运行时可用，代理可以使用它继续，但必须明确说明（"这台机器上没有安装 HyperFrames；我将使用 Remotion 继续。如果你想要替代方案，请安装 HyperFrames。"）。`render_runtime_selection` 决策仍然将不可用的选项记录为 `rejected_because: "runtime not available on this machine"`。

此规则适用于每个调用 `video_compose` 的管道——不仅仅是 Wave 1。管道的导演技能可能推荐一个运行时，但该推荐是与用户对话的输入，而不是决策。

### 合成创作模式 — 模板化 vs 定制工坊

与*运行时*正交的是*创作模式*：**如何**构建合成。将其作为独立的提案决策呈现，并记录在 `decision_log` 中（`category: "composition_mode"`）。

- **模板化** — 将标准的 `cut.type` 场景类型（`text_card`, `stat_card`, `bar_chart`, …）组装到 `Explainer`/`CinematicRenderer` 合成中。快速、廉价、可靠——也是大多数视频看起来相似的原因。适合批量输出、本地化变体、快速草稿和低风险的内部片段。
- **定制工坊** — **从头手写合成**：定制场景、一次性主题和为这个作品编写的运动，通过 `composition_mode: "atelier"` 渲染（参见 `video_compose` → `_render_via_atelier`）。没有可复用的创意组件；每次都是全新的视觉语言。

**对于重要作品默认使用定制工坊** — 营销、发布、品牌宣传片、任何必须让人印象深刻的单次交付解说视频。决定规则：*复用引擎知识，绝不复用创意组件。* 在定制工坊模式下，标准场景类型目录、`hyperframes-registry` 块、固定装置和完成组件是**禁止使用的**——它们是冻结的外观，会重新引入同质化。在构建之前，通过 **`skills/meta/bespoke-composition.md`** 路由，其顺序为：艺术指导（`visual-style`）→ 运动原理（通过 `framer-motion`/`lottie-bodymovin` 的迪士尼12原则）→ 引擎机制（`remotion-best-practices` + 标准组件*仅作为机制法典阅读*）→ 通过定制工坊路径渲染。以**独特性审查**结束：*这可能是任何其他产品的视频吗？它是否复用了我以前做过的外观？*——与"是否匹配参考"相反。定制工坊比模板化消耗更多令牌和迭代；在提案时说明，让用户知情选择。

### 明确上报阻塞问题

当出现阻塞时，代理必须立即按照以下结构上报：

1. 尝试了什么
2. 什么失败了
3. 问题是认证、提供商访问、工具错误还是提示词/设计质量
4. 接下来有什么选项
5. 代理推荐哪个选项，附带理由

在用户批准之前，不要使用替代路径继续。

### 推荐风格

当要求用户做出选择时，不要仅仅列出选项。代理应：

- 提供备选清单，
- 简要解释权衡，
- 推荐一个选项，
- 等待批准后再继续。

### 不得单方面替换

如果批准的路径被阻塞，代理可以调查并准备替代方案，但未经用户批准不得执行这些替代方案。

这尤其适用于：

- 提供商切换，
- 模型切换，
- 回退工具，
- 仅提示词替代参考驱动生成，
- 用静态图像动态分镜替代真实动态。

## 编排器

代理本身编排制作状态机：

`research -> proposal -> script -> scene_plan -> assets -> edit -> compose`

代理：

1. 读取管道清单（`pipeline_defs/*.yaml`）以了解流程
2. 调用 `checkpoint.get_next_stage()` 以找到从哪里恢复
3. 读取阶段的导演技能（`skills/pipelines/<pipeline>/<stage>-director.md`）以了解如何执行
4. 使用工具（`tools/`）实现具体能力
5. 使用审查者元技能（`skills/meta/reviewer.md`）进行自我审查
6. 通过检查点协议（`skills/meta/checkpoint-protocol.md`）设置检查点
7. 当 `human_approval_default: true` 时提交给人工审批

基础设施文件：

- `lib/checkpoint.py` — 读写检查点，阶段验证
- `tools/cost_tracker.py` — 预算治理
- `lib/pipeline_loader.py` — 清单加载和辅助工具

## 项目目录约定

每次制作运行都会在 `projects/` 下创建一个项目工作区。此目录被 gitignore——所有生成的资产都是可重新生成的。

```
projects/<project-name>/
├── artifacts/          # 每个阶段的 JSON 产物（research_brief, script, scene_plan 等）
├── assets/
│   ├── images/         # 生成的图像（PNG）
│   ├── video/          # 生成的视频片段（MP4）
│   ├── audio/          # 旁白片段 + 最终混音（MP3/WAV）
│   ├── music/          # 背景音乐曲目（MP3）
│   └── subtitles.srt   # 生成的字幕
└── renders/
    └── final.mp4       # 最终渲染视频（交付物）
```

**命名约定**：使用从视频标题派生的 kebab-case（例如 `hidden-math-of-nature`、`how-music-rewires-brain`）。

在管道初始化时创建项目目录，在任何阶段运行之前。所有工具和代理应将输出写入这些路径——绝不写入仓库根目录或临时位置。

## 音乐库

用户可以将免版税音乐曲目放入 `music_library/`（gitignore）。资产导演将在回退到基于 API 的音乐生成之前检查此文件夹。

```
music_library/
├── ambient_track.mp3
├── cinematic_epic.mp3
└── ...
```

如果该文件夹有曲目，提案和资产阶段应将它们作为选项与生成的音乐一起呈现。详情请参见提案导演和资产导演技能。

## 可用管道

| 管道 | 最佳用途 | 稳定性 |
|----------|----------|-----------|
| `animated-explainer` | 主题到完整生成的解说视频 | 生产就绪 |
| `talking-head` | 基于素材的演讲者视频 | 测试版 |
| `screen-demo` | 屏幕录制和操作演示 | 生产就绪 |
| `clip-factory` | 从一个长源提取多个片段 | 测试版 |
| `podcast-repurpose` | 播客精彩片段和衍生内容 | 测试版 |
| `cinematic` | 预告片、宣传片和情绪主导的剪辑 | 生产就绪 |
| `documentary-montage` | 真实素材检索与主题纪录片蒙太奇 | 测试版 |
| `animation` | 动态图形和动画优先的视频 | 生产就绪 |
| `character-animation` | 本地骨骼卡通角色和可复用的角色表演 | 测试版 |
| `hybrid` | 源素材加辅助视觉内容 | 生产就绪 |
| `avatar-spokesperson` | 主持人主导的虚拟形象或唇同步视频 | 生产就绪 |
| `localization-dub` | 字幕、配音和翻译变体 | 测试版 |
| `framework-smoke` | 测试：最小化2阶段冒烟测试 | 测试 |

> **测试版管道**尚未经过全面审计。它们可以工作，但可能存在粗糙之处。当用户选择时请提及这一点。

## 强制预检

在任何创意工作之前执行此操作。**首先使用 `provider_menu_summary()`——它是面向人类的汇总报告。** 原始的 `support_envelope()` 转储是信息洪流（在配置良好的机器上可能是数兆字节的 JSON）；将其粘贴到聊天中会淹没用户。

```bash
python -c "
from tools.tool_registry import registry
import json
registry.discover()
print(json.dumps(registry.provider_menu_summary(), indent=2))
"
```

汇总返回四个字段，代理应将其翻译成通俗语言：

- `composition_runtimes` — `ffmpeg`, `remotion`, `hyperframes` 的布尔值。这是"同时呈现两种合成运行时（硬性规则）"检查的真实来源。
- `capabilities[]` — 每个能力系列一个条目，包含 `configured / total` 计数和提供商列表。为"已配置 N/M"菜单做好了准备。
- `setup_offers[]` — 安装只需1分钟环境变量修复的不可用工具。在提供升级时优先展示这些。
- `runtime_warnings[]` — 具体信号，如"hyperframes: npm package not resolvable"。逐字向用户展示这些——它们是那种破坏治理合约的静默失败错误。

然后，进行更深层次的检查（仅在汇总不够时）：

```bash
# 完整菜单——按能力分组显示可用/不可用。
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"

# 原始信封——每个工具的完整合约。较慢/信息量大；仅用于调试。
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
```

然后：

1. 读取 `pipeline_defs/` 中选定的清单。
2. 检查每个 `required_tools` 条目是否在注册表中。
3. 检查 `fallback_tools` 以了解不可用的工具。
4. 报告以下之一：`passed`、`degraded` 或 `blocked`。
5. 在用户了解真实能力范围之前，不要开始制作。

### 提供商菜单（预检强制）

已通过上面的 `provider_menu_summary()` 获取。读取该输出并**将其作为能力菜单呈现给用户**，而不是作为扁平的工具列表。仅当需要汇总所折叠的每个工具详细信息时，才直接使用 `provider_menu()`。

**如何呈现：**

```
你的能力

  视频生成：  0/13 已配置
  图像生成：  1/7 已配置
  文本转语音：    1/3 已配置
  音乐生成：  1/1 已配置
  合成：       3/3 已配置（FFmpeg, video_stitch, video_trimmer）

  你现在可以使用图像 + TTS + FFmpeg 制作视频。
  快速升级可用 — 见下方。
```

对于每个存在不可用提供商的能力，从菜单输出中读取 `install_instructions` 字段，并按工作量分组呈现设置选项：

```
快速设置选项（每个1分钟 — 在 .env 中设置环境变量）

  视频生成（0/13 -> 解锁最大升级）：
    每个不可用提供商列出自己的 install_instructions。
    从 provider_menu 输出中读取它们，并按环境变量分组呈现。
   

  图像生成（1/7 -> 更多样式选项）：
    相同模式 — 从每个不可用工具读取 install_instructions。

  文本转语音（1/3）：
    相同模式。

本地选项（免费，需要硬件）：
  runtime=LOCAL 或 runtime=LOCAL_GPU 的工具 — 从菜单读取。

已可用：
  列出正在工作的内容。用户应该对自己拥有的感到满意。
```

**规则：**
- 不要在你的提示词中硬编码提供商名称、API 密钥名称或设置 URL。
  从注册表中每个工具的 `install_instructions` 字段读取它们。
- 始终显示比例："已配置 X/Y"——这让广度可见。
- 按能力分组，而不是按单个工具分组。
- 显示他们现在**可以**做什么，然后他们**可能解锁**什么。
- 如果用户拒绝设置，继续使用最佳可用路径——不要纠缠。
- 如果一个工具与其他工具共享环境变量，将它们分组（从 `dependencies` 字段读取）。

### 设置提供协议

当工具为 `UNAVAILABLE` 但可以通过简单配置修复时，**主动提供设置帮助，而不是默默绕过限制。** 许多工具只差一个环境变量就能工作。

| 修复复杂度 | 操作 |
|----------------|--------|
| **1分钟修复**（环境变量） | 主动帮助立即配置 — 从工具读取 `install_instructions` |
| **5分钟修复**（安装） | 解释要安装什么以及为什么 — 从工具读取 `install_instructions` |
| **复杂修复**（GPU、模型下载） | 记录限制，解释它会解锁什么，然后继续 |

**规则：**
- 始终告诉用户他们缺少什么以及会获得什么
- 显示成本差异（免费本地 vs. 付费 API）
- 如果用户拒绝设置，继续使用最佳可用路径——不要纠缠
- 对相关修复进行分组（共享相同环境变量依赖的工具）

### 合成运行时（video_compose 内部）

`video_compose` 有**三个**渲染引擎/运行时。它们是并行的，不分级——选择在提案时做出并锁定在 `edit_decisions.render_runtime` 中。检查哪些可用：

```bash
python -c "
from tools.tool_registry import registry
registry.discover()
info = registry._tools['video_compose'].get_info()
print('Render engines:', info.get('render_engines'))
print('Remotion note:', info.get('remotion_note'))
print('HyperFrames note:', info.get('hyperframes_note'))
"
```

| 引擎 | 用途 | 要求 |
|--------|----------|----------|
| **FFmpeg** | 纯视频剪辑、拼接、裁剪、字幕嵌入 | `ffmpeg` 二进制文件（始终可用） |
| **Remotion** | 基于 React 的合成：静态图像 → 动画视频、文本卡片、统计卡片、图表、标注、对比、弹簧物理过渡、逐字字幕嵌入、TalkingHead 虚拟形象 | Node.js（`npx`）+ `remotion-composer/` + `node_modules` |
| **HyperFrames** | HTML/CSS/GSAP 合成：动态排版、产品宣传、发布短片、网站转视频、注册表块驱动场景、SVG 角色骨架 | Node.js ≥ 22 + FFmpeg + `npx`（通过 `npx hyperframes` 使用） |

`render_runtime` **在提案时锁定**（`proposal_packet.production_plan.render_runtime`）并**在 edit_decisions 中保持不变**。`video_compose` 根据此字段路由；禁止静默切换运行时。如果所选运行时在合成时变得不可用，按照上面"明确上报阻塞问题"的方式上报结构化阻塞。参见 `skills/core/hyperframes.md` 了解 Remotion 与 HyperFrames 的决策矩阵。

### 关键规则：需要动态效果的请求

对于交付物本质上依赖动态效果而非静态画面的任何请求，将动态效果视为硬性要求。示例：

- 科幻预告片，
- 由生成片段构建的电影级预告短片，
- 热场剪辑，
- 虚拟形象或代理视频，
- 任何承诺依赖于运动镜头而非静态帧的需求。

对于这些请求：

- 如果计划的视觉处理方案依赖于 `render_runtime`，则在提案时选择的运行时（Remotion、HyperFrames 或 FFmpeg）必须事先确认为可用。
- 禁止回退到静态图像。不要悄悄将工作转换为 Ken Burns 预告片、动态分镜或基于幻灯片的视频。
- 当它将已批准的交付物从动态主导视频变为静态主导视频时，禁止仅回退到 FFmpeg。
- **禁止静默切换运行时。** 如果 `render_runtime="hyperframes"` 已锁定且 HyperFrames 不可用，不要路由到 Remotion。上报阻塞问题，提出选项，获取用户批准，记录 `render_runtime_selection` 决策——然后继续。
- 立即上报关键问题。如果所选运行时不可用、渲染失败或提供商片段生成失败从而阻塞了已批准的处理方案，停下来通知用户后再继续。
- 不要在降级输出上花费更多令牌或时间，除非用户明确批准降级为动态分镜或概念验证。

**当 Remotion 可用时**，代理应围绕它设计制作方案：
- 使用 `flat-motion-graphics` 剧本的解说视频 -> Remotion 动画场景，而不是 Ken Burns
- 数据驱动视频 -> Remotion 统计卡片和图表，而不是静态截图
- 任何使用静态图像的管道 -> Remotion 弹簧动画，而不是 FFmpeg 平移缩放
- **CLI/终端/安装流程的屏幕演示 -> `TerminalScene`（合成屏幕录制），不是操作系统级别捕获。** 参见 `.agents/skills/synthetic-screen-recording/SKILL.md`。更快、确定性强、保护隐私。仅当演示是真实应用 UI 或需要不可预测的实时行为时，才使用真实捕获（`screen_recorder`、`cap_recorder`、`playwright-recording`）。

### `remotion-composer/` 中可用的 Remotion 场景类型

参见 `remotion-composer/SCENE_TYPES.md` 获取权威列表及其剪辑模式。当前可通过 `cut.type` 使用的场景类型：
`text_card`、`stat_card`、`callout`、`comparison`、`hero_title`、`terminal_scene`、`anime_scene`、`bar_chart`、`line_chart`、`pie_chart`、`kpi_grid`、`progress_bar`。覆盖类型包括 `section_title`、`stat_reveal`、`hero_title`、`provider_chip`。

这些标准场景类型是**模板化**路径——快速可靠，但这也是视频看起来相似的原因。对于**重要作品，优先使用定制工坊模式**（手写合成）而不是这个目录；将这些类型作为*机制法典*阅读，而不是可组装的菜单。参见上面的"合成创作模式"和 `skills/meta/bespoke-composition.md`。

**当 Remotion 不可用**且 `render_runtime="remotion"` **未**锁定时，`video_compose` 可以在静态图像上使用 FFmpeg Ken Burns 运动。这仍然有效，但产生的视觉效果吸引力较低。在提案中提及这一权衡。当 `render_runtime="remotion"` **已**锁定且 Remotion 不可用时，这是一个阻塞问题——上报，不要静默切换。

当 `render_runtime="hyperframes"` 已锁定且 HyperFrames 不可用时（Node < 22、缺少 `ffmpeg`/`npx`，或 `hyperframes doctor` 报告问题），这也是一个阻塞问题。未经用户批准 + 记录的 `render_runtime_selection` 决策，不要替换为 Remotion 或 FFmpeg。

路由是自动的——`video_compose` 读取 `edit_decisions.render_runtime` 并分发到匹配的引擎（`_render_via_hyperframes`、`_remotion_render` 或 `_render_via_ffmpeg`）。但**代理必须在提案时知道 Remotion 和 HyperFrames 都存在**，以便有意识地设计视觉方法。不要对 HTML/GSAP 更自然表达的动态图形密集型概念默认使用 Remotion，也不要对复用现有 React 场景栈的需求默认使用 HyperFrames。

## 能力发现

OpenMontage 使用两层来进行能力选择：

- 选择器工具：能力级别路由，如 `tts_selector` 和 `video_selector`
- 提供商工具：通过注册表发现的、调用特定后端的实际工具

始终先检查注册表：

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_catalog(), indent=2))"
```

对于入围工具，检查：

- `capability`
- `provider`
- `usage_location`
- `supports`
- `fallback_tools`
- `related_skills`

当注册表可以回答时，不要依赖记忆或旧的文档。

## 工具系列

**不要维护硬编码的工具列表。** 始终在运行时查询注册表：

```bash
# 查看按能力分组的所有工具（TTS, video_generation, image_generation 等）
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"

# 查看按提供商分组的所有工具（elevenlabs, openai, ffmpeg 等）
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_catalog(), indent=2))"
```

在输出中查找的关键能力系列：

- **tts** — 文本转语音提供商。通过 `tts_selector` 路由。
- **video_generation** — 视频生成提供商（云端、本地 GPU、库存）。通过 `video_selector` 路由。
- **image_generation** — 图像生成提供商（云端、本地 GPU、库存）。通过 `image_selector` 路由。
- **music_generation** — 音乐和音效生成。
- **video_post** — 合成、拼接、裁剪（基于 FFmpeg，始终本地）。
- **audio_processing** — 混音、增强（基于 FFmpeg，始终本地）。
- **analysis** — 转录、场景检测、帧采样。
- **avatar** — 虚拟形象和唇同步生成。
- **character_animation** — 本地角色规格、SVG 骨架、姿势库、动作时间线、预览和 QA。
- **enhancement** — 放大、背景移除、人脸增强、调色。

注册表中的每个工具都声明了 `best_for`、`install_instructions`、`runtime`（LOCAL、API、LOCAL_GPU、HYBRID）和 `status`。读取这些字段——不要凭记忆假设工具的优势。

### 工具类命名约定

所有工具类使用**不带"Tool"后缀的大驼峰命名（PascalCase）**。在 Python 中导入工具时：

| 模块 | 类名 | 错误示例 |
|--------|-----------|-----|
| `tools.audio.music_gen` | `MusicGen` | ~~MusicGenTool~~ |
| `tools.video.video_compose` | `VideoCompose` | ~~VideoComposeTool~~ |
| `tools.audio.audio_mixer` | `AudioMixer` | ~~AudioMixerTool~~ |
| `tools.tts.elevenlabs_tts` | `ElevenLabsTTS` | ~~ElevenLabsTTSTool~~ |
| `tools.analysis.transcriber` | `Transcriber` | ~~TranscriberTool~~ |
| `tools.subtitle.subtitle_gen` | `SubtitleGen` | ~~SubtitleGenTool~~ |

如有疑问，请检查：`grep "^class " tools/<path>.py`

所有工具通过 `.execute(params_dict)` 调用（返回包含 `.success`、`.data`、`.error` 的 `ToolResult`），而不是 `.run()`。

### 选择器模式

三个选择器工具抽象了多提供商能力。**选择器从注册表自动发现提供商。** 添加新的提供商工具会自动使其通过选择器可用——无需更改选择器代码。

| 选择器 | 路由到 | 发现方式 |
|----------|-----------|-----------------|
| `tts_selector` | 所有 `capability="tts"` 的工具（ElevenLabs, Google TTS, OpenAI, Piper） | `registry.get_by_capability("tts")` |
| `image_selector` | 所有 `capability="image_generation"` 的工具（FLUX, Google Imagen, DALL-E, Recraft 等） | `registry.get_by_capability("image_generation")` |
| `video_selector` | 所有 `capability="video_generation"` 的工具 | `registry.get_by_capability("video_generation")` |

选择器根据以下规则路由：用户偏好 > 可用性 > 发现顺序。它们在提供商之间透明地适配输入模式。

### 文生图默认模型（硬性规则）

视频制作流程中的所有纯文生图请求必须通过 `image_selector`，默认使用 `preferred_provider="local_diffusion"`；该工具内部默认基础模型为 `black-forest-labs/FLUX.1-schnell`。用户明确指定其他提供商、`allowed_providers`、图像编辑输入或自定义 ComfyUI 工作流时，可以覆盖这个默认值。

**人物角色参考图例外：** 人物三/四视图必须使用 `character_ref_sheet`，默认并锁定本地 `black-forest-labs/FLUX.2-dev`。该工具按“`front_only` 正面 T2I 与人工确认 → `complete_from_front` 正面参考驱动的侧面/背面/半身 → 1280×720 本地拼接”执行，并在内部逐张通过 `image_selector → local_diffusion`。只有用户明确批准跳过正面检查时才使用 `operation="full"`。不得退回 FLUX.1 Schnell/Dev，也不得让模型一次性生成四栏组合图。

如果本地 FLUX 依赖、基础模型或 LoRA 不可用，不要静默切换到其他图像生成提供商。应上报阻塞并提示安装或确认模型下载；只有用户明确批准后才传递 `allow_model_download=true`。图库搜索（Pexels/Pixabay）、`diagram_gen`、`code_snippet`、Manim 和合成引擎原生图形不属于文生图，不受此默认值约束。

## 面向用户的规划协议

在承诺执行之前，呈现：

1. 当需求仍开放时，提供 `4-5` 个概念方向。
2. 推荐的管道。
3. 推荐的工具路径。
4. 实际可用的替代工具路径。
5. 成本估算和质量权衡。
6. **音乐计划**——每个有音频的管道都必须提供。见下方。
7. 按阶段划分的制作计划。
8. 资产生成前的审批关卡。

如果用户偏好特定供应商且该工具可用，直接展示出来。不要隐藏提供商选择。

### 音乐计划（强制）

音乐是任何视频的关键部分。**在提案/构思阶段就向用户说明音乐情况**——不要默默推迟到资产阶段，那时失败成本会很高。

按此顺序检查音乐可用性并呈现选项：

1. **用户音乐库（`music_library/`）：** 检查此文件夹是否存在且包含曲目。如果是，列出可用曲目及时长，让用户选择一个。
2. **音乐生成 API：** 检查通过注册表（`registry.get_by_capability("music_generation")`）哪些音乐工具可用。如实报告其状态——如果知道配额状态也一并说明。
3. **免版税来源：** 说明用户是否可以提供自己的曲目（例如来自 YouTube Audio Library、Jamendo 或其他免费来源）。提供 `music_library/` 放置路径。

**始终向用户提供明确的选择：**
- 使用他们库中的曲目（哪一首？）
- 提供不同的曲目（放入 `music_library/`）
- 通过 API 生成一个（如果可用——说明提供商和成本）
- 在没有音乐的情况下继续

**如果没有音乐来源可用：** 明确告知用户。不要让这个问题在资产阶段才意外出现。

将音乐决策记录在提案/需求产物中，以便资产导演知道该怎么做。

## 管道资产预期

每个管道清单的 `tools_available` 字段声明了一个阶段可以使用的工具。对于多提供商能力使用选择器——选择器处理到任何可用提供商的路由。阅读管道清单获取每个阶段的权威列表。

## 阶段代理

每个阶段产生一个规范产物，成为下一阶段的合约。阶段导演技能教代理如何生成它。

| 阶段 | 导演技能 | 规范输出 | 核心质量标准 |
|------|---------------|------------------|------------------|
| `idea` | `*-director.md` | `brief` | 清晰的主题、目标平台、时长、基调和用户意图 |
| `script` | `*-director.md` | `script` | 结构化章节、有效的时间安排、连贯的旁白 |
| `scene_plan` | `*-director.md` | `scene_plan` | 有序的场景、时间安排、资产需求 |
| `assets` | `*-director.md` | `asset_manifest` | 来源、路径、模型/工具元数据、场景关联 |
| `edit` | `*-director.md` | `edit_decisions` | 具体的剪辑、叠加、字幕/音乐决策 |
| `compose` | `*-director.md` | `render_report` | 输出路径、编码配置、验证说明 |

阶段合约规则：

- 已完成或等待人工的检查点必须包含该阶段的规范产物。
- 规范产物必须通过 `schemas/artifacts/` 中 JSON 模式的验证。
- 非规范输出（如媒体文件）属于阶段特定目录。
- 工具应记录种子/模型版本以确保可重现性。

## 审查者协议

审查者是一个元技能（`skills/meta/reviewer.md`）——建议性质，从不直接阻止进程。

- 在每个阶段执行后、设置检查点前进行自我审查。
- 从当前阶段的管道清单加载 `review_focus` 项。
- 最多两轮审查。之后，带着警告通过并继续前进。
- 发现分类：关键（必须修复）、建议（应修复）、细枝末节（有则更好）。
- 关键发现 -> 修复并重新审查。建议 -> 记录并继续。
- 将剧本 `quality_rules` 视为约束，而非建议。

## 人工检查点协议

检查点协议元技能（`skills/meta/checkpoint-protocol.md`）教代理何时暂停：

- 从每个阶段的管道清单读取 `human_approval_default`
- 创意阶段（`idea`、`script`、`scene_plan`）通常需要批准
- 技术阶段（`assets`、`edit`、`compose`）通常自动继续
- 当需要批准时：呈现产物摘要、审查发现和成本快照
- 等待人工批准、请求修改或中止

## 通信协议

代理通过规范的 JSON 产物、检查点、管道清单和工具注册表进行协调。

主要文件：

- 产物模式：`schemas/artifacts/`
- 检查点模式：`schemas/checkpoints/checkpoint.schema.json`
- 管道清单模式：`schemas/pipelines/pipeline_manifest.schema.json`
- 管道清单：`pipeline_defs/`
- 风格剧本：`styles/*.yaml`（由 `schemas/styles/playbook.schema.json` 验证）
- 工具合约：`tools/base_tool.py`
- 工具注册表：`tools/tool_registry.py`
- 阶段导演技能：`skills/pipelines/<pipeline>/<stage>-director.md`
- 元技能：`skills/meta/*.md`

检查点规则：

- 检查点位于 `pipelines/<project_id>/checkpoint_<stage>.json`。
- `status` 可以是 `completed`、`failed`、`awaiting_human` 或 `in_progress`。
- `completed` 和 `awaiting_human` 检查点必须包含规范产物。
- 无效的检查点或无效的规范产物是违反合约的行为，应快速失败。

管道清单规则：

- 管道是 `pipeline_defs/` 中的声明式 YAML 清单。
- 阶段声明：`skill`（导演技能路径）、`produces`、`tools_available`、`review_focus`、`success_criteria`、`human_approval_default`。
- 添加新管道需要一个清单 + 阶段导演技能。

工具规则：

- 每个生产工具必须继承自 `BaseTool`。
- 工具发现通过注册表进行，而不是临时导入。
- 支持信封报告是能力、状态和资源需求的真实来源。

## 风格剧本

| 剧本 | 最佳用途 |
|----------|----------|
| `clean-professional` | 企业、教育、SaaS |
| `flat-motion-graphics` | 社交媒体、TikTok、创业公司 |
| `minimalist-diagram` | 技术深度解析、架构 |

## 层映射

OpenMontage 有三个指令层：

1. `tools/`
   存在什么、什么可用、成本、运行时、回退、相关技能。
2. `skills/`
   OpenMontage 希望如何在管道中使用这些工具。
3. `.agents/skills/`
   原始供应商或技术知识。

阅读顺序：

1. 注册表/工具合约 — 发现什么可用
2. 相关管道或创意技能（第2层）——了解在此上下文中如何使用
3. 底层供应商技能（第3层）——**在调用任何生成工具之前必须阅读**

**工具使用优先选择技能而非源代码。** 技能的存在正是为了让你在常见情况下不需要了解实现细节。第2层告诉你*什么*和*何时*。第3层告诉你*如何*。对于编写提示词、选择参数或理解使用模式，你应该阅读技能——而不是 `.py` 文件。

**例外：调试、审计和验证治理合约。** 当技能和工具不一致，或者某些行为与技能声称的不同时，阅读工具源代码是可以的——这通常是捕获静默可用性错误或过时文档字符串的唯一方法。拒绝查看实现的审计将恰恰错过最重要的错误。如果你确实阅读源代码进行调试，考虑该发现是否应在之后更新到技能中，这样下一个代理就不需要重复深入研究了。

**第3层不是可选的。** 每个生成工具（视频、图像、TTS、音乐）都有一个 `agent_skills` 字段列出其第3层技能。这些技能包含提供商特定的提示工程、参数调优和质量技术。在编写提示词之前阅读它们。通用提示词与了解技能的提示词之间的区别，就是"可用"与"电影级"之间的区别。

示例：在调用视频生成工具之前，阅读其 `agent_skills` → 相关技能 → 获取提供商特定的提示结构和质量关键词。

### 第3层技能，按类别分类

`.agents/skills/` 目录很大。当你不是通过工具的 `agent_skills` 指针进入时，使用此表根据*你想做什么*找到正确的文件：

| 类别 | 技能 |
|---|---|
| **合成运行时** | `remotion`, `remotion-best-practices`, `synthetic-screen-recording`（通过 Remotion TerminalScene 模拟终端/UI 演示） |
| **动画知识（通用）** | `gsap-core`, `gsap-timeline`, `gsap-plugins`（SplitText / MorphSVG / DrawSVG / MotionPath / Flip / CustomEase）, `gsap-utils`, `gsap-react`, `gsap-performance`, `gsap-scrolltrigger`, `gsap-frameworks`, `framer-motion`（迪士尼12原则）, `lottie-bodymovin`（Lottie 导出） |
| **角色动画** | `character-rigging`, `svg-character-animation`, `pose-library-design`, `canvas-procedural-animation`, `character-animation-qa` |
| **图像生成** | `bfl-api`, `flux-best-practices`, `flux-character-turnaround`（角色建模三/四视图） |
| **视频生成** | `seedance-2-0`（首选高级默认——电影级、预告片、多镜头、同步音频、唇同步）, `ai-video-gen`, `ltx2` |
| **音频** | `elevenlabs`, `music`, `sound-effects`, `acestep`, `text-to-speech`, `setup-api-key` |
| **虚拟形象/唇同步** | `avatar-video`, `heygen`, `create-video`, `faceswap`, `video-translate`, `speech-to-text`, `agents` |
| **捕获** | `playwright-recording`（浏览器流程）, `ffmpeg`（后期） |
| **可视化** | `beautiful-mermaid`, `d3-viz`, `manim-composer`, `manimce-best-practices`, `manimgl-best-practices` |
| **媒体编辑** | `video-edit`, `video-download`, `video-understand`, `video-toolkit`, `visual-style` |

**如有疑问，先阅读该类别的元路由文件：**
- 选择动画运行时？→ `skills/meta/animation-runtime-selector.md` 在 Remotion 原语、GSAP 插件、framer-motion、Lottie、Manim、D3 之间路由。
- 选择屏幕录制模式（真实捕获 vs 合成终端）？→ `pipeline_defs/screen-demo.yaml` + `skills/pipelines/screen-demo/idea-director.md`。

## 快速查询

| 问题 | 查找位置 |
|----------|---------------|
| 存在哪些工具？ | `tools/tool_registry.py` 和 `registry.support_envelope()` |
| 某个能力有哪些提供商可用？ | `registry.capability_catalog()` |
| 某个供应商有哪些工具？ | `registry.provider_catalog()` |
| 工具实际如何工作？ | 工具在注册表中的 `usage_location` |
| 这个管道阶段应该如何表现？ | `skills/pipelines/<pipeline>/...` |
| 检查点/审查策略是什么？ | `skills/meta/` |

## 禁止事项

- **不要绕过管道。** 永远不要编写临时脚本直接调用工具。所有制作都通过带有导演技能的管道阶段进行。参见第零条规则。
- **不要在未阅读其第3层技能的情况下调用生成工具。** 检查工具的 `agent_skills` 字段，阅读引用的技能，然后根据该指导编写提示词。
- **不要跳过阶段导演技能。** 在执行任何管道阶段之前，阅读其导演技能。该技能包含质量标准、工作流和审查标准。
- 不要使用已删除的旧名称，如 `tts_cloud`、`tts_engine` 或 `video_gen`。
- 不要硬编码提供商名称、API 密钥名称或设置 URL。从注册表的 `install_instructions` 和 `dependencies` 字段读取它们。
- 在用户批准制作计划之前，不要开始资产生成。
- 不要隐藏降级路径。明确记录替换和受阻选项。
- 不要孤立地呈现单个不可用工具。始终显示完整的能力图景："此能力已配置 X/Y 个提供商。"
- 不要跳过预检时的提供商菜单。用户必须看到他们拥有什么以及可能解锁什么。
- 不要在没有先告知用户并在变更实质性时获得批准的情况下更改提供商、模型或渲染路径。
