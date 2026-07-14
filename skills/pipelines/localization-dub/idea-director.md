# 创意导演 - 本地化配音流水线

## 使用时机

当用户拥有源视频并希望获得翻译后的交付物时使用此流水线：字幕、配音音频或一种或多种目标语言的本地化视频。

你的首要职责是确定实际需要的本地化类型，因为纯字幕、配音音频和唇形同步翻译是三种不同的工作。

## 运行时选择（强制 — 呈现约束条件，不要默默选择）

锁定 `render_runtime = "remotion"`（按语言组合交付物，含按地区字幕烧录/唇形同步）或 `"ffmpeg"`（在源视频上直接烧录纯字幕，无需合成）。**HyperFrames 在第一阶段不是此流水线的有效运行时** — 本地化依赖于 Remotion 的字幕栈，而对于带唇形同步的配音，则依赖于 Remotion TalkingHead 流水线。

根据 AGENT_GUIDE.md → "呈现两种合成运行时（硬性规则）"：不要默默地默认使用 remotion。告知用户："HyperFrames 可用，但 localization-dub 依赖于 Remotion 的字幕 + TalkingHead 对等功能，第一阶段尚未就绪 — remotion 是唯一可行的选择"。记录一个 `render_runtime_selection` 决策，其中 hyperframes 的 `rejected_because: "caption + lip-sync parity deferred on localization-dub"`。

## 参考输入

- `docs/localization-dubbing-best-practices.md`
- `skills/creative/short-form.md`
- `skills/creative/long-form.md`

## 流程

### 1. 定义本地化范围

需捕获的信息：

- 源语言
- 目标语言
- 审核负责人
- 是否需要词汇表或法务审核
- 用户需要的是字幕、配音音频、唇形同步还是混合形式

### 2. 对源视频进行分类

记录源模式：

- `single_speaker`（单人主讲）
- `multi_speaker`（多人主讲）
- `voiceover_led`（画外音主导）
- `speaker_led_on_camera`（出镜主讲）

同时记录屏幕文字或动态图形是否需要手动替换或覆盖处理。

### 3. 选择符合实际的交付物

可能的交付物：

- 仅字幕包
- 无唇形同步的配音视频
- 唇形同步的本地化视频
- 按语言导出的捆绑包

### 4. 构建需求简报

推荐的元数据键：

- `source_language`
- `target_languages`
- `deliverable_mode_map`
- `glossary_terms`
- `protected_terms`
- `review_requirements`
- `timing_risks`

### 5. 质量门禁

- 本地化范围明确
- 目标输出符合实际
- 词汇表和审核需求已捕获
- 发言人数量或可见嘴部带来的风险已揭示

## 常见陷阱

- 将所有翻译需求都称为配音需求
- 在音频生成前忽略词汇表控制
- 在视觉困难的源素材上承诺唇形同步而不事先警告
