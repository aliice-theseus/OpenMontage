# 故事板格式 — `STORYBOARD.md` + 解析清单

仅定义故事板的**基础数据格式**：`STORYBOARD.md` 文件形状及其解析生成的 `StoryboardManifest`。工作流_如何生成_故事板存在于该工作流中；可选的解说词/TTS 文件（`SCRIPT.md`）是 TTS 步骤的独立关注点，不在此处。

故事板是视频的**计划层**——一个 markdown 文件中的有序**帧**（关键时刻）集合。HyperFrames Studio 将其渲染为缩略图索引（故事板视图，在 `VITE_STUDIO_ENABLE_STORYBOARD=1` 后面）。解析器：`@hyperframes/core/storyboard` → `StoryboardManifest`；读取 API：`GET /api/projects/<id>/storyboard`。

## Frontmatter（全局方向）

顶部的 YAML 块。未知键保存在 `globals.extra` 下。

| 键         | 含义           | 示例                                       |
| ---------- | -------------- | ------------------------------------------ |
| `format`   | 画布尺寸       | `1920x1080`                                |
| `message`  | 一句话主题     | `Ship a launch video in an afternoon`      |
| `arc`      | 叙事弧         | `Hook → Problem → Solution → Proof → CTA`  |
| `audience` | 目标受众       | `indie devs on X`                          |

## 每帧章节

每个帧一个 `## Frame N — Title` 标题（接受 `Frame` / `Beat` / `Scene` 在 H2/H3 级别）。元数据为 `- key: value` 列表；其下方直到下一个标题的内容为自由格式的**叙述**。

| 键              | 含义                                                                          |
| --------------- | ----------------------------------------------------------------------------- |
| `status`        | `outline` → `built` → `animated`（默认为 `outline`）                           |
| `src`           | 帧的 HTML 子合成相对于项目的路径（平铺海报从中渲染）                            |
| `duration`      | 例如 `4s`                                                                      |
| `transition_in` | `crossfade` / `cut` / `wipe` …（别名 `transition`）                             |
| `scene`         | 一行缩略图索引标题（别名 `description` / `summary` / `caption`）                |
| `voiceover`     | 帧的解说法_指南_（别名 `vo` / `voice_over` / `narration`）                      |
| `poster`        | 查找平铺海报的秒数（在开场动画之后）                                             |
| _任何其他键_     | 逐字保留在帧的 `extra` 中 — 工作流在此携带自己的逐帧数据（效果、资源等）          |

## 解析清单

解析器是**宽松的**：它永远不会抛出异常，并将任何意外内容记录为 `warning`。

```
StoryboardManifest {
  globals: { format?, message?, arc?, audience?, extra: {…} }
  frames: Array<{
    index, number?, title?,
    status,                       // "outline" | "built" | "animated"
    src?, duration? / durationSeconds?, transitionIn?,
    scene?, voiceover?, poster?,
    narrative,                    // 元数据下方的 markdown
    extra: {…}                    // 未知键，保留
  }>
  warnings: Array<{ message, line?, frameIndex? }>
}
```

读取 API 还会为每帧添加 `srcExists`，并在存在时附加可选的 `SCRIPT.md` 负载。

## `SCRIPT.md`（不在本文讨论范围内）

可选的、自由格式的、**未解析到清单中** — 驱动 TTS 的锁定解说词文件。其格式在 `references/script-format.md` 中定义，没有解说词/TTS 的视频不包含此文件。上面的逐帧 `voiceover` 是故事板自身的解说法指南。

## 示例

```markdown
---
format: 1920x1080
message: "Ship a launch video in an afternoon"
arc: Hook → Problem → Solution → Proof → CTA
audience: indie devs on X
---

## Frame 1 — Hook

- scene: Big type punches in on the beat
- duration: 3s
- poster: 2s
- transition_in: cut
- status: animated
- voiceover: "Ship a launch video in an afternoon."
- src: compositions/frames/01-hook.html

Open cold on the promise. This is the thesis — everything after pays it off.

## Frame 2 — The problem

- scene: A 20-minute timer spins on a stack of rejected takes
- duration: 4s
- transition_in: crossfade
- status: built
- voiceover: "The old way? Prompt, wait twenty minutes, get something that misses."
- src: compositions/frames/02-problem.html

The old way: prompt, wait, get something that misses. Establish the pain we remove.
```

## 注释

- `status: outline` 且没有构建的 `src` 的帧将渲染为大纲占位符。
- 多行 `voiceover` 值在保存时折叠为一行。
