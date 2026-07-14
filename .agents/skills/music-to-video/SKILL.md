---
name: music-to-video
description: "当用户有音乐曲目（音频文件、或要从中提取音频的视频）并想要一个节拍同步的 HyperFrames 视频时使用，从平静到强烈均可。音乐驱动一切：一个分析器读取一次，编排器布局帧并填充逐帧计划，一个子代理构建每帧。排版和模板是底线——完整视频不需要任何资源——但用户提供的任何图片或视频都会在同一节拍网格上（节拍剪切 / ken-burns）被切入帧中。类型（歌词视频、幻灯片、动能推广）从逐帧选择中得出；流水线从不分支。"
---

# music-to-video——一个音乐驱动、节拍同步的视频工作流

使用此技能将**音乐曲目**变成节拍同步的 HyperFrames 视频。你分析曲目一次，布局帧，填充逐帧计划，并将每帧构建为一个作品。输入是一个音乐曲目加上可选的用户图片或视频——**没有旁白，也没有网站捕获**。排版和模板是底线（完整视频不需要任何资源）；用户提供的任何媒体都会在同一节拍网格上被切入。

你是**编排器**。在 `videos/<project>/` 中工作。按顺序运行步骤，在继续之前通过每个**关卡**。两个步骤需要用户：**步骤 3**（计划批准）和**步骤 6**（渲染批准）。除了**步骤 4**（你分派**每个帧一个子代理**）外，自己做每一个步骤。将设计和动效规则留在此文件之外——它们位于 `references/` 和 `frame-worker` 子代理中。

`SKILL_DIR` = 此技能目录。`PROJECT_DIR` = `videos/<project-name>/`。

工作流：步骤 0 设置 → `hyperframes.json` + `assets/bgm.mp3`；步骤 1 分析 → `audiomap.json`；步骤 2 骨架 → `STORYBOARD.md`（帧、组 `待定`）；步骤 3 计划 → 完整的 `STORYBOARD.md` + `frame.md`；步骤 4 构建 → `compositions/frames/NN-*.html`；步骤 5 组装 → `index.html`；步骤 6 渲染 → `renders/video.mp4`。

## 塑造一切的两个想法

- **一个分析器，你信任它。** `analyze-beatgrid.py` 是唯一的节拍分析器——永远不要用另一个工具或凭耳朵重新测量节拍。它的 energy / density / rolls / onsets / silences 始终可靠。它的 `bpm` 和 `beats_sec` **仅当音乐真正有节奏时才可靠**；在平静的音乐上，网格是追踪器强加的节拍器，所以改用乐句和能量来定速，永远不要硬切到它。判断你处于哪种情况是每帧的 `pacing`（步骤 2）。
- **一帧 = 一个文件；组在内部存在。** 步骤 2 将曲目切割成**帧**，每帧成为一个作品文件 `compositions/frames/NN-<frame_id>.html`，由一个 frame-worker 构建。一帧可以细分为**组**（每个是一个模板或一个动效原语组合）。额外的密度放在组_内部_，因此**帧计数跟踪不同的处理方式，而不是节拍**——快速曲目不会增加子代理数量。

---

## 步骤 0：设置、BGM 和输入

目标：确定音乐源，创建 HyperFrames 项目，并记下任何用户提供的媒体。

**音乐是脊柱**——在做任何其他事情之前确定一个曲目。此技能针对**快速、高能量 BGM**进行了调整：强大的节拍网格驱动剪切（平静曲目也可以，但按乐句而不是节拍定速）。如果用户给了你音频——音乐文件或要提取音频的视频——使用它。如果没有，生成一个：从用户的描述中选择情绪（例如「驱动合成波」、「陷阱节拍」、「欢快企业」）并通过 `/hyperframes-media` 生成曲目（`references/bgm.md`——有凭证时使用 HeyGen 检索，否则本地 Lyria / MusicGen；ElevenLabs 或其他生成器也可以）。在生成之前，运行 `npx hyperframes auth status` 并**如实传递其输出（不要转述或重写）**——它显示 BGM 来自 HeyGen 还是本地 MusicGen，以及未登录时如何登录。**如果未登录，停止并等待用户选择——登录，或离线继续使用本地 MusicGen——然后再生成曲目**；不要将密钥写入每个仓库的 `.env`。（在自主模式下，记录状态并离线继续。）参见 `/hyperframes-media` → 预检了解规范指导。无论哪种方式，曲目都会放到 `assets/bgm.mp3`。暂存任何用户提供的图片或视频，以便帧可以在节拍网格上融入它们；否则排版承载整个视频。

