# 发布导演 - 播客二次利用流水线

## 何时使用

打包播客衍生的片段和伴随素材，使每个短视频片段都能指向原剧集，而不是成为孤立的碎片。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | Artifact 验证 |
| 前置 artifacts | `state.artifacts["compose"]["render_report"]`, `state.artifacts["idea"]["brief"]`, `state.artifacts["script"]["script"]` | 输出、源真相、章节 |
| Playbook | 活动样式 playbook | 品牌声音 |

## 流程

### 1. 将每个片段链接回剧集

每个短视频素材应引用：

- 节目名称，
- 剧集标题或编号，
- 相关嘉宾姓名，
- 完整剧集的访问地址。

### 2. 定制文案

- Shorts / Reels / TikTok：以钩子为主导，简洁明了
- LinkedIn：以见解为主导，更具上下文
- YouTube 伴随视频：章节丰富，利于搜索

### 3. 安排发布顺序

推荐顺序：

1. 最强有力的预告片段
2. 次佳的见解片段
3. 以引用或嘉宾为主导的后续片段
4. 其余支撑性片段

### 4. 在 Metadata 中存储交叉引用信息

推荐的 metadata 键：

- `episode_reference`
- `guest_tags`
- `posting_schedule`
- `clip_to_episode_map`

### 5. 质量门禁

- 每个片段都指向剧集，
- 嘉宾归属正确，
- 文案与平台匹配，
- 发布顺序反映实际片段质量。

## 常见陷阱

- 发布没有明确剧集引用的片段。
- 在相关受众关注时忘记标记或提及嘉宾。
- 在所有平台上复用同一种字幕风格。
