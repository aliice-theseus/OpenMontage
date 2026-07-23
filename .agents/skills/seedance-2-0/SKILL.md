---
name: seedance-2-0
description: |
  使用字节跳动 Seedance 2.0 生成电影级剪辑 — OpenMontage 中首选的高级视频模型。在以下情况下使用：(1) 制作预告片、预告花絮、宣传剪辑或高级电影片段，(2) 需要单次生成中自带原生同步音频（语音、音效、环境音），(3) 需要一次生成内包含多镜头切换，(4) 需要导演级摄像机控制，(5) 需要提示词中引用对话的口型同步，(6) 需要最多 9 张图片 + 3 个视频片段 + 3 个音频片段的参考条件生成，(7) 需要跨镜头一致的角色身份。可通过火山引擎 Ark（`seedance_video` 工具，中国大陆直连）、HeyGen（Video Agent / Avatar Shots）、Replicate、Runway（企业版，非美国）、Freepik、BytePlus ModelArk、Higgsfield、Pollo 和其他聚合器访问。
allowed-tools: Bash, Read, Write
metadata:
  openclaw:
    requires:
      env_any:
        - ARK_API_KEY
        - HEYGEN_API_KEY
        - REPLICATE_API_TOKEN
---

# Seedance 2.0（字节跳动）

Seedance 2.0 是字节跳动 Seed 团队的统一多模态视频+音频模型（2026 年 2 月发布，2026 年 4 月通过合作伙伴 API 全球可用）。它是 OpenMontage 中电影、预告片、预告花絮和运动导向工作的**首选高级默认**，只要配置了任何支持的网关。OpenMontage 直接封装了四个网关（`seedance_video` → 火山引擎 Ark、`seedance_replicate` → Replicate、`runway_video` with `model="seedance_2.0"` → Runway、`higgsfield_video` with `model="seedance_2.0"` → Higgsfield）；BytePlus / Freepik / HeyGen-Video-Agent 封装在路线图中。评分引擎通过 `provider="seedance"` 去重，因此用户配置的任何网关都会自动胜出 — 代理应向 `video_selector` 传递 `preferred_provider="seedance"`（或让评分器选择），而不是按名称路由到特定网关。

## ⚠️ 提示词语言硬性规则

**所有传递给 Seedance 的提示词必须使用中文编写。** 仅以下内容可用英文（专业影视术语）：

✅ 允许的英文术语（仅限于无优质中文替代的专业词汇）：
- 镜头语言：`wide shot`, `close-up`, `dolly in`, `tilt up`, `rack focus`, `handheld`, `slow motion`, `POV`, `low angle`, `bird's eye`
- 拍摄术语：`ARRI ALEXA`, `anamorphic`, `cinematic`, `photorealistic`, `35mm film`, `chromatic aberration`, `motion blur`, `halation`, `vignette`
- 身份锁定短语：`the same character`, `consistent across all shots`, `no drift`, `no deformation`, `no face morph`
- 镜头编排：`Shot 1`, `Shot 2`, `Cut to`, `RAMPS TO SLOW MOTION`, `SNAPS BACK TO REAL TIME`

❌ 禁止的英文用法：
- 场景描述必须用中文（"a cat playing piano" → "一只猫在弹钢琴"）
- 主体/动作/环境描述必须用中文
- 风格/氛围/色调描述必须用中文
- 提示词结构和格式说明必须用中文

> **原因**：Seedance 2.0 通过火山引擎 Ark 调用，底层模型对中文的理解精度远高于英文。中文场景描述能更准确地控制生成结果，降低语义漂移。专业影视术语因在训练数据中以英文出现为主，保留英文能保持其精确含义。

## 为什么它是 OpenMontage 高级默认

| 能力 | Seedance 2.0 | 备注 |
|---|---|---|
| 单通道原生同步音频 | 是 | 语音 + 音效 + 环境音联合生成，非后期同步 |
| 一次生成内多镜头 | 是 | 单个提示词中的多个切/镜头 |
| 导演级摄像机控制 | 是 | 遵循镜头语言（dolly、tilt、arc、crane、handheld） |
| 引用对话的口型同步 | 是 | `Character says: "..."` 匹配嘴型 |
| 参考条件 | 最多 9 张图片 + 3 个视频片段 + 3 个音频片段 | 12 资产多模态 |
| 角色身份一致性 | 是 | 面部/主体跨镜头稳定 |
| 最大镜头时长 | 15 秒 | auto / 4–15 秒 |
| 分辨率上限 | 某些端点支持 1080p（Ark 默认 720p） | 取决于提供商 |
| Elo（Artificial Analysis） | 1269（截至 2026 年 2 月 #1） | 超越 Veo 3、Sora 2、Runway Gen-4.5 |