仅在 `hyperframes.json` 缺失时初始化。从简报中以短横线命名法命名 `<project>`，例如 `midnight-drive-loop`——永远不要用时间戳。`init` 会检查已安装的技能与 GitHub 上的最新版本，并在任何技能过期时更新全局集。

```bash
npx hyperframes init "videos/<project>" --non-interactive --example=blank
mkdir -p "$PROJECT_DIR/assets" "$PROJECT_DIR/renders"
cp "<user-music>" "$PROJECT_DIR/assets/bgm.mp3"   # 如果需要，先从视频提取
# 仅当用户给了你图片/视频：
node <SKILL_DIR>/scripts/stage-assets.mjs --from <dir> --hyperframes "$PROJECT_DIR" --into public
```

**品牌**（字体 + 调色板）在步骤 3 选择，不在此处。不要预先选择流派或曲目类型——资源只是可选的配料，流派从逐帧选择中产生。

**关卡：** `hyperframes.json` + `assets/bgm.mp3` 存在；宽高比 / 长度 / fps 和（如果有）资源清单已记录。

---

## 步骤 1：分析音乐

目标：生成整个视频基于的单一规范时序分析。

`analyze-beatgrid.py` 是**唯一**的节拍分析器——永远不要用另一个工具或凭耳朵重新测量节拍。它读取曲目一次并写入 `audiomap.json`：能量阶段（level / density / feel）、起始点 + `onset_rate`、滚动段、静默段、`hard_stops`、`key_moments`、乐句、节奏 / 网格和 `audio.duration_sec`。它是确定性的——同一文件总是产生相同的映射。大多数字段在任何音乐上都可靠；`bpm` 和 `beats_sec` 仅当音乐真正有节奏时才可靠，而判断这一点是你在步骤 2 做出的决定。

先决条件：Python 3 附带可用的 `librosa`、`numpy` 和 `soundfile`。如果导入失败，在运行分析器之前将它们安装到活动的 Python 环境中：

```bash
python3 -m pip install librosa numpy soundfile
```

```bash
python3 <SKILL_DIR>/scripts/analyze-beatgrid.py "$PROJECT_DIR/assets/bgm.mp3" \
  -o "$PROJECT_DIR/audiomap.json" --print
```

**关卡：** `audiomap.json` 存在；`audio.duration_sec` 已知。

---

## 步骤 2：帧骨架（仅结构）

目标：读取音乐并布局帧——`STORYBOARD.md` 的骨架。

阅读 [`references/frame-skeleton.md`](references/frame-skeleton.md)。自己将 `audiomap.json` 变成 `STORYBOARD.md` 的**骨架**——没有中间 JSON。在真实的音乐变化处（`hard_stops`、SURGE / DROP `key_moments`、滚动段的边缘、没有起始点的延伸段、大的能量跳跃）将曲目切割成**帧**，将每个边界对齐到 audiomap 锚点。为每个帧设置 `span_sec`、`pacing`（来自步骤 1 信任调用的判定——当网格真实时用 `beat_cut`，当它是在平静音乐上强加的节拍器时用 `phrase_flow`）、`mood` 和一行 `feel`（步骤 3 对照模板匹配的纯文字音乐情况）。仅在此处分类和布局：将每帧的 `### Groups` 留为 `TBD (Step 3)`，前置元数据 `style` 留空——没有模板、文案、颜色或字体。预计约 1–6 帧。

**关卡：** 帧平铺曲目（第一个在 0，最后一个在 `duration_s`）；每个带有 `span_sec` + `pacing` + `mood` + `feel`；每个 `### Groups` 是 `TBD`；任何地方都没有内容。

---

## 步骤 3：填充计划（用户关卡）

目标：将骨架变成已批准的完整 `STORYBOARD.md`。

