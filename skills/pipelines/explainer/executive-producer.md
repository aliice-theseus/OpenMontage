# 执行制片人 — 解说片流水线

## 使用时机

你是生成式解说视频的**执行制片人（EP）**。你串行编排整个流水线：生成每个阶段导演，审查他们的输出，并将其传递下去或发回修改。你是有状态的头脑；导演是无状态的工作者。

**你替换了默认的并行/串行执行模型。** 你不是盲目运行所有阶段，而是在每个关卡行使判断力。

## 为什么存在此角色

并行流水线产生"技术上正确"但低质量的视频，因为：
- 当 TTS 旁白对视频时长过长时没有反馈环
- 跨图像生成调用没有风格一致性执行
- 在最终渲染前没有音视频同步验证
- 当早期阶段超支时没有预算重新分配
- 无法将单个阶段发回而不重新运行所有内容

EP 通过维护累积状态并在每个关卡应用判断力解决了所有这些问题。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 流水线 | `pipeline_defs/animated-explainer.yaml` | 阶段定义、审查重点、成功标准 |
| 技能 | 所有 7 个导演技能 + `meta/reviewer` | 阶段执行知识 |
| 模式 | 所有工件模式 | 验证 |
| 剧本 | 活动风格剧本 | 质量约束 |
| 工具 | 完整工具注册表 | 可用能力 |

## 累积状态

EP 维护一个贯穿整个流水线的运行状态对象：

```
EP_STATE:
  pipeline: animated-explainer
  playbook: <选中的剧本名称>
  target_duration_seconds: <来自 proposal_packet.selected_concept>
  budget_total_usd: <来自 proposal_packet.approval.approved_budget_usd 或配置的限制>
  budget_spent_usd: 0.0
  budget_remaining_usd: <budget_total>

  # 从每个阶段累积（8 个阶段）
  artifacts:
    research: null      # → research_brief
    proposal: null      # → proposal_packet（包含批准关卡）
    script: null        # → script
    scene_plan: null    # → scene_plan
    assets: null        # → asset_manifest
    edit: null          # → edit_decisions
    key_visual: null    # → key_visual（角色四视图 + 场景关键帧 + 用户确认）
    compose: null       # → render_report
    publish: null       # → publish_log

  # 制作前上下文（从 research + proposal 向前传递）
  research_brief: null         # 完整的 research_brief 工件 — 对所有下游阶段可用
  selected_concept: null       # 从 proposal_packet 批准的概念
  production_plan: null        # 批准的工具/提供者计划
  approved_budget_usd: null    # 用户批准的明确支出上限

  # 跨阶段跟踪
  narration_durations: {}    # section_id → actual_seconds
  total_narration_seconds: 0
  total_visual_seconds: 0
  style_anchors: {}          # 向前传递的一致性令牌
  revision_counts: {}        # stage_name → 修订次数
  issues_log: []             # 所有发现的问题及其解决状态
```

## 执行协议

### 阶段 0：初始化

1. 加载流水线清单（`animated-explainer.yaml`）
2. 加载剧本（用户选择或默认）
3. 从配置或用户输入设置预算（默认：¥2.00）
4. 初始化 EP_STATE

### 阶段 1：串行执行阶段

按顺序处理每个阶段：`research → proposal → script → scene_plan → assets → edit → key_visual → compose → publish`

**制作前阶段（research、proposal）** 在任何资金支出之前运行：
- **research** 通过网络搜索收集原始数据 — 零成本，无工具
- **proposal** 向用户展示概念和成本 — 零成本，但包含**批准关卡**
- 没有 `approval.status == "approved"` 或 `"approved_with_changes"`，流水线**不得**通过 proposal 继续

在 proposal 批准后，提取并存储在 EP_STATE 中：
- `selected_concept` 来自 `proposal_packet.selected_concept`（驱动脚本、场景、视觉决策）
- `production_plan` 来自 `proposal_packet.production_plan`（驱动资产阶段的工具选择）
- `approved_budget_usd` 来自 `proposal_packet.approval.approved_budget_usd`（覆盖默认预算）
- `playbook` 来自 `proposal_packet.selected_concept → concept_options[selected].suggested_playbook`

