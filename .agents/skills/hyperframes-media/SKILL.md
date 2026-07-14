---
name: hyperframes-media
description: HyperFrames 作品的音频和媒体资源，由共享的音频引擎（`scripts/audio.mjs`）生成——支持多提供商 TTS（HeyGen / ElevenLabs / Kokoro 本地）、背景音乐 + 音效（默认使用 HeyGen 音频库检索，本地 Lyria / MusicGen 生成 BGM，以及内置 SFX 库作为无凭证时的备选）、Whisper 转录、背景去除和字幕制作。用于配音 / TTS、BGM、SFX / 音效、转录、字幕 / 子标题 / 歌词 / 卡拉 OK / 逐词样式、语音 + 提供商选择以及音乐情绪提示。
---

# HyperFrames Media

创建作品所需的音频和媒体资源——配音（TTS）、背景音乐 + 音效、转录、字幕、背景去除——然后在 HTML 中消费和动画化这些数据。如需将资源放入作品中，请参阅 `hyperframes-core`。

## 音频引擎——TTS · BGM · SFX 的统一来源

工作流**不要**手动处理音频或复制脚本。有一个统一的引擎——**`scripts/audio.mjs`**——它接收中立的 `audio_request.json` 并输出 `audio_meta.json`（以及 `assets/voice|bgm|sfx` 下的资源）：

```bash
# <MEDIA_DIR> = 此技能的目录
node <MEDIA_DIR>/scripts/audio.mjs --request ./audio_request.json --hyperframes . --out ./audio_meta.json
```

所有三种能力取决于**一个开关**——是否存在 HeyGen 凭证（通过 `$HEYGEN_API_KEY` / `$HYPERFRAMES_API_KEY` / `~/.heygen` 解析，**不是** CLI）：

| 能力 | 存在 HeyGen 凭证 | 无凭证 |
| ------- | -------------------------------------------------- | ---------------------------------------------------- |
| TTS | HeyGen Starfish REST（原生词语时间戳） | → ElevenLabs → Kokoro（链式 `transcribe` 获取词语） |
| BGM | HeyGen 音乐**检索** | Lyria → MusicGen 本地**生成**（分离模式） |
| SFX | HeyGen 音效**检索**（min_score 0.4） | 内置的 21 个文件库（`assets/sfx/`） |

- **请求**（`audio_request.json`）：`{ provider?, lang?, speed?, lines: [{ id, text, sfx?: [names] }], bgm: { mode?, query?, prompt? } }`。`id` 将每一行连接回调用方的模型（帧号、场景 ID 等）。`bgm.mode` = `retrieve | generate | none`；省略则为自动（有凭证时检索，否则生成）。**显式** `retrieve` 是严格的——它会跳过而不是启动分离生成（适用于没有 `wait-bgm` 步骤的调用方）。
- **输出**（`audio_meta.json`，以 ID 为键）：`{ tts_provider, voice_id, bgm, bgm_pending, …, voices: [{ id, path, duration_s, words }], sfx: [{ id, name, file, source, offset_s, duration_s, volume }], total_duration_s }`。
- `--only tts,bgm,sfx` 运行子集并**合并**到现有的 `--out` 中（例如先 TTS+BGM，等提示确定后再加 SFX）。
- BGM 生成以**分离**模式启动（`bgm_pending: true`）——在组装前运行 `scripts/wait-bgm.mjs`。
- `scripts/heygen-tts.mjs` 是基于相同代码的单次 CLI（一段文本 → wav + 词语），适用于只需 HeyGen TTS 而不需要请求文件的情况。

完整标志列表和 `audio_meta.json` 的结构定义见 `scripts/audio.mjs` 头部注释。下面的参考资料涵盖了每种能力背后的提供商细节和边界情况。

## 预检——在任何音频生成前显示登录状态

**在生成语音或 BGM 之前务必运行此操作——无论是在完整工作流中还是单独的「给我生成 BGM/配音」请求。** 没有 HeyGen 凭证**不是**静默回退到本地引擎的理由：首先建议登录并让用户决定。运行共享预检并**如实传递其输出**——不要自行编造「缺少密钥」提示，也不要提议将密钥写入每个仓库的 `.env`：

```bash
npx hyperframes auth status
```

- **已登录** → 显示账户信息；继续执行。
- **未登录**（此处 `exit 1` 是预期的——「未登录」是正常状态，不是失败）→ 显示注册优先的指引。建议登录：`npx hyperframes auth login` 是浏览器 OAuth——它会**登录并创建账户**（始终可通过此仓库的 CLI 使用）。如果想使用现有的 HeyGen API 密钥（来自 app.heygen.com/settings/api），运行 `npx hyperframes auth login --api-key`——它会保存到共享的 `~/.heygen`（不创建每个仓库的 `.env`）。输出还会列出语音/BGM 将回退到的本地引擎，以及缺少依赖时的 `pip` 提示。**如实传递此输出——不要用自己的话转述。** 然后**停止并等待**用户选择——登录，或说「继续」/「本地」以离线继续——**然后再生成任何内容。** 这是一个真正的决策点，不是路过备注：不要把它合并到另一个问题中，也不要自行越过它。（例外：在自主/非交互模式下，记录状态并离线继续。）
- `npx hyperframes auth status --json` 返回 `{ configured, recommended_action, offline_engines }` 用于确定性分支。
- **如果 CLI 无法运行**（不在 PATH 上且 `npx` 无法获取）→ 仍然**建议登录**（`npx hyperframes auth login`）并**等待用户选择**——不要将「无凭证」视为静默进行本地生成的绿灯。

