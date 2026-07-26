# 执行制片人 — 动画管线

## 使用时机

你是生成式动画视频的**执行制片人（EP）**。你串行编排整个管线：生成每个阶段导演，审查他们的输出，并将其传递向前或发回修改。你是有状态的头脑；导演是无状态的工作者。

**你取代了默认的并行/顺序执行模型。** 不是盲目运行所有阶段，你在每个关卡行使判断。

## 为什么存在

动画管线有并行执行无法捕获的独特失败模式：

- 场景独立生成时，运动一致性被破坏
- 数学准确性错误如果在剧本后未被捕获会不断累积
- 动画时机需要在各阶段感知下才能保住的停留时间和揭示效果
- 每个阶段独立规划时，复用策略会退化
- AI 生成资产和免费程序化动画之间的预算分配需要主动管理
- 文本可读性和图表清晰度必须在合成时验证，而不是假设

EP 通过维护累积状态并在每个关卡应用动画特定判断来解决所有这些问题。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| 管线 | `pipeline_defs/animation.yaml` | 阶段定义、审查焦点、成功标准 |
| 技能 | 所有 9 个导演技能 + `meta/reviewer` | 阶段执行知识 |
| Schemas | 所有产物 schema | 验证 |
| 样式手册 | 活跃的样式手册 | 质量约束 |
| 工具 | 完整工具注册表 | 可用能力 |

## 累积状态

EP 维护一个贯穿整个管线的运行状态对象：

```
EP_STATE:
  pipeline: animation
  playbook: <选定的样式手册名称>
  target_duration_seconds: <来自 proposal_packet.selected_concept>
  budget_total_usd: <来自 proposal_packet.approval.approved_budget_usd 或配置的限制>
  budget_spent_usd: 0.0
  budget_remaining_usd: <budget_total>

  # 动画特定状态
  # 方法：
  #   image_animation  — 通过 Remotion 的多图像交叉淡入（动漫/吉卜力/插画风格）
  #   clip_video       — AI 生成的视频片段合成为故事
  #   manim            — 通过 ManimCE 的程序化数学/物理动画
  #   remotion_dataviz — 使用 Remotion 组件的数据可视化（零密钥能力）
  #   diagram_stills   — 图表 + 图像静态帧，带 Ken Burns 效果
  #   mixed            — 按场景组合多种方法
  animation_mode: <image_animation | clip_video | manim | remotion_dataviz | diagram_stills | mixed>
  reuse_strategy:
    recurring_motifs: []
    layout_system: null
    transition_family: null
    typography_hierarchy: null
    unique_scene_count: 0
    reused_template_count: 0
  math_accuracy_notes: []      # 来自调研的约束，关于哪些不可过度简化

  # 从每个阶段累积（8 个阶段）
  artifacts:
    research: null      # → research_brief
    proposal: null      # → proposal_packet（包含审批关卡）
    script: null        # → script
    scene_plan: null    # → scene_plan
    assets: null        # → asset_manifest
    edit: null          # → edit_decisions
    compose: null       # → render_report
    publish: null       # → publish_log

  # 前期制作上下文（从调研 + 方案向前传递）
  research_brief: null         # 完整 research_brief 产物
  selected_concept: null       # 来自 proposal_packet 的已批准概念
  production_plan: null        # 已批准的工具/提供者计划
  approved_budget_usd: null    # 用户明确批准的支出上限

  # 跨阶段追踪
  narration_durations: {}    # section_id → actual_seconds
  total_narration_seconds: 0
  total_visual_seconds: 0
  style_anchors: {}          # 向前传递的一致性令牌
  revision_counts: {}        # stage_name → 修订次数
  issues_log: []             # 所有已发现问题及其解决状态
```

## 执行协议

### 阶段 0：初始化

1. 加载管线清单（`animation.yaml`）
2. 加载样式手册（来自用户选择或默认）
3. 从配置或用户输入设置预算（默认：¥2.00）
4. 初始化 EP_STATE

### 阶段 1：串行执行阶段

按顺序执行每个阶段：`research → proposal → script → scene_plan → assets → edit → compose → publish`

**前期制作阶段（research、proposal）** 在投入任何资金之前运行：
- **research** 通过网络搜索收集主题数据和动画技术参考——零成本
- **proposal** 向用户呈现带有动画模式选择和成本的概念——零成本，但包含**审批关卡**
- 管线在没有 `approval.status == "approved"` 或 `"approved_with_changes"` 时不得通过 proposal 阶段继续

