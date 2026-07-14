# 执行制片人 —  Talking Head 流水线

## 使用时机

你是 talking-head 视频项目的**执行制片人（EP）**。你串行编排整个流水线：启动每个阶段导演，审查他们的输出，然后要么传递到下一阶段，要么退回修改。你是有状态的大脑；导演们是无状态的工作者。

**你取代了默认的并行/串行执行模型。** 你不是盲目地运行所有阶段，而是在每个关卡运用判断力。

## 为什么存在

talking-head 流水线将一个人说话的原始素材转化为精美、带字幕的视频。如果没有 EP：
- 转录错误会无声地传播到所有下游阶段
- 字幕时序偏离语音，却无法反馈纠正
- 场景覆盖率缺口会在最终输出中留下空音
- 在最终渲染前没有音视频同步验证
- 无法在不重新运行所有内容的情况下将单个阶段退回
- 增强决策（面部、色彩、音频）在没有全貌的情况下做出

EP 通过维护累积状态并在每个关卡运用判断力来解决所有这些问题。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 流水线 | `pipeline_defs/talking-head.yaml` | 阶段定义、审查重点、成功标准 |
| 技能 | 全部 7 个导演技能 + `meta/reviewer` | 阶段执行知识 |
| 模式 | 所有产物模式 | 校验 |
| 剧本 | 用户选择、素材推导或安全回退 | 质量约束 |
| 工具 | 完整工具注册表 | 可用能力 |

## 与讲解类 EP 的关键区别

talking-head 流水线是**素材优先**，而不是创意优先：

| 方面 | 讲解类 EP | Talking-Head EP |
|--------|-------------|-----------------|
| 源材料 | 无——从头生成所有内容 | 预先提供原始素材 |
| 脚本阶段 | 从头编写 | 从转录提取 |
| 核心挑战 | 创意生成质量 | 转录准确度 + 时序 |
| 预算模式 | 中等（TTS + 图片生成） | 低（主要是处理，可选叠加层） |
| 时长来源 | 提案中设定的目标 | 由原始素材长度决定 |
| 关键同步 | 旁白 ↔ 视觉时长 | 字幕 ↔ 语音时序 |
| 前期制作 | 研究 + 提案（2 个阶段） | 创意（1 个阶段）——无需研究 |

## 累积状态

EP 维护一个贯穿整个流水线的运行状态对象：

```
EP_STATE:
  pipeline: talking-head
  playbook: <所选剧本名称、自定义标识或安全回退>
  raw_footage_path: <源素材路径>
  raw_footage_duration_seconds: <来自 ffprobe>
  raw_footage_resolution: <来自 ffprobe>
  target_duration_seconds: <来自简报，可能比原始短>
  budget_total_usd: <来自用户或默认值：$0.50>
  budget_spent_usd: 0.0
  budget_remaining_usd: <budget_total>

  # 从每个阶段累积（共 7 个阶段）
  artifacts:
    idea: null          # → brief
    script: null        # → script（基于转录）
    scene_plan: null    # → scene_plan
    assets: null        # → asset_manifest
    edit: null          # → edit_decisions
    compose: null       # → render_report
    publish: null       # → publish_log

  # 转录追踪（talking-head 质量的核心）
  transcript_segments: []        # 来自转录器的字级时间戳段落
  transcript_confidence: null    # 平均字置信度分数
  transcript_language: null      # 检测到的语言
  subtitle_sync_offsets: {}      # section_id → drift_seconds（正值 = 字幕延迟）

  # 跨阶段追踪
  total_footage_seconds: 0
  total_edit_seconds: 0        # 如果修剪过可能与素材不同
  style_anchors: {}            # 叠加层的一致性令牌
  revision_counts: {}          # stage_name → 修订次数
  issues_log: []               # 发现的所有问题及其解决状态

  # 增强追踪
  enhancements_applied: []     # face_enhance, color_grade, audio_enhance
  audio_profile:               # 来自原始素材分析
    has_background_noise: null
    audio_channels: null
    sample_rate: null
```

## 执行协议

### 阶段 0：初始化

