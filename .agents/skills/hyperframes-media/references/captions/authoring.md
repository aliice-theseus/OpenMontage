# 字幕

在创作之前：确认转录来自正确的 Whisper 模型。CLI 默认的 `small.en` 会静默翻译非英语音频——参见 [`../transcribe.md`](../transcribe.md) →「语言规则」和 [`transcript-handling.md`](transcript-handling.md) 了解强制性质量检查。

分析口语内容以确定字幕风格。如果用户指定了风格，使用该风格。否则，从转录中检测语调。

## 转录来源

```json
[
  { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 },
  { "id": "w1", "text": "world.", "start": 0.6, "end": 1.2 }
]
```

`id`（`w0`、`w1`……）是逐词覆盖的稳定引用，由 `hyperframes transcribe` 添加。对于手动编写的转录，向后兼容时可省略。参见 [`../transcribe.md`](../transcribe.md) →「输出格式」了解如何生成，以及 [`transcript-handling.md`](transcript-handling.md) 了解消费前的清理。

## 风格检测（未指定风格时）

在做出选择之前阅读完整的转录。四个维度：

**1. 视觉感受**——企业→简洁；充满活力→粗体；叙事→优雅；技术→精确；社交→俏皮。

**2. 调色板**——深色+明亮用于活力；柔和用于专业；高对比用于清晰；一种强调色。

**3. 字体情绪**——粗体/窄体用于冲击力；简洁无衬线用于现代；圆润用于友好；衬线用于优雅。

**4. 动画特性**——缩放弹出用于有力；柔和淡出用于平静；逐词用于强调；打字机用于技术。

## 逐词样式

扫描需要特殊处理的词语：

- **品牌/产品名称**——更大的字号，独特的颜色
- **全大写**——缩放提升，闪烁，强调色
- **数字/统计数据**——粗体，强调色
- **情感关键词**——夸张动画（过冲、弹跳）
- **行动号召**——高亮、下划线、颜色弹出
- **标记高亮**——对于超越颜色的强调（高亮扫光、圆形、爆发、涂鸦、草图轮廓），参见 `hyperframes-animation/rules/css-marker-patterns.md`

## 脚本到样式的映射

| 语调 | 字体情绪 | 动画 | 颜色 | 字号 |
| ------------ | ------------------------ | ---------------------------------- | --------------------------- | ------- |
| 炒作/发布 | 粗体窄体，800-900 | 缩放弹出，back.out(1.7)，0.1-0.2s | 亮色背景上的亮色 | 72-96px |
| 企业 | 简洁无衬线，600-700 | 淡出+滑动，power3.out，0.3s | 白色/中性，柔和强调 | 56-72px |
| 教程 | 等宽/简洁无衬线，500-600 | 打字机/淡出，0.4-0.5s | 高对比，最小化 | 48-64px |
| 叙事 | 衬线/优雅，400-500 | 慢淡出，power2.out，0.5-0.6s | 暖柔和的色调 | 44-56px |
| 社交 | 圆润无衬线，700-800 | 弹跳，elastic.out，逐词 | 俏皮，彩色药丸 | 56-80px |

## 词语分组

- **高能量：** 2-3 个词。快速更替。
- **对话式：** 3-5 个词。自然短语。
- **有节制的/平静：** 4-6 个词。较长的组。

在句子边界、150ms+ 停顿或最大词数处断开。

## 定位

- **横屏（1920x1080）：** 底部 80-120px，居中
- **竖屏（1080x1920）：** 中下部，距底部约 600-700px，居中
- 永远不要遮挡主体的面部
- `position: absolute`——永远不要 relative
- 一次只显示一个字幕组

## 文本溢出预防

使用 `window.__hyperframes.fitTextFontSize()`：

```js
var result = window.__hyperframes.fitTextFontSize(group.text.toUpperCase(), {
  fontFamily: "Outfit",
  fontWeight: 900,
  maxWidth: 1600,
});
el.style.fontSize = result.fontSize + "px";
```

选项：`maxWidth`（横屏 1600，竖屏 900）、`baseFontSize`（78）、`minFontSize`（42）、`fontWeight`、`fontFamily`、`step`（2）。

CSS 安全网：容器上的 `max-width`、`overflow: visible`（**不是** `hidden`——hidden 会裁剪缩放的强调词和光晕效果）、`position: absolute`、显式 `height`。当逐词样式使用 `scale > 1.0` 时，计算 `maxWidth = safeWidth / maxScale` 以留出余量。

**容器模式：** 全宽绝对定位容器，居中。**不要**使用 `left: 50%; transform: translateX(-50%)`——会导致作品边缘裁剪。

## 字幕退出保证

