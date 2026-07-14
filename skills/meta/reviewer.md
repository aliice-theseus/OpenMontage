# 审查者 — 元技能

## 何时使用

在完成任何流水线阶段的工作后、在设置检查点之前。你是"工作完成"和"工作被接受"之间的质量门。本技能用指令驱动的自我审查协议取代 Python 审查者类。

每个阶段都要被审查。无一例外。审查质量决定了最终视频是否值得观看。

## 批评质量（CHAI 规则）

> 发现 ≠ 批评。发现识别问题；批评告诉下一阶段如何修复。CMU/Harvard CHAI 研究（"Building a Precise Video Language with Human-AI Oversight"，arXiv 2604.21718v2）表明，在三个维度上衡量的批评质量直接决定下游输出质量。在每次审查中应用所有三个维度。
>
> **准确。** 每个发现必须引用具体的工件字段、行号或可见的资产帧。禁止幻觉式批评——如果你无法指出问题在哪里，你就是在猜测。
>
> **完整。** 一个发现了一个错误但错过了第二个错误的审查，比评分为"需要另一次审查"然后继续更糟糕。如果你发现一个关键问题，在返回之前扫描同一类的其余部分。模式匹配：这个工件的其他地方可能隐藏着同样的错误？
>
> **建设性。** 每个"关键"发现**必须**提出具体的修复方案，而不仅仅识别问题。"字幕错了"→"字幕写着'右边的男人'；男人在画面左侧。替换为'画面左侧的男人。'"如果你无法提出修复方案，将该发现标记为"调查"而非"关键"。
>
> 移除这三个属性中的任何一个都会可测量地损害流水线输出。审查者是扼制点——请严格把关。

## 协议

### 第 1 步：加载审查上下文

在审查之前，收集：
1. 流水线清单中该阶段的**审查重点项**（`review_focus` 字段）
2. 清单中该阶段的**成功标准**（`success_criteria` 字段）
3. **活动 playbook** 的质量规则
4. 该阶段产生的**工件**

### 第 2 步：Schema 验证

首先，不可协商的检查：
- 对照 JSON schema（`schemas/artifacts/<name>.schema.json`）验证工件
- 如果 schema 验证失败，这是**关键**发现——立即修复，不得继续

### 第 3 步：按审查重点项审查

对清单中的每个 `review_focus` 项：
1. 对照此特定标准评估工件
2. 分配严重性：
   - **关键（critical）**——必须在继续前修复。工件已损坏、不完整或危险地错误。**根据 CHAI 规则，每个关键发现必须携带 `proposed_fix`（具体的替换文本、确切的字段值或具体的纠正措施）。没有修复方案的关键发现降级为 `investigation`。**
   - **建议（suggestion）**——应该修复。能显著改善质量但不阻碍进展。**建议必须携带描述如何改进的 `proposed_change`。**
   - **挑刺（nitpick）**——可以修复。锦上添花的微小优化。可以独立存在，无需提出修改方案。
   - **调查（investigation）**——确实存在问题但你无法定位修复方案。提出以便下一轮处理；不要因此阻止流程。
3. 写出具体、可操作的发现（不要含糊）

**好的发现：** "第 3 段旁白有 180 个词，对应 10 秒窗口——即 1080 wpm，无法完成。减少到 25 个词。"
**坏的发现：** "脚本可能太长了。"

### 第 4 步：对照 Playbook 交叉检查

如果风格 playbook 处于活动状态，验证：
- [ ] 色彩引用匹配 playbook 调色板
- [ ] 转场类型在 playbook 的允许集合内
- [ ] 节奏规则得到遵守（最小/最大时长）
- [ ] 资产描述包含 playbook 风格提示
- [ ] 质量规则未被违反

每个违规是一个**建议**严重性发现。

### 第 5 步：评估成功标准

对清单中的每个 `success_criteria` 项：
- 标准是否满足？（是/否/部分）
- 如果未满足，创建**关键**发现

### 第 6 步：做出决定

按严重性统计发现：

