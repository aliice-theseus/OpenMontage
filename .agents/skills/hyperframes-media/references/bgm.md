# 背景音乐（BGM）

每部作品一个音乐底垫，由共享音频引擎（`scripts/audio.mjs` → `scripts/lib/bgm.mjs`）生成。两条路径，由引擎的一个开关决定——是否存在 HeyGen 凭证：

- **HeyGen 检索——有凭证时的默认方式。** 按情绪搜索 HeyGen 的音乐目录，下载最佳曲目。没有生成过程；与 TTS 使用相同的 `~/.heygen` / `$HEYGEN_API_KEY` 凭证。
- **本地生成（Lyria → MusicGen）——无凭证时的回退方式**（或当显式要求时）。从情绪提示生成 WAV。没有 `npx hyperframes bgm` 命令；引擎直接启动 `scripts/lyria-recipe.py` 或内联的 MusicGen 脚本。

> **首先运行预检——无凭证不是静默本地生成的绿灯。** 在生成之前，完成登录**预检**（参见 `../SKILL.md` → 预检）：运行 `npx hyperframes auth status`，建议登录，并**等待用户选择**（登录以使用 HeyGen 的音乐库，或离线继续使用本地生成）。这同样适用于单独的「生成 BGM」请求和完整工作流。

## 从请求驱动

`audio_request.json` → `bgm: { mode?, query?, prompt? }`：

- **`mode`**——`retrieve | generate | none`。省略则为**自动**（有凭证时检索，否则生成）。**显式** `retrieve` 是严格的：无凭证 ⇒ 跳过，绝不进行分离生成（因此没有 `wait-bgm` 步骤的调用方，例如产品发布，不会得到它不会等待的挂起任务）。
- **`query`**——情绪，用于检索和作为回退提示种子（例如故事板的 `music:` 字段，回退到 `message` → `arc` → `"calm cinematic underscore"`）。
- **`prompt`**——用于生成的显式完整提示；省略时引擎会推断一个（参见情绪推断）。可选的 `blob` / `archetype` / `arc` 提供推断输入。

## HeyGen 检索（默认）

`searchSounds(query, "music", { limit: 5 })` → `GET /audio/sounds?query=<mood>&type=music&limit=5`。取最佳结果（按 `score` 排序），下载其预签名的 `audio_url` → `assets/bgm/track.mp3`。同步。无匹配 → 跳过（BGM 是可选的；从不因它导致渲染失败）。提示写入 `audio_meta.json`：

```jsonc
{
  "path": "assets/bgm/track.mp3",
  "volume": 0.8,
  "mode": "retrieve",
  "query": "calm cinematic underscore",
  "duration_s": 42.0,
}
```

`volume` 在有叙述时为 0.8，无声电影（无语音）时为 0.9。`bgm_pending` 为 `false`——引擎返回时文件已在磁盘上。

## 本地生成（回退）——Lyria → MusicGen

以**分离**模式启动，这样语音工作不会被阻塞；设置 `audio_meta.bgm_pending: true` 和 `bgm_pid` / `bgm_log`，直到完成。**在组装前运行 `scripts/wait-bgm.mjs`**——它会轮询输出文件/进程/日志，检测崩溃，并写入 `bgm_status.json`（`status: ready | failed | timeout | disabled`）。失败/缺失的曲目直接省略；它从不阻塞语音/SFX。

| 顺序 | 提供商 | 环境变量/依赖 | 速度 | 质量 |
| ---- | ------------------------------------ | ------------------------------------------------------------------------------------- | --------------------------------------- | --------------------------- |
| 1 | Google Lyria RealTime | `$GEMINI_API_KEY` 或 `$GOOGLE_API_KEY` + `google-genai`（按需自动安装） | 实时流（≈ 请求时长） | 生产级 |
| 2 | MusicGen（`facebook/musicgen-small`） | Python `transformers + torch + soundfile + numpy`（首次运行约 300 MB；自动安装） | CPU 慢；Apple MPS / CUDA 快 | 尚可；仅提示控制 |

输出 → `assets/bgm/track.wav`，目标 = 总语音时长。MusicGen 生成**一个**种子片段（≤28–30s，受解码器的位置限制），然后交叉淡入淡出循环到目标时长（如果较短则裁剪），避免逐段接缝。后端选择基于实际能**运行**的：仅当 `import google.genai` 成功时使用 Lyria，否则使用 MusicGen；如果两者都无法运行，则跳过 BGM（语音 + SFX 仍然渲染）。

## 情绪推断（生成提示）

`scripts/lib/bgm.mjs` 中的 `inferBgmPrompt()`：显式 `prompt` 优先；否则行业关键词**基础** → 叙事**原型**形状 → 情感**弧**决胜器。

| `blob` / `query` 中的匹配 | 基础提示 | BPM |
| ------------------------------------------------------ | --------------------------------------------------------------------------- | --- |
| `crypto / nft / web3 / defi / token / blockchain` | 氛围电子乐，深沉低音，未来合成器，克制的打击乐 | 100 |
| `finance / fintech / bank / payment / invest / wealth` | 平静电影风，柔和的弦乐，微妙的钢琴，克制的打击乐 | 92 |
| `creative / agency / design / studio / art / brand` | 俏皮电子乐，温暖垫音，轻打击乐 | 115 |
| _（默认：SaaS / 科技 / 平台）_ | 振奋的企业科技风，明亮的现代钢琴配合成器垫音 | 108 |

原型然后重塑弧——PAS →「小调到大调」构建；BAB / 未来规划 → 进取上升；功能瀑布 → +10 BPM 驱动；演示循环 → −8 BPM 最小化。情感弧解决剩余分歧（紧张→缓解、兴奋、信任/安心）。

## Lyria 参数（直接配方使用）

引擎将 BPM / 音阶烘焙到**提示文本**中（通过上述推断），只传递 `--output` / `--duration` / `--prompt` 给配方。如果直接调用 `scripts/lyria-recipe.py`，还可以设置：`--bpm`（90–110 平静，110–130 充满活力）、`--brightness`（0–1，≥0.7 促销用）、`--density`（0–1，越高越丰满）、`--scale`（`MAJOR` / `MINOR` / `PENTATONIC` / ……）、`--negative-prompt`（要排除的风格）。MusicGen 忽略所有这些——把情绪放在提示中。

## 失败模式

| 失败 | 行为 |
| --------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 无音乐匹配（检索） | `bgm: null`，记录异常。渲染继续无 BGM。 |
| 显式 `retrieve`，无凭证 | 跳过（无静默生成回退）。使用 `mode: generate` 或省略 `mode` 以自动处理。 |
| Lyria 和 MusicGen 都无法运行（生成） | `bgm` 禁用，附带 `pip install …` 提示。语音 + SFX 仍然渲染。 |
| 组装时生成仍在渲染 | `bgm_pending: true`；`wait-bgm.mjs` 先等待/检查并写入 `bgm_status.json`。 |
| 生成崩溃 | `wait-bgm.mjs` → `bgm_status.json { status: "failed" }`；省略 `<audio>` 轨道。 |

BGM 失败从不阻塞渲染。
