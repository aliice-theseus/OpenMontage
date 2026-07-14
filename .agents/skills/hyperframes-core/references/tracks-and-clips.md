# 轨道与剪辑

剪辑是合成根的定时子元素。轨道是一个时间重叠概念，而非视觉层叠概念。

## 什么是剪辑

剪辑是任何带有 `data-start`、`data-duration`（需要时）和 `data-track-index` 的 DOM 元素。常见类型：

- **视觉 `<div>` 剪辑** — 场景、卡片、叠加层。始终需要 `data-duration`。
- **子合成宿主** — 带有 `data-composition-src` 的 `<div>`。始终需要 `data-duration`。
- **视频剪辑** — 带有 `muted` 和 `playsinline` 的 `<video>`。时长可以默认为媒体长度。
- **音频剪辑** — `<audio>`。时长可以默认为媒体长度。
- **图片剪辑** — `<img>`。始终需要 `data-duration`。

为创作的视觉剪辑添加 `class="clip"`，以便工具和示例可以找到它们。

## 轨道是时间性的，而非视觉性的

`data-track-index` 控制**时间重叠**，而非绘制顺序：

- **同一 `data-track-index` 上的两个剪辑**不能在时间上重叠。`hyperframes lint` 会标记此问题。
- **视觉层级（前/后）** 由 CSS `z-index` 控制，而非轨道索引。

轨道 `5` 上的剪辑并不"高于"轨道 `1` 上的剪辑 — 它只是在时间上处于不同的音频/视觉通道中。使用 CSS 进行层叠，使用轨道进行排序。

## 选择轨道索引

没有固定的约定，但常见模式：

- **轨道 0** — 基础视频（例如 A-roll）。
- **轨道 1+** — 视觉场景、叠加层、字幕。
- **较高轨道（例如 10+）** — 音频剪辑，与视觉轨道分开以保持 lint 检查清晰。

向现有合成添加新剪辑时：

1. 找到一个现有轨道，其与新剪辑的 `[data-start, data-start + data-duration)` 范围没有重叠。
2. 或者选择一个新的轨道索引。
3. 绝不在同一轨道上重叠两个剪辑 — linter 会失败，渲染结果不确定。

## 合成内的剪辑时间

`data-start` 以秒为单位，从_合成_的开始处测量。对于子合成，子合成的内部时间线（其自身的 `data-duration` 和子剪辑）从宿主的 `data-start` 到 `data-start + data-duration` 运行。

`data-media-start`（在 `<video>`/`<audio>` 上）是_进入源媒体_的偏移量。使用它可以跳过媒体文件的前几秒，而无需修剪文件本身。

## 相对计时

`data-start` 接受剪辑 ID 而不是数字，意思是"在该剪辑结束时开始"。添加 `+ N` / `- N` 来偏移；负数产生重叠（对交叉淡入淡出有用）。

```html
<video id="intro" data-start="0" data-duration="10" data-track-index="0" src="..."></video>
<video id="main" data-start="intro" data-duration="20" data-track-index="0" src="..."></video>
<video
  id="scene-a"
  data-start="intro + 2"
  data-duration="20"
  data-track-index="0"
  src="..."
></video>
<video
  id="scene-b"
  data-start="intro - 0.5"
  data-duration="20"
  data-track-index="1"
  src="..."
></video>
```

规则：

- 引用**仅在同一合成内**解析 — 不能进入父级或同级子合成。
- 被引用的剪辑必须有**已知时长**（显式 `data-duration` 或从媒体推断）。否则引用无法解析。
- **无循环引用** — `A → B → A` 被拒绝。检测到循环会报错。
- 解析为数字的值始终被视为绝对秒数。否则解析器期望 `<id>`、`<id> + <number>` 或 `<id> - <number>`（空格可选）。
- 引用可以链式（`A → B → C`）。保持链在 3-4 级以内以提高可读性。
- 负偏移产生重叠；重叠的剪辑必须在**不同轨道**上，同轨道重叠被拒绝。