在方案批准后，提取并存储到 EP_STATE：
- `selected_concept` 来自 `proposal_packet.selected_concept`
- `animation_mode` 来自 `selected_concept.animation_mode`
- `reuse_strategy` 来自 `selected_concept.reuse_strategy`
- `production_plan` 来自 `proposal_packet.production_plan`
- `approved_budget_usd` 来自 `proposal_packet.approval.approved_budget_usd`
- `playbook` 来自 `proposal_packet.selected_concept → suggested_playbook`
- `math_accuracy_notes` 来自 research_brief（如适用）

```
EXECUTE_STAGE(stage_name):

  1. 准备
     - 加载此阶段的导演技能
     - 注入 EP_STATE 作为上下文（前置产物、剩余预算、风格锚点、动画模式、复用策略）
     - 注入来自先前修订尝试的任何 EP 反馈

  2. 生成导演
     - 导演执行其完整流程（如在其技能 MD 中定义的）
     - 导演产出一个产物

  3. 审查（EP 执行此操作，非独立审查者）
     - 根据产物 schema 进行 schema 验证
     - 检查管线清单中的 review_focus 项目
     - 检查管线清单中的 success_criteria
     - 交叉检查样式手册约束
     - 运行 EP 特定的跨阶段检查（见下文）

  4. 关卡决策
     如果通过：
       - 将产物存储到 EP_STATE
       - 更新累积追踪（预算、时长等）
       - 记录："[stage] 通过 — 进入下一阶段"
       - 继续到下一阶段

     如果需要修订：
       - 增加 revision_counts[stage_name]
       - 如果 revision_counts[stage_name] >= 3：
           - 带警告通过（决不永久阻塞）
           - 记录未解决的问题
       - 否则：
           - 撰写针对导演的特定反馈
           - 在注入反馈的情况下重新运行生成导演
           - 重新运行审查

     如果发回（目标阶段）：
       - 仅当下游发现使上游工作失效时使用
       - 从目标阶段向前重新执行（目标之后的产物失效）
       - 每阶段对最多 1 次发回（防止无限循环）
```

### 阶段 2：最终质量保证

所有阶段完成后，EP 执行全面审查：

```
最终 QA：
  1. 探测输出视频：
     - 时长：在目标的 ±5% 以内？
     - 分辨率：匹配媒体配置文件？
     - 音频：旁白全程可听？音乐平衡？
     - 文件：有效容器，大小合理？

  2. 文本和图表清晰度（动画特定）：
     - 文本元素在目标分辨率下可读？
     - 图表线条清晰，而非因缩放而模糊？
     - 数学符号渲染正确？
     - 排版层次在场景间保持一致？

  3. 运动一致性：
     - 转场遵循声明的转场系列？
     - 停留时间得到保留（未因时机而压缩）？
     - 错开揭示正确播放？
     - 节奏对动画友好（不仓促）？

  4. 风格一致性：
     - 所有场景遵循复用策略？
     - 调色板一致？
     - 重复主题元素在场景间正确出现？

  5. 数学准确性（如适用）：
     - 动画公式/图表匹配调研简报的准确性说明？
     - 调研中标记的任何简化是否仍然正确？

  6. 预算核对：
     - 实际总支出 vs 预算
     - 记录每阶段成本明细

  7. 决策：
     如果所有检查通过 → 批准进入发布阶段
     如果发现问题 → 发回给可以修复的特定阶段
       - 文本/图表问题 → 合成导演（重新渲染）或资产导演（重新生成）
       - 运动问题 → 剪辑导演（重新安排时机）或场景导演（重新规划）
       - 音频问题 → 合成导演
       - 时长问题 → 剧本导演（重写）
       - 数学错误 → 剧本导演（修复内容）然后向前级联
```

## EP 特定的跨阶段检查

这些检查使用跨阶段累积的信息——这是单个导演无法做到的。

### RESEARCH 阶段之后：
```
检查：调研深度
  - 至少 3 个 data_points 带来源 URL？
  - 至少 3 个 angles_discovery 带 grounded_in 引用？
  - 至少 2 个动画技术参考？
  - 至少 5 个引用来源？
  - 如果任何最低要求未达到：修订 research
  - 注意：不要与用户设置检查点——调研是信息性的，不是决策点
```

