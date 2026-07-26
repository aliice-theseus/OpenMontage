# 资产导演 — 动画管线

## 使用时机

此阶段准备实际的动画原料：旁白、图表、数学渲染、运动背景、代码视觉以及可复用的排版或布局系统。

## 动画制作 — 选择哪个运行时

在制作动态图形组件之前，阅读 **`skills/meta/animation-runtime-selector.md`** 了解运行时路由。动画是最可能证明 GSAP 插件合理性的管线——标志变形、曲线镜头路径、动态排版、FLIP 转场。

常见动画管线需求的快速路由：

| 运动类型 | 推荐方法 |
|---|---|
| SVG 标志在两个形状之间变形 | GSAP MorphSVG — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| SVG 上的线条绘制/笔画揭示 | GSAP DrawSVG — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 对象沿曲线路径运动 | GSAP MotionPath — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 逐字符/逐字标题揭示 | GSAP SplitText — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 自定义贝塞尔或弹性缓动 | GSAP CustomEase — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 布局到布局的元素飞行（FLIP） | GSAP Flip — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 跨多个元素的多步序列 | GSAP timeline — 阅读 `.agents/skills/gsap-timeline/SKILL.md` |
| 粒子叠加/背景运动 | Remotion `ParticleOverlay` 组件（已存在） |
| 数学动画（图表、方程式） | Manim — 阅读 `.agents/skills/manim-composer`、`.agents/skills/manimce-best-practices` |
| 吉卜力/动漫风格静态帧驱动场景 | Remotion `AnimeScene` 组件 + FLUX 图像生成 |

**Remotion 确定性规则：** Remotion 组件内每次 GSAP 使用必须通过 `useCurrentFrame()` 驱动时间线前进——决不使用 `requestAnimationFrame`。模式示例见 `.agents/skills/gsap-react/SKILL.md`。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | 产物验证 |
| 前置产物 | `state.artifacts["scene_plan"]["scene_plan"]`、`state.artifacts["script"]["script"]`、`state.artifacts["proposal"]["proposal_packet"]` | 工具路径和节拍映射 |
| 工具 | `tts_selector`、`image_selector`、`video_selector`、`math_animate`、`diagram_gen`、`code_snippet`、`music_gen` — 选择器自动发现注册表中所有可用提供商 | 资产生产选项 |
| 样式手册 | 活跃的样式手册 | 视觉一致性 |

### AI 视频导演技能门控

当动画模式会调用 `video_selector` 时，先读取工具返回的全部 `required_agent_skills`，用画面质感与运镜导演技能锁定视觉锚点和主运动。动作、追逐、跑酷、枪战、武侠或竞技镜头还必须读取 `conditional_agent_skills.action_or_combat_scene` 指向的 `direct-action-scenes`，再生成提示。

## 流程

### 1. 从确定性资产开始

优先选择方差最小的有用路径：

- 结构化图表使用 `diagram_gen` 优先于通用图像生成，
- 代码场景使用 `code_snippet`，
- 真正的数学运动使用 `math_animate`，
- 现有素材优先于新生成。

### 1b. 样片预览（防止浪费支出）

在批量生成资产之前，每种昂贵类型生成一份样片并展示给用户：

1. **TTS 样片**（如果叙述主导）：存在 `script.voice_performance.sample_section_id` 时生成它；否则选择情感或节奏变化最强的部分。在批量之前确认声音、速度、停顿、强调和语调。
2. **视觉样片**：生成一个有代表性的场景视觉（图表、插画或运动背景）。在批量其余部分之前确认风格和质量。

如果被拒绝，调整参数并重试（最多 3 次迭代）。在获得批准前不要批量生产。

### 1c. 基于图像动画的多图像生成（方法 A）

当 `animation_mode == "image_animation"` 时，每个场景需要 **2-3 张图像**用于交叉淡入动画。这就是让静态帧看起来像运动的关键。

**图像生成工作流：**

1. **定义一个视觉系统** — 一组可复用的锚点，用于项目中所有图像。这确保了视觉连贯性，而无需将每个镜头压平到相同的提示中。将其存储为可复用的元数据。
   ```
   示例："手绘自然奇幻，暖色苔藓与琥珀调色板，
   柔和的漫射光，绘画般的 foliage 纹理，温柔的惊奇感。"
   ```
   然后根据每个场景调整：
   - 场景 1：宽阔的森林山谷定场，薄雾，日出
   - 场景 2：特写角色时刻，灯笼光晕，飘浮的孢子
   - 场景 3：抽象魔法能量揭示，更明亮的强调色对比