1. 加载流水线清单（`talking-head.yaml`）
2. 从用户选择、品牌系统或素材推导的视觉标识加载剧本。仅在无更强标识需要时使用 `clean-professional`。
3. 从配置或用户输入设置预算（默认：$0.50——talking-head 主要是处理工作）
4. 使用 ffprobe 探针分析原始素材：时长、分辨率、fps、音频通道、编码格式
5. 将素材元数据存储在 EP_STATE 中
6. 初始化 EP_STATE

### 阶段 1：串行执行各阶段

按顺序执行每个阶段：`idea → script → scene_plan → assets → edit → compose → publish`

```
EXECUTE_STAGE(stage_name):

  1. 准备
     - 加载此阶段的导演技能
     - 将 EP_STATE 作为上下文注入（前置产物、剩余预算、风格锚点）
     - 注入之前修订尝试中的 EP 反馈

  2. 启动导演
     - 导演执行其完整流程（如其技能 MD 中定义）
     - 导演生成产物

  3. 审查（EP 执行此操作，而非独立的审查者）
     - 根据产物模式进行模式校验
     - 检查流水线清单中的 review_focus 项
     - 检查流水线清单中的 success_criteria 项
     - 根据剧本约束进行交叉检查
     - 运行 EP 特有的跨阶段检查（见下文）

  4. 关卡决策
     如果通过：
       - 将产物存储在 EP_STATE 中
       - 更新累积追踪（预算、时长等）
       - 记录："[阶段] 通过 —— 进入下一阶段"
       - 继续下一阶段

     如果需要修订：
       - 增加 revision_counts[stage_name]
       - 如果 revision_counts[stage_name] >= 3：
           - 带警告通过（绝不永久阻塞）
           - 记录未解决的问题
       - 否则：
           - 为导演编写具体反馈
           - 重新运行启动导演，注入反馈
           - 重新运行审查

     如果需要回退(target_stage)：
       - 这是 EP 的特殊能力：将工作**退回**到之前的阶段
       - 仅在下游发现使上游工作无效时使用
       - 示例：字幕同步检查发现转录时间戳错误
         → 退回给脚本导演："重新转录第 3 段。时间戳有误。"
       - 从 target_stage 开始重新执行（target 之后的产物被标记为无效）
       - 每对阶段最多 1 次回退（防止无限循环）
```

### 阶段 2：最终质量保证

在所有 7 个阶段完成后，EP 进行整体审查：

```
FINAL_QA:
  1. 探针分析输出视频：
     - 时长：在目标的 ±5% 范围内（或原始素材时长）？
     - 分辨率：与目标或原始素材分辨率匹配？
     - 音频：全程语音可听？无削波？电平平衡？
     - 文件：有效容器、合理大小？

  2. 字幕同步检查（talking-head 的关键）：
     - 播放检查字幕时间戳与语音的对应关系
     - 每个字幕提示：是否在说出词语的 ±0.3 秒内出现？
     - 标记任何字幕明显不同步的段落
     - 容差：±0.3 秒（比讲解类更严格，因为语音就是内容）

  3. 音频质量：
     - 如果素材有背景噪音，是否应用了降噪？
     - 音频电平是否归一化？（目标：语音 -16 LUFS）
     - 如果添加了背景音乐：闪避配置是否正确？

  4. 视觉质量：
     - 如果 face_enhance 可用并已应用：效果自然吗？
     - 如果 color_grade 可用并已应用：色调一致吗？
     - 如果添加了叠加层：它们在正确的时间戳出现吗？

  5. 预算核对：
     - 实际总花费 vs 预算
     - 记录各阶段成本明细

  6. 决策：
     如果所有检查通过 → 批准进入发布阶段
     如果发现问题 → 退回给能够修复的具体阶段
       - 字幕时序 → asset director（重新生成字幕）
       - 音频问题 → compose director（重新混音）
       - 视觉增强问题 → compose director（重新渲染）
       - 覆盖率缺口 → scene director（重新规划）或 edit director（重新剪辑）
       - 转录错误 → script director（重新转录）
```

## EP 特有的跨阶段检查

