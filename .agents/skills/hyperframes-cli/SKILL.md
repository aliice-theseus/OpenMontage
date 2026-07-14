---
name: hyperframes-cli
description: HyperFrames CLI 开发循环。当运行 npx hyperframes init, add, catalog, capture, lint, validate, inspect, layout, snapshot, preview, play, render, publish, lambda, doctor, browser, info, upgrade, skills, compositions, docs, benchmark, telemetry, transcribe, tts, 或 remove-background，或排查 HyperFrames 构建/渲染环境问题时使用。AWS Lambda 云端渲染入口点（`hyperframes lambda deploy / render / progress / destroy / policies`）。
---

# HyperFrames CLI

除非项目说明指定本地包装器，所有操作都通过 `npx hyperframes` 运行。严格遵循本地包装器。需要 Node.js >= 22 和 FFmpeg。

## 工作流程

1. **脚手架 (Scaffold)** — `npx hyperframes init my-video`（或通过 `capture` 从 URL 抓取）。`init` 还会检查已安装的技能与 GitHub 上的最新版本，并在技能过时时更新全局技能集。`--skip-skills` 标志当前暂时失效（在 skills.sh 注册表追赶进度期间），因此每次 `init` 都会运行此检查并拉取最新的技能。
2. **编写 (Write)** — 创作 HTML 组合（参见 `hyperframes-core` 技能）
3. **Lint** — `npx hyperframes lint`
4. **验证 (Validate)** — `npx hyperframes validate`（运行时错误 + 对比度）
5. **可视化检查 (Visual inspect)** — `npx hyperframes inspect`
6. **预览 (Preview)** — `npx hyperframes preview` 打开 **Studio**，这是一个时间线编辑器，用户可以在其中手动编辑任何内容（不仅仅是观看）。在那里审查，然后征求同意后再渲染。
7. **渲染 (Render)** — 选择变体：
   - 迭代：`npx hyperframes render --quality draft`
   - 交付：`npx hyperframes render --quality high --output out.mp4`
   - CI / 跨主机重现：`npx hyperframes render --docker --strict --output out.mp4`
   - 云端（长时间/大型）：`npx hyperframes lambda render ./my-project --width 1920 --height 1080 --wait`（参见下面 Lambda 章节）

在预览前运行 lint、validate 和 inspect。`lint` 捕获缺少的 `data-composition-id`、重叠轨道和未注册的时间线。`validate` 在无头 Chrome 中加载组合，并报告运行时控制台错误以及 WCAG 对比度问题。`inspect` 在时间线中搜索，报告文本溢出气泡/容器或画布的问题——并且，当存在 `*.motion.json` sidecar 文件时，会验证运动意图（入场动画在搜索时触发、排序顺序、帧内位置、活跃性）与相同搜索的时间线对比。

对于运动密集型工作，推荐快照驱动迭代和 `*.motion.json` sidecar 文件——详见 `references/lint-validate-inspect.md` 了解规范和运动验证规格。

## 代理约定

适用于每个命令的通用规则：

- **`--json` 在每个命令上都可用，但 render、preview 和 play 除外。** 在代理 / CI 调用支持的命令时使用；输出包含 `_meta` 信封（CLI 版本、最新可用、更新建议）。`render` 仅通过 stdout + 退出码报告状态——使用下面的渲染后检查确认成功；`preview` / `play` 是服务器，没有 JSON。
- **`doctor --json` 始终退出码 0**，即使环境有问题。以 payload 的 `ok` 字段为门控：`npx hyperframes doctor --json | jq -e '.ok' > /dev/null`。这使管道免受 CLI 发布变动的影响。
- **非 TTY 模式是自动检测的。** 当 `stdout` 不是 TTY（CI、代理、管道输出）时，CLI 自动切换到非交互模式；此时 `init` **需要 `--example`**。传递 `--non-interactive` 可在 TTY 上也强制此模式。
- **CI 渲染门控**：`--strict` 在 lint 错误时失败，`--strict-all` 在警告时也失败，`--strict-variables` 在未声明的 `--variables` 键时失败。
- **`--json` 中的路径会被脱敏**——`$HOME` 变成了字面量 `$HOME`，这样输出可以安全地粘贴到 bug 报告和代理上下文中。
- **渲染需用户批准。** 检查通过后绝不自动渲染。在 `preview` 处暂停，告诉用户视频可在 Studio 中编辑，只有在他们批准后才渲染。
- **渲染后验证。** 在 `render` 返回退出码 0 后，确认输出文件存在且大小合理：`[ -s "$OUTPUT" ] || echo "render produced no output"`。CLI 打印 `◇  <path>` 表示成功；对于长时间渲染，还用 `ffprobe -i "$OUTPUT" -show_format -v error` 检查时长合理性。