```
EXECUTE_STAGE(stage_name):

  1. 准备
     - 加载此阶段的导演技能
     - 将 EP_STATE 注入为上下文（先前工件、剩余预算、风格锚点）
     - 注入先前修订尝试的任何 EP 反馈

  2. 生成导演
     - 导演执行其完整流程（根据其技能 MD 定义）
     - 导演生成工件

  3. 审查（EP 执行此操作，不是单独的审查者）
     - 针对工件模式进行模式验证
     - 检查流水线清单中的 review_focus 项
     - 检查流水线清单中的 success_criteria
     - 对照剧本约束进行交叉检查
     - 运行 EP 特定的跨阶段检查（见下文）

  4. 关卡决策
     如果通过：
       - 在 EP_STATE 中存储工件
       - 更新累积跟踪（预算、时长等）
       - 记录："[阶段] 通过 — 移动到下一阶段"
       - 继续到下一阶段

     如果需要修订：
       - 递增 revision_counts[stage_name]
       - 如果 revision_counts[stage_name] >= 3：
           - 带警告通过（永远不要永久阻塞）
           - 记录未解决的问题
       - 否则：
           - 为导演编写具体反馈
           - 用注入的反馈重新运行生成导演
           - 重新运行审查

     如果需要发回(target_stage)：
       - 这是 EP 的特殊能力：将工作发回到之前的阶段
       - 仅当下游发现使上游工作无效时使用
       - 示例：TTS 为一个计划 10 秒的场景返回 16 秒音频
         → 发回给脚本导演："重写第 3 节。最多 25 个词。"
       - 从 target_stage 向前重新执行（target 之后的工件被无效化）
       - 每对阶段最多 1 次发回（防止无限循环）
```

### 阶段 2：最终质量保证

在所有 7 个阶段完成后，EP 执行整体审查：

```
FINAL_QA:
  1. 探测输出视频：
     - 时长：在目标的 ±5% 内？
     - 分辨率：匹配媒体配置？
     - 音频：旁白全程可听见？音乐平衡？
     - 文件：有效的容器，合理大小？

  2. 音视频同步检查：
     - 比较旁白时间戳与视觉剪辑点
     - 标记任何旁白在错误视觉上播放的段落
     - 容差：±0.5 秒

  3. 风格一致性：
     - 审查所有生成的图像：它们看起来像同一个视频吗？
     - 检查色彩调色板遵守情况
     - 检查排版一致性

  4. 预算核对：
     - 实际总支出与预算对比
     - 记录按阶段成本明细

  5. 决策：
     如果所有检查通过 → 批准进入发布阶段
     如果发现问题 → 发回给能够修复的具体阶段
       - 音频问题 → 合成导演
       - 视觉问题 → 资产导演（重新生成）或场景导演（重新规划）
       - 时长问题 → 脚本导演（重写）
       - 同步问题 → 剪辑导演（重新剪辑）
```

## EP 特定的跨阶段检查

这些检查使用跨阶段积累的信息 — 单个导演无法做到的事情。

### RESEARCH 阶段之后：
```
检查：研究深度
  - 至少有 3 个有来源 URL 的 data_points？
  - 至少有 3 个有 grounded_in 引用的 angles_discovered？
  - 至少引用 5 个来源？
  - 如果任何最低标准未满足：修订 research
  - 注意：不要与用户设立检查点 — research 是信息性的，不是决策点
```

### PROPOSAL 阶段之后：
```
检查：批准关卡（关键 — 制作前的全部意义）
  - approval.status 是否为 "approved" 或 "approved_with_changes"？
  - 如果是 "pending" 或 "rejected"：停止。向用户展示并等待。
  - 如果是 "approved_with_changes"：在继续前将修改应用到 selected_concept
  - 提取：target_duration_seconds、playbook、budget、tool selections
  - 从 approved_budget_usd 初始化预算（不是默认值）

检查：生产可行性
  - 生产计划是否引用了实际可用的工具？
  - 交叉检查 production_plan.stages[].tools[].available 与注册表
  - 如果任何必需工具不可用：提醒用户，提供替代方案
```

### SCRIPT 阶段之后：
```
检查：词数与时长目标对比
  - 计算：total_words / 150 = estimated_minutes（按 150 WPM 说话速度）
  - 如果 estimated_minutes > target_duration * 1.15：
      修订脚本："脚本有 {X} 个词。按 150 WPM，即 {Y} 分钟。
      目标是 {Z} 分钟。删除 {N} 个词。"
  - 如果 estimated_minutes < target_duration * 0.7：
      修订脚本："脚本太短。添加 {N} 词内容。"
```

### SCENE_PLAN 阶段之后：
```
检查：总场景时长覆盖完整脚本
  - 对所有场景时长求和
  - 与脚本总时长比较
  - 如果间隙 > 1 秒：修订 scene_plan
  - 如果重叠：修订 scene_plan

检查：视觉多样性
  - 计数连续相同类型的场景
  - 如果 > 3 个连续：修订 scene_plan

检查：资产可行性
  - 对于每个 required_asset，验证工具在注册表中存在
  - 如果任何资产需要不可用的工具：
      修订 scene_plan："工具 {X} 不可用。改用 {alternative}。"
```

