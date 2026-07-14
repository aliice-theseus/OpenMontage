# 帧骨架（步骤 2）——读取音乐，布局帧

在步骤 2 **你（编排器）**读取 `audiomap.json` 并直接编写 `STORYBOARD.md` 的**骨架**：将曲目切割成**帧**（一帧 = 一个作品文件 = 一个场景），并为每帧设置其**跨度**、其**节奏**（此延伸段想要硬节拍剪切，还是平静的乐句/能量流？）、其**情绪**和一行**感觉**说明。

你**只分类和布局脊柱。** 你**不**选择模板、编写文案、选择颜色/字体或决定帧的组——那些是步骤 3（计划在原位填充每帧）。将每帧的 `### Groups` 留为 `TBD (Step 3)`，前置元数据 `style` 留空。

没有**中间 JSON**——骨架就是 `STORYBOARD.md` 的开始。步骤 3 编辑同一个文件。

## 信任边界（先阅读此内容）

`audiomap.json` 是一个分析器的输出。有些字段在任何**音乐**上都可靠；有些仅当音乐**真正有节奏**时才可靠。这决定每帧的 `pacing`：

| 字段 | 信任 |
| ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `energy_phases[]`（level / energy / density / feel）、`events[]` + `onset_rate`、`rolls[]`（及其**缺失**）、`silences[]`、`hard_stops[]`、`key_moments[]`、`phrases[]`、`audio.duration_sec` | **始终**——可靠的测量 |
| `tempo.bpm`、`grid.beats_sec` / `downbeats_sec` **精度** | **仅当音乐有节奏时。** 在平静/稀疏材料上，节拍网格是追踪器_强加_的节拍器（通常八度加倍）——通常**网格节拍多于真实起始点**。不要在那里将剪切锚定到它。 |

- **网格可靠**当：存在滚动段、和/或密集阶段、和/或高 `onset_rate` 带稳定网格。
- **网格虚构**当：`rolls`≈0、主要是 `sparse` 阶段、低 `onset_rate` → 按 `phrases[]` + `energy_phases[]` 定速，而不是节拍。

## 如何布局帧（按顺序运行）

1. **完形。** 从 `summary` / `tempo` / `audio.duration_sec` + 滚动段计数，编写前置元数据 `compositionId`、`duration_s`（== `audio.duration_sec`）、`canvas` 和一行曲目密度弧的阅读。
2. **切割成帧。** 遍历 `energy_phases[]` 并在音乐真正改变状态的地方分割——在 `hard_stops[]`、SURGE / DROP `key_moments`、`rolls[]` 运行的开始/结束、**起始沙漠**（`events[]` 中的长间隙）或大的能量水平跳跃处。合并在一个手势内的相邻阶段。预计**约 1–6 帧**；短剪辑可能只有一个。**将每个边界对齐到音频锚点**，然后仅在网格可靠时重新对齐到最近的 `beats_sec`（容差 ≤ ½ 节拍）；在平静材料上改为对齐到 `phrases[]` / `energy_phases[]` 边沿。帧**平铺曲目**（第一个在 0，最后一个在 `duration_s`，无间隙/重叠）。
3. **每帧设置 `pacing`**——信任边界调用：
   - **`beat_cut`**——真正有节奏：存在滚动段、**或**密集、**或**（明显高 `onset_rate` **且**稳定网格）。硬切/每次起始揭示可以锚定到节拍。
   - **`phrase_flow`**——平静/稀疏：`rolls`≈0、主要是稀疏、低 `onset_rate`。**不要**将硬切锚定到网格；按 `phrases[]` + 能量包络（慢交叉淡入淡出、长保持）定速。
4. **每帧标记 `mood`**（1–3 个：`warm` · `dark` · `hype` · `elegant` · `glitch` · `cinematic` · `playful` · `tense` · `dreamy` · `aggressive`）来自 `energy_phases[].feel` + 能量 + 简报/标题中的任何流派提示。
5. **每帧，写一行 `feel`**——步骤 3 对照模板匹配的纯语言音乐情况（例如「加速的起始流进入一个保持的强拍」、「平静的保持垫音，一个起始沙漠」、「快速持续填充滚动段，无可读消息」）。这是规划者对照目录的**适合时机**读取的内容——保持具体，来自可靠字段，永远不发明。

## 骨架的样子

有效的 `STORYBOARD.md`，脊柱已设置，每帧的处理方式留给步骤 3（完整语法在 [`storyboard-format.md`](storyboard-format.md)）：

```markdown
---
compositionId: bgm
duration_s: 30.0 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
style: # 空白——步骤 3 从所选 frame.md 预设填充
build_notes: ["每帧一个暂停的时间线", "无远程资源"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 7.198s # = 跨度长度；组装器求和以得到累积 data-start
- span_sec: [0.0, 7.198] # 曲目秒数；帧平铺曲目
- pacing: beat_cut
- mood: [hype]
- feel: 加速的起始流构建进入一个保持的强拍

### Groups

- TBD（步骤 3）

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 10.4s
- span_sec: [7.198, 17.598]
- pacing: phrase_flow
- mood: [warm, cinematic]
- feel: 平静的保持垫音，一个长起始沙漠

### Groups

- TBD（步骤 3）
```

## 自我检查

- `duration_s == audiomap.audio.duration_sec`；帧平铺曲目无间隙（第一个在 0，最后一个在 `duration_s`）。
- 每帧有 `src` + `span_sec` + `duration` + `pacing` + `mood` + 一行 `feel`。
- `pacing` 从**可靠**字段（energy / density / rolls / onset_rate）设置，从不仅仅来自 `bpm` / `beats_sec`。
- 没有帧边界在 `rolls[]` 运行内部或留下子-1-小节的碎片。
- 每帧的 `### Groups` 是 `TBD (Step 3)`；`style` 为空。**任何地方没有模板、文案、颜色或字体。**
