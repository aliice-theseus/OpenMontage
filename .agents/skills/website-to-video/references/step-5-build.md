# 步骤 5：构建作品

**字幕规则——在构建任何内容之前阅读：** 永远不要创建带有空转录（`const script = []`）的 `compositions/captions.html`。如果配音/转录步骤被跳过或失败，完全不要创建字幕作品。空的字幕文件静默什么都不做，浪费一个轨道槽。只有当 `transcript.json` 有真实的词语时间戳时才创建。

**字幕堆叠错误：** 每个字幕词组的 `opacity` 必须从 `0` 开始（或 `visibility: hidden`），并定位为 `position: absolute`。一次只能显示一个组——GSAP 顺序控制可见性。如果多个组同时可见，意味着(a) 初始 CSS 状态未隐藏，或(b) 在下一个组入场触发之前缺少退出动画。在构建 captions.html 后，在旁白中间拍摄 3–4 个时间戳的快照，并验证每帧只有一个词组可见。

**在构建之前，确认你拥有：**

- **STORYBOARD.md**——逐节拍计划。如果你不记得每个节拍的概念、资源和技巧，立即重新阅读。
- **DESIGN.md**——如果你需要检查记不住的具体值（颜色、字体、组件样式），查找。不要重新读取整个文件。
- **`capture/extracted/asset-descriptions.md`**——当故事板将资源分配给节拍时，检查描述以了解它展示的内容。如果你记不清资源清单，重新阅读此文件。
- **transcript.json**——驱动场景时长的词语级时间戳。

加载 `hyperframes` 技能——它有关于数据属性、时间线约定、确定性渲染和布局的规则。如果你在此会话中尚未阅读，立即阅读。

**关于 capabilities.md 和 techniques.md：** 阅读目录以了解方向，然后只深入故事板实际需要的章节。你不需要重新阅读你的节拍中未使用的动画引擎、注册表块或技巧的章节。

---

## 1. 将 SFX 复制到项目

```bash
cp -r skills/website-to-video/assets/sfx/ <project-dir>/sfx/
# 如果技能安装在其他位置：
find . -path "*/website-to-video/assets/sfx" -exec cp -r {} <project-dir>/sfx/ \;
```

## 2. 构建根 index.html

自己创建 `index.html`。这是编排器——它持有节拍槽、旁白音频、SFX 和着色器过渡（如果有）。

**关键 CSS——每个节拍必须在同一帧中重叠：**

```css
.scene {
  position: absolute;
  top: 0;
  left: 0;
  width: 1920px;
  height: 1080px;
  overflow: hidden;
}
```

**节拍结构：**

```html
<div
  id="root"
  data-composition-id="main"
  data-start="0"
  data-duration="TOTAL"
  data-width="1920"
  data-height="1080"
>
  <div
    id="beat-1"
    class="scene"
    data-composition-id="beat-1-hook"
    data-composition-src="compositions/beat-1-hook.html"
    data-start="0"
    data-duration="5.5"
    data-track-index="1"
    data-width="1920"
    data-height="1080"
  ></div>

  <!-- 更多节拍... -->

  <audio
    id="narration"
    src="narration.wav"
    data-start="0"
    data-duration="NARRATION_LENGTH"
    data-track-index="0"
    data-volume="1"
  ></audio>

  <!-- 内容时刻上的 SFX，而不是着色器过渡上 -->
  <audio
    id="sfx-impact"
    src="sfx/impact-bass-1.mp3"
    data-start="0.3"
    data-duration="2.1"
    data-track-index="41"
    data-volume="0.35"
  ></audio>
</div>
```

SFX 在故事板（步骤 3）中已分配——精确实现 STORYBOARD.md 指定的内容。每个 SFX 条目都有一个文件、触发时间和音量。将每个作为 `<audio>` 元素连接，使用故事板中精确的 `data-start`、`data-duration` 和 `data-volume`。不要添加、删除或替换超出故事板所说的 SFX。

**根据节奏选择架构（来自步骤 3）**

