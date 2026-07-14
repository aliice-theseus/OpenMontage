# 步骤 4：配音、时序 + 字幕

## 如果步骤 2 说「无旁白」

跳过下面的 TTS 部分。故事板已经基于节奏和速度规划了节拍时长——这些将直接成为步骤 5 中的 `data-start` 和 `data-duration` 值。

**背景音乐：** 在进入步骤 5 之前询问用户：

> 「你有这个视频的音乐曲目吗？如果没有，我可以建议在哪里找到：
>
> - **Artlist.io** 或 **Musicbed**——用于商业用途的授权音乐
> - **Uppbeat.io** 或 **Pixabay Music**——带署名的免费曲目
> - **Freesound.org**——免费样本和循环
>
> 或者分享一个参考曲目（「像这样的」），我可以找到类似的东西。」

如果用户提供了曲目：在故事板中记下文件路径和 BPM，供步骤 5 在 `index.html` 中连接。如果他们完全跳过音乐，视频仅使用 SFX——确认这是有意为之。

进入步骤 5。

---

## 在完整旁白之前生成测试片段——先校准时序

**现在**使用脚本的开场行生成一个 2 句话的测试片段。测量实际时长。Kokoro 将脚本压缩约 40%（规划的 35s → 实际 19s），HeyGen 运行得比预期快。如果你发现音频比预期短 40%，你需要在投资时间进行完整旁白生成之前修改故事板节拍时序。

**在提交到节拍数和时长之前执行此操作：**

```bash
# 快速 Kokoro 测试（2 句话）：
npx hyperframes tts "第一句话。第二句话。" --voice af_nova --output /tmp/test-tts.wav
# 测量：秒数 ÷ 词数 × 脚本总词数 = 估计的完整音频长度
```

如果估计值将你的视频放在规划时长的 ±15% 以内，继续。如果偏差超过 15%，首先重新校准脚本长度：

- **音频太短**（比规划时长短超过 15%）→ 添加策略性停顿。在 `narration.txt` 中，在段落之间插入空行（每个约 0.6s）或在句子之间插入 `...`（每个约 0.4s）。目标是让停顿落在故事板节拍边界上，使静默感觉有意而非空白。
- **音频太长**（比规划时长长超过 15%）→ 确定故事板中词语密度最高的节拍。从那**个**节拍的行中删除一个支持句——保留前导句（命名节拍想法的那个）。在提交完整生成之前，用另一个测试片段重新测量。
- **音频匹配计划但节拍边界漂移** → 调整故事板时长以匹配实际旁白，而不是反过来。一旦旁白生成，音频就是地面实况。

脚本公式假设恒定的词/秒速度，但标点、戏剧性停顿和静默提示都会拉伸实际音频。始终相信测量的测试片段而不是公式。

## 背景音乐

**始终询问背景音乐**——即使有旁白：

> 「你想要旁白下的背景音乐吗？（Artlist.io、Musicbed 用于授权；Uppbeat/Pixabay 用于免费；或分享参考曲目）。即使是微妙的氛围背景音也能让句子之间的停顿感觉有意而非空洞。」

如果他们想要音乐，在故事板中记下曲目，供步骤 5 在 `index.html` 中连接。

## TTS 提供商

询问用户他们希望使用哪个语音提供商：

> **你想使用哪个语音提供商进行旁白？**
>
> 1. **HeyGen TTS**——良好的语音质量，自动返回词语级时间戳（省去单独的转录步骤）。需要 HeyGen API 密钥。
> 2. **ElevenLabs**——庞大的语音库，非常自然的输出。需要 ElevenLabs API 密钥。不返回词语时间戳——需要单独转录。
> 3. **Kokoro（免费）**——本地运行，无需 API 密钥。质量尚可，但比其他选项更像机器人。适合草稿或预算运行。

如果用户选择 ElevenLabs 或 HeyGen 但尚未设置密钥，帮助他们：

- **ElevenLabs：**「将 `ELEVENLABS_API_KEY=your-key` 添加到项目根目录的 `.env` 文件中，或直接粘贴到此处，我会设置它。」
- **HeyGen：**「将 `HEYGEN_API_KEY=your-key` 添加到 `.env` 文件，或粘贴到此处。」

不要评判或批评用户是否直接在聊天中粘贴密钥——直接使用并继续。

## 试听语音

在提供商选定后，使用 SCRIPT.md 的第一句话试听至少 2 个语音。

**ElevenLabs：**

