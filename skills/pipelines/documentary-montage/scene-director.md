# 场景导演 - 纪录片蒙太奇流水线

## 使用时机

概要已经存在。你现在必须将一个主题性问题转化为一个具体的**槽位**列表，供检索层填充。每个槽位是一个意图（"黄昏时门口的剪影"）加上能在现实世界中找到它的查询（Pexels/Archive.org/NASA/Wikimedia/Unsplash）。

这是流水线中最具创意的阶段。检索的质量取决于你写的槽位描述。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/scene_plan.schema.json` | 工件验证 |
| 前置工件 | `state.artifacts["idea"]["brief"]` | 主题性问题、基调、时长、结构 |
| 参考 | `skills/pipelines/documentary-montage/executive-producer.md` | 跨阶段规则 |
| 工具 | 暂时没有 — 此阶段纯属规划 | — |

## 思维模型

场景导演的工作**不是**"挑选剪辑片段"。而是"足够清晰地描述剪辑片段需要是什么样子，让 CLIP 能够找到它们"。

像外景勘察员一样思考，而不是素材库管理员。

- 素材库管理员说：*"城市蒙太奇中的雨，15 个剪辑片段"*。
- 外景勘察员说：*"蓝色时刻，雨斜着划过公交车窗，乘客面部柔和虚化，交通灯透过玻璃渗出血红和翠绿的光"*。

第二种是 CLIP 真正能排序的。第一种是一个分类标签，CLIP 会弱匹配且不加区分。

## 流程

### 1. 将结构转化为节拍数量

读取概要的 `duration_seconds` 和 `shape`。推导出槽位数量。除非基调另有要求，使用以下默认值：

| 基调 | 平均停留 | 每 60 秒槽位数 |
|------|--------------|---------------|
| 挽歌式 | 4.0 秒 | ~15 |
| 敬畏式 | 3.5 秒 | ~17 |
| 梦幻式 | 3.0 秒 | ~20 |
| 诙谐式 | 2.0 秒 | ~30 |
| 紧迫式 | 1.2 秒 | ~50 |

然后根据结构规划弧线：

- **列表式**：N 个均匀槽位，无转折。
- **前后对比式**：N/2 个前置槽位 + 1 个枢轴槽位 + N/2 个后置槽位。
- **三幕式**：建立（30%）→ 转折（40%）→ 释放（30%）。
- **单图扩展式**：1 个锚点图像 + N 个围绕它的变体。

在写任何槽位之前先写下班数。

### 2. 将主题性问题分解为具体的节拍

从概要中提取**一个**主题性问题，用感官语言回答。不是主题 — 而是质感。

**示例 — "雨水向你展示了一座城市的什么？"**

不好的分解（抽象，不可搜索）：

- "建立城市的情绪"
- "被困在天气中的感觉"
- "雨的普遍性"

好的分解（具体，可搜索）：

- 单个雨滴慢动作撞击干燥的沥青
- 门口打开的雨伞，一只手可见
- 霓虹灯招牌倒映在水坑中，上下颠倒
- 雨水划过公交车窗，乘客柔和虚化
- 出租车顶灯穿透大雨，长焦镜头
- 排水沟吞没落叶和水，俯拍
- 街头小贩在水果摊上拉塑料布
- 钨丝路灯下湿漉漉的鹅卵石上升起的蒸汽
- 孩子的橡胶靴踩进水坑
- 透过雨幕看到的亮着灯的公寓窗户

以上每一个都是一个**镜头**。每一个都是 CLIP 可排序的。每一个也是**同一个想法的不同角度**，这正是让列表式蒙太奇具有分量的原因。

### 3. 写槽位描述

每个槽位携带一个 `description` 字段。这是 CLIP 将嵌入并排序的文本。写得像好的素材片段标签字符串 — 名词和形容词，没有意图动词，没有情感词汇。

**模板：**

```
<主体>, <动作/姿态>, <环境>, <光线>, <年代/质感提示>
```

**好的：**

- `"单个雨滴撞击干燥沥青，特写，慢动作，温暖的路灯辉光"`
- `"雨后夜晚空无一人的城市人行道，倒映的霓虹灯，手持拍摄，1970 年代颗粒感"`
- `"门口打开的雨伞，手可见，散射的午后光线，浅景深"`

**不好的：**

- `"回家的感觉"` — 情感词，没有主体
- `"一个温暖欢迎的时刻"` — 形容词堆砌，没有图像
- `"有人以象征性方式穿过一扇门"` — 意图，没有镜头

经验法则：如果你无法从描述中想象出一张具体的照片，CLIP 也不能。

### 4. 每个槽位写 2-3 个查询

槽位描述是 CLIP 排序的依据。查询是 `corpus_builder` 用来填充候选池的。这是不同的工作，所以用不同的方式写。

给每个槽位一个包含 2-3 条目的 `queries` 数组：

1. **字面查询** — 最直接的素材搜索短语。Pexels 用户会输入的内容。`"raindrop on asphalt slow motion"`。
2. **侧面查询** — 从不同角度或尺度的同一个想法。`"wet pavement close up"`。
3. **联想查询**（可选，用于英雄槽位）— 一个相邻的概念，可能发现字面查询遗漏的质感剪辑。`"first rain city street"`。

对于素材搜索引擎来说，短查询优于长查询。每个 2-5 个词。没有填充词。

### 5. 按槽位定位来源（年代感知）

读取 `brief.era_mix`。根据素材所在位置为每个槽位分配一个或多个 `preferred_sources`：

| 来源 | 优势 | 使用时机 |
|--------|-----------|----------|
| `pexels` | 现代高清素材、干净的镜头、人物、城市、自然 | 现代/任何年代的默认选择 |
| `pixabay_video` | 大型社区库、自然、人物、技术、生活方式 | Pexels 缺失时的补充；广泛的通用素材 |
| `coverr` | 精选电影感 B-roll、自然、城市、抽象背景 | 高质量定场镜头、情绪营造、现代生活方式 |
| `mixkit` | Envato 精选高清/4K 素材、自然、商业、技术 | 高级感 B-roll、干净的自然素材、无需署名 |
| `archive_org` | Prelinger 家庭影片、20 世纪中期教育电影、1940s-1980s 质感 | 复古、诙谐、梦幻、任何怀旧内容 |
| `nara` | 美国国家档案馆 — 二战、冷战、阿波罗、民权、总统 | 美国历史纪录片、军事、政府、太空竞赛 |
| `loc` | 美国国会图书馆 — 早期电影、新闻短片、文化录音 | 1928 年前公有领域素材、美国历史、民间传统 |
| `pond5_pd` | Pond5 公有领域 — 一战/二战、早期电影、历史演讲 | 档案/复古素材、梅里爱、爱迪生、新闻短片 |
| `videvo` | 9 万+ 免费剪辑、自然、航拍、城市、抽象、延时摄影 | 大型免费库，以不同贡献者补充 Pexels |
| `nasa` | 地球轨道视图、天文学、飞行、宏大尺度影像 | 敬畏式、任何关于尺度、太空、星球、飞行的内容 |
| `esa` | 欧洲太空任务、哈勃/韦伯望远镜影像、地球观测 | 欧洲太空内容，为非美国任务补充 NASA |
| `jaxa` | 日本太空任务、隼鸟号、ISS 希望号实验舱、H-IIA 火箭 | 亚洲太空内容，太空探索的独特视角 |
| `noaa` | 深海 ROV 素材、海洋生物、珊瑚礁、天气、飓风 | 海洋/水下、独特的深海内容、天气现象 |
| `dareful` | 精品 4K 自然 — 山脉、森林、瀑布、延时摄影 | 高质量自然 B-roll、一致的视觉风格、航拍镜头 |
| `wikimedia` | 共享资源的照片和 CC 视频、公民/纪录片/公共事件报道 | 公共空间、地标、抗议、城市质感、教育素材 |
| `unsplash` | 精修社论风格照片、生活方式、产品相关摄影 | 当运动素材不足时的现代静态支撑镜头 |

如果 `era_mix = "vintage"`，将槽位偏向 `archive_org`，并使用符合时代特征的词汇编写查询（"通勤者"、"家庭主妇"、"郊区"而不是"网红"、"在家办公"、"共享办公"）。

如果 `era_mix = "any"`，按槽位混合来源 — 场景导演根据节拍的含义决定哪个槽位使用哪个来源。

#### 儿童/童话内容

当概要的 `tone` 或 `target_audience` 指示为儿童内容（童话、睡前故事、儿童解说片、动画故事）时，**将视觉策略从真实素材切换到 Pixabay 上的 AI 生成幻想剪辑**。

Pixabay 的社区库包含数千个 AI 生成的幻想动画（发光森林、魔法景观、神奇生物），在儿童参与度上显著优于真实素材。

**儿童内容的查询重写规则：**

| 槽位意图 | 真实素材查询 | 幻想重写 |
|-------------|-------------------|-----------------|
| 花园/自然 | `garden flowers morning` | `enchanted fairy tale garden glowing magical` |
| 昆虫/生物 | `caterpillar leaf close up` | `fairy tale caterpillar magical forest glowing` |
| 蜕变/茧 | `chrysalis butterfly cocoon` | `magical chrysalis enchanted tree glowing` |
| 蝴蝶/飞行 | `butterfly flying sky` | `fantasy butterfly glowing magical wings` |
| 日落/风景 | `sunset landscape golden` | `enchanted fantasy landscape magical sunset` |
| 雨/天气 | `rain leaves gentle` | `fairy tale rain magical forest enchanted` |
| 夜空/星星 | `milky way timelapse` | `fantasy night sky magical stars enchanted` |
| 海洋/水 | `river water golden` | `magical underwater world fairy tale` |
| 山脉/航拍 | `mountain peaks golden` | `fantasy mountain castle fairy tale magical` |
| 森林/树木 | `forest path morning` | `fairy tale mushroom forest glowing enchanted` |

**来源路由：** 为所有槽位设置 `preferred_sources: ["pixabay_video"]`。Pixabay 是唯一拥有深度 AI 生成幻想库的免费来源。不要将真实素材与幻想混合 — 风格冲突会破坏儿童的沉浸感。

**可找到 AI 幻想内容的关键词：** `fairy tale`、`fantasy`、`enchanted`、`magical`、`glowing`、`dreamy`、`mystical`、`fairy`、`enchanted forest`、`magical world`。

### 6. 标记英雄槽位

每个蒙太奇有 2-3 个整个作品依赖的槽位：开场画面、转折点、最终画面。在槽位元数据中用 `hero: true` 标记。

英雄槽位获得：

- 更长的停留（2-4 秒而不是基调的默认值）
- 在资产阶段更大的候选池（k=30 而不是 k=10）
- 更多查询（3 个而不是 2 个）

### 7. 为资产阶段留出余地

不要过度指定。资产导演的工作是根据你的描述对候选者排序。如果你同时确定了描述和具体剪辑片段，你就既做坏了资产导演的工作，又抢占了它的创意选择。

规则：像在电话中向研究助理描述槽位那样描述它 — 足够具体以被识别，又足够宽松以带来惊喜。

### 8. 记录镜头列表

使用 `scene_plan.schema.json` 工件，每个槽位一个 `scene`。对于本流水线，将纪录片蒙太奇特有的字段放在每个场景的 `metadata` 内。规范结构：

```json
{
  "version": "1.0",
  "scenes": [
    {
      "id": "slot_01",
      "type": "broll",
      "description": "单个雨滴撞击干燥沥青，特写，慢动作，温暖的路灯辉光",
      "start_seconds": 0.0,
      "end_seconds": 3.5,
      "narrative_role": "establish_context",
      "hero_moment": true,
      "texture_keywords": ["wet", "slow motion", "streetlamp"],
      "required_assets": [
        { "type": "video", "description": "沥青上的雨滴", "source": "source" }
      ]
    }
  ],
  "metadata": {
    "pipeline": "documentary-montage",
    "shape": "list",
    "tone": "elegiac",
    "thematic_question": "雨水向你展示了一座城市的什么？",
    "slots": [
      {
        "id": "slot_01",
        "description": "单个雨滴撞击干燥沥青，特写，慢动作，温暖的路灯辉光",
        "hero": true,
        "preferred_sources": ["pexels", "archive_org"],
        "queries": [
          "raindrop on asphalt slow motion",
          "wet pavement close up",
          "first rain city street"
        ],
        "min_duration": 3.0,
        "target_hold_seconds": 3.5,
        "era_hint": "any"
      }
    ]
  }
}
```

`scenes[]` 数组满足模式要求。`metadata.slots[]` 数组是资产导演实际读取的内容 — 它携带检索特定字段（`queries`、`preferred_sources`、`hero`、`era_hint`），这些字段是 `scene_plan.schema.json` 所不知道的。

### 9. 质量门

- 槽位数与步骤 1 中的节拍计数匹配。
- 每个槽位的 `description` 遵循名词和形容词模板 — 没有情感词，没有意图动词。
- 每个槽位有 2-3 个短查询（每个不超过 5 个词）。
- 至少 2 个槽位标记为 `hero`。
- `target_hold_seconds` 总和在 `brief.duration_seconds` 的 ±10% 以内。
- 如果 `era_mix = "vintage"`，至少 60% 的槽位在 `preferred_sources` 中列出 `archive_org`。
- `metadata.thematic_question` 与概要逐字一致（确认你没有偏离的合理性检查）。

## 常见陷阱

- **将槽位描述写成意图而不是画面。** "进入前的犹豫时刻"是剧本指导，不是 CLIP 查询。"一个女人静静站在门廊上，手靠近门把手"才是。
- **分类查询。** `"home"` 和 `"family"` 匹配一切而又什么都不匹配。推动使用具体名词：门、垫子、钥匙、大厅、鞋。
- **单查询槽位。** 第二个查询是廉价的保险 — 如果第一个查询返回垃圾，语料库仍然有可用的内容。
- **忘记时长计算。** 90 秒挽歌式大约是 ~15 个 ~6 秒的停留。如果你写了 40 个槽位，你就不小心设计了一个紧迫式的作品。
- **在复古概要把上跳过 `era_hint`。** Pexels 会用 2020 年代的高清素材淹没语料库并掩埋 Prelinger 素材。
- **让主题性问题漂移。** 如果概要说的是"回家"，而你的槽位列表有三个飞机镜头，作品将变成关于旅行而不是回家。起草后重新阅读概要。

## 工作示例 — "雨中一分钟"

- 时长：90 秒，挽歌式基调 → ~15 个槽位，每个 ~6 秒。
- 结构：列表式（天气 + 城市的目录）。
- 主题性问题："雨水向你展示了一座城市的什么？"

槽位草图（简写）：

1. **英雄** 单个雨滴慢动作撞击干燥沥青
2. 门口打开的雨伞，散射的午后光线
3. 霓虹灯招牌倒映在水坑中，手持拍摄
4. 雨水划过公交车窗，乘客柔和虚化
5. 出租车顶灯穿透大雨，长焦镜头
6. 排水沟吞没落叶和水，俯拍
7. 街头小贩在水果摊上拉塑料布
8. 湿漉漉的鹅卵石小巷，蒸汽上升，钨丝路灯
9. 灰色天空下的屋顶天线，广角
10. 孩子的橡胶靴踩水坑，低角度
11. **英雄** 透过雨幕看到的亮着灯的公寓窗户
12. 夜晚的雨刷，远处城市彩灯
13. 雨珠凝结在停放的自行车座上，微距
14. 火车站瓷砖地板上积水的脚印
15. **英雄** 第一片蓝天突破灰色云层

每个槽位获得：

- 名词和形容词模板的 `description`
- 2-3 个短查询（例如槽位 5：`"taxi heavy rain"`、`"yellow cab wet street night"`、`"city traffic downpour"`）
- `preferred_sources`（槽位 1-6 → pexels+archive_org，槽位 8 → archive_org 以获得时代质感，槽位 11 → pexels）
- 槽位 1、11、15 上设置 `hero: true`
- `target_hold_seconds` 总和约为 ~90

这是资产导演将执行检索的工件。
