# 背景去除

制作透明叠加层（典型用途：将讲话人置于任意场景之上）。使用 `u2net_human_seg`（MIT 许可）。

```bash
npx hyperframes remove-background subject.mp4 -o transparent.webm          # 默认：VP9 + alpha
npx hyperframes remove-background subject.mp4 -o transparent.mov           # ProRes 4444（编辑用）
npx hyperframes remove-background portrait.jpg -o cutout.png               # 单张图片抠图
npx hyperframes remove-background subject.mp4 -o subject.webm \
  --background-output plate.webm                                           # 一次处理输出两层
npx hyperframes remove-background subject.mp4 -o transparent.webm --device cpu
npx hyperframes remove-background --info                                   # 显示检测到的提供商
```

## 输出格式

- **`.webm`（VP9 alpha）**——默认。直接插入 `<video>` 即可在 Chrome 中实现原生透明播放（约 1 MB / 4s @ 1080p）。
- **`.mov`（ProRes 4444）**——可在编辑器中来回处理（Premiere / Resolve / DaVinci）。约 50 MB / 4s。
- **`.png`**——单张图片抠图。

## 质量（`--quality`）

仅控制 VP9 编码器的 CRF——分割质量是固定的。更高质量能使抠图的 RGB 更接近源 MP4（在将抠图叠加到其自身源上时很重要）。

| 预设 | CRF | 使用场景 |
| ---------- | --- | --------------------------------------------- |
| `fast` | 30 | 迭代中，更小的文件，颜色匹配较宽松 |
| `balanced` | 18 | **默认**；对大多数用途来说视觉上无差异 |
| `best` | 12 | 母版/最终交付，颜色匹配最精确 |

## 设备（`--device`）

`auto`（默认）在 Apple Silicon 上选择 CoreML，在有 CUDA 时选择 CUDA，否则使用 CPU。可使用 `--device cpu | coreml | cuda` 强制指定。CUDA 需要 `HYPERFRAMES_CUDA=1` 以及支持 GPU 的 `onnxruntime-node` 构建。使用 `--info` 检查检测到的提供商，无需实际渲染。

## 合成模式——选择正确的模式

抠图的 WebM 是源 MP4 RGB 的**重新编码副本**。其背后是什么很重要。

| 模式 | 抠图背后 | 结果 |
| -------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **将抠图放在不同场景上**（最常见） | 静态图像、渐变、不相关的视频 | 效果很好。主体的单个 RGB 源。 |
| **将抠图放在其自身的源 mp4 上**（文字在主体后方） | 抠图来源的同一个 mp4 | 在 `balanced` 模式下，加倍几乎不可见；在 `fast` 模式下，会看到颜色偏移/边缘光晕。母版请使用 `best`。 |
| **将抠图放在同一人的不同镜头之上** | 同一主体的画面 | **两个人重叠。不要这样做。** |

## 文字在主体后方模式（两个不明显的规则）

将标题放在演讲者抠图后面：

```html
<video
  src="presenter.mp4"
  id="bg"
  data-start="0"
  data-duration="6"
  data-track-index="0"
  muted
  playsinline
></video>

<h1 id="headline" style="z-index:2; ...">用 HYPERFRAMES 制作</h1>

<div class="cutout-wrap" style="position:absolute; inset:0; z-index:3; opacity:0">
  <video
    src="presenter.webm"
    data-start="0"
    data-duration="6"
    data-track-index="1"
    muted
    playsinline
  ></video>
</div>
```

```js
// 在切换处翻转包装器的透明度，而不是视频的
tl.set(".cutout-wrap", { opacity: 1 }, 3.3);
```

两个容易忽略的规则：

1. **将抠图 `<video>` 包裹在非定时的 `<div>` 中，并动画化包装器的透明度，而不是 video 元素本身。** 框架会在激活的片段（任何带有 `data-start` / `data-duration` 的元素）上强制设置 `opacity: 1`，因此直接动画化 video 的透明度会被静默覆盖。包装器没有 `data-*` 属性，因此它归你的 CSS / GSAP 所有。
2. **两个视频都使用 `data-start="0"` 和 `data-media-start="0"`**，这样框架会从 t=0 开始同步解码它们。延迟挂载抠图（`data-start=3.3`）会引入一次 seek + 预热，导致画面与基础 mp4 错位一帧——在切换处可见一帧的对齐偏差。

## 图层分离（`--background-output`）

在抠图旁边输出**第二个**透明视频：相同的源 RGB，alpha 是 `255 - mask` 而不是 `mask`。抠图中主体不透明；底板中周围环境不透明（主体位置有一个透明孔）。当文字/图形需要位于**两层之间**时使用。

| 文件 | Alpha 是…… | 用途 |
| -------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------- |
| `-o subject.webm` | mask——主体不透明，背景透明 | 前景层（顶部） |
| `--background-output plate.webm` | 反转 mask——周围环境不透明，主体透明 | 底层；将文字/图形放在此层与主体之间 |

两者共享相同的 `--quality`，来自单次推理——只有编码成本大约翻倍。仅对视频输入且输出为 `.webm` / `.mov` 时有效。

**挖孔，不是修复。** `plate.webm` 中的主体区域完全透明——在其下方合成不透明内容以填充孔洞。

**判断 `--background-output` 是否是正确的工具的单一测试：** _是否会有任何东西通过主体的轮廓在其原来的位置变得可见？_ 如果不会，你不需要底板——单独将 `subject.webm` 放在不同背景上就足够了。

### 用例 → 正确工具

| 用例 | 正确工具 |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 文字/图形在抠图和底板之间（此命令存在的原因） | **挖孔**（`--background-output`） |
| 主体放到不相关的场景上 | 只需 `subject.webm`；忽略底板 |
| 显示没有人的房间，单独显示，没有其他内容 | **清洁底板**——需要修复工具（LaMa、ProPainter、E2FGVI）。不是此命令。 |
| 用不同的主体替换主体 | **清洁底板**——同上 |

### 经典的三层模板（底板 + 内容 + 抠图）

只输出两个透明层，让任意内容存在于它们之间——无需原始 mp4：

```html
<!-- z=1 底板：周围环境不透明，主体轮廓透明 -->
<video
  src="plate.webm"
  data-start="0"
  data-duration="6"
  data-track-index="0"
  muted
  playsinline
></video>

<!-- z=2 你的内容位于层之间 -->
<h1 id="headline" style="z-index:2; ...">用 HYPERFRAMES 制作</h1>

<!-- z=3 抠图将主体放回顶部 -->
<div class="cutout-wrap" style="position:absolute; inset:0; z-index:3">
  <video
    src="subject.webm"
    data-start="0"
    data-duration="6"
    data-track-index="1"
    muted
    playsinline
  ></video>
</div>
```

功能上等同于上面的文字在主体后方模式，但不需要提供原始 mp4——底板替代了它。当只输出两个透明层作为可重用资源时使用此方法。

## 何时 `remove-background` 不是正确的工具

如果用户要求「**没有**人的房间，单独显示」（没有主体，没有叠加合成），`--background-output` 是错误的——它的底板有一个透明孔，而不是填充好的清洁底板。他们需要**修复工具**：LaMa、ProPainter 或 E2FGVI。告诉他们此命令无法做到。
