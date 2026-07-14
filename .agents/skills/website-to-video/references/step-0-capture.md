# 步骤 0：捕获

捕获流水线下载网站并提取结构化数据，供工作流的其余部分读取。步骤 0 是一个命令加一次完整性检查。**所有分析（读取文件、查看联系表、推导品牌声音、选择资源）都在步骤 1–3 中完成，不在此处。**

## 运行捕获

基础捕获不需要 API 密钥。但是，在运行之前，询问用户：

> 「为获得最佳效果，建议设置 Gemini API 密钥——它可以为每张捕获的图片提供 AI 驱动的描述，这有助于我为每个场景选择合适的资源。每张图片大约花费 $0.001。如果你想跳过也可以，但视频质量会在有密钥时更好。要设置：在项目根目录的 `.env` 文件中添加 `GEMINI_API_KEY=your-key`。你可以在 ai.google.dev 获得免费密钥。」

如果用户提供了密钥或已有密钥，继续执行。如果他们跳过，无论如何继续——捕获在没有密钥的情况下也能工作，但 `asset-descriptions.md` 将只有 DOM 上下文描述（位置、大小、alt 文本），而不是 AI 视觉描述。

如果视频的项目目录还不存在，请创建，然后将网站捕获到其中的 `capture/` 子文件夹：

```bash
npx hyperframes capture <URL> -o <project-dir>/capture
```

示例：`npx hyperframes capture https://stripe.com -o videos/stripe-launch/capture`

将捕获产物（`screenshots/`、`assets/`、`extracted/`、`AGENTS.md`、`CLAUDE.md`）保留在专用的 `capture/` 子文件夹中，使它们与后续的构建文件（`SCRIPT.md`、`STORYBOARD.md`、`DESIGN.md`、`compositions/`、`index.html`、`narration.wav`、`transcript.json`、`renders/`、`snapshots/`）隔离，后者都位于 `<project-dir>/` 根目录。

对于尚未制作视频的探索性捕获，默认的 `./capture/`（或你选择的任何 `-o <name>`）就足够了——隔离约定仅在你在捕获基础上构建视频时才重要。

## 确认成功

等待捕获完成。打印一行总结捕获的内容：

> 「已捕获 N 张截图、M 个资源、K 个 SVG、F 个字体。准备进入步骤 1。」

如果命令以非零退出，计数全为零，或必需的目录（`extracted/`、`assets/`、`screenshots/`）缺失，显示错误并停止——不要带着失败的捕获进入步骤 1。

## `capture/` 中的内容（参考表——不要在此处读取）

每个下游步骤只读取它需要的内容。不要在步骤 0 中预先获取所有内容；那会膨胀上下文，并在使用时产生已经过时的摘要。

| 路径 | 首次读取在 |
| ----------------------------------------- | --------------------------------------------- |
| `capture/extracted/tokens.json` | 步骤 1（DESIGN.md——颜色/字体） |
| `capture/extracted/design-styles.json` | 步骤 1（DESIGN.md——排版/组件） |
| `capture/extracted/fonts-manifest.json` | 步骤 1（字体识别） |
| `capture/extracted/asset-descriptions.md` | 步骤 2（简报基础）和步骤 3（资源） |
| `capture/extracted/visible-text.txt` | 步骤 2（简报）和步骤 3（脚本） |
| `capture/assets/contact-sheet-*.jpg` | 步骤 3（资源选择） |
| `capture/assets/svgs/contact-sheet-*.jpg` | 步骤 3（SVG/Logo 选择） |
| `capture/screenshots/contact-sheet-*.jpg` | 步骤 3（视觉情绪参考） |
| `capture/extracted/animations.json` | 步骤 3 / 步骤 5（仅当网站有动画时） |
| `capture/extracted/lottie-manifest.json` | 步骤 3（仅当网站使用 Lottie 时） |
| `capture/extracted/video-manifest.json` | 步骤 3（仅当网站嵌入视频时） |
| `capture/extracted/shaders.json` | 步骤 3 / 步骤 5（仅当网站有 WebGL 时） |
| `capture/assets/<individual files>` | 步骤 5（仅在放置特定资源时） |

## 关卡

捕获退出 0。资源/截图/字体计数非零。进入步骤 1。
