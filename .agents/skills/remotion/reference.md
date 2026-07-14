# Remotion API 参考

## 核心 Hooks

### useCurrentFrame()
```tsx
const frame = useCurrentFrame();
```
返回当前帧（从 0 开始）。在 `<Sequence>` 内部，返回相对帧。

### useVideoConfig()
```tsx
const { width, height, fps, durationInFrames, id, defaultProps } = useVideoConfig();
```

## interpolate()

```tsx
interpolate(
  input: number,
  inputRange: number[],
  outputRange: number[],
  options?: {
    extrapolateLeft?: 'extend' | 'clamp' | 'identity' | 'wrap',
    extrapolateRight?: 'extend' | 'clamp' | 'identity' | 'wrap',
    easing?: (t: number) => number
  }
): number
```

**示例：**
```tsx
// 基本插值
interpolate(15, [0, 30], [0, 100]); // 50

// 带钳制
interpolate(50, [0, 30], [0, 1], { extrapolateRight: 'clamp' }); // 1

// 多关键帧
interpolate(frame, [0, 20, 40, 60], [0, 1, 1, 0]);

// 带缓动
interpolate(frame, [0, 30], [0, 100], { easing: Easing.bezier(0.42, 0, 0.58, 1) });
```

## spring()

```tsx
spring({
  frame: number,
  fps: number,
  config?: {
    damping?: number,      // 默认：10
    mass?: number,         // 默认：1  
    stiffness?: number,    // 默认：100
    overshootClamping?: boolean
  },
  from?: number,           // 默认：0
  to?: number,             // 默认：1
  durationInFrames?: number,
  durationRestThreshold?: number,
  delay?: number,
  reverse?: boolean
}): number
```

**配置预设：**
- 高弹跳：`{ damping: 5, stiffness: 200 }`
- 无弹跳：`{ damping: 20, stiffness: 100, overshootClamping: true }`
- 慢速：`{ damping: 20, mass: 2 }`

## measureSpring()

获取弹簧动画的持续时间：
```tsx
import { measureSpring } from 'remotion';

const duration = measureSpring({ fps: 30, config: { damping: 10 } });
// 返回弹簧稳定前的帧数
```

## interpolateColors()

```tsx
interpolateColors(
  input: number,
  inputRange: number[],
  outputRange: string[],  // Hex、rgb()、rgba()、hsl()
  options?: { extrapolateLeft?, extrapolateRight? }
): string
```

## Easing

```tsx
import { Easing } from 'remotion';

// 基本
Easing.linear
Easing.ease
Easing.quad
Easing.cubic

// In/Out/InOut 变体
Easing.in(Easing.quad)
Easing.out(Easing.cubic)
Easing.inOut(Easing.ease)

// 三次贝塞尔
Easing.bezier(x1, y1, x2, y2)

// 其他
Easing.circle
Easing.back(s?)      // 过冲
Easing.elastic(bounciness?)
Easing.bounce
Easing.sin
Easing.exp
Easing.poly(n)       // n 次方
```

## 组件

### Composition
```tsx
<Composition
  id="MyVideo"
  component={MyComponent}
  // 或 lazyComponent={() => import('./MyComponent')}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{ title: 'Hello' }}
  calculateMetadata={async ({ props }) => ({
    durationInFrames: props.items.length * 30,
    props: { ...props, computed: true }
  })}
/>
```

### Sequence
```tsx
<Sequence
  from={30}                    // 起始帧
  durationInFrames={60}        // 可选时长
  name="Intro"                 // Studio 时间线中的标签
  layout="none"                // "none" | "absolute-fill"
>
  <Child />
</Sequence>
```

### Series
```tsx
<Series>
  <Series.Sequence durationInFrames={30} offset={-5}>
    <A />  {/* 帧 0-29 */}
  </Series.Sequence>
  <Series.Sequence durationInFrames={60}>
    <B />  {/* 帧 25-84（偏移导致重叠） */}
  </Series.Sequence>
</Series>
```