仅在以下原因时切换：预算严格（使用 `fast` 变体或 LTX）、用户偏好的提供商（VEO/Sora/Kling）、或风格适配更倾向于其他模型。

## 提供商界面

| 界面 | 环境变量 | OpenMontage 工具 | 状态 | 备注 |
|---|---|---|---|---|
| **火山引擎 Ark**（主要） | `ARK_API_KEY` | `seedance_video` | ✅ 已封装 | 直连字节跳动 Seedance 2.0，中国大陆网络友好。支持 T2V、I2V、参考转视频；`standard` 和 `fast` 变体。OpenMontage 中的默认。 |
| **Replicate** | `REPLICATE_API_TOKEN` | `seedance_replicate` | ✅ 已封装 | `bytedance/seedance-2.0` + `bytedance/seedance-2.0-fast`。标准 Replicate 预测 API。 |
| **Runway** | `RUNWAY_API_KEY` | `runway_video` (model: `seedance_2.0`) | ✅ 已封装 | Runway 内的第三方 Seedance 2.0 模型。**无限/企业计划，仅限非美国地区**。通过 `model` 参数选择。 |
| **Higgsfield** | `HIGGSFIELD_API_KEY` + `_SECRET` | `higgsfield_video` (model: `seedance_2.0`) | ✅ 已封装 | 此工具上 Seedance 2.0 是默认模型。强调角色身份 + 长格式链式生成。 |
| **HeyGen** | `HEYGEN_API_KEY` | `heygen_video`（仅 1.x）+ TODO | ⚠️ 仅 1.x | HeyGen 上的 `seedance_pro` / `seedance_lite` 工作流提供商字符串映射到 Seedance 1.x。2.0 访问通过 Video Agent / Avatar Shots 端点 — 一个单独的 `seedance_heygen` 工具在路线图中。 |
| **BytePlus ModelArk / 火山引擎** | BytePlus 令牌 | 未封装 | 🔜 路线图 | 字节跳动直连。Pro 约 $0.15 / 5 秒，Lite 约 $0.010/秒。基于令牌。 |
| **Freepik** | Freepik 令牌 | 未封装 | 🔜 路线图 | `POST /v1/ai/image-to-video/seedance-pro-1080p` 用于 1080p I2V |
| **Pollo / PiAPI / Atlas Cloud / AIMLAPI** | 各不不同 | 未封装 | 🔜 路线图 | 聚合器转售字节跳动端点 |

### 火山引擎 Ark Endpoint ID（由 `seedance_video` 使用）

`seedance_video` 工具通过火山引擎 Ark API 直连，使用推理接入点（Endpoint）调用模型：

```
# 默认 Endpoint ID 可通过环境变量 SEEDANCE_ENDPOINT_ID 覆盖
ep-20260707160030-dt7sw
```

支持的模型变体通过 Ark 的 content 参数控制。

定价（火山引擎 Ark，720p）：标准约 $0.06 / 秒（T2V/I2V 同价）。快速变体约 $0.04 / 秒。
`fast` 变体以部分镜头/运动保真度为代价换取延迟和成本 — **不要**将慢动作、多镜头或推拉密集提示首次尝试路由到 `fast`。

## 在 OpenMontage 中调用 Seedance 2.0

始终通过 `video_selector` 使用 `preferred_provider="seedance"`（或让评分引擎选择）：

```python
from tools.tool_registry import registry
registry.ensure_discovered()
selector = registry.get("video_selector")
result = selector.execute({
    "prompt": PROMPT,
    "preferred_provider": "seedance",
    "operation": "text_to_video",       # 或 image_to_video / reference_to_video
    "aspect_ratio": "21:9",             # 21:9 / 16:9 / 9:16 / 4:3 / 1:1 / 3:4
    "duration": "10",                   # auto / 4..15
    "resolution": "720p",               # 480p / 720p
    "output_path": "projects/<proj>/assets/video/clip_01.mp4",
})
```

仅在必须绕过选择器时直接调用提供商工具：

```python
seedance = registry.get("seedance_video")
seedance.execute({
    "prompt": PROMPT,
    "model_variant": "standard",   # "standard" 或 "fast"
    "operation": "text_to_video",
    "aspect_ratio": "21:9",
    "duration": "10",
    "resolution": "720p",
    "generate_audio": True,
    "seed": 12345,                 # 可选，用于可重现的变体
    "output_path": "...",
})
```