| 节奏 | 架构 | 原因 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| **快**（广告牌式节拍） | 单个 `index.html`，堆叠的 `<div class="beat">` 元素，GSAP 不透明度排序。无子作品，无 HyperShader。通过 `tl.set()` 硬切。参见下面的堆叠节拍模式。 | 子作品增加延迟；硬切需要即时交换。一个文件 = 零加载延迟。 |
| **中等 / 慢 / 弧** | 带 `HyperShader.init()` 的子作品。每个节拍在 `compositions/beat-N.html` 中。场景之间的 CSS 交叉淡入淡出或着色器过渡。 | 过渡需要 HyperShader 的合成。子代理独立构建每个节拍。 |

如果故事板说「快」节奏：使用下面的堆叠节拍模式。不要使用 HyperShader——它增加了场景注册开销，在硬切之间产生间隙。每一帧都是内容，没有过渡帧。

**堆叠节拍模式（快节奏）：**

每个节拍使用故事板要求的任何原语组合——HTML/CSS、SVG、捕获资源、WebGL、Canvas、Three.js、动态排版、Lottie——单独或组合。狭义的禁止：永远不要将全出血产品 UI 截图作为承重内容。每个节拍的结构来自故事板的组合 + 强调规格。

```html
<div
  data-composition-id="video"
  data-width="1920"
  data-height="1080"
  data-start="0"
  data-duration="TOTAL"
  style="position:relative;width:1920px;height:1080px;"
>
  <!-- 节拍 1：动态排版钩子（从逐词跨度组合） -->
  <div class="beat" id="b01" style="opacity:1;">
    <div class="mega">
      <span class="w">停止</span>
      <span class="w">上下文切换。</span>
    </div>
  </div>

  <!-- 节拍 2：组合看板——3 列卡片即 div，不是截图 -->
  <div class="beat" id="b02">
    <div class="kanban">
      <div class="col">
        <div class="card">分类工单</div>
        <div class="card">审查 PR</div>
      </div>
      <div class="col">
        <div class="card active">设计规范</div>
      </div>
      <div class="col">
        <div class="card">发布 v2.1</div>
      </div>
    </div>
  </div>

  <!-- 节拍 3：SVG Logo 绘制——组合，不是 <img> -->
  <div class="beat" id="b03">
    <svg viewBox="0 0 200 200"><path class="mark" d="..." /></svg>
  </div>
  <!-- 更多节拍——每个是一个组合场景，有自己的视觉世界 -->
</div>
```

如果你发现自己写 `<img src="capture/assets/...">` 作为节拍的主要视觉，而资源是产品 UI 截图，停止。那就是此技能存在的目的是打破的幻灯片模式。使用 DESIGN.md 中的品牌颜色从 div 和 CSS 构建元素。合法的 `<img>` 用途是：(a) 当是纯光栅的品牌 Logo，(b) 作为组合内容后面环境深度的英雄插画，(c) 作为背景洗色的渐变/纹理图像。永远不要将产品 UI 截图作为承重视觉。

```css
.beat {
  position: absolute;
  inset: 0;
  width: 1920px;
  height: 1080px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  overflow: hidden;
}
```

```javascript
var beats = [
  { id: "b01", at: 0, dur: 1.8 },
  { id: "b02", at: 1.8, dur: 1.0 },
  // ...
];
beats.forEach(function (b) {
  var el = document.getElementById(b.id);
  if (b.id !== "b01") tl.set(el, { opacity: 1 }, b.at);
  gsap.set(el, { scale: 1.012 });
  tl.to(el, { scale: 1, duration: 0.25, ease: "power2.out" }, b.at);
  if (b !== beats[beats.length - 1]) tl.set(el, { opacity: 0 }, b.at + b.dur);
});
```

每个节拍获得自己的视觉世界——不同的背景、不同的颜色、不同的能量。没有两个连续的节拍看起来应该相似。每个节拍入口的缩放脉冲（1.012→1.0）微妙但可感知。

如果故事板说「慢」或「电影感」：将每个节拍构建为子作品。使用长交叉淡入淡出（0.8–1.2s 的 `duration`，无 `shader` 键 = CSS 交叉淡入淡出）。在每个节拍内部，使用持续的微妙运动——没有什么是静态的：

