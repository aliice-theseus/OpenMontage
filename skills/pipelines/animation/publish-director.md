# 发布导演 — 动画管线

## 使用时机

打包动画，使元数据、缩略图概念和平台框架反映项目实际的视觉系统。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | 产物验证 |
| 前置产物 | `state.artifacts["compose"]["render_report"]`、`state.artifacts["proposal"]["proposal_packet"]`、`state.artifacts["research"]["research_brief"]`、`state.artifacts["script"]["script"]` | 最终输出和主题框架 |
| 样式手册 | 活跃的样式手册 | 视觉命名一致性 |

## 流程

### 1. 使打包与动画模式匹配

示例：

- 图表密集的视频应看起来结构清晰、易读，
- 动态排版作品应围绕强有力的文案打包，
- 插画风格动画应围绕主角图像打包。

### 2. 保留视觉系统的真实性

存储在 `publish_log.metadata` 中：

- `animation_mode`
- `hero_frame_notes`
- `thumbnail_concept`
- `platform_notes`

### 3. 质量关卡

- 元数据符合实际的动画模式，
- 缩略图概念与最终视觉系统匹配，
- 导出文件按用途和平台标记，
- 打包后的作品无需额外手工即可使用。

## 常见陷阱

- 编写忽略动画风格的通用元数据。
- 创建与最终画面无关的缩略图概念。
- 混合平台变体而没有清晰的标签。