每个组在退出动画后**必须**有一个硬性清除：

```js
tl.to(groupEl, { opacity: 0, scale: 0.95, duration: 0.12, ease: "power2.in" }, group.end - 0.12);
// `tl.set` 是即时翻转，不是动画——在此设置 `visibility` 是安全的（核心的「不动画 visibility」规则适用于动画，因为动画无法平滑插值非数值属性）。
tl.set(groupEl, { opacity: 0, visibility: "hidden" }, group.end);
```

构建时间线后进行自我检查——放在 `window.__timelines[id] = tl` **之前**，使其在作品初始化时运行：

```js
GROUPS.forEach(function (group, gi) {
  var el = document.getElementById("cg-" + gi);
  if (!el) return;
  tl.seek(group.end + 0.01);
  var computed = window.getComputedStyle(el);
  if (computed.opacity !== "0" && computed.visibility !== "hidden") {
    console.warn(
      "[caption-lint] 组 " + gi + " 在 t=" + (group.end + 0.01).toFixed(2) + "s 时仍可见",
    );
  }
});
tl.seek(0);
```

## 预构建的字幕组件

在从头构建字幕样式之前，先检查注册表——15 个即用型字幕组件涵盖了最常见的样式。使用 `npx hyperframes add <name>` 安装，并通过 `data-composition-src` 作为子作品接入（参见 `hyperframes-registry`）。

```bash
npx hyperframes catalog --tag caption-style   # 列出所有字幕组件
npx hyperframes add caption-highlight         # 安装特定的组件
```

| 风格 | 组件 | 最适合 |
| ------------------------- | ---------------------------- | ---------------------------- |
| TikTok 风格高亮 | `caption-highlight` | 社交、高能量 |
| 卡拉 OK 药丸 | `caption-pill-karaoke` | 音乐、歌词视频 |
| 电影编辑风 | `caption-editorial-emphasis` | 纪录片、叙事 |
| 故障/赛博 | `caption-glitch-rgb` | 科技、游戏 |
| 全屏猛击 | `caption-kinetic-slam` | 炒作、公告 |
| 霓虹光晕 | `caption-neon-glow` | 夜晚、俱乐部、霓虹美学 |
| 霓虹强调（多色） | `caption-neon-accent` | 多彩、俏皮 |
| 擦除揭示 | `caption-clip-wipe` | 简洁、现代 |
| 渐变填充 | `caption-gradient-fill` | 充满活力、引人注目 |
| 矩阵解码 | `caption-matrix-decode` | 科幻、科技揭示 |
| Emoji 弹出 | `caption-emoji-pop` | 社交、休闲 |
| 视差图层 | `caption-parallax-layers` | 深度、电影感 |
| 粒子爆发 | `caption-particle-burst` | 庆祝、冲击关键词 |
| 熔岩纹理 | `caption-texture` | 粗体、戏剧性 |
| 重量偏移 | `caption-weight-shift` | 优雅、字体艺术 |

相关：`caption-blend-difference`（标记为 `text` / `blend-mode`，不是 `caption-style`，因此不会出现在上面的过滤结果中）通过 `mix-blend-mode: difference` 自动使文本在任何背景上反转——当背景繁忙或不可预测时很有用。

浏览所有带预览的组件：[hyperframes.heygen.com/catalog](https://hyperframes.heygen.com/catalog)

字幕组件自带透明背景——它们是纯叠加层。如果底层视频很亮或很忙，在宿主作品中字幕子作品下方添加对比层（例如半透明深色 div），不要在组件内部添加。

## 进一步参考

- [`motion.md`](motion.md)——卡拉 OK、标记效果、音频响应调制、散射退出。
- [`transcript-handling.md`](transcript-handling.md)——输入格式、质量检查、清理、外部 API 备选。
- `hyperframes-animation/rules/css-marker-patterns.md`——标记高亮（确定性、完全可搜索）。

## 约束

- 确定性。没有 `Math.random()`，没有 `Date.now()`。
- 同步到转录时间戳。
- 一次只显示一个组。
- 每个组必须在 `group.end` 有硬性 `tl.set` 清除。
- 字体：编译器仅自动嵌入其**内置映射集**（Inter、Roboto、Montserrat……）——对于这些字体，只需在 CSS 中声明 `font-family`。任何**其他**字体（品牌/自定义字体如 `TT Norms Pro`，或非拉丁 CJK/梵文系列）都**不会**自动提供：它需要 `@font-face` 指向项目中实际存在的 `.woff2` 文件，否则文本会在渲染中静默回退到通用字体。不要假设你本地能看到的 `font-family` 就能渲染——渲染机器是一个干净的无头 Chrome，没有安装任何字体。
