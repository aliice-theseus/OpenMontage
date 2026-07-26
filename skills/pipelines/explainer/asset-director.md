# 资产导演 — 解说片流水线

## 使用时机

你是生成式解说视频的资产制作人。你有一个带有必需资产的 `scene_plan` 和一个带有旁白文字的 `script`。你的工作是生成所需的所有资产：旁白音频、图像、图表、代码片段和背景音乐。在你完成之前，每个文件必须存在于磁盘上。

这是计划变成真实文件的地方。一个缺失或低质量的资产会使最终视频功亏一篑。

## 动画创作 — 选择哪个运行时

在为这个流水线创作任何动画化的 Remotion 组件之前，先阅读 **`skills/meta/animation-runtime-selector.md`**。它是决定使用 Remotion 原语还是 GSAP 插件的路由权威。

常见解说片需求的快速路由：

| 场景类型 | 推荐方法 |
|---|---|
| 标题卡片、淡入淡出、滑入、缩放 | Remotion 原语 — `interpolate()` + `spring()` |
| 与旁白同步的词级字幕高亮 | 现有 `CaptionOverlay` 组件（已在 `remotion-composer/src/components/` 中） |
| 逐字符动态排版（"词一个字一个字地爆炸"） | GSAP SplitText — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 4+ 补间的多步骤编排 | GSAP timeline — 阅读 `.agents/skills/gsap-timeline/SKILL.md` |
| Logo 构建（线条绘制、描边揭示） | GSAP DrawSVG — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 数据图表（柱状/折线/饼图/KPI） | Remotion 内置图表组件 — 参见 `remotion-composer/SCENE_TYPES.md` |
| 终端或 CLI 演示 | Remotion TerminalScene — 阅读 `.agents/skills/synthetic-screen-recording/SKILL.md` |

**保持简单的倾向：** 如果 Remotion 原语能在 ≤ 20 行内解决一个场景，使用它们。只有当插件真正值得其包体积时才引入 GSAP。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/asset_manifest.schema.json` | 工件验证 |
| 前置工件 | `state.artifacts["scene_plan"]["scene_plan"]`、`state.artifacts["script"]["script"]`、`state.artifacts["proposal"]["proposal_packet"]` | 要生产的内容 |
| 剧本 | 活动风格剧本 | 图像提示、图表风格、音频偏好 |
| 工具 | `tts_selector`、`image_selector`、`video_selector`、`diagram_gen`、`code_snippet`、`music_gen` — 选择器自动发现注册表中的所有可用提供者 | 生成能力 |
| 成本跟踪器 | `tools/cost_tracker.py` | 预算治理 |

### AI 视频导演技能门控

调用 `video_selector` 前读取工具返回的全部 `required_agent_skills`，其中包括画面质感与运镜导演技能。若场景包含打斗、追逐、跑酷、枪战、武侠或竞技动作，再读取 `conditional_agent_skills.action_or_combat_scene` 指向的 `.agents/skills/direct-action-scenes/SKILL.md`，然后才编写最终提示词。

### COS URL 预检门禁（硬性规则）

**视频生成阶段的所有 `reference_image_urls` 必须使用 COS 公开 URL，严禁使用本地文件系统路径。** 在调用 `video_selector` 之前，必须通过以下预检：

```python
import re

def validate_reference_urls(urls: list[str]) -> None:
    """验证所有 reference URL 均为 COS 公开 URL，拒绝本地路径。"""
    LOCAL_PATH_PATTERNS = [
        r"^[a-zA-Z]:\\",       # Windows 路径如 C:\...
        r"^/",                  # Unix 绝对路径
        r"^\.\.?",              # 相对路径 ./ 或 ../
        r"^projects/",          # 项目本地路径
    ]
    for url in urls:
        for pattern in LOCAL_PATH_PATTERNS:
            if re.match(pattern, url):
                raise ValueError(
                    f"检测到本地路径作为 reference_image_url: {url}\n"
                    f"视频生成阶段只接受 COS 公开 URL（https://...）。\n"
                    f"请确保角色图和场景草图已上传到 COS，并在产物中使用 image_url 字段。"
                )