### Loop
```tsx
<Loop
  durationInFrames={30}
  times={3}                    // 或 Infinity
  layout="none"
>
  <Animation />
</Loop>
```

### AbsoluteFill
```tsx
<AbsoluteFill style={{ backgroundColor: '#000' }}>
  {/* 位置：绝对，全宽/高 */}
</AbsoluteFill>
```

### 媒体组件

**Img**（等待加载）：
```tsx
<Img src={staticFile('photo.jpg')} style={{ width: '100%' }} />
```

**Video/Html5Video：**
```tsx
<Video
  src={staticFile('clip.mp4')}
  volume={0.5}                 // 0-1，或回调：(f) => f / 100
  playbackRate={1.5}
  muted={false}
  loop={false}
  startFrom={30}               // 跳过源的前 30 帧
  endAt={120}                  // 在源的第 120 帧停止
  acceptableTimeShiftInSeconds={0.2}
/>
```

**OffthreadVideo**（更好性能）：
```tsx
<OffthreadVideo
  src={staticFile('clip.mp4')}
  volume={0.5}
  transparent={false}          // 用于带 alpha 的视频
  toneMapped={true}           // HDR 色调映射
/>
```

**Audio：**
```tsx
<Audio
  src={staticFile('music.mp3')}
  volume={0.8}
  startFrom={0}
  endAt={300}
  playbackRate={1}
/>
```

**AnimatedImage**（GIF/APNG）：
```tsx
<AnimatedImage src={staticFile('animation.gif')} />
```

## 异步处理

```tsx
import { delayRender, continueRender, cancelRender } from 'remotion';

// 阻塞渲染
const handle = delayRender('Loading data...');

// 就绪时解除阻塞
continueRender(handle);

// 出错时取消
cancelRender(new Error('Failed to load'));
```

**带超时：**
```tsx
const handle = delayRender('Loading...', { timeoutInMilliseconds: 30000 });
```

## 静态文件与预取

```tsx
import { staticFile, prefetch, getStaticFiles } from 'remotion';

// 引用 public/ 中的文件
const url = staticFile('video.mp4');

// 预取以实现更快播放
const { free, waitUntilDone } = prefetch(url);
await waitUntilDone();
// 稍后：free() 以释放内存

// 列出所有静态文件
const files = getStaticFiles();  // ['video.mp4', 'image.png', ...]
```

## 输入属性

```tsx
import { getInputProps } from 'remotion';

const props = getInputProps();  // 通过 --props CLI 标志传递的数据
```

## 环境检测

```tsx
import { getRemotionEnvironment } from 'remotion';

const env = getRemotionEnvironment();
// { isStudio: boolean, isRendering: boolean, isPlayer: boolean }
```

## random()

确定性随机数，用于一致渲染：
```tsx
import { random } from 'remotion';

const value = random('my-seed');      // 0-1，每次渲染相同
const value2 = random('seed', 0, 100); // 0-100
const value3 = random(null);           // 每次渲染不同
```

## @remotion/renderer API

```tsx
import { bundle } from '@remotion/bundler';
import { 
  renderMedia, 
  renderStill,
  selectComposition,
  getCompositions,
  renderFrames,
  stitchFramesToVideo
} from '@remotion/renderer';

// 打包项目
const bundleLocation = await bundle({
  entryPoint: './src/index.ts',
  webpackOverride: (config) => config,
});

// 获取组合
const composition = await selectComposition({
  serveUrl: bundleLocation,
  id: 'MyComp',
  inputProps: {},
});

// 渲染视频
await renderMedia({
  composition,
  serveUrl: bundleLocation,
  codec: 'h264',              // h264, h265, vp8, vp9, gif, prores
  outputLocation: 'out.mp4',
  inputProps: {},
  onProgress: ({ progress }) => console.log(`${progress * 100}%`),
  imageFormat: 'jpeg',        // jpeg 或 png
  jpegQuality: 80,
  scale: 1,
  frameRange: [0, 59],        // 可选：特定帧
  muted: false,
  audioBitrate: '128k',
  videoBitrate: '5M',
  crf: 18,                    // 质量（越低越好、越大）
  concurrency: 4,
});

// 渲染静态图像
await renderStill({
  composition,
  serveUrl: bundleLocation,
  output: 'thumbnail.png',
  frame: 30,
  imageFormat: 'png',
});
```

