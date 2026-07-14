# 过渡目录

硬规则、场景模板和实现代码的路由。读取你需要的过渡类型的参考文件 — 不要全部加载。

## 内容

- CSS 过渡的硬规则
- 着色器过渡
- 场景模板
- CSS 过渡示例
- 着色器过渡路由

## CSS 的硬规则

这些如果违反会导致真实错误。

**场景可见性：** 场景 1 默认可见（无 `opacity: 0`）。场景 2+ 在 CONTAINER div 上有 `opacity: 0`。GSAP 揭示它们。无可见性垫片（`timedEls`）。

**字体：** 只需写你想要的 `font-family` — 编译器通过 `@font-face` 自动嵌入支持的字体，使用内联数据 URI。无需 `<link>` 标签或 `@import`。在所有上下文中工作，包括沙箱 iframe。

**元素结构：** 独立组合中场景 div 上无 `class="clip"`。只有根 div 获得 `data-composition-id`/`data-start`/`data-duration`。

**叠加元素：** 错开块 = 全屏 1920x1080，非细条。故障 RGB 叠加 = 35% 不透明度的正常混合，非 `mix-blend-mode: multiply`（在暗背景上不可见）。漏光叠加 = 大于画面（2400px+），从不是可见形状。过曝光 = 在场景上使用 `filter: brightness()`，而非仅白色叠加。

**VHS 磁带：** 用 `cloneNode(true)` 克隆实际场景内容，非彩色条。每个条：宽于画面（2020px 在 left:-50px）。红+蓝色差副本在 z-index 高于主条。种子化 PRNG 用于确定性随机偏移。

**Z-index：** 重力掉落、缩小、对角分割需要退出场景在最上面（`zIndex: 10`），使其退出同时揭示后面的新场景（`zIndex: 1`）。

**页面灼烧：** 内容随页面灼烧 — 无坠落碎片。通过 `tl.set` 在灼烧结束时隐藏 scene1，永远不要 `onComplete`（不可逆）。`onUpdate` 必须在 `wp <= 0` 时恢复 `clipPath: "none"` 以支持倒带。进入场景在灼烧 90% 时从黑色淡入。

**时钟擦拭：** 带中间边缘位置的 9 点多边形。用单独的补间遍历 4 个象限。

**网格溶解：** 每单元格循环 5 种调色板颜色，非单色。

**百叶窗数量按能量：** 平静：4h/6v。中等：6-8h/8v。高：12-16h/16v。

**不要使用：** 星形虹膜（多边形插值损坏）、移轴（无选择性 CSS 模糊）、镜头光晕（可见形状，非光学）、铰链/门（扭曲太快）。

## 着色器过渡

着色器设置、WebGL 初始化、捕获和片段着色器由 `@hyperframes/shader-transitions`（`packages/shader-transitions/`）处理。读取包源获取 API 细节。使用着色器的组合必须遵循 `overview.md`（此目录）中的着色器兼容 CSS 规则。

## 场景模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    body { margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #000;
      font-family: "YOUR FONT", sans-serif; /* 编译器自动嵌入支持的字体 */ }
    .scene { position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; overflow: hidden; }
    #scene1 { z-index: 1; background: #color; }
    #scene2 { z-index: 2; background: #color; opacity: 0; }
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-width="1920" data-height="1080"
       data-start="0" data-duration="TOTAL">
    <div id="scene1" class="scene"><!-- visible --></div>
    <div id="scene2" class="scene"><!-- hidden --></div>
  </div>
  <script>
    window.__timelines = window.__timelines || {};
    var tl = gsap.timeline({ paused: true });
    // 过渡代码在此
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
```

每个过渡遵循：定位新场景 → 动画退出 → 交换 → 动画进入 → 清理叠加。

## CSS 过渡

所有代码示例使用 `old` 表示退出场景内部选择器，`new` 表示进入场景，`T` 表示过渡开始时间。读取你需要的类型的参考文件。

| 类型           | 过渡                                            | 参考                              |
| -------------- | ----------------------------------------------- | --------------------------------- |
| 推动           | 推动滑动、垂直推动、弹性推动、挤压              | `transitions/css-push.md`         |
| 径向/形状      | 圆形虹膜、菱形虹膜、对角分割                    | `transitions/css-radial.md`       |
| 3D             | 3D 卡片翻转                                     | `transitions/css-3d.md`           |
| 缩放/缩放      | 缩放穿过、缩小                                  | `transitions/css-scale.md`        |
| 溶解           | 交叉淡入淡出、模糊交叉淡入淡出、焦距拉动、浸入  | `transitions/css-dissolve.md`     |
| 覆盖           | 错开块、水平百叶窗、垂直百叶窗                  | `transitions/css-cover.md`        |
| 光             | 漏光、过曝光灼烧、胶片灼烧                      | `transitions/css-light.md`        |
| 扭曲           | 故障、色差、涟漪、VHS 磁带                      | `transitions/css-distortion.md`   |
| 机械           | 快门、时钟擦拭                                  | `transitions/css-mechanical.md`   |
| 网格           | 网格溶解                                        | `transitions/css-grid.md`         |
| 其他           | 重力掉落、变形圆                                | `transitions/css-other.md`        |
| 模糊           | 模糊穿过、方向模糊                              | `transitions/css-blur.md`         |
| 破坏           | 页面灼烧                                        | `transitions/css-destruction.md`  |

## 着色器过渡

WebGL 着色器过渡由 `@hyperframes/shader-transitions`（`packages/shader-transitions/`）提供。包处理设置、捕获、WebGL 初始化、渲染循环和 GSAP 集成。读取包源以获取可用着色器和 API — 不要手动复制原始 GLSL。

内置着色器不是上限。对于没有内置覆盖的效果，你可以从头编写自定义 GLSL，适配在线找到的着色器代码（ShaderToy、GLSL Sandbox、GitHub），或构建适合没有现有类别的自定义 CSS 过渡 — 以新方式组合 clip-path、变换和滤镜。如果故事板呼唤一个尚不存在的效果，构建它；框架渲染任何浏览器能运行的内容。
