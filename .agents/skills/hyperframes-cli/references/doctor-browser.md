# doctor, browser

环境诊断和捆绑 Chrome 管理。当渲染或预览失败时首先运行这些命令。

## doctor

```bash
npx hyperframes doctor
npx hyperframes doctor --json     # CI / 代理输出（始终退出码 0；以 payload 的 `ok` 为门控）
```

运行独立检查并将每项报告为 ok/warn/fail：

- **版本** — 已安装的 CLI 与 npm 最新版本的比较（过时时提示升级）
- **Node.js** — 需要 ≥ 22
- **CPU**、**内存**、**磁盘** — 主机资源
- **环境** — 影响渲染器的环境变量
- **FFmpeg** / **FFprobe** — 是否找到、版本、编解码器
- **Chrome** — 捆绑或系统、版本、路径
- **Docker** / **Docker 运行中** — 仅 `render --docker` 需要
- **/dev/shm** — 仅在容器内

出现以下情况时首先运行 `doctor`：

- `render` 因 Chrome 或 FFmpeg 错误而失败。
- `preview` 打开但组合加载失败。
- 新机器从未运行过 HyperFrames。

常见问题：

- **缺少 FFmpeg** — 通过 `brew install ffmpeg`（macOS）或包管理器安装。
- **缺少捆绑 Chrome** — 运行 `npx hyperframes browser ensure`。
- **内存不足** — 关闭其他 Chrome，减少 `--workers`，或使用 `--quality draft`。

## browser

```bash
npx hyperframes browser ensure    # 查找或下载固定的 Chrome 版本
npx hyperframes browser path      # 打印浏览器可执行文件路径（用于脚本）
npx hyperframes browser clear     # 移除缓存的 Chrome 下载
```

管理 HyperFrames 用于渲染的 Chrome 构建。使用固定版本是因为像素输出在不同 Chrome 版本之间会有差异——使用捆绑构建可保持各机器间渲染输出的可重现性。

使用 `path` 将二进制文件嵌入脚本：`$(npx hyperframes browser path)`。
