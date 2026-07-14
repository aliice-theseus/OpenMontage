---
name: acestep
description: 使用 ACE-Step 1.5 进行 AI 音乐生成 — 背景音乐、人声轨、翻唱、音轨分离，适用于视频制作。当需要生成音乐、配乐、广告曲或处理音频音轨时使用。触发词包括背景音乐、配乐、广告曲、音乐生成、音轨分离、翻唱、风格迁移或音乐创作任务。
---

# ACE-Step 1.5 音乐生成

通过 `tools/music_gen.py` 使用开源音乐生成（MIT 许可）。运行在 RunPod 无服务器架构上。需要在 `.env` 中配置 `RUNPOD_API_KEY` 和 `RUNPOD_ACESTEP_ENDPOINT_ID`（运行 `--setup` 可创建端点）。

## 快速参考

```bash
# 基础生成
python tools/music_gen.py --prompt "Upbeat tech corporate" --duration 60 --output bg.mp3

# 带音乐控制参数
python tools/music_gen.py --prompt "Calm ambient piano" --duration 30 --bpm 72 --key "D Major" --output ambient.mp3

# 场景预设（视频制作）
python tools/music_gen.py --preset corporate-bg --duration 60 --output bg.mp3
python tools/music_gen.py --preset tension --duration 20 --output problem.mp3
python tools/music_gen.py --preset cta --brand digital-samba --duration 15 --output cta.mp3

# 带歌词的人声
python tools/music_gen.py --prompt "Indie pop jingle" --lyrics "[verse]\nBuild it better\nShip it faster" --duration 30 --output jingle.mp3

# 翻唱 / 风格迁移
python tools/music_gen.py --cover --reference theme.mp3 --prompt "Jazz piano version" --duration 60 --output jazz_cover.mp3

# 音轨分离
python tools/music_gen.py --extract vocals --input mixed.mp3 --output vocals.mp3

# 列出预设
python tools/music_gen.py --list-presets
```

## 创作一首歌（分步指南）

### 1. 纯器乐背景音轨（最简单）
```bash
python tools/music_gen.py --prompt "Upbeat indie rock, driving drums, jangly guitar" --duration 60 --bpm 120 --key "G Major" --output track.mp3
```

### 2. 带人声和歌词的歌
将歌词写入临时文件或通过命令行内联传递。使用结构标签控制歌曲段落。

```bash
# 先将歌词写入文件（长歌推荐）
cat > /tmp/lyrics.txt << 'LYRICS'
[Verse 1]
Walking through the morning light
Coffee in my hand feels right
Another day to build and dream
Nothing's ever what it seems

[Chorus - anthemic]
WE KEEP MOVING FORWARD
Through the noise and doubt
We keep moving forward
That's what it's about

[Verse 2]
Screens are glowing late at night
Shipping code until it's right
The deadline's close but so are we
Almost there, just wait and see

[Chorus - bigger]
WE KEEP MOVING FORWARD
Through the noise and doubt
We keep moving forward
That's what it's about

[Outro - fade]
(Moving forward...)
LYRICS

# 生成歌曲
python tools/music_gen.py \
  --prompt "Upbeat indie rock anthem, male vocal, driving drums, electric guitar, studio polish" \
  --lyrics "$(cat /tmp/lyrics.txt)" \
  --duration 60 \
  --bpm 128 \
  --key "G Major" \
  --output my_song.mp3
```

### 3. 使用预设生成视频背景音乐
```bash
python tools/music_gen.py --preset tension --duration 20 --output problem_scene.mp3
```

### 获得好效果的关键技巧
- **Caption = 整体风格**（流派、乐器、情绪、制作质量）
- **歌词 = 时间结构**（主歌/副歌流程、人声表达）
- **歌词中的大写字母** = 高音强度
- **括号内的文字** = 背景和声："We rise (together)"
- **每行保持 6-10 个音节** 以获得自然的节奏感
- **不要在 caption 中描述旋律** — 描述 *声音* 和 *感觉*
- **使用 `--seed`** 来锁定随机性，方便迭代提示词/歌词

## 场景预设

| 预设 | BPM | 调性 | 用途 |
|--------|-----|------|----------|
| `corporate-bg` | 110 | C Major | 专业背景，演示 |
| `upbeat-tech` | 128 | G Major | 产品发布，技术演示 |
| `ambient` | 72 | D Major | 概览幻灯片，反思性内容 |
| `dramatic` | 90 | D Minor | 揭秘，公告 |
| `tension` | 85 | A Minor | 问题陈述，挑战 |
| `hopeful` | 120 | C Major | 解决方案展示，解决方案 |
| `cta` | 135 | E Major | 行动号召，结尾能量 |
| `lofi` | 85 | F Major | 屏幕录制，编程演示 |

## 任务类型

### text2music（默认）
根据文本提示和可选歌词生成音乐。

### cover
从参考音频进行风格迁移。使用 `--cover-strength`（0.0-1.0）控制混合程度：
- **0.2** — 松散的风格启发（更多创作自由）
- **0.5** — 平衡的风格迁移
- **0.7** — 接近原结构（默认）
- **1.0** — 最大保真度

