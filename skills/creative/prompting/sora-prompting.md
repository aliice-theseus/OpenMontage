# Sora 2 — 提示指南

> 来源：[OpenAI Sora 2 Cookbook](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide)
> 通用词汇表请参见：`skills/creative/video-gen-prompting.md`

**字数：** Sora 2 在 100–250 词左右达到平台期。超过 250 词，额外细节很少改善输出。

## Sora 特定的提示模板

Sora 对结构化格式响应最佳，包含散文+电影摄影块+动作节拍：

```
[散文场景描述 — 角色、服装、风景、天气、细节。
 尽可能描述详细以匹配你的愿景。]

Cinematography:
Camera shot: [构图和角度]
Lens: [焦距、类型]
Lighting: [主光、补光、边缘光、带色温的实际光源]
Mood: [整体基调]

Actions:
- [节拍1：特定手势或运动]
- [节拍2：另一个不同的节拍]
- [节拍3：反应或对话]

Dialogue:
[简短自然的台词，根据片段长度保持简洁]
```

## 高级可选字段

Sora 独特地响应这些大多数模型忽略的制作级细节：

| 字段 | 示例 |
|------|------|
| **镜头规格** | "40mm spherical", "85mm", "Anamorphic 2.0x" |
| **滤镜** | "Black Pro-Mist 1/4", "slight CPL rotation" |
| **调色/调色板** | "Warm Kodak-inspired grade", "teal-and-orange LUT" |
| **胶片模拟** | "16mm black-and-white", "35mm photochemical contrast" |
| **剧情声** | "faint rail screech, rain patters window, clock ticks" |
| **服装** | "navy coat, sleeves rolled, suspenders loose" |
| **后期** | "fine-grain overlay, mild halation, gate weave, soft vignette" |
| **快门** | "180° shutter angle" |
| **播放速度** | "speed ramp from 1x to 0.25x mid-shot", "stop-motion staccato", "time-reversed exhale" |
| **镜头畸变** | "fisheye barrel distortion at the edges", "subtle barrel curvature on straight lines" |
| **对焦模式** | "rack focus from foreground bottle to background figure", "deep focus, FG to BG sharp" |

## Sora 的不同之处

- **散文优先**：先写丰富的段落，然后添加技术块。不要以相机规格开头。
- **角色引用**：通过 API 可锁定最多2个上传的角色 ID。
- **对话同步**：短台词有效。复杂的多角色对话不行。
- **编辑命令**："Same shot, switch to 85mm" 或 "Same lighting, new palette: teal, sand, rust" — Sora 支持在现有生成上的迭代优化。
- **创作自由**：较短的提示 → 更多创作空间。较长的 → 更多控制。

## 调色板技巧

命名 3-5 种锚点颜色，而非含糊的"暖色调"：
- "Amber, cream, walnut brown"（复古温暖）
- "Teal, sand, rust"（沿海沙漠）
- "Cool blues with warm tungsten accents"（黑色电影）

## Sora API 参数（不能在提示中设置）

- `model`: `sora-2` 或 `sora-2-pro`
- `size`: 720x1280, 1280x720, 1080x1920, 1920x1080, 1024x1792, 1792x1024
- `seconds`: 4, 8, 12, 16, 20

## 示例

```
Style: Hand-painted 2D/3D hybrid animation with soft brush textures,
warm tungsten lighting, tactile stop-motion feel. Subtle watercolor wash;
warm-cool balance; filmic motion blur.

Inside a cluttered workshop, shelves overflow with gears and yellowing
blueprints. Small round robot sits on wooden bench, dented body patched
with mismatched plates. Large glowing blue eyes flicker as it fiddles
with a humming light bulb.

Cinematography:
Camera: medium close-up, slow push-in with gentle parallax from hanging tools
Lens: 35mm virtual; shallow depth of field
Lighting: warm key from overhead practical; cool spill from window
Mood: gentle, whimsical, touch of suspense

Actions:
- Robot taps bulb; sparks crackle
- Flinches, dropping bulb, eyes widening
- Bulb tumbles in slow motion; catches it just in time
- Puff of steam escapes chest — relief and pride

Background Sound:
Rain, ticking clock, soft mechanical hum, faint bulb sizzle
```
