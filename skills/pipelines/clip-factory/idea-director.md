# 创意导演 - Clip Factory 流水线

## 使用时机

当视频源为长视频素材且目标是产出多个短视频交付物时使用此流水线：网络研讨会剪辑、访谈片段、直播高光、主题演讲摘录或演示文稿片段。

你不是在规划一个视频，而是在规划一个经过排序的剪辑组合集。

## 运行时选择（强制 — 展示约束条件，不要静默选择）

锁定 `render_runtime = "remotion"`（用于带逐词字幕的合成剪辑）或 `"ffmpeg"`（用于纯拼接/裁剪，无合成）。**HyperFrames 在此流水线的第一阶段不是有效的运行时** — clip-factory 依赖 Remotion 的逐词字幕烧录，HyperFrames 尚无对等功能。

根据 AGENT_GUIDE.md → "展示两种合成运行时（硬性规则）"：不要静默锁定 remotion。向用户说明约束条件："你的机器上可以使用 HyperFrames 运行时，但 clip-factory 依赖 Remotion 的字幕烧录功能，HyperFrames 尚未提供对等支持，因此 remotion 是这里唯一可行的选择 — 可以继续吗？"在 `decision_log` 中用类别 `render_runtime_selection` 记录决策，将 hyperframes 列为被拒绝的选项（`rejected_because: "caption-burn parity deferred on clip-factory"`）。

## 参考输入

- `docs/clip-factory-best-practices.md`
- `skills/creative/short-form.md`
- `skills/creative/video-editing.md`

## 流程

### 1. 理解视频源和目标

明确视频源的形态：

- 网络研讨会（webinar）
- 访谈（interview）
- 圆桌讨论（panel）
- 主题演讲（keynote）
- 直播（stream）
- 客户故事（customer story）

然后明确业务目标：

- 品牌知名度（awareness）
- 思想领导力（thought leadership）
- 线索生成（lead generation）
- 产品教育（product education）
- 活动回顾（event recap）

### 2. 选择剪辑组合策略

一个好的批次应混合不同类型的剪辑，而不是重复提取相同能量的内容。

常见的剪辑家族：

- `hook`（钩子）：令人惊讶的主张或强劲的冷开场
- `insight`（洞察）：有用的收获或经验教训
- `story`（故事）：带有情感曲线的叙事时刻
- `proof`（证据）：统计数据、案例研究、演示结果
- `opinion`（观点）：热评、异议、反向观点

使用 brief 元数据来定义这些家族之间的预期平衡。

### 3. 合理设定产出目标

参考范围：

- `15-30分钟`：3-6 个优秀剪辑
- `30-60分钟`：5-10 个优秀剪辑
- `60分钟以上`：8-15 个优秀剪辑（如果视频源质量支持）

不要为了凑整数而虚增剪辑数量。小而精的批次胜过滥竽充数的弱批次。

### 4. 在提取前规划平台适配

尽早规划平台适配：

- `9:16` 用于 Shorts、Reels、TikTok
- `1:1` 用于 LinkedIn 和更安全的 feed 复用
- `16:9` 用于幻灯片、演示或宽上下文重要的场合

如果视频源的构图明显无法承受竖版裁剪，请立即在 brief 元数据中说明。

### 5. 构建 Brief

保持 schema 级别的 brief 简洁，并将更丰富的批次计划放在 `brief.metadata` 中。

推荐的元数据键：

- `source_type`
- `source_duration_seconds`
- `clip_target_range`
- `clip_families`
- `primary_platforms`
- `secondary_platforms`
- `selection_criteria`
- `known_visual_constraints`
- `distribution_goal`

### 6. 质量门禁

- 剪辑数量目标切合实际，
- 平台组合与内容匹配，
- brief 在提取开始前定义了排序标准，
- 智能体已确认任何明显的重帧限制。

## 常见陷阱

- 在质量之前先以数量规划批次。
- 假设每个视频源都能顺利产出竖版剪辑。
- 将所有剪辑视为可互换的，而非有意差异化。
- 在未定义本次批次"好"的标准之前就开始提取。
