# 内务风格

当未提供设计规范（`frame.md` 或 `design.md`）时的合成创意方向。这些是起点——覆盖任何不服务于内容的设置。当存在设计规范时，其品牌值优先；内务风格填补空白。

## 在编写 HTML 之前

1. **解释提示。** 生成真实内容。食谱列出真实食材。HUD 有真实读数。
2. **选择调色板。** 浅色还是深色？在编写代码前声明 bg、fg、accent。
3. **选择字体。** 运行 [references/typography.md](references/typography.md) 中的字体发现脚本——或选择你已经知道且适合主题的字体。该脚本拓宽你的选择；它不是唯一来源。

## 需质疑的惰性默认值

这些模式是 AI 设计标志——每个 LLM 首先会采用的东西。如果你即将使用其中一个，停下来问：这是为这个内容做的刻意选择，还是我在默认？

- 渐变文字（`background-clip: text` + gradient）
- 卡片/标注上的左边缘强调条纹
- 深色背景上的青色 / 紫到蓝渐变 / 霓虹强调
- 纯 `#000` 或 `#fff`（而是向你的强调色调偏移）
- 相同的卡片网格（重复相同尺寸的卡片）
- 所有内容居中且权重相等（引导视线到某处）
- 禁用字体（完整列表见 [references/typography.md](references/typography.md)）

如果内容确实需要其中之一——庄严结尾的居中布局、真实产品 UI 模拟的卡片、完美匹配主题的禁用字体——那就使用它。目标是意图性，而非回避。

## 颜色

- 将浅/深与内容匹配：食物、健康、儿童 → 浅色。科技、电影、金融 → 深色。
- 一个强调色调。所有场景使用相同的背景。
- 将中性色向你的强调色偏移（即使是微妙的暖/冷也比死灰色好）。
- **对比度：** 由 `hyperframes validate` 强制执行（WCAG AA）。移除装饰后文本必须可读。
- 预先声明调色板。不要逐元素发明颜色。

## 背景层

每个场景都需要视觉深度——在内容动画进入时保持可见的持久装饰元素。没有这些，场景在入场交错期间会感觉空洞。

想法（混搭，每场景 2-5 个）：

- 径向光晕（强调色色调，低不透明度，呼吸缩放）
- 幽灵文字（主题词 3-8% 不透明度，非常大，缓慢漂移）
- 强调线（发丝线，微妙脉动）
- 颗粒/噪点叠加、几何形状、网格图案
- 主题装饰（太空的轨道环、音乐的黑胶唱片槽、数据的网格线）

所有装饰元素应有缓慢的 GSAP 环境动画——呼吸、漂移、脉动。静态的装饰感觉是死的。

**装饰数量 vs 运动数量。** "每场景 2-5 个"指的是装饰_元素_的数量。如果项目的设计规范说"每场景单一环境运动"，意味着应用于这些装饰元素的一个循环运动（共享的呼吸/漂移/脉动）——而不是总共只有一个元素。4 个装饰元素共享一个呼吸运动的场景是正确的；只有 1 个装饰的场景是装饰不足的。

## 运动

完整规则见 [references/motion-principles.md](references/motion-principles.md)。快速参考：0.3-0.6 秒，变化缓动，入场时组合变换，重叠入场。

## 排版

完整规则见 [references/typography.md](references/typography.md)。快速参考：700-900 标题 / 300-400 正文，衬线 + 无衬线（不是两种无衬线），60px+ 标题 / 20px+ 正文。

## 调色板

在编写 HTML 前声明一个背景、一个前景、一个强调色。

| 类别              | 用途                                        | 文件                                                         |
| ----------------- | ------------------------------------------- | ------------------------------------------------------------ |
| 大胆 / 活力        | 产品发布、社交媒体、公告                      | [palettes/bold-energetic.md](palettes/bold-energetic.md)     |
| 温暖 / 编辑        | 讲故事、纪录片、案例研究                      | [palettes/warm-editorial.md](palettes/warm-editorial.md)     |
| 深色 / 高级        | 科技、金融、奢华、电影感                      | [palettes/dark-premium.md](palettes/dark-premium.md)         |
| 干净 / 企业        | 说明视频、教程、演示                          | [palettes/clean-corporate.md](palettes/clean-corporate.md)   |
| 自然 / 大地        | 可持续、户外、有机                            | [palettes/nature-earth.md](palettes/nature-earth.md)         |
| 霓虹 / 电子        | 游戏、科技、夜生活                            | [palettes/neon-electric.md](palettes/neon-electric.md)       |
| 粉彩 / 柔和        | 时尚、美容、生活方式、健康                    | [palettes/pastel-soft.md](palettes/pastel-soft.md)           |
| 宝石 / 丰富        | 奢华、活动、精致                              | [palettes/jewel-rich.md](palettes/jewel-rich.md)             |
| 单色              | 戏剧性、排版聚焦                              | [palettes/monochrome.md](palettes/monochrome.md)             |

或从 OKLCH 推导——选择一个色调，在不同明度下构建 bg/fg/accent，将所有内容向该色调偏移。
