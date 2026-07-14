# HTML 幻灯片连接器 (frontend-slides)

将 `visual-style.md` 应用于 HTML 幻灯片演示。

## 概述

此连接器将 `visual-style.md` 字段映射到 CSS 变量和样式规则，用于 [frontend-slides](https://github.com/zarazhangrui/frontend-slides) 或类似的 HTML 演示框架。

## 字段映射

| visual-style.md 字段 | CSS 输出 |
|----------------------|----------|
| `colors.primary[0].hex` | `--color-bg` |
| `colors.primary[1].hex` | `--color-text` |
| `colors.accent[0].hex` | `--color-accent` |
| `colors.neutral[0].hex` | `--color-muted` |
| `typography.display.family` | `--font-display` |
| `typography.body.family` | `--font-body` |
| `typography.display` | `h1, h2, h3` 样式 |
| `typography.body` | `p, li` 样式 |
| `typography.caption` | `.label, code, small` 样式 |
| `typography.rules` | 额外 CSS 规则 |
| `layout.grid` | CSS grid/flexbox 系统 |
| `layout.aspect_ratio` | 幻灯片尺寸 |
| `motion.transitions` | CSS 幻灯片过渡 |
| `mood.avoid` | 设计约束检查清单 |

## CSS 变量模板

```css
:root {
  /* Colors */
  --color-bg: [colors.primary[0].hex];
  --color-text: [colors.primary[1].hex];
  --color-accent: [colors.accent[0].hex];
  --color-muted: [colors.neutral[0].hex];

  /* Typography */
  --font-display: "[typography.display.family]", system-ui, sans-serif;
  --font-body: "[typography.body.family]", system-ui, sans-serif;

  /* Spacing (derive from style) */
  --space-sm: clamp(0.5rem, 1vw, 1rem);
  --space-md: clamp(1rem, 2vw, 2rem);
  --space-lg: clamp(2rem, 4vw, 4rem);
}

body {
  font-family: var(--font-body);
  background: var(--color-bg);
  color: var(--color-text);
}

h1, h2, h3 {
  font-family: var(--font-display);
  font-weight: [typography.display.weight];
  /* Apply typography.display.style rules */
}

.accent {
  color: var(--color-accent);
}

.muted {
  color: var(--color-muted);
}
```

## frontend-slides 约束

生成 HTML 幻灯片时，遵循以下规则：

1. **单 HTML 文件** — 零依赖，内联 CSS/JS
2. **视口单位** — 所有尺寸使用 `clamp()`，绝不用固定 px/rem
3. **无滚动** — 每张幻灯片 `height: 100vh; overflow: hidden;`
4. **内容溢出** — 如果内容不适合，拆分为多张幻灯片
5. **Google Fonts** — 通过 `<head>` 中的 `<link>` 标签加载

## 示例：瑞士风格幻灯片

给定 `mueller-brockmann-swiss.visual-style.md`：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Presentation</title>
  <link href="https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --color-bg: #000000;
      --color-text: #FFFFFF;
      --color-accent: #0066FF;
      --color-muted: #CCCCCC;
      --font-display: "Helvetica Neue", Helvetica, Arial, sans-serif;
      --font-body: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: var(--font-body);
      background: var(--color-bg);
      color: var(--color-text);
    }

    .slide {
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: clamp(2rem, 5vw, 6rem);
    }

    h1 {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: clamp(3rem, 8vw, 8rem);
      text-transform: uppercase;
      letter-spacing: -0.02em;
      line-height: 0.9;
      text-align: left;
    }

    .accent { color: var(--color-accent); }

    /* Grid overlay for Swiss style */
    .slide::before {
      content: '';
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(
        90deg,
        transparent,
        transparent calc(100% / 12 - 1px),
        var(--color-muted) calc(100% / 12 - 1px),
        var(--color-muted) calc(100% / 12)
      );
      opacity: 0.1;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <section class="slide">
    <h1>Grid-locked<br><span class="accent">precision</span></h1>
  </section>
</body>
</html>
```

## 工作流程

1. **加载风格** — 读取 `visual-style.md` 文件
2. **生成 CSS 变量** — 映射颜色和排版
3. **应用排版规则** — 遵循 `typography.rules` 约束
4. **检查约束** — 对照 `mood.avoid` 列表验证
5. **生成幻灯片** — 每张幻灯片一个 `<section class="slide">`
6. **验证** — 确保无滚动，所有尺寸响应式

## 提示

- **排版驱动层级** — 标题使用 `typography.display`，内容使用 `typography.body`
- **尊重避免列表** — 添加装饰元素前检查 `mood.avoid`
- **过渡效果** — 将 `motion.transitions` 映射到幻灯片间的 CSS 过渡
- **字体加载** — 始终在字体栈中包含后备字体
