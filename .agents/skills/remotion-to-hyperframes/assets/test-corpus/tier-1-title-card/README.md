# 第 1 层 — title-card-fade

## 测试内容

最简单的非平凡 Remotion → HyperFrames 翻译。单个文本元素在前 0.5 秒淡入，保持 2.0 秒，然后在最后 0.5 秒淡出。没有音频、媒体或自定义组件。

如果翻译不能通过 T1，则它在最基本的核心能力上就存在问题：`AbsoluteFill`、`useCurrentFrame`、带多段输入的 `interpolate`，以及 Remotion 基于帧的驱动器和 HF 暂停 GSAP 驱动器之间的时间偏移。

## 翻译演练

| Remotion                                                      | HyperFrames                                                                                              |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `<AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>`       | `<body style="background: #0a0a0a">` + 一个定位的根 div                                                  |
| `useCurrentFrame()`                                           | 丢弃 — HF 定位时间线                                                                                     |
| `interpolate(frame, [0, 15, 75, 90], [0, 1, 1, 0])` 在 fps=30 | `gsap.timeline({ paused: true })`，在偏移 0s/0.5s/2.5s 处有三个 `.to()` 调用，每个 `ease: "none"`       |
| `<div style={{ opacity }}>HELLO</div>`                        | 静态标记；透明度由时间线动画控制                                                                         |

Remotion→HF 的时间转换是 `time = frame / fps`。因此在 30 fps 时 `[0, 15, 75, 90]` 变为 `[0, 0.5, 2.5, 3.0]` 秒。

## 如何渲染和评估

```bash
# 渲染 Remotion 基线
cd remotion-src && npm install && npm run render
# 渲染到 remotion-src/out/baseline.mp4

# 渲染 HyperFrames 翻译
cd ../hf-src && npx hyperframes render --output ../hf.mp4

# 使用评估框架进行比较（来自技能 scripts/）
../../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```

`expected.json` 记录了此测试用例的 SSIM 阈值（0.95）；针对 Remotion @ 4.0 使用 PNG/BT.709 输出校准的平均值为 0.974。
