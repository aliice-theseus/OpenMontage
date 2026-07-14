# HyperFrames 的 GSAP 特效

即用动画模式。每个特效自包含（HTML + CSS + JS）并遵循 HyperFrames 的 seek 驱动约定 — 确定性、无随机性、时间线在 `window.__timelines` 上注册。

## 索引

- [打字机](#打字机) — 逐字符文本揭示，可选光标/退格/单词旋转
- [音频可视化器](#音频可视化器) — 预提取音频数据，从时间线驱动 Canvas/DOM 渲染

---

## 打字机

使用 GSAP 的 TextPlugin 逐字符揭示文本。

### 所需插件

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/TextPlugin.min.js"></script>
<script>
  gsap.registerPlugin(TextPlugin);
</script>
```

### 基本打字机

```js
const text = "Hello, world!";
const cps = 10; // 每秒字符数：3-5 戏剧性，8-12 对话式，15-20 精力充沛
tl.to(
  "#typed-text",
  { text: { value: text }, duration: text.length / cps, ease: "none" },
  startTime,
);
```

### 带闪烁光标

三条规则：

1. **一次只有一个光标可见** — 在显示下一个之前隐藏前一个。
2. **光标空闲时必须闪烁** — 打字后，暂停期间。
3. **文本和光标之间无间隙** — 元素必须在 HTML 中紧贴。

```html
<span id="typed-text"></span><span id="cursor" class="cursor-blink">|</span>
```

```css
@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}
.cursor-blink {
  animation: blink 0.8s step-end infinite;
}
.cursor-solid {
  animation: none;
  opacity: 1;
}
.cursor-hide {
  animation: none;
  opacity: 0;
}
```

模式：闪烁 → 实心（打字开始）→ 打字 → 实心 → 闪烁（打字完成）。

```js
tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], startTime);
tl.to("#typed-text", { text: { value: text }, duration: dur, ease: "none" }, startTime);
tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], startTime + dur);
```

### 退格

TextPlugin 从前端移除 — 不符合退格需求。使用手动子字符串移除：

```js
function backspace(tl, selector, word, startTime, cps) {
  const el = document.querySelector(selector);
  const interval = 1 / cps;
  for (let i = word.length - 1; i >= 0; i--) {
    tl.call(
      () => {
        el.textContent = word.slice(0, i);
      },
      [],
      startTime + (word.length - i) * interval,
    );
  }
  return word.length * interval;
}
```

### 与静态文本的间距

当打字机单词与静态文本相邻时，在包裹 span 上使用 `margin-left`。不要使用 flex `gap`（它会使光标与文本产生间距），也不要在静态文本中放尾随空格（当动态 span 为空时它会塌缩）。

```html
<div style="display:flex; align-items:baseline;">
  <span style="font-size:40px; color:#555;">Ship something</span>
  <span style="margin-left:14px;"><span id="word"></span><span id="cursor">|</span></span>
</div>
```

### 单词旋转

打字 → 保持 → 退格 → 下一个单词。光标在每个空闲时刻（保持时、退格后）闪烁。

```js
let offset = 0;
words.forEach((word, i) => {
  const typeDur = word.length / 10;
  tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], offset);
  tl.to("#typed-text", { text: { value: word }, duration: typeDur, ease: "none" }, offset);
  tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], offset + typeDur);
  offset += typeDur + 1.5; // 保持

  if (i < words.length - 1) {
    tl.call(() => cursor.classList.replace("cursor-blink", "cursor-solid"), [], offset);
    const clearDur = backspace(tl, "#typed-text", word, offset, 20);
    tl.call(() => cursor.classList.replace("cursor-solid", "cursor-blink"), [], offset + clearDur);
    offset += clearDur + 0.3;
  }
});
```

### 追加单词

逐词构建句子到同一元素中：

```js
let accumulated = "";
let offset = 0;
words.forEach((word) => {
  const target = accumulated + (accumulated ? " " : "") + word;
  const newChars = target.length - accumulated.length;
  tl.to("#typed-text", { text: { value: target }, duration: newChars / 10, ease: "none" }, offset);
  accumulated = target;
  offset += newChars / 10 + 0.3;
});
```

### 多行光标交接

在打字机行之间交接：隐藏前一个 → 闪烁新 → 暂停 → 打字时实心。永远不要 `hidden → solid`（跳过空闲闪烁）。

```js
tl.call(
  () => {
    prevCursor.classList.replace("cursor-blink", "cursor-hide");
    nextCursor.classList.replace("cursor-hide", "cursor-blink");
  },
  [],
  handoffTime,
);

