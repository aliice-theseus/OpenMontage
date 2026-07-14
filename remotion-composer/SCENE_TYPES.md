# Remotion Composer——场景与叠加层速查表

`Explainer` 合成接受的 `cut.type` 和 `overlay.type` 值的权威列表。每一行对应 `src/Explainer.tsx` 中的一个调度分支。

当你添加新组件时，请在此文件和 `src/components/index.ts` 中追加。

---

## 剪辑类型（`cut.type`）

| `type` | 组件 | 必填字段 | 常用字段 | 用途 |
|--------|------|---------|---------|------|
| *（无——视频）* | `OffthreadVideo` | `source`（mp4 路径） | `source_in_seconds`, `animation`（放大, ken-burns）, `in_seconds`, `out_seconds` | 直接播放 MP4 片段 |
| *（无——图片）* | `Img` | `source`（png/jpg 路径） | `animation`, `in_seconds`, `out_seconds` | 使用 Ken Burns 效果播放静态图片 |
| `text_card` | `TextCard` | `text` | `fontSize`, `backgroundVideo`, `backgroundOverlay`, `color` | 大字排版节拍 |
| `hero_title` | `HeroTitle` | `text` | `heroSubtitle`, `backgroundVideo`, `backgroundOverlay` | 标题/结束卡片 |
| `stat_card` | `StatCard` | `stat` | `subtitle`, `accentColor`, `backgroundVideo` | 单一大数据数字 |
| `callout` | `CalloutBox` | `text` | `callout_type`（info/warning/tip/quote）, `title`, `backgroundVideo` | 带要点的框式消息 |
| `comparison` | `ComparisonCard` | `leftLabel`, `leftValue`, `rightLabel`, `rightValue` | `title`, `backgroundColor` | 并排比较 |
| `bar_chart` | `BarChart` | `chartData` | `chartAnimation`, `showValues`, `showGrid`, `backgroundVideo` | 动画柱状图 |
| `line_chart` | `LineChart` | `chartSeries` | `chartAnimation`, `xLabel`, `yLabel`, `showMarkers` | 动画折线图 |
| `pie_chart` | `PieChart` | `chartData` | `donut`, `centerLabel`, `centerValue`, `showLegend` | 饼图/环形图 |
| `kpi_grid` | `KPIGrid` | `chartData` | `title`, `columns`, `chartAnimation` | 2-4 列 KPI 网格 |
| `progress_bar` | `ProgressBar` | `progress` | `progressLabel`, `progressColor`, `progressSegments` | 动画进度条 |
| `anime_scene` | `AnimeScene` | `images`（列表） | `particles`, `lightingFrom`, `lightingTo`, `vignette` | 静态图片动漫场景，带粒子和摄像机运动 |
| **`terminal_scene`** | **`TerminalScene`** | **`steps`**（cmd/out/pause/pill 列表） | **`terminalTitle`, `prompt`, `accentColor`** | **合成终端动画——无需真实录屏。见 [`.agents/skills/synthetic-screen-recording/SKILL.md`](../.agents/skills/synthetic-screen-recording/SKILL.md)** |
| **`screenshot_scene`** | **`ScreenshotScene`** | **`backgroundImage`**（`public/` 中的路径）, **`screenshotSteps`**（叠加层列表） | **`screenshotSize`（自然像素宽/高）, `cursorStartAt`, `accentColor`** | **方法-1 合成 UI——放置任意截图，在之上动画化脚本化叠加层（光标、click_pulse、type_into、bubble_append、typing_dots、highlight_box、callout_balloon）。对于 15-30s 的聚焦演示，观众无法区分与真实录屏。坐标针对 contain-fit 矩形归一化（0-1）。见 [`.agents/skills/synthetic-ui-recording/SKILL.md`](../.agents/skills/synthetic-ui-recording/SKILL.md)（计划中）。** |

---

## 叠加层类型（`overlay.type`）

| `type` | 组件 | 必填字段 | 常用字段 | 用途 |
|--------|------|---------|---------|------|
| `section_title` | `SectionTitle` | `text` | `accentColor`, `position`（top-left 等） | 小章节标签 |
| `stat_reveal` | `StatReveal` | `text` | `subtitle`, `accentColor`, `position` | 角落统计徽章 |
| `hero_title` | `HeroTitle`（作为叠加层） | `text` | `subtitle` | 全帧标题叠加层 |
| **`provider_chip`** | **`ProviderChip`** | **`providers`**（字符串列表） | **`cycleSeconds`, `position`, `accentColor`, `label`** | **轮播在提供商名称间循环的徽章——用于 AI 生成运动场景，显示该片段由哪个模型生成** |

---

## 添加新的场景类型

1. 在 `src/components/MyScene.tsx` 中创建 React 组件。使用 `interpolate(frame, [inFrame, outFrame], [from, to])` 和 `spring(...)` 实现运动。读取 `useCurrentFrame()` 和 `useVideoConfig()`。
2. 在 `src/components/index.ts` 中导出它。
3. 在 `src/Explainer.tsx` 的 `Cut` 接口中添加 `type`（以及任何新的 prop 字段）。
4. 在 `SceneRenderer` 中添加调度分支：
   ```tsx
   if (cut.type === "my_scene" && cut.mySceneData) {
     return maybeWrapWithBg(<MyScene ... />);
   }
   ```
5. 在此文件中记录。这就是让下一个代理能发现它的方式。

## 现有合成 UI 组件

目前仅存在 `TerminalScene`。该模式可推广——如果流水线需要，可能接下来添加的候选项包括：

- `ChatTranscript`——带打字动画的 Claude/Cursor/GPT 聊天气泡时间线
- `EditorScene`——VS Code 风格代码编辑器，带语法高亮和光标运动
- `PrReview`——GitHub PR 差异视图，带内联评论展示
- `SlackThread`——Slack 线程，带头像和反应弹出
- `TicketBoard`——Jira / Linear 卡片在列间移动

模式：遵循 `TerminalScene.tsx`——一个 `steps` 列表，包含时间线原语、光标推进持续时间、基于 spring 的展示、可选的非阻塞 pill/徽章。