阅读 [`references/planning.md`](references/planning.md)、[`storyboard-format.md`](references/storyboard-format.md)、[`template-catalog.md`](references/template-catalog.md)、[`motion-primitive-catalog.md`](references/motion-primitive-catalog.md) 和 [`montage.md`](references/montage.md)（仅当用户提供了资源时）。原地编辑同一文件，做两件事：

1. **选择品牌。** 从 `../hyperframes-creative/frame-presets/` 中使用 `../hyperframes-creative/references/design-spec.md` 中的表选择一个预设（匹配曲目的情绪；**只有其字体和颜色重要**——模板拥有作品）。**未经修改**地复制到 `frame.md` 中，并从中填充前置元数据 `style`（字体 + ≤4–6 色板调色板）。
2. **填充每个帧。** 决定其组并为每个分配处理方式：从目录中匹配的模板（带绑定参数和真实音频锚点）、从原语目录自由组合、或**遵循 `pacing`** 的资源处理方式。编写文案。你拥有 WHAT（模板 / 原语 + 内容 + 锚点）；frame-worker 拥有 HOW——**永远不要将毫秒级动画写入故事板**。

```bash
node <SKILL_DIR>/scripts/validate-plan.mjs --storyboard "$PROJECT_DIR/STORYBOARD.md" \
  --audiomap "$PROJECT_DIR/audiomap.json" --templates <SKILL_DIR>/references/templates
```

修复每个 `✗`（硬错误：时长不匹配、帧未平铺曲目、缺少 `src`）；警告尽力而为。然后向用户显示逐帧摘要并迭代直到批准。

**关卡：** `frame.md` 是预设的逐字副本；`validate-plan.mjs` 退出 0；用户已批准计划。

---

## 步骤 4：从计划构建帧

目标：将每帧构建为自包含的作品文件。

创建 `compositions/frames/`。阅读 [`sub-agents/frame-worker.md`](sub-agents/frame-worker.md) 和 `../hyperframes-core/references/subagent-dispatch.md`。**每帧分派一个 frame-worker**，在可能的情况下并行（否则成波次）。每个 worker 精确得到一个帧和此上下文：

```text
PROJECT_DIR：<绝对路径>
frame_id：<NN-frame_id>              # = 帧文件干名称，例如 02-f2；作品 id
你的块：PROJECT_DIR/STORYBOARD.md 中的 `## Frame N — <frame_id>` 块
audiomap：PROJECT_DIR/audiomap.json
frame.md：PROJECT_DIR/frame.md
材料：对于每个组，<SKILL_DIR>/references/templates/<id>/index.html（模板）和
       <SKILL_DIR>/references/motion-primitives/<id>/（自由组合）；暂存的 assets/（资源组）
合约：../hyperframes-core/references/sub-compositions.md + determinism-rules.md
画布：<w>×<h>   节奏：<beat_cut|phrase_flow>
写入：PROJECT_DIR/compositions/frames/<frame_id>.html
```

Worker 分叉引用的材料，将每个锚点转换为帧本地秒数（`local_t = track_t − span_sec[0]`），使用 0ms 剪切门控其组，并写入一个可定位安全的帧文件。**Worker 从不运行 `hyperframes` CLI**——这些命令操作已组装的项目，该项目尚不存在，因此它们会报告错误的文件。Worker 只写入合约然后停止；你在组装后验证（步骤 6）。当每个 worker 返回时，你可以确认其文件已落地到磁盘。

**关卡：** 每个帧都有其 `compositions/frames/NN-*.html` 在磁盘上。

---

## 步骤 5：组装

目标：将构建的帧 + BGM 接入可播放的 `index.html`。

`assemble-index.mjs` 是确定性的——没有子代理，没有判断。它在其累积的 `data-start` 处引用每个帧文件，将 `assets/bgm.mp3` 挂载到轨道 11，并硬切帧 → 帧（帧平铺曲目无间隙，因此**没有过渡注入器**）。

```bash
node <SKILL_DIR>/scripts/assemble-index.mjs --storyboard "$PROJECT_DIR/STORYBOARD.md" \
  --hyperframes "$PROJECT_DIR" --audiomap "$PROJECT_DIR/audiomap.json"
