# 接入组件

组件是效果片段——HTML、CSS 和可选的 JS，你直接合并到现有作品中。与块不同，组件没有独立的时间线；它们参与宿主作品的时间线。

## 通用流程

1. 运行 `hyperframes add <component-name>`
2. 打开已安装的文件（例如 `compositions/components/grain-overlay.html`）
3. 阅读注释标题中的使用说明
4. 将各部分复制到你的宿主作品中：
   - **HTML 元素**——在你的 `<div data-composition-id="...">` 内部
   - **CSS 样式**——放入作品的 `<style>` 块
   - **JS 设置**——放入作品的 `<script>`，在你的时间线代码之前
   - **时间线调用**——放入你的 GSAP 时间线（如果组件暴露了它们）

## 示例：grain-overlay（纯 CSS，无需时间线集成）

```html
<!-- 将叠加 div 粘贴到你的作品中 -->
<div
  id="grain-overlay"
  style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 100;"
>
  <div class="grain-texture"></div>
</div>
```

然后将 CSS 关键帧和 `.grain-texture` 规则粘贴到你的样式中。无需 GSAP 时间线调用——颗粒通过 CSS `@keyframes` 动画。

## 示例：shimmer-sweep（需要时间线集成）

参见 `examples/add-component.md` 了解完整的 shimmer-sweep 演示（HTML 包装、CSS、JS 设置和时间线调用）。

## 关键原则

- 组件继承宿主作品的尺寸和时长
- 将组件 HTML 放在相对于你内容的适当 z-index 处
- 阅读每个片段中的注释标题以了解可自定义的值
- 接入后运行 `hyperframes lint` 以捕获结构问题
