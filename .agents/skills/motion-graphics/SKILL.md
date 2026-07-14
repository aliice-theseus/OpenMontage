---
name: motion-graphics
description: >
  当用户想要一个简短、以设计为主导的动态图形时使用，其中动态本身就是
  信息：动态文字排版、统计数据或数字计数、图表/数据可视化、
  标志片头、品牌组合、下方三分一标题、标注、社交覆盖层、动画
  标题/推文/新闻条目、动态海报或快速捕获的页面高亮。
  通常在10秒以内，最长约30秒，没有叙述弧、画外音或
  真人拍摄对象。可渲染为MP4或透明覆盖层。不适用于更长、
  多场景、带旁白或品牌短片（使用general-video）、带旁白
  网站视频（website-to-video）、主题讲解
  （faceless-explainer）、产品宣传（product-launch-video）、公关视频
  （pr-to-video）或对现有素材加字幕（embedded-captions）。当不确定是
  动态优先的短篇还是较长/带旁白的制作时，请参阅/hyperframes。
metadata:
  {
    "tags": "orchestrator, motion-graphics, kinetic-type, data-viz, logo-reveal, lower-thirds, news, tweet, webpage, asset-fusion, short-form, overlay, no-narration",
  }
---

# motion-graphics — 调度入口

> **在第0步之前确认路由。** 此技能制作**简短、以设计为主导、无旁白的动态图形**（动态本身就是信息；约10秒以内，无画外音）。**较长、多场景或带旁白**的制作→`/general-video`；**带旁白的网站视频**→`/website-to-video`；**主题讲解**→`/faceless-explainer`；**产品宣传**→`/product-launch-video`；**对现有素材加字幕**→`/embedded-captions`。**超出范围**：实时/渲染时数据，或无法捕获的素材。不确定是动态优先还是带旁白？**先阅读`/hyperframes`。**

一个简短、以设计为主导的动态图形。**资产优先**：先决定资产策略并获取真实素材，然后围绕已有素材设计镜头，最后通过复用目录能力进行合成。所有工件保存到 `PROJECT_DIR = videos/<project-name>/`（在第0步创建）；以下所有路径均基于此目录。

| 阶段    | 执行方式                                                            | 主要工件                                                  | 详细流程                      |
| -------- | ------------------------------------------------------------------- | --------------------------------------------------------- | ----------------------------- |
| init     | Bash                                                                | `hyperframes.json`                                        | 第0步                         |
| plan     | 子代理 — **决定是否搜索？** + 分类 + 资产策略                        | `shot-plan.json`（草稿：分类、`asset_needs`查询、简报）  | `agents/director.md`（第1部分）|
| source ◇ | Bash — 媒体使用解析（**如果`asset_needs`为空则跳过**）              | `assets/` + `assets/index.md`                             | `phases/source/guide.md`      |
| design   | 子代理 — 围绕已解析资产进行镜头设计                                  | `shot-plan.json`（最终：block(s) + 布局 + 动态 + 位置）  | `agents/director.md`（第2部分）|
| build    | 子代理 — 优先复用组合                                               | `compositions/index.html`                                 | `agents/builder.md`           |
| render   | Bash — `hyperframes render`（MP4，或`--format webm/mov`用于覆盖层） | `renders/video.mp4`                                       | 第5步                         |
| verify   | Bash — `lint`/`inspect` → 失败时修复子代理                          | （原地修复）                                              | `agents/finalize.md`          |

`◇ source`仅在所选类别声明需要资产时运行。纯代码/文字类别（例如`kinetic-type`、大多数`charts`/`stat`）的`asset_needs: []`，直接从计划跳到设计。

## 类别 — 按搜索决策划分

`plan`的**第一个决策是：是否需要搜索？** 这个分支将类别分为两组；然后选择具体类别——对于搜索驱动的类别，**按搜索返回的内容类型选择**。每个类别是一个`categories/<id>/module.md`（其规划和构建规则）；共享的动态词汇表位于`references/motion-vocabulary.md`（→ `hyperframes-animation`规则/蓝图 + 注册表块）。

**形式类别 — 无需搜索；用户提供内容：**

| 类别             | 意图                                        | 依赖                                                                      |
| ---------------- | ------------------------------------------- | ------------------------------------------------------------------------- |
| `kinetic-type`   | 有力的一句话/引用/标题，文字即主角           | `caption-*`块 + 动画规则                                                  |
| `stat`           | 单个主角数字/计数 + 环形                    | `apple-money-count`/`rules/{counting-dynamic-scale, stat-bars-and-fills}` |
| `charts`         | 条形/折线/饼图/竞赛/百分比数据              | `data-chart`块                                                            |
| `logo-reveal`    | 标志片头/品牌组合（用户提供标志）            | `logo-outro`/`rules/svg-path-draw`                                        |
| `lower-thirds`   | 名称/标题栏、标注、社交覆盖层               | `caption-*` + 注册表覆盖层块                                              |