const typeStart = handoffTime + 0.5; // 短暂闪烁暂停
tl.call(() => nextCursor.classList.replace("cursor-blink", "cursor-solid"), [], typeStart);
tl.to("#next-text", { text: { value: text }, duration: dur, ease: "none" }, typeStart);
tl.call(() => nextCursor.classList.replace("cursor-solid", "cursor-blink"), [], typeStart + dur);
```

### 时间指南

| CPS  | 感受           | 适合                 |
| ---- | -------------- | -------------------- |
| 3-5  | 慢、慎重       | 戏剧性揭示、悬念     |
| 8-12 | 自然打字       | 对话、旁白           |
| 15-20| 快速、精力充沛 | 技术演示、代码       |
| 30+  | 近乎瞬时       | 填充长块             |

---

## 音频可视化器

预提取音频数据，从单个 `tl.call(...)` 每帧驱动 Canvas/DOM 渲染。**不要在渲染时使用 Web Audio API** — 定位期间没有播放。

### 提取音频数据

使用捆绑的提取器（需要 `ffmpeg` 和 Python `numpy`）：

```bash
python skills/hyperframes-creative/scripts/extract-audio-data.py audio.mp3 -o audio-data.json
python skills/hyperframes-creative/scripts/extract-audio-data.py video.mp4 --fps 30 --bands 16 -o audio-data.json
```

### 数据格式

```json
{
  "fps": 30,
  "totalFrames": 5415,
  "frames": [{ "time": 0.0, "rms": 0.42, "bands": [0.8, 0.6, 0.3] }]
}
```

- **`rms`** (0-1) — 整体响度，跨轨道归一化。
- **`bands[]`** (0-1) — 频率幅度。索引 0 = 低音，较高索引 = 高音。每个频带独立归一化。

### 加载数据（同步）

```js
// 选项 A — 内联（小文件，约 500 KB 以下）
var AUDIO_DATA = {
  /* 粘贴 audio-data.json 内容 */
};

// 选项 B — 同步 XHR（大文件；必须是同步的以实现确定性时间线构建）
var xhr = new XMLHttpRequest();
xhr.open("GET", "audio-data.json", false);
xhr.send();
var AUDIO_DATA = JSON.parse(xhr.responseText);
```

**不要使用异步 `fetch()`。** HyperFrames 在页面加载后同步读取 `window.__timelines` — 在 `.then()` 内构建时间线意味着捕获开始时时间线尚未就绪。

### 驱动时间线

**Canvas 2D** — 最常见（条、波形、圆形、渐变）：

```js
const canvas = document.getElementById("viz");
const ctx = canvas.getContext("2d");

for (let f = 0; f < AUDIO_DATA.totalFrames; f++) {
  tl.call(
    () => {
      const frame = AUDIO_DATA.frames[f];
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // 使用 frame.rms 和 frame.bands 绘制
    },
    [],
    f / AUDIO_DATA.fps,
  );
}
```

**WebGL / Three.js** — HyperFrames 补丁了 `THREE.Clock` 以实现确定性时间。每帧从音频数据更新 uniforms。

**DOM 元素** — 少于 ~20 个元素可以，多于则比 Canvas 慢。

### 平滑

```js
let prev = null;
const smoothing = 0.25; // 0.1-0.2 干脆，0.3-0.5 流畅
function smooth(f) {
  const raw = AUDIO_DATA.frames[f];
  if (!prev) {
    prev = { rms: raw.rms, bands: [...raw.bands] };
    return prev;
  }
  prev = {
    rms: prev.rms * smoothing + raw.rms * (1 - smoothing),
    bands: raw.bands.map((b, i) => prev.bands[i] * smoothing + b * (1 - smoothing)),
  };
  return prev;
}
```

### 空间映射

- **水平**：低音左，高音右（从左到右迭代频带）
- **垂直**：低音底部，高音顶部
- **圆形**：低音在 12 点钟方向，顺时针包裹；镜像用于完整圆形

### 运动原则

- **低音驱动大动作** — 缩放、辉光、位置偏移。
- **高音驱动细节** — 闪烁、微光、边缘效果。
- **RMS 驱动全局** — 背景亮度、整体能量。
- 选择 2-3 个属性进行动画化。更多看起来嘈杂。
- 保持最小值高于零 — 安静部分仍需要生命力。

### 频带数

| 频带 | 细节   | 适合                     |
| ---- | ------ | ------------------------ |
| 4    | 低     | 背景辉光、脉冲           |
| 8    | 中     | 条形图、基本频谱         |
| 16   | 高     | 详细 EQ（默认）          |
| 32   | 非常高 | 密集径向布局              |

### 分层

使用 CSS `z-index` 叠加多个 canvas 以实现深度 — 由低音/RMS 驱动的背景层和由单独频带驱动的前景层创造深度，无需逐元素复杂度。

```html
<canvas id="bg-layer" style="position:absolute;top:0;left:0;z-index:1;"></canvas>
<canvas id="main-layer" style="position:absolute;top:0;left:0;z-index:2;"></canvas>
```
