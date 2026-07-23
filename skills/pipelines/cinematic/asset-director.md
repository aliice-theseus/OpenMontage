# 资产导演 - 电影化流水线

## 适用场景

此阶段为最终的电影化剪辑准备可用媒体：源素材精选、标题卡片资产、可选的支持插片、音乐、环境音，以及需要时的字幕资产。

## 电影化标题和叠加层的动画创作

在创作标题卡片、名牌或 SVG 叠加层之前，阅读 **`skills/meta/animation-runtime-selector.md`** 了解运行时路由。电影化作品依赖于少数高工艺的运动模式：

| 电影化需求 | 推荐方法 |
|---|---|
| 带有微妙揭示效果的主标题 | Remotion `HeroTitle` 组件（已有） |
| Logo 构建 / SVG 上的电影化动态标 | GSAP DrawSVG + MotionPath — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 在宽阔静止画面或叠加层上的曲线摄影机运动 | GSAP MotionPath — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 逐字标题揭示效果（高端/预告片风格） | GSAP SplitText — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 电影化缓动（Unreal 风格、顿挫感、加权） | GSAP CustomEase / EasePack — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 带有弹性稳定的名牌下三分之一 | Remotion `spring()` 通常足够；如果需要顿挫感用 GSAP CustomEase |
| 胶片颗粒 / 粒子叠加层 | Remotion `ParticleOverlay`（已有） |
| 调色 / LUT | `tools/enhancement/color_grade.py`（非动画范畴） |

