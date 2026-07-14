# news — 类别模块（搜索驱动）

搜索一篇真实新闻文章 → 将其动画化为**文章高亮** — 居中强调技术的忠实 HF 移植。标志性动画：文章文字以**可读大小（非放大）**排版，滑入 + 淡入，然后**关键词在原地被高亮** — 标记带在其后面从左向右生长。无放大缩放。约5–7秒。

两种布局共享这一高亮核心 — 根据宽高比和是否有标志/人物来选择：

| 布局                      | 宽高比    | 何时使用                                                      | 包含内容                                                                  |
| ------------------------- | --------- | ------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **A · 居中强调**          | 9:16 / 1:1 | 纯文字、社交竖版                                              | 导语 + 一个居中句子 + 关键词高亮                                          |
| **B · 完整文章**          | 16:9       | 故事中有真实的**来源标志**和/或**人物**时                      | 标志 + 日期 + 多行标题高亮 + 摘要 + 来源 + 人物抠图                      |

## 素材来源（第2步）

RWA/网页搜索（或 `hyperframes capture`）→ 一篇真实文章。Director 提取**关键词**（1–2个词/一个数字/一个名字 — 钩子），对于布局 B，还需要**品牌标志**、**日期**和**人物照片**。`asset_needs: { kind: news|web|image, query }` — 请求标志（Wikimedia/simple-icons）和人物照片（Wikimedia）作为单独的资产查询。通过 `hyperframes remove-background <in> -o <out>.png` 处理人物照片以获得透明抠图。

## 高亮核心（两种布局共享）— 标记带技术

关键词高亮是一个通过 `background-size` 从左向右生长的标记带（**不是** `transform:scaleX` 条）：

```css
.hl {
  --hlw: 0%;
  background-image: linear-gradient(var(--hl), var(--hl)); /* --hl: rgba(250,222,99,.6) */
  background-repeat: no-repeat;
  background-position: 0 72%;
  background-size: var(--hlw) 64%;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
```

`box-decoration-break:clone` 使标记带**无缝跨行换行** — 跨2–3行的多词关键词仍然连续高亮（旧的 `scaleX` 条做不到）。GSAP 补间 CSS 变量 `--hlw` 从 0%→100%，**在文字安定后扫入 — 绝不预先应用**。可选择按关键词长度缩放时长，约0.5–1.5秒。

## 布局 A — 居中强调（9:16，纯文字）— Builder

1. **以可读大小排版关键词句子 — 不要缩放。** 纸张浅色舞台；顶部有来源 `#kicker`（例如 "BBC NEWS · TECHNOLOGY"，品牌强调色）；关键词句子居中，衬线字体，**约70–76px / 700 / 行高约1.4**，`max-width ≈ 900`。整个句子保持可读；关键词在句_内_被强调。
2. 内联包裹关键词：`… raised <span class="hl" id="kw">$750M</span> at …`。
3. **时间线**（seek 安全，暂停）：导语淡入+滑入 → **句子滑入+淡入**（`set{autoAlpha:0,y:52}`→`to{autoAlpha:1,y:0,duration:0.8,ease:"power3.out"}`，无缩放）→ **关键词高亮生长**（`--hlw 0→100%`，句子安定后）→ 柔和保持（`scale 1.012`）。

**参考：** `samples/news/_ref-centered-emphasis.html`（+ `news/v2-*`）。

## 布局 B — 完整文章（16:9，标志 + 人物）— Builder

编辑文章卡片布局（左上角标志 + 日期 + 大号衬线标题带多行关键词高亮 + 摘要 + 左下角来源 + 右下角背景去除的**人物抠图**）。1920×1080，纸张浅色渐变舞台，Georgia 衬线字体。

1. **标志**左上角（`#logo`，约64px）— 内联来源/品牌 SVG，`fill:currentColor`，`color` 设置为标志本身的色相（单色标志使用近黑色）。**日期**在其下方（`#date`，约30px，柔和色）。
2. **标题**（`#headline`，Georgia **96px / 700**，`width≈1080`，`line-height 1.16`）关键词包裹在 `<span class="hl" id="kw">` 中 — 高亮带扫过该短语的**所有换行**。
3. **摘要**（`#dek`，Helvetica 约38px 灰色）在标题下方；**来源**（`#outlet`，Georgia 粗体 约50px）左下角。
4. **人物抠图**（`#subject`，背景去除的 PNG，`height≈860`，`right:40; bottom:0`，`drop-shadow`）— **从右下角滑入**作为主角节拍。
5. **时间线**（seek 安全，暂停）：标志 `back.out` @0.15 → 日期 @0.4 → **主体滑入**（`set{autoAlpha:0,x:90,y:60}`→`to{autoAlpha:1,x:0,y:0,duration:0.85,ease:"power3.out"}`）@0.45 → 标题 @0.7 → 摘要 @1.5 → 来源 @1.9 → **关键词高亮**（`--hlw 0→100%`，`duration:0.8`）@2.2。总时长约6.5秒。

**参考：** `samples/news/_ref-article-layout.html`（一篇真实文章，使用真实来源标志 + 背景去除的人物 + 真实故事渲染）。

## 关键

高亮是**在原地生长，在文字之后扫入 — 绝不预先应用**。文字**保持可读 — 不要将关键词放大到充满画面**（团队反馈 2026-06-09：放大失去上下文且读起来不对；该技术从不放大 — 它呈现文字并高亮词汇）。对于布局 B，人物必须是 `remove-background` 抠图（无矩形照片框）。确定性；遵守 `references/builder-contract.md`。
