# Remotion 技能

## 使用时机

从第三阶段开始，在需要基于 React 的场景组装、参数化模板、动画叠加层、转场或数据驱动的批量渲染时，使用 Remotion 进行高级视频合成。对于简单的剪切、烧录和编码，优先直接使用 FFmpeg。

## 与 Remotion Agent 技能的关系

**已安装的 agent 技能**（`.agents/skills/remotion-best-practices/`）教授正确的 Remotion API 用法——导入、时机、动画约束、代码模式。**本文件**教授 OpenMontage 如何使用 Remotion——哪些合成映射到流水线阶段、工件如何流入、以及渲染如何触发。

## Remotion 优先路由

**Remotion 是所有最终渲染的默认合成引擎（当可用时）。** 它通过基于 React 的单一渲染过程处理视频片段（通过 `<OffthreadVideo>`）、静态图像、动画场景、组件类型、转场和混合内容。

FFmpeg 是**回退方案**——仅在 Remotion 不可用时，或用于不需要 React 渲染的简单独立操作时使用。

| 使用场景 | 后端 | 原因 |
|----------|---------|-----|
| 最终视频渲染（任何内容类型） | **Remotion** | 所有合成的默认选择 |
| 视频片段 + 动画静态图 + 文字卡片 | **Remotion** | 混合内容一次渲染完成 |
| 纯视频剪辑加转场 | **Remotion** | 原生 `<OffthreadVideo>` + 转场 |
| 动画图表/文字卡片 | **Remotion** | 逐帧控制 |
| 数据驱动批量视频 | **Remotion** | Zod props + 参数化渲染 |
| 单词级字幕（合成内） | **Remotion** | CaptionOverlay 带单词高亮——优于 SRT |
| 音频嵌入（旁白 + 音乐） | **Remotion** | 原生 `<Audio>` 组件，支持音量/淡入淡出 |
| 简单裁剪、拼接（无合成） | FFmpeg | 即时处理，无需 Node 依赖 |
| 字幕烧录（独立、事后处理） | FFmpeg | 仅用于向已渲染完成的视频添加字幕而无需重新渲染 |
| 人脸增强、调色 | FFmpeg | 基于滤镜，确定性 |
| Remotion 不可用 | FFmpeg | 自动回退 |

**注意：** `render` 操作默认自动路由到 Remotion。仅当 Remotion 未安装或 agent 显式调用 `operation='compose'` 进行独立操作时，才会选择 FFmpeg。当现有合成不覆盖特定布局时（例如自定义画中画、分屏），agent 还可以通过能力扩展协议即时编写自定义 Remotion 合成。

## 支持的场景类型（剪辑类型）

Explainer 合成支持以下剪辑类型：

| 类型 | 所需属性 | 最佳用途 |
|------|---------------|----------|
| `text_card` | `text` | 陈述、标题、结尾信息 |
| `stat_card` | `stat`，可选 `subtitle`、`accentColor` | 大数字、有影响力的指标 |
| `hero_title` | `text`，可选 `heroSubtitle` | 开场标题、震撼揭示 |
| `callout` | `text`，可选 `title`、`callout_type`（info/warning/tip/quote） | 提示、引用、重要说明 |
| `comparison` | `leftLabel`、`rightLabel`、`leftValue`、`rightValue` | 前后对比、A/B 测试、对决 |
| `bar_chart` | `chartData` [{label, value}]，可选 `title`、`chartAnimation` | 类别比较、排名 |
| `line_chart` | `chartSeries` [{label, data: [{x,y}]}]，可选 `title` | 趋势、时间序列、增长 |
| `pie_chart` | `chartData` [{label, value}]，可选 `donut`、`centerLabel` | 比例、构成分析 |
| `kpi_grid` | `chartData` [{label, value, prefix, suffix, change, icon}] | 仪表盘、增长指标 |
| `progress_bar` | `progress`（0-100），可选 `progressSegments` | 进度可视化、完成度、堆叠指标 |
| `anime_scene` | `images`（1-4 个路径），可选 `animation`、`particles`、`particleColor`、`particleCount`、`particleIntensity`、`vignette`、`lightingFrom`、`lightingTo` | 动漫/吉卜力风格场景，包含多图交叉淡入淡出、摄像机运动、粒子叠加 |

