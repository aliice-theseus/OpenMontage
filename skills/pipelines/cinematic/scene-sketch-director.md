# 场景草图导演 — 电影化流水线

## 适用场景

你是**场景草图导演**。你在 `scene_plan` 完成之后、`assets` 之前工作。
你的工作是为 `scene_plan` 中的每一个场景生成**构图草图**，
让用户在投入资产生成前确认镜头设计和色调。

**这是强制阶段，不得跳过。** 即使 `scene_plan` 已完成、角色四视图已就绪，`scene_sketch` 也必须执行。`assets` 阶段依赖 `scene_sketch` 产物作为构图参考，跳过此阶段会导致资产生成缺少镜头构图指引。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/scene_sketch.schema.json` | 产物验证 |
| 前置产物 | `scene_plan` | 场景列表和镜头语言 |
| 工具 | `image_selector` | 生成草图 |

## 流程

（同解说片流程 — 参见 `skills/pipelines/explainer/scene-sketch-director.md` 步骤 1-3，使用 `pipeline_type="cinematic"`）

### 步骤 4：展示给用户并等待确认

```
=== 场景草图确认 ===

场景 1: 竹林追逐
  [草图预览]
  镜头: 斯坦尼康跟拍
  色调: 冷色, 高对比度

场景 2: 悬崖决斗
  [草图预览]
  镜头: 远景, 推轨
  色调: 黄昏, 暖色背景光

请确认:
  [A] 全部批准 → 进入素材生成
  [R] 需要修改
  [X] 拒绝
```

### 步骤 5：写入检查点

```python
write_checkpoint(
    pipeline_dir=...,
    project_id=...,
    stage="scene_sketch",
    status="completed",
    artifacts={"scene_sketch": scene_sketch},
    pipeline_type="cinematic",
    human_approval_required=True,
    human_approved=(approval == "approved"),
)
```

## 验证清单

- [ ] 每个 scene_plan 中的场景都有一张草图
- [ ] 草图宽高比与最终视频一致
- [ ] 草图中不包含角色，仅为纯场景搭建
- [ ] `approval.status` 为 `"approved"`
