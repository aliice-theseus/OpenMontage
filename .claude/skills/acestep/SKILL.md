---
name: acestep
description: 使用 ACE-Step 1.5 进行 AI 音乐生成 — 背景音乐、人声曲目、翻唱、音轨分离，用于视频制作。在生成音乐、配乐、广告曲或处理音频音轨时使用。触发词包括背景音乐、配乐、广告曲、音乐生成、音轨分离、翻唱、风格迁移或音乐创作任务。
---

# ACE-Step 1.5 音乐生成

开源音乐生成（MIT 许可证），通过 `tools/music_gen.py` 使用。运行在 RunPod serverless 上。
需在 `.env` 中配置 `RUNPOD_API_KEY` 和 `RUNPOD_ACESTEP_ENDPOINT_ID`（运行 `--setup` 创建端点）。

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

## 创作歌曲（分步指南）

### 1. 纯音乐背景音轨（最简单）
```bash
python tools/music_gen.py --prompt "Upbeat indie rock, driving drums, jangly guitar" --duration 60 --bpm 120 --key "G Major" --output track.mp3
```

### 2. 带人声和歌词的歌曲
将歌词写入临时文件或内联传递。使用结构标签控制歌曲段落。

```bash
# 先将歌词写入文件（长歌曲推荐）
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

### 3. 使用视频背景音乐预设
```bash
python tools/music_gen.py --preset tension --duration 20 --output problem_scene.mp3
```

### 优秀结果的关键技巧
- **描述文字 = 整体风格**（流派、乐器、情绪、制作质量）
- **歌词 = 时间结构**（主歌/副歌的流动、人声表达）
- **歌词中的大写字母** = 高音强度
- **括号** = 背景人声："We rise (together)"
- **每行保持 6-10 个音节** 以获得自然节奏
- **不要在描述文字中描述旋律** — 描述 *声音* 和 *感觉*
- **使用 `--seed`** 在迭代提示/歌词时锁定随机性

## 场景预设

| 预设 | BPM | 调性 | 使用场景 |
|--------|-----|-----|----------|
| `corporate-bg` | 110 | C 大调 | 专业背景、演示文稿 |
| `upbeat-tech` | 128 | G 大调 | 产品发布、技术演示 |
| `ambient` | 72 | D 大调 | 概览幻灯片、反思性内容 |
| `dramatic` | 90 | D 小调 | 揭晓、公告 |
| `tension` | 85 | A 小调 | 问题陈述、挑战 |
| `hopeful` | 120 | C 大调 | 解决方案揭晓、决议 |
| `cta` | 135 | E 大调 | 行动号召、结尾能量 |
| `lofi` | 85 | F 大调 | 屏幕录制、编程演示 |

## 任务类型

### text2music（默认）
从文本提示 + 可选歌词生成音乐。

### cover
参考音频风格迁移。通过 `--cover-strength`（0.0-1.0）控制混合程度：
- **0.2** — 松散的风格灵感（更多创作自由度）
- **0.5** — 平衡的风格迁移
- **0.7** — 接近原始结构（默认）
- **1.0** — 最大程度忠实于源

### extract
音轨分离 — 从混合音频中分离出独立音轨。
可用音轨：`vocals`（人声）、`drums`（鼓）、`bass`（贝斯）、`guitar`（吉他）、`piano`（钢琴）、`keyboard`（键盘）、`strings`（弦乐）、`brass`（铜管）、`woodwinds`（木管）、`other`（其他）

### repaint（未来功能）
重新生成现有音频中的特定时间段，同时保留其余部分。

### lego（未来功能，需基础模型）
在现有音频上下文中生成独立的乐器音轨。

### complete（未来功能，需基础模型）
通过添加指定乐器扩展不完整的作曲。

## 提示工程

### 描述文字撰写 — 分层维度

通过组合多个描述性维度来撰写描述文字，而非使用单一词语描述。

**应包含的维度：**
- **流派/风格**：流行、摇滚、爵士、电子、lo-fi、合成波、管弦乐
- **情感/情绪**：忧郁、欢快、梦幻、怀旧、亲密、紧张
- **乐器**：原声吉他、合成垫、808 鼓、弦乐、铜管、钢琴
- **音色**：温暖、清脆、空灵、有力、丰满、精致、原始
- **时代**："80 年代合成波"、"现代独立"、"古典浪漫"
- **制作**：lo-fi、录音室精致、现场录音、电影感
- **人声**：气声、有力、假声、沙哑、念白（或"纯器乐"）

**优秀示例**："Slow melancholic piano ballad with intimate female vocal, warm strings building to powerful chorus, studio-polished production"
**差劲示例**："Sad song"

### 关键原则

1. **具体优于模糊** — 描述乐器、情绪、制作风格
2. **避免矛盾** — 不要同时要求"古典弦乐"和"硬核金属"
3. **重复强化优先级** — 重复重要元素以强调
4. **简洁的描述文字 = 更多创作自由度** — 详细的描述文字会约束模型
5. **使用元数据参数控制 BPM/调性** — 不要在描述文字中写"120 BPM"，使用 `--bpm 120`

### 歌词格式

**结构标签**（用在歌词中，而非描述文字中）：
```
[Intro]（前奏）
[Verse]（主歌）
[Chorus]（副歌）
[Bridge]（桥段）
[Outro]（尾奏）
[Instrumental]（器乐）
[Guitar Solo]（吉他独奏）
[Build]（推进）
[Drop]（高潮）
[Breakdown]（低谷）
```

**人声控制**（前缀行或段落）：
```
[raspy vocal]（沙哑人声）
[whispered]（低语）
[falsetto]（假声）
[powerful belting]（强力高音）
[harmonies]（和声）
[ad-lib]（即兴）
```

**能量标识：**
- 大写 = 高能量（"WE RISE ABOVE"）
- 括号 = 背景人声（"We rise (together)"）
- 段落内每行保持 6-10 个音节以获得自然节奏

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

### 场景类型配乐

| 场景 | 预设 | 时长 | 备注 |
|-------|--------|----------|-------|
| 标题 | `dramatic` 或 `ambient` | 3-5 秒 | 简短，营造氛围 |
| 问题 | `tension` | 10-15 秒 | 阴暗，不安 |
| 解决方案 | `hopeful` | 10-15 秒 | 解脱，乐观 |
| 演示 | `lofi` 或 `corporate-bg` | 30-120 秒 | 不分心，匹配演示长度 |
| 数据 | `upbeat-tech` | 8-12 秒 | 建立可信度 |
| 行动号召 | `cta` | 5-10 秒 | 最大能量，有力 |
| 演职员表 | `ambient` | 5-10 秒 | 柔和淡出 |

### 时间工作流

1. 先规划场景时长（根据配音脚本）
2. 生成匹配的音乐：`--duration <场景秒数>`
3. 音乐时长精确（在请求值 0.1 秒内）
4. 对于跨多个场景的背景音乐：生成长音轨

### 配合配音

背景音乐应在 Remotion 中以 10-20% 音量混音：
```tsx
<Audio src={staticFile('voiceover.mp3')} volume={1} />
<Audio src={staticFile('bg-music.mp3')} volume={0.15} />
```

配音下的音乐：使用纯音乐预设（`corporate-bg`、`ambient`、`lofi`）。
以音乐为主的场景（标题、行动号召）：可使用更高音量或人声音轨。

### 品牌一致性

使用 `--brand <name>` 从 `brands/<name>/brand.json` 加载提示。
使用 `--cover --reference brand_theme.mp3` 创建品牌声音标识的变体。
为了在项目中保持一致的音效：固定种子（`--seed 42`），仅变化时长/提示。

## 技术细节

- **输出**：48kHz MP3/WAV/FLAC
- **时长范围**：10-600 秒
- **BPM 范围**：30-300
- **推理**：GPU 上约 2-3 秒（turbo，8 步），Mac MPS 上约 40-60 秒
- **Turbo 模型**：8 步，无需 CFG，快速且质量好
- **Shift 参数**：turbo 推荐 3.0（提升质量）

### 何时不使用 ACE-Step
- **声音克隆** — 改用 Qwen3-TTS 或 ElevenLabs
- **音效** — 使用 ElevenLabs SFX（`tools/sfx.py`）
- **语音/旁白** — 使用配音工具，而非音乐生成
- **从视频中分离音轨** — 先用 FFmpeg 提取音频，然后使用 `--extract`
