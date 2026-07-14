# 需求与缓存

## 凭证与密钥优先级

运行 `npx hyperframes auth status` 查看已配置的内容以及工作流将使用哪些引擎（参见技能的**预检**部分）。密钥按以下顺序解析——**第一个匹配的胜出**：

| 提供商 | 解析顺序（第一个非空胜出） | 使用时的本地依赖 |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **HeyGen**（TTS + BGM/SFX 检索） | `$HEYGEN_API_KEY` → `$HYPERFRAMES_API_KEY` → `~/.heygen/credentials`（与 heygen-cli 共享；`$HEYGEN_CONFIG_DIR` 可覆盖目录；由 `hyperframes auth login` 写入） | 无（REST） |
| **ElevenLabs**（TTS 备选） | `$ELEVENLABS_API_KEY` | `pip install elevenlabs` |
| **Lyria**（BGM 备选） | `$GEMINI_API_KEY` → `$GOOGLE_API_KEY` | `pip install google-genai` |
| **Kokoro**（TTS，无需密钥） | 始终可用——最终语音备选 | `pip install kokoro-onnx soundfile` |
| **MusicGen**（BGM，无需密钥） | 始终可用——最终音乐备选 | `pip install transformers torch soundfile numpy` |

`hyperframes auth login`（浏览器 OAuth）是推荐的设置方式：一次登录，所有项目，无需每个仓库的 `.env`。OAuth 登录作为 `Authorization: Bearer` 发送；API 密钥作为 `X-Api-Key` 发送。如果没有 HeyGen 凭证，语音/BGM 完全在本地运行（Kokoro / MusicGen）——`hyperframes auth status` 和 `hyperframes doctor` 都会报告这些本地依赖是否已安装。

## 模型缓存与系统依赖

每个命令在首次运行时下载自己的模型并缓存在 `~/.cache/hyperframes/` 下：

- **TTS（HeyGen）**——无本地依赖；需要 HeyGen 凭证 + PATH 上的 `ffmpeg`（用于将 mp3 响应转码为 `.wav`）。凭证解析方式与 CLI 相同：`$HEYGEN_API_KEY` → `$HYPERFRAMES_API_KEY` → `~/.heygen/credentials`（与 heygen-cli 共享；运行 `npx hyperframes auth login`）。OAuth 登录作为 `Authorization: Bearer` 发送；API 密钥作为 `X-Api-Key`。
- **TTS（ElevenLabs）**——与 HeyGen 相同：API 密钥 + `ffmpeg`。
- **TTS（Kokoro）**——Kokoro-82M（约 311 MB）+ 语音（约 27 MB）在 `tts/` 目录下。需要 Python 3.8+ 并安装 `kokoro-onnx` 和 `soundfile`（`pip install kokoro-onnx soundfile`）。非英语文本还需要系统级安装 `espeak-ng`。
- **BGM（Lyria）**——需要 `$GEMINI_API_KEY` 或 `$GOOGLE_API_KEY` + `pip install google-genai`。无本地模型缓存。
- **BGM（MusicGen）**——`pip install transformers torch soundfile`。`facebook/musicgen-small`（约 300 MB）首次运行时缓存到 `~/.cache/huggingface/` 下。
- **转录（Transcribe）**——Whisper 模型大小取决于选择（75 MB – 3.1 GB）在 `whisper/` 目录下。包含 `whisper.cpp`。
- **去除背景（Remove-background）**——`u2net_human_seg`（约 168 MB ONNX）在 `background-removal/models/` 目录下。峰值推理内存约 1.5 GB。

如果命令因缺少依赖而失败，运行 `npx hyperframes doctor`。
