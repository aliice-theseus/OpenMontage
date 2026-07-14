# 参数翻译：Zod schemas、defaultProps、calculateMetadata

有类型的 Remotion `<Composition schema={...} defaultProps={...} />` 如何转化为参数化的 HF 合成。

## 同步 calculateMetadata（可翻译）

```tsx
<Composition
  id="MyVideo"
  component={MyVideo}
  schema={z.object({ title: z.string(), duration: z.number() })}
  defaultProps={{ title: "Hello", duration: 90 }}
  calculateMetadata={({ props }) => ({
    durationInFrames: props.duration,
    fps: 30,
  })}
/>
```

当 `calculateMetadata` 是同步的且只使用 `props` 时，**在翻译时解析它** — 使用 `defaultProps`（或调用者指定的任何值）调用它，并将具体结果写入 HTML：

```html
<div
  id="stage"
  data-composition-id="MyVideo"
  data-start="0"
  data-duration="3"          <!-- 90/30 -->
  data-fps="30"
  data-title="Hello"
></div>
```

`data-title` 属性携带值。原来读取 `props.title` 的代码在 HF 中读取 `document.getElementById("stage").dataset.title`。

## 异步 calculateMetadata（不可翻译）

```tsx
<Composition
  calculateMetadata={async ({ props }) => {
    const res = await fetch(...);
    return { durationInFrames: res.duration };
  }}
/>
```

**拒绝 + 互操作**。HF 需要预先知道合成的元数据来生成 HTML。在翻译时解析网络调用违背了动态元数据的目的。参见 [escape-hatch.md](escape-hatch.md)。

lint 规则 `r2hf/async-metadata` 会捕获此情况。T4 案例 03 测试了此情况。

## 默认属性（Default props）

```tsx
defaultProps={{
  title: "Hello",
  subtitle: "World",
  count: 42,
}}
```

翻译为根 `#stage` div 上的 `data-*` 属性：

```html
<div id="stage" data-title="Hello" data-subtitle="World" data-count="42">...</div>
```

约定：`propName` → `data-prop-name`（kebab-case）。在 GSAP 脚本内部，通过 `document.getElementById("stage").dataset.propName` 读取。

## 嵌套对象 / 数组属性

```tsx
defaultProps={{
  stats: [
    { label: "Stars", value: 1247, color: "#fbbf24" },
    { label: "Forks", value: 312, color: "#60a5fa" },
  ],
}}
```

不要尝试将数组编码为 JSON `data-` 属性 — HF 的运行时不会解析这些。将数组物化为**重复的 HTML 标记**：

```html
<div id="scene-stats">
  <div class="stat-card" data-stat-index="0" data-stat-value="1247" style="--card-color:#fbbf24">
    <div class="number">0</div>
    <div class="label">Stars</div>
  </div>
  <div class="stat-card" data-stat-index="1" data-stat-value="312" style="--card-color:#60a5fa">
    <div class="number">0</div>
    <div class="label">Forks</div>
  </div>
</div>
```

组件模板（`StatCard.tsx`）成为标记模板；每个实例将其标量属性渲染为 `data-*` 和 CSS 自定义属性。

在 T3 中验证 — 三个 StatCards 使用不同属性重用，平均 SSIM 0.953。

## 需要类型解析的数字属性

`document.getElementById("stage").dataset.count` 是字符串。在读取时转换：

```js
const count = Number(stage.dataset.count);
```

或者当数据在翻译时已知且不需要因渲染而异时，将值直接内联到 GSAP 脚本中。

## 布尔属性

```tsx
defaultProps={{ darkMode: true }}
```

两种约定：

- `data-dark-mode="true"` — 作为字符串读取，比较 `=== "true"`
- `data-dark-mode`（存在/缺失） — true 时 `<div data-dark-mode>`，false 时省略

选择一种并保持一致。存在/缺失形式符合 HTML 习惯，并且与 CSS 属性选择器配合良好：

```css
[data-dark-mode] .scene {
  background: #000;
}
```

## Zod 运行时验证

Remotion 的 `schema` 在合成加载时验证属性。HF 没有等价物 — 当 HTML 进入渲染器时，schema 已经不存在了。

改为在翻译时验证。如果用户传递了无效数据，在生成 HTML 之前以翻译错误失败。这符合 Zod 的"大声失败"意图，而不需要运行时依赖。

## 当合成使用属性进行计算派生

```tsx
const Composition: React.FC<Props> = ({ stats }) => {
  const total = stats.reduce((acc, s) => acc + s.value, 0);
  return <div>{total}</div>;
};
```

在翻译时计算派生值，并将其烘焙到 HTML 或 `data-` 属性中。不要在 HF 合成中尝试用 JS 表达计算 — 这会增加运行时开销，并使 HTML 以复杂化人工编辑的方式变为有状态。

如果派生过程非平凡（涉及数组本身，而不仅仅是标量），将其物化为 HTML 中的静态文本。
