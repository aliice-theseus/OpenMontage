# 创意导演 - 电影化流水线

## 适用场景

将本流水线用于预告片、品牌影片、戏剧性蒙太奇或以情绪为主导的短视频，其中节奏、氛围和情感递进比直接解说更重要。

不要仅仅因为用户说了"让它看起来电影化"就使用此流水线。如果项目实际上是屏幕演示、解说视频或重新利用素材的任务，请将其路由到相应的地方。

## 参考输入

- `docs/cinematic-best-practices.md`
- `skills/creative/cinematic.md`
- `skills/creative/storytelling.md`

## 流程

### 1. 分类源素材形态

记录源素材模式：

- `footage_only`（仅视频素材）
- `footage_plus_stills`（视频素材加静止图像）
- `still_led`（静止图像主导）
- `generated_support`（生成辅助素材）
- `mixed_montage`（混合蒙太奇）

同时分类所要求的交付物是否需要动态效果。以布尔值形式存储在 `brief.metadata.motion_required` 中。

当视频的承诺依赖于运动镜头或动画合成而非静态帧时，设置 `motion_required = true`。这包括：

- 科幻预告片，
- 电影化预告精简版，
- 动作或热血剪辑，
- 智能体/数字人输出，
- 任何质量依赖于生成视频片段的概念。

除非用户已提供素材或环境确实能够生成，否则不要假设存在素材库、生成的 B-roll 或音乐。

### 2. 定义情感弧线

用平实的语言选择弧线：

- tension -> reveal（紧张 -> 揭示）
- wonder -> scale（惊奇 -> 宏大）
- intimacy -> payoff（亲密 -> 回馈）
- urgency -> resolution（紧迫 -> 解决）
- mystery -> CTA（神秘 -> 行动召唤）

简报应告诉后续阶段视频想让观众感受什么，而不仅仅是关于什么。

### 3. 选择交付形态

常见的输出形态：

- `teaser`（预告精简版）
- `trailer`（预告片）
- `hero_brand_film`（主品牌影片）
- `mood_cut`（情绪剪辑）
- `social_cutdown`（社交媒体精简版）

将更长的规划细节存储在 `brief.metadata` 中。

推荐的元数据键：

- `source_mode`
- `motion_required`
- `delivery_shape`
- `emotional_arc`
- `anchor_assets`
- `music_strategy`
- `generated_support_level`
- `aspect_ratio_plan`
- `rights_constraints`

### 4. 对处理方案做现实检查

如果用户的源素材薄弱且没有生成途径，请如实说明。电影化的结果仍然需要足够的视觉或音频素材来承载情绪。

如果 `motion_required = true`，明确说明动态实现路径：

- 确认计划中的片段生成提供商，
- 确认是否需要 Remotion 来完成预期的合成，
- 如果任一不可用或不稳定，将处理方案标记为受阻，而不是静默地围绕静态图像重新设计。

### 5. 音乐计划（强制性）

电影化视频的成功与否取决于音频。**在用户批准简报之前，提前说明音乐情况。**

按此顺序检查可用性：

1. **用户音乐库（`music_library/`）：** 检查此文件夹是否存在以及是否包含曲目。列出可用曲目及其时长和情绪。让用户选择。
2. **音乐生成 API：** 检查 `registry.get_by_capability("music_generation")`。如实报告状态、配额和每首曲目的成本。
3. **免版税来源：** 说明用户可以通过将曲目放入 `music_library/` 来从 YouTube Audio Library、Jamendo 或其他免费来源提供曲目。

提供明确的选项：

```
音乐计划
├── 您的音乐库：[N 首曲目 / 空]
├── AI 生成：[提供商] — [可用/不可用] [成本]
└── 自带曲目：在资产阶段前将曲目放入 music_library/

选项：
  (a) 使用音乐库中的曲目（哪一首？）
  (b) 提供您自己的曲目
  (c) 通过 API 生成（如果可用）
  (d) 无音乐继续（不推荐用于电影化作品）
```

将决策记录在 `brief.metadata.music_strategy` 中，包含选定的来源和路径/提示词。

### 6. 质量门禁

- 源信息明确，
- 简报说明动态效果是否是硬性要求，
- 情感弧线具体明确，
- 输出形态与可用素材匹配，
- 音乐计划已确定（来源已选定或明确推迟），
- 处理方案之所以是电影化的是有理由的，而不仅仅是标签。

## 常见陷阱

- 把实际上只是普通剪辑加黑边的作品称为电影化。
- 未检查工具就假设生成的插片可用。
- 默默地将动态主导的简报变成静态图像主导的预告精简版。
- 规划预告片形态但没有任何揭示或回馈时刻。
