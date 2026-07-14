---
name: manim-composer
description: |
  Trigger when: (1) User wants to create an educational/explainer video, (2) User has a vague concept they want visualized, (3) User mentions "3b1b style" or "explain like 3Blue1Brown", (4) User wants to plan a Manim video or animation sequence, (5) User asks to "compose" or "plan" a math/science visualization.

  Transforms vague video ideas into detailed scene-by-scene plans (scenes.md). Conducts research, asks clarifying questions about audience/scope/focus, and outputs comprehensive scene specifications ready for implementation with ManimCE or ManimGL.

  Use this BEFORE writing any Manim code. This skill plans the video; use manimce-best-practices or manimgl-best-practices for implementation.
---

## 工作流程

### 阶段 1：理解概念

1. **深入研究主题**后再提问
   - 使用网络搜索理解核心概念
   - 确定使该主题有趣的关键见解
   - 找到"顿悟时刻"——是什么让学习者恍然大悟
   - 记录需要解决的常见误解

2. **确定叙事钩子**
   - 这个视频回答什么问题？
   - 观众为什么要在意？
   - 什么元素令人惊讶或反直觉？

### 阶段 2：与用户澄清

提出针对性的问题（不要一次全部提出——根据回答调整）：

**受众与范围**
- 我应该假设什么样的数学/科学背景？（例如"懂微积分"或"高中代数"）
- 目标视频长度？（短：5-10 分钟，中：15-20 分钟，长：30 分钟以上）
- 应该独立成篇还是作为系列的一部分？

**重点与深度**
- 是否有需要强调或跳过的特定方面？
- 侧重证明还是侧重直觉？
- 是否包含实际应用？

**风格偏好**
- 配色方案偏好？
- 旁白风格？（休闲、正式、有趣）
- 有没有想到的特定视觉隐喻？

### 阶段 3：创建 scenes.md

输出一个结构完整的 `scenes.md` 文件：

```markdown
# [视频标题]

## 概述
- **主题**：[核心概念]
- **钩子**：[开场问题/谜团]
- **目标受众**：[先决条件]
- **预计时长**：[X 分钟]
- **关键见解**：[顿悟时刻]

## 叙事弧线
[用 2-3 句话描述从困惑到理解的旅程]

---

## 场景 1：[场景名称]
**时长**：约 X 秒
**目的**：[此场景达到的目的]

### 视觉元素
- [所需 mobject 列表]
- [要使用的动画]
- [摄像机移动]

### 内容
[详细描述发生了什么、展示了什么、解释了什么]

### 旁白说明
[要传达的关键点、语气、节奏说明]

### 技术说明
- [要使用的特定 Manim 类/方法]
- [任何需要注意的技巧性实现]

---

## 场景 2：[场景名称]
...

---

## 过渡与流程
[关于场景如何连接、重复出现的视觉主题的说明]

## 调色板
- 主色：[颜色] - 用于[用途]
- 辅色：[颜色] - 用于[用途]
- 强调色：[颜色] - 用于[用途]
- 背景色：[颜色]

## 数学内容
[需要渲染的方程、公式或数学对象列表]

## 实现顺序
[建议的场景实现顺序，注明依赖关系]
```

## 3b1b 风格原则

在编写场景时应用以下原则：

### 视觉叙事
- **展示，而非仅仅讲述** - 每个概念都需要视觉表现
- **渐进揭示** - 逐步构建复杂度，不要一次性展示所有内容
- **视觉连续性** - 尽可能变换对象而不是替换它们

### 节奏与韵律
- **为顿悟留白** - 给观众时间吸收关键时刻
- **变化节奏** - 混合快速序列和较慢的解释
- **场景以解决收尾** - 每个场景应感觉完整

### 数学之美
- **强调优雅** - 突出数学令人惊讶地简单或优美的部分
- **连接表达方式** - 以多种方式展示同一概念（代数、几何、直觉）
- **逐步拥抱抽象** - 从具体开始，然后概括

### 参与技巧
- **提出问题** - 在揭示答案前激发观众的好奇心
- **承认难度** - "乍看可能令人困惑..."
- **庆祝洞察** - 让"顿悟时刻"感觉是应得的

## 参考

- [references/narrative-patterns.md](references/narrative-patterns.md) - 常见 3b1b 叙事结构
- [references/visual-techniques.md](references/visual-techniques.md) - 高效可视化模式
- [references/scene-examples.md](references/scene-examples.md) - 示例 scenes.md 节选

## 模板

- [templates/scenes-template.md](templates/scenes-template.md) - 空白 scenes.md 模板