## @remotion/lambda API

```tsx
import {
  deployFunction,
  deploySite,
  renderMediaOnLambda,
  renderStillOnLambda,
  getRenderProgress,
  downloadMedia,
} from '@remotion/lambda';

// 部署函数
const { functionName } = await deployFunction({
  region: 'us-east-1',
  timeoutInSeconds: 120,
  memorySizeInMb: 2048,
});

// 部署站点
const { serveUrl } = await deploySite({
  entryPoint: './src/index.ts',
  region: 'us-east-1',
  siteName: 'my-video',
});

// 渲染
const { renderId, bucketName } = await renderMediaOnLambda({
  region: 'us-east-1',
  functionName,
  serveUrl,
  composition: 'MyComp',
  codec: 'h264',
  inputProps: {},
  framesPerLambda: 20,
});

// 检查进度
const progress = await getRenderProgress({
  renderId,
  bucketName,
  region: 'us-east-1',
  functionName,
});

// 完成时下载
if (progress.done) {
  await downloadMedia({
    bucketName,
    renderId,
    region: 'us-east-1',
    outPath: 'video.mp4',
  });
}
```

## @remotion/player API

```tsx
import { Player, PlayerRef } from '@remotion/player';

const playerRef = useRef<PlayerRef>(null);

<Player
  ref={playerRef}
  component={MyComp}
  // 或 lazyComponent={() => import('./MyComp')}
  durationInFrames={150}
  fps={30}
  compositionWidth={1920}
  compositionHeight={1080}
  inputProps={{}}
  style={{ width: '100%' }}
  controls={true}
  autoPlay={false}
  loop={false}
  showVolumeControls={true}
  allowFullscreen={true}
  clickToPlay={true}
  doubleClickToFullscreen={true}
  spaceKeyToPlayOrPause={true}
  playbackRate={1}
  renderLoading={() => <div>Loading...</div>}
  errorFallback={({ error }) => <div>Error: {error.message}</div>}
  numberOfSharedAudioTags={5}
  initiallyShowControls={3000}
  renderPlayPauseButton={() => null}
  moveToBeginningWhenEnded={true}
/>

// 命令式 API
playerRef.current?.play();
playerRef.current?.pause();
playerRef.current?.toggle();
playerRef.current?.seekTo(30);
playerRef.current?.getCurrentFrame();
playerRef.current?.isPlaying();
playerRef.current?.getVolume();
playerRef.current?.setVolume(0.5);
playerRef.current?.isMuted();
playerRef.current?.mute();
playerRef.current?.unmute();
playerRef.current?.requestFullscreen();
playerRef.current?.exitFullscreen();
playerRef.current?.isFullscreen();

// 事件
<Player
  onPlay={() => {}}
  onPause={() => {}}
  onEnded={() => {}}
  onError={(e) => {}}
  onSeeked={(frame) => {}}
  onTimeUpdate={({ frame }) => {}}
  onFullscreenChange={(isFullscreen) => {}}
/>
```

## calculateMetadata

动态组合属性：
```tsx
export const calculateMetadata: CalculateMetadataFunction<Props> = async ({ 
  props, 
  abortSignal, 
  defaultProps 
}) => {
  const data = await fetch('/api/data', { signal: abortSignal });
  
  return {
    durationInFrames: data.items.length * 30,
    fps: 60,
    width: 1920,
    height: 1080,
    props: { ...props, items: data.items },
  };
};

<Composition
  id="Dynamic"
  component={MyComp}
  calculateMetadata={calculateMetadata}
  // 基础值（可被 calculateMetadata 覆盖）
  durationInFrames={1}
  fps={30}
  width={1920}
  height={1080}
/>
```