## 提示词结构 — Higgsfield 方法论（截至 2026 年的规范）

**关键：每个提示以镜头结构声明开头。** Seedance 奖励在创造性描述之前声明格式的提示。这是最大的质量杠杆。

### 开头模板（复制一个逐字使用，然后扩展）

**对于动作/战斗/多镜头（效果最好的格式）：**
```
Montage, multi-shot Hollywood action, don't use one camera angle or single cut, cinematic lighting, photorealistic, 35mm film quality, ARRI ALEXA aesthetic, heavy film grain, sharp but imperfect focus, motion blur on fast actions, halation on highlights, soft highlight rolloff, wide-angle lens with strong distortion, subtle chromatic aberration near frame edges, no 3D, no cartoon, no VFX aesthetic.
```

**对于单 POV 连续镜头（球体视角、漫游）：**
```
Single continuous shot, first-person POV perspective, the camera IS [his/her] eyes, hyper-chaotic handheld motion, completely unstabilized, violent raw human movement, constant micro-jitters, aggressive head swings, abrupt jerks, frequent over-rotation, no smoothness at all, no cuts, no zoom, 35mm film, photorealistic.
```

**对于锁定 POV 反应场景：**
```
One continuous shot, POV [setting] perspective, no cuts, no zoom, natural head movement, photorealistic, 35mm film grain.
```

### 主体结构（开头之后）

1. **环境/位置** — 感官细节（湿沥青、钠灯、霓虹渗色、雨水微粒、体积雾）
2. **角色块** — 带参考标签和身份锁定语言（见下方参考转视频）
3. **敌人/次要角色块** — 相同细节级别
4. **逐拍编排** 带时间标记：`0–3s: … 3–6s: … 6–10s: …`
5. **VFX 在括号内联：** `[VFX: branching white-blue electric arcs pulsing along forearms, sparks jumping between fingers]`
6. **慢动作标记：** 在冲击节拍前写 `RAMPS TO SLOW MOTION`，在恢复时写 `SNAPS BACK TO REAL TIME`
7. **声音设计块：** 要么 `no music, only raw SFX`，要么显式 SFX 序列。音乐语言保持质感。

### 战斗词汇（已验证有效）

- `snaps forward`、 `lunges`、 `sprints`、 `weaves`、 `chambers`、 `drives`、 `pivots`、 `redirects`、 `ducks`、 `slips`
- `explodes outward`、 `devastating`、 `raw force`、 `kinetic`、 `overload`、 `compresses`、 `erupts`、 `fractures`、 `ripples`
- 避免软动词：`attacks`、`hits`、`fights` — 这些读起来太通用，Seedance 在此表现不佳

### 摄像机行为 — 说明它正在和没有做什么

当摄像机意图不明确时，Seedance 会出错。始终显式否定你不想要的：
- `no cuts`（用于连续 POV）
- `no zoom`（防止不自然的透视推入）
- `no stabilization`（当你想要混乱的手持效果时）
- `no smoothness at all`
- `no 3D, no cartoon, no VFX aesthetic` — 反直觉，但强制照片级皮肤/纹理/光照，即使场景有大量 VFX 元素

### 真实感强化短语

当需求有 VFX 但你想要照片级皮肤/纹理（非塑料漫威卡通效果）时，包含：
```
no 3D, no cartoon, no VFX aesthetic — photorealistic textures, real skin pores, authentic fabric detail, grounded in reality
```

### 格式优先级（Higgsfield 经验排序）

| 格式 | 最适合 | 模式 |
|---|---|---|
| **变形** | 平静 → 威胁 → 变形 → 后果 | 6 个编号镜头 × 每镜头 2.5 秒 @ 共 15 秒 |
| **球体视角** | 单一连续 POV | 1 镜头 × 15 秒，极度混乱手持 |
| **战斗** | 战斗编排 | 逐拍，明确力量差距，RAMPS/SNAPS |
| **POV** | 锁定反应 | 连续，"no cuts no zoom" 咒语 |
| **动画** | 风格化 3D | `@image` 关键帧 + 定时段 |

**每镜头 2.5 秒节奏** 在多镜头生成中似乎是最优的。

## 遗留 8 部分模板（仅用于简单单镜头，非动作）

Seedance 2.0 对镜头语言、多镜头切换和引用对话异常字面。使用此 8 部分模板：

