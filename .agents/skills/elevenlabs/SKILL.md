---
name: elevenlabs
description: 使用 ElevenLabs API 生成 AI 画外音、音效和音乐。在创建视频、播客或游戏的音频内容时使用。触发条件包括生成画外音、旁白、对话、根据描述生成音效、背景音乐、配乐生成、语音克隆或任何音频合成任务。
---

# ElevenLabs 音频生成

需要在 `.env` 中设置 `ELEVENLABS_API_KEY`。

## 文本转语音

```python
from elevenlabs.client import ElevenLabs
from elevenlabs import save, VoiceSettings
import os

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

audio = client.text_to_speech.convert(
    text="Welcome to my video!",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    voice_settings=VoiceSettings(
        stability=0.5,
        similarity_boost=0.75,
        style=0.5,
        speed=1.0
    )
)
save(audio, "voiceover.mp3")
```

### 模型

| 模型 | 质量 | SSML 支持 | 说明 |
|-------|---------|--------------|-------|
| `eleven_multilingual_v2` | 最高一致性 | 无 | 稳定，生产就绪，29 种语言 |
| `eleven_flash_v2_5` | 良好 | `<break>`、`<phoneme>` | 快速，支持暂停/发音标签 |
| `eleven_turbo_v2_5` | 良好 | `<break>`、`<phoneme>` | 最快延迟 |
| `eleven_v3` | 最具表现力 | 无 | Alpha——不可靠，需要提示工程 |

**选择：** multilingual_v2 用于可靠性，flash/turbo 用于 SSML 控制，v3 用于最大表现力（预期需要重录）。

### 按风格的语音设置

| 风格 | stability | similarity | style | speed |
|-------|-----------|------------|-------|-------|
| 自然/专业 | 0.75-0.85 | 0.9 | 0.0-0.1 | 1.0 |
| 对话式 | 0.5-0.6 | 0.85 | 0.3-0.4 | 0.9-1.0 |
| 精力充沛/YouTuber | 0.3-0.5 | 0.75 | 0.5-0.7 | 1.0-1.1 |

### 段落之间暂停

**使用 flash/turbo 模型：** 内联使用 SSML break 标签：
```
...end of section. <break time="1.5s" /> Start of next...
```
每个 break 最长 3 秒。过多的 break 可能导致速度伪影。

**使用 multilingual_v2 / v3：** 不支持 SSML。选项：
- 段落分隔（空行）——产生约 0.3-0.5 秒的自然停顿
- 使用 ffmpeg 后期处理：拆分音频并插入静音

**警告：** `...`（省略号）不是可靠的暂停——它可能被发音为词/声音。不要使用省略号作为暂停机制。

### 发音控制

**拼写变体（任何模型）：** 按您希望的发音方式写词：
- `Janus` → `Jan-us`
- `nginx` → `engine-x`
- 使用破折号、大写字母、撇号来引导发音

**SSML 音素标签（仅 flash/turbo）：**
```
<phoneme alphabet="ipa" ph="ˈdʒeɪnəs">Janus</phoneme>
```

### 迭代工作流

1. 生成 → 收听 → 识别发音/节奏问题
2. 调整：拼写变体、break 标签、语音设置
3. 重新生成。如果暂停不够精确，后期用 ffmpeg 添加静音，而不是与 TTS 引擎对抗。

## 语音克隆

### 即时语音克隆

```python
with open("sample.mp3", "rb") as f:
    voice = client.voices.ivc.create(
        name="My Voice",
        files=[f],
        remove_background_noise=True
    )
print(f"Voice ID: {voice.voice_id}")
```

- 使用 `client.voices.ivc.create()`（不是 `client.voices.clone()`）
- 以二进制模式（`"rb"`）传递文件句柄，而不是路径
- 先转换 m4a：`ffmpeg -i input.m4a -codec:a libmp3lame -qscale:a 2 output.mp3`
- 多个样本（2-3 个剪辑）可提高准确性
- 保存语音 ID 以便重用

**专业语音克隆：** 需要 Creator 计划+，30 分钟以上音频。请参阅 [reference.md](reference.md)。