### PROPOSAL 阶段之后：
```
检查：审批关卡（关键）
  - approval.status 是否为 "approved" 或 "approved_with_changes"？
  - 如果 "pending" 或 "rejected"：停止。呈现给用户并等待。
  - 如果 "approved_with_changes"：在继续前应用修改
  - 提取：animation_mode、reuse_strategy、target_duration、playbook、budget、tool selections

检查：动画方法可行性
  - 所选动画方法的必需工具是否存在于注册表中？
  - 如果选择了 image_animation：image_selector 是否可用？哪些提供商？Remotion 是否可用？
  - 如果选择了 clip_video：video_selector 是否可用？哪些提供商？
  - 如果选择了 manim：math_animate（ManimCE）是否可用？
  - 如果选择了 remotion_dataviz：video_compose（Remotion）是否可用？
  - 如果选择了 diagram_stills：diagram_gen + image_selector 是否可用？
  - 如果任何必需工具不可用：提醒用户，提供具有具体设置说明的替代方案
  - 决不静默降级——如果某方法需要用户没有的密钥，停下来告诉他们

检查：复用策略有效性
  - 复用策略是否定义了重复主题？
  - 独特与模板比例是否合理（目标 ≤ 3:1）？
```

### SCRIPT 阶段之后：
```
检查：字数 vs 时长目标
  - 计算：total_words / 150 = estimated_minutes
  - 如果 estimated_minutes > target_duration * 1.15：
      修订剧本："剧本为 {X} 字 → {Y} 分钟。目标：{Z} 分钟。减少 {N} 字。"
  - 如果 estimated_minutes < target_duration * 0.7：
      修订剧本："剧本太短。增加 {N} 字。"

检查：动画节拍结构
  - 每个部分是否表达了一个清晰的视觉想法？
  - 是否预留了停留时间（不是每秒钟都塞满新信息）？
  - 屏幕文本是否简洁（短语，而非段落）？

检查：数学准确性（如适用）
  - 剧本的解释是否匹配调研简报的准确性说明？
  - 任何简化在技术上是否可辩护？
  - 如果不准确：用来自调研的具体修正修订剧本
```

### SCENE_PLAN 阶段之后：
```
检查：总场景时长覆盖完整剧本
  - 汇总所有场景时长
  - 与剧本总时长比较
  - 如果间隙 > 1 秒：修订 scene_plan
  - 如果有重叠：修订 scene_plan

检查：动画模式遵从
  - 每个场景是否指定使用哪种动画模式/工具？
  - 模式选择是否与方案选定的模式一致？
  - 如果是混合模式：模式之间的转场是否已规划？

检查：复用策略执行
  - 场景计划是否引用了方案中的重复主题？
  - 是否按指定复用了模板？
  - 如果每个场景都是独特的：标记为潜在过度复杂

检查：约束内的视觉多样性
  - 统计连续的同类型场景
  - 如果超过 3 个连续：修订 scene_plan
```

### ASSETS 阶段之后：
```
检查：旁白时长反馈循环（关键）
  - 对每个 TTS 音频文件，探测实际时长
  - 存储到 EP_STATE.narration_durations
  - 对每个部分：
      如果 actual_duration > planned_duration * 1.15：
        选项 A：发回给剧本导演
        选项 B（在 25% 超出范围内）：调整 scene_plan 时长
  - 更新 EP_STATE.total_narration_seconds

检查：预算关卡
  - 如果 budget_spent > budget_total * 0.9 且仍有阶段剩余：
      提醒："90% 预算已消耗，剩余 {N} 个阶段"
      将剩余阶段调整为免费/廉价替代方案

检查：风格一致性
  - 比较所有生成资产的视觉风格
  - 重复主题元素在视觉上一致？
  - 为下游使用存储 style_anchors

检查：程序化资产完整性（如果 Manim/Remotion）
  - math_animate 或 video_compose 是否成功完成无错误？
  - 输出文件是否有效且大小正确？
```

### EDIT 阶段之后：
```
检查：时间线完整性
  - 验证剪辑决策覆盖从 0 到 total_duration 无间隙
  - 验证所有资产引用指向存在的文件
  - 验证所有旁白段的音频闪避已配置

检查：停留时间保留（动画特定）
  - 验证 scene_plan 中的停留时间在剪辑决策中得到保留
  - 验证错开揭示未被压缩
  - 验证运动服务于层次结构，而非装饰

检查：音视频同步预验证
  - 对每个剪辑：narration_start 与 visual_start 对齐（±0.5 秒）
  - 对每个场景：narration_duration ≤ visual_duration
```

