# STORYBOARD.md 格式——帧 → 组

`STORYBOARD.md` 是用户在步骤 3 批准的单一可审核计划，也是每个 frame-worker 在步骤 4 遵循的**手册**。它是**分层级的**：每帧一个块，写为 `## Frame N — <frame_id>` 标题（解析器识别 `Frame`）。**一帧 = 一个场景 = 一个作品文件。** 在每个帧块内部是其**组**（处理单元）。组装器读取帧级别（`duration` → `data-start`、`src`）；worker 读取自己的帧块。帧的**作品 id = 其 `src` 文件干名**（`compositions/frames/01-f1.html` → `01-f1`），worker 将其用作 `data-composition-id` 和 `window.__timelines` 键。

步骤 2 编写骨架（帧字段，组 `TBD`）；步骤 3 填充组 + 品牌。它是一个构建规格，不是代码——规划者写 WHAT，worker 决定 HOW。**永远不要在此编写毫秒级动画。**

## 文件结构

YAML 前置元数据（视频范围的脊柱）+ 每帧一个 `## Frame N — <frame_id>` 块。

```markdown
---
compositionId: bgm
duration_s: 30.0 # == audiomap.audio.duration_sec，精确
canvas: { w: 1920, h: 1080, fps: 30 }
style: # 品牌脊柱——来自所选 frame.md 预设（步骤 3）
  font: "EB Garamond / Inter / JetBrains Mono" # 预设的排版，逐字
  palette: ["#FAF9F5", "#141413", "#CC785C", "#181715"] # 来自预设颜色的 ≤4–6 色板
assets: false # false，或像 "assets/ 有 6 张用户照片" 这样的说明
build_notes: ["每帧一个暂停的时间线", "无远程资源"]
avoid: ["通用幻灯片", "小到不可读的英雄文本"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html # worker 写入此处；组装器引用；干名（01-f1）= 作品 id
- duration: 7.198s # = 跨度长度；组装器读取此值以计算累积的 data-start
- span_sec: [0.0, 7.198] # 曲目秒数；帧平铺曲目
- pacing: beat_cut # beat_cut | phrase_flow（来自骨架；遵循它）
- mood: [hype]
- feel: 加速的起始流进入一个保持的强拍

### Groups

- **g1** — template: `intro-kinetic-cascade`
  - span_sec: [0.0, 4.017] # 帧本地构建是 0 基的；这些是曲目秒数（worker 减去帧开始）
  - params: { theme: "light", icon: "bolt", phrases: "[…]", climax: "{…}" }
  - role_bindings: { phrase: { times: [0.14, 0.55, 0.87] }, climax: { in: 3.79, iconAt: 4.9 } }
  - copy: "通过创造力成长"
- **g2** — free_design
  - span_sec: [4.017, 7.198]
  - free_design: { dominant_system: "每次起始排版", primitives: ["content-swap", "braam-punch"], density_topology: "accumulate" }
  - anchors: [4.10, 4.80, 5.50, 6.20] # 揭示依托的起始秒数（来自 audiomap）
  - copy: ["构建", "发布", "重复"]

## Frame 2 — f2

…
```

## 帧块——必需字段

| 字段 | 含义 |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 标题 `## Frame N — <frame_id>` | `frame_id` 匹配 `src` 干名；`N` = 基于 1 的索引。 |
| `src` | `compositions/frames/NN-<frame_id>.html`——worker 写入的位置；组装器引用它。干名 = `data-composition-id`。 |
| `duration` | 帧跨度长度（秒），例如 `7.198s`——**必需**；组装器将这些求和以得到累积的 `data-start`。 |
| `span_sec` | `[start, end]` 曲目秒数。`duration = end − start`。 |
| `pacing` | `beat_cut` | `phrase_flow`——来自骨架；worker 必须遵循（`phrase_flow` 上不能硬切）。 |
| `mood`、`feel` | 来自骨架；语调 + 规划者匹配的一行音乐情况。 |
| `### Groups` 列表 | ≥1 组；组按顺序平铺帧跨度。 |

## 组条目——三种类型之一

每个组是 **template** 或 **free_design** 或 **asset**——从不是两种，从不是无。全部三种都带有 `span_sec`（曲目秒数，平铺帧）并可以带有 `copy`。

- **template**——`template: <catalog id>` + `params`（来自目录条目的键）+ `role_bindings`（真实音频锚点秒数）+ `copy`。
- **free_design**——`free_design: { dominant_system, primitives: [catalog ids], density_topology }` + `anchors`（真实节拍/起始秒数）+ `copy`。
- **asset**——`asset: { treatment, clips: [public/…], anchors?, overlay_copy? }`。`treatment` ∈ `beat_cut`（每个锚点一个片段——仅当在 `beat_cut` 帧上）| `ken_burns`（慢推——适合 `phrase_flow`）| `bg_under_text`（在模板/自由组后面调暗的片段）。参见 [`montage.md`](montage.md)。

## 规则

- 帧平铺曲目（无间隙，第一个在 0，最后一个在 `duration_s`）；帧的组平铺其跨度；不允许组 < 约 1 小节；不允许组边界在 `rolls[]` 运行内部。
- `params` 键来自模板的 [`template-catalog.md`](template-catalog.md) 条目。
- 所有锚点秒数是来自 `audiomap.json` 的**曲目秒数**——worker 通过减去帧开始转换为帧本地时间。
- `phrase_flow` 帧**不能**使用 `beat_cut` 资源处理方式或每次起始硬切。
- 品牌 `style` 设置一次；每个组的调色板从中提取。
- 可审核的散文加数据；保持可扫描性。没有 GSAP，没有毫秒级时序。

## 自我检查（规划者运行 `validate-plan.mjs`）

- 前置元数据有 `compositionId`、`duration_s`（== audiomap）、`canvas`、`style`。
- 每个帧有 `span_sec` + `src` + 正 `duration` + `pacing` + ≥1 组；帧平铺曲目。
- 每个组正好是 template / free_design / asset 之一；模板 id 存在于目录中；锚点是真实的 audiomap 秒数；`phrase_flow` 帧没有 `beat_cut`。