## 音效

每次生成最长 22 秒。

```python
result = client.text_to_sound_effects.convert(
    text="Thunder rumbling followed by heavy rain",
    duration_seconds=10,
    prompt_influence=0.3
)
with open("thunder.mp3", "wb") as f:
    for chunk in result:
        f.write(chunk)
```

**提示技巧：** 要具体——"Heavy footsteps on wooden floorboards, slow and deliberate, with creaking"

## 音乐生成

10 秒到 5 分钟。使用 `client.music.compose()`（不是 `.generate()`）。

```python
result = client.music.compose(
    prompt="Upbeat indie rock, catchy guitar riff, energetic drums, travel vlog",
    music_length_ms=60000,
    force_instrumental=True
)
with open("music.mp3", "wb") as f:
    for chunk in result:
        f.write(chunk)
```

**提示结构：** 流派、情绪、乐器、节奏、用途。添加"no vocals"或使用 `force_instrumental=True` 表示背景音乐。

## Remotion 集成

### 完整工作流：从脚本到同步场景

```
VOICEOVER-SCRIPT.md → voiceover.py → public/audio/ → Remotion composition
        ↓                  ↓               ↓                 ↓
  场景旁白            生成 MP3        音频文件        <Audio> 组件
  带时长              按场景          带时序          与场景同步
```

### 步骤 1：生成按场景音频

使用工具包的画外音工具为每个场景生成音频：

```bash
# 为每个场景生成画外音文件
python tools/voiceover.py --scene-dir public/audio/scenes --json

# 输出：
# public/audio/scenes/
#   ├── scene-01-title.mp3
#   ├── scene-02-problem.mp3
#   ├── scene-03-solution.mp3
#   └── manifest.json  （每个文件的时长）
```

`manifest.json` 包含时间信息：
```json
{
  "scenes": [
    { "file": "scene-01-title.mp3", "duration": 4.2 },
    { "file": "scene-02-problem.mp3", "duration": 12.8 },
    { "file": "scene-03-solution.mp3", "duration": 15.3 }
  ],
  "totalDuration": 32.3
}
```

### 步骤 2：在 Remotion 合成中使用音频

```tsx
// src/Composition.tsx
import { Audio, staticFile, Series, useVideoConfig } from 'remotion';

// 导入场景组件
import { TitleSlide } from './scenes/TitleSlide';
import { ProblemSlide } from './scenes/ProblemSlide';
import { SolutionSlide } from './scenes/SolutionSlide';

// 场景时长（来自 manifest.json，按 30fps 转换为帧）
const SCENE_DURATIONS = {
  title: Math.ceil(4.2 * 30),      // 126 帧
  problem: Math.ceil(12.8 * 30),   // 384 帧
  solution: Math.ceil(15.3 * 30),  // 459 帧
};

export const MainComposition: React.FC = () => {
  return (
    <>
      {/* 场景序列 */}
      <Series>
        <Series.Sequence durationInFrames={SCENE_DURATIONS.title}>
          <TitleSlide />
        </Series.Sequence>
        <Series.Sequence durationInFrames={SCENE_DURATIONS.problem}>
          <ProblemSlide />
        </Series.Sequence>
        <Series.Sequence durationInFrames={SCENE_DURATIONS.solution}>
          <SolutionSlide />
        </Series.Sequence>
      </Series>

      {/* 音轨 - 在所有场景中连续播放 */}
      <Audio src={staticFile('audio/voiceover.mp3')} volume={1} />

      {/* 可选：以较低音量播放背景音乐 */}
      <Audio src={staticFile('audio/music.mp3')} volume={0.15} />
    </>
  );
};
```

### 步骤 3：按场景音频（替代方案）

为更多控制，为每个场景单独添加音频：

```tsx
// src/scenes/ProblemSlide.tsx
import { Audio, staticFile, useCurrentFrame } from 'remotion';

export const ProblemSlide: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{ /* 幻灯片样式 */ }}>
      <h1>The Problem</h1>
      {/* 场景内容 */}

      {/* 音频在此场景开始时开始（此序列的第 0 帧） */}
      <Audio src={staticFile('audio/scenes/scene-02-problem.mp3')} />
    </div>
  );
};
```