- 组合场景根上的慢相机漂移：`tl.fromTo(scene, {scale:1.05, x:20}, {scale:1, x:-20, duration: BEAT, ease:"none"})`（Ken-Burns 风格，但在你的组合元素上——不在截图上）
- 视差文本层：`tl.fromTo(text, {y:30}, {y:-30, duration: BEAT, ease:"power1.inOut"})`
- 文本进入前 1–2s 的呼吸空间（不要在 t=0 动画化所有内容）
- 柔和缓动：`expo.out` 用于入口，`power1.inOut` 用于漂移

**带 HyperShader 的多场景 index.html——用于中等/慢/弧节奏**

对于带子作品节拍和场景过渡的视频，`index.html` **必须**使用 `HyperShader.init()`。这是整个场景编排层。不要尝试使用注册表块子作品（例如 `compositions/domain-warp-dissolve.html`）进行过渡——那些是独立展示演示，不是 HyperShader 在多场景作品中的工作方式。

首先复制本地着色器构建：

```bash
cp packages/shader-transitions/dist/index.global.js <project-dir>/hyper-shader-local.js
```

完整工作 `index.html` 模式——每个字段都重要：

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="hyper-shader-local.js"></script>

<div id="root" data-composition-id="main" data-start="0" data-duration="TOTAL"
     data-width="1920" data-height="1080">

  <!-- 宿主 div：必须同时具有 id 和 data-composition-id 匹配相同的值。
       HyperShader.init() 使用 getElementById()——如果没有 id="beat-1"，
       它会失败并显示「场景 ID 在 DOM 中未找到」。 -->
  <div id="beat-1" class="scene"
    data-composition-id="beat-1-hook"
    data-composition-src="compositions/beat-1-hook.html"
    data-start="0"        <!-- 进入此节拍的过渡从此开始 -->
    data-duration="4.5"   <!-- 必须与作品中 GSAP BEAT 常量匹配 -->
    data-track-index="1"
    data-width="1920" data-height="1080"
    style="background: #YOUR_BEAT_BG_COLOR;"><!-- 在此或在子作品 CSS 中设置背景——两者均可 -->
  </div>

  <div id="beat-2" class="scene"
    data-composition-id="beat-2-features"
    data-composition-src="compositions/beat-2-features.html"
    data-start="4.0"
    data-duration="5.5"
    data-track-index="2"  <!-- 使用顺序轨道索引（1,2,3...）以避免检查器错误 -->
    data-width="1920" data-height="1080"
    style="background: #YOUR_BEAT_BG_COLOR;">
  </div>

  <!-- ... 更多节拍 ... -->

  <!-- 始终添加一个虚拟的 s-end 场景作为最后一个条目。
       HyperShader 在某些上下文中将 scenes[N-1] 渲染为黑色。
       s-end 是不可见的——它只是防止你的 CTA 成为最后一个。 -->
  <div id="s-end" class="scene"
    data-composition-id="s-end"
    data-start="TOTAL_MINUS_0.1"
    data-duration="0.1"
    data-track-index="N"
    data-width="1920" data-height="1080">
  </div>

</div>

<script>
  window.__timelines = window.__timelines || {};
  var tl = HyperShader.init({
    bgColor: "#000000",
    accentColor: "#YOUR_ACCENT",
    scenes: ["beat-1", "beat-2", "beat-3", ..., "s-end"],
    transitions: [
      { time: 4.0, shader: "sdf-iris", duration: 0.7 },    // WebGL 着色器
      { time: 9.5, duration: 0.5 },                         // CSS 交叉淡入淡出（无着色器）
      // ... 每个场景边界一个过渡 ...
      { time: TOTAL_MINUS_0.1, duration: 0.1 }              // 虚拟 → s-end
    ],
  });
  // 在 init() 后将所有节拍动画添加到返回的 tl
  window.__timelines["main"] = tl;
