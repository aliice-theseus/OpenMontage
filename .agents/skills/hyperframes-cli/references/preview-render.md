# preview, play, render, publish

服务、渲染和分享命令。

## preview

```bash
npx hyperframes preview                   # 服务当前目录
npx hyperframes preview --port 4567       # 自定义端口（默认 3002）
```

文件更改时热重载。自动在浏览器中打开 Studio——完整的时间线编辑器，用户可以在其中播放视频并在渲染前手动编辑任何内容。这是审查界面，不仅仅是查看器。

将项目交还给用户时，使用 Studio 项目 URL，而非源 `index.html` 路径：

```text
http://localhost:<port>/#project/<project-name>
```

使用实际的端口和项目目录名；将 `index.html` 视为源代码上下文，而非预览界面。例如，在 `codex-openai-video` 中执行 `npx hyperframes preview --port 3017` 后，报告 `http://localhost:3017/#project/codex-openai-video`。

## play（轻量播放器）

```bash
npx hyperframes play                  # 当前项目，端口 3003
npx hyperframes play ./my-video       # 指定项目
npx hyperframes play --port 8080      # 自定义端口
```

`play` 通过可嵌入的 `<hyperframes-player>` Web 组件提供组合服务，而不是完整的 Studio UI。在分享预览链接或 Studio 过于重量级时使用（无编辑器、无面板）。`play` 报告纯 `http://localhost:<port>` URL——没有 `#project/<name>` 片段（这是 Studio 路由约定，仅 `preview` 使用）。

播放器的 `playback-rate` 属性（预览速度控制，驱动时间线的 `timeScale`）被限制在 `[0.1, 5]` 范围内；`≤ 0` 或非有限值回退到 `1`。这是预览/播放旋钮，不是组合的 `data-*` 属性——创作的运动仍以 `1×` 渲染。

### 使用外部浏览器启动（preview + play）

`preview` 和 `play` 都可以在指定的 Chromium 兼容浏览器中打开，而不是使用操作系统默认浏览器。两种用例：隔离的 Chromium 配置文件，或外部 CDP 连接（DevTools / Playwright / Puppeteer / browser-MCP）。**HyperFrames 本身不拥有 CDP 自动化**——这只是暴露端点；连接到它的是您的责任。不要与 `--browser-gpu`（`render` 中控制捕获期间 Chrome GPU 访问的标志）混淆。

| 标志                        | 类型             | 说明                                                                                                                                                        |
| --------------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--browser-path`            | 路径             | Chromium 兼容可执行文件的绝对路径（`/usr/bin/chromium`、`/Applications/Brave Browser.app/...`）。                                                            |
| `--user-data-dir`           | 路径             | Chromium 兼容配置文件目录。需要 `--browser-path`。使用一次性目录以保持状态不进入主配置文件。                                                                |
| `--remote-debugging-port`   | 整数 1-65535     | 在给定端口上打开 Chromium CDP 端点。**同时需要** `--browser-path` 和 `--user-data-dir`——否则被拒绝，以确保 CDP 端点不会意外泄漏到主配置文件中。            |

```bash
# 在隔离的 Chromium 配置文件中打开预览
npx hyperframes preview --browser-path /usr/bin/chromium --user-data-dir /tmp/hf-profile

