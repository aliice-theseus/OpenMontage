---
name: remotion
description: 工具包特定的 Remotion 模式 — 自定义过渡、共享组件和项目约定。有关核心 Remotion 框架知识（hooks、动画、渲染等），请参见 `remotion-official` 技能。
---

# Remotion — 工具包扩展

> **核心 Remotion 知识** 位于 `.claude/skills/remotion-official/`（从官方 [remotion-dev/skills](https://github.com/remotion-dev/skills) 仓库同步）。本文档仅涵盖**工具包特定**的模式。

## 共享组件

`lib/components/` 中的可重用视频组件。通过以下方式在模板中导入：

```tsx
import { AnimatedBackground, SlideTransition, Label } from '../../../../lib/components';
```

| 组件 | 用途 |
|-----------|---------|
| `AnimatedBackground` | 浮动形状背景（变体：subtle、tech、warm、dark） |
| `SlideTransition` | 场景过渡（fade、zoom、slide-up、blur-fade） |
| `Label` | 浮动标签徽章，可选 JIRA 引用 |
| `Vignette` | 电影感边缘暗化覆盖层 |
| `LogoWatermark` | 角落徽标品牌标识 |
| `SplitScreen` | 并排视频对比 |
| `NarratorPiP` | 画中画讲解员覆盖 |
| `Envelope` | 带开盖动画的 3D 信封 |
| `PointingHand` | 带滑入和脉冲动画的手势表情符号 |
| `MazeDecoration` | 用于角落的动画等距网格装饰 |

## 自定义过渡

工具包包含 `lib/transitions/` 中的过渡库，提供官方 `@remotion/transitions` 包之外的特效。

### 使用 TransitionSeries

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
// 从 lib 导入自定义过渡（根据项目位置调整路径）
import { glitch, lightLeak, clockWipe, checkerboard } from '../../../../lib/transitions';
// 或从 @remotion/transitions 导入官方过渡
import { slide, fade } from '@remotion/transitions/slide';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <TitleSlide />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={glitch({ intensity: 0.8 })}
    timing={linearTiming({ durationInFrames: 30 })}
  />
  <TransitionSeries.Sequence durationInFrames={120}>
    <ContentSlide />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

### 可用自定义过渡

| 过渡 | 选项 | 最佳用途 |
|------------|---------|----------|
| `glitch()` | `intensity`、`slices`、`rgbShift` | 技术演示、前卫展示、赛博朋克 |
| `rgbSplit()` | `direction`、`displacement` | 现代科技、充满活力的过渡 |
| `zoomBlur()` | `direction`、`blurAmount` | 行动号召、高能量时刻、冲击力 |
| `lightLeak()` | `temperature`、`direction` | 庆祝、胶片美学、温馨时刻 |
| `clockWipe()` | `startAngle`、`direction`、`segments` | 时间相关内容、有趣的揭示 |
| `pixelate()` | `maxBlockSize`、`gridSize`、`scanlines`、`glitchArtifacts`、`randomness` | 复古/游戏、数字变换 |
| `checkerboard()` | `gridSize`、`pattern`、`stagger`、`squareAnimation` | 有趣的揭示、结构化过渡 |

**棋盘格图案：** `sequential`、`random`、`diagonal`、`alternating`、`spiral`、`rows`、`columns`、`center-out`、`corners-in`

### 过渡示例

```tsx
// 技术/赛博朋克风格
glitch({ intensity: 0.8, slices: 8, rgbShift: true })

// 温馨庆祝
lightLeak({ temperature: 'warm', direction: 'right' })

// 高能量缩放
zoomBlur({ direction: 'in', blurAmount: 20 })

// 色差
rgbSplit({ direction: 'diagonal', displacement: 30 })

// 时钟扫掠揭示
clockWipe({ direction: 'clockwise', startAngle: 0 })

// 复古像素化
pixelate({ maxBlockSize: 50, glitchArtifacts: true })

// 棋盘格图案
checkerboard({ pattern: 'diagonal', gridSize: 8 })
checkerboard({ pattern: 'spiral', gridSize: 10 })
checkerboard({ pattern: 'center-out', squareAnimation: 'scale' })
```

### 过渡时长指南

| 类型 | 帧数 | 说明 |
|------|--------|-------|
| 快速剪切 | 15-20 | 快速、有力 |
| 标准 | 30-45 | 最常用 |
| 戏剧化 | 50-60 | 缓慢揭示 |
| 毛刺效果 | 20-30 | 应感觉突然 |
| 漏光效果 | 45-60 | 需要时间扫掠 |

### 预览过渡

运行展示画廊查看所有过渡：

```bash
cd showcase/transitions && npm run studio
```

## 工具包最佳实践

1. **仅使用基于帧的动画** — 避免 CSS 过渡/动画；它们在渲染过程中会导致闪烁
2. **使用 useVideoConfig() 中的 fps** — 使动画独立于帧率
3. **钳制插值** — 使用 `extrapolateRight: 'clamp'` 防止值失控
4. **使用 OffthreadVideo** — 对于复杂合成，性能优于 `<Video>`
5. **对异步操作使用 delayRender** — 始终阻塞渲染直到数据就绪
6. **资源文件使用 staticFile** — 正确引用 `public/` 文件夹中的文件
7. **所有项目使用 30fps** — 计时：帧数 = 秒数 × 30
8. **playbackRate 必须恒定** — 对于可变/极端速度，先用 FFmpeg 预处理

## 项目计时约定

| 场景类型 | 时长 | 说明 |
|------------|----------|-------|
| 标题 | 3-5s (90-150f) | 标志 + 标题 |
| 概览 | 10-20s | 3-5 个要点 |
| 演示 | 10-30s | 调整 playbackRate 以适应 |
| 数据 | 8-12s | 3-4 个数据卡片 |
| 致谢 | 5-10s | 快速淡出 |

**节奏：** 画外音约 150 字/分钟。画外音决定计时。

## 高级 API

有关所有 hooks、组件、渲染器、Lambda 和 Player API 的详细 API 文档，请参见 [reference.md](reference.md)。

## 许可说明

Remotion 有特殊的许可。公司可能需要获得商业使用许可。请查看 https://remotion.dev/license

---

## 反馈与贡献

如果此技能缺少信息或可以改进：

- **缺少某个模式？** 描述您需要的内容
- **发现错误？** 请告知问题所在
- **想要贡献？** 我可以帮助您：
  1. 用改进更新此技能
  2. 向 github.com/digitalsamba/claude-code-video-toolkit 创建 PR

只需说"improve this skill"，我将引导您更新 `.claude/skills/remotion/SKILL.md`。
