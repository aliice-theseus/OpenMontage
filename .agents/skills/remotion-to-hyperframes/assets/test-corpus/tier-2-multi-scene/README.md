# 第 2 层 — title-image-outro

## 测试内容

三场景合成。每个场景测试不同的 Remotion 惯用用法：

1. **场景 1（0–2 秒）** — TitleScene，使用 `spring({damping:12, stiffness:100, mass:1})` 驱动文本的 `transform: scale()`。测试有损的 `spring → GSAP ease` 翻译。
2. **场景 2（2–4 秒）** — ImageScene，淡入通过 `staticFile` 加载的图片，并将其从 0.8 线性缩放到 1.0。测试资源路径 + 线性 `interpolate`。
3. **场景 3（4–6 秒）** — OutroScene，具有 1 秒线性淡入。在较难场景之后的基本正确性检查。

一个 6 秒的静音 WAV 以 `volume={0.5}` 贯穿全程。测试 `<Audio>` 翻译。

如果翻译通过 T2，说明技能正确处理了 `<Sequence>` 边界、`<Audio>` / `<Img>` / `staticFile` 以及 Remotion `spring → GSAP ease` 启发式方法。

## 翻译演练

| Remotion                                                            | HyperFrames                                                                                              |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `<Sequence from={0} durationInFrames={60}>`                         | `<div data-start="0" data-duration="2" data-track-index="0">`                                            |
| `spring({frame, fps, config: {damping:12, stiffness:100, mass:1}})` | `gsap.to(target, { scale: 1, duration: 0.7, ease: "back.out(1.4)" })`                                    |
| `<Audio src={staticFile("music.wav")} volume={0.5} />`              | `<audio src="assets/music.wav" data-start="0" data-duration="6" data-volume="0.5" data-track-index="1">` |
| `<Img src={staticFile("square.png")} />`                            | `<img src="assets/square.png">`（通过 setup.sh 复制到两个树中）                                           |
| `interpolate(frame, [0, 15], [0, 1])` 在 30 fps 时                  | `gsap.to(target, { opacity: 1, duration: 0.5, ease: "none" })`                                           |

场景交叉淡入淡出是 HyperFrames 的惯用用法，而非 Remotion 的：在场景边界处我们使用 `gsap.set(scene, { opacity: 0 })`，以便前一个场景在正确的时间消失。Remotion 通过 `<Sequence>` 的 durationInFrames 隐式实现这一点。

## 如何渲染和评估

```bash
# 1. 通过 ffmpeg 生成二进制资源（PNG + WAV）
./setup.sh

# 2. 渲染 Remotion 基线
cd remotion-src && npm install && npm run render

# 3. 渲染 HyperFrames 翻译
cd ../hf-src && npx hyperframes render --output ../hf.mp4

# 4. 比较
../../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```

## 为什么阈值是 0.95？

与 T1 相同的阈值（`expected.json` 将其编入协调器）。Spring → `back.out(1.4)` 在校准时比预测的更干净 — 验证后的平均值为 0.985，而门限为 0.95。如果翻译破坏了其他任何内容（spring 过冲错误、交错偏移、资源路径漂移），平均 SSIM 将远低于 0.95 — 这就是失败信号。