```

这段预检在入口处拦截本地路径，防止混合了本地路径的 reference list 传入视频生成工具。

### 角色参考图 — 通过注册表获取 COS URL

如果 `character_design` 阶段已执行（有角色身份注册表），在调用 `video_selector` 生成含角色的视频片段时，通过 `CharacterRegistry.build_reference_config(require_cos_urls=True)` 获取 COS URL：

```python
from lib.character_registry import CharacterRegistry

registry = CharacterRegistry(Path(f"projects/{project_id}"))
# require_cos_urls=True 时，如果角色没有 COS URL 会主动抛 ValueError
# reference_mode="four_view" 只传四视图组合图（比单张正脸更完整的角色定义）
ref_config = registry.build_reference_config(
    character_ids=["hero"],
    require_cos_urls=True,
    reference_mode="four_view",
)
# ref_config["reference_image_urls"] 包含一个四视图组合图 URL

validate_reference_urls(ref_config["reference_image_urls"])

video_selector.execute({
    "prompt": scene_prompt,
    "operation": "text_to_video",
    "reference_image_urls": ref_config["reference_image_urls"],
    "identity_lock": ref_config["identity_lock"],
    "require_identity_lock": True,
})
```

### 场景草图参考 — 使用 image_url 字段

场景草图同样**必须**使用 `scene_sketch.scenes[i].image_url`（COS 公开 URL）而非 `image_path`（本地路径）传入 `reference_image_urls`。详见 scene-sketch-director.md 的「与资产阶段的衔接」。

```python
# 收集场景草图的 COS URL
sketch_urls = [
    scene["image_url"]
    for scene in scene_sketch["scenes"]
    if scene.get("image_url")
]

validate_reference_urls(sketch_urls)

video_selector.execute({
    "prompt": scene_prompt,
    "operation": "text_to_video",
    "reference_image_urls": sketch_urls,
    # ...
})
```

**如果 `image_url` 字段为空或缺失，不得继续生成。** 必须回退到 COS 上传补全后重试。

## 流程

### 步骤 1：盘点必需资产

遍历场景计划中的每个场景。对于每个 `required_assets` 条目，创建一个资产任务：

```
资产任务：
  scene_id: scene-3
  type: diagram
  description: "Mermaid 流程图：query -> encode -> search -> rank -> return"
  source: generate
  tool: diagram_gen
  estimated_cost: ¥0.00
