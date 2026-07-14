# 媒体翻译：Audio, Video, Img, IFrame, staticFile

## 资源路径

Remotion 的 `staticFile("x.png")` 解析到项目的 `public/` 目录。HF 使用相对于合成 `index.html` 的路径，约定为 `assets/`：

```tsx
<Img src={staticFile("logo.png")} />
```

```html
<img src="assets/logo.png" />
```

翻译时，将资源从 `remotion-src/public/x` 复制到 `hf-src/assets/x`。多个文件可以通过设置脚本批量处理；参见 T2 的 `setup.sh` 了解示例模式。

## `<Audio>`

```tsx
<Audio src={staticFile("music.wav")} volume={0.5} />
```

```html
<audio
  data-start="0"
  data-duration="6"
  data-track-index="2"
  data-volume="0.5"
  src="assets/music.wav"
></audio>
```

`data-start` 和 `data-duration` 是必需的 — 运行时需要它们来调度音频。如果 Remotion 未指定修剪，默认为合成的完整时长。

### 音量渐变

```tsx
<Audio src={staticFile("music.wav")} volume={(f) => interpolate(f, [0, 30], [0, 1])} />
```

HF 目前仅支持静态 `data-volume`。音量渐变需要在翻译时应用到音频文件（使用 ffmpeg `afade`），否则渐变会被丢弃并附带翻译说明。

### 修剪 / 播放速率

```tsx
<Audio src={staticFile("music.wav")} startFrom={60} endAt={180} playbackRate={1.5} />
```

```html
<audio
  data-start="0"
  data-duration="<根据修剪解析>"
  data-trim-start="2"
  data-trim-end="6"
  data-playback-rate="1.5"
  src="assets/music.wav"
></audio>
```

`startFrom` / `endAt` 是帧索引；转换为秒。

## `<Video>` 和 `<OffthreadVideo>`

```tsx
<Video src={staticFile("intro.mp4")} muted playsInline />
<OffthreadVideo src={staticFile("intro.mp4")} muted />
```

```html
<video
  muted
  playsinline
  data-start="0"
  data-duration="5"
  data-track-index="0"
  src="assets/intro.mp4"
></video>
```

`<OffthreadVideo>` 是 Remotion 特有的无头渲染优化。HF 已经运行在无头 Chrome 中，因此离线程变体降级为普通的 `<video>`。

`muted` 和 `playsinline` 是运行时自动播放所必需的（浏览器策略）。始终生成它们。

## `<Img>`

```tsx
<Img src={staticFile("logo.png")} style={{ width: 200, height: 200 }} />
```

```html
<img src="assets/logo.png" style="width: 200px; height: 200px;" />
```

宽/高四舍五入为整数像素。如果原始样式有动画尺寸，GSAP 补间会对它们进行动画 — 参见 [timing.md](timing.md)。

## `<IFrame>`

```tsx
<IFrame src="https://example.com" />
```

```html
<iframe src="https://example.com"></iframe>
```

当 HF 在合成中检测到嵌套的 iframe 时，它会自动回退到**截图模式**而不是确定性的 BeginFrame 模式。这会牺牲渲染性能但产生视觉正确的输出。详情参见 [hyperframes-vs-remotion.mdx](https://github.com/heygen-com/hyperframes/blob/main/docs/guides/hyperframes-vs-remotion.mdx)。

## `delayRender()` / `continueRender()`

```tsx
const handle = delayRender();
useEffect(() => {
  loadAsset().then(() => continueRender(handle));
}, []);
```

丢弃。HF 通过 [Frame Adapter 模式](https://hyperframes.heygen.com/concepts/frame-adapters) 等待资源就绪 — 图像、视频、字体和 Lottie 动画都原生地发出加载完成信号。应用层无需做任何事。

## 当资源不是文件时

如果 Remotion 的媒体源是 Buffer、dataURL 或 URL.createObjectURL，资源在磁盘上不存在，无法通过 setup.sh 复制。两种选择：

1. 在翻译时物化资源 — 将缓冲区写入 `hf-src/assets/` 中的文件。
2. 对于小资源（< 100 KB），直接以 data URL 嵌入 HTML（`src="data:image/png;base64,..."`）。

对于音频/视频 Buffer，首选方案 1 — base64 编码的媒体会使 HTML 臃肿并减慢渲染器速度。
