# logo-reveal — 类别模块

**标志片头/品牌组合。** 标志由用户提供（`asset_needs` = 一个标志 `source`，不是搜索）。约3–5秒。通常 `export: alpha-overlay`（片头作为覆盖层叠加到其他素材上）。

## 规划（Director）

`content`：`{ logo: <asset path>, tagline, url }`。概要：品牌调色板（或从标志取色），优雅节奏。

## 词汇表 / 依赖

- 块：**`logo-outro`**（逐片组装 + 辉光泛光 + 标语淡入 + URL 药丸）。
- 规则：`rules/svg-path-draw`（矢量标志的绘制动画）· `rules/scale-swap-transition` · `rules/3d-text-depth-layers`。
- 原语：绘制/遮罩揭示/粒子组装 · `glow` 泛光 · `underline_sweep` · 保持。

## 构建（优先复用）

复用 `logo-outro` + 替换标志/标语/URL/调色板；**或**手动编写：将标志放置在其主角帧（CSS），通过绘制动画（SVG `stroke-dashoffset`）或遮罩/缩放揭示，添加辉光泛光 + 强调下划线扫过，保持。对于 SVG 标志，优先使用绘制动画；对于栅格标志，使用遮罩/缩放 + 辉光。作为覆盖层导出时使用透明背景。
