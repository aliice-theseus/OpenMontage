# 创意总监 - 虚拟形象发言人管线

## 使用时机

当交付物是以主持人为主导的虚拟形象视频时使用本管线：包括发言人广告、产品介绍、入职引导消息、内部沟通更新，或简短的有脚本讲解视频，其中主讲人始终是视觉核心。

你的首要任务是诚实地对虚拟形象路径进行分类，避免在无法实现的生产方案上撰写精致的文案。

## 运行时选择（强制要求 — 说明约束条件，不要静默选择）

锁定 `render_runtime = "remotion"`。**HyperFrames 在此管线的 Phase 1 中不是有效运行时** — avatar-spokesperson 依赖 Remotion 的 `TalkingHead` 合成组件和 `remotion_caption_burn`，两者在 Phase 1 中均未与 HyperFrames 实现功能对等。

根据 AGENT_GUIDE.md → "展示两种合成运行时（硬性规则）"：不要静默默认选择。告知用户："您的机器上可以使用 HyperFrames，但 avatar-spokesperson 依赖 Remotion 的 TalkingHead 合成组件和字幕烧录功能，因此 remotion 是这里唯一可行的运行时 — 是否继续？" 记录 `render_runtime_selection` 决策，hyperframes 设为 `rejected_because: "TalkingHead + caption parity deferred on avatar-spokesperson"`。

## 参考输入

- `docs/avatar-spokesperson-best-practices.md`
- `skills/creative/storytelling.md`
- `skills/creative/short-form.md`

## 流程

### 1. 分类虚拟形象路径

记录项目实际采用的生产模式：

- `platform_avatar`
- `photo_talking_head`
- `presenter_plate_lip_sync`

同时记录该虚拟形象是否已存在，还是需要在当前运行之外另行创建。

### 2. 定义信息形态

捕获以下内容：

- 目标受众，
- 核心卖点或 CTA，
- 目标时长，
- 目标平台，
- 视频是销售导向、入职引导、技术支持还是公告通知。

发言人视频在只有一个明确任务时效果最佳。

### 3. 获取源素材实情

创意简报应明确说明：

- 是否提供干净的旁白音频，
- 是否可以使用 TTS，
- 是否有品牌背景或叠加层，
- 是否需要字幕，
- 是否预期有多语言版本。

### 4. 构建创意简报

推荐元数据键：

- `avatar_path`
- `avatar_exists`
- `narration_source`
- `target_audience`
- `cta_type`
- `background_strategy`
- `deliverable_mix`
- `missing_capabilities`

### 5. 质量门禁

- 虚拟形象路径明确，
- 信息范围足够聚焦，适合发言人格式，
- 缺失的旁白或虚拟形象依赖项早期可见，
- 交付物符合实际源素材条件。

## 常见陷阱

- 将通用的生成视频请求当作确定性的虚拟形象工作流处理。
- 在确认虚拟形象和旁白路径之前就编写 CTA。
- 在主角布局尚未验证之前就规划多种宽高比。
