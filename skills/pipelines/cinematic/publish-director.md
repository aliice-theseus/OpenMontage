# 发布导演 - 电影化流水线

## 适用场景

打包电影化作品及其精简版本，确保主版本清晰明确，分发意图一目了然。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/publish_log.schema.json` | 制品验证 |
| 前置产物 | `state.artifacts["compose"]["render_report"]`, `state.artifacts["proposal"]["proposal_packet"]`, `state.artifacts["research"]["research_brief"]`, `state.artifacts["script"]["script"]` | 最终输出和节拍图 |
| 手册 | 当前风格手册 | 调性和命名一致性 |

## 流程

### 1. 区分主版本和衍生版本

典型的交付物：

- 主预告片或品牌影片，
- 预告精简版，
- 社交媒体精简版，
- 海报帧或缩略图概念。

### 2. 元数据匹配调性

打包应反映实际情绪：

- 戏剧性，
- 高端，
- 神秘，
- 沉思，
- 紧迫。

### 3. 保留编辑真相

存储在 `publish_log.metadata` 中：

- `hero_output`
- `derivative_outputs`
- `poster_frame_notes`
- `distribution_notes`

### 4. 质量门禁

- 主版本输出清晰标识，
- 衍生版本输出按用途标签区分，
- 元数据符合调性，
- 打包成果无需手动清理即可使用。

## 常见陷阱

- 预告精简版和主版本输出混在一起，没有清晰命名。
- 编写忽略情绪的通用元数据。
- 将所有精简版本视为可互换。