```
[Shot / framing] + [Camera movement] +
[Subject description — physical detail that must persist across shots] +
[Action beat 1] → [optional cut] → [Action beat 2] +
[Setting / environment] + [Lighting / palette] +
[Style / grade / era] + [Audio — ambient, diegetic, music, dialogue]
```

### 一次生成内的多镜头

Seedance 接受提示中的显式镜头列表。格式化每个镜头：

```
Shot 1 (wide establishing, slow aerial push-in): ...
Shot 2 (medium close-up, handheld): ...
Shot 3 (extreme close-up, rack focus): ...
```

保持主题描述跨镜头一致以实现身份稳定。

### 引用对话的口型同步

```
Aang stands on the cliff edge, staff raised, wind in his cloak.
Aang says: "I won't run anymore."
Sokka, half a step behind, replies: "Then we fight."
```

准确使用 `Character says: "..."` / `Character replies: "..."` — 嘴型以引用字符串为关键。每行保持在约 6 个词以下；较长的行在快速片段中可能漂移。

### 有效的音频提示

环境音：`distant thunder rolling over mountains`、`wind through reeds`、`crackling campfire`
叙事内音效：`boots crunching snow`、`staff planting on stone`、`wingbeats overhead`
音乐方向（轻触）：`low orchestral swell building`、`taiko drums entering on Shot 3`
**不要**请求复杂的多乐器配乐 — 保持音乐语言质感。

### 多角色参考图引用（Ark API `@ImageN` 语法）

火山引擎 Ark API 使用 content 数组的**图片顺序**作为引用标识：

- content 中第 1 张参考图 → prompt 中用 `@Image1` 引用
- content 中第 2 张参考图 → prompt 中用 `@Image2` 引用
- 依此类推（序号从 1 开始，按在 `reference_image_paths`/`reference_image_urls` 中的顺序）

```python
inputs = {
    "prompt": (
        "@Image1 是角色「林月」— 黑色长发, 红色劲装, "
        "the same character, maintain exact appearance, no drift.\n"
        "@Image2 是角色「云澈」— 银白短发, 蓝色长袍, "
        "the same character, maintain exact appearance, no drift.\n"
        "Shot 1: 林月与云澈在竹林中对峙..."
    ),
    "reference_image_paths": [
        "char_yue_combined.jpg",  # → @Image1
        "char_yun_combined.jpg",  # → @Image2
    ],
}
```

每个角色必须有独立的身份锚定语句。关键短语：
- `the same character`
- `consistent across all shots`
- `maintain exact appearance from @ImageN`
- `no deformation, no drift, no face morph`

### 参考转视频

当你有人物/产品/服装参考时，使用参考转视频端点。Seedance 2.0 接受显式的括号标签语法：

```
[reference_image: hero_portrait.png]
[identity_lock]
The same character — bald, blue arrow tattoo, orange robes — consistent across all shots, no drift or deformation. Do not alter clothing category or primary color.

Shot 1 (wide, slow push-in): hero walks across the snowy Air Temple courtyard, wind lifting robes.
Shot 2 (medium close-up): hero turns toward camera, staff in hand.
Shot 3 (extreme close-up, rack focus): hero's eyes open, wind whipping.
```

**可测量减少面部漂移的身份锚定短语**（堆叠它们 — 冗余有帮助）：
- `the same character`
- `consistent across different scenes / all shots`
- `maintain exact appearance from reference image`
- `no deformation, no drift, no face morph`
- `Do not alter clothing category or primary color`

**单参考工作流（实践中常见）：** 当你只有一张照片时：
- 使用清晰、正面的肖像，光线中性，最小运动模糊；避免遮挡的面部（如手机、太阳镜、重度阴影）
- 在所有镜头中复用**同一张**参考图片 — 不要为每个镜头生成新参考
- 将所有镜头放在一个提示中的单个 `[identity_lock]` 块下，使模型将其视为连贯序列
- 如果服装按设计改变（例如便装 → 戏服），在其出现的每个镜头上逐字描述戏服，并添加 `Do not alter clothing category or primary color` 以在生成后锁定

**抗漂移回退：** 如果面部在首次渲染时跨帧变形，降到更短的时长（5-6 秒而非 10 秒），收紧身份锁定语言，如果你有多张参考图片，减少到最一致的 3 张而非用 9 张泛滥。

## 参数指导

