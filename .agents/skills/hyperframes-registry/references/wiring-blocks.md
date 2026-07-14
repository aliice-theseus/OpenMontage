# 接入块

块是独立作品，有自己的 `data-composition-id`、尺寸、时长和 GSAP 时间线。通过在 `<div>` 上使用 `data-composition-src` 将其包含在宿主作品中。

## 基本接入

在 `hyperframes add data-chart` 后，将其接入你的 `index.html`：

```html
<div id="stage" data-composition-id="main" data-width="1920" data-height="1080" data-duration="20">
  <video id="a-roll" src="video.mp4" data-start="0" data-duration="20" data-track-index="0"></video>

  <!-- 块：在 2s 出现，播放 15s，在第 1 层 -->
  <div
    data-composition-id="data-chart"
    data-composition-src="compositions/data-chart.html"
    data-start="2"
    data-duration="15"
    data-track-index="1"
    data-width="1920"
    data-height="1080"
  ></div>
</div>
```

## 必需属性

| 属性 | 描述 |
| ---------------------- | -------------------------------------------------------------------- |
| `data-composition-src` | 块 HTML 文件的路径（相对于 index.html） |
| `data-composition-id` | 与块的内部作品 ID 匹配的唯一 ID |
| `data-start` | 块在宿主时间线中出现的时间（秒） |
| `data-duration` | 块播放的时长（秒，最多为块自身的时长） |
| `data-track-index` | 图层排序——更高的数字渲染在前 |
| `data-width` | 块画布宽度（与块的尺寸匹配） |
| `data-height` | 块画布高度（与块的尺寸匹配） |

## 时间线协调

块的内部 GSAP 时间线与宿主时间线独立运行。HyperFrames 运行时加载子作品，找到其 `window.__timelines` 注册，并在与宿主同步的情况下定位块，偏移量为 `data-start`。你不需要在宿主的 GSAP 代码中引用块的时间线。

## 定位块

要将块定位在屏幕的特定区域，添加 CSS：

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
  style="position: absolute; right: 0; top: 0; width: 40%; height: 100%;"
></div>
```

## 多个块

添加额外的 `<div data-composition-src="...">` 兄弟元素，使用不重叠或重叠的 `data-start` 值——每个块的时间线都是独立的，由运行时同步定位。