| 场景 | 操作 |
|----------|--------|
| 0 个关键，任何建议/挑刺 | **通过** — 继续到检查点。记录建议备案。 |
| 1+ 个关键发现 | **修订** — 修复所有关键发现，然后重新审查（最多 2 轮）。 |
| 2 轮修订后仍有关键问题 | **带警告通过** — 无论如何继续，记录未解决的问题。永远不要无限期阻止。 |

### 第 7 步：记录审查

将你的审查结构化如下：

```
## 审查：[stage_name] — 第 [N] 轮

**决定：** 通过 / 修订 / 带警告通过

### 发现

1. [关键] 发现的标题
   - 描述：什么问题
   - 操作：如何修复
   - 状态：待处理 / 已修复 / 已接受 / 已推迟

2. [建议] 发现的标题
   - 描述：什么可以更好
   - 操作：如何改进
   - 状态：待处理 / 已接受 / 已推迟

### 总结
- 关键：N（已修复 N）
- 建议：N
- 挑刺：N
- Playbook 违规：N
- 成功标准达成：N/M
```

## 关键原则

1. **具体，不要模糊。** "钩子太弱"是无用的。"钩子问了一个问题但没有营造紧迫感——尝试用关键点 #2 中的惊人统计数据开头"是可操作的。

2. **关键就是关键。** 不要夸大严重性。缺少 schema 字段是关键。稍微啰嗦的段落是建议。逗号拼接是挑刺。

3. **最多两轮。** 目标是交付，不是完美。经过两轮修订后，带警告通过并继续。完美主义会扼杀流水线。

4. **审查工件，而非过程。** 你检查的是输出，而不是它是如何产生的。如果简报引人注目，agent 使用了非传统方法并不重要。

5. **Playbook 是法律。** 如果 playbook 说"屏幕上不超过 3 种颜色"，那不是建议——那是约束。违规一定要标记。

## 阶段特定审查指南

| 阶段 | 最重要的是什么 |
|-------|-----------------|
| research | 来源多样性、声明可验证性、视觉参考质量 |
| proposal | 交付承诺清晰度、渲染器系列和渲染运行时选择、音乐/语音方案、决策日志已启动 |
| idea | 钩子独特性、研究深度、角度多样性 |
| script | 时间准确性、叙事弧线、增强提示密度 |
| scene_plan | 全面覆盖、视觉多样性、资产可行性、幻灯片风险评分 |
| assets | 文件存在性、风格一致性、预算遵守 |
| edit | 时间线覆盖、音频同步、字幕存在、交付承诺合规 |
| compose | 可播放性、时长准确性、音频质量、合成前验证通过 |
| publish | SEO 质量、元数据完整性、导出打包 |

## 参考对齐审查

当存在 VideoAnalysisBrief（参考驱动制作）时，在**每个阶段**运行。

### 检查项：

1. **基础检查：** 输出是否引用了 VideoAnalysisBrief 中的具体发现，还是在凭空编造关于参考的内容？
   - 提案提到"快节奏"但参考的 pacing_style 是"慢速沉思"→ **关键**
   - 脚本声称参考有旁白但 VideoAnalysisBrief 显示无旁白 → **关键**

2. **差异化检查：** 每个概念/场景是否与参考有清晰的创意差异，还是复制品？
   - 提案是参考的完全复制（相同话题、相同结构、相同处理方式）→ **关键**
   - 每个概念中至少有一个元素必须与参考不同 → 如果较弱标记为**建议**
   - brief 中的创意差异化种子应在提案中体现

3. **承诺保留：** 用户说他们喜欢的参考元素在输出中是否仍然存在？
   - 用户说"我喜欢这个节奏"但 scene_plan 的场景时长是其 2 倍 → **建议**
   - 用户说"保留钩子风格"但脚本使用了不同的钩子 → **建议**

4. **成本对齐：** 成本估算仍然准确，还是范围已经扩大？
   - 如果实际支出超过估算 >30% 且未经用户重新批准 → **关键**
   - 如果在已批准的提案之外添加了新资产 → **建议**

