---
name: flux-character-turnaround
description: 使用本地 FLUX.2 Dev 分步生成用于 3D 建模、角色绑定、服装拆分和 Cosplay 制版的人物四视图参考图，包含正面全身、90 度侧面全身、背面全身和胸部以上特写。用户提到四视图、四视图、角色建模参考、人物设定稿、建模四视图、服装拆分参考、正面侧面背面或人体比例参考时使用。
---

# FLUX.2 Dev 角色四视图

生成同一人物、同一服装和统一比例的建模参考图。虽然用户常称“四视图”，本技能的标准交付物是三个全身视角加一个半身特写。

## 前置读取

1. 完整读取 [references/prompt-template.json](references/prompt-template.json)。
2. 在编写或调整提示词前读取 `../flux-best-practices/SKILL.md`。
3. 在 OpenMontage 管道中调用 `character_ref_sheet`；它会逐张通过 `image_selector` 路由到 `local_diffusion`，不要直接实例化提供商工具。

## 工作流

1. 从用户请求提取 `dynamic_custom_vars`。未提供的字段使用参考配置中的默认值。
2. 将角色年龄、体型、服装层级、颜色、发型、鞋履和配饰写成明确、无歧义的自然语言。
3. 将所有视图共享的身份、面容、体型、服装、材质、发型和配饰合成为一段稳定的 `character_core`；视角和构图不要混入其中。
4. 使用分步流程：正面全身 T2I → 以正面图为共同参考分别生成侧面、背面和半身 → 本地确定性拼接。不要要求扩散模型一次生成四栏，因为这会显著增加身份漂移、布局错位和肢体裁切。
5. 将负向模板作为质量禁用项读取。FLUX 不支持负面提示词，因此不要传入 `negative_prompt`；改写成正向约束，例如“仅一个人物”“头脚完整可见”“四个视图服装完全相同”“无文字和水印”。
6. 生成前向用户声明工具、提供商、模型和运行模式。基础模型或 LoRA 未缓存时，停止并请求下载确认；未经确认不得设置 `allow_model_download=true`。
7. 正面图是身份锚点。先以 `operation="front_only"` 生成并提交用户审查；如果正面存在脸部、服装、人体或裁切问题，不要继续。批准后以 `operation="complete_from_front"` 和 `front_image_path` 生成其余视图。只有用户明确批准跳过中间检查时才用 `operation="full"`。
8. 生成后按验收清单检查。关键失败最多重试两轮；仍失败则展示当前结果和问题，不宣称其可用于建模。

## 固定调用契约

```python
result = character_ref_sheet.execute({
    "character_id": character_id,
    "character_core": character_core,
    "output_dir": f"projects/{project_id}/assets/images/characters",
    "model": "black-forest-labs/FLUX.2-dev",
    "seed": seed,
    "num_inference_steps": 20,
    "guidance_scale": 3.5,
    "allow_model_download": False,
    "operation": "front_only",
})

# 用户批准正面身份锚点后：
result = character_ref_sheet.execute({
    "character_id": character_id,
    "character_core": character_core,
    "output_dir": f"projects/{project_id}/assets/images/characters",
    "model": "black-forest-labs/FLUX.2-dev",
    "seed": seed,
    "num_inference_steps": 20,
    "guidance_scale": 3.5,
    "allow_model_download": False,
    "operation": "complete_from_front",
    "front_image_path": approved_front_path,
})
```

内部生成尺寸：

- 正面 T2I：`1024 × 1536`
- 侧面、背面、半身参考生成：`832 × 1248`
- 交付组合图：`1280 × 720`

工具对四次生成复用同一个 `Flux2Pipeline`，采用 `enable_sequential_cpu_offload()`，结束后清空缓存。侧面、背面和半身均使用正面图作为 `image` 条件，并保持同一 seed。模型缺失时必须请求下载确认，不得切换到 FLUX.1 或云端模型。

## 硬性构图

- 最终横向四栏由本地拼接保证：正面 281 px、侧面 281 px、背面 281 px、半身 437 px，总计 `1280 × 720`，栏间距 0 px。
- 纯白无缝背景，无场景、道具、装饰、文字或水印。
- 四栏必须是同一人物、同一服装、同一发型、同一配色、同一人体比例和同一棚拍光。
- 三个全身视图必须从头到脚完整可见，标准自然站姿，四肢无遮挡。
- 半身特写必须包含完整头部和双肩，清楚展示五官、发型、领口、肩线、材质与配饰位置。

半身图拼接前保留顶部 80%，各栏使用 LANCZOS 缩放和居中裁切。分栏布局由代码保证，但人物是否完整、视角是否正确仍须目视检查。

## 验收清单

- [ ] 四栏顺序正确，面积接近 22/22/22/34。
- [ ] 只有一个角色身份，没有多余人物或视图重叠。
- [ ] 正面、侧面、背面和特写的脸型、发型与配色一致。
- [ ] 正面严格正对，侧面严格 90 度，背面严格背对。
- [ ] 全身视图头、手、脚完整，无裁切、断肢和明显手足畸形。
- [ ] 服装前后结构、接缝、层次、鞋袜和配件位置可识别且一致。
- [ ] 人体比例自然，肩线和骨盆水平，无夸张动态。
- [ ] 背景纯白，光影均匀，无厚重阴影、文字、水印和噪点。

任何身份不一致、服装漂移、视角错误、头脚裁切或严重肢体畸形均为关键失败。
