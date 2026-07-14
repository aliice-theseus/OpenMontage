# 发布导演 - Clip Factory 流水线

## 使用时机

此阶段将剪辑批次打包为分发计划。目标不仅仅是导出文件，而是打造一个可用的内容引擎。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | 制品验证 |
| 前置制品 | `state.artifacts["compose"]["render_report"]`, `state.artifacts["idea"]["brief"]`, `state.artifacts["script"]["script"]` | 输出、排序和目标 |
| Playbook | 当前样式 playbook | 品牌语调 |

## 流程

### 1. 用最强的剪辑开头

不要按时间顺序安排发布。按排名安排发布。

第一个发布的剪辑通常是：

- 最强的钩子，
- 最完整的独立剪辑，
- 与批次目标最一致的剪辑。

### 2. 根据平台定制文案

每个平台需要自己的语气和包装方式：

- TikTok / Reels：直接、快速、钩子驱动
- Shorts：可搜索、关键词感知
- LinkedIn：见解驱动、更加专业
- X：简短、有力、观点友好

### 3. 干净地打包整个批次

按平台分组，包含可即用粘贴的文本资源，而不仅仅是视频文件。

### 4. 保留批次的真实信息

存储在 `publish_log.metadata` 中：

- `clip_catalog`
- `posting_order`
- `platform_copy_map`
- `schedule_notes`

### 5. 质量门禁

- 最强的剪辑引领发布节奏，
- 标题/说明因平台而异，
- 导出文件夹无需额外清理即可使用，
- 批次目录清晰关联排名、文件路径和发布意图。

## 常见陷阱

- 在同一天发布整个批次。
- 在所有平台使用同一文案。
- 渲染完成后丢失排名/排序逻辑。