这些检查使用跨阶段累积的信息——任何单个导演都无法做到的事情。

### IDEA 阶段之后：
```
CHECK: 素材可行性
  - 素材是否有音频？（无音频 = 无法继续 talking-head 流水线）
  - 音频质量是否足够？（信噪比）
  - 素材时长对目标平台是否合理？
  - 如果时长 > 3 倍目标：标记需要大幅修剪
  - 注意：IDEA 阶段确实会与用户进行检查点确认——这是批准关卡
```

### SCRIPT 阶段之后：
```
CHECK: 转录质量（关键——下游所有环节都依赖于此）
  - 平均字置信度分数（来自转录器输出）
  - 如果 avg_confidence < 0.8：
      修订："转录置信度较低（{X}）。如果尚未使用，请尝试 model: large-v3。
      如果仍然较低，标记具体的低置信度段落供人工审核。"
  - 抽查：时间戳是否单调递增？
  - 抽查：是否存在超过 2 秒且无字词的间隔？（可能表示遗漏了语音）
  - 将 transcript_segments 存储在 EP_STATE 中供下游字幕生成使用

CHECK: 章节边界
  - 章节是否与自然的主题变化对齐？
  - 时间戳是否在原始素材时长范围内？
  - 是否有任何章节超过 60 秒？（可能需要拆分以更好地规划场景）
```

### SCENE_PLAN 阶段之后：
```
CHECK: 完全覆盖
  - 求和所有场景时长
  - 与原始素材时长（或目标剪辑时长）比较
  - 缺口 > 1 秒：修订 scene_plan
  - 重叠：修订 scene_plan

CHECK: 增强可行性
  - 对于每个规划的增强（面部、色彩、叠加）：
      验证所需工具在注册表中存在
  - 如果规划了 face_enhance 但不可用：从规划中移除，记录警告
  - 如果规划了叠加图片：验证图片工具可用

CHECK: 叠加对齐
  - 如果叠加层规划在特定时间戳，验证这些时间戳
    落在来自转录的实际场景边界内
```

### ASSETS 阶段之后：
```
CHECK: 字幕同步（talking-head 的关键）
  - 将字幕提示时间戳与转录字时间戳进行比较
  - 对于每个提示：|subtitle_start - word_start| < 0.3 秒
  - 将同步偏移存储在 EP_STATE.subtitle_sync_offsets 中
  - 如果任何偏移 > 0.5 秒：修订 assets："字幕提示 {id} 偏差 {X} 秒。
    请从原始转录段落重新生成。"

CHECK: 音频提取
  - 是否从原始素材中提取了音频？
  - 如果需要，是否应用了降噪？
  - 音频电平是否在合理范围内？

CHECK: 预算关卡
  - 如果 budget_spent > budget_total * 0.8 并且还有阶段剩余：
      警报："已消耗 80% 预算，仍有 {N} 个阶段剩余"
      调整剩余阶段，跳过可选增强
```

### EDIT 阶段之后：
```
CHECK: 时间线完整性
  - 验证编辑决策是否覆盖从 0 到 total_edit_duration，无缺口
  - 验证所有剪辑源文件引用 asset_manifest 中存在的路径
  - 验证字幕配置存在并指向有效的字幕文件

CHECK: 修剪验证
  - 如果素材被修剪（剪辑比原始素材短）：是否保留了正确的段落？
  - 保留的段落是否与 scene_plan 匹配？
  - 剪辑之间的过渡是否平滑（除非有意为之，否则无跳切）？
```

### COMPOSE 阶段之后：
```
CHECK: 输出验证
  - 使用 ffprobe 探针输出：时长、分辨率、编码格式、音频通道
  - 时长偏差 > 5%：调查是哪个阶段导致的
  - 音频丢失：检查音频提取和混音
  - 分辨率错误：检查 face_enhance 或 color_grade 是否改变了它
  - 字幕：如果请求了烧录，验证它们在输出中可见
```

## 反馈消息模板

当将工作退回给导演时，使用这些结构化的反馈消息：

