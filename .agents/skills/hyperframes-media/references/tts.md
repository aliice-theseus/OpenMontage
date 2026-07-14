# 文字转语音（TTS）

`npx hyperframes tts` 从环境变量自动检测提供商；可通过 `--provider` 显式覆盖。

> **首先运行预检——无凭证不是静默使用本地语音的绿灯。** 在生成配音之前，完成登录**预检**（参见 `../SKILL.md` → 预检）：运行 `npx hyperframes auth status`，建议登录，并**等待用户选择**（登录以使用 HeyGen 语音，或离线继续使用本地 Kokoro）。这同样适用于单独的「生成配音」请求和完整工作流。

## 提供商链

| 顺序 | 提供商 | 环境变量触发 | 语音 ID | 词语时间戳 | 音频格式 |
| ---- | ----------------- | ------------------------------------------- | ------------------------------------------- | ----------------------------------------- | -------------------- |
| 1 | HeyGen（Starfish） | `$HEYGEN_API_KEY` / `~/.heygen/credentials` | 来自 `GET /v3/voices?engine=starfish` 的 UUID | **是**（响应中的 `word_timestamps[]`） | mp3 → 通过 ffmpeg 转 wav |
| 2 | ElevenLabs | `$ELEVENLABS_API_KEY` | 来自 elevenlabs.io 仪表板的 UUID | 否 | mp3 → 通过 ffmpeg 转 wav |
| 3 | Kokoro-82M | 始终可用（本地备选） | `am_michael`、`af_heart`……（54 个语音） | 否 | 直接 wav |

```bash
# 自动检测（设置了密钥则用 HeyGen，否则 ElevenLabs，否则 Kokoro）
npx hyperframes tts "欢迎使用 HyperFrames" -o narration.wav

# 显式指定提供商
npx hyperframes tts "你好" --provider kokoro
npx hyperframes tts "你好" --provider heygen --voice <heygen-uuid>
npx hyperframes tts "你好" --provider elevenlabs --voice 21m00Tcm4TlvDq8ikWAM

# HeyGen 路径：一次调用捕获词语时间戳（跳过 Whisper 步骤）
npx hyperframes tts "你好" --words narration.words.json
```

## 独立的 HeyGen（无需 CLI）——`scripts/heygen-tts.mjs`

已发布的 `hyperframes tts` CLI 仅使用 Kokoro 在本地合成。当您
专门需要 HeyGen——最佳质量**加上**一次调用获取词语时间戳——请使用
此技能附带的脚本，它直接调用 HeyGen v3 REST API，无需
CLI 提供商管道：

该脚本以与 CLI 相同的方式解析 HeyGen 凭证——第一个来源
胜出：`$HEYGEN_API_KEY` → `$HYPERFRAMES_API_KEY` → 项目 `.env`（自动加载，
向上搜索最多 5 层目录）→ `~/.heygen/credentials`（与 heygen-cli 共享；
`$HEYGEN_CONFIG_DIR` 覆盖目录）。OAuth 登录作为
`Authorization: Bearer` 发送；API 密钥作为 `X-Api-Key` 发送。如果唯一的凭证是
过期的 OAuth 令牌，它会停止并提示运行 `npx hyperframes auth refresh`。

```bash
# 仅在尚未运行 `npx hyperframes auth login` 时需要：
export HEYGEN_API_KEY=...   # 或将其放在项目 .env 中

# 一次调用合成 + 捕获词语时间戳（跳过 Whisper 步骤）
node skills/hyperframes-media/scripts/heygen-tts.mjs \
  "欢迎使用 HyperFrames。" -o narration.wav --words narration.words.json

node skills/hyperframes-media/scripts/heygen-tts.mjs ./script.txt -o narration.wav
node skills/hyperframes-media/scripts/heygen-tts.mjs --list   # 列出公共 starfish 语音
```

- **语音：** `--voice <id>` 必须是 **starfish** voice_id（`--list`，或 `GET /v3/voices?engine=starfish`）。v2 目录的 ID 会返回 HTTP 400 错误。省略 `--voice`（英语）则默认为 **Marcia**（`05f19352e8f74b0392a8f411eba40de1`，这是一个固定的默认值，使选择具有确定性）。非英语且未指定 `--voice` 则回退到目录中第一个匹配的语音。
- **输出：** `.wav` → 通过 ffmpeg 转码为 44.1k 单声道；`.mp3` → 原始字节（无需 ffmpeg）。
- **词语：** `--words <path>` 写入下面的扁平 `[{id,text,start,end}]` 格式，可直接用于字幕流水线。HeyGen 的 `<start>`/`<end>` 边界标记被过滤掉，ID 重新连续编号。
- **非英语：** `--lang <code>`（除 `en` 外的任何值）作为请求的 `language` 发送。