# 同上，加上 :9222 上的 CDP 端点（连接 DevTools / Playwright 等）
npx hyperframes play --browser-path /usr/bin/chromium --user-data-dir /tmp/hf-profile --remote-debugging-port 9222
```

在任何服务器启动前进行验证，因此无效值会干净退出，不会留下监听套接字。

## render

> 只有在用户在 `preview` 中审查并批准后才渲染。不要在检查通过时自动渲染。

```bash
npx hyperframes render                                # 从当前目录渲染标准 MP4
npx hyperframes render ./my-video --output ./out.mp4  # 从项目目录外层渲染
npx hyperframes render --output final.mp4             # 命名输出（不含时间戳）
npx hyperframes render -c compositions/intro.html -o intro.mp4  # 渲染特定子组合文件
npx hyperframes render --quality draft                # 快速迭代
npx hyperframes render --fps 60 --quality high        # 最终交付
npx hyperframes render --format webm                  # 透明 WebM
npx hyperframes render --docker                       # 字节一致
```

> 默认 `--output` 是 `renders/<project-name>_<YYYY-MM-DD>_<HH-MM-SS>.<ext>`——每次渲染带时间戳，因此连续运行不会互相覆盖。传递 `--output` 以获得稳定名称。

| 标志                                | 选项                                                                                              | 默认值                             | 说明                                                                                                                                                                                                                               |
| ----------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dir`（位置参数）                    | 路径                                                                                              | cwd                                | 项目目录。省略以使用当前工作目录。                                                                                                                                                                                                   |
| `--composition`、`-c`               | 组合文件路径                                                                                      | `index.html`                       | 渲染指定的组合文件（例如 `compositions/intro.html`）而不是项目的 `index.html`。                                                                                                                                                      |
| `--output`、`-o`                    | 路径                                                                                              | `renders/<project>_<ts>.<ext>`     | 输出路径。默认带时间戳（`<project-name>_YYYY-MM-DD_HH-MM-SS.<ext>`）。                                                                                                                                                               |
| `--fps`                             | 24、30、60                                                                                        | 30                                 | 60fps 使渲染时间加倍                                                                                                                                                                                                                 |
| `--quality`                         | draft、standard、high                                                                             | standard                           | 迭代时使用 draft                                                                                                                                                                                                                    |
| `--format`                          | mp4、webm、mov、gif、png-sequence                                                                | mp4                                | WebM/MOV 带透明度渲染；gif 用于 GitHub PR/README/文档中的内联自动播放（两遍调色板编码，fps 上限 30——推荐 `--fps 15`——无音频，仅 1 位透明度，HDR 回退到 SDR）；png-sequence 将 RGBA 帧写入目录（AE/Nuke/Fusion 导入）                 |
| `--gif-loop`                        | 0-65535                                                                                           | 0                                  | GIF 循环次数；`0` 表示永远循环。仅与 `--format gif` 一起使用。                                                                                                                                                                     |
| `--resolution`                      | landscape、portrait、landscape-4k、portrait-4k、square、square-4k（+ 别名 `1080p`、`4k`、`uhd`） | —                                  | 通过 Chrome `deviceScaleFactor` 超采样。宽高比必须与组合匹配；缩放必须为整数。不能与 `--hdr` 同时使用。                                                                                                                              |
| `--crf`                             | 0-51                                                                                              | —                                  | 编码器 CRF（越低质量越高）。与 `--video-bitrate` 互斥。                                                                                                                                                                            |
| `--video-bitrate`                   | 例如 `10M`、`5000k`                                                                               | —                                  | 目标比特率。与 `--crf` 互斥。                                                                                                                                                                                                       |
| `--hdr`                             | 标志                                                                                              | 关闭                               | 即使使用 SDR 源也强制 HDR 输出。仅 MP4。                                                                                                                                                                                            |
| `--sdr`                             | 标志                                                                                              | 关闭                               | 即使使用 HDR 源也强制 SDR 输出。                                                                                                                                                                                                    |
| `--workers`                         | 数字或 `auto`                                                                                     | auto                               | 每个 worker 启动 Chrome（约 256 MB）                                                                                                                                                                                               |
| `--docker`                          | 标志                                                                                              | 关闭                               | 跨主机可重现输出                                                                                                                                                                                                                   |
| `--gpu`                             | 标志                                                                                              | 关闭                               | GPU 加速 FFmpeg 编码（NVENC / VideoToolbox / VAAPI / QSV）                                                                                                                                                                         |
| `--browser-gpu` / `--no-browser-gpu` | 标志                                                                                              | auto（本地）、off（docker）        | Chrome/WebGL 捕获的主机 GPU                                                                                                                                                                                                          |
| `--browser-timeout`                 | 秒（0.001–86400）                                                                                  | 60                                 | 入口 HTML 的 Puppeteer 页面导航超时。当重量级组合（大量视频/字体/远程资产）在默认 60 秒内无法到达 `domcontentloaded` 时，请增大此值。                                                                                             |
| `--quiet`                           | 标志                                                                                              | 关闭                               | 抑制详细输出                                                                                                                                                                                                                       |
| `--strict`                          | 标志                                                                                              | 关闭                               | 在 lint 错误时失败                                                                                                                                                                                                                 |
| `--strict-all`                      | 标志                                                                                              | 关闭                               | 在 lint 错误和警告时均失败                                                                                                                                                                                                         |
| `--variables`                       | JSON 对象                                                                                         | —                                  | 覆盖在 `data-composition-variables` 中声明的值                                                                                                                                                                                     |
| `--variables-file`                  | 路径                                                                                              | —                                  | 包含变量值的 JSON 文件（`--variables` 的替代方案）                                                                                                                                                                                 |
| `--strict-variables`                | 标志                                                                                              | 关闭                               | 在 `--variables` 中存在未声明的键或类型不匹配时渲染失败                                                                                                                                                                            |

**质量指南：** 迭代时使用 `draft`，审查时使用 `standard`，最终交付时使用 `high`。

**参数化渲染：** 组合在 `<html>` 根元素上用 **`data-composition-variables`** 声明变量——一个 JSON **声明数组**（每个条目 `{id, type, label, default}`），定义模式。内部脚本通过 `window.__hyperframes.getVariables()` 读取解析后的值。CLI 的 `--variables '{"title":"Q4 Report"}'` 是一个按 id 键控的 JSON **对象**，覆盖一次渲染的这些声明默认值；缺失的键会穿透，因此同一组合在开发预览和生产环境中运行时保持不变。子组合 host 也可以用 `data-variable-values` 覆盖每个实例的值。完整模式参见 `hyperframes-core` 技能。

## publish

```bash
npx hyperframes publish              # 上传当前项目，返回公开 URL
npx hyperframes publish ./my-video   # 指定项目
npx hyperframes publish --yes        # 跳过确认提示（脚本/CI）
```

上传项目的源代码（HTML + 资产）并返回一个在浏览器中渲染的稳定公开 URL。用于在渲染 MP4 之前分享草稿以供审查，或用于在其他地方嵌入组合。Lint 结果在上传前显示，但不会阻止上传。
