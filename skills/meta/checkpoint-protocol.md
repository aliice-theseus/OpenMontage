# 检查点协议 — 元技能

## 何时使用

在完成阶段工作并通过审查之后。本技能教你何时以及如何设置检查点，以及何时请求人工批准。它用指令驱动的协议取代了 Python 的 `checkpoint_policy.py`。

检查点是流水线的保存点。它们支持故障恢复、人工监督和审计跟踪。

## 协议

### 第 1 步：检查清单策略

从流水线清单中读取当前阶段的配置：

```yaml
- name: idea
  checkpoint_required: true      # 必须设置检查点？
  human_approval_default: true   # 必须请求人工批准？
```

| `checkpoint_required` | `human_approval_default` | 操作 |
|----------------------|------------------------|--------|
| true | true | 设置检查点 + 呈现给人工审批 |
| true | false | 设置检查点 + 自动继续 |
| false | * | 完全跳过检查点（罕见） |

### 第 2 步：准备检查点数据

收集检查点所需的一切：

1. **阶段名称** — 刚刚完成的是哪个阶段
2. **状态** — `"completed"`（或如果需要批准则为 `"awaiting_human"`）
3. **工件** — 该阶段产生的规范工件
4. **元数据** — 审查发现、成本快照、时间信息

### 第 3 步：写入检查点

调用检查点工具：

```python
write_checkpoint(
    pipeline_dir,      # 项目工作目录
    project_name,      # 项目标识符
    stage_name,        # 例如 "idea"
    status,            # "completed" 或 "awaiting_human"
    artifacts,         # {"brief": {...}} — 阶段的输出
)
```

检查点工具将：
- 对照 schema 验证工件
- 将检查点 JSON 写入磁盘
- 包含时间戳和阶段元数据

### 第 4 步：阶段内检查点（恢复支持）

长时间运行的阶段（如 `assets` 或 `compose` 循环）可能因 API 错误、速率限制或会话中断而在中途失败。为了支持从确切的故障点（例如场景 4）恢复：

1. **写入部分进度**：每次成功生成一个重大项目（例如一个场景的资产、一个剪辑）时，写入一个 `in_progress` 检查点。

   `in_progress` 检查点可以省略阶段的规范工件，但任何以已知工件名称存储的工件仍会通过 schema 验证。如果部分数据还不是有效的规范工件，将其存储在 `metadata.partial_progress` 而非 `artifacts` 中。
   ```python
   write_checkpoint(
       pipeline_dir, project_name,
       stage="assets",
       status="in_progress",
       artifacts={},  # 尚无完整的规范工件
       metadata={
           "partial_progress": {
               "asset_manifest_draft": partial_manifest_dict,
               "completed_scene_ids": completed_scene_ids,
           }
       },
   )
   ```
   如果部分工件已经满足其 schema（例如，带有 `version: "1.0"` 和有效的 `assets[]` 条目的 `asset_manifest`），可以直接存储在 `artifacts` 中。
2. **从部分进度恢复**：在启动一个阶段时，**始终**检查是否存在 `in_progress` 检查点。参见第 7 步（恢复协议）了解如何处理。

### 第 5 步：人工审批（如需要）

当 `human_approval_default: true` 时：

1. **向人工呈现摘要**：
   ```
   ## 阶段完成：[stage_name]

   ### 工件摘要
   [工件的关键细节——标题、时长、关键决策]

   ### 审查发现
   [审查者摘要：N 个关键（全部已修复）、N 个建议]

   ### 截至目前成本
   [已花费预算 / 总计，按工具分解]

   ### 需要操作
   请审查并批准以继续，或提供反馈进行修订。
   ```

2. **等待人工响应：**
   - **已批准** → 将检查点状态更新为 `"completed"`，继续下一阶段
   - **请求修订** → 带着人工的反馈返回阶段指导技能，生成修订后的工件，重新审查，重新设置检查点
   - **中止** → 停止流水线