### 将视觉同步到画外音

从音频计算场景时长，而不是反过来：

```tsx
// src/config/timing.ts
import manifest from '../../public/audio/scenes/manifest.json';

const FPS = 30;

// 将音频时长转换为帧数
export const sceneDurations = manifest.scenes.reduce((acc, scene) => {
  const name = scene.file.replace(/^scene-\d+-/, '').replace('.mp3', '');
  acc[name] = Math.ceil(scene.duration * FPS);
  return acc;
}, {} as Record<string, number>);

// 在组合中的用法：
// <Series.Sequence durationInFrames={sceneDurations.title}>
```

### 音频时间模式

```tsx
import { Audio, Sequence, interpolate, useCurrentFrame } from 'remotion';

// 音频淡入
export const FadeInAudio: React.FC<{ src: string; fadeFrames?: number }> = ({
  src,
  fadeFrames = 30
}) => {
  const frame = useCurrentFrame();
  const volume = interpolate(frame, [0, fadeFrames], [0, 1], {
    extrapolateRight: 'clamp',
  });
  return <Audio src={src} volume={volume} />;
};

// 延迟音频开始
export const DelayedAudio: React.FC<{ src: string; delayFrames: number }> = ({
  src,
  delayFrames
}) => (
  <Sequence from={delayFrames}>
    <Audio src={src} />
  </Sequence>
);

// 用法：
// <FadeInAudio src={staticFile('audio/music.mp3')} fadeFrames={60} />
// <DelayedAudio src={staticFile('audio/sfx/whoosh.mp3')} delayFrames={45} />
```

### 画外音 + 演示视频同步

当场景同时有画外音和演示视频时：

```tsx
import { Audio, OffthreadVideo, staticFile, useVideoConfig } from 'remotion';

export const DemoScene: React.FC = () => {
  const { durationInFrames, fps } = useVideoConfig();

  // 计算播放速率以将演示适配到画外音时长
  const demoDuration = 45; // 秒（原始演示长度）
  const sceneDuration = durationInFrames / fps; // 秒（来自画外音）
  const playbackRate = demoDuration / sceneDuration;

  return (
    <>
      <OffthreadVideo
        src={staticFile('demos/feature-demo.mp4')}
        playbackRate={playbackRate}
      />
      <Audio src={staticFile('audio/scenes/scene-04-demo.mp3')} />
    </>
  );
};
```

### 错误处理

```tsx
import { Audio, staticFile, delayRender, continueRender } from 'remotion';
import { useEffect, useState } from 'react';

export const SafeAudio: React.FC<{ src: string }> = ({ src }) => {
  const [handle] = useState(() => delayRender());
  const [audioReady, setAudioReady] = useState(false);

  useEffect(() => {
    const audio = new window.Audio(src);
    audio.oncanplaythrough = () => {
      setAudioReady(true);
      continueRender(handle);
    };
    audio.onerror = () => {
      console.error(`Failed to load audio: ${src}`);
      continueRender(handle); // 继续而不挂起
    };
  }, [src, handle]);

  if (!audioReady) return null;
  return <Audio src={src} />;
};
```

### 工具包命令：/generate-voiceover

`/generate-voiceover` 命令处理完整工作流：

```
/generate-voiceover

1. 读取 VOICEOVER-SCRIPT.md
2. 提取每个场景的旁白
3. 通过 ElevenLabs API 生成音频
4. 保存到 public/audio/scenes/
5. 创建带时长的 manifest.json
6. 用时序信息更新 project.json
```

## 热门语音

- George：`JBFqnCBsd6RMkjVDRZzb`（温暖旁白）
- Rachel：`21m00Tcm4TlvDq8ikWAM`（清晰女性）
- Adam：`pNInz6obpgDQGcFmaJgB`（专业男性）

列出所有：`client.voices.get_all()`

完整 API 文档请参阅 [reference.md](reference.md)。
