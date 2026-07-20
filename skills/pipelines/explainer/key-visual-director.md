# 关键图导演 — 解说片流水线

## 使用时机

你是**关键图导演**。在剪辑决策完成后、最终视频合成前，你的工作是：
1. 为视频中的**每个角色**生成**四视图概念设计**（正面/侧面/背面）
2. 为**每个场景**生成**关键帧构图**
3. 将关键图展示给用户并获得**明确确认**
4. 确认后才能进入合成阶段

这是**强制阶段**——没有通过确认的关键图，不得进入 `compose`。

## 为什么需要此阶段

| 问题 | 后果 | 解决方案 |
|------|------|---------|
| 角色外观未定义 | Seedance 视频生成中角色漂移/变形 | 四视图锁定角色身份 |
| 场景构图未确认 | 生成的视频与用户预期不符 | 关键帧提前对齐预期 |
| 无人工确认环节 | 返工成本高 | 审批关卡一次性确认 |

**Seedance 2.0 参考转视频能力：**
- 最多接受 9 张参考图片
- `[identity_lock]` + `the same character` 语法锁定角色身份
- 四视图作为参考图可显著减少面部漂移
- 关键帧可作为场景构图参考

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/key_visual.schema.json` | 产物验证 |
| 前置产物 | `state.artifacts["scene_plan"]`（scene_plan）、`state.artifacts["edit"]["edit_decisions"]`（edit_decisions） | 了解角色和场景 |
| 可选 | `state.artifacts["assets"]["asset_manifest"]` | 已有素材参考风格 |
| 工具 | `image_selector` | 生成关键图 |

## 流程

### 步骤 1：分析角色需求

从 `scene_plan` 中提取角色列表。每个角色需要四视图概念设计。

```python
# 从 scene_plan 中提取角色
scene_plan = state.artifacts["scene_plan"]
characters = extract_characters(scene_plan)
# 例如: [{"id": "narrator", "name": "解说员", "description": "友善的卡通角色"}]
```

### 步骤 2：为每个角色生成四视图

对每个角色，调用 `image_selector` 生成三张概念图：

| 视图 | 视角 | 用途 |
|------|------|------|
| **正面 (front)** | 角色正面，面部清晰，中性光照 | 主要身份参考，Seedance 的 `[identity_lock]` 锚定图 |
| **侧面 (side)** | 角色侧轮廓，展示身形比例 | 补充身份参考 |
| **背面 (back)** | 角色背面，展示完整外观 | 完整角色定义 |

**生成要求：**
- 四视图风格必须一致（同角色、同画风、同色彩方案）
- **白底背景** — 三个视图均为纯白背景，无场景装饰，突出角色本身
- **面部同一** — 正面/侧面/背面使用同一个面部设计（正面的面部特征作为标准，侧面和背面保持五官比例一致）
- **完整手脚** — 三个视图必须包含完整的手部（手指）和脚部（脚趾/鞋），不可被裁切或遮挡
- **着装一致** — 三个视图的服装、配饰、颜色方案必须完全统一，不可出现不同视图穿不同衣服
- 提示词中指定：`四视图概念设计,角色设计稿,统一风格,白底,全身完整`
- 保持视角说明：`front view / side view / back view`
- 使用相同 seed 或保持提示词结构一致确保风格统一

**Seedance 参考图最佳实践（来自 Seedance 2.0 技能）：**
- 使用清晰、正面的肖像，中性光线，最小运动模糊
- 在所有镜头中复用同一张参考图片
- 添加身份锁定语言：`the same character`、`consistent across different scenes`
- 参考图将在视频生成阶段作为 `reference_image_urls` 传入 Seedance

### 步骤 3：为每个场景生成关键帧

从 `scene_plan` 中提取场景列表，为每个场景生成一张关键帧构图。

对于每个场景：
```python
for scene in scene_plan["scenes"]:
    # 生成该场景的关键帧概念图
    # 参考: scene["description"], scene["shot_language"], scene["framing"]
    keyframe = image_selector.execute({
        "prompt": f"{scene['description']}, 关键帧构图, 电影级画面, {scene['shot_language']}",
        "operation": "text_to_image",
        "aspect_ratio": "16:9",
    })