**搜索驱动的类别 — 先搜索，然后按内容类型动画化**（RWA路径）：

| 返回的内容         | 类别             | 动画方式                                                        |
| ------------------ | ---------------- | --------------------------------------------------------------- |
| 网页/链接          | `webpage`        | 网页/UI动画（滚动、揭示、光标、标注）                            |
| 新闻文章           | `news`           | 标题揭示 + 来源卡片 + 关键事实标注                               |
| 推文               | `tweet`          | 动画推文卡片                                                    |
| 图片/实体          | `asset-fusion`   | 资产的几何形状_变成_图表（RWA叙事融合）                          |

构建顺序：一次一个，覆盖优先（粗糙即可）。`kinetic-type`从原型移植；其余后续跟进。

## 前置条件

macOS Apple Silicon 或 Linux x64。系统工具：`brew install node ffmpeg`。运行一次`npx hyperframes doctor`。macOS GPU渲染：`export PRODUCER_BROWSER_GPU_MODE=hardware`。

可选密钥（未设置时使用本地回退）——仅当类别通过媒体使用搜索/生成资产时需要使用：

| 密钥                                 | 用途                                      | 回退                        |
| ------------------------------------ | ----------------------------------------- | --------------------------- |
| `GEMINI_API_KEY` / `GOOGLE_API_KEY`  | 图片生成（媒体使用解析）                  | 跳过生成 / 仅搜索           |
| (asset_scout / 搜索提供方)           | `webpage`/`news`/`tweet` + `asset-fusion` 真实资产搜索 | 类别降级为无资产 |

## 流程

### 第0步 — 初始化

当前工作目录为代理工作区根目录；所有工件写入 `PROJECT_DIR = videos/<project-name>/`。`<project-name>`：使用用户给定的目录，否则从意图中提取简短的短横线命名（`<subject>-motion`）。不要使用工作区基础名称或时间戳。

仅在 `$PROJECT_DIR/hyperframes.json` 不存在时：

```bash
PROJECT_DIR="${MOTION_GRAPHICS_DIR:-videos/<project-name>}"
mkdir -p "$(dirname "$PROJECT_DIR")"
npx hyperframes init "$PROJECT_DIR" --non-interactive --example=blank
```

`init` 检查已安装的技能是否与 GitHub 上的最新版本一致，如有过期则更新全局技能集。

**约束：** 绝不在工作区根目录执行 `hyperframes init`；绝不在 `PROJECT_DIR` 内嵌套另一个 `hyperframes/`；每个 Bash 命令（主代理 + 子代理）都是一个 `(cd "$PROJECT_DIR" && ...)` 子 shell — 绝不要裸用 `cd`。

### 第1步 — 规划（子代理：Director 第1部分）

调度一个子代理。提示内容 = 完整 `agents/director.md` + `## 调度上下文`（`SKILL_DIR`/`PROJECT_DIR`/用户请求/`Schema: <SKILL_DIR>/references/shot-plan-ir.md`）。它必须：

1. **决定：是否需要搜索？**（第一个分支）
   - **否** → 选择一个**形式类别**（kinetic-type / stat / charts / logo-reveal / lower-thirds）；内容由用户提供；`asset_needs: []`。
   - **是** → 生成一个**搜索计划**到 `asset_needs[]`（news / web / tweet / image；两极查询）。具体的**搜索驱动类别**（webpage / news / tweet / asset-fusion）由第2步返回的内容类型确认，并在第3步最终确定。
2. 编写草稿 `shot-plan.json`（概要 + 选定的形式类别 _或_ 搜索意图 + `asset_needs` + 一段镜头的简短说明）。模式：`references/shot-plan-ir.md`。

验证：`[ -s "$PROJECT_DIR/shot-plan.json" ] && echo ok || echo missing`。

### 第2步 — 素材来源 ◇（Bash：媒体使用，条件执行）

如果 `shot-plan.json.asset_needs` 非空，则解析资产（搜索/生成/获取 → 冻结的项目本地路径 + 账本）。参见 `phases/source/guide.md`（封装 `media-use resolve`；搜索驱动类别使用新闻/网页/推文/图片搜索）。如果 `asset_needs` 为空，则**跳到第3步**。

```bash
# 说明性 — 参见 phases/source/guide.md
(cd "$PROJECT_DIR" && node <SKILL_DIR>/phases/source/resolve.mjs --plan ./shot-plan.json --out ./assets)
```

