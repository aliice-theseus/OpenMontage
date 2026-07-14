# 资产导演 - 纪录片蒙太奇流水线

## 使用时机

镜头列表已存在。你现在必须实际去寻找填充每个槽位的剪辑片段。有两条路径：

### 标准路径：语料库 + CLIP 检索

1. **构建语料库** — 将场景导演的查询分发到所有可用的素材来源（Pexels、Pixabay Video、Coverr、Mixkit、Archive.org、NARA、Library of Congress、Pond5 PD、Videvo、NASA、ESA、JAXA、NOAA、Dareful、Wikimedia、Unsplash）并下载/嵌入候选素材。
2. **按槽位选择** — 对语料库运行 CLIP 检索，使用每个槽位描述，为每个槽位选出一个胜者。

最佳用于：50+ 槽位的制作、自动化多样化、无需手动干预的 CLIP 相似度排序槽位填充。

### 快速路径：直接搜索（推荐用于逐幕制作）

1. **搜索并下载** — 使用 `direct_clip_search` 分发到所有可用的提供者，每个查询下载 2-3 个剪辑片段。无需 CLIP 嵌入、无语料库索引、无 .npy 文件。
2. **检查缩略图** — 浏览提取的缩略图（或使用子代理）以验证视觉匹配槽位描述。
3. **将剪辑映射到槽位** — 基于视觉检查手动将最佳剪辑分配给每个槽位。

最佳用于：逐幕制作并在幕间进行用户审查、快速迭代、每幕少于 30 个槽位的制作。

**跨幕重用：** 在逐幕制作时，为较早幕下载的剪辑可以填充较晚幕的槽位。将代理指向先前下载的目录并重用符合新槽位描述的剪辑。这在生产中节省了 40-50% 的下载时间。

**并行工作流：** 当 `direct_clip_search` 在后台运行时，同时生成 TTS 旁白、构建音频混音、创建字幕和搜索音乐。这显著减少了总制作时间。

**回退：** 如果快速路径对特定槽位产生较差的视觉匹配，仅对那些槽位使用 `corpus_builder` + `clip_search`。这两种方法并不互斥。

