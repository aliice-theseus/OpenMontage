---
name: prompt-optimizer
description: 为 HeyGen Video Agent 编写生产级提示词——从基本想法到完全导演级的逐场景脚本
---

# Video Agent 提示词优化器

为 HeyGen Video Agent API 编写有效的提示词。基于 40+ 个已制作视频的模式总结。

**核心见解：Video Agent 是一个 HTML 解释器。** 它原生渲染布局、排版和结构化内容。将 B-roll 描述为带有动作动词（"猛击入"、"逐字打出"、"递增计数"）的分层文字动态图形——而不是布局规范（"左上角，48pt"）。

## 参考文件

| 文件 | 何时使用... |
|------|-------------|
| [visual-styles.md](visual-styles.md) | 选择视觉风格（20 种风格及完整规格） |
| [prompt-examples.md](prompt-examples.md) | 从零编写提示词（完整生产示例 + 模板） |

## 工作流：从需求到提示词

1. **提取数据** — 研究主题：网页搜索、API、内部文档。收集真实的引用、统计数据、账号
2. **整合论点** — 不是列表。而是一个故事。*"因为 Y 所以发生 X——以下是证据。"* 按叙述弧线分组为 3-5 个主题
3. **选择风格** — 先匹配情绪，再匹配内容。问：*"应该让观众感受到什么？"* 参见 [visual-styles.md](visual-styles.md)
4. **编写头像** — 与内容情感上下文匹配的主题化着装。场景中的品牌标识和内容特定道具（参见下方头像指南）
5. **提取关键文本** — 列出必须逐字显示的每个数字、引用、账号和标签
6. **分解场景** — 一个场景一个概念。轮换场景类型。永远不要连续 3+ 个相同类型。至少 2 个纯 B-roll 场景
7. **编写旁白** — 旁白拼出数字（"一百八十五万"），屏幕使用数字（"185万"）。每个场景包括 B-roll 都要有旁白
8. **分层每个 B-roll 场景** — L1 背景，L2 主视觉，L3 辅助信息，L4 信息栏，L5 特效。每个元素必须**动起来**
9. **添加音乐指导** — 参考艺术家，描述能量弧线
10. **添加旁白风格** — 如何表达：快/慢，哪里停顿，每个段落的情绪基调

## 提示词结构

每个生产级提示词都遵循此结构：

```
FORMAT:    什么类型的视频，多长，什么能量
TONE:      情绪基调，参考
AVATAR:    详细的外貌 + 环境描述（60-100字）
STYLE:     已命名的美学风格，包含颜色、排版、动效规则、转场
CRITICAL ON-SCREEN TEXT:  必须出现的精确字符串
SCENE-BY-SCENE:  逐个场景分解，含旁白和分层视觉
MUSIC:     流派、参考艺术家、能量弧线
NARRATION STYLE:  如何表达旁白
```

### FORMAT（格式）

```
FORMAT: 75秒高强度科技每日简报。想象一个刚收到好消息的创作者。
FORMAT: 彭博社风格战略简报。100-120秒。CEO 亲自讲述。
```

### TONE（基调）

```
TONE: 自信、直接、数据支撑。亮点重锤。低点坦诚——不粉饰。
TONE: 前卫、朋克科技评论。Vice News 遇上 The Face 杂志——原始、对抗性。
```

### CRITICAL ON-SCREEN TEXT（关键屏幕文字）

列出必须在屏幕上显示的每个精确字符串。没有这个，agent 可能会总结、四舍五入数字或改写引用。

```
CRITICAL ON-SCREEN TEXT (display literally):
- "$141M ARR — All-Time High"
- "1.85M Signups — +28% MoM"
- Quote: "Use technology to serve the message, not distract from it." — Shalev Hani
- "@username" — exact social handle
```

### MUSIC & NARRATION（音乐与旁白）

```
MUSIC: 驱动型电子乐，关键数字处重低音。Run the Jewels 遇上科技主题演讲。
不停推进，仅在客户故事时柔和。

NARRATION STYLE: 全程高能。让数字重击——大数字前停顿，然后重重说出。
客户故事赋予温暖。结尾应像是麦克风掉落。
```

## 头像描述指南

**头像不是固定的头像照片**——像电影角色一样为每个视频设计。想象服装设计师 + 场景设计师。

### 主题化着装规则

头像的服装和环境必须与内容的情感/文化上下文匹配：

| 内容类型 | 头像设计 | 不要这样 |
|---|---|---|
| 春节 | 红色旗袍配金色刺绣，灯笼照亮的庭院 | "穿西装外套的记者" |
| 科技重磅新闻 | 现场记者，风吹凌乱的头发，耳机，城市天际线 | "坐在桌前的播报员" |
| 睡眠科学 | 超大奶油色针织衫，盘腿坐在床上，暖色台灯 | "实验室里的分析师" |
| Reddit 社区 | 凌乱的桌子，显示器上的 Reddit 外星人，墙上的点赞箭头 | "工作室里的研究员" |

