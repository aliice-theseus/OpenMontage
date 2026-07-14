# 创意导演 - 屏幕演示流水线

## 运行时选择（必须 — 列出所有可行的运行时）

在创意阶段与制作模式一起锁定 `render_runtime`。哪些运行时可行取决于制作模式：

| 制作模式 | 可行的运行时 |
|-----------------|-----------------|
| `real_capture`（实机屏幕录制） | `remotion`（推荐 — 混合录制与叠加层）, `ffmpeg`（纯拼接/裁剪） |
| `synthetic_terminal`（Remotion `TerminalScene`） | 仅限 `remotion` |
| `synthetic_ui`（自定义 HTML UI 演示） | `remotion` 或 `hyperframes` — 真正可选，列出两者 |

根据 AGENT_GUIDE.md → "列出两种合成运行时（硬性规则）"：当制作模式允许多种运行时且机器上两者都可用时（检查 `video_compose.get_info()["render_engines"]`），向用户列出两者，并附上针对该需求的简要分析，推荐其中一个，等待用户批准。不要静默地使用默认值。当制作模式限制了选择时（例如 `synthetic_terminal` 仅限 Remotion），明确告知用户这一限制，而不是静默锁定 remotion。在 `decision_log` 的 `render_runtime_selection` 下记录所有选择及所有考虑过的选项。

## 使用时机

当交付物是屏幕录制风格的演示时使用此流水线。有两种**制作模式** — 在需求说明中选择一种：

| 模式 | 源素材 | 选择时机 |
|---|---|---|
| **`real_capture`** | 通过 `screen_recorder`、`cap_recorder` 或 `playwright-recording` 捕获的实际屏幕录制（MP4） | 真实应用 UI、实时行为、浏览器流程、IDE 插件、用户要求录制自己的屏幕 |
| **`synthetic_terminal`** | 无 — 无需录制。您为 Remotion 编写 `terminal_scene` 分镜 | CLI / 终端 / 安装流程 / make 目标 / git clone / API 密钥配置 — 任何可脚本化且每条命令及输出都可预测的场景 |

**决策问题：** *"我能否在拍摄前预测每一条命令及其输出？"* 如果可以 → 合成模式。如果不行 → 实机录制。

**将制作模式记录在 `brief.metadata.production_mode` 中。** asset-director 读取此字段来选择是使用捕获+叠加资源，还是使用与旁白节奏匹配的 `steps` 列表。

对于 `synthetic_terminal`，在继续之前还需阅读 `.agents/skills/synthetic-screen-recording/SKILL.md` — 它记录了曾导致早期展示渲染失败的节奏规则（命令在场景时间的 40% 内就执行完毕，然后终端在剩余 60% 时间内冻结）。

您在此阶段的工作是将用户需求转化为清晰的程序化视频计划。主要输出是一个符合 schema 的 `brief`，流水线特定的细节存储在 `brief.metadata` 中。

## 操作原则

屏幕演示的最佳实践是一致的：

- 优先关注操作流程而非理论
- 将范围限定在一个工作流或一个结果
- 将旁白映射到可见操作
- 有节制地规划注意力引导
- 在风格之前优先考虑可读性

参考文档：
- `docs/screen-demo-best-practices.md`
- `skills/creative/screen-recording.md`

## 流程

### 1. 检查源素材

在编写需求说明之前使用可用的分析工具：

- `frame_sampler` — 提取代表性帧和关键时刻附近的密集采样
- `scene_detect` — 检测窗口切换、页面变化和重大布局变化
- `transcriber` — 确定录制是否有旁白、仅系统音频或静音

识别：

- 显示的软件和界面
- 正在演示的单个工作流
- 关键交互：点击、输入、滚动、提交、结果
- 明显需要缩放或高亮标注的时刻
- 死时间：安装、构建、加载、重复输入
- `9:16` 是否可行且不失意义

### 2. 分类演示类型

选择一种主导原型：

- `tutorial`（教程）：逐步完成任务
- `feature_showcase`（功能展示）：展示某个功能
- `troubleshooting`（故障排除）：复现并解决问题
- `walkthrough`（引导说明）：解释跨多个工具的多步流程
- `comparison`（对比）：比较两种方法或结果

如果素材混合了多种原型，选择应驱动节奏和打包方式的那一种。

### 3. 设定交付物目标

屏幕演示应保持狭窄范围并以结果为导向：

- `30-60s`：快速提示或功能展示
- `60-120s`：专注的产品引导或 bug 修复
- `120-300s`：分章节教程

默认选择能清晰教授任务的最短时长。除非用户明确需要最小压缩的训练素材，否则不要保留原始时长。

### 4. 选择可行的输出形态

围绕可读性规划发布平台，而非追逐趋势：

- 对密集的桌面 UI 使用 `youtube` 或 `linkedin`
- 仅在活动区域能适应窄裁切时使用 `instagram` 或 `tiktok`
- 当界面有多个面板或代码窗口时，优先选择 `1:1` 或 `16:9`

### 5. 构建需求说明

使用 schema 字段形成精炼的创意合约，将更丰富的制作细节存储于 `metadata` 中。

推荐的 `metadata` 键：

- `source_path`
- `source_duration_seconds`
- `source_resolution`
- `has_voiceover`
- `software_shown`
- `demo_archetype`
- `critical_moments`
- `dead_time_segments`
- `recommended_aspect_ratios`
- `notes_for_scene_planner`

需求说明应回答：

- 观众将学到什么
- 这是给谁看的
- 视频应以什么证明/结果收尾
- 必须展示的操作有哪些
- 哪些裁切方向是安全的

### 6. 质量门禁

在提交检查点之前，验证：

- 工作流范围是否足够窄以适配所选时长
- "啊哈时刻"结果是否被明确识别
- 目标平台是否匹配 UI 密度
- 需求说明是否命名了实际软件而非模糊描述
- 元数据是否为下游阶段提供了足够的制作实况

## 常见陷阱

- 默认将 7 分钟的录制视为 7 分钟的交付物
- 仅因为用户要求短视频就为密集的桌面录制选择 `9:16`
- 在用户真正需要任务完成时编写概念沉重的需求说明
- 未能标注静音；如果没有旁白，下游阶段必须立即知晓