**图表动画：** `grow-up`、`slide-in`、`pop`（柱状图）、`draw`、`fade-in`（折线图）、`spin`、`expand`、`sequential`（饼图）、`count-up`、`pop`、`cascade`（KPI）

### 动漫场景——多图交叉淡入淡出 + 粒子

`anime_scene` 类型渲染 1-4 张图像，带有平滑的交叉淡入淡出转场、电影级摄像机运动和动画粒子叠加。这可以从静态图像中创造出动画般的视觉效果。

**摄像机运动类型：** `zoom-in`、`zoom-out`、`pan-left`、`pan-right`、`ken-burns`、`drift-up`、`drift-down`、`parallax`、`static`

**粒子类型：** `fireflies`（飘浮的金色光球）、`petals`（飘落的樱花）、`sparkles`（闪烁的星星）、`mist`（飘动的雾层）、`light-rays`（晨光射线）

**关键属性：** `sceneDurationSeconds` 由 `SceneRenderer` 自动传入——这修复了一个关键的 Remotion 陷阱，即 `useVideoConfig().durationInFrames` 返回的是整个合成的时长，而非场景的 Sequence 时长。

**多图交叉淡入淡出算法：** 每张图像拥有相等的时间段。图像 N 的淡出和图像 N+1 的淡入在 `crossfadeDur`（约1.2秒）内重叠，确保不会出现空白帧。从同一视觉系统为每个场景生成 2-3 张图像，但改变镜头、主体和光照节奏。相近的随机种子有助于创造微妙动画，而不会让整个序列因重复提示而变得平淡。

**参考合成：** `remotion-composer/public/demo-props/mori-no-seishin.json`——6个动漫场景，30秒，包含粒子、灯光、叠加和氛围音乐。

**风格手册：** `styles/anime-ghibli.yaml`——以吉卜力为灵感的美学风格，包含调色板、字体排版、运动参数和 FLUX 提示前缀。

**零素材视频策略：** 当无法生成图像或视频时，完全通过这些组件类型构建整个视频。精心编排的 hero_title → kpi_grid → bar_chart → comparison → stat_card → text_card 序列可以制作出精致、专业的视频，无需任何外部依赖。

### 零素材视频的可靠公式

以下规则是通过系统化渲染测试发现的，能够产生电影级效果：

**1. 每个视频只使用一个背景系列。** 使用从风格手册或自定义标识中衍生的连贯背景处理方案，而不是强制每个序列都使用相同的深色仪表盘风格。这可以避免刺眼的白↔深色闪动转场，并使图表颜色更加突出。目标是视觉连贯性，而非强制使用深色主题。

**2. 扁平属性格式。** 所有场景属性直接放在剪辑对象的顶层（例如 `cut.text`、`cut.chartData`），而不是嵌套在 `props` 键下。

**3. KPI 网格数据规则：**
- `value` 必须是一个小型的、人类可读的数字。组件自动格式化 ≥1M 为 "XM"，≥1K 为 "XK"。对于 "8.1 Billion"，使用 `value: 8.1, suffix: " Billion"`。切勿使用原始大数字加后缀。
- `change` 必须是**数字**（例如 `3.2`），而不是字符串（例如**不要**使用 `"+3.2%"`）。

**4. Comparison 和 Callout 主题：**
- `comparison` 接受 `backgroundColor` 和 `color`（文字颜色）以支持深色主题。
- `callout` 接受 `backgroundColor`，同时设置容器和卡片背景。

**5. 叠加层增加精致感。**
- `section_title` 叠加层在叙事上对场景进行分组（"危机"、"数据"）。
- `stat_reveal` 叠加层在图表场景上浮动醒目数字（例如角落里的 "10x"）。

**6. 场景节奏：** 每个场景 4-6 秒，45-50 秒的视频使用 8-10 个场景。给图表动画至少 4 秒完成。标题场景只需要 4 秒。

