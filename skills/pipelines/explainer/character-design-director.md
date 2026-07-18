# 角色设计导演 — 解说片流水线

## 适用场景

你是**角色设计导演**。你在 `scene_plan` 完成之后、`scene_sketch` 之前工作。
当剧本中出现人物角色（尤其是主角）时，你需要为**每个角色生成三视图概念设计**，
产出**角色身份锁定包**，提交用户确认后方可进入下一阶段。

**这是强制阶段。** 当 `scene_plan` 分析出有人物主角时，此阶段不可跳过。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/character_design.schema.json` | 产物验证 |
| 前置产物 | `scene_plan` | 提取角色列表和描述 |
| 可选 | 上一项目的 `character_registry.json` | 复用已有角色身份 |
| 工具 | `image_selector` | 生成三视图 |
| 第 3 层技能 | `.agents/skills/flux-character-turnaround/SKILL.md` | FLUX.1 Dev 四视图提示模板、变量和验收规则 |

## 流程

### 步骤 1：从 scene_plan 提取角色

```python
scene_plan = state.artifacts["scene_plan"]
characters = extract_characters(scene_plan)
# 例如: [{"id": "hero", "name": "剑客", "description": "黑衣侠客"}]
```

如果没有角色或角色只是背景路人，跳过此阶段，标记 `has_characters: false`，
直接进入 `scene_sketch` 阶段。

如果有主角角色（`role: protagonist`），标记 `has_characters: true`，继续。

### 步骤 1b：检查角色身份注册表

在生成新角色前，先检查本项目是否存在 `character_registry.json`：

```python
from lib.character_registry import CharacterRegistry

registry = CharacterRegistry(Path(f"projects/{project_id}"))
if registry.has("hero"):
    # 复用已有角色，跳过生成
    print(f"角色 hero 已存在，复用注册身份")
    existing = registry.get("hero")
    # 将 registry 中的信息注入 character_design 产物
```

如果角色已注册，直接复用身份锁，无需重新生成三视图。
如果角色需要更新（例如新剧情需要不同服装），正常生成并更新注册表。

### 步骤 2：为每个角色生成角色形象图

生成前必须完整读取 `.agents/skills/flux-character-turnaround/SKILL.md` 及其引用的
`references/prompt-template.json`，按该技能组合变量与提示词。此角色建模参考场景固定使用
`image_selector → local_diffusion → black-forest-labs/FLUX.1-dev`；不得改用通用 schnell 默认。

对每个角色，调用 `image_selector` 生成一张组合图，包含：

| 区域 | 内容 | 用途 |
|------|------|------|
| **画面左侧** | 三视全身图（正面、侧面、背面并排） | 完整角色定义，Seedance identity_lock 锚定图 |
| **画面右侧** | 上半身正面视角特写图 | 面部细节参考 |

**画面布局：**
- 同一画布横向四栏：正面全身约 22%、90° 侧面全身约 22%、背面全身约 22%、胸部以上特写约 34%
- 默认画布为 **16:9（1344×768）**；用户可按技能支持的比例覆盖

**生成要求（硬性）：**
- **纯白色背景** — 整张画布均为纯白背景，无任何场景装饰
- **人物比例协调** — 全身与半身的人物比例保持统一
- **禁止出现任何文字** — 画面中不得有任何标题、标签、说明文字
- **禁止出现道具** — 角色不持有或佩戴任何道具，只有服装本身
- **极度写实** — 照片级写实风格，拒绝卡通、二次元、插画风
- **不美化** — 保留真实皮肤纹理、毛孔、皱纹、瑕疵，拒绝过度美化/磨皮
- **皮肤有质感，拒绝陶瓷肌** — 皮肤应呈现真实质感，而非光滑陶瓷效果
- **面部同一** — 三视全身图和上半身特写必须使用同一个面部设计
- **发型一致** — 全部视图的发型（包括发色、发长、刘海、发髻等）必须完全统一
- **着装一致** — 所有视图的服装配色完全统一
- **视角必须绝对正对** — 正面必须是正对镜头（不能有角度偏移），背面必须是正对背面，侧面必须是 90° 正侧面（耳朵、下颌线轮廓清晰），上半身特写也是正对镜头，拒绝任何四分之三侧面或带角度的视角

```python
for char in characters:
    # composed_prompt 由 flux-character-turnaround 技能的完整模板和动态变量生成。
    result = image_selector.execute({
        "prompt": composed_prompt,
        "preferred_provider": "local_diffusion",
        "model": "black-forest-labs/FLUX.1-dev",
        "pipeline_type": "flux",
        "width": 1344,
        "height": 768,
        "num_inference_steps": 28,
        "guidance_scale": 3.5,
        "allow_model_download": False,
        "output_path": f"projects/{project_id}/assets/images/{char['id']}-turnaround.png",
    })
