---
name: remotion-best-practices
description: Remotion 最佳实践 - 使用 React 创建视频
metadata:
  tags: remotion, video, react, animation, composition
---

## 使用时机

当处理 Remotion 代码时，使用此技能获取领域特定知识。

## 字幕

处理字幕或说明文字时，加载 [./rules/subtitles.md](./rules/subtitles.md) 文件获取更多信息。

## 使用 FFmpeg

对于某些视频操作，如裁剪视频或检测静音，应使用 FFmpeg。加载 [./rules/ffmpeg.md](./rules/ffmpeg.md) 文件获取更多信息。

## 音频可视化

当需要可视化音频（频谱条、波形、低音响应效果）时，加载 [./rules/audio-visualization.md](./rules/audio-visualization.md) 文件获取更多信息。

## 音效

当需要使用音效时，加载 [./rules/sound-effects.md](./rules/sound-effects.md) 文件获取更多信息。

## 使用方法

阅读各个规则文件获取详细解释和代码示例：

- [rules/3d.md](rules/3d.md) - 使用 Three.js 和 React Three Fiber 在 Remotion 中创建 3D 内容
- [rules/animations.md](rules/animations.md) - Remotion 基础动画技能
- [rules/assets.md](rules/assets.md) - 将图片、视频、音频和字体导入 Remotion
- [rules/audio.md](rules/audio.md) - 在 Remotion 中使用音频 - 导入、裁剪、音量、速度、音调
- [rules/calculate-metadata.md](rules/calculate-metadata.md) - 动态设置合成时长、尺寸和属性
- [rules/can-decode.md](rules/can-decode.md) - 使用 Mediabunny 检查视频是否可被浏览器解码
- [rules/charts.md](rules/charts.md) - Remotion 图表和数据可视化模式（柱状图、饼图、折线图、股票图）
- [rules/compositions.md](rules/compositions.md) - 定义合成、静态图、文件夹、默认属性和动态元数据
- [rules/extract-frames.md](rules/extract-frames.md) - 使用 Mediabunny 从视频中提取指定时间戳的帧
- [rules/fonts.md](rules/fonts.md) - 在 Remotion 中加载 Google 字体和本地字体
- [rules/get-audio-duration.md](rules/get-audio-duration.md) - 使用 Mediabunny 获取音频文件时长（秒）
- [rules/get-video-dimensions.md](rules/get-video-dimensions.md) - 使用 Mediabunny 获取视频文件的宽度和高度
- [rules/get-video-duration.md](rules/get-video-duration.md) - 使用 Mediabunny 获取视频文件时长（秒）
- [rules/gifs.md](rules/gifs.md) - 显示与 Remotion 时间线同步的 GIF
- [rules/images.md](rules/images.md) - 使用 Img 组件在 Remotion 中嵌入图片
- [rules/light-leaks.md](rules/light-leaks.md) - 使用 @remotion/light-leaks 实现漏光叠加效果
- [rules/lottie.md](rules/lottie.md) - 在 Remotion 中嵌入 Lottie 动画
- [rules/measuring-dom-nodes.md](rules/measuring-dom-nodes.md) - 在 Remotion 中测量 DOM 元素尺寸
- [rules/measuring-text.md](rules/measuring-text.md) - 测量文本尺寸、适配容器和检查溢出
- [rules/sequencing.md](rules/sequencing.md) - Remotion 序列模式 - 延迟、裁剪、限制项目时长
- [rules/tailwind.md](rules/tailwind.md) - 在 Remotion 中使用 TailwindCSS
- [rules/text-animations.md](rules/text-animations.md) - Remotion 排版和文字动画模式
- [rules/timing.md](rules/timing.md) - Remotion 插值曲线 - 线性、缓动、弹簧动画
- [rules/transitions.md](rules/transitions.md) - Remotion 场景转场模式
- [rules/transparent-videos.md](rules/transparent-videos.md) - 渲染带透明度的视频
- [rules/trimming.md](rules/trimming.md) - Remotion 裁剪模式 - 裁剪动画的开头或结尾
- [rules/videos.md](rules/videos.md) - 在 Remotion 中嵌入视频 - 裁剪、音量、速度、循环、音调
- [rules/parameters.md](rules/parameters.md) - 通过添加 Zod schema 使视频参数化
- [rules/maps.md](rules/maps.md) - 使用 Mapbox 添加地图并制作动画
- [rules/voiceover.md](rules/voiceover.md) - 使用 ElevenLabs TTS 为 Remotion 合成添加 AI 生成画外音