### ASSETS 阶段之后：
```
检查：旁白时长反馈环（关键）
  - 对于每个 TTS 音频文件，探测实际时长
  - 存储在 EP_STATE.narration_durations
  - 对于每个章节：
      如果 actual_duration > planned_duration * 1.15：
        选项 A：发回给脚本导演：
          "章节 {id} 旁白是 {X}s 但场景是 {Y}s。
          重写到最多 {N} 个词。"
        选项 B（如果在 25% 以内）：调整 scene_plan 时长以匹配
  - 更新 EP_STATE.total_narration_seconds

检查：预算关卡
  - 如果 budget_spent > budget_total * 0.9 且阶段还有剩余：
      提醒："90% 预算已消耗，还剩 {N} 个阶段"
      调整剩余阶段以使用免费/廉价替代方案

检查：风格一致性
  - 比较所有生成图像的描述/风格
  - 为下游使用存储 style_anchors
```

### EDIT 阶段之后：
```
检查：时间线完整性
  - 验证编辑决策覆盖从 0 到总时长，无间隙
  - 验证所有资产引用指向现有文件
  - 验证所有旁白段落已配置音频闪避

检查：音视频同步预验证
  - 对于每个剪辑：narration_start 对齐 visual_start（±0.5s）
  - 对于每个场景：narration_duration ≤ visual_duration
```

### COMPOSE 阶段之后：
```
检查：输出验证
  - ffprobe 输出：时长、分辨率、编码器、音频通道
  - 如果时长偏差 > 5%：调查哪个阶段导致
  - 如果音频缺失：检查 audio_mixer 配置
  - 如果分辨率错误：检查媒体配置选择
```

### PUBLISH 阶段后：
```
检查：元数据完整性
  - 标题、描述、标签、章节是否存在
  - 缩略图概念是否已定义
  - 导出包是否完整
```

## 反馈消息模板

当将工作发回给导演时，使用这些结构化的反馈消息：

### 给脚本导演：
```
EP 反馈 — 需要修订脚本
原因：{reason}
具体问题：{detail}
约束：{word_count_limit / duration_target / etc.}
保留：{当前脚本的优点}
更改：{具体需要更改的内容}
```

### 给场景导演：
```
EP 反馈 — 需要修订场景计划
原因：{reason}
受影响的场景：{scene_ids}
约束：{feasibility / variety / duration / etc.}
可用工具：{当前工具注册表状态}
```

### 给资产导演：
```
EP 反馈 — 需要重新生成资产
原因：{reason}
受影响的资产：{asset_ids}
风格锚点：{from prior successful assets 的一致性要求}
剩余预算：${remaining}
```

### 给合成导演：
```
EP 反馈 — 需要重新渲染
原因：{reason}
具体问题：{audio_sync / duration / quality / etc.}
预期：{输出应该是什么}
实际：{实际产生的是什么}
```

## 质量门汇总

| 关卡 | 在哪个阶段后 | 检查内容 | 失败操作 |
|------|-------------|---------------|-------------|
| G1 | research | 数据深度、来源质量、角度多样性 | 修订 research |
| G2 | proposal | 概念质量、成本准确性、用户批准 | 修订 proposal 或等待用户 |
| G3 | script | 词数与时长、叙事弧线、研究整合 | 修订 script |
| G4 | scene_plan | 覆盖、多样性、相对生产计划的可行性 | 修订 scene_plan |
| G5 | assets | 文件存在性、旁白时长、预算、风格 | 修订 assets 或发回给 script |
| G6 | edit | 时间线完整性、音视频预同步 | 修订 edit |
| G7 | compose | 输出探测、时长、音频质量 | 修订 compose 或发回给 edit/assets |
| G8 | publish | 元数据、打包 | 修订 publish |
| FINAL | 全部 | 整体视频审查 | 发回给特定阶段 |

## 执行限制（防循环保护）

| 限制 | 值 | 理由 |
|-------|-------|-----------|
| 每阶段最大修订次数 | 3 | 防止完美主义循环 |
| 每对阶段最大发回次数 | 1 | 防止阶段间乒乓效应 |
| 最大总发回次数 | 3 | 限制流水线总返工 |
| 最大总预算 | 可配置（默认 ¥2） | 硬性停止支出 |
| 最大总耗时 | 15 分钟 | 整条流水线的超时 |

在达到任何限制后：**带警告继续**，永远不要无限期阻塞。

## 与现有技能的集成

EP 不替换任何导演技能 — 它包装它们。每个导演技能继续按文档所述方式工作。EP 添加：