2. **使用种子管理** — 对每个场景，为 A/B 变体使用相近的种子值（例如种子 100 和 101）。相同提示 + 不同种子 = 相同构图但细微差异 = 自然的交叉淡入运动。

3. **首先生成一张测试图像** — 渲染单个场景以验证视觉系统能在 1920×1080 下产生好的结果，然后再批量生成所有图像。

4. **批量生成** — 生成所有场景图像。跳过已存在于磁盘上的任何图像（幂等操作）。

5. **合成 JSON** — 每个场景获得 `type: "anime_scene"`，包含 `images: ["path/a.png", "path/b.png"]` 以及镜头运动、粒子类型和光照配置。

**成本估算：** 每场景 2-3 张图像 × ¥0.03-0.13/张，取决于提供商。

**参考：** 参见 `projects/mori-no-seishin/generate_images.py` 了解已验证的批量生成模式。

6. **复制到 Remotion 公共目录** — 生成所有图像后，将其复制到 `remotion-composer/public/<项目名>/`，以便 Remotion 可以通过 `staticFile()` 访问它们。合成 JSON 中的图像路径相对于此目录：
   ```
   remotion-composer/public/<项目名>/scene1-a.png   ← Remotion 从这里读取
   remotion-composer/public/<项目名>/ambient-music.mp3  ← 音乐也是
   ```
   **如果跳过此步骤，渲染将因文件缺失错误而失败。** 这是新项目渲染失败的第一大原因。

### 2. 构建可复用系统

一次性创建：

- 排版样式，
- 下部三分一或标签样式，
- 重复主题元素资产，
- 背景容器。

### 3. 旁白是可选的，但计划必须明确

如果项目是叙述主导的，生成或获取旁白。阅读 `skills/meta/voice-performance-director.md`，然后在构建 TTS 请求时应用 `script.voice_performance` 和各部分的 `delivery_cues`。当 `provider_text` 存在时使用它，将提示映射到提供商控制参数，并在每个旁白资产上记录应用设置。如果是文本主导或音乐主导，在元数据中明确说明。

### 4. 使用元数据表达可行性的真相

推荐的元数据键：

- `tool_path_map`
- `reusable_assets`
- `narration_assets`
- `voice_performance`：样片批准路径、提供者设置以及是否应用了语音提示
- `scene_asset_index`
- `blocked_assets`

### 5. 质量关卡

- 每个场景的资产路径明确，
- 可复用资产实际被复用，
- 缺失的能力诚实公开，
- 每个引用的文件都存在，
- 叙述主导的资产应用了已批准的语音表现设置。

### 中期制作事实核查

如果在资产生成过程中遇到不确定性：
- 使用 `web_search` 验证主体的视觉准确性（例如这个建筑实际看起来什么样？）
- 使用 `web_search` 在生成插画之前查找参考图像
- 在决策日志中记录验证：`category="visual_accuracy_check"`

视觉准确性很重要。如果剧本提到特定地点、人物或对象，在生成图像之前验证其实际外观。不要依赖 AI 模型的训练数据——它可能是错误或过时的。

## 常见陷阱

- 在确定性资产效果更好的情况下使用高方差生成。
- 重复构建相同的标题或标签系统。
- 隐藏失败的资产路径而不是报告它们。
- 将 TTS 视为纯文本到音频。叙述主导的动画需要从剧本传递到生成音频的停顿、强调和节奏提示。
- 将"一致性"视为"每次相同的提示"。好的动画保持可识别的世界，同时让每个节拍感觉新鲜。

## 当你不知道如何做时

如果遇到不确定的生成技术、提供者行为或提示模式：

1. **搜索网络**了解当前最佳实践——模型和 API 频繁变化，代理的训练数据可能已过时
2. **检查 `.agents/skills/`** 中现有的 Layer 3 知识（提供者特定的提示指南、API 模式）
3. **如果两者都不起作用**，在 `projects/<项目名>/skills/<名称>.md` 编写项目范围的技能，记录你学到的东西
4. **在技能中引用来源 URL**，使知识可追溯
5. **在决策日志中记录**：`category: "capability_extension"`，`subject: "learned technique: <名称>"`

以下方面尤其重要：
- **视频生成提示**——模型对特定词汇的响应会随每个版本变化
- **图像模型参数**——FLUX、DALL-E、Imagen 的最佳设置各不相同且不断演变
- **音频提供者特性**——语音克隆、音乐生成和 TTS 各有模型特定的最佳实践
- **Remotion 组件模式**——新的合成技术随框架演变而出现

不要依赖过时的知识。有疑问时，先搜索。
