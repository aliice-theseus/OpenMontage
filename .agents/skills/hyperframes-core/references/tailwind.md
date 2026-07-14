# HyperFrames Tailwind

HyperFrames `init --tailwind` 使用脚手架固定的 Tailwind 浏览器运行时。将其视为 Tailwind v4，而不是 Studio 的 Tailwind v3 设置。

## 何时使用

- 项目使用 `npx hyperframes init --tailwind` 脚手架初始化。
- `index.html` 包含 `window.__tailwindReady`。
- 任务在合成中要求使用 Tailwind 工具类、`@theme`、自定义工具类或 v3 到 v4 的迁移修复。
- 渲染的帧缺少 Tailwind 样式或出现第 0 帧闪烁。

## 版本约定

- **固定版本：`@tailwindcss/browser@4.2.4`**（真实来源：`packages/cli/src/commands/init.ts` 中的 `TAILWIND_BROWSER_VERSION`）。
- 不要用 `cdn.tailwindcss.com` 替换脚手架的运行时（未固定版本，破坏可复现性）。
- 保持就绪状态 shim 确定性；HyperFrames 在第 0 帧捕获前等待 `window.__tailwindReady`。
- 对于离线 / 锁定 / 生产稳定渲染，将 Tailwind 编译为 CSS 并提供样式表，而不是使用浏览器运行时。

## v4 浏览器运行时规则

Tailwind v4 是 CSS 优先的：

```html
<style type="text/tailwindcss">
  @theme {
    --color-brand: oklch(0.68 0.2 252);
    --font-display: "Inter", sans-serif;
  }

  @utility headline-balance {
    text-wrap: balance;
    letter-spacing: 0;
  }
</style>
```

在浏览器运行时合成中避免仅 v3 的模式：

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

不要仅为合成颜色、字体、间距或工具类添加 `tailwind.config.js`。使用 `@theme` 和 `@utility`。

**从 v3 迁移？** 明确加载现有的 JS 配置：在 `text/tailwindcss` 块中添加 `@config "./tailwind.config.js";`。v4 **不会**自动检测 v3 配置文件。

## 合成模式

使用 Tailwind 进行静态布局和样式。将渲染关键的时间控制在 GSAP 或其他可查找的 HyperFrames 适配器中。

```html
<section
  id="hero"
  class="clip absolute inset-0 grid place-items-center bg-zinc-950 text-white"
  data-start="0"
  data-duration="5"
  data-track-index="1"
>
  <div class="w-[1280px] max-w-[82vw] text-center">
    <h1 class="text-7xl font-black leading-none text-balance">Render-ready Tailwind</h1>
  </div>
</section>
```

对于重复项，**通过 CSS 变量参数化** — 保持类列表静态，以便运行时看到每个工具类：

```html
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 0"></span>
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 1"></span>
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 2"></span>
```

## 动态类安全性

浏览器运行时扫描它可以看到的类。不要仅在查找时才构建渲染关键的类名：

```js
// 有风险：运行时可能永远看不到每个生成的类。
element.className = `bg-${color}-500`;
```

优先在 HTML、data 变体或显式 CSS 中使用完整的类 token：

```html
<div data-tone="blue" class="bg-blue-500 data-[tone=rose]:bg-rose-500"></div>
```

如果生成的类不可避免，确保在验证之前完整的类 token 出现在 `text/tailwindcss` 块中。

## 视频特定防护

v4 + 渲染模式陷阱。每一条都是硬性规则：

- **仅稳定尺寸** — 使用 `w-[…]` / `h-[…]` / `aspect-video` / grid / flex。**没有 `md:` / `lg:` 断点**（渲染器是固定视口）。
- **通过 transforms / opacity 进行动画** — `translate-*`、`scale-*`、`opacity-*` 是查找安全的；对 Tailwind 尺寸工具类进行动画则不是。
- **渲染关键运动不要使用 `transition-*`** — 可查找运行时（GSAP）必须拥有状态控制权。
- **没有交互变体** — `hover:` / `focus:` / `active:` / `group-*:` / `peer-*:` / 滚动 / 指针变体在渲染期间永远不会触发。
- **v4 中裸 `border` 有问题** — v4 默认为 `currentColor`（v3 是 `gray-200`）。始终写明颜色：`border border-white/20`。
- **v4 工具类重命名** — `shadow-sm` → `shadow-xs`，`rounded-sm` → `rounded-xs`，`outline-none` → `outline-hidden`，`flex-shrink-*` → `shrink-*`，`flex-grow-*` → `grow-*`。
- **现代 CSS 没问题** — `color-mix()`、容器查询、逻辑属性都可用；渲染器是当前版本的 Chrome。

## 验证

```bash
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect

# 渲染验证 — 第 0 帧绝不能闪烁无样式内容。仅预览可能隐藏此问题。
npx hyperframes render . --workers 1 --quality draft --output tailwind-proof.mp4
```

## 快速调试检查清单

当 Tailwind 样式在渲染中不生效时，按顺序检查：

1. 项目使用 `npx hyperframes init --tailwind` 脚手架初始化？
2. `index.html` 的 `<head>` 中有 `<script src="…@tailwindcss/browser@4.2.4…">`（不是 `cdn.tailwindcss.com`）？
3. `<head>` 中存在 `window.__tailwindReady` Promise？
4. 文件中没有 v3 指令（`@tailwind base/components/utilities`）？
5. 从 `tailwind.config.js` 迁移到 `@theme` 的 token（或 v3 迁移使用 `@config` 引用）？
6. 每个渲染关键的类都作为完整的静态 token 出现（没有 `bg-${color}-500` 样式拼接）？
7. 重新运行 `npx hyperframes validate`，然后运行上面的渲染验证。