```

同时为以下创建任务：
- **旁白音频** — 每个脚本章节一个（使用 `tts_selector` 或具体的 TTS 提供者）
- **背景音乐** — 整个视频一个曲目（使用 `music_gen` 或从库中选择）
- **音效** — 根据剧本的 `sfx_style`（可选，使用 `music_gen` 或素材）

### 步骤 2：检查预算

在生成任何内容之前：
1. 汇总所有资产任务的预估成本
2. 与成本跟踪器的剩余预算对比
3. 如果超预算：
   - 将昂贵的工具切换到更便宜的替代方案（使用 `tts_selector` 带 `preferred_provider` 路由到更便宜的 TTS；使用 `image_selector` 路由到更便宜的图像提供者）
   - 减少图像数量（合并类似场景）
   - 跳过可选资产（SFX、B-roll）
4. 在继续前通过成本跟踪器获取成本批准

### 步骤 2b：样本预览（防止浪费支出）

在批量生成资产之前，对每种昂贵的资产类型生成一个样本，并向用户展示以供批准：

1. **TTS 样本**：为 `script.voice_performance.sample_section_id`（当存在时）生成旁白；否则选择要求最高的章节。为用户播放。在生成其余部分之前，确认声音、节奏、停顿、强调和基调可接受。
2. **图像样本**：为最具代表性的场景生成一张图像。展示给用户。在批量生成所有图像之前，确认风格、质量和提示方法。
3. **音乐样本**（如果使用 `music_gen`）：生成一个短片。在提交前确认情绪和能量。

如果用户拒绝样本：
- 调整参数（声音、提示风格、提供者）并重新生成样本。
- 在样本批准前不要批量生成。
- 每种资产类型最多 3 次样本迭代，然后向用户升级以作决定。

此步骤通常花费 ¥0.03–0.08 总计，并防止 ¥1–3 的浪费生成。

### 步骤 3：生成旁白（仅 narration 章节）

**跳过 dialogue 章节。** 遍历脚本章节时，只处理 `section_type` 为 `"narration"` 的章节。
`section_type` 为 `"dialogue"` 的章节由步骤 4b 处理——对话语音直接嵌入 Seedance 视频生成，不使用 TTS。

对于每个 `"narration"` 章节：
1. 提取旁白文本
2. 读取 `script.voice_performance` 和章节 `delivery_cues`
3. 当存在时使用 `delivery_cues.provider_text`；否则用有目的的标点转换章节文本，仅在所选提供者支持时使用中断标签
4. 应用脚本中的说话者指示（节奏、强调、情感）
5. 应用剧本的 `audio.voice_style`
6. 将提示映射到提供者参数：
   - OpenAI：仅 `instructions` 使用 `model: "gpt-4o-mini-tts"`；使用 `response_format` 设置输出格式
   - Google TTS：使用 `<break>` 标签时 `input_type: "ssml"`，加上 `speaking_rate` 在 `0.25..2.0` 和 `pitch` 在 `-20..20`
   - ElevenLabs：`stability`、`similarity_boost`、`style`、`speed` 和 `use_speaker_boost`
7. 使用 `tts_selector` 生成 — 它根据用户偏好和可用性自动路由到最佳可用 TTS 提供者。检查注册表的 `best_for` 字段以了解每个提供者的优势。
8. 在每个旁白资产上记录应用的 `voice_performance` 元数据
9. 验证音频文件存在且时长与预期时序匹配（±15%）

**发音指南**：如果脚本包含技术术语、行话或发音不明显的名称，在 TTS 请求中包含发音映射。

**平淡声音失败：** 如果批准的声音听起来单调、机械、匆忙或忽略预期的停顿，不要批量处理剩余章节。修订 `voice_performance` 计划或提供者参数并重新生成样本。

### 步骤 3b：生成对话视频（dialogue 章节 — Seedance 原生音频）

对于每个 `section_type` 为 `"dialogue"` 的章节，使用 `video_selector`（`preferred_provider="seedance"`）生成包含角色对话的视频片段。
**不生成单独的 TTS 音频**——对话语音由 Seedance 在视频生成时原生合成，附带口型同步。

```python
for section in script["sections"]:
    if section.get("section_type") != "dialogue":
        continue

    dialogue = section["dialogue"]
    char_id = dialogue["character_id"]
    line = dialogue["line"]

    from lib.character_registry import CharacterRegistry

    registry = CharacterRegistry(Path(f"projects/{project_id}"))

    # 获取角色显示名（Seedance prompt 中使用 display_name 而非 ID）
    identity = registry.get(char_id)
    char_name = identity.display_name if identity else char_id

    # 构建 Seedance 对话提示：Character says: "..."
    prompt = f"{section['text']}\n{char_name} says: \"{line}\""
    if dialogue.get("emotion"):
        prompt += f"\n{char_name} speaks with {dialogue['emotion']} tone."

    # 角色参考图（COS URL）— 使用 four_view 模式，只传四视图组合图
    ref_config = registry.build_reference_config(
        character_ids=[char_id],
        require_cos_urls=True,
        reference_mode="four_view",
    )

    # 场景构图参考（COS URL）
    sketch_url = scene_sketch["scenes"][i].get("image_url", "")

    all_refs = ref_config["reference_image_urls"] + ([sketch_url] if sketch_url else [])
    validate_reference_urls(all_refs)  # 硬性门禁

    result = video_selector.execute({
        "prompt": prompt,
        "preferred_provider": "seedance",
        "operation": "text_to_video",
        "generate_audio": True,       # 必须开启——对话音频由 Seedance 生成
        "reference_image_urls": all_refs,
        "identity_lock": ref_config["identity_lock"],
        "require_identity_lock": True,
        "aspect_ratio": "16:9",
        "duration": str(section["end_seconds"] - section["start_seconds"]),
        "output_path": f"projects/{project_id}/assets/video/dialogue_{section['id']}.mp4",
    })
