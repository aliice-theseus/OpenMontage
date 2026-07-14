---
name: remotion
description: 工具包特定的 Remotion 模式——自定义过渡、共享组件和项目约定。关于核心 Remotion 框架知识（hooks、动画、渲染等），请参阅 `remotion-official` 技能。
---

# Remotion — 工具包扩展

> **核心 Remotion 知识** 位于 `.claude/skills/remotion-official/`（从官方 [remotion-dev/skills](https://github.com/remotion-dev/skills) 仓库同步）。本文件仅涵盖**工具包特定**模式。

## 共享组件

`lib/components/` 中的可复用视频组件。在模板中通过以下方式导入：

```tsx
import { AnimatedBackground, SlideTransition, Label } from '../../../../lib/components';
```

| 组件 | 用途 |
|-----------|---------|
| `AnimatedBackground` | 浮动形状背景（变体：subtle、tech、warm、dark）|
| `SlideTransition` | 场景过渡（fade、zoom、slide-up、blur-fade）|
| `Label` | 浮动标签徽章，可选 JIRA 引用 |
| `Vignette` | 电影感边缘暗化叠加 |
| `LogoWatermark` | 角落 Logo 品牌标志 |
| `SplitScreen` | 并排视频比较 |
| `NarratorPiP` | 画中画演示者叠加 |
| `Envelope` | 带开口翻盖动画的 3D 信封 |
| `PointingHand` | 带动画滑入和脉冲的手部表情符号 |
| `MazeDecoration` | 用于角落的动画等距网格装饰 |

## 自定义过渡

工具包包含 `lib/transitions/` 上的过渡库，用于场景间的效果，超越了官方的 `@remotion/transitions` 包。

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

### 可用的自定义过渡

| 过渡 | 选项 | 最佳用途 |
|------------|---------|----------|
| `glitch()` | `intensity`、`slices`、`rgbShift` | 技术演示、前卫揭示、赛博朋克 |
| `rgbSplit()` | `direction`、`displacement` | 现代科技、充满活力的过渡 |
| `zoomBlur()` | `direction`、`blurAmount` | CTA、高能量时刻、冲击力 |
| `lightLeak()` | `temperature`、`direction` | 庆祝、电影美学、温馨时刻 |
| `clockWipe()` | `startAngle`、`direction`、`segments` | 时间相关内容、有趣的揭示 |
| `pixelate()` | `maxBlockSize`、`gridSize`、`scanlines`、`glitchArtifacts`、`randomness` | 复古/游戏、数字变换 |
| `checkerboard()` | `gridSize`、`pattern`、`stagger`、`squareAnimation` | 有趣的揭示、结构化过渡 |

**Checkerboard 模式：** `sequential`、`random`、`diagonal`、`alternating`、`spiral`、`rows`、`columns`、`center-out`、`corners-in`

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

// 时钟扫描揭示
clockWipe({ direction: 'clockwise', startAngle: 0 })

// 复古像素化
pixelate({ maxBlockSize: 50, glitchArtifacts: true })

// Checkerboard 模式
checkerboard({ pattern: 'diagonal', gridSize: 8 })
checkerboard({ pattern: 'spiral', gridSize: 10 })
checkerboard({ pattern: 'center-out', squareAnimation: 'scale' })
```

### 过渡时长指南

| 类型 | 帧数 | 说明 |
|------|--------|-------|
| 快速切换 | 15-20 | 快、有力 |
| 标准 | 30-45 | 最常见 |
| 戏剧性 | 50-60 | 缓慢揭示 |
| 故障效果 | 20-30 | 应感觉突然 |
| 光泄漏 | 45-60 | 需要时间扫过 |

### 预览过渡

运行展示画廊查看所有过渡：

```bash
cd showcase/transitions && npm run studio
```

## 工具包最佳实践

1. **仅基于帧的动画** — 避免 CSS 过渡/动画；它们在渲染期间导致闪烁
2. **使用 useVideoConfig() 中的 fps** — 使动画与帧率无关
3. **钳制插值** — 使用 `extrapolateRight: 'clamp'` 防止失控值
4. **使用 OffthreadVideo** — 对于复杂合成，性能优于 `<Video>`
5. **异步使用 delayRender** — 始终阻塞渲染直到数据就绪
6. **静态文件使用 staticFile** — 正确引用 `public/` 文件夹中的文件
7. **所有项目使用 30fps** — 时间：帧数 = 秒数 × 30
8. **playbackRate 必须是常数** — 对于可变/极端速度，使用 FFmpeg 预处理

## 项目时间约定

| 场景类型 | 时长 | 说明 |
|------------|----------|-------|
| 标题 | 3-5s（90-150f） | Logo + 标题 |
| 概述 | 10-20s | 3-5 个要点 |
| 演示 | 10-30s | 调整 playbackRate 以适配 |
| 统计数据 | 8-12s | 3-4 个统计卡片 |
| 致谢 | 5-10s | 快速淡出 |

**节奏：** 画外音约 150 词/分钟。画外音驱动时间。

## 高级 API

所有 hooks、组件、渲染器、Lambda 和 Player API 的详细 API 文档，请参阅 [reference.md](reference.md)。

## 许可证说明

Remotion 有特殊许可。公司可能需要获得商业使用许可。查看 https://remotion.dev/license

---

## 反馈与贡献

如果此技能缺少信息或可以改进：

- **缺少模式？** 描述您需要的内容
- **发现错误？** 告诉我哪里有问题
- **想要贡献？** 我可以帮助您：
  1. 用改进更新此技能
  2. 向 github.com/digitalsamba/claude-code-video-toolkit 创建 PR

只需说"improve this skill"，我将引导您更新 `.claude/skills/remotion/SKILL.md`。