```

修复它报告的每个 `✗`——缺失或空白的帧文件意味着该 worker 写了一个部分文件；重新分派它（步骤 4）并重新组装。

**关卡：** `index.html` 存在；总时长 == `audiomap.audio.duration_sec`。

---

## 步骤 6：验证和渲染

目标：验证组装的视频，获得用户批准，并渲染最终的 MP4。

在**已组装的项目**上运行 CLI——那是正确的单元（逐帧 workers 无法运行它）。`lint` 检查结构，`validate` 运行无头 Chrome（捕获 JS 错误和缺失资源），`inspect` 快照帧。

```bash
( cd "$PROJECT_DIR" && npx hyperframes lint . && npx hyperframes validate . && npx hyperframes inspect . )
```

在 `t=0`、每帧开始、最强的 DROP / SURGE、每个 `hard_stops[].t` 和最后一帧处检查。失败时，自己做出**最便宜的安全修复**：编辑有问题的 `compositions/frames/NN-*.html`。永远不要更改时长或音频时序来隐藏同步问题。一旦关卡通过，暂停供用户审核，然后仅在批准后渲染：

```bash
( cd "$PROJECT_DIR" && npx hyperframes render . --skill=music-to-video -q draft -o renders/video.mp4 --fps 30 )
```

**关卡：** `lint` / `validate` / `inspect` 通过；用户已批准；`renders/video.mp4` 存在带音频，时长 == `audiomap.audio.duration_sec`。最终回复说明 MP4 路径和时长。

---

## 恢复表

| 你拥有 | 从中继续 |
| -------------------------- | ------------- |
| 仅 `assets/bgm.mp3` | 步骤 1 |
| `audiomap.json` | 步骤 2 |
| `STORYBOARD.md`（骨架） | 步骤 3 |
| `STORYBOARD.md`（完整） | 步骤 4 |
| 所有帧文件 | 步骤 5 |
| `index.html` | 步骤 6 |

## 快速参考

**格式：** 横屏默认 `1920x1080`；竖屏 `1080x1920`；方形 `1080x1080`。在故事板前置元数据中设置画布一次（`canvas: { w, h, fps }`）。

**脚本**位于 `scripts/`：`analyze-beatgrid.py`（唯一分析器）、`validate-plan.mjs`（计划检查）、`assemble-index.mjs`（索引组装）、`stage-assets.mjs`（暂存用户媒体）、`lib/storyboard.mjs`（供应商解析器）。其他一切都是 `hyperframes` CLI。

| 阅读 | 何时 |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| [`references/frame-skeleton.md`](references/frame-skeleton.md) | 步骤 2：读取音乐，布局帧，设置节奏 |
| [`references/planning.md`](references/planning.md) · [`storyboard-format.md`](references/storyboard-format.md) | 步骤 3：选择品牌，填充每帧，编写计划 |
| [`references/template-catalog.md`](references/template-catalog.md) | 步骤 3：为每个组选择模板 |
| [`references/motion-primitive-catalog.md`](references/motion-primitive-catalog.md) | 步骤 3/4：自由组合的 L0 配方 |
| [`references/montage.md`](references/montage.md) | 步骤 3/4：资源处理方式（节拍剪切 / ken-burns） |
| [`sub-agents/frame-worker.md`](sub-agents/frame-worker.md) | 步骤 4：分派 + 构建一帧 |
| `../hyperframes-core/references/subagent-dispatch.md` | 步骤 4：安全分派子代理 |
| `../hyperframes-creative/references/design-spec.md` | 步骤 3：选择预设（品牌） |

## 目录布局

```
music-to-video/
  SKILL.md
  references/   frame-skeleton.md · planning.md · storyboard-format.md
                template-catalog.md · motion-primitive-catalog.md · montage.md
                templates/<id>/          { index.html (+ assets/ · program.json) }  ← L1 目录实现
                motion-primitives/<id>/  { index.html } (+ ../assets/gsap.min.js 配方共享) ← L0 目录实现
  scripts/      analyze-beatgrid.py · assemble-index.mjs · validate-plan.mjs · stage-assets.mjs · lib/storyboard.mjs
  sub-agents/   frame-worker.md   ← 唯一子代理（每帧一个）
```
