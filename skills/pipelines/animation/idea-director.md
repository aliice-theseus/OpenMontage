# 创意导演 — 动画管线

## 使用时机

当视频应主要通过设计好的动态来构建时使用本管线：动态图形、动态排版、图表驱动的解说、数学视觉或插画风格动画。

当项目主要是实拍素材并带有少量叠加时，不使用本管线。那属于 `hybrid` 管线。

## 参考输入

- `docs/animation-best-practices.md`
- `skills/creative/animation-pipeline.md`
- `skills/creative/storytelling.md`

## 流程

### 1. 分类动画模式

选择主要模式：

- `diagrammatic`（图表式）
- `motion_graphics`（动态图形）
- `kinetic_type`（动态排版）
- `math_animation`（数学动画）
- `illustrative`（插画风格）
- `mixed_animation`（混合动画）

### 2. 尽早决定视觉路径

确定应由哪些工具执行工作：

- `diagram_gen`
- `math_animate`
- `code_snippet`
- `image_selector`
- `video_selector` 或具体的视频提供者工具
- 来源提供的素材

如果请求的模式依赖于不可用的工具，请在简介元数据中立即说明。

### 3. 选择复用策略

每个场景都独特时，动画成本很高。定义：

- 重复出现的主题元素，
- 布局系统，
- 转场系列，
- 排版层次。

### 4. 构建简介

推荐的元数据键：

- `animation_mode`
- `visual_path`
- `narration_strategy`
- `reuse_strategy`
- `timing_style`
- `blocked_capabilities`

### 5. 质量关卡

- 动画模式明确，
- 视觉路径可行，
- 项目设计为可复用，
- 简介诚实说明缺失的工具。

## 常见陷阱

- 将所有动画视为一个通用类别。
- 为每个场景规划定制视觉效果。
- 隐藏缺失的工具路径直到资产阶段才暴露。
