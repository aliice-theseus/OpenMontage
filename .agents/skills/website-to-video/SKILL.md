---
name: website-to-video
description: "捕获通用网站/URL 并将其转换为 HyperFrames 视频（网站导览、展示或使用网站自身视觉元素的社交短片）。使用无头 Chrome 截图 + 品牌资源。当意图是通用的——作品集/博客/着陆页展示或网站的社交短片时使用。不适用于：产品/SaaS 发布或推广（→ /product-launch-video，即使来自 URL）；主题讲解无网站（→ /faceless-explainer）；GitHub PR（→ /pr-to-video）；为现有视频添加字幕（→ /embedded-captions）；短的无旁白页面高亮动态图形（→ /motion-graphics）。不确定发布和通用网站的区别？问一个问题或从 /hyperframes 开始。"
---

> **media-use**: 在获取音频/图片之前，调用 `/media-use` 从 HeyGen 目录解析 BGM/SFX/图片。先运行 `--adopt` 注册现有资源。参见 `/media-use` 技能。

# 网站到 HyperFrames

捕获一个网站，然后从中制作专业视频。

> **在步骤 0 之前确认路径。** 此技能制作的是**面向/来自通用网站**的视频。如果用户实际上是**营销/发布/推广产品**（即使来自此 URL，即使是「我们网站的推广」）→ `/product-launch-video`。**无网站的主题讲解** → `/faceless-explainer`；**GitHub PR** → `/pr-to-video`；**重新剪辑/重新调色/重新排序现有视频文件** → 不在范围内。因模糊的「制作视频」而路由到此，或不确定发布与通用网站的区别？**先阅读 `/hyperframes`**（完整路由表 + § HyperFrames 不能做什么）。

用户会说类似：

-「把这个网站变成 15 秒的 Instagram 社交短片」
-「从 https://... 制作 30 秒的网站导览/展示」
-「捕获我们的首页并用它自己的视觉元素制作视频」

工作流有 7 个步骤。每个步骤产生一个工件，作为下一步的关卡。默认情况下是协作式的——标记为 💬 的关卡会停止并询问用户。如果用户指示自主模式（「替我做决定」、「给我惊喜」），💬 用户偏好关卡将被跳过；参见 step-2-brief.md 了解如何传播。

**自主模式不是「跳过所有关卡」。** 自动模式涵盖用户偏好问题（TTS 提供商、语音、颜色强调、节拍数、音乐是/否、字幕是/否——代理代表用户做决定）。它不包括质量验证关卡。以下内容在自动模式下仍不可跳过：

- 资源审计（步骤 3）——查看联系表并为每个资源证明使用/跳过
- 逐节拍 HTML 阅读（步骤 5）——每个节拍的结构化证据块
- DoD 清单（步骤 6）——包括动画映射、逐警告 WCAG 验证、音频/动作播放
- 诚实披露部分（步骤 6）——「我未验证的内容」必须出现在你的最终总结中

如果你发现自己推理「自动模式偏向行动，所以我跳过 X」——而 X 是验证关卡，不是偏好问题——这种推理是错误的。偏向行动适用于决定**构建什么**，而不是决定**是否验证**。

---

## 步骤 0：捕获与理解品牌

**阅读：** [references/step-0-capture.md](references/step-0-capture.md)

捕获网站，然后阅读提取的数据以理解**品牌和产品**——它做什么、为谁服务、用什么声音说话、处于什么情绪。捕获的资源是以后使用的品牌工具箱，不是视频的构建模块。

**在简报前显示登录状态**——运行 `npx hyperframes auth status` 并**如实传递其输出（不要转述或重写）。** 它报告语音/BGM 将使用 HeyGen 还是本地引擎，以及未登录时如何登录。**如果未登录，停止并等待用户选择——登录，或说「继续」/「离线」以使用本地引擎继续——然后再询问简报或任何其他内容。** 将其视为真正的决策点，不是路过备注；不要将选择折叠到简报问题中，也不要将密钥写入每个仓库的 `.env`。（在自主模式下，记录状态并离线继续。）参见 `../hyperframes-media` → 预检了解规范指导。

**关卡：** 打印网站摘要——策略优先（产品做什么、为谁服务、品牌声音）然后资源/颜色/字体清单；显示登录状态（已登录，或正在离线继续）。

---

## 步骤 1：品牌标识

**阅读：** [references/step-1-design.md](references/step-1-design.md)

编写 DESIGN.md——品牌备忘单，涵盖视觉标识：颜色、字体、组件样式、布局原则。使用 `design-styles.json` 获取精确的计算值。

**速度选项：** 对于快节奏视频（每节拍广告牌），DESIGN.md 可以是 50 行的颜色 + 字体 + 做/不做摘要——而不是 300 行的文档。步骤 5 中的子代理提示直接粘贴品牌值，因此 DESIGN.md 的深度仅对复杂作品重要。

**关卡：** `DESIGN.md` 存在（任意长度），至少包含：调色板、字体选择、做/不做。

---

## 步骤 2：策略与信息

**阅读：** [references/step-2-brief.md](references/step-2-brief.md)、[references/capabilities.md](references/capabilities.md)（扫描目录——仅在需要时深入具体章节）

在讨论视觉或资源之前，与用户对齐**视频必须传达什么**。解析用户的提示——他们可能已经给了你视频类型和风格。只询问缺失的内容：这个视频必须说的**一件事**、叙事弧和受众。