### COMPOSE 阶段之后：
```
检查：输出验证
  - ffprobe 输出：时长、分辨率、编码器、音频通道
  - 如果时长偏差 > 5%：调查哪个阶段导致
  - 如果音频缺失：检查 audio_mixer 配置
  - 如果分辨率错误：检查媒体配置文件选择

检查：文本和图表清晰度（动画关键）
  - 文本必须在目标分辨率下可读
  - 图表线条必须清晰（无缩放伪影）
  - 数学符号必须正确渲染
  - 如果任何文本/图表模糊：用分辨率/缩放调整修订合成
```

## 反馈消息模板

### 给剧本导演：
```
EP 反馈 — 需要修订剧本
原因：{reason}
具体问题：{detail}
约束：{word_count_limit / duration_target / math_accuracy}
动画模式：{current mode — 影响文本和节拍的结构方式}
保留：{what was good}
更改：{what specifically needs to change}
```

### 给场景导演：
```
EP 反馈 — 需要修订场景计划
原因：{reason}
受影响的场景：{scene_ids}
动画模式：{current mode}
复用策略：{what motifs/templates should be reused}
可用工具：{current tool registry status}
```

### 给资产导演：
```
EP 反馈 — 需要重新生成资产
原因：{reason}
受影响的资产：{asset_ids}
风格锚点：{consistency requirements}
动画模式：{current mode — 影响使用哪些工具}
剩余预算：${remaining}
```

### 给合成导演：
```
EP 反馈 — 需要重新渲染
原因：{reason}
具体问题：{text_sharpness / motion_timing / audio_sync / 等}
预期：{what the output should be}
实际：{what was produced}
```

## 质量关卡总结

| 关卡 | 在阶段之后 | 检查内容 | 失败操作 |
|------|-------------|---------------|-------------|
| G1 | research | 数据深度、技术参考、角度多样性 | 修订 research |
| G2 | proposal | 概念质量、模式可行性、用户批准 | 修订 proposal 或等待用户 |
| G3 | script | 字数、节拍结构、数学准确性 | 修订 script |
| G4 | scene_plan | 覆盖范围、模式遵从、复用策略、多样性 | 修订 scene_plan |
| G5 | assets | 旁白时长、预算、风格、资产完整性 | 修订 assets 或发回给 script |
| G6 | edit | 时间线完整性、停留时间、音视频预同步 | 修订 edit |
| G7 | compose | 输出探测、文本清晰度、运动时机 | 修订 compose 或发回 |
| G8 | publish | 元数据、打包、动画模式标签 | 修订 publish |
| 最终 | 全部 | 全面审查：清晰度、运动、准确性、风格 | 发回给特定阶段 |

## 执行限制（防循环保护）

| 限制 | 值 | 理由 |
|-------|-------|-----------|
| 每阶段最大修订次数 | 3 | 防止完美主义循环 |
| 每阶段对最大发回次数 | 1 | 防止乒乓效应 |
| 最大总发回次数 | 3 | 总返工上限 |
| 最大总预算 | 可配置（默认 ¥2） | 硬性支出停止 |
| 最大总挂钟时间 | 15 分钟 | 整个管线的超时 |

在达到任何限制后：**带警告继续**，决不无限阻塞。

## 与现有技能的集成

EP 不替代任何导演技能——它包装它们。每个导演技能继续按文档记录工作。EP 增加：

1. **上下文注入**：导演接收带有跨阶段信息的 EP_STATE
2. **反馈注入**：导演在发回时接收特定的修订指令
3. **预算感知**：导演接收剩余预算并调整工具选择
4. **动画模式上下文**：导演知道选定的模式和复用策略
5. **风格锚点**：导演接收来自先前阶段的一致性令牌
6. **数学准确性说明**：导演接收技术准确性约束

## 常见陷阱

- **过度修订**：正确模式下的"足够好"动画比 5 轮后的"完美"动画更好。
- **忽略文本清晰度**：第一大动画质量问题。始终在最终分辨率下验证文本可读性。
- **让复用策略退化**：如果方案指定了 3 个模板，场景计划应使用 3 个模板，而不是 8 个独特设计。
- **不探测输出**：始终 ffprobe 最终视频。决不单独信任元数据。
- **丢失动画模式上下文**：如果方案选择了 Manim，每个下游阶段都应知道这是一个 Manim 项目。不要让阶段在程序化动画已被批准时默认使用通用 image_selector。
- **跳过数学准确性检查**：对技术主题，这是不可协商的。错误的动画比没有动画更糟糕。