```

**关键规则：**
- `generate_audio` **必须为 True**——Seedance 同时生成视频和对话音频，口型同步到 `Character says: "..."` 中的文本
- `dialogue.line` 每行不超过 6 个词，超过会导致口型漂移
- **不生成 TTS**——该场景的 `asset_manifest` 中 `audio` 类型资产为空，`video` 资产标记 `has_native_audio: true`
- 视频片段时长约等于脚本章节的 `end_seconds - start_seconds`
- 角色参考图通过 `CharacterRegistry.build_reference_config(require_cos_urls=True)` 获取，该函数无 COS URL 时会抛错

### 步骤 4：生成视觉资产

按工具分组处理资产任务以提高效率：

> **⚠️ 视频生成（video_selector）硬性前置校验：**
> 在调用 `video_selector` 之前，必须调用本文档上方的 `validate_reference_urls()` 对所有 `reference_image_urls` 做校验。
> 任何本地路径（`C:\...`、`/home/...`、`./...`、`projects/...`）都会触发 `ValueError` 并阻止调用。
> 这是硬性门禁，禁止绕过。

**图像（`image_selector`）：**
1. 从场景的实际目的构建提示：
   - 来自 `shot_language`、`shot_intent` 和 `texture_keywords` 的场景特定镜头/光线/质感提示
   - 来自剧本或自定义身份的改编视觉锚点
   - 具体的主体/动作/环境
   在有用时使用 `lib/shot_prompt_builder.py`。
2. 从剧本添加负面提示
3. 包含一致性锚点（相同角色/世界/调色板家族），但不要为每个图像重复使用完全相同的措辞
4. 生成并验证文件存在
5. 如果结果不匹配预期，完善提示并重新生成（最多 2 次重试）

**图表（`diagram_gen`）：**
1. 将场景描述转换为有效的 Mermaid 语法
2. 应用剧本的 `asset_generation.diagram_style`
3. 生成 SVG/PNG
4. 验证所有节点和边都存在

**代码片段（`code_snippet`）：**
1. 从场景描述中提取语言和代码
2. 应用来自剧本叠加样式的语法高亮主题
3. 生成高亮图像或 Remotion 兼容的数据

### 步骤 5：生成音乐

1. 读取剧本的 `audio.music_mood` 和 `audio.music_volume`
2. 检查来自 `proposal_packet.production_plan.music_source` 的音乐决策（由提案导演设置）
3. 按此优先级顺序获取背景曲目：
   - **用户选择的库曲目**：如果提案指定了来自 `music_library/` 的曲目，复制到 `projects/<project>/assets/music/background_music.mp3`
   - **用户音乐库（`music_library/`）**：如果文件夹存在且有曲目，选择与剧本 `audio.music_mood` 最匹配的。按文件名列出候选并让 EP 决定。
   - **音乐生成 API**：如果可用，使用 `music_gen`（ElevenLabs）或 `suno_music`。首先通过注册表检查状态 — 如果工具不可用或配额已耗尽，立即跳过（不要尝试并悄悄失败）。
   - **没有可用音乐**：在资产清单中明确记录为 `"music_status": "unavailable"` 并附原因。不要悄悄生成没有音乐的视频 — EP 和用户应该知道。
4. 时长应至少与总视频时长一样长。如果更短，合成阶段可以循环。
5. 验证音频文件存在于 `projects/<project>/assets/music/background_music.mp3`

**关键：** 如果音乐生成失败或不可用，立即在资产清单中报告 — 不要将问题推迟到合成阶段。

### 步骤 6：构建资产清单

将所有生成的资产组装到清单中：

```json
{
  "version": "1.0",
  "assets": [
    {
      "id": "narration-s1",
      "type": "audio",
      "subtype": "narration",
      "path": "assets/narration/s1.mp3",
      "source_tool": "tts_selector",
      "scene_id": "scene-1",
      "duration_seconds": 8.2,
      "cost_usd": 0.003
    },
    {
      "id": "img-scene-3",
      "type": "image",
      "path": "assets/images/scene-3-diagram.png",
      "source_tool": "diagram_gen",
      "scene_id": "scene-3",
      "cost_usd": 0.00
    },
    {
      "id": "music-bg",
      "type": "audio",
      "subtype": "music",
      "path": "assets/music/background.mp3",
      "source_tool": "music_gen",
      "duration_seconds": 62,
      "cost_usd": 0.05
    }
  ],
  "total_cost_usd": 0.053,
  "generation_summary": {
    "narration_sections": 5,
    "images_generated": 8,
    "diagrams_generated": 2,
    "music_tracks": 1
  }
}
```

### 生成提示的前/后自我审查

> 在向任何生成工具发送提示之前 — `image_selector`、`diagram_gen`、`video_selector`，甚至 `code_snippet` 样式提示 — 运行一个三步自我审查，基于 CHAI 监督循环（"Building a Precise Video Language with Human-AI Oversight"，arXiv 2604.21718v2）。成本很小（没有额外的工具调用）；收益很大（避免浪费的生成）。这同样适用于 `diagram_gen` Mermaid 提示和 `image_selector` 插图提示，就像适用于视频生成一样 — 不好的解说片视觉以相同的方式失败：缺少主体、缺少构图、模糊的"让它看起来有教育意义"。
>
> **步骤 1 — 前说明阶段。** 写出你今天会写的提示。不要过度编辑；目标是完整的初稿。
>
> **步骤 2 — 批评阶段。** 对照 5 方面检查清单（主体 / 主体运动 / 场景 / 空间构图 / 镜头）为草稿评分。对于每个方面：
> - 是否指定？如果没有，省略是有意的（例如"镜头 N/A — Remotion 原生场景"、"无主体运动 — 静态图表"）还是偶然的？
> - 易混淆的术语是否已消歧？（dolly vs zoom、pan vs truck、鸟瞰 vs 航拍、鱼眼 vs 桶形、全景 vs 特写；对于图表：流程图 vs 时序图 vs 状态图、从上到下 vs 从左到右）
> - 情感形容词（"干净"、"专业"、"现代"）是否已被替换为它们的视觉原因（无衬线字体、宽敞留白、单色调色板带一个强调色）？
> - 对于多镜头提示：身份是否逐字锚定？对于在多个场景中出现的 `image_selector` 提示（角色或世界），一致性锚点是否逐字指定？
>
> **步骤 3 — 后说明阶段。** 重写，填补缺失的方面，修复易混淆的术语，替换主观语言。后说明是发送到生成工具的内容。
>
> 在资产元数据中记录（前、批评、后）三元组以保持可追溯性。这反映了 CHAI 工作流，并创建了审查者可以审计的记录。

### 步骤 7：验证所有资产

**存在性检查：**
- [ ] 每个资产 `path` 在磁盘上存在
- [ ] 每个旁白章节有对应的音频文件
- [ ] 每个带有 `required_assets` 的场景已生成所有资产
- [ ] 背景音乐文件存在

**质量检查：**
- [ ] 旁白时长在预期时序的 ±15% 以内
- [ ] 旁白资产记录 `voice_performance.delivery_cues_applied`
- [ ] 批准的 TTS 样本使用与批量相同的提供者、声音和表现力设置
- [ ] 图像匹配剧本风格（审查一致性锚点）
- [ ] 图表清晰可读且完整
- [ ] 总成本在预算内

### 步骤 8：自我评估

评分（1-5）：

| 标准 | 问题 |
|-----------|----------|
| **完整性** | 每个场景是否都有所有必需的资产？ |
| **音频质量** | 旁白听起来自然且节奏正确吗？ |
| **视觉一致性** | 所有图像看起来是否属于同一个视频？ |
| **预算遵守** | 总成本是否在批准的预算内？ |
| **剧本忠实度** | 资产是否匹配剧本的风格指南？ |

如果任何维度得分低于 3，在继续前修复。

### 步骤 9：提交

对照模式验证 asset_manifest 并通过检查点持久化。

### 制作中的事实验证

如果在资产生成过程中遇到不确定性：
- 使用 `web_search` 验证主体的视觉准确性（例如这个建筑实际看起来像什么？）
- 在生成插图前使用 `web_search` 查找参考图像
- 在决策日志中记录验证：`category="visual_accuracy_check"`

视觉准确性很重要。如果脚本提到了一个特定的地点、人或物体，在生成图像之前验证它的实际外观。不要依赖 AI 模型的训练数据 — 它可能错误或过时。

## 常见陷阱

- **在检查预算之前生成**：始终先估算总成本。一个 60 秒的视频带 15 张图像可以快速烧掉 ¥3+。
- **不一致的图像风格**：每个 image_selector 调用是独立的。使用一致的锚点，但根据场景调整。如果你将相同的风格前缀粘贴到每个提示中，视频会感觉机器制作和重复。
- **忽略旁白计时**：如果 TTS 为一个 10 秒的章节产生 12 秒的音频，剪辑阶段将很困难。检查时长。
- **忽略交付提示**：当 `provider_text` 或 `delivery_cues` 存在时生成原始脚本文本会使朗读平淡。先应用声音表现合同。
- **缺少发音指南**："PostgreSQL"或"Kubernetes"在没有明确指导的情况下会被读错。
- **一次重试就放弃**：如果图像不匹配，具体地完善提示 — 不要只是重试相同的提示。
- **AI 生成带有确凿文字的图像（CTA、商号、联系方式）**：AI 图像模型经常幻觉错误的文字 — 错误的商号、错误的电话号码、拼写错误的词。**永远不要对需要逐字准确的文字场景使用 AI 图像生成。** 改用 Remotion `text_card` 类型。这适用于：CTA 屏幕、带有商号的标题卡、联系方式叠加、法律声明。如果场景在场景计划中的 `type` 是 `text_card`，不要为它生成图像 — 跳过它，让合成阶段在 Remotion 中原生渲染。

## 当你不确定时

如果你遇到不熟悉的生成技术、提供者行为或提示模式：

1. **搜索网络**了解当前最佳实践 — 模型和 API 频繁变化，代理的训练数据可能过时
2. **检查 `.agents/skills/`** 是否有现有的第 3 层知识（提供者特定提示指南、API 模式）
3. **如果两者都不行**，在 `projects/<project-name>/skills/<name>.md` 编写项目范围的技能，记录你学到的内容
4. **在技能中引用来源 URL**，使知识可追溯
5. **在决策日志中记录**：`category: "capability_extension"`、`subject: "learned technique: <name>"`

这对以下方面尤其重要：
- **视频生成提示** — 模型响应特定的词汇，这些词汇随每个版本变化
- **图像模型参数** — FLUX、DALL-E、Imagen 的最佳设置各不相同且不断演变
- **音频提供者特性** — 声音克隆、音乐生成和 TTS 各有模型特定的最佳实践
- **Remotion 组件模式** — 随着框架发展，新的合成技术不断涌现

不要依赖过时的知识。有疑问时，先搜索。