输出是一个 `asset_manifest`，将每个槽位映射到恰好一个剪辑片段，包含完整的来源信息。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/asset_manifest.schema.json` | 工件验证 |
| 前置工件 | `state.artifacts["scene_plan"]["scene_plan"]` | 槽位描述 + 查询 + 首选来源 |
| 前置工件 | `state.artifacts["idea"]["brief"]` | `era_mix`、`sources_allowed`、`music_plan` |
| 工具（快速路径） | `direct_clip_search` | 轻量级多提供者搜索 + 下载 |
| 工具（标准路径） | `corpus_builder` | 使用 CLIP 嵌入填充检索索引 |
| 工具（标准路径） | `clip_search` | 根据槽位描述对剪辑排序 |
| 工具（可选） | `music_gen`、用户的 `music_library/` | 配乐基底 |

## 思维模型

语料库**不是**素材库。它是代理按需构建的搜索索引。你不是浏览它 — 而是查询它。

由此得出三条规则：

1. **先构建，后选择。** 永远不要在一个不包含该槽位查询族候选的语料库上调用 `clip_search.rank_for_slot`。排序会返回垃圾，你会浪费这个槽位。
2. **扩展，不替换。** 语料库是只追加的。如果一个槽位的检索较弱，添加更多查询并重新构建 — 不要从头开始。
3. **按槽位选择，不按剪辑选择。** 每个剪辑在最终剪辑中只属于一个槽位。使用 `exclude_ids` 防止重复使用。

## 儿童/童话内容 — 来源覆盖

当场景计划的 `metadata.tone` 或 `metadata.target_audience` 指示为儿童内容（童话、睡前故事、儿童解说片、动画故事）时，**覆盖正常的来源路由**，仅从 Pixabay Video 获取。

### 为什么仅用 Pixabay Video

Pixabay 的社区库包含数千个 AI 生成的幻想动画 — 发光森林、魔法景观、神奇生物 — 由创作者使用 Midjourney/Stable Diffusion 视频工作流上传。这些在儿童参与度上显著优于真实素材。没有其他免费来源在此风格上有可比的深度。

### 获取规则

1. **来源锁定。** 为所有查询设置 `sources: ["pixabay_video"]`。不要将真实素材提供者（Pexels、Dareful 等）与幻想剪辑混合 — 风格冲突会破坏儿童的沉浸感。

2. **查询重写。** 场景导演已经为幻想风格重写了槽位描述。如果你需要写回退查询，在前面加上幻想关键词：
   - 魔法关键词：`fairy tale`、`fantasy`、`enchanted`、`magical`、`glowing`、`dreamy`、`mystical`、`fairy`、`enchanted forest`、`magical world`
   - 示例：槽位需要"叶子上的毛毛虫" → 查询 `"fairy tale caterpillar magical forest glowing"`

3. **视觉一致性检查。** 下载后，验证所有剪辑共享 AI 生成的幻想美学。拒绝任何看起来像真实素材的剪辑 — 即使 CLIP 分数更高。在幻想蒙太奇中，一个真实的剪辑片段会打破魔幻效果。

4. **回退。** 如果 Pixabay 对一个槽位没有返回幻想结果，在尝试更广泛的术语之前，先用不同的幻想关键词重写查询。每个槽位两次重写。如果仍为空，向用户标记该槽位 — 不要悄悄替换为真实素材。

## 流程 — 快速路径（直接搜索）

在逐幕制作并在幕间进行用户审查时，或当总槽位数约在 30 以内时使用此方法。

### F1. 后台运行 `direct_clip_search`

在你并行处理旁白/音频/字幕时触发搜索：

```python
direct_clip_search.execute({
    "output_dir": "projects/<name>/assets/video/raw_act2",
    "queries": [
        {"query": "铯原子钟实验室", "slot_id": "slot_01"},
        {"query": "激光束实验室光学",   "slot_id": "slot_02"},
        {"query": "夜空中的卫星天线",        "slot_id": "slot_03"},
        # ... 每个槽位一个
    ],
    "sources": ["pexels", "pixabay_video", "coverr", "mixkit", "archive_org"],  # 或省略以搜索所有可用来源
    "clips_per_query": 3,
    "filters": {
        "min_duration": 3,
        "max_duration": 40,
        "orientation": "landscape",
        "min_width": 1280,
    },
})
```

**关键参数：**
- `clips_per_query=3` 是最佳值。足够的选择，快速下载。
- 省略 `sources` 以自动搜索所有可用提供者。
- 设置 `skip_existing=true`（默认）以避免重试时重新下载。

### F2. 检查缩略图

浏览 `<output_dir>/thumbnails/` 以验证每个剪辑。如果需要，使用子代理读取缩略图图像进行视觉确认。

对于每个槽位，从下载集中选择最佳匹配的剪辑。

### F3. 跨幕重用

在处理第 2-5 幕时，在下载新剪辑之前检查早期幕的剪辑。不同幕之间存在许多主题重叠：

- 实验室素材（显微镜、激光器、科学家）
- 技术镜头（服务器、卫星、电路）
- 自然/抽象素材（山脉、太空、延时摄影）

在运行新搜索之前，将代理指向先前的幕目录，并将现有剪辑映射到新槽位。

### F4. 用定向搜索填补空白

如果特定槽位在初始搜索后没有好的匹配：
1. 重写查询（更多具体名词，不同词汇）。
2. 仅用那些查询运行 `direct_clip_search`。
3. 如果仍无匹配，仅对那些特定槽位回退到 `corpus_builder` + `clip_search`。

### F5. 记录资产清单

格式与标准路径相同（见下面的步骤 9）。`source_tool` 字段应为 `"direct_clip_search"` 而不是 `"corpus_builder"`。

---

## 流程 — 标准路径（语料库 + CLIP 检索）

用于大型制作（50+ 槽位），当你需要自动化的 CLIP 排序，或快速路径产生较差匹配时。

### 1. 确定语料库目录

决定语料库的位置。惯例：

```
projects/<project-name>/corpus/
```

相同的 `corpus_dir` 被传递给每个 `corpus_builder` 和 `clip_search` 调用。语料库可跨多次运行重用 — 如果场景导演后来添加槽位，你可以扩展同一个语料库而不是从头重建。

### 2. 将查询分发到 `corpus_builder`

读取 `scene_plan.metadata.slots[]`。收集每个槽位的所有 `queries[]` 数组。去重。按 `preferred_sources` 分组。

每个来源集调用一次 `corpus_builder.execute(...)`：

```python
# 示例结构。代理从镜头列表构建此结构。
corpus_builder.execute({
    "corpus_dir": "projects/<name>/corpus",
    "queries": [
        {"query": "沥青上的雨滴慢动作", "kind": "video", "per_source": 8},
        {"query": "湿漉漉的城市街道夜晚霓虹灯",       "kind": "video", "per_source": 8},
        {"query": "出租车大雨黄色",           "kind": "video", "per_source": 6},
        # ... 每个唯一槽位查询一个条目
    ],
    "sources": ["pexels", "archive_org", "wikimedia"],   # 来自 preferred_sources 的并集
    "filters": {
        "min_duration": 3,
        "max_duration": 40,
        "orientation": "landscape",
        "min_width": 1280,
    },
    "max_new_clips": 150,          # 扩大搜索空间
    "thumbs_per_video": 5,
})
```

**分发规则：**

- 如果概要指定了一个来源且 `corpus_builder.source_provider_menu` 显示该来源不可用，**停止**并上报。不要悄悄降级到其余来源。
- 预算语料库为槽位数的 8-12 倍。15 个槽位的蒙太奇需要约 150 个候选，以便检索有真正的选择。
- 每个查询的 `per_source` 为 4-8 通常足够。推高到 20+ 主要用于增加噪音。
- 如果 `era_mix = "vintage"`，运行一个单独的仅限于 `["archive_org"]` 的分发，使用符合时代的查询。Prelinger 搜索很慢 — 不要将其与现代 Pexels 批次交错。
- 如果有任何槽位在 `preferred_sources` 中有 `nasa`，运行一个**小**的仅 `nasa` 批次。NASA 很慢且其结果是小众的。
- `unsplash` 仅限图片。将其用作支持来源，而不是运动主导的纪录片剪辑的骨干。

### 3. 在检索前对语料库进行合理性检查

在花费 token 进行槽位选择之前，调用 `clip_search` 并设置 `operation=stats`：

```python
clip_search.execute({
    "operation": "stats",
    "corpus_dir": "projects/<name>/corpus",
})
```

查看 `rows`、`per_source`、`per_kind`、`mean_motion_score`。你检查三种失败模式：

- `rows < 50` — 语料库太小。扩展它。
- `per_source` 严重偏斜（例如 98% pexels、2% archive_org）在复古概要上 — 运行一个定向的 archive_org 分发。
- `mean_motion_score < 1.0` — 语料库充满静态剪辑，会导致幻灯片效果。用不同的查询重新运行，或在排序时应用 `motion_min`。

### 4. 按槽位对候选排序

对于 `scene_plan.metadata.slots[]` 中的每个槽位，调用 `clip_search` 并设置 `operation=rank_for_slot`：

```python
clip_search.execute({
    "operation": "rank_for_slot",
    "corpus_dir": "projects/<name>/corpus",
    "query_text": slot["description"],      # 不是 slot["queries"] — 描述更丰富
    "k": 30 if slot.get("hero") else 12,
    "tag_weight": 0.3,
    "motion_min": 1.5,
    "kind": "video",
    "exclude_ids": already_picked_ids,      # 全局累加器
})
```

关键点：

- 使用槽位的 **description**，而不是 queries。描述是场景导演写的丰富的名词和形容词字符串。CLIP 对其排序效果优于短搜索短语。
- `tag_weight=0.3` 混合视觉嵌入（70%）与源标签嵌入（30%）。当 Pexels URL 标签强且视觉通道嘈杂时提升到 0.5。当标签是长篇散文时（如 Prelinger）降低到 0.15。
- 始终传递 `exclude_ids`，包含每个已锁定到槽位的剪辑，这样同一个钥匙在门的剪辑不会赢得两个槽位。

### 5. 用判断力选择，而非按分数

最高的结果不总是正确的选择。查看前 3-5 个，并根据以下标准判断每个：

- **年代匹配。** 2022 年的 4K Pexels 镜头适合一个关于家的挽歌式列表蒙太奇吗？也许。也许不。
- **运动匹配。** 场景导演的基调表告诉你停留时长。如果剪辑有 4.0 秒的停留目标但剪辑只有 2 秒长且带有快速的甩镜头，它撑不住。
- **构图传承。** 这个剪辑能与为相邻槽位选择的剪辑配合工作吗？你还不知道 — 但如果 slot_02 是雨中宽幅屋顶，而 slot_03 的最高匹配也是雨中宽幅屋顶，选择 #2 代替。
- **情感基调。** CLIP 会很乐意将"夜晚空无一人的城市人行道"匹配到明亮的霓虹 Vegas 切出镜头。霓虹镜头对挽歌式概要来说是**错误**的。分数 0.42 不能覆盖基调。

**可接受分数的经验法则（CLIP ViT-B/32 余弦）：**

- `>= 0.30` — 强匹配，通常可用。
- `0.22-0.30` — 可能，需要人类判断。
- `< 0.22` — 语料库不包含你需要的。扩展它，不要强行选择。

### 6. 当检索较弱时扩展语料库

如果一个槽位的最高分数低于 0.22，不要选择坏中之好。而是：

1. 重写槽位的查询 — 可能太抽象，可能用词不符合时代。
2. 仅用那个槽位的新查询再运行一次 `corpus_builder.execute(...)`。构建器会跳过索引中已有的剪辑，所以这是廉价的。
3. 重新排序。

每个槽位两次扩展就足够了。如果三次都无法找到高于 0.22 的分数，告诉创意导演该槽位无法从开放语料库中拍摄，并建议要么放弃该槽位，要么让用户提供素材。

### 7. 多样化相邻选择

一旦每个槽位有一个候选，你就有了一个按时间线顺序的 clip_id 列表。视觉冗余的相邻镜头会破坏剪辑。对列表运行 `clip_search.diversify`：

```python
clip_search.execute({
    "operation": "diversify",
    "corpus_dir": "projects/<name>/corpus",
    "candidate_ids": picked_ids_in_timeline_order,
    "n": len(picked_ids_in_timeline_order),
    "diversity": 0.5,
})
```

如果 `diversify` 丢弃了一个剪辑，它告诉你你的两个选择视觉相同。对剪辑被丢弃的槽位重新排序，在 `exclude_ids` 中包含存活的同类剪辑。

### 8. 处理音乐计划

读取 `brief.music_plan`。精确执行创意导演记录的计划 — 不要在这里发明新来源：

- **`source=library`**：验证 `music_plan.path` 处的文件存在。在资产清单中记录为 `type=music`、`subtype=library`。
- **`source=user`**：同上，`subtype=provided`。
- **`source=generated`**：调用命名的音乐工具，使用概要中的种子提示。先采样，确认情绪后再批量。记录提供者和成本。
- **`source=none`**：不要生成静音。不要因为剪辑感觉单薄就换入一个曲目。如果用户批准了"不要音乐"，按无音乐运行。

**绝不要在此阶段切换音乐来源。** 这是决策沟通合同违规 — 更改音乐模式是一个重大的制作变更，需要在提案时获得用户批准。

### 9. 记录资产清单

使用规范模式为每个槽位输出一个资产。纪录片蒙太奇特定字段放在 `metadata` 中：

```json
{
  "version": "1.0",
  "assets": [
    {
      "id": "asset_slot_01",
      "type": "video",
      "path": "projects/<name>/corpus/clips/pexels_12345/video.mp4",
      "source_tool": "corpus_builder",
      "scene_id": "slot_01",
      "duration_seconds": 7.2,
      "resolution": "1920x1080",
      "format": "mp4",
      "provider": "pexels",
      "license": "Pexels 许可（免费，无需署名）",
      "original_url": "https://www.pexels.com/video/12345",
      "subtype": "stock",
      "generation_summary": "通过 CLIP 排序为槽位 '沥青上的雨滴慢动作...' 检索。分数 0.38。"
    },
    {
      "id": "asset_music_bed",
      "type": "music",
      "path": "music_library/dawn_04.mp3",
      "source_tool": "music_library",
      "scene_id": "global",
      "subtype": "library",
      "license": "用户提供"
    }
  ],
  "metadata": {
    "pipeline": "documentary-montage",
    "corpus_dir": "projects/<name>/corpus",
    "corpus_stats": { "rows": 157, "per_source": {"pexels": 98, "archive_org": 52, "nasa": 7} },
    "rejected_picks": [
      {
        "slot_id": "slot_03",
        "clip_id": "pexels_99921",
        "score": 0.41,
        "reason": "年代错误 — 2022 年 4K 厨房，概要是复古风格"
      }
    ]
  }
}
```

`rejected_picks` 日志很重要。当选择感觉不对且需要用到 #2 选项时，剪辑导演会读取它。

### 10. 质量门

- 场景计划中的每个槽位恰好有一个资产映射到它。
- 每个选中的剪辑在 rejected-picks 日志中有 `score >= 0.22`（或记录了"用户批准的覆盖"说明）。
- 没有 clip_id 作为主要选择出现在两个槽位中。
- `diversify` 在最终列表上干净运行（没有丢弃的选择，或所有丢弃的选择被重新填充）。
- `corpus_stats` 显示行数至少为槽位数的 8 倍。
- 音乐资产存在或 `music_plan.source = "none"` 带有明确确认。
- 对于复古概要，至少 60% 的选择来自 `archive_org`。
- 所有文件路径可解析。

## 常见陷阱

- **在空语料库上运行 `clip_search.rank_for_slot`。** 你将得到一个空的 `results` 列表或一个难以理解的形状错误。在构建之后、排序之前，始终调用 `stats`。
- **仅按分数选择。** 分数是判断的输入，不是判断本身。一个充满高分 Pexels 高清阳光的挽歌式作品，无论分数如何都会感觉不对劲。
- **忘记 `exclude_ids`。** 没有它，同一个惊人的剪辑会赢得每个槽位，蒙太奇变成了一幅图像的幻灯片。
- **悄悄替换音乐。** 用户说了"不要"，代理却因为"剪辑感觉单薄"而生成。这是一个重大变更，需要批准 — 参见 `skills/pipelines/documentary-montage/executive-producer.md` 的跨阶段规则。
- **无限制地扩展语料库。** 每个弱槽位两次扩展是极限。超过这个，素材可能根本不在开放语料库中存在，槽位需要更改。
- **使用槽位查询作为排序文本。** 查询是用于素材 API 的搜索短语；描述是用于 CLIP 的语义文本。它们是不同的。用描述排序。
- **丢失来源信息。** 每个剪辑必须在清单中包含 `provider`、`original_url` 和 `license`。这些是任何下游发布步骤的不可协商项。

## 检索配方

一些经常出现的检索操作：

### "找到我喜欢的这个剪辑的 N 个变体"

```python
clip_search.execute({
    "operation": "find_similar_set",
    "corpus_dir": "projects/<name>/corpus",
    "seed_clip_id": "pexels_12345",
    "n": 5,
    "diversity": 0.4,
    "candidate_pool": 40,
})
```

当槽位想要"五个更多像这样的镜头"时使用 — 例如，以相同基调拍摄的门廊目录。

### "我有 20 个候选，修剪到 8 个非冗余的选择"

```python
clip_search.execute({
    "operation": "diversify",
    "corpus_dir": "projects/<name>/corpus",
    "candidate_ids": [...],
    "n": 8,
    "diversity": 0.5,
})
```

### "查找一个剪辑的完整元数据"

```python
clip_search.execute({
    "operation": "get",
    "corpus_dir": "projects/<name>/corpus",
    "clip_id": "archive_org_Prelinger_HomeMovies_0042",
})
```

当剪辑导演想在锁定剪辑前确认提供者/URL 时使用。