凭证解析、完整密钥优先级和本地依赖列表见 `references/requirements.md`。

## 提供商链（引擎背后的细节）

**TTS**——第一个可用的提供商胜出（引擎，或 `npx hyperframes tts "..."`）：

| 顺序 | 提供商 | 检测条件 | 词语时间戳 |
| ---- | ----------------------------- | -------------------------------------------- | ---------------------------------------------------------------- |
| 1 | HeyGen（Starfish） | `$HEYGEN_API_KEY` / `hyperframes auth login` | **是，原生**——传递 `--words narration.words.json` 以捕获 |
| 2 | ElevenLabs | 设置了 `$ELEVENLABS_API_KEY` | 否——之后链式 `transcribe` |
| 3 | Kokoro-82M（本地，54 个语音） | 始终可用（无需密钥） | 否——之后链式 `transcribe` |

> 已发布的 `hyperframes tts` CLI 通常是仅本地的构建版本（其 `--help` 显示「Kokoro-82M」，没有 `--provider`/`--words`），即使设置了 `$HEYGEN_API_KEY` 也会静默回退到 Kokoro。这就是为什么引擎的 HeyGen 路径是独立的 `scripts/heygen-tts.mjs`（REST），而不是 CLI；CLI 仅用于 Kokoro 路径。参见 `references/tts.md`。

**BGM & SFX**——默认从 HeyGen 音频库**检索**（`/v3/audio/sounds`），与 HeyGen TTS 使用相同的凭证，无凭证时使用上述开关的备选：

| 资源 | HeyGen `type` | 存放位置 | 备选（无凭证） |
| ----- | ------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| BGM | `music` | `assets/bgm/track.mp3`（检索）· `track.wav`（生成） | Lyria / MusicGen 生成 |
| SFX | `sound_effects`（min_score 0.4） | `assets/sfx/<slug>.mp3` | 内置的 21 个文件库（`assets/sfx/*` + `manifest.json`） |

参见 `references/bgm.md` 和 `references/sfx.md`。

## 路由

| 任务 | 阅读 |
| ------------------------------------------------------------------- | -------------------------------------------- |
| 音频引擎——请求/元数据结构、`--only`、开关 | `scripts/audio.mjs`（头部注释） |
| `npx hyperframes tts` / `heygen-tts.mjs`——提供商、语音、词语 | `references/tts.md` |
| BGM——HeyGen 检索 + 本地 Lyria / MusicGen 生成 | `references/bgm.md` |
| SFX——HeyGen 检索（min_score 0.4）+ 内置本地库 | `references/sfx.md` |
| `npx hyperframes transcribe`——Whisper、模型规则、输出格式 | `references/transcribe.md` |
| `npx hyperframes remove-background`——透明抠图 | `references/remove-background.md` |
| TTS → 转录 → 字幕（无录制配音） | `references/tts-to-captions.md` |
| 字幕制作——样式检测、布局、词语分组、退出 | `references/captions/authoring.md` |
| 转录处理——输入格式、质量门控、清理、API | `references/captions/transcript-handling.md` |
| 字幕动画——卡拉 OK、标记效果、音频响应 | `references/captions/motion.md` |
| 模型缓存、系统依赖、故障排除 | `references/requirements.md` |

## 不可协商的规则

- **一个引擎，没有复制版。** 通过 `scripts/audio.mjs`（或单次 HeyGen TTS 的 `heygen-tts.mjs`）生成音频。不要在工作流中重新实现 TTS/BGM/SFX——编写 `audio_request.json` 适配器并调用引擎。
- **「HeyGen 可用」= 可解析的凭证，而不是 CLI。** 整个开关以 `heygenCredential()` 为关键；发布的 `hyperframes tts` 可能仅支持 Kokoro，并且根本没有 `hyperframes bgm` / `hyperframes sfx` 命令。
- **语音 ID 是提供商特定的。** `am_michael` 仅适用于 Kokoro；HeyGen UUID 在 Kokoro 上不起作用。如果传递 `--voice`，也要指定 `--provider`，以避免用户环境变化时提供商标识静默漂移。
- **始终向 `transcribe` 传递 `--model`。** CLI 默认的 `small.en` 会静默翻译非英语音频。参见 `references/transcribe.md` →「语言规则」。
- **HeyGen 返回词语时间戳；ElevenLabs / Kokoro 不返回。** 引擎会自动为后两者链式 `transcribe`；独立使用时，向 HeyGen 传递 `--words` 或对音频文件运行 `transcribe`。
- **字幕消费扁平的词语数组格式**，包含 `{ id, text, start, end }`。参见 `references/transcribe.md` →「输出格式」。
- **`remove-background --background-output` 是挖孔，不是修复。** 对于「没有人的场景」，需要不同的工具。参见 `references/remove-background.md` →「何时不是正确的工具」。
- **BGM/SFX 默认使用 HeyGen 检索；无凭证时回退到生成（BGM）或内置库（SFX）。** `/audio/sounds` 按文本查询排序——具体命名效果（`glass shatter`，而不是 `dramatic sound`）；无匹配则**跳过**，从不阻塞渲染。SFX 在语音 + BGM 下的音量约为 0.35。参见 `references/sfx.md` / `references/bgm.md`。
- **将工作流字幕 HTML 视为生成输出。** 对于基于预设的视频，可重用皮肤源位于 `.hyperframes/caption-skin.html`，工作流脚本写入 `compositions/captions.html`；不要编辑生成的 `compositions/captions.html` 来修复皮肤。通过工作流的 `captions.mjs` 重建，或在其存在时使用该工作流的显式覆盖机制。