### 需要指定的元素

| 要素 | 弱 | 强 |
|---------|------|--------|
| 服装 | "商务休闲" | "黑色罗纹美利奴高领毛衣，高领勾勒下颌线" |
| 环境 | "一个办公室" | "玻璃墙会议室。白板上手绘层级金字塔" |
| 显示器内容 | "电脑屏幕" | "显示器显示滚动的绿色终端文本和红色安全警报" |
| 灯光 | "光线充足" | "左侧冷蓝色显示器光，右侧暖琥珀色台灯光" |

### 模板

```
AVATAR: [服装 — 面料、颜色、版型、配饰、姿势]。
[环境 — 特定道具、品牌标识、墙上的东西]。
[显示器/桌面 — 屏幕上可见的内容、桌上的物品]。
[灯光 — 方向、色温]。 [空间氛围]。
60-100字。3个以上内容特定道具。可见的品牌元素。
```

## 场景类型

| 类型 | 格式 | 何时使用 |
|------|--------|-------------|
| **A-ROLL** | 头像对着镜头说话 | 开场、关键见解、CTA、情感节点 |
| **FULL SCREEN B-ROLL** | 无头像 — 仅动态图形 | 数据可视化、信息密集型内容 |
| **A-ROLL + OVERLAY** | 分屏：头像 + 内容 | 呈现数据时保持人情味沟通 |

**轮换是强制性的。** 永远不要连续 3+ 个相同类型。每个提示词至少需要 2 个纯 B-roll 场景。

**每个场景都要有旁白。** 每个 B-roll 场景必须包含 `VOICEOVER:` 行。静音 B-roll = 无效视频。

### 场景结构

**A-ROLL：**
```
SCENE 1 — A-ROLL (10s)
[Avatar center-frame, excited, hands gesturing]
VOICEOVER: "The exact script for this scene."
Lower-third: "TITLE TEXT" white on blue bar.
```

**带分层的 B-roll：**
```
SCENE 2 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — motion graphic only]
VOICEOVER: "The exact script for this scene."
LAYER 1: Dark #1a1a1a background with subtle grid lines pulsing.
LAYER 2: "HEADLINE" SLAMS in from left in white Bold 100pt at -5 degrees.
LAYER 3: Three data cards CASCADE from right, staggered 0.3s.
LAYER 4: Bottom ticker SLIDES in: "supporting text scrolling continuously."
LAYER 5: Grid lines RIPPLE outward from impact point.
Hard cut.
```

**A-ROLL + OVERLAY：**
```
SCENE 3 — A-ROLL + OVERLAY (10s)
[SPLIT — Avatar LEFT 35%. Content RIGHT 65%. NO overlap.]
Avatar gestures toward content side.
VOICEOVER: "The exact script for this scene."
RIGHT SIDE: "HEADLINE" in cyan 60pt. Three stats COUNT UP below.
```

在重叠场景之间交替头像出现的一侧。

## 视觉分层系统

将 B-roll 分解为 5 个叠加层。这是动态图形场景最强大的技巧。

| 层 | 用途 | 示例 |
|-------|---------|---------|
| **L1** | 背景 | 纹理表面、网格、渐变、色场 |
| **L2** | 主视觉内容 | 主导画面的主标题/数字 |
| **L3** | 辅助数据 | 卡片、统计数据、要点、次要信息 |
| **L4** | 信息栏 | 滚动条、标签、来源说明、引用 |
| **L5** | 特效 | 粒子、故障、网格动画、环境动效 |

每个 B-roll：4 层以上。每个叠加内容侧：3 层以上。**每个元素必须动起来。**

## 动作词汇

### 高能量
| 动词 | 示例 |
|------|---------|
| **SLAMS（猛击）** | `"$95M" SLAMS in from left at -5 degrees` |
| **CRASHES（撞入）** | `Title CRASHES in from right, screen-shake on impact` |
| **PUNCHES（重击）** | `Quote card PUNCHES up from bottom` |
| **STAMPS（盖印）** | `Data blocks STAMP in staggered 0.4s` |
| **SHATTERS（碎裂）** | `Text SHATTERS after 1.5s, revealing number underneath` |

### 中等能量
| 动词 | 示例 |
|------|---------|
| **CASCADE（层叠）** | `Three cards CASCADE from top, staggered 0.3s` |
| **SLIDES（滑入）** | `Ticker SLIDES in from right — continuous scroll` |
| **DROPS（落下）** | `"TIER 1" DROPS in with white flash` |
| **FILLS（填充）** | `Progress bar FILLS 0 to 90% in orange` |
| **DRAWS（绘制）** | `Chart line DRAWS itself left to right` |