</script>
```

**轨道索引和检查器：** 为每个节拍使用顺序的轨道索引（`data-track-index="1"`、`"2"`、`"3"`...）——不是都在轨道 `"1"` 上。检查器将同一轨道上的重叠片段标记为错误，而 HyperShader 作品总是有重叠的节拍（过渡窗口）。使用顺序索引可以静默检查器；HyperShader 通过不透明度管理哪个场景是**可见的**，无论轨道索引如何。

**场景背景颜色：** 在 index.html 中的宿主 `<div id="beat-1">` 上设置 `style="background: #3139FB"` 是最简单的模式——从根文件中一眼可见。在子作品的 CSS 内部设置背景也可以。两者都可以；宿主 div 是首选，以保持清晰。

**关键：节拍宿主 div 必须有顺序的 `data-start` 和匹配的 `data-duration`。** 不要在所有节拍上设置 `data-start="0"`——渲染引擎将每个节拍的 GSAP 时间线定位到 `global_time - data_start`。在 t=10s 时使用 `data-start=0`，一个 5.5s 的时间线会被定位到其末尾之后，所有内容消失。

`data-duration` 必须与作品中的 GSAP `BEAT` 常量（子作品内部时间线的长度）匹配。如果两者不一致，动画会被截断。

**故事板节拍时序部分**告诉你两个值——直接使用：

- `data-start` = 故事板中的「过渡进入在：」值
- `data-duration` = 故事板中的「GSAP 时长：」值

**字体处理：** 常见字体由渲染器自动解析：使用 `"Inter"`（而不是 `"Inter Variable"`——编译器只映射基础名称）、`"Roboto"`、`"JetBrains Mono"`、`"Poppins"`。如果作品使用 `"Inter Variable"`，它会记录编译器警告并可能错误回退——始终使用 `"Inter"`。只有品牌特定的字体（GT Walsheim、Aeonik 等）才需要 `@font-face`。检查 `capture/assets/fonts/`——哈希文件名是自动解析的 Google Fonts 子集；可识别的文件名（例如 `BrandSans-Bold.woff2`）是需要 `@font-face` 声明的品牌字体。

**品牌字体 @font-face：** 如果故事板的品牌值列出了品牌特定字体及 `capture/assets/fonts/` 中的路径，在使用该字体的每个作品顶部添加 `@font-face` 块——除非你显式告诉子代理，否则他们不会这样做。在子代理提示的品牌值部分中粘贴确切的 `@font-face` 声明。没有这个，每个作品都会回退到 `system-ui`，品牌字体永远不会加载。

**⚠ 资源路径——最常见的子代理错误（每次运行 5+ 个代理）：** 当作品引用捕获的强调资源（Logo、渐变层、英雄插画）时，路径必须相对于**项目根目录**，而不是作品文件。`compositions/beat-N.html` 深一层目录，但路径必须写为从根目录出发。

- ✅ `capture/assets/logo.svg`
- ❌ `../capture/assets/logo.svg`

Studio 预览服务器将基础 URL 重写为项目根目录——在本地似乎可以工作的 `../` 路径在预览和渲染中会返回 404。将此逐字添加到每个子代理提示的规则部分。

## 3. 构建每个作品——使用子代理

**在分派之前，重新阅读 DESIGN.md 和 STORYBOARD.md。** 你在会话早期编写了这些文件，你以为你记得它们。你不记得——不是精确的十六进制值、不是特定的字体家族、不是按钮的圆角、不是做/不做。立即重新阅读它们，以便将准确的品牌规则和节拍规格粘贴到每个子代理提示中。

**如果你的运行时支持并行子代理**（Claude Code、Cursor、大多数代理框架）：每个节拍分派一个子代理——比顺序构建快 3 到 4 倍。对于 3+ 个节拍，始终并行了发。对于 1-2 个节拍，顺序就足够了。

**如果你的运行时不支持并行子代理**（某些 Codex 设置、仅顺序模型）：使用下面相同的上下文打包模板顺序构建。该模板给每个构建过程与子代理相同的上下文——粘贴前/本/后节拍 + 品牌值——因此输出质量相同，只是更慢。

无论哪种情况，使用模板。不要跳过它凭记忆构建。

每个子代理阅读 [beat-builder-guide.md](beat-builder-guide.md)——它包含所有内容：规则、缓动、文件参考、验证命令。**不要尝试将所有规则自己粘贴到提示中。** 而是告诉子代理阅读指南文件。你只粘贴节拍特定的上下文：故事板章节、品牌值和资源路径。

```
为节拍 N 构建作品。保存到 compositions/beat-N-name.html。