3. **审批阶段**（哪些阶段通常需要人工审批）：
   - `idea` — 始终。创意方向决定了下游的一切。
   - `script` — 始终。文字是基础。
   - `scene_plan` — 通常。视觉选择是主观的。
   - `assets` — 很少。自动化质量检查就足够了。
   - `edit` — 很少。技术性组装，非创意性。
   - `compose` — 很少。但人工可能想预览。
   - `publish` — 始终。任何内容公开发布前必须经人工批准。

### 第 6 步：确定下一阶段

检查点写入和批准（如果需要）后：

```python
next_stage = get_next_stage(pipeline_dir, project_name)
```

这会读取所有现有检查点，并返回需要运行的下一个阶段，如果流水线完成则返回 `None`。

### 第 7 步：恢复协议

在任何流水线运行**开始**时（不仅仅是在阶段之后），始终检查现有进度：

```python
next_stage = get_next_stage(pipeline_dir, project_name)
```

如果 `next_stage` 不是第一阶段：
1. 告知人工："发现现有进度。从阶段 [next_stage] 继续。"
2. **检查部分进度**：读取 `next_stage` 的检查点：
   ```python
   current_cp = read_checkpoint(pipeline_dir, project_name, next_stage)
   ```
   如果 `current_cp` 存在且其状态为 `"in_progress"`，告知人工你正在从阶段中间恢复。
3. **加载工件**：从检查点加载先前的工件作为上下文。如果从 `"in_progress"` 恢复，首先从 `current_cp["artifacts"]` 加载任何通过 schema 验证的部分工件。如果部分数据存储在 `current_cp["metadata"]["partial_progress"]` 中，使用该草稿数据及其完成标记（如 `completed_scene_ids`）跳过已经完成的子任务。
4. **继续**：从下一个成功步骤继续生成，追加到部分工件。

如果存在状态为 `"awaiting_human"` 的检查点：
1. 告知人工："阶段 [name] 正在等待你的审批"
2. 呈现检查点数据供审查
3. 等待批准后再继续

### 样本检查点（参考驱动制作）

当制作是参考驱动的（VideoAnalysisBrief 存在时），在提案批准和完整制作之间有一个额外的检查点：

| 阶段 | checkpoint_required | human_approval_default | 说明 |
|-------|--------------------|-----------------------|-------|
| `sample` | true | true | 始终需要人工审批 |

样本检查点：
1. 呈现：渲染的样本剪辑（10-15 秒）
2. 成本：样本成本 vs. 预估完整视频成本
3. 操作：批准（→ 继续到脚本）、修订（→ 重新生成样本）、中止

样本检查点不是流水线阶段——它是提案阶段内的子检查点。它不产生规范工件。它产生一个存储在 `projects/<name>/assets/sample/sample_v{N}.mp4` 的渲染预览剪辑。

**呈现格式：**
```
## 样本预览就绪

**样本剪辑：** [sample_v1.mp4 的路径]
- 时长：[X] 秒（钩子 + 1 个中间场景）
- 语音：[TTS 提供商 + 语音名称]
- 视觉：[描述——AI 图像、Remotion 动画等]
- 音乐：[来源]

**样本成本：** $[X.XX]
**预估完整视频成本：** $[X.XX]

感觉对吗？我可以调整：语音、视觉风格、节奏、音乐、颜色。
```

## 关键原则

1. **始终对已完成的工作设置检查点。** 即使 `checkpoint_required: false`，如果阶段花费了显著的时间或成本，也考虑设置检查点。丢失工作比多一个磁盘上的文件更糟糕。

2. **在创意阶段永远不要跳过人工审批。** `idea` 和 `script` 塑造一切。为了节省时间而跳过它们会产生没人想看的视频。

3. **包含成本快照。** 在批准成本高昂的下游阶段（assets、compose）之前，人工应该知道已经花了多少以及还剩多少。

4. **检查点支持恢复。** 如果流水线在 `compose` 阶段崩溃，人工可以重新启动并从 `compose` 继续——而不是从 `idea`。这就是其全部意义所在。

5. **在审批请求中保持透明。** 不要只展示工件——还要展示审查发现、成本和任何问题。帮助人工做出明智的决定。
