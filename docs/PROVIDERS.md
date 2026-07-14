# OpenMontage 提供商指南

关于 OpenMontage 中每个提供商你需要知道的一切——设置说明、定价、免费层级以及每个提供商解锁的功能。

---

## 快速开始：我应该设置什么？

**从免费开始，按需添加付费提供商。** 以下是推荐的顺序：

| 步骤 | 成本 | 设置内容 | 解锁功能 |
|------|------|---------|---------|
| 1 | **$0** | Pexels + Pixabay | 素材库照片和视频——足以制作基础视频 |
| 2 | **$0** | Google API 密钥 | TTS，700+ 种语音（每月 100 万字符免费）+ $300 新账户信用额度 |
| 3 | **$0** | ElevenLabs | 高级 TTS + 音乐 + 音效（每月 1 万字符免费） |
| 4 | **$0** | Piper（本地安装） | 完全离线 TTS——无需 API 密钥、无成本、无网络 |
| 5 | **~$0.03/张** | fal.ai | FLUX 图像 + Kling/Veo/MiniMax 视频 + Recraft——单密钥覆盖广泛的图像和视频 |
| 6 | **~$0.04/张** | OpenAI | DALL-E 3 图像 + OpenAI TTS |
| 7 | **~$0.04/张** | Google Imagen | Imagen 4 图像（与 Google API 密钥共享） |
| 8 | **$12/月** | Runway | Gen-4 视频——最高质量 AI 视频 |
| 9 | **按量付费** | HeyGen | 虚拟形象视频、多模型视频网关 |
| 10 | **按量付费** | Suno | 带人声和歌词的完整歌曲生成 |
| 11 | **$0 + GPU** | 本地视频生成 | WAN 2.1、Hunyuan、CogVideo、LTX——免费、离线 |
| 12 | **$0 + GPU** | 本地扩散模型 | Stable Diffusion 图像——免费、离线 |

### 环境变量汇总

```bash
# .env——在此添加你的密钥

# 免费（永远免费）
PEXELS_API_KEY=              # 素材库照片 + 视频
PIXABAY_API_KEY=             # 素材库照片 + 视频

# GOOGLE（一个密钥，两个工具，慷慨的免费层级）
GOOGLE_API_KEY=              # Google TTS + Google Imagen

# 语音 + 音乐
ELEVENLABS_API_KEY=          # TTS、音乐、音效（每月 1 万字符免费）
OPENAI_API_KEY=              # OpenAI TTS + DALL-E 3 图像
XAI_API_KEY=                 # xAI Grok 图像生成/编辑 + Grok 视频生成
DOUBAO_SPEECH_API_KEY=       # 火山引擎豆包语音 TTS（强大的普通话旁白）
DOUBAO_SPEECH_VOICE_TYPE=    # 默认豆包说话人/语音类型

# 多模型网关（一个密钥，6+ 个工具）
FAL_KEY=                     # FLUX、Recraft、Kling、Veo、MiniMax 视频

# 视频
HEYGEN_API_KEY=              # HeyGen 虚拟形象视频网关
RUNWAY_API_KEY=              # Runway Gen-4 视频（直连）
SUNO_API_KEY=                # Suno 音乐生成

# 本地（无需密钥——只需 GPU + 安装）
VIDEO_GEN_LOCAL_ENABLED=     # 设为 "true" 以启用本地视频生成
VIDEO_GEN_LOCAL_MODEL=       # wan2.1-1.3b、wan2.1-14b、hunyuan-1.5、ltx2-local、cogvideo-5b
```

---

## 云提供商

### xAI——Grok 图像 + 视频

> **如果你想要一个同时提供图像编辑和参考条件短视频的提供商，这是最佳选择。** Grok 在一个密钥下同时覆盖图像生成/编辑和视频生成。

**解锁的工具：** `grok_image`, `grok_video`
**环境变量：** `XAI_API_KEY`

#### 设置

1. 创建一个 xAI 开发者账户
2. 在 xAI 开发者控制台生成 API 密钥
3. 添加到 `.env`：`XAI_API_KEY=xai-...`

#### 最适合用于

- 图像编辑和风格迁移
- 将多张图像合成为一帧生成内容
- 需要人物、服装或产品动起来的短参考图像视频

#### 定价

当前 xAI 文档中 Grok 媒体模型的定价：

| 模型 | 价格 |
|------|------|
| `grok-imagine-image` | 每张生成图像 $0.02 |
| `grok-imagine-image` 输入图像（编辑/合成） | 每张输入图像 $0.002 |
| `grok-imagine-video` 480p | $0.05/秒 |
| `grok-imagine-video` 720p | $0.07/秒 |
| `grok-imagine-video` 输入图像 | 每张输入图像 $0.002 |

