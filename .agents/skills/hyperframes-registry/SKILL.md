---
name: hyperframes-registry
description: 安装并将注册表块和组件接入 HyperFrames 作品。在运行 hyperframes add、安装块或组件、将已安装项接入 index.html 或处理 hyperframes.json 时使用。涵盖 add 命令、安装位置、块子作品接入、组件片段合并、注册表发现以及创作新块或组件以贡献上游（想法 → 脚手架 → 验证 → PR）。
---

# HyperFrames 注册表

注册表提供可通过 `hyperframes add <name>` 安装的可重用块和组件。

- **块（Blocks）**——独立子作品（有自己的尺寸、时长、时间线）。通过宿主作品中的 `data-composition-src` 引入。
- **组件（Components）**——效果片段（没有自己的尺寸）。直接粘贴到宿主作品的 HTML 中。

## 快速参考

```bash
hyperframes add data-chart              # 安装块
hyperframes add grain-overlay           # 安装组件
hyperframes add shimmer-sweep --dir .   # 指定目标项目
hyperframes add data-chart --json       # 机器可读输出
hyperframes add data-chart --no-clipboard  # 跳过剪贴板（CI/无头）
```

安装后，CLI 会打印已写入的文件以及要粘贴到宿主作品中的片段。片段是起点——在接入块时，你需要添加 `data-composition-id`（必须与块的内部作品 ID 匹配）、`data-start` 和 `data-track-index` 属性。

注意：`hyperframes add` 仅适用于块和组件。对于示例，使用 `hyperframes init <dir> --example <name>`。

## 安装位置

块默认安装到 `compositions/<name>.html`。
组件默认安装到 `compositions/components/<name>.html`。

这些路径可在 `hyperframes.json` 中配置：

```json
{
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  }
}
```

参见 [install-locations.md](./references/install-locations.md) 了解完整详情。

## 接入块

块是独立作品——通过宿主 `index.html` 中的 `data-composition-src` 引入：

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

关键属性：

- `data-composition-src`——块 HTML 文件的路径
- `data-composition-id`——必须与块的内部 ID 匹配
- `data-start`——块在宿主时间线中出现的时间（秒）
- `data-duration`——块播放的时长
- `data-width` / `data-height`——块画布尺寸
- `data-track-index`——图层排序（越高越靠前）

参见 [wiring-blocks.md](./references/wiring-blocks.md) 了解完整详情。

## 接入组件

组件是片段——将其 HTML 粘贴到作品的标记中、CSS 粘贴到样式块中、JS 粘贴到脚本中（如果有）：

1. 读取已安装的文件（例如 `compositions/components/grain-overlay.html`）
2. 将 HTML 元素复制到你的作品的 `<div data-composition-id="...">` 中
3. 将 `<style>` 块复制到作品的样式中
4. 将任何 `<script>` 内容复制到作品的脚本中（在你的时间线代码之前）
5. 如果组件暴露了 GSAP 时间线集成（见片段中的注释块），将这些调用添加到你的时间线

参见 [wiring-components.md](./references/wiring-components.md) 了解完整详情。

## 发现

浏览可用项：

```bash
# 读取注册表清单
curl -s https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json
```

每个项的 `registry-item.json` 包含：名称、类型、标题、描述、标签、尺寸（仅块）、时长（仅块）和文件列表。

参见 [discovery.md](./references/discovery.md) 了解按类型和标签过滤的详情。

## 贡献新块或组件

要创作一个新的注册表项（字幕风格、VFX 块、过渡、下方三分之一或可重用组件）并将其作为上游 PR 提交——而不是安装现有的——请遵循 [contributing.md](./references/contributing.md) 中的完整想法 → 脚手架 → 构建 → 验证 → 预览 → 发布工作流。可复制粘贴的起始模板（字幕 / VFX / 组件 / `registry-item.json`）在 [templates.md](./references/templates.md) 中。