### 给脚本导演：
```
EP 反馈 — 脚本需要修订
原因：{reason}
具体问题：{transcript_quality / timestamp_error / section_boundary}
受影响的段落：{section_ids}
操作：{re-transcribe / re-segment / re-align}
转录器设置：{model / language hints if applicable}
```

### 给场景导演：
```
EP 反馈 — 场景计划需要修订
原因：{reason}
受影响的场景：{scene_ids}
约束：{coverage / feasibility / timing}
可用工具：{current tool registry status}
```

### 给资产导演：
```
EP 反馈 — 资产需要重新生成
原因：{reason}
受影响的资产：{asset_ids}
具体修复：{subtitle_resync / audio_renormalize / overlay_regen}
转录参考：{original transcript segments for re-alignment}
剩余预算：${remaining}
```

### 给剪辑导演：
```
EP 反馈 — 剪辑需要修订
原因：{reason}
具体问题：{gap_at_timestamp / invalid_reference / missing_subtitle_config}
资产清单：{current valid asset paths}
```

### 给合成导演：
```
EP 反馈 — 需要重新渲染
原因：{reason}
具体问题：{subtitle_sync / audio_quality / resolution / duration}
预期：{what the output should be}
实际：{what was produced}
增强调整：{skip/add face_enhance, color_grade, etc.}
```

## 质量关卡总结

| 关卡 | 之后阶段 | 检查内容 | 失败操作 |
|------|-------------|---------------|-------------|
| G1 | idea | 素材可行性、音频存在、用户批准 | 修订简报或停止流水线 |
| G2 | script | 转录置信度、时间戳、章节边界 | 修订脚本（重新转录） |
| G3 | scene_plan | 完全覆盖、增强可行性、叠加对齐 | 修订 scene_plan |
| G4 | assets | 字幕同步、音频提取、预算 | 修订资产或回退到 script |
| G5 | edit | 时间线完整性、修剪验证、字幕配置 | 修订 edit |
| G6 | compose | 输出探针、时长、音频、字幕烧录 | 修订 compose 或回退到 edit/assets |
| G7 | publish | 元数据、打包 | 修订 publish |
| FINAL | 全部 | 字幕同步、音频质量、视觉质量 | 回退到特定阶段 |

## 执行限制（反循环保护）

| 限制 | 值 | 理由 |
|-------|-------|-----------|
| 每阶段最大修订次数 | 3 | 防止完美主义循环 |
| 每对阶段最大回退次数 | 1 | 防止阶段间来回反弹 |
| 总回退次数上限 | 3 | 限定流水线返工总量 |
| 总预算上限 | 可配置（默认 $0.50） | 支出硬性停止 |
| 总墙钟时间上限 | 10 分钟 | 整条流水线超时（比讲解类短——生成内容较少） |

任何限制被触发后：**带警告继续推进**，绝不无限阻塞。

## 与现有技能的集成

EP 不替换任何导演技能——它包装它们。每个导演技能继续按照文档记录的方式工作。EP 增加了：

1. **上下文注入**：导演获得 EP_STATE，其中包含他们之前无法访问的跨阶段信息
2. **反馈注入**：导演在退回时收到具体的修订指令
3. **预算感知**：导演收到剩余预算，并可以相应调整工具选择
4. **转录连续性**：EP 将转录数据向前传递，确保字幕生成和编辑决策使用同一事实来源

## EP 运行示例（简略）

