# 场景草图导演 — 解说片流水线

## 适用场景

你是**场景草图导演**。你在 `scene_plan` 完成之后、`assets` 之前工作。
你的工作是为 `scene_plan` 中的每一个场景生成**构图草图**，
让用户在投入资产生成前确认镜头设计和色调。

**这是强制阶段。** 每个场景都需要有一张草图，用户确认后方可进入 assets。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/scene_sketch.schema.json` | 产物验证 |
| 前置产物 | `scene_plan` | 场景列表和镜头语言 |
| 工具 | `image_selector` | 生成草图 |

## 流程

### 步骤 1：加载场景列表

```python
scene_plan = state.artifacts["scene_plan"]
scenes = scene_plan["scenes"]
```

### 步骤 2：为每个场景生成草图

对每个场景，使用 `image_selector` 生成草图。

```python
for scene in scenes:
    # 构建提示词（纯场景，不包含角色）
    sketch_prompt = build_sketch_prompt(scene)
    
    result = image_selector.execute({
        "prompt": sketch_prompt,
        "operation": "text_to_image",
        "aspect_ratio": "16:9",
    })
```

**草图要求：**
- 宽高比与最终视频一致（默认 16:9）
- 聚焦场景搭建：背景环境、空间布局、构图方式
- 体现场景的色调和氛围
- **不包含角色** — 草图只呈现场景本身，角色由后续资产阶段处理

**提示词结构参考：**
```
场景构图草图, 纯场景, {scene_description},
镜头: {shot_language},
色调: {color_palette},
无角色, 仅有场景和空间, 电影级构图, 简要渲染
```

### 步骤 3：整理产物

```python
scene_sketch = {
    "version": "1.0",
    "scenes": [
        {
            "scene_id": scene["id"],
            "description": scene["description"],
            "image_path": image_path,
            "shot_language": scene.get("shot_language"),
            "prompt": prompt,
            "source_tool": "image_selector",
            "cost_usd": 0.02,
        }
        for scene in scenes
    ],
    "approval": {"status": "pending", "reviewed_at": ""},
}
```

### 步骤 4：展示给用户并等待确认

向用户呈现所有场景草图：

```
=== 场景草图确认 ===

场景 1: <场景标题>
  [草图预览]
  镜头: <景别>, <运镜方式>
  色调: <色调描述>
  费用: $0.02

场景 2: <场景标题>
  [草图预览]
  镜头: <景别>, <运镜方式>
  色调: <色调描述>
  费用: $0.02

...

总成本: $0.XX

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
    pipeline_type="animated-explainer",
    human_approval_required=True,
    human_approved=(approval == "approved"),
)
```

## 与资产阶段的衔接

scene_sketch 产物中的草图将在 `assets` 阶段作为构图参考传入视频生成工具：

```python
# 在 assets 阶段调用 video_selector 时:
video_selector.execute({
    "prompt": scene_prompt,
    "operation": "text_to_video",
    "operation_type": "text_to_video",
    "reference_image_urls": [
        # 场景构图参考（来自 scene_sketch）
        scene_sketch["scenes"][i]["image_path"],
    ],
})
```

## 验证清单

- [ ] 每个 scene_plan 中的场景都有一张草图
- [ ] 草图宽高比与最终视频一致
- [ ] 草图体现了场景的镜头语言和色调
- [ ] 草图中不包含角色，仅为纯场景搭建
- [ ] 所有图片文件存在
- [ ] `approval.status` 为 `"approved"`