### extract
音轨分离 — 从混合音频中分离出单独的音轨。
可用音轨：`vocals`、`drums`、`bass`、`guitar`、`piano`、`keyboard`、`strings`、`brass`、`woodwinds`、`other`

### repaint（未来功能）
重新生成现有音频中的特定时间段，同时保留其余部分。

### lego（未来功能，需要基础模型）
在现有音频上下文中生成单独的乐器音轨。

### complete（未来功能，需要基础模型）
通过添加指定的乐器来扩展部分创作。

## 提示词工程

### Caption 写作 — 层次维度

通过叠加多个描述性维度来编写 caption，而不是使用单个词语描述。

**应包含的维度：**
- **流派/风格**：pop、rock、jazz、electronic、lo-fi、synthwave、orchestral
- **情感/情绪**：melancholic、euphoric、dreamy、nostalgic、intimate、tense
- **乐器**：acoustic guitar、synth pads、808 drums、strings、brass、piano
- **音色**：warm、crisp、airy、punchy、lush、polished、raw
- **时代**：80s synth-pop、modern indie、classical romantic
- **制作**：lo-fi、studio-polished、live recording、cinematic
- **人声**：breathy、powerful、falsetto、raspy、spoken word（或 instrumental）

**好例子**："Slow melancholic piano ballad with intimate female vocal, warm strings building to powerful chorus, studio-polished production"
**坏例子**："Sad song"

### 关键原则

1. **具体优于模糊** — 描述乐器、情绪、制作风格
2. **避免矛盾** — 不要同时要求 classical strings 和 hardcore metal
3. **重复强化优先级** — 重复重要元素以加强效果
4. **稀疏的 caption = 更多创作自由** — 详细的 caption 会约束模型
5. **使用元数据参数设置 BPM/调性** — 不要在 caption 里写 120 BPM，用 `--bpm 120`

### 歌词格式

**结构标签**（在歌词中使用，不在 caption 中）：
```
[Intro]
[Verse]
[Chorus]
[Bridge]
[Outro]
[Instrumental]
[Guitar Solo]
[Build]
[Drop]
[Breakdown]
```

**人声控制**（在行或段落前添加）：
```
[raspy vocal]
[whispered]
[falsetto]
[powerful belting]
[harmonies]
[ad-lib]
```

**能量指示：**
- 大写字母 = 高能量（"WE RISE ABOVE"）
- 括号 = 背景和声（"We rise (together)"）
- 段落内每行保持 6-10 个音节，以获得自然的节奏感

**示例 — 科技产品广告曲：**
```
[Verse]
Build it better, ship it faster
Every feature tells a story

[Chorus - anthemic]
THIS IS YOUR PLATFORM
Your vision, your stage
Digital Samba, every page

[Outro - fade]
(Build it better...)
```

## 视频制作集成

### 各场景类型的音乐

| 场景 | 预设 | 时长 | 备注 |
|-------|--------|----------|-------|
| 标题 | `dramatic` 或 `ambient` | 3-5 秒 | 短促，营造氛围 |
| 问题 | `tension` | 10-15 秒 | 黑暗，不安 |
| 解决方案 | `hopeful` | 10-15 秒 | 如释重负，乐观 |
| 演示 | `lofi` 或 `corporate-bg` | 30-120 秒 | 不分散注意力，匹配演示长度 |
| 数据 | `upbeat-tech` | 8-12 秒 | 建立可信度 |
| CTA | `cta` | 5-10 秒 | 最大能量，有力 |
| 致谢 | `ambient` | 5-10 秒 | 轻柔渐出 |

### 时机工作流

1. 先规划场景时长（根据旁白脚本）
2. 生成匹配的音乐：`--duration <场景秒数>`
3. 音乐时长精确（误差在请求值的 0.1 秒内）
4. 如需覆盖多个场景的背景音乐：生成一个长音轨

### 与旁白结合

背景音乐在 Remotion 中应混音至 10-20% 音量：
```tsx
<Audio src={staticFile('voiceover.mp3')} volume={1} />
<Audio src={staticFile('bg-music.mp3')} volume={0.15} />
```

旁白下的音乐：使用器乐预设（`corporate-bg`、`ambient`、`lofi`）。
以音乐为主的场景（标题、CTA）：可以使用更高音量或人声音轨。

### 品牌一致性

使用 `--brand <名称>` 从 `brands/<名称>/brand.json` 加载提示。
使用 `--cover --reference brand_theme.mp3` 创建品牌声音标识的变体。
如需项目内保持声音一致：固定 seed（`--seed 42`），只变化时长/提示词。

## 技术细节

- **输出格式**：48kHz MP3/WAV/FLAC
- **时长范围**：10-600 秒
- **BPM 范围**：30-300
- **推理时间**：GPU 上约 2-3 秒（turbo，8 步），Mac MPS 上约 40-60 秒
- **Turbo 模型**：8 步，无需 CFG，快速且质量好
- **Shift 参数**：turbo 推荐 3.0（提升质量）

### 何时不应使用 ACE-Step
- **语音克隆** — 改用 Qwen3-TTS 或 ElevenLabs
- **音效** — 使用 ElevenLabs SFX（`tools/sfx.py`）
- **语音/旁白** — 使用旁白工具，非音乐生成
- **从视频中提取音轨** — 先用 FFmpeg 提取音频，再使用 `--extract`