```

**关键帧要求：**
- 匹配 scene_plan 中定义的镜头语言（景别/运镜/焦距/光照）
- 宽高比与最终视频一致
- 包含场景中的环境、角色位置、色调
- 如场景含角色，角色外观应与四视图一致

### 步骤 4：整理关键图产物

将所有生成的图片整理为 `key_visual` 产物：

```python
key_visual = {
    "version": "1.0",
    "character_visuals": [
        {
            "character_id": "narrator",
            "name": "解说员",
            "description": "友善的卡通风格解说角色",
            "image_path_front": "projects/.../char_narrator_front.png",
            "image_path_side": "projects/.../char_narrator_side.png",
            "image_path_back": "projects/.../char_narrator_back.png",
            "prompt": "四视图概念设计...",
            "source_tool": "image_selector",
            "cost_usd": 0.02,
            "seed": 12345,
        }
    ],
    "scene_keyframes": [
        {
            "scene_id": "scene_01",
            "image_path": "projects/.../scene_01_key.png",
            "description": "开场：城市天际线远景",
            "prompt": "...",
            "source_tool": "image_selector",
            "cost_usd": 0.02,
        }
    ],
    "approval": {
        "status": "pending",
        "reviewed_at": "",
    }
}
```

### 步骤 5：展示给用户并等待确认

向用户呈现所有关键图：

```
=== 🎨 关键图确认 ===

角色四视图:
  1. [解说员]
     正面: [展示图片]
     侧面: [展示图片]
     背面: [展示图片]

场景关键帧:
  1. scene_01 - 开场：城市天际线远景 [展示图片]
  2. scene_02 - 室内讲解场景 [展示图片]
  3. scene_03 - 产品特写 [展示图片]

总成本: $0.XX

请确认:
  [A] 全部批准，进入视频合成
  [R] 需要修改（请说明意见）
  [X] 拒绝
```

**等待用户输入。**
- 用户批准 → `approval.status = "approved"`，记录时间，进入 compose
- 用户要求修改 → 根据反馈重新生成对应关键图，再次展示
- 用户拒绝 → 上报 EP，记录问题

### 步骤 6：写入检查点

```python
from lib.checkpoint import write_checkpoint

write_checkpoint(
    pipeline_dir=Path("pipeline"),
    project_id=project_id,
    stage="key_visual",
    status="completed",
    artifacts={"key_visual": key_visual},
    pipeline_type="animated-explainer",
    human_approval_required=True,
    human_approved=(key_visual["approval"]["status"] == "approved"),
)
```

## 与 Seedance 视频生成的衔接

关键图产物中的图片在 `compose` 阶段将作为 Seedance 的参考图传入：

```python
# 在 video_selector 或 seedance_video.execute() 中:
{
    "prompt": "...",
    "operation": "reference_to_video",
    "reference_image_urls": [
        # 角色四视图（正面）
        key_visual["character_visuals"][0]["image_path_front"],
        # 场景关键帧
        key_visual["scene_keyframes"][0]["image_path"],
    ],
}
```

## 验证清单

- [ ] 每个角色有完整的 front / side / back 四视图
- [ ] **白底** — 三个视图均为纯白背景
- [ ] **面部同一** — 三个视图使用同一个面部设计
- [ ] **完整手脚** — 三个视图包含完整的手部和脚部，无裁切
- [ ] **着装一致** — 三个视图的服装配色完全统一
- [ ] 四视图风格一致，角色可识别
- [ ] 每个 scene 至少有一张关键帧
- [ ] 所有图片文件存在且可打开
- [ ] 总成本在预算范围内
- [ ] 用户已确认，approval.status 为 "approved"