```

FLUX 不接收 `negative_prompt`。将技能配置中的负面模板作为禁用项和验收清单，
把关键限制改写进正向提示词。模型未缓存时停止并请求用户确认下载。

### 步骤 3：构建角色身份锁定包

每个角色需要一个 `identity_lock`，用于后续视频生成时保持角色一致。

```python
identity_lock = {
    "lock_id": f"char_{project_id}_{char['id']}",
    "seed_image_path": combined_image_path,  # 组合图(左侧三视全身+右侧上半身特写)
    "identity_phrases": [
        "the same character",
        "consistent across all shots",
        f"appearance: {char['description']}",
        "no deformation, no drift, no face morph",
    ],
    "prompt_template": char_prompt,
    "registered_at": datetime.now(timezone.utc).isoformat(),
}
```

### 步骤 4：写入注册表

```python
from lib.character_registry import CharacterRegistry, CharacterIdentity

registry = CharacterRegistry(Path(f"projects/{project_id}"))
registry.register_from_character_design(character_design_artifact)
```

### 步骤 5：展示给用户并等待确认

向用户呈现所有角色设计：

```
=== 角色设计确认 ===

角色 1: 剑客
  [角色形象组合图 — 左侧三视全身 + 右侧上半身特写]
  风格: 极致写实, 古风
  生成工具: image_selector | 费用: $0.03

角色 2: 反派
  [角色形象组合图 — 左侧三视全身 + 右侧上半身特写]
  风格: 极致写实, 暗色调
  生成工具: image_selector | 费用: $0.03

总成本: $0.06

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
    pipeline_type="animated-explainer",
    human_approval_required=True,
    human_approved=(approval == "approved"),
)
```

## 验证清单

- [ ] 每张图为同一画布：左侧三视全身 + 右侧上半身正面特写
- [ ] 四栏实际面积接近 22% / 22% / 22% / 34%，而非仅在提示词中声明
- [ ] **纯白色背景** — 整张画布无任何场景装饰
- [ ] **人物比例协调** — 全身与半身比例统一
- [ ] **禁止文字** — 画面中无任何文字
- [ ] **禁止道具** — 角色不持有任何道具
- [ ] **极度写实** — 照片级，不卡通、不插画
- [ ] **不美化** — 保留真实皮肤纹理、毛孔、瑕疵
- [ ] **拒绝陶瓷肌** — 皮肤有真实质感，非光滑陶瓷效果
- [ ] **面部同一** — 全部视图使用同一个面部设计
- [ ] **发型一致** — 全部视图发型（发色、发长、刘海等）完全统一
- [ ] **着装一致** — 全部视图服装配色完全统一
- [ ] **视角绝对正对** — 正面正对镜头、侧面 90° 正侧面、背面正对背面，无角度偏移
- [ ] `identity_lock` 已配置身份锁定短语
- [ ] 角色已写入 `character_registry.json`
- [ ] `approval.status` 为 `"approved"`
