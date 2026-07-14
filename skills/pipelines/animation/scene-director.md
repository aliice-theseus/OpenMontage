# 场景导演 — 动画管线

## 使用时机

你将剧本转换为可行的动画计划。这个阶段决定了项目是感觉经过精心设计还是杂乱无章。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | 产物验证 |
| 前置产物 | `state.artifacts["script"]["script"]`、`state.artifacts["proposal"]["proposal_packet"]` | 节拍映射和工具路径 |
| 样式手册 | 活跃的样式手册 | 调色板、排版、运动一致性 |

## 流程

### 1. 制定动画分镜思维的计划

为每个场景定义：

- 什么先出现，
- 什么变化，
- 什么保持不变，
- 场景如何退出。

### 2. 限制转场系列

选择一小组转场含义：

- 切，
- 淡入淡出，
- 滑动，
- 变换。

### 3. 匹配场景类型到工具路径

使用：

- `diagram` 场景用于结构化解释，
- `animation` 场景用于运动优先的序列，
- `text_card` 用于干净的高冲击力文案时刻，
- `generated` 仅在需要时使用。

**对于 `image_animation` 方法（动漫/插画风格）：**

为每个场景使用 `anime_scene` 类型。规划：

- **每场景图像数量**：2-3 张图像，基于相同的视觉系统和相近的种子构建，用于交叉淡入淡出效果
- **镜头运动**：从 `zoom-in`、`zoom-out`、`pan-left`、`pan-right`、`ken-burns`、`drift-up`、`drift-down`、`parallax`、`static` 中选择——每场景变化以防止单调
- **粒子类型**：从 `fireflies`、`petals`、`sparkles`、`mist`、`light-rays` 中选择——匹配场景情绪
- **光照**：可选的 `lightingFrom`/`lightingTo` 渐变，用于场景内的氛围变化
- **暗角**：`true` 用于电影感构图（默认），`false` 用于明亮/开放场景
- **场景时长**：每场景 4-7 秒。更长的场景需要更多图像以实现交叉淡入的多样性。

**image_animation 的场景多样性规则：**
- 不要对连续场景使用相同的镜头运动
- 在暖色和冷色粒子类型之间交替
- 混合特写和宽幅定场镜头
- 使用叠加层（`hero_title`、`section_title`）增加叙事结构

**JSON 属性名映射**（在合成 JSON 中使用这些确切的字段名）：

| 概念 | JSON 字段 | 示例值 |
|---------|-----------|----------------|
| 镜头运动 | `animation` | `"zoom-in"`、`"pan-right"`、`"ken-burns"` |
| 粒子效果 | `particles` | `"fireflies"`、`"sparkles"`、`"mist"` |
| 粒子颜色 | `particleColor` | `"#FFE082"` |
| 粒子密度 | `particleCount` | `20`（范围：1-50） |
| 粒子亮度 | `particleIntensity` | `0.5`（范围：0-1） |
| 光照起始 | `lightingFrom` | `"rgba(255,200,100,0.15)"` 或 `"transparent"` |
| 光照结束 | `lightingTo` | `"rgba(255,107,157,0.08)"` 或 `"transparent"` |
| 电影感边缘暗化 | `vignette` | `true` / `false` |
| 场景背景 | `backgroundColor` | 主题派生的值，如 `"#0A0A1A"` 或 `"#F6F1E8"` |

参考：`remotion-composer/public/demo-props/mori-no-seishin.json`——6 个场景使用此模式。
参考：`remotion-composer/public/demo-props/deep-ocean.json`——6 个水下场景，不同调色板。

### 4. 使用元数据表达时机规则

推荐的元数据键：

- `animatic_rules`
- `transition_rules`
- `hold_rules`
- `tool_path_map`
- `reusable_motifs`

### 5. 场景计划 5 维度检查清单

> 每个场景必须指定全部五个维度，但侧重点随场景的 `animation_mode` 而转移。Manim 和其他图表/程序化场景最关心**主体**和**空间构图**——电影摄影意义上的镜头和主体运动通常映射为 N/A 或抽象等价物。AI 视频 / `image_animation` / `anime_scene` 场景关心所有五个维度，行为类似于电影镜头。将某个维度标记为 N/A 是允许的，但必须在每个场景中明确说明；禁止静默省略。
>
> 1. **主体（Subject）**——类型 + 关键视觉属性；对于 Manim，是指被前景化的方程/对象/图形；对于 `anime_scene`，是指焦点所在的角色或环境。
> 2. **主体运动（Subject Motion）**——对于 Manim，是指 `Create`/`Transform`/`FadeIn` 的顺序以及每个动画传达的内容；对于 AI 视频，是指按时间顺序的动作和交互。
> 3. **场景（Scene）**——叠加层（单独列出！）+ 视角 + 设定 + 时段 + 场景动态。对于 Manim，"设定"是画布背景 + 坐标轴样式；对于 `anime_scene`，是环境 + 光照渐变。
> 4. **空间构图（Spatial Framing）**——镜头尺寸 + 画面内位置 + 深度（前景/中景/背景）+ 相机相对高度；以及这些如何**变化**。Manim 关心布局网格 + 元素位置；AI 视频关心完整的电影摄影构图。
> 5. **镜头（Camera）**——播放速度 → 镜头畸变 → 高度 → 角度 → 对焦/景深 → 稳定度 → 运动。对于 Manim 和纯动态图形，除非使用虚拟镜头移动（`MoveCamera`、`self.frame`），否则默认为 N/A。对于 `anime_scene` 和 AI 视频，完整指定。
>
> 将这些与场景元数据中的 `animation_mode` 关联：一个 Manim 场景如果完整列出镜头维度就是过度指定；一个 AI 视频场景如果省略镜头维度就是指定不足。参见 `skills/creative/video-gen-prompting.md` 了解原始词汇。

> **叠加层说明。** 叠加层（标题、字幕、HUD、水印、构图图形、下部三分一、`hero_title`、`section_title`、`provider_chip`）不属于场景的前景/中景/背景深度轴。在场景元数据中单独列出（`overlays: [...]`），包含内容和位置。绝不要将叠加层描述为"在前景中"——这会使下游工具和任何重新分析输出的视频理解模型都感到困惑。

### 6. 质量关卡

- 每个场景都有清晰的时机意图，
- 5 维度检查清单满足场景的 `animation_mode`（适当位置有明确的 N/A），
- 叠加层位于 `overlays:` 下，绝不在构图描述内部，
- 转场系统有限且有意义，
- 工具路径明确，
- 序列感觉像一个设计好的系统。

## 常见陷阱

- 在每个场景中添加新的转场想法。
- 规划没有现实制作路径的场景。
- 过度动画化文本密集的场景。
