# lint, validate, inspect, snapshot

正确性检查流水线。按此顺序运行：`lint`（静态、快速）→ `validate`（运行时、无头 Chrome）→ `inspect`（布局扫描）。`snapshot` 是用于捕获静态帧的独立工具。

## 规范（运动密集型工作）

当组合是动画驱动时，在进入 `preview` 或 `render` 之前运行检查：

- 在第一次 HTML 通过后尽快运行 `lint`——早比晚好。
- 在有意义的时间线状态捕获 `snapshot`；查看 PNG。
- _在_ 调整自动警告之前检查快照——您的眼睛能捕捉到审计器遗漏的问题。
- 将布局警告视为缺陷，除非快照证明溢出是有意的，此时用 `data-layout-allow-overflow` 标记。
- 在 `*.motion.json` sidecar 文件中说明运动意图，以便 `inspect` 自动检查——入场动画在搜索时触发、排序顺序、帧内位置、活跃性。这是最接近"观看 MP4"的自动化代理，能捕捉眼睛遗漏的渲染≠预览错误（参见下面的**运动验证**）。

## lint

```bash
npx hyperframes lint                  # 当前目录
npx hyperframes lint ./my-project     # 指定项目
npx hyperframes lint --verbose        # 信息级别发现
npx hyperframes lint --json           # 机器可读
```

检查 `index.html` 和 `compositions/` 中的所有文件。报告错误（必须修复）、警告（应该修复）和信息（使用 `--verbose`）。捕获缺少的 `data-composition-id`、同一 `data-track-index` 上的重叠轨道以及未注册的时间线。

**盲区——子组合内的媒体（尚未有 lint 规则）。** `compositions/*.html` `<template>` 内（或嵌套在任何包装器 `<div>` 中）的 `<video>`/`<audio>` 永远不会被搜寻/解码，渲染为空白/黑色；`lint`/`validate`/`inspect` 都通过。媒体必须是 host root（`index.html`）的直接子元素——参见 `hyperframes-core` → `variables-and-media.md`。在规则存在之前，请在渲染前手动检查：

```bash
grep -nE '<(video|audio)\b' compositions/*.html   # 预期没有匹配项；媒体属于 index.html
```

非空结果是缺陷。然后对每个包含视频的场景使用 `snapshot`，确认面板实际显示画面内容（应该播放剪辑的地方出现空白/黑色面板是错误，不是占位符——将其视为阻塞渲染的问题）。

## validate

```bash
npx hyperframes validate              # 当前目录
npx hyperframes validate ./my-project # 指定项目
npx hyperframes validate --json       # 代理可读的发现
npx hyperframes validate --timeout 5000  # 等待脚本的毫秒数（默认 3000）
npx hyperframes validate --no-contrast   # 迭代时跳过 WCAG 对比度审计
```

静态 lint 很快但无法发现运行时失败。`validate` 在无头 Chrome 中加载组合，播放它，并报告：

- JavaScript 控制台错误和未处理的异常
- 失败的网络请求（媒体文件 `ERR_ABORTED` 被过滤掉）
- 可见文本的 WCAG AA 对比度违规——在时间线上采样 5 个时间戳。使用 `--no-contrast` 禁用。

**修复对比度警告**——阈值为普通文本 4.5:1，大号文本 3:1（24px+ 或 19px+ 粗体）：

- 在深色背景上，提高失败颜色亮度直到通过阈值；在浅色背景上，降低其亮度。
- 保持在调色板系列内——不要发明新颜色，调整现有颜色。
- 重新运行 `validate` 直到干净。

当动画有脚本、获取的数据或主题时，在 `inspect` 之前运行 `validate`。在 CI 中与 `render --strict` 结合使用。

## inspect