优雅降级：如果搜索/提供方不可用，类别回退为无资产（在 `context.log` 中记录）。

### 第3步 — 设计（子代理：Director 第2部分）

调度一个子代理（提示内容 = `agents/director.md` 第2部分 + 调度上下文，包括已解析的 `assets/index.md`（如果第2步已执行）+ `catalog-map.md`）。它**围绕可用资产**设计镜头：选择目录块 + `hyperframes-animation` 规则/蓝图、布局、动态、节拍，以及（对于 `asset-fusion`）`element_positions` + 取色板。最终确定 `shot-plan.json`（`content.block` + `content.customize` + 各类别特有内容）。

### 第4步 — 构建（子代理：Builder，优先复用）

调度一个子代理。提示内容 = 完整 `agents/builder.md` + 调度上下文（`shot-plan.json`、`catalog-map.md`、该类别的 `module.md`、`references/motion-vocabulary.md`、`references/builder-contract.md`）。**优先复用**：`npx hyperframes add <block>` + 原地定制；仅手写空白 + asset-fusion 适配器。输出 `compositions/index.html`，遵守 HF 约定（暂停的 GSAP 时间线在 `window.__timelines` 上、`class="clip"` + 稳定的 id、`tl.seek(0)`、确定性）。

### 第5步 — 渲染（Bash）

```bash
(cd "$PROJECT_DIR" && npx hyperframes render . --skill=motion-graphics -q draft -o ./renders/video.mp4)
# 透明覆盖层变体：--format webm（或 mov）
```

### 第6步 — 验证（Bash → 失败时修复子代理）

```bash
(cd "$PROJECT_DIR" && npx hyperframes lint . && npx hyperframes inspect .)
```

exit 0 → 完成。如有 lint/inspect 错误，调度修复子代理（`agents/finalize.md`：快照 QA + 一次原地修复 + 重新渲染）。修复时切勿更改固定的 `data-duration`。

### 报告 + 可选预览

报告最终输出（`renders/video.mp4`，或 `.webm`/`.mov` 覆盖层变体）+ 时长。**运行期间不要打开预览。** 仅在请求时提供，且在**渲染完成后**启动，以便提供最终文件：

```bash
(cd "$PROJECT_DIR" && npx hyperframes preview)   # Studio UI；或 `npx hyperframes play` 获取可分享链接
```

标志位位于 `hyperframes-cli` 技能中（`references/preview-render.md`）。

## 恢复表

| 状态                                                    | 从何处继续            |
| ------------------------------------------------------- | --------------------- |
| 无 `shot-plan.json`                                     | 第1步（规划）         |
| `shot-plan.json` 有 `asset_needs`，无 `assets/`         | 第2步（素材来源）     |
| `shot-plan.json` 最终版，无 `compositions/index.html`   | 第3/4步（设计+构建）  |
| `compositions/index.html` 存在，无 `renders/video.mp4`  | 第5步（渲染）+ 第6步  |
| `renders/video.mp4` 存在                                | 报告 + 停止           |

## 设计说明（维护者 — 执行时不读取此内容）

- **资产优先理由：** 素材获取前置并指导镜头设计（RWA 流程：分析 → 搜索 → 审查 → 合成）。搜索驱动类别（`webpage`/`news`/`tweet`）和 `asset-fusion` 都依赖媒体使用搜索（新闻/网页/推文/图片），这是媒体使用文档化的 RWA 传统。
- **优先复用：** 生态系统内的模板类比是"组合目录块 + `hyperframes-animation` 规则"。HF 暂停的 GSAP 时间线 ≙ Remotion 的 `useCurrentFrame`。
- **类别模块约定：** 每个类别一个 `categories/<id>/module.md`（规划 + 构建），共享 `references/motion-vocabulary.md`（+ 可选评估）。添加类别 = 创建文件夹 + 在 `agents/director.md` 中注册其分类行 + 在 `catalog-map.md` 中添加其行；阶段流水线保持不变。
- **目录结构：**
  ```
  videos/<project-name>/
    hyperframes.json  context.log
    shot-plan.json            # IR（Director 输出）
    assets/  assets/index.md  # 媒体使用输出（如已获取素材）
    compositions/index.html   # Builder 输出
    renders/video.mp4
  ```
- **注册：** 在 `hyperframes` 路由中 — 添加"以设计为主导的简短动态图形"意图 + 工作流描述；从 `/general-video` 中切出 motion-graphics 触发条件；添加反向的请勿使用边。参见 `motion-graphics-genre.md` §5-7。
