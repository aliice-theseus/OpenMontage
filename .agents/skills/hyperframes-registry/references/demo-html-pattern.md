# demo.html 约定

## 为什么组件附带 demo.html

注册表中的每个组件都附带一个 `demo.html` 文件，与其片段一起存在。demo 有两个目的：

1. **预览夹具**——CI 预览流水线渲染 demo 以为目录文档页面生成缩略图和预览视频。
2. **使用示例**——demo 展示了应用于代表性内容的组件效果，作为工作参考。

## Demo 结构

demo 是一个完整的独立 HTML 作品：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>组件名称 — Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      /* 重置 + 画布大小 */
    </style>
  </head>
  <body>
    <div data-composition-id="<name>-demo" data-width="1920" data-height="1080" data-duration="N">
      <!-- 展示效果的 Demo 内容 -->
      <!-- 内联组件片段 -->
    </div>
    <script>
      // 演示效果的 GSAP 时间线
      window.__timelines = window.__timelines || {};
      window.__timelines["<name>-demo"] = tl;
    </script>
  </body>
</html>
```

关键约定：

- `data-composition-id` 为 `<component-name>-demo` 以避免冲突
- demo 是自包含的——片段中的所有 CSS 和 JS 都已内联
- GSAP 时间线注册在 `window.__timelines` 上
- 时长应足够展示效果（通常 5-8 秒）

## 块不需要 demo.html

块已经是可直接渲染的独立作品。只有组件需要 demo 包装器。

## Demo 不被安装

`demo.html` **不**由 `hyperframes add` 安装——它仅存在于注册表中，用于预览生成和作为参考。