```bash
npx hyperframes inspect                 # 检查时间线上的渲染布局
npx hyperframes inspect ./my-project    # 指定项目
npx hyperframes inspect --json          # 代理可读的发现（schemaVersion、samples、issues、bboxes）
npx hyperframes inspect --samples 15    # 更密集的时间线扫描（默认 9）
npx hyperframes inspect --at 1.5,4,7.25 # 显式主角帧时间戳
npx hyperframes inspect --tolerance 4   # 报告前允许的溢出像素数（默认 2）
npx hyperframes inspect --strict        # 警告也退出非零（默认仅错误）
```

在 `lint` 和 `validate` 之后使用，特别是对于包含对话气泡、卡片、字幕或紧凑排版的组合。它报告：

- 文本延伸到最近的视觉容器或气泡外部
- 文本被其自身的固定宽度/高度框裁剪
- 文本延伸到组合画布外部
- 子元素逃逸裁剪容器

错误应在渲染前修复。警告供代理审查；添加 `--strict` 也可在警告时失败。重复的静态问题默认折叠，使 JSON 输出对 LLM 上下文窗口保持紧凑。

**逃生口：**

- `data-layout-allow-overflow` — 当溢出是入场/退场动画的有意行为时，标记元素或祖先。
- `data-layout-ignore` — 标记永远不应被审计的装饰性元素。

`npx hyperframes layout` 作为相同视觉检查的兼容别名仍然可用。

### 运动验证（`*.motion.json` sidecar）

`inspect` 还根据渲染器使用的相同搜索时间线检查**运动意图**——这是最接近"渲染 MP4 并观看"的自动化代理。它能捕获布局采样无法发现的渲染≠预览错误：搜索已经过晚的入场揭示、错误的排序顺序、在补间过程中漂移到帧外的元素、冻结的镜头。

在组合旁边放置一个 `*.motion.json` sidecar 文件（当多个组合共享一个目录时，匹配 html 基本名称）。`inspect` 自动发现它——无需标志、无需创作框架更改。没有 sidecar 时，`inspect` 行为完全不变。

```json
{
  "duration": 6,
  "assertions": [
    { "kind": "appearsBy", "selector": "#headline", "bySec": 0.5 },
    { "kind": "before", "a": "#headline", "b": "#cta" },
    { "kind": "staysInFrame", "selector": ".card" },
    { "kind": "keepsMoving", "withinSelector": ".scene" }
  ]
}
```

| 断言                             | 失败（代码）时                                                                       |
| -------------------------------- | ------------------------------------------------------------------------------------ |
| `appearsBy(selector, bySec)`     | 在 `bySec` 时不可见（不透明度 ≥ 0.5）—— `motion_appears_late`                       |
| `before(a, b)`                   | `a` 没有严格在 `b` 之前首次出现—— `motion_out_of_order`                              |
| `staysInFrame(selector)`         | 一旦可见，其盒子离开画布—— `motion_off_frame`                                        |
| `keepsMoving(withinSelector?)`   | 完全静态的窗口超过 `maxStaticSec`（默认 2 秒）—— `motion_frozen`                     |

`duration`、`withinSelector` 和 `maxStaticSec` 是可选的。发现默认为**错误**（失败的断言导致运行失败，如同布局错误——`--strict` 仍门控警告）并出现在与布局发现相同的人类可读和 `--json` 输出中。选择器未匹配任何内容时报告为 `motion_selector_missing` 而非静默通过——因此拼写错误的选择器会大声失败。在反馈循环中使用它代替目测渲染：断言运动应该做什么，让 `inspect` 告诉您搜索何时偏离了意图。

## snapshot

```bash
npx hyperframes snapshot                       # 5 个关键帧作为 PNG
npx hyperframes snapshot ./my-project          # 指定项目
npx hyperframes snapshot --frames 10           # 均匀间隔的 N 帧
```

从组合中捕获静态 PNG，用于视觉对比、缩略图或附加到 PR。当只需要几个主角帧时，比渲染视频更快。输出存放在项目的 snapshots 目录中。
