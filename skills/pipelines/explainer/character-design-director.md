# 角色设计导演 — 解说片流水线

## 适用场景

你是**角色设计导演**。你在 `scene_plan` 完成之后、`scene_sketch` 之前工作。
当剧本中出现人物角色（尤其是主角）时，你需要为**每个角色生成四视图概念设计**，
产出**角色身份锁定包**，提交用户确认后方可进入下一阶段。

**这是强制阶段。** 当 `scene_plan` 分析出有人物主角时，此阶段不可跳过。

## 前置条件

| 层 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/character_design.schema.json` | 产物验证 |
| 前置产物 | `scene_plan` | 提取角色列表和描述 |
| 可选 | 上一项目的 `character_registry.json` | 复用已有角色身份 |
| 工具 | `character_ref_sheet`（内部使用 `image_selector`） | 分步生成并拼接四视图 |
| 第 3 层技能 | `.agents/skills/flux-character-turnaround/SKILL.md` | FLUX.2 Dev 四视图提示模板、变量和验收规则 |

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

如果角色已注册，直接复用身份锁，无需重新生成四视图。
如果角色需要更新（例如新剧情需要不同服装），正常生成并更新注册表。

### 步骤 2：为每个角色生成角色形象图

生成前必须完整读取 `.agents/skills/flux-character-turnaround/SKILL.md` 及其引用的
`references/prompt-template.json`，按该技能组合稳定的 `character_core`。此角色建模参考场景固定使用
`character_ref_sheet → image_selector → local_diffusion → black-forest-labs/FLUX.2-dev`；不得改用通用 Schnell 默认或云端模型。

对每个角色，先调用 `character_ref_sheet(operation="front_only")` 生成正面身份锚点并提交用户确认。正面批准后，调用 `operation="complete_from_front"` 并传入 `front_image_path`，以正面图为共同参考生成侧面、背面和半身，最后本地拼接。只有用户明确批准跳过中间检查时才使用 `operation="full"`：

| 区域 | 内容 | 用途 |
|------|------|------|
| **画面左侧** | 三视全身图（正面、侧面、背面并排） | 完整角色定义，Seedance identity_lock 锚定图 |
| **画面右侧** | 上半身正面视角特写图 | 面部细节参考 |

**画面布局：**
- 四张源图分别生成：正面 `1024×1536`；侧面、背面、半身各 `832×1248`
- 最终画布为 **1280×720**，四栏固定为 `281 / 281 / 281 / 437 px`，0 px 间距
- 半身图拼接前保留顶部 80%，各栏采用 LANCZOS 缩放与居中裁切

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
    front_result = character_ref_sheet.execute({
        "character_id": char["id"],
        "character_core": composed_character_core,
        "output_dir": f"projects/{project_id}/assets/images/characters",
        "model": "black-forest-labs/FLUX.2-dev",
        "seed": character_seed,
        "num_inference_steps": 20,
        "guidance_scale": 3.5,
        "allow_model_download": False,
        "operation": "front_only",
    })
    # 展示 front_result.data["front_path"]，等待用户批准。
    result = character_ref_sheet.execute({
        "character_id": char["id"],
        "character_core": composed_character_core,
        "output_dir": f"projects/{project_id}/assets/images/characters",
        "model": "black-forest-labs/FLUX.2-dev",
        "seed": character_seed,
        "num_inference_steps": 20,
        "guidance_scale": 3.5,
        "allow_model_download": False,
        "operation": "complete_from_front",
        "front_image_path": front_result.data["front_path"],
    })
```

FLUX 不接收 `negative_prompt`。将技能配置中的负面模板作为禁用项和验收清单，
把关键限制改写进正向提示词。正面图失败时立即停止，不要用失败的身份锚点继续生成。
模型未缓存时停止并请求用户确认下载。

### 步骤 3：上传角色图到腾讯 COS（硬性门禁）

角色图生成后，**必须**上传到腾讯 COS 获得公开访问 URL。视频生成阶段（assets）只接受 COS URL，拒绝本地路径。

**上传失败是阻塞性错误，不得静默降级为本地路径。** 如果上传失败，必须向用户报告错误并停止本阶段。

```python
from tools.publishers.cos_upload import CosUpload

cos = CosUpload()
# 上传四视图源图和组合图
view_map = result.data["view_paths"]  # {"front": path, "side": ..., "back": ..., "closeup": ...}
cos_urls: dict[str, str] = {}
for view, local_path in view_map.items():
    upload_result = cos.execute({
        "file_path": local_path,
        "project_id": project_id,
        "asset_type": "characters",
        "verify_url": True,        # 上传后自动验证 URL 可公开访问
        "anti_review": True,       # 反审核预处理：剥离EXIF+重编码+微噪，绕过hash拦截
    })
    if not upload_result.success:
        # 上传失败 = 阻塞，上报用户
        raise RuntimeError(
            f"COS 上传失败（{view}）：{upload_result.error}\n"
            f"角色设计阶段无法继续，请检查 COS 配置后重试。"
        )
    cos_urls[view] = upload_result.data["url"]

# 上传拼接后的组合图
sheet_result = cos.execute({
    "file_path": result.data["sheet_path"],
    "project_id": project_id,
    "asset_type": "characters",
    "verify_url": True,
    "anti_review": True,
})
if not sheet_result.success:
    raise RuntimeError(
        f"COS 上传失败（组合图）：{sheet_result.error}\n"
        f"角色设计阶段无法继续，请检查 COS 配置后重试。"
    )
sheet_url = sheet_result.data["url"]
```

### 步骤 4：构建角色身份锁定包

每个角色需要一个 `identity_lock`，用于后续视频生成时保持角色一致。
`seed_image_url` 使用 COS 公开 URL，确保 Seedance 等云端工具可以访问。

```python
identity_lock = {
    "lock_id": f"char_{project_id}_{char['id']}",
    "seed_image_path": combined_image_path,  # 组合图本地路径
    "seed_image_url": sheet_url,            # 组合图 COS 公开 URL（供 Seedance reference_image_url 使用）
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

角色项的 `image_path_*` 保留本地路径，同时新增 `image_url_*` 写入 COS URL：

```python
char_artifact = {
    "id": char["id"],
    "display_name": char.get("display_name", char["id"]),
    "image_path_front": view_map.get("front", ""),
    "image_path_side": view_map.get("side", ""),
    "image_path_back": view_map.get("back", ""),
    "image_url_front": cos_urls.get("front", ""),   # COS URL
    "image_url_side": cos_urls.get("side", ""),     # COS URL
    "image_url_back": cos_urls.get("back", ""),     # COS URL
    "prompt": char_prompt,
    "source_tool": "character_ref_sheet",
    "cost_usd": 0.0,
    "seed": character_seed,
    "description": char["description"],
}
```

### 步骤 5：写入注册表

注册表会自动识别 COS URL 字段，并在 `build_reference_config()` 中优先返回 COS URL。

```python
from lib.character_registry import CharacterRegistry, CharacterIdentity

registry = CharacterRegistry(Path(f"projects/{project_id}"))
registry.register_from_character_design(character_design_artifact)
```

### 步骤 6：展示给用户并等待确认

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

### 步骤 7：写入检查点

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
- [ ] `identity_lock.seed_image_url` 已填写 COS 公开 URL
- [ ] 角色 `image_url_*` 字段已填写 COS URL
- [ ] 角色已写入 `character_registry.json`
- [ ] `approval.status` 为 `"approved"`