**7. 调色板连贯性。** 选择 4-5 个与主题相关的强调色，并在图表、叠加层和装饰中一致使用。在柱状图/饼图/折线图场景中使用相同的 chartColors 数组以保持视觉统一。

**参考合成：** 参见 `remotion-composer/public/demo-props/climate-dashboard.json` 作为黄金标准，以及其他演示文件中的更多模式。

### 渲染前验证（必须执行）

**在渲染之前，务必运行 `composition_validator`。** 它能捕获以下问题：
- 缺失的资源文件（图片、音频），会导致渲染失败
- 旁白音频时长超过视频时长（音频会被截断）
- 音乐短于视频（结尾出现静音）
- 无效的剪辑时序（out ≤ in）

```python
from tools.analysis.composition_validator import CompositionValidator
result = CompositionValidator().execute({
    "composition_path": "path/to/composition.json",
    "assets_root": "remotion-composer/public",
})
# result.data["valid"] 在渲染前必须为 True
```

**音频时长对齐：**
- 生成 TTS 旁白后，工具会返回 `audio_duration_seconds`。
- 如果旁白超过视频时长：缩短脚本并重新生成，或延长最后一个场景。
- 使用 `tools.analysis.audio_probe.probe_duration(path)` 检查任何音频文件的时长。
- 音乐应 ≥ 视频时长；播放器通过 `fadeOutSeconds` 处理淡出。

## 架构

```
remotion-composer/
├── src/
│   ├── Root.tsx              # 合成注册表
│   ├── compositions/         # 每种流水线类型一个文件
│   │   ├── Explainer.tsx     # 生成的讲解合成
│   │   ├── AnimatedScene.tsx # 单个动画场景
│   │   └── TitleCard.tsx     # 独立标题卡片
│   ├── components/           # 可复用的视觉构建块
│   │   ├── Caption.tsx       # 字幕/说明文字渲染器
│   │   ├── DiagramOverlay.tsx
│   │   ├── ProgressBar.tsx
│   │   └── TransitionWrapper.tsx
│   └── styles/               # Tailwind + 风格手册派生样式
├── public/                   # 静态资源（字体、LUT）
├── package.json
├── remotion.config.ts
└── tsconfig.json
```

## 流水线集成

### 工件到 Remotion 属性的映射

| OpenMontage 工件 | Remotion 属性 | 映射目标 |
|---------------------|---------------|---------|
| `scene_plan.json` → `scenes[]` | `scenes` 属性 | `<TransitionSeries>` 子元素 |
| `scene.type` | 组件选择器 | `talking_head` → `<Video>`、`diagram` → `<DiagramOverlay>` 等 |
| `scene.start_seconds` / `end_seconds` | `from` / `durationInFrames` | `fps * 秒数` 转换 |
| `scene.transition_in` / `transition_out` | `<TransitionSeries.Transition>` | `fade`、`slide`、`wipe` |
| `asset_manifest.json` → assets | `assets` 属性 | `staticFile()` 或绝对路径 |
| `style_playbook` | `theme` 属性 | 颜色、字体、动画曲线 |
| `edit_decisions.json` → cuts | `cuts` 属性 | `<Series>` 包含裁剪后的 `<Video>` 片段 |
| `media_profile` | 合成尺寸 | 来自配置文件的 `width`、`height`、`fps` |

### 渲染调用

编排器通过 CLI 调用 Remotion 渲染：

```bash
# 标准渲染（合成名称为 "Explainer"，无需入口点）
npx remotion render Explainer \
  --props="public/demo-props/my-video.json" \
  --output=output/final.mp4 \
  --codec=h264 --crf=18

# 指定媒体配置
npx remotion render Explainer \
  --width=1080 --height=1920 --fps=30 \
  --props="public/demo-props/my-video.json" \
  --output=output.mp4
```

**注意：** 不要将 `src/index.ts` 指定为入口点——Remotion 会自动发现合成。合成名称为 `Explainer`（不是 `ExplainerVideo`）。