### 严重性：
- 关于参考视频的事实错误：**关键**
- 无差异化的完全复制品：**关键**
- 差异化较弱（仅表面层面的变化）：**建议**
- 用户偏好未被尊重：**建议**
- 成本偏移 >30%：**关键**

## 幻灯片风险审查

在 **scene_plan** 和 **edit** 阶段运行。使用 `lib/slideshow_risk.py` 计算评分。

### 在 scene_plan 阶段：
1. 计算 `score_slideshow_risk(scenes, renderer_family=renderer_family)`
2. 如果判定为 **"fail"**（平均值 ≥ 4.0）：**关键** — 场景计划必须在继续前修订
3. 如果判定为 **"revise"**（平均值 ≥ 3.0）：**建议** — 标记评分 ≥ 3.5 的特定维度
4. 如果判定为 **"strong"** 或 **"acceptable"**：在审查总结中注明，无需发现项

### 在 edit 阶段：
1. 使用完整 edit_decisions 重新计算：`score_slideshow_risk(scenes, edit_decisions, renderer_family)`
2. 相同阈值适用——如果 edit 阶段使情况恶化（评分高于 scene_plan），标记出来

### 需要按维度标记的内容：
| 维度 | 当评分 ≥ 3.0 时该如何说 |
|-----------|------------------------------|
| repetition | "X 个场景使用相同的布局/景别——变化视觉语法" |
| decorative_visuals | "X 个场景没有说明目的（缺少 information_role 或 shot_intent）" |
| weak_motion | "相机运动存在但缺乏叙事理由" |
| weak_shot_intent | "X 个场景缺少 shot_intent——这个镜头为什么存在？" |
| typography_overreliance | "X% 的场景是文字/数据卡片——视频感觉像动画幻灯片" |
| unsupported_cinematic_claims | "声称电影级但缺少英雄时刻/灯光/运动" |

## 决策日志审查

在提案后的**每个阶段**运行。决策日志（`schemas/artifacts/decision_log.schema.json`）是累积的审计跟踪。

### 检查项：
1. **存在性**：检查点是否引用了 `decision_log_ref`？如果在提案阶段之后还没有，标记为**建议**。
2. **覆盖范围**：每个重大选择是否有条目？必须记录的关键决策：
   - 提供商选择（哪个图像/视频/音频工具及原因）
   - 风格/playbook 选择
   - 音乐曲目选择
   - 语音选择
   - 渲染器系列选择
   - 任何回退或降级（如动态→静态）
3. **质量**：每个决策应有：
   - 至少 2 个 `options_considered`（不仅仅是选中的那个）
   - 不是套话的 `reason`（"最佳选项"不是理由）
   - 正确的 `confidence`（0.0–1.0）——如果所有都是 1.0 则标记（不现实）
4. **用户可见性**：标记为 `user_visible: true` 的决策应该是用户真正关心的（不是内部路由）

### 严重性：
- 提案后缺少决策日志：**建议**（第一次），**关键**（如果到 edit 阶段仍缺失）
- 决策只考虑了 1 个选项：**建议**——"为可审计性记录被拒绝的备选方案"
- 所有决策置信度为 1.0：**建议**——"不现实的置信度——至少提供商选择涉及权衡"

## 创意差异化审查

在 **scene_plan** 和 **edit** 阶段运行。防止"每个视频看起来都一样"的失败模式。

### 检查项：
1. **变化检查**（仅 scene_plan）：使用 `lib/variation_checker.py` → `check_scene_variation(scenes)`。
   - 如果判定为 **"poor"**（评分 ≤ 2）：**关键** — "场景计划缺乏多样性：[列出违规项]"
   - 如果判定为 **"fair"**（评分 ≤ 3）：**建议** — 注明来自检查器的具体建议

2. **Playbook 对齐**：活动的 playbook 是否适合此内容？
   - 电影预告片使用"clean-professional"主题 → 标记不匹配
   - 教育解说视频使用"anime-ghibli"主题且未获用户要求 → 标记

3. **镜头语言完整性**（scene_plan）：
   - 每个场景应至少包含 `shot_size` 和 `shot_intent`
   - 英雄时刻应有完整的 shot_language（全部 6 个字段）
   - 将 shot_language 为空的场景标记为**建议**

