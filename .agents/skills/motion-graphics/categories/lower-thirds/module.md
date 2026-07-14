# lower-thirds — 类别模块

**名称/标题栏、标注、社交覆盖层** — 设计为叠加在其他素材上的图形。无资产（+ 可选标志）。通常 `export: alpha-overlay`（透明）。约3–6秒（或循环/保持）。

## 规划（Director）

`content`：`{ name, role, position (lower-left / lower-third / corner), brand_colors[] }`。默认 `export: alpha-overlay`。

## 词汇表 / 依赖

- 块：`caption-*`（pill-karaoke、neon-accent、editorial-emphasis）+ 注册表**覆盖层**块（`instagram-follow`、`tiktok-follow`、`yt-lower-third`、`x-post`、`spotify-card`、`macos-notification`）。
- 原语：滑入/擦入 · 条揭示 · `glow` · 淡出/滑出。

## 构建（优先复用）

复用最接近的覆盖层/字幕块 + 设置名称/角色/用户名/品牌颜色/位置；**或**手动编写一个擦入的条（`scaleX` 从0开始，`transform-origin:left`），文字在其后面向上滑动，保持，滑出。**透明背景**（`export: alpha-overlay` → `render --format webm/mov`）以便合成到素材上。保持在标题安全的底部区域。
