# VEO 3.1 / VEO 3 — 提示指南

> 来源：[Vertex AI 视频生成提示指南](https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide)
> 通用词汇表请参见：`skills/creative/video-gen-prompting.md`

**字数：** VEO 3.1 的甜蜜点是 100–250 词；更长的提示不再有帮助。

## VEO 特定的 14 组件结构

VEO 对所有模型中最为全面的提示结构有响应：

1. **主体** — 动作围绕谁/什么展开
2. **动作** — 运动、交互、表情
3. **场景/背景** — 地点、时间、天气、时期
4. **镜头角度** — 镜头类型和视角
5. **镜头运动** — 动态运动
6. **镜头/光学效果** — 镜头如何"观看"
7. **光照** — 光源、方向、质量
8. **基调/情绪** — 情感基调
9. **艺术风格** — 照片级真实感、电影感、动画、艺术运动
10. **氛围** — 调色板、大气效果、纹理
11. **时间元素** — 节奏、时间流、韵律
12. **音频** — 音效、环境、对话（VEO 3 生成对话）
13. **电影术语** — 剪辑技巧（匹配切、蒙太奇、分光镜）
14. **负面提示** — 要排除的内容

## VEO 特有的优势

- **对话生成**：VEO 3 原生生成角色语音。自然地写对话。
- **音频集成**：环境音、音乐和语音与视频一起生成。
- **负面提示**：明确支持 — "无文字叠加、无水印、无镜头光晕"
- **剪辑词汇**：理解"匹配切"、"跳切"、"蒙太奇"、"分光镜"作为提示术语。

### VEO 字面遵循的镜头词汇

VEO 3.1 区分三个镜头运动家族，并将其令牌视为独立的基元。混淆它们（例如，当你意思是"推轨"时要求"变焦"）会产生错误的运动。

- **平移（支架物理移动）：** `dolly`（沿镜头轴进/出）、`truck`（左/右横向）、`pedestal`（上/下垂直）
- **旋转（支架不动，相机旋转）：** `pan`（偏航，左/右）、`tilt`（俯仰，上/下）、`roll`（斜角/Z轴）
- **纯镜头（支架和机身不移动）：** `zoom`（焦距变化）、`rack focus` / `pull focus` / `focus tracking`（焦平面变化）

推轨 ≠ 变焦；摇摄 ≠ 横移。VEO 遵循占主导的令牌。

## VEO 镜头效果（独特）

VEO 具体响应对大多数模型忽略的光学效果：

| 效果 | 提示语言 |
|------|---------|
| **焦距切换** | "rack focus from foreground flower to background figure"（快速切换） |
| **焦距推移** | "slow pull focus from the candle in the foreground to the doorway behind"（渐进，慢于切换） |
| **跟焦** | "focus tracks the runner as she crosses frame; background stays soft"（焦点跟随移动主体） |
| **推轨变焦（眩晕效果）** | "vertigo effect as character realizes the truth" |
| **鱼眼** | "fisheye lens distortion, skatepark POV" |
| **变形镜头光晕** | "anamorphic lens flare streaking horizontally from setting sun" |

这三种对焦模式（切换、推移、跟踪）是不同的 — VEO 3.1 按照论文区分它们。

## VEO 艺术运动参考

VEO 对特定艺术运动作为风格锚点反应良好：
- "Van Gogh-inspired swirling sky"
- "Surrealist Dalí-esque melting landscape"
- "Art Deco geometric patterns in the architecture"
- "Bauhaus clean lines and primary colors"
- "Gritty graphic novel illustration style"
- "Chinese ink wash painting animation"

## 字幕预防

VEO 可能默认对话添加字幕。为预防：
- 在负面提示中添加："no subtitles, no captions, no text overlays"

## 示例

```
Subject: A lone astronaut in a weathered white spacesuit
Action: Slowly turns to face the camera, visor reflecting a dying star
Scene: Surface of a barren moon, cracked grey terrain, massive ringed
       planet filling the horizon
Camera: Low-angle medium shot, slow arc around subject
Lens: Wide-angle, deep focus keeping both astronaut and planet sharp
Lighting: Harsh rim light from the star behind, cool blue fill from
         planet reflection, no atmosphere diffusion
Mood: Awe, isolation, quiet grandeur
Style: Photorealistic sci-fi cinematography, IMAX-scale
Audio: Breathing inside helmet, faint radio static, low rumble
Negative: No text, no HUD overlay, no lens flare
```
