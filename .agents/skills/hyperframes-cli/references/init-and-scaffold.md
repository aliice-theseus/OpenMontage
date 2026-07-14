# init, capture, skills

脚手架命令。使用这些命令而不是手动创建文件——它们会设置正确的文件结构、复制媒体、运行转录并安装 AI 编码技能。

## init

```bash
npx hyperframes init my-video                                    # TTY：交互式向导
npx hyperframes init my-video --example warm-grain               # 选择一个示例
npx hyperframes init my-video --example blank --resolution portrait
npx hyperframes init my-video --video clip.mp4                   # 配合视频文件
npx hyperframes init my-video --audio track.mp3                  # 配合音频文件
npx hyperframes init my-video --example blank --tailwind         # Tailwind v4 浏览器运行时
npx hyperframes init my-video --non-interactive --example blank  # CI/代理——仅标志模式
```

**默认行为取决于 TTY**：在终端中，CLI 会提示示例/选项。在非 TTY 环境（CI、代理、管道输出）中，它自动切换到非交互模式并**需要 `--example`**（CLI 在缺失时打印用法示例并报错）。传递 `--non-interactive` 可在 TTY 上也强制仅标志模式。

模板：`blank`、`warm-grain`、`play-mode`、`swiss-grid`、`vignelli`、`decision-tree`、`kinetic-type`、`product-promo`、`nyt-graph`。

其他有用的标志：

- `--resolution` — 预设：`landscape`（1920×1080）、`portrait`（1080×1920）、`landscape-4k`、`portrait-4k`、`square`（1080×1080）、`square-4k`。别名：`1080p`、`4k`、`uhd`、`1080p-square`、`4k-square`。
- `--skip-skills` — **暂时被忽略**：在 skills.sh 注册表追赶进度期间，`init` 始终检查 AI 编码技能与 GitHub 的对比。要退出此检查（CI/测试），请设置环境变量 `HYPERFRAMES_SKIP_SKILLS=1`。
- `--skip-transcribe` — 不对 `--audio` / `--video` 自动使用 Whisper 转录。
- `--model`、`--language` — 用于自动转录的 Whisper 模型/语言。

使用 `--tailwind` 时，在编辑类或主题令牌之前调用 `hyperframes-core`（Tailwind 参考）技能。脚手架使用 Tailwind v4 浏览器运行时模式，而非 Studio 的 Tailwind v3 设置。

当提供了 `--audio` 或 `--video` 时，`init` 使用 Whisper 转录文件。有关语音/模型选择，请参见 `hyperframes-media` 技能。

## capture

```bash
npx hyperframes capture https://stripe.com                  # 从网站脚手架
npx hyperframes capture https://linear.app -o linear-video  # 自定义输出目录
npx hyperframes capture https://example.com --json          # 面向代理的 JSON 输出
npx hyperframes capture https://example.com --skip-assets   # 跳过图片/SVG 下载
npx hyperframes capture https://example.com --max-screenshots 12
npx hyperframes capture https://example.com --timeout 60000 # 页面加载超时（毫秒）
```

将实时 URL 捕获为可编辑的 HyperFrames 项目：截图成为分层场景，资产本地下载，结果是一个可以 `lint` / `preview` / `render` 的正常项目。当用户提供 URL 作为视频起点时使用此命令。

## skills

```bash
npx hyperframes skills    # 为 AI 编码工具安装 HyperFrames 技能
```

一次性设置，将 HyperFrames 技能包（`hyperframes-core`、`-creative`、`-animation`、`-cli`、`-registry`、`-media`，加上 `product-launch-video` 和 `hyperframes` 编排器）添加到本地 AI 编码环境，使代理遵循框架约定。在主要 HyperFrames 升级后重新运行。