- 如果 ElevenLabs MCP 可用：使用 `mcp__elevenlabs__search_voices` 浏览，`mcp__elevenlabs__text_to_speech` 生成。
- 如果没有 MCP：直接调用 REST API：

  ```bash
  # 列出语音
  curl -s "https://api.elevenlabs.io/v1/voices" \
    -H "xi-api-key: $ELEVENLABS_API_KEY" | jq '.voices[:5] | .[].name'

  # 生成语音（将 VOICE_ID 替换为选定的语音）
  curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID" \
    -H "xi-api-key: $ELEVENLABS_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"text":"你脚本的第一句话","model_id":"eleven_multilingual_v2"}' \
    --output narration.mp3
  ```

- 不返回词语时间戳——生成后单独转录。

**HeyGen TTS：**

- 如果 HeyGen MCP 可用：直接使用 TTS 工具。
- 如果没有 MCP：使用 v3 API（当前版本；v1/v2 已弃用，支持到 2026 年 10 月）。**认证取决于凭证类型：** 下面的 `x-api-key` 头仅对**账户 API 密钥**（`HEYGEN_API_KEY`）有效。如果你通过 **OAuth** 认证（例如 claude.ai / HeyGen MCP 登录），`x-api-key` 会返回 401——改为发送 `Authorization: Bearer $HEYGEN_OAUTH_TOKEN`，或直接使用上述 MCP TTS 工具。

  ```bash
  # 列出语音——响应格式：{ "data": [...], "has_more": bool }
  # data 是直接列表（不是 data.voices——那是 v2）
  curl -s "https://api.heygen.com/v3/voices?engine=starfish&type=public&limit=20" \
    -H "x-api-key: $HEYGEN_API_KEY" | python3 -c \
    "import json,sys; v=json.load(sys.stdin)['data']; [print(x['voice_id'], x['name'], x['language']) for x in v[:10]]"

  # 生成音频——响应：{ "data": { "audio_url": ..., "word_timestamps": [...] } }
  curl -s -X POST "https://api.heygen.com/v3/voices/speech" \
    -H "x-api-key: $HEYGEN_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"text":"你的脚本在此","voice_id":"VOICE_ID","speed":1.0}' \
    | python3 -c "
  import json,sys
  r=json.load(sys.stdin)
  d=r['data']
  print(d['audio_url'])
  open('transcript_raw.json','w').write(json.dumps(d.get('word_timestamps',[]),indent=2))
  "

  # 然后下载音频
  curl -sL "来自上方的 AUDIO_URL" --output narration.mp3
  ```

- 直接在响应中返回词语级时间戳——无需单独的转录步骤。

**Kokoro（免费，本地）：**

```bash
npx hyperframes tts SCRIPT.md --voice af_nova --output narration.wav
```

无需 API 密钥，无需 MCP。本地运行。使用 `--list` 查看所有 54 个可用语音。

选择听起来最自然和会话式的语音。听节奏——它在句子之间呼吸吗？听起来像人还是机器人？

## 脚本长度检查

在生成之前，验证脚本对视频有意义。词数完全取决于创意方向。故事板的节奏和风格决定视频需要多少旁白。

关键检查：是否有连续的地方**没有什么在发生**——没有旁白也没有引人注目的视觉运动？这些是失去观众的死点。每一秒要么需要口语词，要么需要强大的视觉能量来承载。

## 生成完整旁白

将完整脚本生成为项目目录中的 `narration.wav`（或 `.mp3`）。

**如果任何命令挂起超过 60 秒——不要只是等待。** 用户坐在那里看着你什么都不做。升级顺序：

1. **再试一次**——杀死进程，再次运行同一命令（瞬时故障很常见）
2. **尝试不同的标志**——更小的模型（`--model tiny.en`）、不同的语音、先用短的测试句
3. **尝试用于同一任务的不同工具**——如果 `hyperframes transcribe` 挂起，直接对音频运行 `whisper-cli`
4. **完全切换提供商**——如果 ElevenLabs 宕机，尝试 HeyGen 或 Kokoro。如果 Kokoro 挂起，尝试 ElevenLabs。

永远不要闲坐 10 分钟希望一个卡住的进程会完成。

**Kokoro 发音问题：** Kokoro 会错误发音产品名称和技术术语。在生成之前始终应用替换。已知问题和修复：