## 何时使用哪个提供商

| 目标 | 使用 |
| --------------------------------------------------------- | --------------------------------------------------- |
| 一次调用获得最佳语音质量 + 词语时间戳 | **HeyGen** |
| 即插即用的云端 TTS，庞大的语音目录 | **ElevenLabs** |
| 离线，无需 API 密钥，快速迭代 | **Kokoro** |
| 非英语多语言，确定性音素化 | **Kokoro**（`ef_dora`、`jf_alpha`、`zf_xiaobei`……） |

## 表现性配音约定

在生成配音之前，编写一个简洁的语音表演计划：

- `performance_intent`——叙述者是谁以及他们应该有什么感觉
- `pacing_profile`——沉思的、对话式的、充满活力的、技术性的或自定义的
- `energy_curve`——朗读在整段内容中的变化方式
- `pause_policy`——哪些地方应该有静默以及为什么
- 段落级提示——`pace`、`energy`、`emphasis_words`、`pause_before_seconds`、
  `pause_after_seconds` 以及可选的提供商就绪文本

不要依赖像「让它自然」这样模糊的指示。将方向放在
文本或提供商设置中：

- 使用短句和有目的性的标点符号。
- 当所选提供商支持 SSML 风格的 break 标签时，使用 `<break time="0.4s"/>` 到 `<break time="1.0s"/>` 来实现重要停顿。
- 在批量生成之前，先从对表演最敏感的部分生成一个样本。
- 如果样本听起来单调、急促或忽略了停顿，在生成其余部分之前修改计划或提供商设置。

## ffmpeg 要求

HeyGen + ElevenLabs 返回 mp3。当 `--output` 以 `.wav` 结尾时（这是默认设置，也是下游 `ffprobe` + Whisper 所期望的），CLI 会转码为 wav。如果您希望跳过转码，传递 `-o file.mp3`。如果 PATH 上没有 `ffmpeg`，云端提供商的 `.wav` 输出将失败——请安装 ffmpeg 或使用 `.mp3`。

## 语音选择（Kokoro）

默认 `af_heart`。精选推荐：

| 内容类型 | 语音 |
| ----------------- | ---------------------- |
| 产品演示 | `af_heart`、`af_nova` |
| 教程/操作指南 | `am_adam`、`bf_emma` |
| 营销/推广 | `af_sky`、`am_michael` |
| 文档 | `bf_emma`、`bm_george` |
| 休闲/社交 | `af_heart`、`af_sky` |

运行 `npx hyperframes tts --list` 查看捆绑的语音集。

## 多语言（Kokoro 语音前缀 → 语言）

Kokoro 语音 ID 的第一个字母决定了音素化器语言；`--lang` 可覆盖自动检测。

| 前缀 | 语言 |
| ------ | -------------------- |
| `a` | 美式英语 |
| `b` | 英式英语 |
| `e` | 西班牙语 |
| `f` | 法语 |
| `h` | 印地语 |
| `i` | 意大利语 |
| `j` | 日语 |
| `p` | 巴西葡萄牙语 |
| `z` | 普通话 |

```bash
npx hyperframes tts "La reunión empieza a las nueve" --voice ef_dora --provider kokoro
npx hyperframes tts "今天是个好天气" --voice af_heart --provider kokoro
```

有效的 `--lang` 代码（仅在需要覆盖语音的自动检测语言时使用）：`en-us`、`en-gb`、`es`、`fr-fr`、`hi`、`it`、`pt-br`、`ja`、`zh`。

非英语音素化需要系统级安装 `espeak-ng`（`brew install espeak-ng` / `apt-get install espeak-ng`）。

## 速度

- `0.7-0.8`——教程、复杂内容、无障碍
- `1.0`——自然语速（默认）
- `1.1-1.2`——开场白、过渡、 upbeat 内容
- `1.5+`——很少适用，请谨慎测试

Kokoro + HeyGen 支持速度设置；ElevenLabs 忽略 `--speed`（在其仪表板的语音设置中调整）。

## 长脚本

超过几段文字后，将文本写入 `.txt` 文件并传递路径。超过约 5 分钟语音的输入可能适合拆分为多个段落。

## HeyGen 词语时间戳格式

当向 HeyGen 调用传递 `--words <path>` 时，文件以与 `transcribe` 生成的相同的扁平格式写入——可直接与字幕流水线兼容：

```json
[
  { "id": "w0", "text": "嗨", "start": 0.0, "end": 0.21 },
  { "id": "w1", "text": "你好", "start": 0.22, "end": 0.55 }
]
```

对于 ElevenLabs / Kokoro，运行 `npx hyperframes transcribe narration.wav --model small.en` 以获得相同格式。