4. **渲染器系列匹配**（edit 阶段）：
   - `edit_decisions` 中的 `renderer_family` 是否与提案设置的一致？
   - 如果在决策日志中没有记录原因就更改 → **关键**

5. **渲染运行时匹配**（edit 和 compose 阶段）：
   - `edit_decisions` 中的 `render_runtime` 必须与 proposal_packet.production_plan.render_runtime 匹配
   - 如果在决策日志中没有记录 `render_runtime_selection` 决策就更改 → **关键**
   - 在 compose 阶段，`final_review.checks.promise_preservation.runtime_swap_detected` 必须为 `false`。如果为 `true` 但没有经批准的 `render_runtime_selection` 决策 → **关键**
   - compose 时运行时不可用不是无声交换的借口——正确的做法是上报、获取批准、记录决策、然后运行。

6. **运行时选择呈现了两个选项**（提案阶段，强制要求）：
   - 查询 `video_compose.get_info()["render_engines"]`。如果 `remotion` 和 `hyperframes` 都显示 `True`，则 `decision_log` 中的 `render_runtime_selection` 决策的 `options_considered` **必须**包含两个运行时。
   - 当机器上两者都可用时，`render_runtime_selection` 的 `options_considered` 中只有一个运行时 → **关键**。agent 默默使用了默认值；用户没有被呈现备选方案。重新打开提案阶段并呈现两者。
   - 如果只有一个运行时可用，`options_considered` 仍然必须列出不可用的那个，并附带 `rejected_because: "runtime not available on this machine"`——否则审计跟踪会丢失选择是受限的而非自由的事实。
   - 根据 AGENT_GUIDE.md > "Present Both Composition Runtimes (HARD RULE)"：流水线建议的"默认"运行时**不是**跳过与用户对话的许可证。

## 交付承诺审查

在 **edit** 和 **compose** 阶段运行。使用 `lib/delivery_promise.py`。

### 在 edit 阶段：
1. 从 proposal packet 或 edit_decisions 元数据中提取交付承诺
2. 对已解析的剪辑列表运行 `promise.validate_cuts(cuts)`
3. 如果 `valid` 为 False：**关键** — "交付承诺违规：[违规项]"
4. 检查 `motion_ratio`：如果以动态为主的承诺的 motion 剪辑比例 < 50%，即使技术上有效也标记出来

### 在 compose 阶段：
1. `video_compose.py` 中的 `_pre_compose_validation()` 会自动强制执行此检查
2. 审查应验证该验证未被绕过（检查渲染报告中的警告）
3. 如果在以动态为主的承诺上尽管 motion 比例低但渲染成功，标记为**建议**

## 源素材理解审查

在 **research** 和 **proposal** 阶段运行，当存在用户提供的媒体文件时。

### 检查项：
1. **存在性**：如果用户提供的文件已提供给项目，是否存在 `source_media_review` 工件？
   - 如果用户媒体存在但没有 `source_media_review`：**关键** — "用户提供了媒体但 agent 在规划前没有检查它。在继续之前运行 `lib/source_media_review.review_source_media()`。"
2. **实际检查**：每个文件条目是否有 `reviewed: true` 和非空的 `technical_probe`？
   - 如果 `reviewed` 缺失或 `technical_probe` 为空：**关键** — "source_media_review 声称已审查但没有任何探测数据。文件实际上未被检查。"
3. **规划反映**：`planning_implications` 是否出现在提案的制作计划中？
   - 如果识别出了质量风险（如低分辨率、单声道音频）但提案未提及：**建议** — "源媒体存在提案未涉及的质量风险。"
4. **内容准确性**：计划是否依赖于源媒体实际不包含的内容？
   - 例如，计划假设有采访对话，但 transcript_summary 显示没有语音：**关键** — "计划假设有对话但源媒体不包含语音。"
5. **无幻觉内容**：agent 不得仅从文件名推断不支持的内容。如果 `content_summary` 说"采访素材"但探测只显示 3 秒无声视频，标记为**关键**。

