# 角色设计导演 — 电影化流水线

## 适用场景

你是**角色设计导演**。你在 `scene_plan` 完成之后、`scene_sketch` 之前工作。
当电影化剧本中出现人物角色时，你需要为**每个角色生成四视图概念设计**，
产出**角色身份锁定包**，提交用户确认后方可进入下一阶段。

**这是强制阶段。** 当 `scene_plan` 分析出有人物主角时，此阶段不可跳过。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/character_design.schema.json` | 产物验证 |
| 前置产物 | `scene_plan` | 提取角色列表和描述 |
| 可选 | 上一项目的 `character_registry.json` | 复用已有角色身份 |
| 工具 | `character_ref_sheet`（内部使用 `image_selector`） | 分步生成并拼接四视图 |
| 第 3 层技能 | `.agents/skills/flux-character-turnaround/SKILL.md` | FLUX.2 Dev 四视图生成契约 |

## 流程

### 步骤 1：从 scene_plan 提取角色

```python
scene_plan = state.artifacts["scene_plan"]
characters = extract_characters(scene_plan)
```

如果没有角色或角色只是背景路人，跳过此阶段，标记 `has_characters: false`。

如果有主角角色（`role: protagonist`），标记 `has_characters: true`，继续。

### 步骤 1b：检查角色身份注册表

```python
from lib.character_registry import CharacterRegistry

registry = CharacterRegistry(Path(f"projects/{project_id}"))
if registry.has("hero"):
    # 复用已有角色，跳过生成
    existing = registry.get("hero")
```

### 步骤 2：为每个角色生成角色形象图

（同解说片流程 — 参见 `skills/pipelines/explainer/character-design-director.md` 步骤 2。
同样要求：同一画布下，左侧三视全身 + 右侧上半身正面特写，
纯白背景、禁止文字、禁止道具、极度写实、拒绝陶瓷肌。）

执行前必须读取 `.agents/skills/flux-character-turnaround/SKILL.md` 和其提示模板，
并调用 `character_ref_sheet`，固定使用本地 `black-forest-labs/FLUX.2-dev`。先用 `operation="front_only"` 生成正面 T2I 并等待确认，批准后用 `operation="complete_from_front"` 和该正面图生成侧面/背面/半身、最后本地拼接；不得让模型一次生成四栏。只有用户明确批准跳过正面检查时才使用 `operation="full"`。模型缺失时请求下载确认，不得静默换模型。

### 步骤 3：构建角色身份锁定包

（同解说片流程 — 参见 `skills/pipelines/explainer/character-design-director.md` 步骤 3。
`seed_image_path` 指向组合图路径。）

### 步骤 4：写入注册表

（同解说片流程 — 参见 `skills/pipelines/explainer/character-design-director.md` 步骤 4）

### 步骤 5：展示给用户并等待确认

电影化角色设计展示风格应匹配电影化基调。使用电影化的展示语言：

```
=== 角色设计确认 ===

角色 1: 剑客
  [角色形象组合图 — 左侧三视全身 + 右侧上半身特写]
  角色类型: 主角
  风格: 极致写实, 电影化古装

角色 2: 黑暗领主
  [角色形象组合图 — 左侧三视全身 + 右侧上半身特写]
  角色类型: 反派
  风格: 极致写实, 哥特黑暗

请确认:
  [A] 全部批准 → 进入场景草图
  [R] 需要修改
  [X] 拒绝
```

### 步骤 6：写入检查点

```python
write_checkpoint(
    pipeline_dir=...,
    project_id=...,
    stage="character_design",
    status="completed",
    artifacts={"character_design": character_design},
    pipeline_type="cinematic",
    human_approval_required=True,
    human_approved=(approval == "approved"),
)
```

## 验证清单

- [ ] 每张图为同一画布：左侧三视全身 + 右侧上半身正面特写
- [ ] **纯白色背景** — 无场景装饰
- [ ] **人物比例协调**
- [ ] **禁止文字** — 无任何文字
- [ ] **禁止道具**
- [ ] **极度写实** — 照片级，不美化
- [ ] **拒绝陶瓷肌** — 皮肤有真实质感
- [ ] **面部同一** — 全部视图使用同一个面部设计
- [ ] **发型一致** — 全部视图发型（发色、发长、刘海等）完全统一
- [ ] **着装一致** — 全部视图服装配色完全统一
- [ ] **视角绝对正对** — 正面正对镜头、侧面 90° 正侧面、背面正对背面、上半身特写也是正对镜头
- [ ] `identity_lock` 已配置
- [ ] 角色已写入 `character_registry.json`
- [ ] `approval.status` 为 `"approved"`