首先：定位并阅读节拍构建器指南。你的 CWD 是项目目录，因此
技能在其外部——运行此命令找到它：

  find "$HOME" -path '*/website-to-video/references/beat-builder-guide.md' -maxdepth 10 2>/dev/null | head -1

从头到尾阅读该文件。它有你的完整工作流、所有规则、缓动词汇
和文件参考。严格遵循它的工作流：
  build → lint（`npx hyperframes lint .`）
        → snapshot（`npx hyperframes snapshot . --frames 3`）
        → 查看联系表并阅读 snapshots/descriptions.md
        → 修复问题

完成后，主代理将自上而下阅读你的作品 HTML，
并对照 DESIGN.md 和 STORYBOARD.md 进行交叉检查——品牌背景/强调
十六进制是否实际出现在你的 CSS 中、故事板要求捕获的资源
是否实际被引用、标题是否 ≥80px、GSAP 时间线是否覆盖
完整的节拍时长。诚实地完成工作。没有完成工作而报告「看起来不错」
会在主代理打开文件时被发现。

═══ 前一个节拍（节拍 N-1）═══
[粘贴 STORYBOARD.md 中的完整前一个节拍部分]

═══ 此节拍（节拍 N）═══
[粘贴 STORYBOARD.md 中的完整节拍部分——这是构建规格]

═══ 下一个节拍（节拍 N+1）═══
[粘贴 STORYBOARD.md 中的完整下一个节拍部分]

═══ 品牌值（来自 DESIGN.md）═══
颜色：
  --bg：       #[hex]   主背景
  --fg：       #[hex]   主文本
  --accent：   #[hex]   CTA/高亮
  --surface：  #[hex]   卡片/面板背景
  [如果需要，添加更多]

字体：
  标题：[字体家族]、[权重]
  正文：[字体家族]、[权重]
  [如果需要，品牌字体路径：capture/assets/fonts/Brand.woff2]

关键组件样式：
  [粘贴 DESIGN.md 中的相关行]

