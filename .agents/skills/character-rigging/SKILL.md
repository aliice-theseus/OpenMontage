---
name: character-rigging
description: 构建数据驱动的二维角色绑定系统用于本地动画：部件、枢轴点、图层、约束、视角和可复用的绑定包。
license: MIT
---

# 角色绑定

在构建 OpenMontage `rig_plan` 制品或为本地二维角色动画构建渲染器输入时使用此技能。

## 成熟模式

- 保持运行时代码通用化；将每个角色做成一个数据包。
- 将角色拆分为可独立变换的部件。
- 在与美术作品相同的坐标空间中定义枢轴点。
- 在运动部件上存储约束以防止不可能的旋转。
- 保持图层顺序显式；不要在生成后依赖 SVG 源顺序。
- 从一个视角开始，仅在镜头列表需要时添加更多视角。

## 绑定包

```json
{
  "character_id": "mouse",
  "rig_type": "svg_rig",
  "parts": [
    { "id": "body", "kind": "torso", "layer": 10 },
    { "id": "head", "kind": "head", "layer": 30, "parent": "body" },
    { "id": "arm_right", "kind": "limb", "layer": 40, "parent": "body" }
  ],
  "joints": {
    "head": { "pivot": [320, 180], "rotation": [-20, 20] },
    "arm_right": { "pivot": [390, 310], "rotation": [-70, 95] }
  }
}
```

## 质量检查清单

- 每个运动部件都有枢轴点。
- 在层级关系重要的地方，每个子部件都有父部件。
- 嘴型是单独的资产或单独的路径组。
- 当视线需要变化时，眼睛和瞳孔是分开的。
- 如果角色触摸或携带道具，道具是分离的。

## 参考资料

- SVG transform-origin 行为由浏览器定义，对坐标空间敏感；使用 GSAP `svgOrigin` 时，优先使用显式的 SVG 坐标枢轴点：https://gsap.com/docs/v3/GSAP/CorePlugins/CSS/
- Remotion 动画必须通过当前帧实现帧驱动和确定性：https://www.remotion.dev/docs/use-current-frame
