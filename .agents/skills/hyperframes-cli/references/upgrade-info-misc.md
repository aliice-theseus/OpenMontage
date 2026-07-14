# info, upgrade, compositions, docs, benchmark, telemetry, 资产预处理

不属于主要开发循环的命令的通用参考。

## info

```bash
npx hyperframes info                   # 项目元数据
npx hyperframes info ./my-video        # 指定项目
npx hyperframes info --json
```

打印**项目**元数据：名称、分辨率、时长、按类型统计的元素数量、轨道数量和项目总大小。项目级别——而非环境级别。环境健康检查请使用 `doctor`。

## upgrade

```bash
npx hyperframes upgrade                # 检查 + 交互式提示
npx hyperframes upgrade --check        # 仅检查并退出，不提示（代理友好）
npx hyperframes upgrade --check --json # 机器可读：current / latest / updateAvailable
npx hyperframes upgrade --yes          # 打印升级命令而不提示
```

比较已安装的 CLI 版本与 npm 最新版本。

## compositions, docs

```bash
npx hyperframes compositions           # 列出项目中的组合
npx hyperframes compositions --json
npx hyperframes docs                   # 列出可用主题
npx hyperframes docs rendering         # 在终端中内联打印一个主题
```

`compositions` 列出项目中每个 `data-composition-id`（包括子组合），包含时长、分辨率和元素数量。

`docs` **在终端中**内联打印文档——它不会打开浏览器。主题：`data-attributes`、`examples`、`rendering`、`gsap`、`troubleshooting`、`compositions`。不指定主题运行以查看列表。

## benchmark

```bash
npx hyperframes benchmark              # 在当前项目中运行预设矩阵
npx hyperframes benchmark ./my-video   # 指定项目
npx hyperframes benchmark --runs 5     # 重复每个配置 N 次（默认 3）
npx hyperframes benchmark --json
```

使用 5 种预设配置渲染项目——`30fps draft 2w`、`30fps standard 2w`、`30fps high 2w`、`30fps standard 4w`、`60fps standard 4w`——并打印渲染速度和输出文件大小的比较。用于在您的机器上找到最快可接受的预设。这不是带阶段分解的单次渲染。

## telemetry

```bash
npx hyperframes telemetry status      # 显示遥测状态
npx hyperframes telemetry disable     # 禁用匿名使用遥测
npx hyperframes telemetry enable      # 重新启用遥测
```

遥测仅包含匿名使用计数器。如果希望通过环境变量控制而不是子命令，可以使用 `HYPERFRAMES_NO_TELEMETRY=1` 全局禁用。

事件包括两个用于区分受管沙箱运行与真实笔记本的指纹属性——不包含 PII，不包含环境变量**值**，仅检查存在性：

- **`sandbox_runtime`**：`gvisor` / `firecracker` / `docker` / `kvm` / `wsl` / `null`。gVisor 通过内核字符串 + `/proc/version` 检测。Firecracker 通过 `/dev/vsock` + DMI sys_vendor 检测。Docker 通过 `/.dockerenv` + cgroup 检测。
- **`agent_runtime`**：`claude_code` / `codex` / `cursor` / `copilot_agent` / `jules` / `replit` / `devin` / `aider` / `gemini_cli` / `hermes` / `openclaw` / `null`。通过检查已知厂商环境变量的存在性检测；变量值本身从不被读取。

## 资产预处理

```bash
npx hyperframes tts
npx hyperframes transcribe
npx hyperframes remove-background
```

这些命令产生可放入组合的资产（旁白音频、词级转录、透明视频）。每个命令可能在首次运行时下载自己的模型。

有关语音选择、Whisper 模型规则、输出格式选择以及 TTS → 转录 → 字幕链，请调用 `hyperframes-media` 技能。本技能专注于开发循环。
