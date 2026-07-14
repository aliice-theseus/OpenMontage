# 合成导演 — 动画管线

## 使用时机

渲染动画，重点关注文本清晰度、时机完整性和一致的输出节奏。对于 `image_animation` 方法，此阶段还包括构建合成 JSON、获取音乐、运行渲染前验证和执行渲染后自我审查。

## 运行时路由（强制第一步）

在任何其他工作之前，读取 `edit_decisions.render_runtime`。它在方案阶段已锁定，不得静默更改。本技能的其余部分假设 `render_runtime="remotion"`（此管线的默认值）。如果方案锁定了不同的运行时：

- **`render_runtime="hyperframes"`** — HTML/CSS/GSAP 渲染。不要遵循下面的 Remotion 特定部分（public/ 存放、Remotion 合成 JSON）。而是：
  1. 阅读 `skills/core/hyperframes.md` 了解完整路由模型。
  2. 阅读 `.agents/skills/hyperframes/SKILL.md` 和 `.agents/skills/hyperframes-cli/SKILL.md` 了解编写合约和 CLI 用法。
  3. 以 `edit_decisions.render_runtime="hyperframes"` 调用 `video_compose`——它会委托给 `hyperframes_compose`，后者拥有 `projects/<名称>/hyperframes/` 下的工作空间物化，运行 `hyperframes lint → validate → render`，并返回 MP4 路径。
  4. `hyperframes lint` 和 `hyperframes validate` 都必须在渲染前通过。绝不跳过 validate；在迭代期间可以通过 `skip_contrast=true` 推迟对比检查，但最终交付不可跳过。
- **`render_runtime="ffmpeg"`** — 简单拼接/裁剪，无合成。直接调用 `video_compose`；它不会自动升级到 Remotion。
- **运行时不可用** — 不要静默切换到不同的引擎。按照 AGENT_GUIDE.md > "Escalate Blockers Explicitly" 将阻塞点暴露给用户，并在切换前等待批准（在 decision_log 中记录为 `render_runtime_selection` 决策）。

渲染后自我审查（final_review）在所有运行时中相同——相同的 ffprobe 探测、帧采样、音频抽查和承诺保留检查。`final_review.checks.promise_preservation.render_runtime_used` 必须等于实际运行的运行时。

**在调用时向 `video_compose.execute()` 传递 `proposal_packet`**。这让工具直接将方案锁定的运行时与 `edit_decisions` 中记录的运行时进行比较，如果它们不同则翻转 `runtime_swap_detected=true`。没有它，检查为 `skipped`，审查者技能必须通过跨产物比较来捕获交换。

## 前置条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 产物验证 |
| 前置产物 | `state.artifacts["edit"]["edit_decisions"]`、`state.artifacts["assets"]["asset_manifest"]` | 时机计划和资产文件 |
| 工具 | `video_compose`、`audio_mixer`、`video_stitch` | 最终组装 |
| 工具 | `composition_validator` | 渲染前验证（强制） |
| 工具 | `audio_probe` | 音乐时长检查 |
| 样式手册 | 活跃的样式手册 | 渲染一致性 |
| 参考 | `remotion-composer/public/demo-props/mori-no-seishin.json` | 合成 JSON 格式参考 |
| 参考 | `skills/core/remotion.md` | Remotion 模式、anime_scene 类型、关键约束 |

## 流程

### 1. 确保资产在 Remotion 的公共目录中

**关键：** Remotion 只能通过 `staticFile()` 访问文件，该函数从 `remotion-composer/public/` 解析。生成的图像和音乐文件必须在渲染前复制或符号链接到此目录中。

```
项目结构：
  projects/<名称>/assets/images/*.png     ← 图像生成位置
  remotion-composer/public/<名称>/*.png   ← Remotion 读取位置

必需：将图像和音乐复制或符号链接到 public/<项目名>/
```

合成 JSON 中的图像路径相对于 `remotion-composer/public/`：
```json
"images": ["deep-ocean/scene1-a.png", "deep-ocean/scene1-b.png"]
"src": "deep-ocean/ambient-music.mp3"
```

**如果跳过此步骤，渲染将因文件缺失错误而失败或产生黑帧。**

### 2. 构建合成 JSON（image_animation 方法）

对于 `anime_scene` 合成，在 `remotion-composer/public/demo-props/<名称>.json` 构建一个 JSON 文件。

**必需结构：**

```json
{
  "cuts": [
    {
      "id": "scene-1-name",
      "source": "",
      "in_seconds": 0,
      "out_seconds": 5,
      "type": "anime_scene",
      "images": ["<项目>/<图像-a>.png", "<项目>/<图像-b>.png"],
      "animation": "<镜头运动>",
      "particles": "<粒子类型>",
      "particleColor": "#十六进制颜色",
      "particleCount": 20,
      "particleIntensity": 0.5,
      "backgroundColor": "#0A0A1A",
      "vignette": true,
      "lightingFrom": "rgba(r,g,b,a)",
      "lightingTo": "transparent"
    }
  ],
  "overlays": [...],
  "audio": { "music": { "src": "<项目>/music.mp3", "volume": 0.15, "fadeInSeconds": 2, "fadeOutSeconds": 3 } }
}
```

**属性名参考（JSON 字段 → AnimeScene 属性）：**