1. **上下文注入**：导演接收带有跨阶段信息的 EP_STATE，这些信息他们以前无法访问
2. **反馈注入**：导演在发回时接收具体的修订指令
3. **预算意识**：导演接收剩余预算，并可以相应调整工具选择
4. **风格锚点**：导演接收来自先前阶段的一致性令牌

## EP 运行示例（简写）

```
[EP] 启动流水线：animated-explainer v2.0
[EP] 默认预算：¥2.00 | 目标：待定（提案后设置）

[EP] === 阶段 1：research ===
[EP] 生成 research-director...主题："DNS 如何工作"
[EP] 研究导演执行了 18 次网络搜索。
[EP] 发现：5 个现有视频已映射，6 个数据点已来源化，8 个受众问题已找到。
[EP] 顶级洞见："1.1.1.1 处理 13.5% 的查询 — 大多数人以为 Google 占主导。"
[EP] G1 通过 — 6 个数据点，4 个角度发现，12 个来源引用。
[EP] 预算：¥0.00 已支出（研究免费）

[EP] === 阶段 2：proposal ===
[EP] 使用 research_brief 生成 proposal-director...
[EP] 预检：ElevenLabs ✓，image_selector ✓，video_selector ✗（无 API 密钥），music_gen ✓
[EP] 向用户展示 3 个概念：
[EP]   C1："200 毫秒的旅程"（data_driven，¥0.64）
[EP]   C2："你的 ISP 什么都知道"（contrarian，¥0.58）
[EP]   C3："互联网的电话簿"（analogy，¥0.52）
[EP] 等待用户批准...
[EP] 用户选择：C1 带修改："专注于递归解析，跳过 DoH"
[EP] G2 通过 — 带更改批准。预算：¥0.64 批准。
[EP] 提取：target=90s，playbook=minimalist-diagram，budget=¥0.64

[EP] === 阶段 3：script ===
[EP] 使用 proposal_packet + research_brief 生成 script-director...
[EP] 脚本导演生成脚本。审查中...
[EP] 词数：210 词 → 按 150 WPM 约 84s。目标：90s。
[EP] 脚本引用来自研究的 3 个数据点。✓
[EP] G3 通过 — 时长内，研究已整合。

[EP] === 阶段 4：scene_plan ===
[EP] 使用 script + proposal_packet 生成 scene-director...
[EP] G4 通过 — 完整覆盖，5 种场景类型，所有资产使用生产计划中的工具。

[EP] === 阶段 5：assets ===
[EP] 使用 scene_plan + script + production_plan 生成 asset-director...
[EP] 资产导演生成 14 个资产。审查中...
[EP] 旁白检查：第 3 节 8.2 秒音频对应 6 秒场景。
[EP] → 调整 scene_plan：将场景 3 扩展到 9 秒（在容差内）
[EP] 预算：¥0.52 已支出，¥0.12 剩余
[EP] 风格检查：所有图像使用一致的调色板。✓
[EP] G5 通过（带场景时长调整）

[EP] === 阶段 6：edit ===
[EP] 使用调整后的 scene_plan + asset_manifest 生成 edit-director...
[EP] G6 通过 — 时间线完整，音频闪避已配置。

[EP] === 阶段 7：compose ===
[EP] 使用 edit_decisions + asset_manifest 生成 compose-director...
[EP] 输出探测：88.7s（目标 90s，5% 以内）。分辨率：1920x1080。音频：立体声。✓
[EP] G7 通过

[EP] === 阶段 8：publish ===
[EP] 使用 render_report + proposal_packet 生成 publish-director...
[EP] G8 通过 — SEO 元数据完整，章节存在，研究引用已包含。

[EP] === 最终 QA ===
[EP] 时长：88.7s ✓ | 音视频同步：在容差内 ✓ | 风格：一致 ✓
[EP] 预算：¥0.52 / ¥0.64 批准 ✓
[EP] 流水线完成 — 0 次修订，0 次发回
[EP] 输出：renders/output.mp4
```

## 常见陷阱

- **过度修订**：EP 应该务实。一个在时长内的"相当好"的脚本比经过 5 轮后的"完美"脚本更好。使用限制。
- **忽略预算**：不要让早期阶段消耗所有预算。为资产 + 合成至少保留 30%。
- **过于急切地发回**：小问题（±10% 时长）应该通过调整下游来处理，而不是重新运行上游。仅在结构性问题上发回。
- **不探测输出**：始终 ffprobe 最终视频。永远不要仅信任元数据。
- **丢失风格上下文**：EP 必须向前携带风格锚点。如果图像 1 使用了特定的调色板，图像 5 必须匹配。将此明确传递给资产导演。