### 低能量
| 动词 | 示例 |
|------|---------|
| **types on（逐字打出）** | `Quote types on word by word in italic white` |
| **fades in（淡入）** | `Logo fades in at center, held for 3 seconds` |
| **FLOATS（漂浮）** | `Bokeh orbs FLOAT across frame at different speeds` |
| **morphs（变形）** | `Number morphs from 17 to 18.9` |
| **COUNTS UP（递增计数）** | `"1.85M" COUNTS UP from 0 in amber 96pt` |

## 转场类型

| 转场 | 能量 | 适合的风格 |
|------------|--------|---------------|
| Smash cut（猛切） | 激烈 | Deconstructed, Maximalist, Carnival Surge |
| White flash frame（白闪帧） | 有力 | Deconstructed, Maximalist |
| Grid wipe（网格擦除） | 系统化 | Swiss Pulse, Digital Grid |
| Hard cut（硬切） | 干净 | Swiss Pulse, Shadow Cut |
| Liquid dissolve（液体溶解） | 优雅 | Data Drift, Dream State |
| Slow cross-dissolve（慢交叉溶解） | 精致 | Velvet Standard |
| Pop cut / bounce（弹出/弹跳） | 有趣 | Play Mode, Carnival Surge |
| Snap cut（快速切） | 紧急 | Red Wire, Contact Sheet |
| Soft dissolve（柔和溶解） | 温暖 | Soft Signal, Warm Grain, Quiet Drama |
| Iris wipe（虹膜擦除） | 怀旧 | Heritage Reel |

## 时间指南

| 内容类型 | 时长 |
|--------------|----------|
| 钩子/开场（A-roll） | 6-10 秒 |
| 数据密集型 B-roll | 10-15 秒（永远不要 ≤5 秒——会导致黑帧） |
| A-roll + 叠加 | 8-12 秒 |
| CTA / 结尾（A-roll） | 6-8 秒 |

**常见视频长度：** 社交片段：30-45秒（5-7个场景）| 简报：60-75秒（7-9个场景）| 深度分析：90-120秒（10-13个场景）

**语速：** ~150字/分钟。计算：`字数 / 150 * 60 = 秒数`

## 无效模式

持续产生不良效果的模式：

**布局语言** — 屏幕坐标导致 B-roll 空白/黑屏：
```
❌ "UPPER-LEFT: headline in 48pt Helvetica"
❌ "CENTER-SCREEN: display at coordinates (400, 300)"
✅ "135K" SLAMS in from left, white Impact 120pt, fills 40% of frame.
```

**仅提艺术家名称而不给规格** — "Ikko Tanaka 风格"对 Video Agent 毫无意义。转化为具体规则：
```
❌ "Use an Ikko Tanaka style"
✅ "Flat color blocks, maximum 3 colors per frame, 60% negative space, typography as primary element"
```

**将风格示例注入提示词** — 风格库中的完整场景示例会混淆 agent。使用风格的**规则**，而不是示例场景。

**强制短 B-roll（≤5 秒）** — 太短无法渲染。每个测试过的 5 秒 B-roll 视频都有空白/黑屏。使用 10-15 秒。

**内容以列表而非故事呈现** — "这里有 5 条推文"会产生平淡的视频。始终整合：*"因为 Y 所以发生 X——以下是证据。"*

## 制作经验

### 风格表现（来自 40+ 视频）

| 排名 | 风格 | 优势 |
|------|-------|----------|
| 1 | Deconstructed (Brody) | 所有话题中最可靠 |
| 2 | Swiss Pulse (Müller-Brockmann) | 数据密集型内容最佳 |
| 3 | Digital Grid (Crouwel) | 科技话题表现出色 |
| 4 | Geometric Bold (Tanaka) | 优雅且多功能 |
| 5 | Maximalist Type (Scher) | 高能量，谨慎使用 |

### 不同方法下的时长

| 方法 | 平均时长 | 质量 |
|----------|-------------|---------|
| 自然分镜 + 自定义头像 | ~106秒 | 最佳 |
| 自然分镜，无自定义头像 | ~69秒 | 良好 |
| 强制短场景 + 自定义头像 | ~71秒 | 混合 |
| 布局语言提示词 | ~48秒 | 差 |

## 质量检查清单

- [ ] 论点驱动——故事，而不是要点
- [ ] 风格已命名，包含颜色、排版、动效、转场（参见 [visual-styles.md](visual-styles.md)）
- [ ] 头像具有主题化着装 + 品牌化环境（60-100字）
- [ ] 列出关键文字——每个统计数据、引用、标签
- [ ] 场景轮换类型——永远不要 3+ 相同类型。至少 2 个 B-roll 场景
- [ ] 每个场景都有旁白——包括 B-roll
- [ ] B-roll 场景有 4 层以上，每个元素都有动作动词
- [ ] B-roll 场景为 10-15 秒（永远不要 ≤5 秒）
- [ ] 讨论公司时出现品牌标识
- [ ] 每个元素都有动效——没有静态画面