═══ 此节拍的捕获资源 ═══
[粘贴 asset-descriptions.md 中的实际文件路径 + 描述：

- capture/assets/hero-dashboard.png — 全出血产品仪表板，暗色主题
- capture/assets/logo.svg — 品牌字标，透明底白色

不要说「见 asset-descriptions.md」。在此处粘贴路径。]
```

故事板节拍已经包含一切——概念、精确时序的视觉编排、CSS 值、SFX 提示。子代理的工作是将该描述转换为工作 HTML/CSS/GSAP，而不是重新发明创意方向。如果你愿意，也可以向子代理粘贴你认为好的其他相关和有用的上下文，为什么不呢。

### 每个作品的流程

对于每个节拍：

**1. 阅读故事板节拍。** 故事板就是构建规格。它告诉你存在什么元素、它们如何进入、在节拍期间做什么以及如何退出。遵循它。如果故事板中的某些内容不清楚或似乎不可能，研究如何做或询问——不要默默跳过。

**2. 首先构建静态结束状态。** 将每个元素定位在其最可见的时刻。仅 HTML+CSS，尚无 GSAP。CSS 位置是地面实况。

**3. 添加动画序列。** 遵循故事板的编排——它指定了什么发生以及何时发生。对于入口使用 `tl.fromTo()`（而不是 `tl.from()`）。按故事板描述的顺序构建时间线。

**4. 添加退出**（如果是 CSS 过渡退出）。如果是着色器过渡——无需退出动画。

**5. 查看结果。** 构建后，在不同时间戳（应该发生事情、动画、移动等等的地方）拍摄此节拍的快照，并从所有角度、角落和位置查看它。画面是否充满，一切是否精确在其应该的位置？你确定吗？元素可读吗？它与故事板描述的内容匹配吗？

### 技术规则

- **没有 `repeat: -1`**——从节拍时长计算精确重复次数
- **没有 `Math.random()`**——使用种子 PRNG
- **没有裸 `gsap.to()`**——所有动画在 `tl` 上，从不独立
- **没有全屏暗色线性渐变**——H.264 条带
- **最小字体**：80px+ 标题，20px+ 正文
- **渐变背景上的 WCAG 对比度：** 对比度验证器会采样文本元素下的实际背景像素——如果背景是渐变图像，图像的暗色部分会使测量比率在文本颜色变暗时_更差_，而不是更好。修复：要么将文本放在纯色区域上，要么向不需要 WCAG 合规性的装饰性标签添加 `data-layout-ignore` 属性。当背景不是纯色时，不要盲目地使文本颜色变暗。

## 4. 所有作品构建后——对账检查

在进入步骤 6 之前，运行此完整性检查：

```bash
# 列出 compositions/ 中的每个文件，验证每个在 index.html 中都有宿主 div
ls compositions/
```

对于 `compositions/` 中的每个 `.html` 文件，确认 `index.html` 有一个指向它的 `data-composition-src="compositions/<filename>"`。如果有任何作品文件未在 `index.html` 中引用，立即添加缺失的宿主 div——未引用的作品在运行时完全不可见。

**字幕存根规则：** 永远不要创建带有空转录（`const script = [];`）的 `compositions/captions.html`。如果配音/转录步骤被跳过或失败，完全不要创建字幕作品。一个立即返回的空字幕文件比没有字幕文件更糟——它静默什么都不做，浪费一个轨道槽。

### 并行子代理快照是过时的——在所有完成后重新快照

当你并行分派子代理（每个节拍一个）时，每个子代理快照的项目中兄弟节拍可能尚不存在。它们在隔离状态下对每个节拍的快照对其自身的节拍是有效的，但**任何在节拍边界或着色器过渡期间的快照都会显示错误的内容**——通常是前一个节拍的内容，因为下一个节拍尚未构建。

示例：节拍 6 的子代理在 t=25.7s 拍摄快照，看到了节拍 1 的内容，因为当节拍 6 的子代理运行时节拍 5 尚不存在。子代理将此报告为「显示前一场景的着色器过渡行为」——听起来合理但错误的诊断。

**在所有子代理完成后必需：**

```bash
node /<repo-root>/packages/cli/dist/cli.js snapshot <project-dir> --frames <N>
```

其中 N 遵循快照公式：`max(节拍数 × 3, ceil(时长_秒 / 2))`。这是步骤 6 的 DoD 使用的规范快照——不是任何单个子代理的中间快照。

子代理的快照仍然有用，作为每个节拍的完整性检查，但它们不是交付物。完成后重新快照才是。不要因为「子代理已经快照了」就跳过它。

## 5. 自上而下阅读每个节拍 HTML——步骤 6 之前的必需关卡

**此关卡不可跳过。**「我读了它，看起来很好」、「子代理已确认」、「快照看起来正确」都是不可接受的。快照是运动中 300+ 帧中的 3 帧——它们隐藏了它们之间发生的所有问题。

**为什么存在此关卡：** 早期的会话中，子代理回复「看起来不错，0 错误」，主代理信任了他们——这就是视频如何带着不匹配的颜色、缺失的 Logo、小到无法阅读的标题以及晚了 1 秒触发的 SFX 交付的，因为代理「凭眼力」输入了时间戳而不是计算它们。

对于每个 `compositions/beat-N.html`：

1. **打开文件并自上而下阅读。** 不是一瞥。不是 grep。阅读 `<style>` 块，然后标记，然后 `<script>` 块。
2. **用来自文件的引用值填写此证据块——每一行：**

```
节拍 N：compositions/beat-N-NAME.html
  CSS 中的背景颜色：     <来自第 Y 行的十六进制>      ← 引用确切的代码行
  CSS 中的强调色：     <来自第 Z 行的十六进制>      ← 引用确切的代码行
 标题字体大小：     <来自某行的 px>         （≥80？是/否）
 标题字体家族：   <来自某行的堆栈>      （匹配 DESIGN.md？是/否）
 @font-face src 路径：   <列表>                 （每个路径存在？是/否）
 使用的捕获资源：   <来自 <img src=>、内联 SVG id、background-image url() 的完整路径列表>
 故事板要求：  <来自 STORYBOARD.md 节拍 N 的列表>
 资源匹配故事板？是/否 — 如果否，指定差距
 GSAP 第一个事件：       tl.X("...", {...}, <t>)   节拍本地 t=<num>
 GSAP 最后一个事件：        tl.X("...", {...}, <t>)   节拍本地 t=<num>
 节拍时长：          <N>s                   （事件覆盖完整时长？是/否）
 SFX 触发：            <元素> data-start=<num>
 故事板 SFX 行：    "引用该行" → 预期 t=<num>
 SFX 时间戳匹配？ 是/否 — 如果否，指定漂移
 技术关卡：        data-composition-id 匹配 window.__timelines 键？是/否
                           script 在 <template> 内部？是/否
                           没有 Math.random / 没有 repeat:-1 / 没有裸 gsap.to？是/否
 判定：通过 / 修复（精确指定什么）