### 严重性：
- 用户文件存在但缺少 `source_media_review`：提案阶段**关键**
- 未审查的文件（无探测）：**关键**
- 计划未反映质量风险：**建议**
- 计划假设源中没有的内容：**关键**

## 最终自我审查审查

在 **compose** 和 **publish** 阶段运行。确保 agent 审查了实际渲染输出。

### 在 compose 阶段：
1. **存在性**：`render_report` 旁边是否存在 `final_review` 工件？
   - 如果缺失：**关键** — "Compose 产生了 render_report 但没有 final_review。agent 在呈现之前必须检查渲染输出。"
2. **状态检查**：`final_review.status` 是什么？
   - `pass` → 正常，继续
   - `revise` → agent 在呈现前应已修复问题。如果流水线仍然继续了：**关键** — "自我审查发现值得修订的问题但 agent 仍然呈现了。"
   - `fail` → 流水线**不得**继续。如果继续了：**关键**
3. **检查完整性**：所有 5 个必要检查必须有数据：
   - `technical_probe` 必须显示有效的容器和合理的时长/分辨率
   - `visual_spotcheck` 必须有 `frames_sampled >= 4`
   - `audio_spotcheck` 必须报告旁白/音乐存在性
   - `promise_preservation` 必须确认 `delivery_promise_honored`
   - `subtitle_check` 必须报告存在/缺失
   - 任何数据缺失的检查：**建议** — "自我审查检查 [X] 数据不完整"
4. **承诺保留**：如果 `promise_preservation.silent_downgrade_detected` 为 true：**关键** — "自我审查检测到从动态主导无声降级到静态主导。"

### 在 publish 阶段：
1. 验证 `final_review` 已作为必需工件传递
2. 如果 `final_review.status` 不是 `pass`：**关键** — "自我审查未通过，无法发布"
3. 如果 `final_review.issues_found` 非空且 `recommended_action` 不是 `present_to_user`：**建议** — "自我审查发现问题；在发布前验证它们已解决"

## 合成创作模式审查

模板化→工作室反转（`AGENT_GUIDE.md` → "Composition Authoring Mode" + `skills/meta/bespoke-composition.md`）是治理规则，而非建议。审查者是执法点：没有这些检查，下一个 agent 会悄悄回到默认的剪辑 schema，每个视频又开始看起来一样。

### 在提案阶段：
1. `decision_log` 必须包含一个 `composition_mode` 决策，`options_considered: ["templated","atelier"]` 和一个带有与需求简报相关的真实理由的 `selected` 值。
   - 完全缺少 `composition_mode` 决策：**关键** — "提案缺少 composition_mode 选择。Atelier 与 templated 是强制呈现的决策（见 AGENT_GUIDE.md → Composition Authoring Mode）。"
   - 决策记录只考虑了一个选项：**关键** — "composition_mode 决策在未同时呈现 templated 和 atelier 备选方案的情况下被记录。"
2. 对于**英雄作品**（需求简报标记为营销/发布/品牌/有质量要求的解说/任何单个交付物且质量是重点），其中 `selected == "templated"`：**关键** — "英雄需求锁定了 composition_mode='templated'。根据原则默认是 atelier；templated 需要在 `decision_log.<entry>.reason` 中有明确理由（例如本地化变体、批量处理、限时草稿）。"仅在理由字段指定了允许的例外时才抑制。
3. 如果 `composition_mode == "atelier"` 且 `proposal_packet` 缺少 `art_direction` 声明（调色板、字体、动态、签名装置）：**关键** — "Atelier 提案缺少艺术指导承诺。根据 `skills/meta/bespoke-composition.md` 第 1 步，在编写场景之前必须*书面记录*艺术指导。"

### 在 scene_plan / edit 阶段（`composition_mode == "atelier"` 时）：
1. `edit_decisions.composition_mode` 必须等于 `"atelier"`，且 `edit_decisions.bespoke.{entry, composition_id, art_direction}` 必须全部设置。
   - 缺少 `entry`/`composition_id` 中的任何一个：**关键** — "Atelier compose 合约不完整；渲染将被 `_render_via_atelier` 拒绝。"
   - 缺少 `art_direction`：**关键** — "Atelier 没有艺术指导声明；审查者无法评估独特性。"
