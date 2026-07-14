# 动态图形构建器

将 `shot-plan.json` 转换为一个可渲染的 HyperFrames 合成（`compositions/index.html`）。一切保持在 HF 生态系统中 — HTML 是事实来源；一个**暂停**的 GSAP 时间线承载所有动画；引擎 seek 它。特定类别的构建规则位于 `categories/<id>/module.md` 中；此文件是共享约定。

## 优先复用（默认）

默认 = **组合现有目录能力，而非手动编写**：

- `npx hyperframes add <block>`（注册表）→ 原地定制。大多数块将内容/数据烘焙到自己的脚本中（只有少数暴露 CSS 变量参数），所以复用 = **添加 + 编辑**。
- 用于动画的 `hyperframes-animation` 规则/蓝图/过渡；运行时适配器（默认 GSAP）。

仅手动编写（a）没有块/规则覆盖的空白、（b）`asset-fusion` 适配器绑定。Director 在 `shot-plan.json`（`content.block` + `content.customize`）中指定了块和定制项；参见 `catalog-map.md`。

## HF 约定（不可协商）

- 根 `#stage` 携带 `data-composition-id`、`data-start="0"`、`data-duration=<s>`、`data-fps`、`data-width`、`data-height`。
- 恰好**一个** `gsap.timeline({ paused:true })`；注册 `window.__timelines["<id>"] = tl;`；以 `tl.seek(0)` 结束。**绝不要为渲染关键动画使用 `tl.play()`**。无定时器/异步/事件驱动的时间线构建。仅限有限重复。
- **时间剪辑**需要 `class="clip"` + 稳定的 `id`。一个全时长剪辑内的时间线驱动组不需要每个都有定时属性。
- **字体**：优先使用本地 `@font-face`（.woff2）以实现确定性和离线渲染；CDN Google Fonts 可以渲染（编译器缓存 + 注入 `@font-face`）但会发出警告且需要网络。
- **仅确定性** — 无 `Date.now()`/`Math.random()`/网络。

## 先布局后动画

先用 CSS 构建**主角帧终态**（flex + padding；绝不在内容容器上使用绝对偏移；根必须有尺寸）。然后用 `gsap.from()` 从外部进入该终态；通过过渡或最终场景退出。完整规则：`references/builder-contract.md`。

## IR → 合成

- `content.block` → `hyperframes add`（或内联）+ 应用 `content.customize`。
- 各类别 `content`（文字场景/图表数据/融合位置/新闻推文内容）→ 按 `categories/<id>/module.md` 实现。
- 已解析的 `asset_needs` → 引用**冻结的项目本地路径**（绝不使用远程 URL 或提示）。
- 来自概要的 `palette[-1]`/bg + `font`。
- `export: alpha-overlay` → 透明背景；使用 `--format webm`（或 `mov`）渲染。

## 关键正确性（GSAP / seek）

透明度门控延迟元素（设置为隐藏直到其入场）。在动画边界处钳制（不超调超出保持值）。允许的缓动：`power1–4`、`back`、`bounce`、`circ`、`elastic`、`expo`、`sine`（`.in/.out/.inOut`）。每场景一个主题。运行 `hyperframes inspect` 检查溢出/碰撞。

## 验证修复

`hyperframes lint` → `inspect` → `render -q draft`。失败时，修复有问题的元素 + 重新运行。（来源于 Remotion 的先前工作通过 `/remotion-to-hyperframes` SSIM 测试套件评分。）**修复期间切勿更改固定的 `data-duration`。**