| JSON 字段 | 类型 | 值 | 必需 |
|------------|------|--------|----------|
| `type` | string | `"anime_scene"` | 是 |
| `images` | string[] | 1-4 个图像路径，相对于 `public/` | 是 |
| `animation` | string | `zoom-in`、`zoom-out`、`pan-left`、`pan-right`、`ken-burns`、`drift-up`、`drift-down`、`parallax`、`static` | 否（默认：`ken-burns`） |
| `particles` | string | `fireflies`、`petals`、`sparkles`、`mist`、`light-rays` | 否 |
| `particleColor` | string | 十六进制颜色 | 否（默认：`#FFE082`） |
| `particleCount` | number | 1-50 | 否（默认：20） |
| `particleIntensity` | number | 0-1 | 否（默认：0.6） |
| `backgroundColor` | string | 场景背景十六进制颜色 | 否（默认：`#0A0A1A`） |
| `vignette` | boolean | 电影感暗角叠加 | 否（默认：true） |
| `lightingFrom` | string | 起始渐变颜色（`rgba(...)` 或 `transparent`） | 否 |
| `lightingTo` | string | 结束渐变颜色 | 否 |

**参考：** 参见 `mori-no-seishin.json`（吉卜力森林）和 `deep-ocean.json`（水下生物发光）获取完整的工作示例。

### 3. 获取音乐并找到最佳偏移

使用 `tools/audio/pixabay_music.py` 查找匹配情绪的免版税环境音乐。

**下载后，运行音频能量分析（强制）：**

```python
from tools.analysis.audio_energy import AudioEnergy
result = AudioEnergy().execute({
    "input_path": "path/to/music.mp3",
    "video_duration_seconds": 30,  # 你的视频时长
})
data = result.data
print(f"推荐偏移：{data['recommended_offset_seconds']}s")
print(f"原因：{data['offset_reason']}")
print(f"需要循环：{data['needs_loop']}")
```

此工具：
1. **找到最佳部分** — 分析每秒响度，找到平均能量最高的 N 秒窗口。环境音乐曲目通常有安静的 intro（10-30 秒），然后主旋律才进入。
2. **推荐循环** — 如果从偏移处开始的音乐短于视频，它会告知你启用循环。

**在合成 JSON 中应用偏移：**

```json
"audio": {
  "music": {
    "src": "project/music.mp3",
    "volume": 0.15,
    "fadeInSeconds": 2,
    "fadeOutSeconds": 3,
    "offsetSeconds": 55,
    "loop": false
  }
}
```

- `offsetSeconds` — 从曲目的此点开始播放（跳过安静 intro）
- `loop` — 如果剩余音乐短于视频，设为 `true`

**如果工具显示 `needs_loop: true`：** 在合成 JSON 中设置 `"loop": true`。Remotion 将在音量淡出每循环重置的情况下无缝循环音频。

### 4. 渲染前验证（强制 — 无例外）

在每次渲染前运行 `composition_validator`：

```python
from tools.analysis.composition_validator import CompositionValidator
result = CompositionValidator().execute({
    "composition_path": "remotion-composer/public/demo-props/<名称>.json",
    "assets_root": "remotion-composer/public",
})
# result.data["valid"] 必须为 True 才能继续
```

这可以捕获：
- 缺失的图像/音频文件，会导致黑帧或渲染错误
- 无效的剪辑时机（out ≤ in）
- 音频长于视频时长

**如果验证失败，在渲染前修复问题。不要渲染无效的合成。**

### 5. 保护运动时机

不要让导出设置或粗心的合成改变停留、错开或场景转场的感知时机。

### 6. 保护文本和图表的清晰度

动画在导出时经常因文本模糊、细线浑浊或移动端构图拥挤而失败。

### 7. 渲染

```bash
cd remotion-composer
npx remotion render Explainer \
  --props="public/demo-props/<名称>.json" \
  --output="<输出路径>/final.mp4" \
  --codec=h264 --crf=18
```

**注意：** 合成名称是 `Explainer`（不是 `ExplainerVideo`）。不要指定 `src/index.ts` 作为入口点——Remotion 会自动发现它。

### 8. 渲染后自我审查（强制）

渲染后，提取场景中间帧并进行视觉检查：

```bash
# 从每个场景中间提取一帧
ffmpeg -y -i final.mp4 \
  -vf "select='eq(n\,75)+eq(n\,225)+eq(n\,375)+eq(n\,525)+eq(n\,675)+eq(n\,825)'" \
  -vsync vfr frames/scene_%02d.png
```

**检查每帧：**
- [ ] 图像可见（不是黑/暗帧）
- [ ] 粒子正在渲染（闪光、萤火虫等可见）
- [ ] 镜头运动明显（构图与静态不同）
- [ ] 叠加层在正确时刻显示，文本清晰
- [ ] 场景间调色板一致
- [ ] 暗角营造电影感深度

**同时验证输出文件：**
```bash
ffprobe -v quiet -print_format json -show_format -show_streams final.mp4
```
- 时长在目标的 ±5% 以内？
- 分辨率匹配 1920×1080？
- 音频流存在？

**如果发现问题：** 确定原因（缺失图像、时机错误、渲染故障），在呈现给用户之前修复。

### 9. 使用渲染元数据

推荐的元数据键：

- `render_fps`
- `sharpness_checks`
- `safe_zone_checks`
- `variant_outputs`

## 常见陷阱

- **忘记将资产复制到 `remotion-composer/public/`** — 渲染失败的第一大原因。图像生成到 `projects/<名称>/assets/`，但 Remotion 从 `public/` 读取。
- 渲染后文本模糊或有锯齿。
- 损害图表的压缩选择。
- 预览和最终版本之间场景节奏发生变化。
- **跳过 `composition_validator`** — 在你浪费渲染时间之前捕获缺失文件、错误时机、音频不匹配。
- **不提取帧进行自我审查** — 渲染的视频在视觉检查帧之前不算"完成"。黑帧、缺失粒子或不可见的图像并非总能通过文件大小明显判断。
- **使用 `useVideoConfig()` 的 `durationInFrames` 进行场景级的时机判断** — 这返回的是完整合成的时长，而不是场景的 Sequence 时长。参见 `skills/core/remotion.md` 的关键约束。