**电影化是 GSAP 最常展现其价值的地方**——这种风格奖励精心制作的缓动和精确的曲线运动，而原始的 `interpolate()` 难以清晰地表达这些效果。但也不要过度使用：对于淡入标题，Remotion 的 `spring()` 仍然胜过引入整个 GSAP 依赖。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/asset_manifest.schema.json` | 制品验证 |
| 前置产物 | `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]`, `state.artifacts["proposal"]["proposal_packet"]` | 场景意图和节拍计划 |
| 工具 | `subtitle_gen`, `audio_enhance`, `image_selector`, `video_selector`, `pixabay_music`（免费，默认）, `freesound_music`（免费）, `music_gen`（ElevenLabs，付费）— 选择器自动发现注册表中所有可用的提供商。**在求助于 `music_gen` 之前，默认使用 `pixabay_music`。** | 可选的支持资产创建 |
| 手册 | 当前风格手册 | 品牌和排版一致性 |

### AI 视频导演技能门控

调用 `video_selector` 生成支持镜头前，读取工具返回的全部 `required_agent_skills`，先完成画面质感和运镜设计。若镜头属于打斗、追逐、跑酷、枪战、武侠或竞技动作，再读取 `conditional_agent_skills.action_or_combat_scene` 指向的 `direct-action-scenes`。这些模型无关导演决策完成后，再应用提供商特定技能。

## 流程

### 1. 优先处理源素材精选

从以下开始：

- 源视频素材精选，
- 静止图像，
- 标题卡片背景，
- 任何已批准的已提供音乐或环境基底。

这些是主要材料。其他一切都是支持性的。

如果 `proposal_packet.metadata.motion_required = true`，则实际的运动素材或生成的视频片段是强制性的。在这种情况下：

- 静止图像只能作为较大动态合成中的参考材料或背景元素使用，
- 静止图像不得替换计划中的运动镜头，
- 除非用户明确批准动态分镜（animatic），否则静态图像预告片不可作为可接受的降级方案。

### 1b. 样本预览（防止浪费支出）

在批量生成支持资产之前，对每种昂贵生成类型制作一个样本并展示给用户：

1. **生成的插片样本**（如果使用 `image_selector` 或 `video_selector`）：生成一个代表性视觉画面。在批量生成前确认它是否与源素材相得益彰。
2. **音乐样本**（先尝试 `pixabay_music`——免费，可按情绪/BPM 搜索；备选 `freesound_music` 用于音效和环境音；仅在搜索工具无法满足简报要求时才求助于 `music_gen`）：采样或获取一个短片段。确认情绪和能量是否匹配节拍计划。

如果 `motion_required = true`，代表性视觉画面必须是视频片段样本，而不是静态图像样本。

如果被拒绝，调整参数并重试（最多 3 轮）。在获得批准前不要批量生成。

在样本生成之前，告知用户将使用哪个生成路径：

- 工具，
- 提供商，
- 模型或变体，
- 生成模式，
- 为何选择它。

如果该路径失败，在尝试不同提供商、模型或生成模式之前，请停下来询问。

### 2. 仅在需要时生成支持资产

可选的生成资产应填补明确的空白：

- 缺少的过渡 B-roll，
- 概念主导的插片，
- 纹理或氛围卡片，
- 简单的纹理动态背景。

对于需要动态效果的任务，首选使用 `video_selector` 生成镜头。`image_selector` 可用于支持外观开发、概念帧或嵌入式设计层，但其本身无法满足动态要求。

### 3. 准备真正的音频计划

存储：

- 选定的音乐曲目或提示词，
- 环境音层，
- 冲击音或转场音效，
- 字幕资产（如果存在对话或旁白）。

### 4. 用元数据记录权利和意图

推荐的元数据键：

- `source_selects`
- `music_plan`
- `ambience_plan`
- `title_assets`
- `generated_support_assets`
- `rights_notes`

### 生成提示词的前/后自我审查

> 在将提示词发送到任何图像或视频生成工具之前，运行一个三步自我审查，参考 CHAI 监督循环（"Building a Precise Video Language with Human-AI Oversight", arXiv 2604.21718v2）。成本很小（无需额外工具调用）；收益很大（避免浪费的生成）。对于电影化作品，这对**英雄帧提示词**最为重要——一个糟糕的英雄帧会毁掉整个作品，而英雄帧是最昂贵的镜头来重新生成。
>
> **第 1 步——预处理描述。** 按照你今天的写法写出提示词。不要过度编辑；目标是完成一个完整的第一稿。
>
> **第 2 步——批评检查。** 根据 5 方面检查清单（主体 / 主体运动 / 场景 / 空间构图 / 摄影机）对草稿评分。对每个方面：
> - 是否已指定？如果没有，省略是刻意的（例如，"无主体——风景镜头"）还是偶然的？
> - 是否有易混淆的术语被消歧？（dolly 与 zoom，pan 与 truck，bird's-eye 与 aerial，fisheye 与 barrel，full shot 与 close-up）
> - 情感形容词（"史诗般的"、"情绪化的"、"电影化的"）是否被替换为它们的视觉成因（低调照明、缓慢推镜、变形光晕、深阴影）？
> - 对于多镜头提示词和身份锚定的英雄帧：身份是否在各镜头间逐字锚定？
>
> **第 3 步——后处理描述。** 重写，补充缺失的方面、修正易混淆的术语并替换主观语言。后处理描述是发送到生成工具的内容。
>
> 将（预处理、批评、后处理）三元组记录在资产元数据中以便追溯。这模仿了 CHAI 工作流，并创建了审阅者可审计的记录。

### 5. 质量门禁

- 源资产和支持资产清楚区分，
- 生成的插片数量有限且有目的性，
- 音频计划与节拍图匹配，
- 每个引用的文件都存在，
- 如果需要动态效果，资产集包含用于动态主导节拍的实际视频片段。

### 制作中期事实核查

如果在资产生成过程中遇到不确定性：
- 使用 `web_search` 核实主体的视觉准确性（例如，这个建筑实际看起来是什么样？）
- 使用 `web_search` 在生成插图前查找参考图像
- 在决策日志中记录核查：`category="visual_accuracy_check"`

视觉准确性很重要。如果剧本提到某个特定的地点、人物或物体，在生成图像前核实它的实际外观。不要依赖 AI 模型的训练数据——它可能是错误或过时的。

## Seedance 提示词语言规则（硬性规则）

当使用 `video_selector` 调用 Seedance 2.0 时：
- ⚠️ **prompt 必须用中文编写**，仅专业影视术语可用英文
- 允许的英文：`wide shot`、`close-up`、`dolly in`、`the same character`、`no drift` 等无优质中文替代的专业术语
- 禁止的英文：场景描述、主体动作、环境氛围等**必须用中文**

## Seedance 参考图限制 + Ark API role 规则（硬性规则）

当使用 `video_selector` 调用 Seedance 2.0 时：

1. **参考图片总计不得超过 9 张** — 包括首帧图（`image_url`/`image_path`）和多参考图
   （`reference_image_urls`/`reference_image_paths`）在内，**统一计数**
2. **所有参考图自动缩放到 1280×720 以内**（等比例） — `seedance_video` 会在转为
   data URI 前用 Pillow 自动 resize，远程 URL 也会先下载再缩放
3. **seedance_video.py 会严格校验** — 超限时抛出 `ValueError`，拒绝调用
4. **Ark API role 区分**（火山引擎 v3 协议）：
   - 首帧图（`image_url`/`image_path`）→ `role: "first_frame"` — 模型从此帧开始续接
   - 多参考图（`reference_image_urls`/`reference_image_paths`）→ `role: "reference_image"` — 模型参考其视觉特征
5. 参考图包括：角色四视图、场景关键帧、尾帧链式引用图等全部参考图片

## 尾帧链式引用（跨片段视觉连续性）

当按顺序生成多个 Seedance 视频片段时，将前一段的**尾帧**作为
后一段的**首帧参考**，可显著提升跨片段一致性。

### 工作流

```python
# 步骤 1：生成片段 N
result_1 = video_selector.execute({
    "prompt": "片段 1 提示词",
    "operation": "reference_to_video",
    "reference_image_paths": [char_front, keyframe_1],
    "output_path": "projects/.../assets/video/clip_01.mp4",
})