```

如果你无法填写任何行（例如，「我没有看到 SFX 触发」或「标题字体家族未指定」），那本身就是发现——修复或上报，不要掩盖。

3. **打开 `snapshots/beat-N/` 中的每个帧**并目视确认进场/保持/退出与故事板匹配。

**任何不正确的地方——内联修复（小的 CSS/GSAP 修正）或用引用的具体问题重新分派子代理。** 不要进入步骤 6，直到每个节拍都有其证据块已填写并通过。

### SFX 时间戳计算——计算，不要目测

每个 SFX `data-start` 值必须从 STORYBOARD.md 计算，而不是目测估计。

对于每个 SFX 条目：

1. 故事板命名节拍本地时间（例如「节拍 2 在节拍内 1.2s 处」）。
2. 从节拍排序获取节拍的全局开始时间（例如节拍 1：0–3.5s → 节拍 2 全局从 3.5s 开始）。
3. 节拍本地 + 全局开始相加：`3.5 + 1.2 = 4.7s`。
4. 在 index.html 中写入 `data-start="4.7"`。

**禁止：** 通过阅读故事板并目测估计来写入 `data-start="<大约的视觉时刻>"`。上面的证据块**必须**引用故事板 SFX 行和 index.html `data-start` 行——并确认它们在 ±0.1s 内匹配（约 3 帧在 30fps；与 `w2h-verify.mjs` 执行的和 `step-6-validate.md` 用于播放验证的相同容差）。1 秒的漂移不是四舍五入误差；是构建失败。

### 向用户呈现重复出现的子代理变通方案

当 2+ 个子代理独立报告相同的变通方案时（例如，「我必须对数据 URI 进行 base64 编码，因为检查器对内联 SVG 有误报」），那是值得呈现的工具 bug。在步骤 5 最终报告中将这些列出在「遇到的工具问题」下，即使每个实例已解决。格式：

```
工具问题（值得归档）：
- 3 个子代理（节拍 1、4、6）在 CSS 内联 SVG 数据 URI 上遇到了 `root_missing_composition_id` 误报。
  变通方案：base64（节拍 1）、移除叠加（节拍 4、6）。
  值得作为回归问题归档到 packages/core/src/lint。
```

埋没重复出现的变通方案意味着下一个会话会遇到相同的 bug 并再次变通。不要这样。

### 品牌默认检查（全视频，在每个节拍通过自身阅读后）

这些是大多数品牌视频的默认设置，不是硬性要求：

- 第一个节拍引用来自 `capture/assets/svgs/` 的品牌 Logo/字标 SVG
- 最后一个节拍引用品牌 Logo/字标
- 网站的签名视觉（英雄插画、渐变波浪、独特的 UI 标记）至少出现一次

如果有任何缺失，检查故事板——如果 STORYBOARD.md 有目的地延迟品牌揭示或出于概念原因省略签名视觉，那没问题。如果遗漏是无意的，修复它（或在添加前询问主代理/用户）。

一旦每个节拍阅读干净，进入步骤 6（验证与交付）进行 lint、validate、快照和视觉审核。
