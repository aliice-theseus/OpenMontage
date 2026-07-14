---
name: audio-visualization
description: 音频可视化模式 - 频谱条、波形、低音响应效果
metadata:
  tags: audio, visualization, spectrum, waveform, bass, music, audiogram, frequency
---

# Remotion 中的音频可视化

## 前置条件

```bash
npx remotion add @remotion/media-utils
```

## 加载音频数据

使用 `useWindowedAudioData()`（https://www.remotion.dev/docs/use-windowed-audio-data）加载音频数据：

```tsx
import { useWindowedAudioData } from "@remotion/media-utils";
import { staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
  src: staticFile("podcast.wav"),
  frame,
  fps,
  windowInSeconds: 30,
});
```

## 频谱条可视化

使用 `visualizeAudio()`（https://www.remotion.dev/docs/visualize-audio）获取用于条形图的频率数据：

```tsx
import { useWindowedAudioData, visualizeAudio } from "@remotion/media-utils";
import { staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
  src: staticFile("music.mp3"),
  frame,
  fps,
  windowInSeconds: 30,
});

if (!audioData) {
  return null;
}

const frequencies = visualizeAudio({
  fps,
  frame,
  audioData,
  numberOfSamples: 256,
  optimizeFor: "speed",
  dataOffsetInSeconds,
});

return (
  <div style={{ display: "flex", alignItems: "flex-end", height: 200 }}>
    {frequencies.map((v, i) => (
      <div
        key={i}
        style={{
          flex: 1,
          height: `${v * 100}%`,
          backgroundColor: "#0b84f3",
          margin: "0 1px",
        }}
      />
    ))}
  </div>
);
```

- `numberOfSamples` 必须是 2 的幂（32、64、128、256、512、1024）
- 值范围为 0-1；数组左侧 = 低音，右侧 = 高音
- 对于 Lambda 或高采样数，使用 `optimizeFor: "speed"`

**重要提示：** 将 `audioData` 传递给子组件时，同时传递父级的 `frame`。不要在子组件中调用 `useCurrentFrame()`——这会导致当子组件位于带有偏移量的 `<Sequence>` 内部时出现不连续的视觉效果。

## 波形可视化

使用 `visualizeAudioWaveform()`（https://www.remotion.dev/docs/media-utils/visualize-audio-waveform）配合 `createSmoothSvgPath()`（https://www.remotion.dev/docs/media-utils/create-smooth-svg-path）实现示波器风格的显示：

```tsx
import {
  createSmoothSvgPath,
  useWindowedAudioData,
  visualizeAudioWaveform,
} from "@remotion/media-utils";
import { staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { width, fps } = useVideoConfig();
const HEIGHT = 200;

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
  src: staticFile("voice.wav"),
  frame,
  fps,
  windowInSeconds: 30,
});

if (!audioData) {
  return null;
}

const waveform = visualizeAudioWaveform({
  fps,
  frame,
  audioData,
  numberOfSamples: 256,
  windowInSeconds: 0.5,
  dataOffsetInSeconds,
});

const path = createSmoothSvgPath({
  points: waveform.map((y, i) => ({
    x: (i / (waveform.length - 1)) * width,
    y: HEIGHT / 2 + (y * HEIGHT) / 2,
  })),
});

return (
  <svg width={width} height={HEIGHT}>
    <path d={path} fill="none" stroke="#0b84f3" strokeWidth={2} />
  </svg>
);
```

## 低音响应效果

提取低频用于节拍响应动画：

```tsx
const frequencies = visualizeAudio({
  fps,
  frame,
  audioData,
  numberOfSamples: 128,
  optimizeFor: "speed",
  dataOffsetInSeconds,
});

const lowFrequencies = frequencies.slice(0, 32);
const bassIntensity =
  lowFrequencies.reduce((sum, v) => sum + v, 0) / lowFrequencies.length;

const scale = 1 + bassIntensity * 0.5;
const opacity = Math.min(0.6, bassIntensity * 0.8);
```

## 基于音量的波形

当你需要简化的音量数据而非频谱时，使用 `getWaveformPortion()`（https://www.remotion.dev/docs/get-waveform-portion）：

```tsx
import { getWaveformPortion } from "@remotion/media-utils";
import { useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const currentTimeInSeconds = frame / fps;

const waveform = getWaveformPortion({
  audioData,
  startTimeInSeconds: currentTimeInSeconds,
  durationInSeconds: 5,
  numberOfSamples: 50,
});

// 返回 { index, amplitude } 对象的数组（amplitude: 0-1）
waveform.map((bar) => (
  <div key={bar.index} style={{ height: bar.amplitude * 100 }} />
));
```

## 后处理

低频自然占据主导地位。应用对数缩放以实现视觉平衡：

```tsx
const minDb = -100;
const maxDb = -30;

const scaled = frequencies.map((value) => {
  const db = 20 * Math.log10(value);
  return (db - minDb) / (maxDb - minDb);
});
```