# 步骤 2：提取片段 N 的尾帧
from tools.video._shared import extract_last_frame

last_frame = extract_last_frame(
    video_path="projects/.../assets/video/clip_01.mp4",
    output_path="projects/.../assets/images/clip_01_last_frame.jpg",
)

# 步骤 3：尾帧作为片段 N+1 的首帧参考
# 注意 role 区分：
#   image_path → Ark API role: "first_frame"（首帧锁定，模型从此帧续接）
#   reference_image_paths → Ark API role: "reference_image"（多模态视觉参考）
result_2 = video_selector.execute({
    "prompt": "片段 2 提示词",
    "operation": "reference_to_video",
    "image_path": last_frame,              # ← role: first_frame，前一段尾帧
    "reference_image_paths": [char_front, keyframe_2],  # ← role: reference_image
    # 参考图总计：1（尾帧）+ 2（其他）= 3，≤ 9 ✓
    "output_path": "projects/.../assets/video/clip_02.mp4",
})
```

### 规则

- **首帧图计入 9 张限制**：`image_path` + `reference_image_paths` 合计 ≤ 9
- **首个片段无尾帧**：第一段不使用尾帧引用，可从第二个片段开始链式引用
- **工具函数**：`tools.video._shared.extract_last_frame()` 或
  `frame_sampler` 的 `strategy="last_frame"` 均可提取尾帧
- **偏移量**：默认从末尾前移 0.5 秒提取，避免黑帧/淡出帧

### 多角色四视图的引用

当有多个角色时，在 prompt 中通过 `@ImageN` 语法引用参考图（序号为 content 数组中
从 1 开始的顺序），并逐角色进行身份锁定：

```python
inputs = {
    "prompt": (
        # 角色 A
        "@Image1 是角色「林月」— 黑色长发, 红色劲装, "
        "the same character, consistent, no drift.\n"
        # 角色 B  
        "@Image2 是角色「云澈」— 银白短发, 蓝色长袍, "
        "the same character, consistent, no drift.\n"
        "Shot 1: 林月与云澈在竹林中对峙..."
    ),
    "reference_image_paths": [
        "char_yue_combined.jpg",  # @Image1
        "char_yun_combined.jpg",  # @Image2
        "keyframe.jpg",           # @Image3
    ],
}
```

也可为每个角色上传独立的正面/侧面/背面四视图（占用更多参考位但细节更丰富）。
详情见 `key-visual-director.md` → **多角色四视图的区分与引用**。

## 常见陷阱

- 在证明源素材剪辑可行之前就生成额外的镜头。
- 将音乐视为单一循环而非对节拍有感知的元素。
- 忘记已提供资产的权利或来源说明。
- 因为某个提供商或渲染器失败，静默地将视频片段降级为静态图像。
- 在用户批准了生成路径后静默切换提供商或模型。

## 当你不确定如何操作时

如果你遇到不熟悉的生成技术、提供商行为或提示词模式：

1. **搜索网络**了解当前最佳实践——模型和 API 频繁变更，智能体的训练数据可能已过时
2. **检查 `.agents/skills/`** 中已有的第 3 层知识（提供商特定的提示词指南、API 模式）
3. **如果以上都没有帮助**，在 `projects/<project-name>/skills/<name>.md` 编写项目范围的技能文档，记录你学到的东西
4. **在技能文档中引用来源 URL**，使知识可追溯
5. **记录到决策日志中**：`category: "capability_extension"`, `subject: "learned technique: <name>"`

这在以下方面尤其重要：
- **视频生成提示词**——模型对特定词汇有反应，这些词汇随每个版本变化
- **图像模型参数**——FLUX、DALL-E、Imagen 的最佳设置各不相同且不断演变
- **音频提供商的特性**——语音克隆、音乐生成和 TTS 各有模型特定的最佳实践
- **Remotion 组件模式**——随着框架演进，新的合成技术不断涌现

不要依赖过时的知识。有疑问时，先搜索。
