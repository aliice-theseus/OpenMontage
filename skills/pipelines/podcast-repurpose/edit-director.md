# 剪辑导演 - 播客二次利用流水线

## 何时使用

此阶段为短视频片段和任何可选的全剧集伴随素材创建实际的时间轴逻辑。音频仍然是主要内容。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Artifact 验证 |
| 前置 artifacts | `state.artifacts["assets"]["asset_manifest"]`, `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]` | 素材、布局、转录文本时间 |
| Playbook | 活动样式 playbook | 动效和字幕规则 |

## 流程

### 1. 快速构建片段时间轴

对于短视频片段：

- 以钩子开场，
- 立即显示字幕，
- 让说话人归属清晰可见，
- 让结尾干净利落地收束。

### 2. 使剪辑匹配处理方案

- 源视频片段应强调说话人构图和反应，
- audiogram 片段应强调字幕、说话人身份和节奏，
- 引用主导的片段应在句子结束后留出足够的阅读时间。

### 3. 保持全剧集伴随视频简洁

如果制作伴随视频：

- 使用章节卡片，
- 使用有限的循环视觉系统，
- 如果素材不足，不要强行追求持续的视觉新鲜感。

### 4. 使用 Metadata 记录更丰富的时间轴注释

推荐的 metadata 键：

- `clip_timelines`
- `quote_hold_times`
- `speaker_change_markers`
- `chapter_card_windows`

### 5. 质量门禁

- 每个短视频片段快速吸引注意力，
- 字幕和归属信息呈现完整，
- 引用主导的片段停留时间足够阅读，
- 长格式伴随视频在编辑上诚实且在技术上可行。

## 常见陷阱

- 构建忽略说话人身份的通用 audiogram。
- 音频一结束就立即切断引用片段，不给文字阅读时间。
- 将长格式伴随视频变成制作精良的视频播客的拙劣模仿。
