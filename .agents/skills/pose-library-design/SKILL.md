---
name: pose-library-design
description: 设计可复用的二维角色姿态库、动作循环和表情状态，用于数据驱动的动画。
license: MIT
---

# 姿态库设计

在制作 `pose_library` 制品时使用此技能。

## 姿态分类

- 中性：idle、breathe、listening。
- 注意力：look_up、look_down、look_left、look_right。
- 表情：happy、sad、surprised、worried、determined。
- 动作：reach、point、hold、jump、flap、walk_contact、walk_passing。
- 嘴型：closed、small_o、wide_open、smile、frown、类似音素形状。

## 表演模式

使用定时姿态序列：

```text
anticipation -> action -> hold -> settle
```

不要持续动画每个部位。停顿使表演可读。

## 姿态数据模式

```json
{
  "pose": "surprised",
  "parts": {
    "head": { "rotation": -6, "y": -4 },
    "pupil_left": { "x": 4, "y": -6 },
    "mouth": "small_o"
  },
  "hold_frames": 18,
  "transition": "back.out"
}
```

## 质量检查清单

- 必需的表情都有姿态。
- 必需的动作都有姿态或循环。
- 复用的循环有接触和过渡姿态。
- 姿态仅命名变化的部件；默认值来自绑定。

## 参考资料

- GSAP 时间线排序，实现可读的多步骤姿态：
  https://gsap.com/docs/v3/GSAP/Timeline/
- Remotion 插值，用于基于帧的过渡：
  https://www.remotion.dev/docs/interpolate
- Remotion spring，用于自然的运动：
  https://www.remotion.dev/docs/spring