2. `edit_decisions.cuts` 中任何出现库存 `cut.type` 场景类型（`text_card`、`stat_card`、`bar_chart`、`kpi_grid`、`callout`、`comparison`、`hero_title`、`terminal_scene`、`anime_scene`、`progress_bar`、`pie_chart`、`line_chart`）：**关键** — "Atelier 作品使用了库存 cut.type {name}。手动编写场景；库存注册表是机制代码库，不是零件箱（`skills/meta/bespoke-composition.md`）。"

### 在 compose 阶段（`composition_mode == "atelier"` 时）：
1. compose 阶段的 `final_review.checks.atelier` 块必须存在。如果缺失：**关键** — "Atelier 渲染跳过了原则检查——`_render_via_atelier` 返回时没有 `atelier` 检查；调查工具接线。"
2. 如果 `final_review.checks.atelier.stock_reuse_detected == true`：**关键** — "在定制项目内发现库存注册表导入（{offending_imports[0].file} → {offending_imports[0].import}）。手动编写场景；不要从库存 src/ 导入。"
3. 如果 `final_review.checks.atelier.art_direction_declared == false`：**关键** — "Atelier 渲染没有艺术指导声明。在重新渲染之前设置 `edit_decisions.bespoke.art_direction`。"
4. **场景独特性——无英雄组件脊柱（强制记录）。** 每个场景采样一个代表性帧（例如每个 `props.sections[i]` 的中间窗口），并在审查记录中回答：
   - *每个场景是否有不同的主要视觉主体？* 如果两个或更多场景共享其主要视觉内容（相同的英雄元素仅重新标注——从未离开的蜡烛、每个节拍中的浏览器框架、作为支架的评分环）：**关键** — "检测到英雄组件脊柱：场景 {ids} 共享主要视觉主体。根据 `skills/meta/bespoke-composition.md` 第 1.5 步，每个场景必须赢得自己的构图；签名装置属于一个高潮节拍，而非作为支架。重新规划受影响的场景。"
   - *`art_direction` 中命名的签名装置是否至少在一个节拍中出现？*（否 ⇒ 关键，重新创作或更新声明以匹配实际构建的内容）
   - *签名装置是否出现在**大多数**节拍中？*（是 ⇒ 关键——参见上面的英雄组件脊柱；签名应该稀缺）
   此检查不能默默跳过；缺少逐场景清单记录本身即**关键**（"scene_distinctness inventory not recorded"）。
5. **字幕/屏幕文字去重（强制检查）。** 将活动字幕文本与同一时间窗口中渲染的任何屏幕文字进行比较：
   - 如果它们是相同的内容（字幕重复了旁白正在朗读的场景标题/标题）：**关键** — "字幕在 {t}s 处重复屏幕文字（'{text}'）。每个作品决定一次，字幕是增加意义（数字、名字、翻译）还是辅助功能字幕；不要对同一行同时做两者。要么清除这些场景的 `captions=[]`，要么删除冗余的屏幕 SerifLine。"
6. **独特性审查（人工判断，强制）。** 在批准渲染之前，审查者必须在审查记录中明确回答：
   - *"这个视频可能是任何其他产品的视频吗？"*（是 ⇒ 关键，重新创作艺术指导）
   - *"它的视觉语言是否重复了我以前作品的外观？"*（是 ⇒ 关键，重新创作）
   独特性是品味判断领域，工具无法自动化；审查者在此问题上的缺席本身即**关键**发现（"distinctness review not recorded"）。

### 在 publish 阶段（`composition_mode == "atelier"` 时）：
1. 上述所有六个 atelier compose 阶段检查（`atelier` 块的存在性、stock_reuse、art_direction_declared、scene_distinctness、字幕/文字去重、人工独特性审查）必须在审查记录中显示 `resolved`。任何未解决：**关键** — "无法在未解决的原则或独特性发现的情况下发布 atelier 作品。"
