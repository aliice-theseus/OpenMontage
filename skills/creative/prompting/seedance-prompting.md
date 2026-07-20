# Seedance 2.0 — 提示指南

> Layer 3 权威：`.agents/skills/seedance-2-0/SKILL.md`
> 通用词汇表请参见：`skills/creative/video-gen-prompting.md`

## 何时选择 Seedance 2.0

Seedance 2.0（字节跳动 Seed 团队，2026年2月发布）是 OpenMontage 的**首选高级默认值，用于电影感、预告片、预告、热血剪辑和运动主导的片段工作**，只要配置了付费网关（通过 `seedance_video`，或 HeyGen Video Agent / Avatar Shots）。它是产品线中唯一能同时交付以下所有功能的模型：

- 单次原生同步音频（语音 + 音效 + 环境一起，非后期同步）
- 单个提示内的多镜头生成
- 导演级相机控制
- 引用对话的唇形同步
- 最多9张图像 + 3个视频片段 + 3个音频片段的参考条件生成
- 跨镜头的一致角色身份

发布时 Artificial Analysis Elo 1269 — 领先于 Veo 3、Sora 2、Runway Gen-4.5。

仅在确实有原因时才切换出 Seedance 2.0：严格预算（使用 `fast` 变体或 LTX）、明确的用户偏好（VEO/Sora/Kling）、或其他模型做得更好的风格匹配（VEO 用于照片级真实感风景，Kling 用于动漫）。

## Seedance 2.0 的 8 组件提示结构

Seedance 对镜头语言、多镜头剪切和引用对话异常字面。使用此结构 — 包含重要的，省略不重要的：

1. **镜头/构图** — 广角定场、中景、特写、斜角等
2. **相机运动** — 静态、慢推、航拍、手持、环绕、推轨变焦
3. **主体描述** — 必须在镜头间持续的物理细节（身份锚点）
4. **动作节拍** — 每句话一个节拍，多镜头使用 `→` 或明确 `Shot 1 / Shot 2`
5. **环境/场景** — 地点、时代、天气、时间
6. **光照/调色板** — 一个光照思路，选择并坚持
7. **风格/调色/时代** — "anamorphic lens, teal-orange grade, 35mm film grain"
8. **音频** — 环境音、剧情声、音乐方向（仅纹理）、唇形同步的引用对话

## Seedance 特有优势

| 能力 | 如何调用 |
|------|---------|
| **原生同步音频** | 在提示中描述声景。保持 `generate_audio=true`。 |
| **单次生成多镜头** | 使用 `Shot 1 (...)`、`Shot 2 (...)` 等。跨镜头保持主体描述一致。 |
| **导演级相机** | 使用无歧义的术语：`slow dolly-in`、`arc shot`、`Dutch tilt`、`aerial push-in`、`handheld with micro-shake` |
| **引用对话的唇形同步** | `Character says: "line."` — 快速剪切上每行 ≤ 约6个词 |
| **参考转视频** | 使用 `reference-to-video` 端点；在提示中命名每个资产（`Reference 1: hero character — ...`） |
| **角色身份一致性** | 在每个镜头中描述相同的物理细节 — Seedance 将其用作身份锚点 |

## 多镜头模式

> **在每个镜头中逐字重复身份。** "the same character" / 代词 / "Aang again" 不起作用。在每个镜头块中逐字重复 3-6 个可区分的视觉属性。Seedance 对每个镜头的处理如同你第一次说出来。

Seedance 遵循明确的镜头列表：

```
Shot 1 (wide aerial establishing, slow push-in):
Snow-covered Air Temple at dawn, spires catching first orange light.
Wind lifting prayer flags.

Shot 2 (medium, low angle, handheld):
Aang — bald, blue arrow tattoo, orange robes — plants his staff on stone.
He squints into the rising sun.

Shot 3 (extreme close-up, rack focus):
Rack focus from the glowing arrow tattoo on his forehead to the distant peaks.
Aang says: "It's time."

Style: anamorphic lens, teal-orange cinematic grade, 35mm film grain.
Audio: rising orchestral swell with low taiko pulse, wind, distant wingbeats.
```

### 多镜头中的主体转场基元

Seedance 处理主体进入或离开镜头的四种不同方式。显式命名基元有助于模型在镜头之间构建正确的转场。

- **Subject revealing（主体揭示）**（通过相机运动或主体运动）— 主体在镜头中变得可见。
  示例：`Shot 2 (slow truck right): empty corridor at first; the camera trucks right to reveal Aang — bald, blue arrow tattoo, orange robes — pressed flat against the wall.`

- **Subject disappearing（主体消失）** — 主体通过运动或遮挡离开画面。
  示例：`Shot 4 (static wide): Aang — bald, blue arrow tattoo, orange robes — sprints into the temple doorway and is swallowed by shadow; camera holds on the empty threshold.`

