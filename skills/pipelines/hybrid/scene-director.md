# 场景导演 - 混合流水线

## 使用时机

你将混合结构转化为一个视觉系统，使源素材保持可见，同时控制支持层的数量。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | 产物验证 |
| 前置产物 | `state.artifacts["script"]["script"]`, `state.artifacts["idea"]["brief"]` | 混合结构和源素材真值 |
| 工具 | `frame_sampler`, `scene_detect` | 可选的源素材检查 |
| Playbook | 当前样式 playbook | 布局一致性 |

## 生成镜头的导演技能

如果支持层包含 AI 视频镜头，先读取 `.agents/skills/direct-visual-quality/SKILL.md` 和 `.agents/skills/direct-camera-movement/SKILL.md`，再填写色调/光源、景别、主运镜、速度和起止构图。若镜头包含打斗、追逐、跑酷、枪战或竞技动作，再读取 `.agents/skills/direct-action-scenes/SKILL.md`，把动作拆为因果清晰的单镜头节拍。源素材镜头只应用这些技能做分析和匹配，不得虚构原素材中不存在的运动。

## 流程

### 1. 保持锚定媒介可见

如果作品是源主导的，源素材必须在场景计划中保持视觉上的首要地位。不要将锚定内容隐藏在持续的叠加层之后。

### 2. 为明确任务保留支持素材

使用支持场景用于：

- 章节过渡，
- 说明性图表，
- 数据强调，
- CTA 或总结时刻，
- 填补空白的内容插片。

### 3. 规划多版本安全性

如果项目需要多种宽高比，请定义以下位置：

- 字幕放置，
- 说话人标签放置，
- 图表或代码安全区域，
- 对裁切敏感的源素材变为不安全的区域。

### 4. 使用元数据定义平衡规则

推荐的元数据键：

- `anchor_rules`
- `support_rules`
- `safe_zones`
- `variant_rules`
- `overlay_density_limits`

### 5. 质量门禁

- 锚定媒介在预期位置保持首要地位，
- 支持层有数量限制且目的明确，
- 宽高比规划明确，
- 没有场景依赖不可见的未来魔法。

## 常见陷阱

- 将源主导场景变成叠加层混乱。
- 直到合成阶段才想起多版本安全区域。
- 每个过渡都用生成的内容插片。