在 Python 中，当 `backend="remotion"` 时，通过 `video_compose.py` 中的 `subprocess` 调用。

### 媒体配置映射

| OpenMontage 配置 | Remotion 配置 |
|--------------------|-----------------|
| `youtube_landscape` | `width: 1920, height: 1080, fps: 30` |
| `youtube_shorts` | `width: 1080, height: 1920, fps: 30` |
| `tiktok_vertical` | `width: 1080, height: 1920, fps: 30` |
| `instagram_reels` | `width: 1080, height: 1920, fps: 30` |
| `instagram_square` | `width: 1080, height: 1080, fps: 30` |
| `cinematic_wide` | `width: 2560, height: 1080, fps: 24` |

## 关键模式

### 场景计划到合成

`scene_plan.json` 中的每个场景都成为 `<TransitionSeries>` 的子元素：

```tsx
// 伪代码——实际组件在 remotion-composer/src/compositions/Explainer.tsx 中
const Explainer: React.FC<ExplainerProps> = ({ scenes, theme, assets }) => {
  return (
    <TransitionSeries>
      {scenes.map((scene, i) => (
        <React.Fragment key={scene.id}>
          {scene.transition_in && (
            <TransitionSeries.Transition
              presentation={mapTransition(scene.transition_in)}
              timing={timing({ durationInFrames: 15 })}
            />
          )}
          <TransitionSeries.Sequence durationInFrames={secondsToFrames(scene)}>
            <SceneRenderer scene={scene} theme={theme} assets={assets} />
          </TransitionSeries.Sequence>
        </React.Fragment>
      ))}
    </TransitionSeries>
  );
};
```

### 使用 calculateMetadata 实现动态时长

当 TTS 音频决定视频长度时（生成的讲解视频），使用 `calculateMetadata`：

```tsx
export const ExplainerVideo = {
  component: Explainer,
  calculateMetadata: async ({ props }) => {
    const totalDuration = props.scenes.reduce(
      (sum, s) => sum + (s.end_seconds - s.start_seconds), 0
    );
    return {
      durationInFrames: Math.ceil(totalDuration * props.fps),
      fps: props.fps,
      width: props.width,
      height: props.height,
    };
  },
};
```

### 风格手册到主题

风格手册（`skills/styles/`）定义视觉参数。将其映射到 Remotion 主题：

```tsx
// 源自风格手册 YAML
const cleanProfessional = {
  background: "#FFFFFF",
  text: "#1A1A1A",
  accent: "#2563EB",
  fontFamily: "Inter",
  headingWeight: 600,
  transitionType: "fade",
  transitionDuration: 15, // 帧数
  animationEasing: "easeInOutCubic",
};
```

### 音频分层

旁白 + 背景音乐 + 音效作为并行的 `<Audio>` 组件。

**音乐偏移和循环：** `audio.music` 配置支持：
- `offsetSeconds`——跳过安静的引子，从曲目最有能量的部分开始。使用 `tools/analysis/audio_energy.py` 自动寻找最佳偏移量。
- `loop`——如果音乐短于视频则循环播放。Remotion 原生支持。
- `fadeInSeconds` / `fadeOutSeconds`——在开始/结束时平滑音量渐变。

```json
"audio": {
  "music": {
    "src": "project/music.mp3",
    "volume": 0.15,
    "offsetSeconds": 55,
    "loop": false,
    "fadeInSeconds": 2,
    "fadeOutSeconds": 3
  }
}
```

```tsx
<AbsoluteFill>
  <Audio src={narrationUrl} />
  <Audio src={musicUrl} volume={0.06} startFrom={offsetFrames} loop />
  {sfxCues.map(cue => (
    <Sequence key={cue.id} from={secondsToFrames(cue.time)}>
      <Audio src={cue.url} volume={cue.volume} />
    </Sequence>
  ))}
  {/* 视觉层 */}
</AbsoluteFill>
```

### 成本追踪