- **Subject switching（主体切换）**（焦距切换 / 相机运动）— 焦点或构图从一个主体转移到另一个。
  示例：`Shot 5 (close-up, rack focus): rack focus from Aang's glowing arrow tattoo in foreground to Sokka — dark hair, blue tunic, boomerang on back — emerging from the mist behind.`

- **Complex alternating focus（复杂交替焦点）** — 焦点在一个镜头内在两个主体之间振荡。
  示例：`Shot 7 (medium two-shot, alternating rack focus): focus on Aang — bald, blue arrow tattoo, orange robes — as he speaks, then pulls to Katara — long brown hair, blue water-tribe parka — as she answers, then back to Aang on the final beat.`

## 唇形同步模式

```
Aang says: "I won't run anymore."
Sokka, half a step behind, replies: "Then we fight."
```

- 精确使用 `Character says: "..."` / `Character replies: "..."` — 嘴形基于引用的字符串。
- 保持台词简短（快速剪切镜头 ≤ 6 个词）以避免漂移。
- 对于单说话者独白，保持相机靠近并在说话者镜头上静态。

## 参数速查表

| 参数 | 指导 |
|------|------|
| `duration` | 主镜头 `5`–`8` 秒，多镜头场景 `10`–`12` 秒，插入镜头 `4` 秒。不确定时用 `auto`。 |
| `aspect_ratio` | 预告片 `21:9`，广播 `16:9`，Reels/Shorts/TikTok `9:16` |
| `resolution` | 默认 `720p`。仅成本受限预览用 `480p`。 |
| `generate_audio` | 保持 `true` — 同步音频是护城河。如果不用，在合成中剥离。 |
| `model_variant` | 主镜头 + 多镜头 + 相机重使用 `standard`。B-roll、预览、延迟受限任务用 `fast`。 |
| `seed` | 一旦镜头构图可读即锁定种子；使用相同种子迭代变体。 |
| `prompt length` | 主镜头 200–400 词；插入镜头 80–150 词。Seedance 是少数奖励长而结构化的 5 方面提示的模型之一。 |

## 迭代策略

1. **勾勒形状** — `duration=5`、`fast`、一个镜头。确认构图。
2. **锁定种子** — 在每片段 README 中记录。
3. **升级到 `standard`** — 相同种子，收紧相机 + 光照语言。
4. **扩展或多镜头** — 仅在单镜头版本干净后。
5. **提升到最终版** — 将提示、种子、变体和时长写入资产清单，以便合成可以重新渲染一致的重复镜头。

## 应避免的内容

| 不要 | 原因 |
|------|------|
| 一个镜头中四个以上同时动作 | 运动连贯性崩溃。拆分为多镜头。 |
| 片段内可读文字/标志 | 文字渲染不可靠。在 Remotion 叠加中处理文字。 |
| 冲突的光照（`bright noon` + `neon night`） | 模型选择一个并忽略另一个。 |
| 快速剪切镜头上长对话 | 唇形同步漂移。 |
| 慢动作、多镜头或复杂相机使用 `fast` 变体 | 首次尝试常失败。路由到 `standard`。 |
| 请求 Seedance 生成完整多乐器配乐 | 保持音频方向为纹理性；真正的配乐属于 `music` / `pixabay_music` / `elevenlabs` 并在合成中混音。 |
| 无故绕过 `video_selector` | 失去评分、回退和成本处理。 |

## 集成说明

- **电影感流程：** Seedance 2.0 是默认值。21:9，蒙太奇多镜头，当简报有视觉圣经时使用参考转视频。
- **动画讲解：** 仅将 Seedance 2.0 用于定场/情绪/冷开场片段 — 核心动态图形保持在 Remotion。
- **屏幕演示/播客/片段工厂：** 不是正确的默认值。仅用于风格化冷开场。
- **成本检查：** 在提案阶段做预算。

## 示例 — Airbender 预告片主镜头节拍（60秒总预告片，这是7个镜头中的第3个）

```
Shot 1 (wide aerial, slow push-in, 3s):
Snow-covered Air Temple at dawn, spires catching orange light,
prayer flags lifting in wind.

Shot 2 (low angle medium, handheld, 3s):
Aang — bald, blue arrow tattoo on forehead, orange and yellow robes —
plants his staff on weathered stone, squints into the rising sun.

Shot 3 (extreme close-up, rack focus, 3s):
Rack focus from the glowing arrow on his forehead to distant peaks.
Aang says: "It's time."

Lighting: cold blue ambient with warm break on the horizon,
rim light from rising sun.
Style: anamorphic 2.39:1, teal-orange cinematic grade, 35mm film grain,
halation on speculars.
Audio: low taiko drums rising to orchestral swell on Shot 3,
wind through temple, distant wingbeats, leather staff-grip creak.
```

参数：`duration=10`、`aspect_ratio=21:9`、`resolution=720p`、`model_variant=standard`、`generate_audio=true`，镜头2后锁定种子。
