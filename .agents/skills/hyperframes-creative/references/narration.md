# 旁白与脚本

如何为视频合成编写旁白脚本。当合成包含画外音或 TTS 时阅读。

## 节奏

- **每秒 2.5 个词**是自然的说话速度
- 15 秒 ≈ 37 词。30 秒 ≈ 75 词。60 秒 ≈ 150 词
- 为停顿留出空间。句子之间的静默是一种特性，不是死寂
- 脚本应感觉比视频**更短**——视觉呼吸空间很重要

## 语气

像人一样写作，而不是宣传册：

- 使用缩写："it's"、"you'll"、"that's"、"we've"
- 变化句子长度——短促有力的短语与较长的流畅句子混合
- 大声读出来。如果听起来像机器人，就重写
- 除非受众期望，否则避免使用行话

## 数字发音

写出你希望语音说的内容。TTS 会逐字读取。

| 产品中显示 | 脚本中写作                     |
| ---------- | ------------------------------ |
| 135+       | more than one hundred thirty five |
| $1.9T      | nearly two trillion dollars       |
| 99.999%    | ninety nine point nine percent    |
| 200M+      | over two hundred million          |
| 10x        | ten times                         |
| API        | A P I                             |
| stripe.com | stripe dot com                    |

视觉可以显示确切数字，而语音将其四舍五入。

## 结构

对于产品视频：

1. **钩子** — 这个产品有什么令人惊讶或印象深刻的地方？一个大胆的主张、一个挑衅性的问题、一个对比或一个惊人的数字。这是开场白。**变化钩子类型** — 不要每次都默认为统计数据。
2. **故事** — 产品做什么？谁使用它？保持具体。
3. **证明** — 统计数据、客户名称、社交证明。来自产品的真实数据。
4. **CTA（行动号召）** — 观众应该做什么？"Start building at stripe dot com。"

并非每个视频都需要全部四个。一个 15 秒的社交广告可能只有钩子 + 证明 + CTA。一个 60 秒的产品演示使用全部四个，故事部分更丰富。

## 开场白

视频中最重要的句子。它必须在头 3 秒内创造张力、好奇心或惊喜。

有效的模式：

- **一个大胆的主张**："支撑互联网经济的金融基础设施。"
- **一个挑衅的问题**："如果你的数据库能思考呢？"
- **一个对比**："你的 AI 代理已经知道如何制作视频。它只需要正确的格式。"
- **一个令人震惊的数字**："近两万亿美元。"（谨慎使用——不是每个视频都该以统计数据开场。）

如果开场很通用（"欢迎使用 Stripe" / "介绍我们的产品"），重新开始。

## 示例

来自一个 62 秒的产品发布视频（团队参考）：

```
Your AI agent already knows how to make videos.
It just needs the right format.

This is Hyperframes. An open source framework. HTML in, video out.

A div is a keyframe. Data attributes are your timeline.
CSS is your look. G-Sap is your animation engine.

Anything a browser can render can be a frame in your video.

CSS animations. G-Sap. Lottie. Shaders. Three.js.

Drop in music, sound effects, footage — it all composes together.

No new framework for the agent to learn.
Just HTML.

The agent writes it. The renderer captures every frame as MP4.
It's deterministic. Identical outputs, every time.

Give your agent the CLI. Tell it what to make.
Watch it build.

Hyperframes. Go make something.
```

注意：62 秒约 140 词——即每秒 2.3 词，为停顿和视觉呼吸留出空间。
