# 规划（步骤 3）——选择品牌，填充每帧

在步骤 3 **你（编排器）**将步骤 2 的骨架变成完整的、已批准的 `STORYBOARD.md`。你原地编辑**同一个文件**：选择品牌脊柱，然后为每帧决定其**组**，为每个组分配处理方式，绑定真实节拍锚点，编写文案。

你的口头禅：**音乐是脊柱；模板是起点，不是牢笼；排版是底线，资源是同一节拍网格上的可选配料。**

**你拥有 WHAT，不拥有 HOW。** 你命名模板/原语、内容、品牌、锚点秒数和意图。frame-worker（步骤 4）决定 HOW——微时序、实现、帧内剪切。**永远不要将毫秒级动画写入故事板。**

## 输入

- 已在 `STORYBOARD.md` 中的步骤 2 骨架——帧带 `span_sec` + `pacing` + `mood` + `feel`。
- `audiomap.json`——时序真相；读取每帧跨度内的真实锚点秒数。
- [`template-catalog.md`](template-catalog.md)——模板选择菜单。
- [`motion-primitive-catalog.md`](motion-primitive-catalog.md)——自由组合菜单（L0 配方）。
- [`montage.md`](montage.md)——资源处理方式（仅当用户提供了图片/视频时）。
- 用户简报/提供的文案——主题、情绪、要保留的确切词语。

## 步骤 A——选择品牌脊柱（一个预设，未经修改）

整个视频共享一个字体家族 + 调色板。从 `../hyperframes-creative/frame-presets/` 中使用 `../hyperframes-creative/references/design-spec.md` 中的预设表选择一个**现成预设**——按曲目情绪 + 简报选择，并**只有其字体 + 颜色重要**（模板拥有作品 + 动效；预设只设置外观）。**未经修改**地复制：

```bash
cp ../hyperframes-creative/frame-presets/<preset>/FRAME.md "$PROJECT_DIR/frame.md"
```

然后从中填充故事板前置元数据 `style`：`font` 来自其 `typography:` 和 ≤4–6 色板 `palette` 来自其 `colors:`。**逐字引用十六进制/家族——永远不要发明或四舍五入。** 每个组的调色板参数从这个调色板中提取；这种统一性使不同模板读起来像一体的。

## 步骤 B——每帧，决定其组

一帧通常是**一个组**（一个模板或一个自由组合跨越整个帧）。**仅当单一处理方式不能覆盖帧时才细分为 2+ 组**——例如一个繁忙的开场加上一个结尾词组。当你拆分时，在帧跨度内的一个**真实音频锚点**处切割（一个 `key_moment` / `phrase` 边沿 / 起始集群间隙），**永远不在 `rolls[]` 运行内部**，并保持每个组**≥ 约 1 小节**。密度并**不**强制更多组——密集帧通常是一个组，其模板内部吸收了密度（元模板如 `poster-tile-mosaic`）。**组计数跟踪不同的处理方式，而不是节拍。**

## 步骤 C——每个组，选择处理方式（三种之一）

### A. 匹配模板

阅读 [`template-catalog.md`](template-catalog.md)。将组的 `feel` + `mood` + `pacing` 与模板的**适合时机**匹配；取最接近的匹配。然后绑定它：

- 填充 `params`（来自目录条目的键）——你的文案放入文本槽，调色板来自品牌脊柱，`duration` = 组的跨度长度。
- 用此组从其跨度上 `audiomap.json` 中读取的**真实锚点秒数**（不是示例时间）填充 `role_bindings`。
- 如果模板的自然停止和组的跨度结束不一致，对齐到最近的锚点。

### B. 自由组合（没有模板匹配）

写一个 `free_design`——来自 [`motion-primitive-catalog.md`](motion-primitive-catalog.md) 的一个视觉主题（一个主导系统 + 命名的 L0 原语 + 密度拓扑）+ `anchors`（动作依托的真实节拍/起始秒数）。自由组合是一个**一等**选择，写得像匹配组一样仔细——永远不是失败。

### C. 资源处理方式（仅当用户提供了资源且它们适合时）

使其成为一个 `asset` 组（[`montage.md`](montage.md)）。**遵循 `pacing`：** 在 `beat_cut` 帧上使用 `beat_cut`（每个锚点一个片段）或 `bg_under_text`；在 `phrase_flow` 帧上使用 `ken_burns` 或慢交叉淡入淡出——**永远不要**每次起始硬切。资源是附加的：如果没有适合组，回退到模板/自由（排版是底线——完整视频不需要资源）。

## 文案（你拥有词语）

- 保留用户的确切词语；否则有品味地创造，符合简报情绪。
- **信息 vs 纹理：** 一个可读的词保持 ≥1 节拍（标题 3–8、句子 4–10），稳定 + 聚焦；一个保持 <1 节拍的词是纹理（频闪/网格/滴答）。永远不要将信息强加给子节拍——将其降级为纹理。
- 将文案放入模板的文本参数、自由组的锚点上，或作为资源组的 `overlay_copy`。声明锚点 + 累积/交错意图；将微时序留给 worker。
- 结尾 Logo / CTA 在最终命中/硬停止上落地并通过拖尾静默保持。

## 过渡（你不发出它们）

现在一切都是 **0ms 硬切**。**帧 → 帧**由组装器拥有（背靠背文件）；相邻的 `span_sec` 已经暗含了切。**帧内组 → 组**由 worker 在其帧时间线上拥有；你只设置每个组的 `span_sec`。

## 编写 + 验证

完成 `STORYBOARD.md`（[`storyboard-format.md`](storyboard-format.md)），然后运行 `node scripts/validate-plan.mjs` 并修复每个 `✗`。向用户显示逐帧摘要并迭代直到批准。

## 自我检查

- `frame.md` 是一个预设的逐字副本；前置元数据 `style.font` / `style.palette` 从中提取（精确值）。
- 每帧变成了 ≥1 组；组按顺序平铺帧跨度；没有组 < 约 1 小节；没有组边界在 `rolls[]` 运行内部。
- 每个组正好是 template / free_design / asset 之一。
- 模板 `params` 键匹配目录条目；`role_bindings` / `anchors` 使用真实的 audiomap 秒数。
- 资源处理方式遵循 `pacing`（`phrase_flow` 帧上没有 `beat_cut`）。
- 每个组的调色板从一个品牌调色板中提取。
- `duration_s == audiomap.audio.duration_sec`；`validate-plan.mjs` 通过。
