# 创意导演 - 混合流水线

## 使用时机

当项目结合真实源素材与支持视觉内容时使用此流水线：访谈加图表、视频片段加叠加层、屏幕录制加品牌图形，或源主导剪辑加生成插片。

混合并非万能方案。你的首要任务是定义什么内容保持主导地位。

## 运行时选择（必选 — 呈现两种运行时）

在锁定制作计划之前，与用户一起决定 `render_runtime`。混合流水线同时支持 Remotion 和 HyperFrames；两者均非自动默认选项。遵循 AGENT_GUIDE.md → "Present Both Composition Runtimes (HARD RULE)" 中的约定：

1. 查询 `video_compose.get_info()["render_engines"]`。如果 `remotion` 和 `hyperframes` 均为 `True`，则向用户呈现两者，并附上针对该 brief 的分析：
   - **Remotion** — 适用于源素材占主导且支持层为 React 场景组件（图表、标注、文本卡片）的情况。Remotion 通过 `<OffthreadVideo>` 在一次渲染中合成视频片段 + React 叠加层。
   - **HyperFrames** — 适用于支持层为 HTML/GSAP 原生内容（动态标注、注册块、排版叠加）且源素材通过 `<video class="clip">` 嵌入的情况。
2. 根据锚定媒介和支持层的形态推荐一个，并说明理由。
3. 等待用户明确批准。
4. 在 `decision_log` 中将选择记录为 `render_runtime_selection` 决策，`options_considered` 中必须包含两种运行时。

如果两者都可用但 `options_considered` 中只有一种运行时，则 `render_runtime_selection` 决策将被审稿人视为 CRITICAL 问题。

## 参考输入

- `docs/hybrid-video-best-practices.md`
- `skills/creative/storytelling.md`
- `skills/creative/video-editing.md`

## 流程

### 1. 选择锚定媒介

选择故事讲述的锚定方式：

- `talking_head`
- `broll_footage`
- `screen_recording`
- `still_sequence`
- `narration_led_graphics`

### 2. 定义支持层

可能的支持层：

- 字幕，
- 图表，
- 代码视觉化，
- 数据卡片，
- 生成插片，
- 旁白，
- 音乐。

每个支持层应解决特定问题，而不仅仅是装饰时间线。

### 3. 决定交付物组合

常见输出：

- 主剪版本，
- 竖屏缩减版，
- 方形缩减版，
- 分章节版本，
- 广告变体。

### 4. 构建 Brief

推荐的元数据键：

- `anchor_medium`
- `source_inventory`
- `support_layers`
- `deliverable_mix`
- `missing_capabilities`
- `fallback_policy`

### 5. 质量门禁

- 锚定媒介明确，
- 支持层有合理依据，
- 交付物组合匹配源素材清单，
- 缺失能力尽早暴露。

## 常见陷阱

- 什么都叫混合，却没有定义主要媒介。
- 在了解源素材之前就规划支持层。
- 将可选的生成插片视为必然存在的资源。