OpenMontage 现在在 Grok 工具估算器中使用这些已公布的价格。

---

### fal.ai——多模型网关

> **单密钥广泛覆盖。** 一个 API 密钥即可解锁跨多个模型的图像和视频提供商。

**解锁的工具：** `flux_image`, `recraft_image`, `kling_video`, `veo_video`, `minimax_video`
**环境变量：** `FAL_KEY`

#### 设置

1. 前往 [fal.ai](https://fal.ai/) 并点击**注册**（GitHub 或 Google）
2. 导航至 [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)
3. 点击**创建密钥**，复制它
4. 添加到 `.env`：`FAL_KEY=your-key-here`

#### 定价

无需订阅——纯按量付费，无最低消费。

**图像生成：**

| 模型 | 价格 | 每 $1 可生成 |
|------|------|-------------|
| FLUX Pro v1.1 | $0.05/张 | 20 张 |
| FLUX Dev | $0.03/张 | 33 张 |
| Recraft v3 | ~$0.04/张 | 25 张 |

**视频生成：**

| 模型 | 价格 | 每 $1 可生成 |
|------|------|-------------|
| Kling 2.5 Turbo Pro | $0.07/秒 | 14 秒 |
| MiniMax | ~$0.05/秒 | 20 秒 |
| Veo 3 | $0.40/秒 | 2.5 秒 |
| WAN 2.5 | $0.05/秒 | 20 秒 |

**免费层级：** 无——但 $0 即可开始，你只需为使用的部分付费。

---

### ElevenLabs——语音、音乐、音效

> **高级语音质量。** 对旁白密集型视频最佳的 TTS。还能生成音乐和音效。

**解锁的工具：** `elevenlabs_tts`, `music_gen`
**环境变量：** `ELEVENLABS_API_KEY`

#### 设置

1. 前往 [elevenlabs.io](https://elevenlabs.io) 并点击**注册**
2. 前往**个人资料**（左下角）> **API 密钥**，或访问 [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys)
3. 点击**创建 API 密钥**，命名，复制
4. 添加到 `.env`：`ELEVENLABS_API_KEY=xi_your-key-here`

#### 定价

| 套餐 | 价格 | 字符数/月 | 主要功能 |
|------|------|-----------|---------|
| **免费** | $0 | 10,000 | 3 个自定义语音、API 访问、需注明来源 |
| Starter | $5/月 | 30,000 | 无需注明来源 |
| Creator | $22/月 | 100,000 | 专业语音克隆 |
| Pro | $99/月 | 500,000 | 96kbps 音频、使用分析 |
| Scale | $330/月 | 2,000,000 | 优先支持 |

**免费层级：** 每月 10,000 字符（约 2-3 分钟旁白）。包含 API 访问。音乐生成和音效在免费层级也可用，但有限额。

---

### 豆包语音——普通话 TTS

> **强大的普通话旁白。** 火山引擎豆包语音是中文讲解配音和需要字幕时间元数据的长篇旁白的良好选择。

**解锁的工具：** `doubao_tts`
**环境变量：** `DOUBAO_SPEECH_API_KEY`, `DOUBAO_SPEECH_VOICE_TYPE`

#### 设置

1. 打开火山引擎豆包语音控制台，启用语音合成 2.0。
2. 创建一个新版控制台 API 密钥。
3. 选择 Speech 2.0 语音类型，例如 `zh_female_vv_uranus_bigtts`。
4. 添加到 `.env`：
   ```bash
   DOUBAO_SPEECH_API_KEY=your-api-key
   DOUBAO_SPEECH_VOICE_TYPE=zh_female_vv_uranus_bigtts
   ```

#### API 说明

OpenMontage 使用新版控制台 API 密钥流程：

```text
X-Api-Key: ${DOUBAO_SPEECH_API_KEY}
X-Api-Resource-Id: seed-tts-2.0
```

不要将新版控制台 API 密钥作为 `X-Api-App-Id` 或 `X-Api-Access-Key` 传递。这种不匹配可能导致 `load grant: requested grant not found`。

#### 最适合用于

- 中文讲解视频的自然普通话旁白
- 通过 `/api/v3/tts/submit` 和 `/api/v3/tts/query` 实现的异步长篇旁白
- 用于字幕对齐的字符级时间元数据
- 平静的教育节奏，视频时长可以跟随已批准的语音节奏

#### 节奏

从 `speech_rate: 0` 开始，获得自然的普通话表达。如果已批准格式需要更紧凑的时长，在生成完整旁白之前，比较 `speech_rate: 25` 或 `50` 的短样本。除非用户明确要求，否则不要强迫豆包匹配其他提供商的时长。

#### 定价

豆包语音 2.0 在火山引擎中按字符包或使用量计费。OpenMontage 根据文本长度估算成本，并在提供方返回使用元数据时优先使用。

---

### Google——TTS + Imagen（共享密钥）

> **一个密钥，两个工具。** Google Cloud TTS 拥有 50 多种语言的 700+ 种语音——最强的本地化选项。Imagen 4 生成高质量图像。

**解锁的工具：** `google_tts`, `google_imagen`
**环境变量：** `GOOGLE_API_KEY`

#### 设置

1. 前往 [Google AI Studio](https://aistudio.google.com/) 并登录
2. 导航至 [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
3. 点击**创建 API 密钥**，选择一个 Google Cloud 项目
4. 复制密钥
5. 添加到 `.env`：`GOOGLE_API_KEY=AIza...`

**对于 TTS 特定用途**，你还需要启用 Text-to-Speech API：
1. 访问 [console.cloud.google.com/apis/library/texttospeech.googleapis.com](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com)
2. 点击**启用**
3. 确保你的 API 密钥限制允许 Text-to-Speech API

**对于 Imagen**，启用 Generative Language API：
1. 访问 [console.cloud.google.com/apis/library/generativelanguage.googleapis.com](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com)
2. 点击**启用**

#### Google TTS 定价

| 语音类型 | 免费层级 | 付费（每百万字符） | 说明 |
|---------|---------|------------------|------|
| **Standard** | 每月 100 万字符 | $4.00 | 基础质量，快速 |
| **WaveNet** | 每月 100 万字符 | $16.00 | 自然听感 |
| **Neural2** | 每月 100 万字符 | $16.00 | 最佳质量 |
| **Studio** | — | $24.00 | 专业录音室语音 |
| **Chirp** | — | $4.00 | 对话风格 |

免费层级是*独立*计算的——你每月免费获得 100 万 Standard AND 100 万 WaveNet AND 100 万 Neural2 字符。相当于每月约 250+ 分钟的免费旁白。

#### Google Imagen 定价

| 模型 | 每张图像价格 |
|------|-------------|
| Imagen 4 Fast | $0.02 |
| Imagen 4 Standard | $0.04 |
| Imagen 4 Ultra | $0.06 |

**Imagen 免费层级：** 无。仅付费层级。

**新账户奖励：** Google Cloud 为新账户提供 **$300 免费信用额度**（90 天试用），适用于 TTS 和 Imagen。

#### Google TTS 语音类型

Google TTS 提供 50 多种语言的 700+ 种语音。语音名称遵循 `{language}-{type}-{letter}` 模式：

| 类型 | 示例 | 质量 | 成本 |
|------|------|------|------|
| **Chirp 3 HD** | `en-US-Chirp3-HD-Orus` | **最佳（2024 年，最自然）** | **中等——默认** |
| Standard | `en-US-Standard-A` | 良好 | 最便宜 |
| WaveNet | `en-US-WaveNet-D` | 很好 | 中等 |
| Neural2 | `en-US-Neural2-D` | 优秀 | 中等 |
| Studio | `en-US-Studio-O` | 专业 | 最高 |
| Journey | `en-US-Journey-D` | 对话式（长篇） | 中等 |

**推荐语音：** `en-US-Chirp3-HD-Orus`（男声，丰富/电影感），`en-US-Chirp3-HD-Aoede`（女声，温暖）。这些是 Google 最新层级——最自然的听感，自动使用 v1beta1 端点。

**支持的语言包括：** 英语（美国、英国、澳大利亚、印度）、西班牙语、法语、德语、意大利语、葡萄牙语、日语、韩语、中文（普通话、粤语）、阿拉伯语、印地语、俄语、荷兰语、波兰语、土耳其语、越南语、泰语、印尼语及 30 多种其他语言。

---

### OpenAI——TTS + 图像生成

> **扎实的全能选手。** DALL-E 3 擅长处理复杂的多元素构图。TTS 快速且实惠。

**解锁的工具：** `openai_tts`, `openai_image`
**环境变量：** `OPENAI_API_KEY`

#### 设置

1. 前往 [platform.openai.com/signup](https://platform.openai.com/signup) 并创建账户
2. 在 [platform.openai.com/account/billing](https://platform.openai.com/account/billing) 添加支付方式
3. 导航至 [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. 点击**创建新的密钥**，命名，复制
5. 添加到 `.env`：`OPENAI_API_KEY=sk-...`

#### TTS 定价

| 模型 | 每百万字符价格 |
|------|--------------|
| tts-1 | $15.00 |
| tts-1-hd | $30.00 |
| gpt-4o-mini-tts | $12.00 |

#### 图像定价

| 模型 | 尺寸 | 质量 | 每张图像价格 |
|------|------|------|-------------|
| DALL-E 3 | 1024x1024 | standard | $0.040 |
| DALL-E 3 | 1024x1024 | hd | $0.080 |
| DALL-E 3 | 1024x1792 | standard | $0.080 |
| DALL-E 3 | 1024x1792 | hd | $0.120 |

**免费层级：** 无。需要预付费账单。以前为新账户提供 $5 免费信用额度（大多数注册已停止）。

---

### Runway——Gen-3/Gen-4 视频

> **评分最高的 AI 视频质量。** Elo 排名第一。专业级视频生成，支持 Gen-3 Alpha Turbo、Gen-4 Turbo 和 Gen-4 Aleph 模型。

**解锁的工具：** `runway_video`
**环境变量：** `RUNWAY_API_KEY`

#### 设置

1. 前往 [dev.runwayml.com](https://dev.runwayml.com/) 并创建开发者账户
2. 订阅付费套餐（Standard 或以上——API 需要订阅）
3. 从开发者门户生成 API 密钥
4. 添加到 `.env`：`RUNWAY_API_KEY=key_...`

#### 定价

| 套餐 | 价格 | 信用额度/月 | 视频容量 |
|------|------|------------|---------|
| **免费** | $0 | 125（一次性） | Gen-4 约 5 秒 |
| Standard | $12/月 | 625 | Gen-4 约 25 秒 |
| Pro | $28/月 | 2,250 | Gen-4 约 90 秒 |
| Unlimited | $76/月 | 无限（探索模式） | Gen-4 Turbo 无限 |

**API 定价（约）：**

| 模型 | 每秒价格 |
|------|---------|
| Gen-3 Alpha Turbo | ~$0.05 |
| Gen-4 Turbo | ~$0.05 |
| Gen-4 Aleph | ~$0.15 |

**免费层级：** 125 一次性信用额度（无月度续费）。足够生成约 5 秒的 Gen-4 视频。API 访问需要付费订阅。

---

### Higgsfield——多模型视频编排器

> **多模型视频平台。** 通过单个 API 路由到 Kling 3.0、Veo 3.1、Sora 2、WAN 2.5 和专有 Soul Cinema。包括用于跨片段角色一致性的 Soul ID。

**解锁的工具：** `higgsfield_video`
**环境变量：** `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET`（或组合 `HIGGSFIELD_KEY=key:secret`）

#### 设置

1. 前往 [cloud.higgsfield.ai](https://cloud.higgsfield.ai/) 并创建账户
2. 订阅套餐（Starter 或以上以获得 API 访问）
3. 导航至 [cloud.higgsfield.ai/api-keys](https://cloud.higgsfield.ai/api-keys) 的 API 密钥部分
4. 生成 API 密钥和密钥
5. 添加到 `.env`：
   ```
   HIGGSFIELD_API_KEY=your-api-key
   HIGGSFIELD_API_SECRET=your-api-secret
   ```

#### 定价

| 套餐 | 价格 | 说明 |
|------|------|------|
| 免费 | $0 | 有限信用额度 |
| Starter | $15/月 | 基本配额 |
| Plus | $34/月 | 中端，约 33-56 个 Kling 3.0 片段 |
| Ultra | $84/月 | 高容量 |

**每次生成成本（约，通过信用额度）：**

| 模型 | 每片段成本 |
|------|----------|
| Kling 3.0 | ~$0.10（最便宜） |
| WAN 2.5 | ~$0.10 |
| Soul Cinema | ~$0.15 |
| Veo 3.1 | ~$0.50 |
| Sora 2 | ~$0.50 |

**免费层级：** 注册时有限信用额度。免费套餐无月度续费。

---

### HeyGen——虚拟形象视频网关

> **多模型视频网关。** 通过单个 API 访问 VEO、Sora、Runway、Kling 和 Seedance。

**解锁的工具：** `heygen_video`
**环境变量：** `HEYGEN_API_KEY`

#### 设置

1. 前往 [app.heygen.com/register](https://app.heygen.com/register) 并创建账户
2. 导航至设置中的 API 部分
3. 生成你的 API 密钥
4. 添加 API 余额（预付费，与 Web 套餐信用额度分开）
5. 添加到 `.env`：`HEYGEN_API_KEY=your-key-here`

#### 定价

| 服务 | 价格 |
|------|------|
| 虚拟形象视频（Engine III） | $0.017/秒 |
| 虚拟形象视频（Engine IV） | $0.10/秒 |
| 提示词转视频 | $0.033/秒 |
| 视频翻译（快速） | $0.05/秒 |
| 视频翻译（精确） | $0.10/秒 |

**Web 套餐：**

| 套餐 | 价格 | 说明 |
|------|------|------|
| 免费 | $0 | 1 信用额度（演示） |
| Creator | $24/月 | 有限信用额度 |
| Business | $72/月 | API 访问，更多信用额度 |

**免费层级：** Web 平台 1 信用额度。API 是基于预付费余额的按量付费。

---

### Suno——AI 音乐生成

> **带人声和歌词的完整歌曲。** 任意风格，最长 8 分钟。纯音乐或人声曲目。

**解锁的工具：** `suno_music`
**环境变量：** `SUNO_API_KEY`

#### 设置

1. 前往 [suno.com](https://suno.com) 并创建 Suno 账户
2. 对于 API 访问，前往 [sunoapi.org](https://sunoapi.org) 并创建账户
3. 导航至仪表盘并复制你的 API 密钥
4. 添加信用额度（1 信用额度 = $0.005 USD）
5. 添加到 `.env`：`SUNO_API_KEY=your-key-here`

#### 定价

**Suno 平台：**

| 套餐 | 价格 | 信用额度 | 说明 |
|------|------|---------|------|
| 免费 | $0 | 50/天 | 约 10 首歌曲/天，仅非商业用途 |
| Pro | $10/月 | 2,500/月 | 商业许可证 |
| Premier | $30/月 | 10,000/月 | 商业许可证 |

**API（通过 sunoapi.org）：** 按量付费，1 信用额度 = $0.005。每次生成产生 2 首曲目。

---

### Pexels——免费素材库媒体

> **完全免费。** 无需成本、无需注明来源、允许商业使用。

**解锁的工具：** `pexels_image`, `pexels_video`
**环境变量：** `PEXELS_API_KEY`

#### 设置

1. 前往 [pexels.com/join](https://www.pexels.com/join/) 并创建免费账户
2. 导航至 [pexels.com/api](https://www.pexels.com/api/)
3. 点击**你的 API 密钥**或请求 API 访问
4. 从仪表盘复制你的密钥
5. 添加到 `.env`：`PEXELS_API_KEY=your-key-here`

#### 定价

**完全免费。** 无付费层级。无需注明来源。允许商业使用。

- 200 次请求/小时
- 20,000 次请求/月
- 照片和视频搜索 + 下载

---

### Pixabay——免费素材库媒体

> **完全免费。** 500 万+ 免版税图像和视频。

**解锁的工具：** `pixabay_image`, `pixabay_video`
**环境变量：** `PIXABAY_API_KEY`

#### 设置

1. 前往 [pixabay.com/accounts/register](https://pixabay.com/accounts/register/) 并创建免费账户
2. 导航至 [pixabay.com/api/docs](https://pixabay.com/api/docs/)
3. 你的 API 密钥显示在文档页面顶部（登录后）
4. 复制密钥
5. 添加到 `.env`：`PIXABAY_API_KEY=your-key-here`

#### 定价

**完全免费。** 无付费层级。无需注明来源。允许商业使用。

- 约 100 次请求/分钟
- 5,000 次请求/小时
- 照片和视频搜索 + 下载
- 标准 API 限制为 1280px 图像（全分辨率需要编辑 API）

---

## 本地提供商（免费，无需 API 密钥）

这些提供商完全在你自己的机器上运行。无需网络、无需 API 密钥、无需成本。部分需要 GPU。

### Remotion——程序化视频合成

> **基于 React 的视频渲染。** 将静态图像转换为动画视频，支持弹簧物理、动画文字卡片、统计卡片、图表和转场。**这是当没有配置视频生成提供商时的关键回退方案**——代理生成图像，Remotion 将它们动画化为专业外观的视频。

**工具：** `video_compose`（使用 `operation="render"`——在需要时自动路由到 Remotion）
**运行时：** CPU（需要 Node.js）
**环境变量：** 无

#### 设置

```bash
# 包含在 make setup 中，或手动安装：
cd remotion-composer && npm install && cd ..
```

需要 **Node.js 18+** 和 `npx`。`remotion-composer/` 项目包含在仓库中。

#### Remotion 渲染的内容

| 组件 | 产生的内容 |
|------|----------|
| **TextCard** | 带有弹簧物理进入动画的动画标题/正文文本 |
| **StatCard** | 带计数动画的动画统计数字 |
| **ProgressBar** | 动画进度指示器 |
| **CalloutBox** | 带图标动画的高亮标注面板 |
| **ComparisonCard** | 并排比较布局 |
| **BarChart / LineChart / PieChart** | 动画数据可视化 |
| **KPIGrid** | 多指标仪表盘卡片 |
| **图像场景** | 带弹簧动画运动的静态图像（替代 Ken Burns 效果） |

#### Remotion 何时激活？

`video_compose` 工具的 `render` 操作自动检测何时需要 Remotion：
- 剪辑包含静态图像（`.png`, `.jpg` 等）
- 剪辑的 `type` 设置为 `text_card`、`stat_card`、`chart` 等
- 剪辑指定了 `animation` 或 `transition_in`/`transition_out`

如果未安装 Remotion，合成会回退到 FFmpeg Ken Burns 平移和缩放——能用但吸引力较低。

**成本：** 免费。始终本地运行。

---

### HyperFrames——HTML/CSS/GSAP 视频合成

> **GSAP 原生本地渲染。** HyperFrames 是运动图形密集型 HTML 合成以及 `character-animation` 流水线的骨骼化 SVG 角色表演的首选运行时。

**工具：** 直接使用 `hyperframes_compose`，或使用 `edit_decisions.render_runtime="hyperframes"` 的 `video_compose`
**运行时：** CPU（需要 Node.js >= 22、FFmpeg 和 `npx`）
**环境变量：** 无

#### 设置

```bash
node --version
ffmpeg -version
npx --yes hyperframes doctor
```

CLI 通过 `npx hyperframes` 使用。不要使用 `npx @hyperframes/cli`；该包名不是 OpenMontage 运行时路径。

#### HyperFrames 渲染的内容

| 用例 | 产生的内容 |
|------|----------|
| **动态文字** | 由 GSAP 时间线驱动的 HTML/CSS 文本动画 |
| **产品/发布视频** | 结构化 HTML 场景、注册表块和转场 |
| **网站转视频** | 浏览器捕获的网站合成，经过 HyperFrames 验证 |
| **角色动画** | SVG 角色骨骼、姿势/动作时间线和 GSAP 表演节拍，渲染到 `renders/final.mp4` |

HyperFrames 工作区位于 `projects/<project-name>/hyperframes/`。最终视频仍然遵循标准的 OpenMontage 约定：`projects/<project-name>/renders/final.mp4`。

**成本：** 免费。始终本地运行。

---

### Piper TTS——离线文本转语音

> **完全免费、完全离线的 TTS。** 无需网络。适用于草稿和预算受限项目的良好质量。

**工具：** `piper_tts`
**运行时：** CPU（无需 GPU）
**环境变量：** 无

#### 设置

```bash
# 通过 pip 安装
pip install piper-tts

# 或从 GitHub 下载二进制文件
# https://github.com/rhasspy/piper/releases

# 下载语音模型（首次运行自动下载）
piper --download-dir ~/.piper/models --model en_US-lessac-medium
```

**可用语音：** 约 30 种英语语音，以及德语、法语、西班牙语、意大利语和其他语言的语音。种类比云提供商少，但完全免费且离线。

**质量：** 适合草稿、内部视频和预算项目。对于面向客户的旁白，使用 ElevenLabs 或 Google TTS。

---

### 本地视频生成（需要 GPU）

> **免费 AI 视频生成。** 需要具有足够 VRAM 的 NVIDIA GPU。

**工具：** `wan_video`, `hunyuan_video`, `cogvideo_video`, `ltx_video_local`
**运行时：** 本地 GPU（需要 CUDA）
**环境变量：** `VIDEO_GEN_LOCAL_ENABLED=true`, `VIDEO_GEN_LOCAL_MODEL=<model>`

#### 设置

```bash
# 1. 安装 GPU 栈
make install-gpu
# 或手动安装：
pip install diffusers transformers accelerate torch pillow requests

# 2. 在 .env 中启用本地生成
VIDEO_GEN_LOCAL_ENABLED=true

# 3. 根据你的 GPU VRAM 选择模型
VIDEO_GEN_LOCAL_MODEL=wan2.1-1.3b      # 6GB+ VRAM（入门级）
VIDEO_GEN_LOCAL_MODEL=wan2.1-14b       # 24GB+ VRAM（最佳本地质量）
VIDEO_GEN_LOCAL_MODEL=hunyuan-1.5      # 12GB+ VRAM
VIDEO_GEN_LOCAL_MODEL=ltx2-local       # 8GB+ VRAM（最快）
VIDEO_GEN_LOCAL_MODEL=cogvideo-5b      # 10GB+ VRAM
VIDEO_GEN_LOCAL_MODEL=cogvideo-2b      # 6GB+ VRAM（最轻量）
```

#### 模型比较

| 模型 | VRAM | 质量 | 速度 | 最适合 |
|------|------|------|------|--------|
| **WAN 2.1（1.3B）** | 6GB | 良好 | 快 | 入门级 GPU，快速迭代 |
| **WAN 2.1（14B）** | 24GB | 优秀 | 慢 | 最佳质量与 VRAM 比 |
| **Hunyuan 1.5** | 12GB | 很好 | 中等 | 中端 GPU |
| **LTX-2** | 8GB | 良好 | 最快 | 快速草稿，最低延迟 |
| **CogVideo（5B）** | 10GB | 良好 | 中等 | 均衡选择 |
| **CogVideo（2B）** | 6GB | 一般 | 快 | 低 VRAM 实验 |

**所有本地模型支持：** 图生视频、文生视频、离线生成、种子可复现性。

---

### 本地扩散模型——离线图像生成（需要 GPU）

> **免费的 Stable Diffusion 图像生成。** 无 API 成本，完全离线。

**工具：** `local_diffusion`
**运行时：** 本地 GPU（需要 CUDA）
**环境变量：** 无（通过安装依赖启用）

#### 设置

```bash
pip install diffusers transformers accelerate torch
```

首次运行下载模型（约 4GB）。后续运行使用缓存的模型。

**VRAM 需求：** 4GB+（建议 8GB 用于 1024x1024 图像）

**支持：** 负向提示词、种子、自定义尺寸。质量低于 FLUX 或 DALL-E 3，但完全免费且离线。

---

### Modal 上的 LTX-2——自托管云 GPU

> **在 Modal 的云 GPU 上运行 LTX-2。** 你自己的端点，你自己的规模。比本地 GPU 更稳定，比商业 API 更便宜。

**工具：** `ltx_video_modal`
**运行时：** 云端（自托管）
**环境变量：** `MODAL_LTX2_ENDPOINT_URL`

#### 设置

1. 创建 [Modal](https://modal.com) 账户
2. 部署 LTX-2 端点（参见 Modal 文档）
3. 在 `.env` 中设置端点 URL：`MODAL_LTX2_ENDPOINT_URL=https://your-modal-endpoint`

**Modal 定价：** A100 GPU 时间约 $0.99/小时。每个视频的成本取决于生成时间。

---

### 其他本地工具（始终可用）

这些工具仅需要 FFmpeg 或 Python 包——无需 GPU、无需 API 密钥。

| 工具 | 安装 | 功能 |
|------|------|------|
| **FFmpeg 工具**（video_compose, video_stitch, video_trimmer, audio_mixer, audio_enhance, color_grade, face_enhance, frame_sampler, scene_detect） | `brew install ffmpeg` / `sudo apt install ffmpeg` / `winget install FFmpeg` | 视频编辑、音频处理、调色、分析 |
| **Transcriber** | `pip install faster-whisper` | 带词级时间戳的语音转文本 |
| **背景移除** | `pip install rembg`（CPU）或 `pip install rembg[gpu]` | 移除图像/视频背景 |
| **放大** | `pip install realesrgan`（需要 PyTorch + CUDA） | Real-ESRGAN 图像/视频放大 |
| **人脸修复** | `pip install gfpgan`（需要 PyTorch） | CodeFormer/GFPGAN 人脸修复 |
| **代码片段** | `pip install Pygments Pillow` | 语法高亮代码图像 |
| **图表生成** | `npm install -g @mermaid-js/mermaid-cli` | Mermaid 图表渲染 |
| **数学动画** | `pip install manim` | ManimCE 数学动画 |
| **字幕生成** | 无需安装 | SRT/VTT 字幕文件生成 |
| **视频理解** | `pip install transformers torch` | CLIP/BLIP-2 视觉分析 |
| **虚拟形象** | 克隆 [SadTalker](https://github.com/OpenTalker/SadTalker) | 从照片 + 音频创建虚拟形象动画 |
| **唇形同步** | 克隆 [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) | 音频驱动的唇形同步 |

---

## 提供商到工具的映射

| 提供商 | 环境变量 | 解锁的工具 | 成本 |
|--------|---------|-----------|------|
| **Pexels** | `PEXELS_API_KEY` | `pexels_image`, `pexels_video` | 免费 |
| **Pixabay** | `PIXABAY_API_KEY` | `pixabay_image`, `pixabay_video` | 免费 |
| **Piper** | —（仅安装） | `piper_tts` | 免费 |
| **Google** | `GOOGLE_API_KEY` | `google_tts`, `google_imagen` | 免费层级 + 付费 |
| **ElevenLabs** | `ELEVENLABS_API_KEY` | `elevenlabs_tts`, `music_gen` | 免费层级 + 付费 |
| **fal.ai** | `FAL_KEY` | `flux_image`, `recraft_image`, `kling_video`, `veo_video`, `minimax_video` | 按量付费 |
| **OpenAI** | `OPENAI_API_KEY` | `openai_tts`, `openai_image` | 仅付费 |
| **xAI** | `XAI_API_KEY` | `grok_image`, `grok_video` | 仅付费 |
| **Runway** | `RUNWAY_API_KEY` | `runway_video` | 免费试用 + 付费 |
| **Higgsfield** | `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` | `higgsfield_video` | 订阅（$15-84/月） |
| **HeyGen** | `HEYGEN_API_KEY` | `heygen_video` | 按量付费 |
| **Suno** | `SUNO_API_KEY` | `suno_music` | 按量付费 |
| **本地 GPU** | `VIDEO_GEN_LOCAL_ENABLED` | `wan_video`, `hunyuan_video`, `cogvideo_video`, `ltx_video_local` | 免费（需要 GPU） |
| **本地扩散模型** | —（仅安装） | `local_diffusion` | 免费（需要 GPU） |
| **Modal** | `MODAL_LTX2_ENDPOINT_URL` | `ltx_video_modal` | 自托管云端 |

---

## 能力覆盖范围

每个能力有多少提供商覆盖：

| 能力 | 云提供商 | 本地提供商 | 免费选项 |
|------|---------|-----------|---------|
| **图像生成** | FLUX、Grok、Google Imagen、DALL-E 3、Recraft | 本地扩散模型 | Pexels、Pixabay（素材库） |
| **视频生成** | Grok、Kling、Runway、Veo、Higgsfield、MiniMax、HeyGen | WAN、Hunyuan、CogVideo、LTX | Pexels、Pixabay（素材库） |
| **文本转语音** | ElevenLabs、Google TTS、OpenAI | Piper | Piper、Google 免费层级、ElevenLabs 免费层级 |
| **音乐生成** | ElevenLabs、Suno | — | ElevenLabs 免费层级 |
| **后期制作** | — | FFmpeg（合成、拼接、裁剪、混音、增强、调色） | 全部免费 |
| **分析** | — | WhisperX、场景检测、帧采样器、CLIP/BLIP-2 | 全部免费 |
| **增强** | — | 放大、背景移除、人脸增强、人脸修复 | 全部免费 |
| **虚拟形象** | — | SadTalker、Wav2Lip | 全部免费 |

---

## 常见问题

**问：制作视频所需的最低配置是什么？**
答：FFmpeg + Node.js（均免费、本地运行）。FFmpeg 处理视频组装、音频混音和字幕。配合 Node.js，Remotion 将静态图像渲染为动画视频——因此即使没有任何视频生成 API，代理也能生成图像，Remotion 将它们转化成带有弹簧动画、文字卡片和转场的专业外观视频。添加 Piper TTS 获取免费旁白，Pexels/Pixabay 获取免费素材库素材。

**问：我没有配置任何视频生成提供商。还能制作视频吗？**
答：可以。代理生成静态图像（通过任何图像提供商——甚至来自 Pexels/Pixabay 的免费素材库素材），Remotion 将它们合成为带有弹簧物理转场、文字卡片、统计卡片和图表的动画视频。当没有配置视频生成时，这是讲解和动画流水线的默认路径。

**问：获取 AI 生成的图像和视频有什么低门槛的方法？**
答：fal.ai（`FAL_KEY`）是一个按量付费选项，单密钥覆盖广泛。它解锁 FLUX 图像以及多个视频提供商。无需订阅——只为你生成的内容付费。

**问：我有 GPU。本地可以免费运行什么？**
答：设置 `VIDEO_GEN_LOCAL_ENABLED=true` 并安装 `diffusers`。你将获得 WAN 2.1、Hunyuan、CogVideo 和 LTX 视频生成，以及 Stable Diffusion 图像生成——全部免费，全部离线。

**问：应该使用哪个 TTS 提供商？**
答：追求质量 → ElevenLabs。追求本地化（50+ 语言）→ Google TTS。追求预算 → Google 免费层级（每月 100 万字符）。追求离线 → Piper。

**问：我需要所有这些提供商吗？**
答：不需要。从你已有的开始。选择器模式自动路由到任何可用的方案。缺少某个提供商？系统会自动回退到下一个。