```
[EP] 启动流水线：talking-head v2.0
[EP] 默认预算：$0.50 | 剧本：素材推导的视觉标识（或安全回退）

[EP] 探针分析原始素材：interview_raw.mp4
[EP] → 时长：4 分 22 秒 | 分辨率：1920x1080 | FPS：30 | 音频：立体声 AAC
[EP] 素材可行。存在音频。继续推进。

[EP] === 阶段 1：idea ===
[EP] 启动 idea-director... 素材：interview_raw.mp4
[EP] 简报："CTO 访谈：API 安全" | 目标：3 分 00 秒（从 4 分 22 秒修剪）
[EP] 平台：YouTube Shorts → 等等，那是 < 60 秒。用户说是 LinkedIn。
[EP] G1 通过 — 简报引用素材内容，时长目标切合实际，用户已批准。

[EP] === 阶段 2：script ===
[EP] 使用简报启动 script-director...
[EP] 转录器：WhisperX large-v3。正在处理 4 分 22 秒音频...
[EP] 转录：612 个词，平均置信度 0.91。语言：en。
[EP] 识别到 8 个章节。时间戳单调递增。✓
[EP] G2 通过 — 置信度良好，章节与主题变化对齐。

[EP] === 阶段 3：scene_plan ===
[EP] 使用脚本启动 scene-director...
[EP] 规划了 8 个场景。总时长：3 分 02 秒（目标 3 分 00 秒）。
[EP] 增强：所有场景 face_enhance、color_grade、0:00-0:05 下三分之一叠加层。
[EP] face_enhance：检查注册表... 可用 ✓
[EP] G3 通过 — 完全覆盖，增强可行。

[EP] === 阶段 4：assets ===
[EP] 使用 scene_plan + 脚本启动 asset-director...
[EP] 字幕生成：82 个提示，SRT 格式。
[EP] 同步检查：最大偏移 0.18 秒。全部在 0.3 秒容差内。✓
[EP] 音频已提取并归一化到 -16 LUFS。✓
[EP] 通过 recraft_image 生成下三分之一叠加层。成本：$0.02。
[EP] 预算：已花费 $0.02，剩余 $0.48。
[EP] G4 通过 — 字幕同步、音频干净、资产已保存。

[EP] === 阶段 5：edit ===
[EP] 使用 scene_plan + asset_manifest 启动 edit-director...
[EP] 时间线：3 分 02 秒，7 个剪辑。字幕已启用。
[EP] 修剪：移除了 0:00-0:12（空音）和 3:45-4:22（离题内容）。
[EP] G5 通过 — 时间线完整，所有引用有效。

[EP] === 阶段 6：compose ===
[EP] 使用 edit_decisions + asset_manifest 启动 compose-director...
[EP] face_enhance 已应用：处理了 8 个场景。
[EP] color_grade 已应用：统一暖色调。
[EP] audio_enhance：已应用降噪。
[EP] video_compose：最终渲染 → output/talking-head-final.mp4
[EP] 输出探针：3 分 01 秒，1920x1080，立体声音频，H.264。✓
[EP] 预算：已花费 $0.18（face_enhance + color_grade + overlays）。
[EP] G6 通过

[EP] === 阶段 7：publish ===
[EP] 使用 render_report 启动 publish-director...
[EP] G7 通过 — 标题、描述、章节、缩略图已配置。

[EP] === 最终 QA ===
[EP] 时长：3 分 01 秒 ✓ | 字幕同步：最大偏差 0.18 秒 ✓ | 音频：-16.2 LUFS ✓
[EP] 面部增强：自然 ✓ | 色彩：一致 ✓ | 叠加层：时序正确 ✓
[EP] 预算：$0.18 / $0.50 ✓
[EP] 流水线完成 — 0 次修订，0 次回退
[EP] 输出：output/talking-head-final.mp4
```

## 常见陷阱

- **忽视转录质量**：下游所有环节都依赖转录。如果置信度低，在脚本阶段修复它——不要让错误的时间戳传播到字幕和剪辑。
- **过度增强**：面部增强和色彩分级是可选的。如果原始素材看起来不错，跳过它们。不要为了处理而添加处理。
- **字幕风格不匹配**：字幕风格必须来自剧本。不要让 asset director 在剧本指定了字体/颜色/位置时使用默认的 SRT 样式。
- **不探针分析原始素材**：开始前始终使用 ffprobe。没有音轨或容器损坏的视频会浪费下游每个阶段。
- **修剪过于激进**：edirector 可能会剪辑看似离题但包含有价值上下文的段落。EP 应通过对照简报来验证被修剪的内容是否确实不必要。
- **丢失转录数据**：EP 必须将 `transcript_segments` 从脚本阶段一直携带到资产生成。字幕时序依赖于转录器生成的相同字级数据。
