# 评估：如何端到端验证翻译

每次翻译都应该被度量。该技能附带三个脚本和一个分层测试语料库，共同把关翻译质量。

## 三个脚本

| 脚本                     | 输入                           | 输出                                                                   |
| ------------------------ | ------------------------------ | ---------------------------------------------------------------------- |
| `scripts/lint_source.py` | Remotion 源码目录或文件         | JSON 结果 + 退出码（0 干净, 1 有阻断器）                                |
| `scripts/render_diff.sh` | 两个 MP4 路径                  | 逐帧 SSIM + JSON 摘要（`mean`、`min`、`p05`、`p95`、`pass`）           |
| `scripts/frame_strip.sh` | 两个 MP4 路径                  | 并排对比条 PNG，用于可视化调试                                           |

按此顺序运行：**lint → render → diff →（如果失败）strip**。

## 每个测试用例流程

```bash
# 1. 检查源码 — 阻断器表示停止
python3 ../../scripts/lint_source.py ./remotion-src/src/

# 2. 生成任何二进制资源（仅 T2+T3）
[ -f setup.sh ] && ./setup.sh

# 3. 渲染 Remotion 基线
cd remotion-src && npm install && npm run render
# -> remotion-src/out/baseline.mp4

# 4. 渲染 HF 翻译
cd .. && node ../../../packages/cli/dist/cli.js render hf-src/ --output hf.mp4
# -> hf.mp4

# 5. SSIM 差异比较
../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
# -> diff/summary.json

# 6. 如果差异比较失败，生成帧条用于视觉检查
../../scripts/frame_strip.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./strip 8
# -> strip/strip.png
```

## 读取 `diff/summary.json`

```json
{
  "frame_count": 90,
  "mean": 0.974,
  "min": 0.972,
  "max": 0.999,
  "p05": 0.972,
  "p95": 0.983,
  "threshold": 0.95,
  "pass": true
}
```

| 字段           | 含义                                                                       |
| -------------- | -------------------------------------------------------------------------- |
| `mean`         | 所有帧的平均 SSIM；核心指标                                                  |
| `min`          | 最差帧；低于阈值表示至少有一帧存在结构性错误                                   |
| `p05` / `p95`  | 第 5 / 第 95 百分位 — 大多数帧落在此范围内                                    |
| `threshold`    | 来自 `R2HF_SSIM_THRESHOLD` 环境变量（默认 0.85）                             |
| `pass`         | `mean >= threshold` 是否成立                                                 |

## 已验证的分层阈值

针对实际的 Remotion + HF 渲染进行校准：

| 层级 | 合成形状                               | 平均 SSIM | 阈值    | 余量     |
| ---- | -------------------------------------- | --------- | ------- | ------ |
| T1   | 单元素淡入                             | 0.974     | 0.95    | +0.022 |
| T2   | 多场景 + spring + 音频 + 图片          | 0.985     | 0.95    | +0.016 |
| T3   | 数据驱动、自定义子组件、计数动画         | 0.953     | 0.90    | +0.038 |

每个测试用例的 `expected.json` 包含：

- `ssim_threshold` — `pass` 的阈值门限
- `validation` — 校准运行的实际测量数据
- `translation_notes` — 有损部分及原因

## 关键：编码器配置

Remotion 和 HF 必须输出相同的像素格式，SSIM 才有意义。Remotion 的默认 JPEG 输出写入 `yuvj420p`（全范围）；HF 输出 `yuv420p`（有限范围）。这种不匹配会导致约 ~0.05 SSIM 的损失。

每个测试用例的 `remotion.config.ts` 设置：

```ts
Config.setVideoImageFormat("png");
Config.setColorSpace("bt709");
```

如果用户的源码没有这些设置，在翻译步骤中添加它们 — 否则差异比较测量的是编码器差异，而非翻译保真度。

## 噪声基底的表现

主要的非翻译噪声是**系统字体回退差异**。Remotion 捆绑的 Chromium 和 HF 的 `chrome-headless-shell` 在没有安装真实字体时对 `font-weight: 800` 的解释不同：

- Remotion 中 160px 的 HELLO：中等粗细笔画
- HF 中 160px 的 HELLO：粗笔画

这造成约 ~0.025 的平均 SSIM 损失。在 T1 的帧条中可见。[fonts.md](fonts.md) 介绍了如何缓解（使用 Inter、加载显式的 Google Fonts）。

## 阈值经验法则

将阈值设置在测量的 `p05` 以下约 ~0.02：

- 真正的翻译回归会导致均值下降 0.05 以上 — 会被捕获。
- CI 运行间的编码器/字体漂移被限制在约 ~0.01 — 不会被捕获。

如果校准运行测量的均值远高于你最初的阈值猜测，_不要_收紧阈值来拟合。留出余量 — 在不同硬件上重新渲染的测试用例会发生漂移。

## 当差异比较失败时

1. **首先查看 `frame_strip.sh` 的输出。** 6–10 个均匀间隔时间戳的并排对比条可以显示失败是结构性的（错误的场景时长、缺少元素）还是外观性的（不同的字体粗细、轻微的时间偏差）。
2. **检查 `diff/ssim.log`。** 逐帧 SSIM 告诉你_哪些_帧失败了。场景中间的不良帧簇 = 动画问题；场景边界的不良帧 = 序列问题。
3. **重新阅读相关参考。** 弹簧/缓动问题参见 [timing.md](timing.md)，场景边界问题参见 [sequencing.md](sequencing.md)，资源加载问题参见 [media.md](media.md)。

## CI 集成

这些测试用例尚未接入 CI（`packages/producer/tests/` 在 Docker 内运行；技能语料库需要同样的环境）。PR 7 添加了运行所有四个层级并输出聚合通过报告的组织器。目前，手动评估每个测试用例。
