# 贡献模板

每种组件类型的可复制粘贴起始模板。这些嵌入了经过验证的模式，可通过 lint 和 validate。

## 字幕模板

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <link
      href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&display=swap"
      rel="stylesheet"
    />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
      body { background:#111; overflow:hidden; }
      #root-BLOCKNAME { position:relative; width:1920px; height:1080px; overflow:hidden; background:#111; }
      .cap-container { position:absolute; top:0; left:0; width:100%; height:100%; display:flex; align-items:center; justify-content:center; }
      .cg { position:absolute; display:flex; align-items:center; justify-content:center; gap:32px; max-width:1700px; overflow:visible; opacity:0; visibility:hidden; }
      .cw { font-family:"Montserrat",sans-serif; font-weight:900; font-size:128px; color:#ffffff; text-transform:uppercase; line-height:1; display:inline-block; -webkit-text-stroke:3px rgba(0,0,0,0.8); paint-order:stroke fill; text-shadow:0 4px 12px rgba(0,0,0,0.5); }
    </style>
  </head>
  <body>
    <!-- 模板内容，需要替换 BLOCKNAME 和 PREFIX -->
  </body>
</html>
```

**替换清单：**

- `BLOCKNAME` → 你的块名称（例如 `cap-swoosh`）
- `PREFIX` → 短唯一 ID 前缀（例如 `sw`）
- 字体家族、权重、大小 → 你的样式的排版
- 入口动画 → 你的样式的入口
- 卡拉 OK 高亮 → 你的样式的活跃词处理
- 颜色 → 你的样式的调色板

## registry-item.json 模板

**对于块：**

```json
{
  "$schema": "https://hyperframes.heygen.com/schema/registry-item.json",
  "name": "BLOCKNAME",
  "type": "hyperframes:block",
  "title": "人类可读标题",
  "description": "一句话：它的作用和谁使用它",
  "dimensions": { "width": 1920, "height": 1080 },
  "duration": 10,
  "tags": ["category", "subcategory"],
  "files": [
    {
      "path": "BLOCKNAME.html",
      "target": "compositions/BLOCKNAME.html",
      "type": "hyperframes:composition"
    }
  ]
}
```

**对于组件（无 `dimensions` 或 `duration`）：**

```json
{
  "$schema": "https://hyperframes.heygen.com/schema/registry-item.json",
  "name": "COMPONENTNAME",
  "type": "hyperframes:component",
  "title": "人类可读标题",
  "description": "一句话：它的作用",
  "tags": ["category"],
  "files": [
    {
      "path": "COMPONENTNAME.html",
      "target": "compositions/components/COMPONENTNAME.html",
      "type": "hyperframes:snippet"
    }
  ]
}
```

## 组件模板

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
      body { background:transparent; overflow:hidden; }
      .COMPNAME-wrap { position:absolute; inset:0; overflow:hidden; pointer-events:none; }
    </style>
  </head>
  <body>
    <div class="COMPNAME-wrap">
      <!-- 你的可重用效果/叠加在此 -->
    </div>
    <script>
      (function () {
        // 组件片段——没有 data-composition-id，没有 __timelines。
        // 父作品控制时序。
        // 所有类名和 ID 使用 COMPNAME 前缀。
      })();
    </script>
  </body>
</html>
```

**替换清单：**

- `COMPNAME` → 你的组件名称（例如 `shimmer-sweep`）
- 背景应为 `transparent` 以便干净叠加
- 无 `data-composition-id` 或 `window.__timelines`——父级拥有时序
