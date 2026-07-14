# 设计规范 — `frame.md` / `design.md`

关于**设计规范是什么、如何找到它以及如何阅读它**的单一信息源。其他参考资料在此解析格式；_消费_合约（"品牌，不是布局"）存在于 `video-composition.md` 中。

## `frame.md` 是什么

`frame.md` 是视频/hyperframes 项目的**帧级设计系统**——`design.md`（为网页/静态页面编写）的视频优先伴侣。与 `design.md` 相同的文件格式；它以帧为单位重新定义品牌。

一个规范是 **YAML frontmatter + markdown 正文**，两个层级不相等：

- **Frontmatter 是规范层** — `colors`、`typography`、`spacing`、`components` 是真正的机器可读值。逐字引用它们（确切的十六进制、字体家族、字重）；永远不要发明或四舍五入。
- **散文是上下文** — `##` 部分（概述、帧、构图规则……）承载意图、使用时机以及令牌无法容纳的约束。阅读它们用于判断，而非用于取值。

## 解析要读取的规范

优先级——读取**第一个存在的**，忽略其余：

```
frame.md  →  design.md  →  DESIGN.md
```

```bash
SPEC=$(ls frame.md design.md DESIGN.md 2>/dev/null | head -1)
```

- `frame.md` 是视频/hyperframes 项目的首选规范，当存在多个时胜出。
- `frame.md` **始终是小写**——没有 `FRAME.md` 变体。（`design.md` 和 `DESIGN.md` 在 Linux 上是真正不同的文件；帧预设提供的是大写的 `FRAME.md` _模板_，采用为小写 `frame.md`——参见下面的"从预设开始"。）

**在步骤 1 中一次性**加载规范；之后的每一步（扩展、创作、遵循）都使用已加载的规范，而不是重新解析。

## 从预设开始（可选）

可选地从 `[../frame-presets/](../frame-presets/)` 中的现成**帧预设**播种 `frame.md`——固定集合，每个提供一个 `FRAME.md` 模板，工作流的设计步骤将其复制进来并用品牌令牌覆盖。引用预设**不是必需的**；定制的或由[选择器](design-picker.md)生成的规范同样有效。