**关卡：** 视频类型、时长、格式以及——关键地——信息和叙事弧已锁定。没有这些，步骤 3 无法编写概念优先的故事板。

---

## 步骤 3：故事板 + 脚本 💬

**阅读：** [references/step-3-storyboard.md](references/step-3-storyboard.md)

编写概念优先的故事板：信息 → 叙事弧 → 服务弧的节拍 → 每个节拍的技术 → 最后品牌强调通过。然后编写匹配的旁白脚本。将两者呈现给用户，附带节拍逐拍摘要。迭代直到用户批准。

**关卡：** `STORYBOARD.md` + `SCRIPT.md` 存在**且**用户已批准计划。

---

## 步骤 4：配音、时序 + 字幕 💬

**阅读：** [references/step-4-vo.md](references/step-4-vo.md)

如果步骤 2 说无需旁白——询问背景音乐，然后跳到步骤 5。否则：询问用户希望使用哪个 TTS 提供商（HeyGen TTS、ElevenLabs 或 Kokoro），生成音频，转录，将时间戳映射到节拍。然后询问字幕。

**关卡：** (a) 没有要求旁白且故事板有手动节拍时序，或 (b) `narration.wav` + `transcript.json` 存在且节拍时序已用实际时长更新。

---

## 步骤 5：构建作品

**阅读：** `hyperframes` 技能（加载它——每条规则都重要）
**阅读：** [references/step-5-build.md](references/step-5-build.md)

按照故事板（步骤 3）确定的架构和节奏构建 index.html 和作品。子代理在每个节拍报告前运行 `hyperframes lint` 和 `hyperframes snapshot`。

**关卡：** 主代理已自上而下阅读每个 `compositions/beat-N.html`，对照 DESIGN.md 和 STORYBOARD.md。逐节拍清单位于 [step-5-build.md](references/step-5-build.md)。

---

## 步骤 6：验证与交付

**阅读：** [references/step-6-validate.md](references/step-6-validate.md)

检查、验证、拍摄按视频长度缩放的快照（公式：`max(节拍数 × 3, ceil(时长_秒 / 2))`），并审核每个快照。在交付前修复问题。交付 localhost Studio 项目 URL——仅在用户明确要求时渲染为 MP4。仅在交接时展示 Studio URL——它是最终、稳定的预览；构建阶段的快照是无头的，因此不要在构建过程中弹出预览。

**交付你引以为豪的作品。** 在交接前问问自己：我会把这个发布到社交媒体上并署上我的名字吗？如果不是，修复问题。

**关卡：** `npx hyperframes lint` 和 `npx hyperframes validate` 通过，零错误，最终响应包含活动的 Studio 项目 URL。

---

## 快速参考

### 视频类型

各视频类型的典型约束——作为起点使用，不是公式。节拍数应由内容和旁白决定，而不是目标范围。

| 类型 | 典型时长 | 时长驱动因素 | 旁白 |
| --------------------- | ---------------- | ------------------ | --------------------- |
| 社交广告（IG/TikTok） | 10–15s | 平台限制 | 可选 |
| 产品演示 | 30–60s | 脚本长度 | 完整旁白 |
| 功能公告 | 15–30s | 功能复杂度 | 完整旁白 |
| 品牌短片 | 20–45s | 音乐曲目 | 可选，音乐为主 |
| 发布预告 | 10–20s | 钩子能量 | 最少 |

节拍数不在此表中是有意设计的——应来自故事板，而不是来自「社交广告 = 3-4 个节拍」。复杂产品的社交广告可能需要 5 个精心时机的节拍。有一个强大视觉主题的品牌短片可能需要 3 个。

### 格式

- **横屏**：1920x1080（默认）
- **竖屏**：1080x1920（Instagram Stories、TikTok）
- **方形**：1080x1080（Instagram 信息流）

### 参考文件

| 文件 | 何时阅读 |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| [step-0-capture.md](references/step-0-capture.md) | 步骤 0——捕获、理解品牌和产品，编写策略优先的网站摘要 |
| [step-1-design.md](references/step-1-design.md) | 步骤 1——编写 DESIGN.md 品牌备忘单（5 个章节，250-350 行；广告牌式社交广告的 50 行快速路径） |
| [step-2-brief.md](references/step-2-brief.md) | 步骤 2——与用户对齐信息、叙事弧、受众 |
| [capabilities.md](references/capabilities.md) | 步骤 2 和 5——HyperFrames 能做什么的完整清单（24 个章节）。在简报期间扫描目录，构建期间深入具体章节 |
| [step-3-storyboard.md](references/step-3-storyboard.md) | 步骤 3——故事板 + 脚本（组合）带用户审核关卡 |
| [step-4-vo.md](references/step-4-vo.md) | 步骤 4——TTS 提供商选择、生成、时序 |
| [step-5-build.md](references/step-5-build.md) | 步骤 5——构建 index.html + 作品 |
| [step-6-validate.md](references/step-6-validate.md) | 步骤 6——检查、验证、快照（按视频长度缩放）、预览 |
| [techniques.md](../hyperframes/references/techniques.md) | 步骤 3 和 5——13 种原始动画技术及代码模式（适配，不要复制粘贴） |
| [html-in-canvas-patterns.md](../hyperframes/references/html-in-canvas-patterns.md) | 步骤 5——HTML-in-Canvas 效果的完整代码模式（位于 hyperframes 技能中） |