| 参数 | 指导 |
|---|---|
| `duration` | 主角镜头用 `5`–`8`，带多镜头切换的全场景用 `10`–`12`，快速插入用 `4`。不确定时用 `auto`。 |
| `aspect_ratio` | 电影预告片用 `21:9`，广播/YouTube 用 `16:9`，Reels/Shorts/TikTok 用 `9:16` |
| `resolution` | `720p` 默认。降级到 `480p` 用于成本上限的批量预览，最终渲染不用 |
| `generate_audio` | 保持**开启**，除非你有关闭音频的特定原因 — Seedance 的护城河是同步音频。如有需要可在合成中下游剥离音频。 |
| `model_variant` | 主要/电影镜头用 `standard`；仅 B-roll、预览或延迟是硬约束时用 `fast` |
| `seed` | 在迭代所选镜头的变体前设置种子 — 其他所有参数保持不变 |

## 应避免的事项

| 不要 | 原因 |
|---|---|
| 在一个镜头中塞入四个以上同时发生的角色动作 | 运动连贯性断裂；拆分为多镜头 |
| 要求片段内包含可读文字/标志 | 文字渲染不可靠 — 在 Remotion 覆盖层中处理文字 |
| 混合冲突的光照（"bright noon" + "neon night"） | 模型选择一个并忽略另一个 |
| 在快速剪辑镜头上写超过约 6 词的对话 | 口型同步漂移 |
| 对慢动作、多镜头或复杂相机移动使用 `fast` 变体 | 首次尝试通常会失败 — 路由到 `standard` |
| 通过 Seedance 音频生成音乐 | 仅质感没问题；真正的配乐使用 `music` / `pixabay_music` / `elevenlabs` 并在合成中混合 |
| 无理由绕过 `video_selector` | 丧失成本/可用性/回退处理和评分上下文 |

## 迭代策略

1. **勾勒形状** — 用单个 `duration=5` `fast` T2V 传递以目标构图进行。确认构图可行。
2. **锁定种子** — 在构图可读后锁定种子。
3. **升级到 `standard`** — 使用相同种子，收紧镜头和光照语言。
4. **扩展并添加镜头** — 仅在单镜头版本干净后，才转向多镜头或更长时长。
5. **保留每个片段的 README** — 为每个通过的镜头保存提示 + 种子 + 变体，以便合成阶段可以重新渲染一致的重拍。

## OpenMontage 管线的集成说明

- **电影管线：** Seedance 2.0 是默认视频模型。主角用 21:9，蒙太奇节拍用多镜头，当需求有视觉圣经时用参考转视频。
- **动画解说：** 仅将 Seedance 2.0 用于建立/氛围镜头；大多镜头应保留在 Remotion 中。不要用 Seedance 替换 Remotion 动态图形 — 不同的工具，不同的工作。
- **屏幕演示 / 播客 / 剪辑工厂：** Seedance 不是正确的默认 — 这些以素材为导向。仅用于风格化的开场。
- **成本纪律：** `standard` 在 10 秒时约 $3.03/片段。在提案阶段据此预算。`fast` 在 5 秒时约 $1.21 用于预览。

## 每个 Seedance 镜头的验证清单

- [ ] 在所选镜头长度下运动连贯可读
- [ ] 音频实际同步（检查对话 + 脚步/冲击节拍）
- [ ] 角色身份匹配参考/先前镜头
- [ ] 镜头方向匹配提示词（当你要求静态时没有自动推拉）
- [ ] 没有模型试图渲染的可读文字
- [ ] 色调匹配已批准的风格手册
- [ ] 输出时长匹配请求值（某些端点会取整）

## 参考资料

- 火山引擎 Ark Seedance 2.0：https://console.volcengine.com/ark
- 火山引擎 Ark API 文档：https://www.volcengine.com/docs/
- Replicate bytedance 集合：https://replicate.com/bytedance
- HeyGen Seedance 2.0：https://www.heygen.com/blog/introducing-seedance-2-and-heygen
- Runway Seedance：https://runwayml.com/product/seedance
- BytePlus Dreamina Seedance 2.0：https://www.byteplus.com/en/product/seedance
- Freepik Seedance 2.0：https://www.freepik.com/seedance-2
- Higgsfield Seedance 2.0：https://higgsfield.ai/seedance/2.0
- Pollo Seedance 2.0：https://pollo.ai/m/seedance/seedance-2-0
- 字节跳动 Seed 官方：https://seed.bytedance.com/en/seedance2_0
- Seedance 2.0 Wikipedia：https://en.wikipedia.org/wiki/Seedance_2.0