| 预设                                                               | 外观                                                                                                                                                                                                                                                                                                                       | 选择时机                                                                                                                         |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `[biennale-yellow](../frame-presets/biennale-yellow/FRAME.md)`     | 文学编辑目录——暖羊皮纸底色，单一深靛蓝油墨，太阳黄作为径向光晕/面板/瓷砖底色，Instrument Serif 400 展示（紧缩，负字距）+ Archivo 正文 + JetBrains Mono 数据，严格矩形（0 圆角），1px 发丝线作为唯一边框，无阴影                                                   | 自信 / 氛围 / 克制；想要博物馆目录优雅和编辑权威的产品                                                                            |
| `[blockframe](../frame-presets/blockframe/FRAME.md)`               | 极繁新粗野主义——4px 黑色边框，8px 硬偏移阴影，五种糖果粉彩，Inter 800-900 大写，方角，倾斜装饰                                                                                                                                                                                                                              | 大胆 / 有力 / 俏皮响亮；想要感到自信和图形化的产品                                                                                |
| `[blue-professional](../frame-presets/blue-professional/FRAME.md)` | 咨询级克制——暖奶油画布，单一饱和钴蓝（#1e2bfa）强调，Space Grotesk + Inter 排版，柔和着色卡片（4% 填充 / 20% 边框 / 10-14px 圆角）无阴影，药丸铬色（100px），三步灰文本阶梯，钴蓝进度条                                                                      | 有分寸 / 高管可读 / 高级信号；想要投资研究严谨性和精致克制感的产品                                                               |
| `[bold-poster](../frame-presets/bold-poster/FRAME.md)`             | 民粹编辑海报——Shrikhand 展示倾斜 -6°..+2°，Libre Baskerville 衬线正文，Space Grotesk 等宽铬色，仅四色（白 / 棕黑油墨 / 番茄红 / 米白），双边框网格（3px+1.5px），红色左边距卡片，红色 em-dash 项目符号，红色展示上的堆叠文字阴影，方角                              | 有力 / 印刷感 / 克制；想要编辑权威和复古庄重的产品                                                                               |
| `[broadside](../frame-presets/broadside/FRAME.md)`                 | 抗议海报系统——双色域平面（墨黑 / 火焰橙），大尺寸小写 Barlow 900 作为图形基元，IBM Plex Mono 铬色（大写，0.14em），火焰橙唯一强调，1px 发丝线，锐角，无阴影                                                                                                    | 大胆 / 排版 / 宣言式；想要存在感和权威的产品                                                                                     |
| `[capsule](../frame-presets/capsule/FRAME.md)`                     | 俏皮编辑——每个容器都是药丸形（2px 墨轮廓），奶油画布，九种糖果强调色，Bodoni Moda + Space Grotesk，柔和偏移阴影，浮动药丸壁纸                                                                                                                                    | 友好 / 柔和 / 编辑风；想要温暖和亲切感的产品                                                                                     |
| `[cartesian](../frame-presets/cartesian/FRAME.md)`                 | 博物馆目录编辑——1px 灰褐发丝网格，五色暖石调色板（#EDE8E0 / #E2DBD1 / #1A1A1A / #5A5A5A / #8A8178），Playfair Display 400 + Inter，锐角，圆规绘制的几何环，零阴影 / 零填充                                                                                      | 稀疏 / 文学 / 克制；想要安静权威和编辑严谨性的产品                                                                               |
| `[claude](../frame-presets/claude/FRAME.md)`                       | 温暖编辑品牌书——暖奶油纸（从不纯白），陶土珊瑚（#CC785C）作为稀缺电压，发丝墨色抬升（无沉重阴影），EB Garamond 衬线展示 + Inter 正文 + JetBrains Mono 索引/代码在暖海军蓝代码表面，句首字母大写展示，✱ 珊瑚尖刺                                            | 深思熟虑 / 文学 / 面向开发者；代码变更、发布或文档，想要编辑冷静和一流代码表面的产品                                              |
| `[cobalt-grid](../frame-presets/cobalt-grid/FRAME.md)`             | 现代主义双色 risograph——奶油纸，电钴蓝油墨，永久方格纸网格（10% 钴蓝），顶部/底部钴蓝发丝线，Newsreader 400 衬线 + Hanken Grotesk + DM Mono，0° 角，像素故障列 + QR 块补丁                                                                                     | 克制 / 系统化 / 编辑风；想要清晰和有节制权威的产品                                                                                |
| `[coral](../frame-presets/coral/FRAME.md)`                         | 大胆编辑杂志——三个实色表面（珊瑚火 / 墨黑 / 暖奶油）在硬边缘交汇，45° 对角线阴影在珊瑚上，Bebas Neue + Inter 追踪大写，零阴影/半径（圆形 50%），超大壁纸数字和巨大标记                                                                                          | 大胆 / 结构主义 / 编辑风；想要图形自信和硬朗确定性的产品                                                                          |
| `[creative-mode](../frame-presets/creative-mode/FRAME.md)`         | 新粗野主义编辑——奶油画布，4px 墨色边框，硬偏移阴影（无模糊），四种强调色限用两到三种，Archivo Black 大写 0.92 行高，JetBrains Mono 分类，Space Grotesk 正文，除一个药丸碎片外均为方角                                                                            | 稀疏 / 图形化 / 有力而克制；想要编辑存在感和几何自信的产品                                                                        |
| `[daisy-days](../frame-presets/daisy-days/FRAME.md)`               | 快乐图画书——3px 炭笔轮廓，6/4px 硬偏移阴影（无模糊），九种阳光花园粉彩（奶油 + 蓝绿/柔粉/黄油/薄荷/薰衣草/桃/天蓝 + 珊瑚强调），Fredoka One + Quicksand，大圆角（20-50px），手绘 SVG 装饰层（雏菊/星星/太阳/云/彩虹）                                      | 俏皮 / 童真 / 贴纸 kawaii；想要温暖和奇思妙想的产品                                                                              |
| `[editorial-forest](../frame-presets/editorial-forest/FRAME.md)`   | 衬线领先的文学编辑——绿/粉/奶油编辑三元组，Source Serif 4 字重 500（opsz）展示 + JetBrains Mono 500 大写铬色，平面纸质深度（无阴影），2px 发丝线规则，6/8px 卡片圆角，字母组合圆形印章                                                                        | 宽敞 / 克制 / 编辑风；想要安静自信和文学基调的产品                                                                                |

每个预设文件夹还附带一个 `frame-showcase.html`——其帧处理的预览样张；打开它_查看_外观，永远不要将其包含在项目中。

## 消费规范

如何将规范应用到帧——品牌严格（十六进制、字体、字重关系、该做/不该做），布局自由——是 `[video-composition.md](video-composition.md)`（"设计规范是品牌，不是布局"）中的消费合约。在选择颜色或编写 HTML 之前阅读它；本文档仅涵盖查找和解析规范。