Remotion 渲染是 CPU 密集型但 API 成本为 $0。通过 cost_tracker 追踪：
- `estimate`：基于合成时长 × 分辨率级别
- `reserve`：0（无 API 支出）
- `reconcile`：壁钟渲染时间，用于基准测试

## 关键约束

- **不要使用 CSS 动画或转场**——它们无法正确渲染。所有运动使用 `useCurrentFrame()` + `interpolate()`。
- **不要使用 Tailwind 动画类**——`animate-*` 类会破坏基于帧的渲染。静态 Tailwind 工具类可以正常使用。
- **始终对 interpolate() 进行钳制**——使用 `extrapolateLeft: 'clamp', extrapolateRight: 'clamp'` 防止值超出端点。
- **`useVideoConfig().durationInFrames` 返回的是合成的时长，而不是 Sequence 的时长**——这是 Remotion 的头号陷阱。如果你的合成是 31 秒（930 帧），而场景的 `<Sequence>` 是 5 秒（150 帧），`durationInFrames` 在该场景内部仍然返回 930。任何直接使用 `durationInFrames` 的交叉淡入淡出、摄像机运动或时机逻辑都会大错特错。**修复方法：** 从父组件传入 `sceneDurationSeconds` 作为属性，并在组件内部计算 `effectiveDuration = Math.round(sceneDurationSeconds * fps)`。`AnimeScene` 组件实现了这一模式。
- **需要 Node.js 18+**——在最低系统中列为可选，推荐系统中为必需。
- **依次渲染，不要并行**——除非机器有足够的内存。每个渲染会启动一个 Chromium 实例。

## 渲染后验证协议（所有流水线）

**每次 Remotion 渲染在呈现给用户之前必须经过验证。** 此协议适用于所有流水线，不仅仅是讲解视频。流水线特定的 compose-director 可以扩展它，但不得跳过任何步骤。

**步骤 1：探测输出文件（关卡——阻止所有其他步骤）：**
```bash
ffprobe -v quiet -print_format json -show_format -show_streams rendered_video.mp4
```
验证所有项目：
- [ ] 视频流存在且分辨率和 FPS 正确
- [ ] **音频流存在**——如果缺失，立即停止，修复音频配置，重新渲染
- [ ] 时长在目标的 ±5% 范围内
- [ ] 文件大小合理（不是 0 字节，也不异常地小）

**如果缺少音频流，请不要继续。** 这意味着旁白/音乐未被嵌入。最常见的原因：音频源在外部混合但从未传入 Remotion 的 `audio` 属性。修复方法：将 `audio.narration` 和 `audio.music` 添加到合成属性并重新渲染。

**步骤 2：在场景中间点提取审核帧**，并目视检查每一帧。

**步骤 3：使用 WhisperX/transcriber 工具转写渲染视频的音频。**
- 如果返回 0 个单词 → 音频虽然存在流但为静音 → 调查原因
- 如果单词数 < 脚本的 80% → 音频被截断 → 调查原因
- 比较最后一个转写的单词与脚本的最后一个单词

**步骤 4：向用户呈现结构化审核报告**，包含文件统计、音频验证结果、视觉发现和字幕状态，然后才能宣布视频完成。

## 质量检查清单

- [ ] 合成时长等于各场景时长之和减去转场重叠部分
- [ ] 所有 `staticFile()` 引用解析到已存在的资源
- [ ] 转场不会截断内容（在时机中考虑重叠部分）
- [ ] **渲染输出中存在音频流**（ffprobe 确认 codec_type: "audio"）
- [ ] **旁白单词已通过转写验证**（不仅仅是假设属性正确）
- [ ] 音频层与视觉场景同步
- [ ] 字幕/说明文字渲染正确（优先使用 Remotion CaptionOverlay 而非 FFmpeg SRT）
- [ ] 主题颜色与激活的风格手册一致
- [ ] 输出分辨率和 FPS 匹配目标媒体配置
- [ ] 渲染完成且无 Chromium 超时错误
- [ ] 最终输出在目标平台上播放正常
- [ ] 包含文字的场景（CTA、标题）使用 Remotion 的 text_card，而非 AI 生成的带文字图像
