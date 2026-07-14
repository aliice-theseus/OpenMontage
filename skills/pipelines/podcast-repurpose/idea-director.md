# 创意导演 - 播客二次利用流水线

## 何时使用

当源素材是播客剧集（纯音频或视频播客），且用户需要片段、社交媒体素材或伴随的长视频处理方案时，使用此流水线。

你的首要职责是根据实际存在的源素材判断哪些是可行的。

## 运行时选择（强制要求 — 展示约束条件，不要静默选择）

锁定 `render_runtime = "remotion"`（用于 audiogram 和合成输出）或 `"ffmpeg"`（用于纯音频主导的片段导出）。**Phase 1 中 HyperFrames 在此流水线上不是有效的运行时** — 播客输出依赖于 Remotion 的逐词字幕栈，HyperFrames 尚未具备同等能力。

根据 AGENT_GUIDE.md → "展示两种合成运行时（硬性规则）"：向用户说明约束条件 — "你的机器上可以使用 HyperFrames，但 podcast-repurpose 依赖于 Remotion 的字幕烧录，因此 remotion 是这里唯一可行的选择"。记录一个 `render_runtime_selection` 决策，其中 hyperframes 的 `rejected_because: "caption-burn parity deferred on podcast-repurpose"`。

## 参考输入

- `docs/podcast-repurposing-best-practices.md`
- `skills/creative/short-form.md`
- `skills/creative/long-form.md`

## 流程

### 1. 对源素材进行分类

记录源素材模式：

- `audio_only`
- `video_podcast`
- `hybrid`（音频加静态图片、封面艺术、嘉宾照片）

同时记录对话格式：

- 单人独播
- 访谈
- 多人讨论
- 叙述型 / 制作型节目

### 2. 选择符合实际的交付物

默认交付物应基于现有源素材和工具切实可行。

安全选项：

- 短视频精彩片段，
- audiogram 或以字幕为主导的片段，
- 以引用为主导的片段，
- 一个可选的全剧集伴随布局。

除非源视频、品牌素材和可选图像确实存在，否则不要假设高制作水准的全剧集 YouTube 处理方案。

### 3. 设定合理的交付物组合

典型起点：

- `3-5` 个精彩片段
- 如果剧集有精彩的金句，`1-3` 个以引用为主导的素材
- 如果源素材具备条件，可选的长期式伴随视频

### 4. 尊重平台差异

- `9:16` 用于 Shorts、Reels、TikTok
- `1:1` 用于 LinkedIn 和更安全的 Feed 二次利用
- `16:9` 用于 YouTube 伴随视频

如果源素材是纯音频，请在 brief 中明确说明。下游阶段不应规划不存在的说话人画面视频。

### 5. 构建 Brief

使用 `brief.metadata` 存储更丰富的播客特定契约：

- `source_mode`
- `show_name`
- `episode_title`
- `episode_number`
- `speakers`
- `conversation_format`
- `deliverable_mix`
- `brand_assets_available`
- `full_episode_companion_feasible`

### 6. 质量门禁

- 交付物组合与实际源素材匹配，
- 片段数量对于剧集长度来说是现实的，
- brief 明确指出视觉效果将以源素材、引用还是 audiogram 为主导，
- 长格式的雄心与可用素材相匹配。

## 常见陷阱

- 将纯音频和视频播客源视为相同的制作问题。
- 从一集薄弱的剧集规划过多交付物。
- 在没有素材支持的情况下承诺丰富的全剧集视觉处理方案。