## 路由

| 想要……                                                                                          | 阅读                                  |
| ----------------------------------------------------------------------------------------------- | ------------------------------------- |
| 脚手架一个项目（`init`、`capture`、`skills`）                                                    | `references/init-and-scaffold.md`     |
| 检查正确性（`lint`、`validate`、`inspect`、`snapshot`）                                          | `references/lint-validate-inspect.md` |
| 预览或渲染（`preview`、`play`、`render`、`publish`）                                            | `references/preview-render.md`        |
| 诊断环境（`doctor`、`browser`）                                                                 | `references/doctor-browser.md`        |
| 在 AWS Lambda 上云端渲染（`lambda deploy / sites / render / progress / destroy / policies`）   | `references/lambda.md`                |
| 其他所有（`info`、`upgrade`、`compositions`、`docs`、`benchmark`、`telemetry`、资产预处理）     | `references/upgrade-info-misc.md`     |

## 跨技能交接

- **Tailwind 项目**（`init --tailwind`）→ 在编辑类或主题令牌之前使用 `hyperframes-core`（Tailwind 参考）
- **注册表块/组件**（`hyperframes add`、`hyperframes catalog`）→ 使用 `hyperframes-registry` 了解安装路径、子组合接线和代码片段合并
- **资产预处理**（`tts`、`transcribe`、`remove-background`）→ 使用 `hyperframes-media` 了解语音选择、Whisper 模型规则、字幕和 TTS 到字幕链
- **参数化渲染**（`--variables`）→ 通过 `<html>` 上的 `data-composition-variables` 声明；完整模式见 `hyperframes-core`

## Lambda（云端渲染）

`hyperframes lambda` 将分布式渲染部署到 AWS Lambda，并从您的笔记本或 CI 驱动渲染。端到端三步：

```bash
npx hyperframes lambda deploy                                             # 配置 SAM 堆栈（Lambda + Step Functions + S3）
npx hyperframes lambda render ./my-project --width 1920 --height 1080 --wait
npx hyperframes lambda destroy                                            # 拆除（S3 存储桶保留）
```

当渲染对单台主机来说时间过长/体积过大（多分钟视频、4K、大型并行批次）且您已配置 AWS 凭证时使用 Lambda。开发循环迭代请继续使用本地 `render`。

详见 `references/lambda.md` 了解先决条件、全部 6 个子命令（`deploy`、`sites create`、`render`、`progress`、`destroy`、`policies`）、IAM 策略验证、状态文件以及成本/清理规则。

## 最低完成门控

### 静态门控

```bash
npx hyperframes lint
npx hyperframes validate
```

对于布局敏感的工作添加 `inspect`，在 CI 中使用 `render --strict` 在 lint 错误时失败。

### 可视化冒烟测试——当项目使用子组合时必须执行

`lint` / `validate` / `inspect` **分别**评估每个组合。它们从不加载 `index.html` 并通过 `data-composition-src` 挂载子组合，因此无法捕获跨文件挂载失败（参见 `hyperframes-core` → `references/sub-compositions.md`，"常见陷阱"）。唯一能捕获它们的门控是实际加载 `index.html` 并在时间线中搜索。

使用 `hyperframes snapshot`——它像 `render` 一样加载项目（因此执行相同的挂载路径），但只捕获您请求的时间戳，只需几秒钟而不是完整渲染：

```bash
# 在每段子组合的中间点捕获一帧。
# 中间点 = index.html 中每个 host slot 的 data-start + data-duration/2。
npx hyperframes snapshot --at <t1>,<t2>,<t3>,...

# 或者，如果不需要逐场景定位，使用均匀采样：
npx hyperframes snapshot --frames 9
```

输出存放在 `snapshots/frame-NN-at-Xs.png`。对照场景计划目测每一帧。

每帧危险信号（每个都对应静态门控遗漏的特定失败模式）：

| 您看到的现象                                                                                  | 根本原因                                                                                          |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 文字在左上角显示为微小无样式                                                                  | `<style>` 块留在了 `<head>` 的 `<template>` 之外（陷阱 1）——CSS 未到达真实 DOM                     |
| SVG/图标元素放大到画布大小                                                                    | 同上——未应用宽度/高度约束                                                                         |
| 场景的主角元素完全缺失；仅背景和水印可见                                                      | Host-id ≠ 模板 id（陷阱 2）——时间线从未运行，在初始状态捕获了帧                                   |
| 快照命令日志 `Sub-composition timelines not registered after 45000ms`                         | 陷阱 2——直接确认                                                                                  |

`snapshots/` 可在目测后删除；最终的面向用户的渲染是另一次 `npx hyperframes render` 过程。
