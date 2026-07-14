# 文本模块 · 动态词汇表（原语 → GSAP）

Director 在 `motion` 字符串中引用的命名原语，Builder 实现它们。`code_hint` 是框架中立的物理描述；GSAP 配方是 HF 实现。当有合适的 HF **注册表组件**（底部）时优先使用 — 不要重新发明。

## 入场

| 原语                           | GSAP 配方（进入 CSS 终态）                                          | 适用场景                   |
| ----------------------------- | ------------------------------------------------------------------- | -------------------------- |
| `slide_bottom/top/left/right` | `from({ y:±150 / x:±200, opacity:0, ease:"power4.out" })`          | 平静、构建感、专业         |
| `scale_grow`                  | `from({ scale:0, opacity:0, duration:.6, ease:"power2.out" })`      | 平静、柔和                 |
| `scale_punch`                 | `from({ scale:.6, opacity:0, ease:"back.out(2.2)" })`               | 冲击、有活力               |
| `fade_in`                     | `from({ opacity:0, duration:.4 })`                                  | 微妙                       |
| `fade_blur`                   | `from({ opacity:0, filter:"blur(14px)" })`                          | 电影感、梦幻               |
| `typewriter`                  | 通过 clip/`SplitText` 宽度步进揭示                                   | 技术、叙事                 |
| `word_reveal`                 | 逐词 `from({opacity:0,y:..}, stagger:.1)`                           | 讲故事                     |
| `wave`                        | 逐字母 `from({y:..}, stagger:{each:.04})`                           | 流动感、音乐感             |
| `bounce_in`                   | `from({y:-120}, ease:"bounce.out")`                                 | 俏皮                       |
| `slam`                        | `from({ y:-300, ease:"power4.out" })` + 落地时震动                  | 冲击、重型                 |

## 强调（原地，通常在节拍上）

| 原语           | GSAP 配方                                                            | 适用场景           |
| ------------- | -------------------------------------------------------------------- | ----------------- |
| `scale_pulse` | `to({ scale:1.12, yoyo:true, repeat:1, ease:"sine.inOut" })` 在节拍 | 节奏感、峰值      |
| `shake`       | `to({ keyframes:[{x:-9},{x:9},{x:0}], ease:"none" })`               | 紧急、强烈        |
| `glow`        | `to({ textShadow:"0 0 46px <ink/accent>", yoyo:true, repeat:1 })`   | 重要、魔法般      |
| `color_shift` | `to({ color:"<accent>" })`（或在 CSS 中为词加重音）                   | 动态              |

## 退出

| 原语         | GSAP 配方                                        | 适用场景      |
| ----------- | ------------------------------------------------ | ------------ |
| `fade_out`  | `to({ opacity:0, duration:.4, ease:"power2.in" })` | 结束         |
| `slide_out` | `to({ y/x: off, opacity:0, ease:"power2.in" })`    | 过渡         |
| `scale_out` | `to({ scale:1.06, opacity:0, ease:"power2.in" })`  | 过渡         |

## 装饰图形（非文字）

`underline_sweep` `fromTo({scaleX:0},{scaleX:1}, transformOrigin:"left center")` · `bar_wipe` · `hold_breath` `to({scale:1.015, ease:"sine.inOut"})`。

## 优先使用 HF 注册表组件（如适用）

`caption-kinetic-slam` · `caption-editorial-emphasis` · `caption-neon-glow` · `caption-glitch-rgb` · `caption-particle-burst` · `caption-weight-shift` · `caption-matrix-decode` · `caption-pill-karaoke` · `shimmer-sweep`。这些是预先构建的、在生态系统内的且已经过渲染测试 — Builder 应优先使用它们，而不是手动编写等效内容。