- `API` → `A P I`（拼写出来）
- `UI` → `U I`、`SaaS` → `sass`、`DevOps` → `dev ops`
- 拼写不寻常的产品名称：先测试第一句并听。常见失败：「Vercel」→「versatile」、「WorkOS」→「work O S」、「One API」→「Wanna PI」
- 如果名称听起来不对：在 `narration.txt` 中按发音写（例如 `Vercel` → `Ver-sell`、`Supabase` → `Soopa-base`）
- 始终先生成包含前 2 句话的短测试片段，然后再生成完整音频
- **没有 SSML 标签**——Kokoro 会将其作为字面文本读取。`<break time="1s"/>` 会被读作「break time equals one slash。」在 `narration.txt` 中使用空行或 `...` 表示停顿

对于 ElevenLabs 和 HeyGen TTS，替换通常不需要——它们正确处理产品名称。

**同时保存确切的朗读文本**——应用发音替换后（例如 `API` → `A P I`、`$2T` → `two trillion` 等）——作为同一目录中的 `narration.txt`。这是传递给 TTS 的字符串，与作为人类可读创意文档的 `SCRIPT.md` 不同。拥有 `narration.txt` 使得稍后无需重新推导替换即可用不同的语音重新生成音频。精确命名为 `narration.txt`。

## 转写为词语级时间戳

**如果你使用了 HeyGen v3 TTS：** 词语时间戳已在生成调用中返回。在保存前规范化格式——HeyGen v3 使用 `word` 但流水线期望 `text`：

```python
import json
raw = json.load(open('transcript_raw.json'))
normalized = [{"text": w["word"], "start": w["start"], "end": w["end"]} for w in raw]
json.dump(normalized, open('transcript.json', 'w'), indent=2)
```

无需单独的转录步骤。

**如果你使用了 ElevenLabs 或 Kokoro：**

```bash
npx hyperframes transcribe narration.wav
```

生成 `transcript.json`，每个词包含 `[{ text, start, end }]`。这些时间戳是所有节拍时长的真相来源。

## 将时间戳映射到节拍

逐节拍检查 STORYBOARD.md。对于每个节拍：

1. 在 `transcript.json` 中找到该节拍配音提示的第一个词
2. 找到该节拍配音提示的最后一个词
3. 设置 `beat.start = firstWord.start`、`beat.end = lastWord.end`
4. 在末尾添加 0.3-0.5s 的填充以提供视觉呼吸空间

用实际时长更新 STORYBOARD.md。将估计时间（例如「0:00-0:05」）替换为尽可能精确的实际时间戳（例如「0.00-3.21s」）。

节拍边界落在词语起始上——硬切到配音。

## 时序对账——在步骤 5 之前必需

在映射所有节拍后，将实际总音频时长与故事板的规划时长进行比较：

```
real_total = last_word.end + cta_hold（通常 2–3s）
planned_total = 所有节拍规划时长之和
delta = |real_total - planned_total|
```

**如果 delta > 规划总时长的 15%——不要不解决就进入步骤 5。** 常见原因和修复：

- **音频短于规划（Kokoro 最常见）：** Kokoro 生成压缩的语音，停顿最少。按比例将所有非 CTA 节拍时长缩减到匹配实际音频。示例：规划 30s，音频 19s——将每个节拍时长乘以 19/30（不包括 CTA 保持）。更新 STORYBOARD.md。
- **音频远长于规划（>30% 超出）：** 脚本对于预期的时长来说太长。修剪脚本（删除一个节拍的配音），重新生成音频，重新转写。
- **CTA 节拍时序：** CTA 节拍应在最后口播词之后保持 2–3 秒——而不是扩展到填充空白时间。`cta_start = last_word.end + 0.3s`、`cta_duration = 2.5s`。硬上限。CTA 保持后的死寂会失去观众。

**如果与故事板计划相比显著调整了时长，始终告知用户。** 他们批准了特定的节拍结构——如果它变了，他们需要知道。

## 字幕

在旁白生成并转写后，询问用户：

> **你想要视频上的字幕吗？**
>
> - **是**——与旁白同步的逐词字幕。适合社交媒体（大多数观众静音观看）和无障碍访问。
> - **否**——仅旁白音频，无文本叠加。

如果选是，字幕将在步骤 5 中作为独立作品（`compositions/captions.html`）构建。`transcript.json` 驱动时序——每个词在念出时出现/高亮。阅读[字幕参考](../../hyperframes/references/captions.md)了解样式选项（缩放弹出、打字机、淡出+滑动等）和定位规则。

## 为步骤 5 保存时序数据

记录最终节拍时序（开始、时长），以便步骤 5（构建）在构建 `index.html` 时使用。故事体现在有时间戳——当根作品在步骤 5 中组装时，这些将成为每个场景槽上的 `data-start` 和 `data-duration` 值。
