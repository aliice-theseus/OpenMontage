---
name: audio
description: 在 Remotion 中使用音频 - 导入、裁剪、音量、速度、音调
metadata:
  tags: audio, media, trim, volume, speed, loop, pitch, mute, sound, sfx
---

# 在 Remotion 中使用音频

## 前置条件

首先，需要安装 @remotion/media 包。
如果尚未安装，请使用以下命令：

```bash
npx remotion add @remotion/media
```

## 导入音频

使用 `@remotion/media` 的 `<Audio>` 组件为合成添加音频。

```tsx
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";

export const MyComposition = () => {
  return <Audio src={staticFile("audio.mp3")} />;
};
```

也支持远程 URL：

```tsx
<Audio src="https://remotion.media/audio.mp3" />
```

默认情况下，音频从开头开始播放，音量最大，播放完整长度。
可以通过添加多个 `<Audio>` 组件来叠加多轨音频。

## 裁剪

使用 `trimBefore` 和 `trimAfter` 移除音频的部分内容。值以帧为单位。

```tsx
const { fps } = useVideoConfig();

return (
  <Audio
    src={staticFile("audio.mp3")}
    trimBefore={2 * fps} // 跳过前 2 秒
    trimAfter={10 * fps} // 在第 10 秒处结束
  />
);
```

音频仍然从合成的开头开始播放——仅播放指定部分。

## 延迟

将音频包裹在 `<Sequence>` 中以延迟其开始播放：

```tsx
import { Sequence, staticFile } from "remotion";
import { Audio } from "@remotion/media";

const { fps } = useVideoConfig();

return (
  <Sequence from={1 * fps}>
    <Audio src={staticFile("audio.mp3")} />
  </Sequence>
);
```

音频将在 1 秒后开始播放。

## 音量

设置静态音量（0 到 1）：

```tsx
<Audio src={staticFile("audio.mp3")} volume={0.5} />
```

或使用回调函数实现基于当前帧的动态音量：

```tsx
import { interpolate } from "remotion";

const { fps } = useVideoConfig();

return (
  <Audio
    src={staticFile("audio.mp3")}
    volume={(f) =>
      interpolate(f, [0, 1 * fps], [0, 1], { extrapolateRight: "clamp" })
    }
  />
);
```

`f` 的值从音频开始播放时（而非合成帧）从 0 开始计数。

## 静音

使用 `muted` 使音频静音。可以动态设置：

```tsx
const frame = useCurrentFrame();
const { fps } = useVideoConfig();

return (
  <Audio
    src={staticFile("audio.mp3")}
    muted={frame >= 2 * fps && frame <= 4 * fps} // 在 2s 到 4s 之间静音
  />
);
```

## 速度

使用 `playbackRate` 更改播放速度：

```tsx
<Audio src={staticFile("audio.mp3")} playbackRate={2} /> {/* 2 倍速 */}
<Audio src={staticFile("audio.mp3")} playbackRate={0.5} /> {/* 半速 */}
```

不支持倒放。

## 循环

使用 `loop` 无限循环播放音频：

```tsx
<Audio src={staticFile("audio.mp3")} loop />
```

使用 `loopVolumeCurveBehavior` 控制循环时帧数的行为：

- `"repeat"`：每次循环帧数重置为 0（默认）
- `"extend"`：帧数继续递增

```tsx
<Audio
  src={staticFile("audio.mp3")}
  loop
  loopVolumeCurveBehavior="extend"
  volume={(f) => interpolate(f, [0, 300], [1, 0])} // 跨多个循环淡出
/>
```

## 音调

使用 `toneFrequency` 调整音调而不影响速度。值范围从 0.01 到 2：

```tsx
<Audio
  src={staticFile("audio.mp3")}
  toneFrequency={1.5} // 更高音调
/>
<Audio
  src={staticFile("audio.mp3")}
  toneFrequency={0.8} // 更低音调
/>
```

音调调整仅在服务端渲染时生效，在 Remotion Studio 预览或 `<Player />` 中不生效。
