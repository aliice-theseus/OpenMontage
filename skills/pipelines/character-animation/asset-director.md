# 资源导演 - 角色动画管线

## 目标

产出 `asset_manifest`，包含角色部件、背景、道具、音频、音乐和预览产物。

## Layer 3 门控

在创作或生成动画资源之前，请阅读相关的 Layer 3 技能：

- `character-rigging`
- `svg-character-animation`
- `pose-library-design`
- `canvas-procedural-animation`（当使用 p5/canvas 特效时）
- `character-animation-qa`（审阅前）
- `gsap-core`、`gsap-timeline` 和 `gsap-react`（用于 GSAP/Remotion 工作）
- `remotion` 和 `remotion-best-practices`（用于 Remotion 渲染工作）
- `hyperframes` 和 `hyperframes-cli`（用于 HyperFrames 工作）

在图像/TTS/音乐生成之前，请从注册表中读取工具的 `agent_skills`。

## 资源组织

角色资源存放在：

```text
projects/<project-name>/assets/characters/<character-id>/
```

使用子文件夹：

```text
parts/
poses/
previews/
```

生成的背景存放在：

```text
projects/<project-name>/assets/backgrounds/
```

## 流程

1. 仅制作或获取 `rig_plan` 所需的部件。
2. 保持每个活动部件独立分离。
3. 为部件保留透明背景。
4. 记录提示词、种子、提供者和模型名称。
5. 在全量资源扩展之前先构建一个小型预览。

## 质量门槛

`rig_plan` 引用的所有部件必须在合成之前存在。缺失部件构成阻塞，除非动作时间线移除了需要该部件的动作。
