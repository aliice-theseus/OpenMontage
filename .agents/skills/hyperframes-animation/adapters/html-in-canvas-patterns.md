# HTML-in-Canvas 模式

HyperFrames 最强大的视觉能力。将**任何**实时 HTML/CSS 捕获为 GPU 纹理，然后通过 WebGL 着色器、Three.js 3D 场景或后处理特效进行渲染——以 60fps、像素完美、支持所有 CSS 特性的方式呈现。

**当一个节拍值得超越平面 GSAP 动画的电影级处理时，请阅读此文件。** 每个视频仅用于 1-3 个主角色的节拍，而非所有节拍。其余部分可以使用标准 GSAP——平面节拍与 HTML-in-Canvas 节拍之间的对比本身就是视觉叙事的一部分。

---

## 核心模板（每个 HTML-in-Canvas 组合中相同）

每个 HTML-in-Canvas 特效共享此结构。学习一次，适用于任何特效。

```html
<!-- 1. 源 HTML —— 你的内容放在 layoutsubtree canvas 内部 -->
<canvas
  id="hic-source"
  layoutsubtree
  width="1920"
  height="1080"
  style="position:absolute;inset:0;opacity:0;"
>
  <div id="hic-content" style="width:1920px;height:1080px;">
    <!-- 你的 HTML 内容在这里 —— 文本、图像、卡片、仪表板等 -->
  </div>
</canvas>

<!-- 2. 渲染目标 —— 显示特效的可见 canvas -->
<canvas id="hic-output" width="1920" height="1080" style="position:absolute;inset:0;"></canvas>
```

```js
// 3. 特性检测 —— 始终检查，始终提供回退
function isHiCSupported() {
  var tc = document.createElement("canvas");
  if (!("layoutSubtree" in tc)) return false;
  tc.setAttribute("layoutsubtree", "");
  var ctx = tc.getContext("2d");
  return ctx && typeof ctx.drawElementImage === "function";
}
var apiOk = isHiCSupported();

// 4. 捕获函数 —— 在 onUpdate 中每一帧调用
var capCanvas = document.getElementById("hic-source");
var capCtx = capCanvas.getContext("2d");
function captureContent() {
  if (apiOk) {
    capCtx.drawElementImage(document.getElementById("hic-content"), 0, 0, 1920, 1080);
  }
}

// 5. 从 GSAP 时间线驱动 —— 每帧捕获 + 渲染
tl.to(
  proxy,
  {
    /* 你的动画属性 */
    duration: BEAT_DURATION,
    ease: "sine.inOut",
    onUpdate: function () {
      captureContent();
      // 在这里渲染你的特效（Three.js 或 WebGL2）
    },
  },
  0,
);
```

**回退方案：** 当 `drawElementImage` 不可用时（无 Chrome 标志的预览），绘制纯色占位符或使用 Canvas 2D 文本。HyperFrames 渲染器会自动启用该标志——特效**会**在最终视频中生效。参见液态玻璃块以获取完整的回退示例。

---

## 特效目录

### 1. 带辉光的 3D 旋转（Three.js）

**效果描述：** 内容悬浮在 3D 空间中，缓慢旋转，明亮边缘带有电影级辉光。如同在黑暗影院中展示产品截图。

**使用时机：** 主角产品展示、功能揭示、高级感 CTA。

**关键 Three.js 组件：** `PlaneGeometry` + `CanvasTexture` + `EffectComposer` + `UnrealBloomPass`

```js
// 在上述模板之后，添加：
var scene3d = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(45, 1920 / 1080, 0.1, 100);
camera.position.set(0, 0, 4);

var renderer = new THREE.WebGLRenderer({
  canvas: document.getElementById("hic-output"),
  antialias: true,
  alpha: true,
});
renderer.setSize(1920, 1080);

var texture = new THREE.CanvasTexture(capCanvas);
var mesh = new THREE.Mesh(
  new THREE.PlaneGeometry(3.6, 2.2),
  new THREE.MeshBasicMaterial({ map: texture }),
);
scene3d.add(mesh);

// 后处理：辉光实现电影效果。
// EffectComposer / RenderPass / UnrealBloomPass 是 ES 模块命名导入
// （参见下面的导入块）——在 modern 版本中它们不是 THREE 的属性。
// Three.js r150+ 移除了 UMD `examples/js/` 全局变量。
var composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene3d, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(1920, 1080), 0.3, 0.4, 0.85));

var proxy = { rotY: -0.12, zoom: 4.2 };
tl.to(
  proxy,
  {
    rotY: 0.12,
    zoom: 3.6,
    duration: BEAT_DURATION,
    ease: "sine.inOut",
    onUpdate: function () {
      captureContent();
      texture.needsUpdate = true;
      mesh.rotation.y = proxy.rotY;
      camera.position.z = proxy.zoom;
      composer.render();
    },
  },
  0,
);
```

**通过 ESM 加载 Three.js 和后处理（使用 `type="module"` 脚本）：**

```html
<script type="module">
  import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";
  import { EffectComposer } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/EffectComposer.js";
  import { RenderPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/RenderPass.js";
  import { ShaderPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/ShaderPass.js";
  import { UnrealBloomPass } from "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/postprocessing/UnrealBloomPass.js";
  // ... 使用这些导入的其余组合代码
</script>
```

Three.js r152 中移除了 `examples/js/` 路径。使用 `three@0.181.2` 配合 `examples/jsm/`（ES 模块）——这是 HyperFrames Three.js 适配器使用的版本。

---

### 2. 磁性光标扭曲（原生 WebGL2）

**效果描述：** 内容向一个移动点弯曲和变形，如同磁铁吸引像素。色差在扭曲部位分裂 RGB 通道。

**使用时机：** 交互感、带光标的產品演示、"看这个功能"的瞬间。

**关键技术：** 带有高斯扭曲 + 色差分裂的自定义片段着色器。无需 Three.js——只需原生 WebGL2。

```js
// WebGL2 设置
var gl = document.getElementById("hic-output").getContext("webgl2", {
  alpha: false,
  preserveDrawingBuffer: true,
});

// 顶点着色器 —— 全屏四边形
var VS = `#version 300 es
in vec2 a_pos;
out vec2 v_uv;
void main() {
  v_uv = a_pos * 0.5 + 0.5;
  gl_Position = vec4(a_pos, 0.0, 1.0);
}`;

// 片段着色器 —— 磁性扭曲 + 色差
var FS = `#version 300 es
precision highp float;
in vec2 v_uv;
out vec4 fragColor;
uniform sampler2D u_tex;
uniform vec2 u_cursor;   // 光标位置 (0-1)
uniform float u_strength; // 扭曲强度 (0-1)

void main() {
  vec2 uv = v_uv;
  vec2 delta = uv - u_cursor;
  float dist = length(delta);
  float warp = u_strength * exp(-dist * dist * 8.0);
  vec2 warped = uv - delta * warp * 0.3;

  // 扭曲部位的色差
  float aberration = warp * 0.008;
  float r = texture(u_tex, warped + vec2(aberration, 0.0)).r;
  float g = texture(u_tex, warped).g;
  float b = texture(u_tex, warped - vec2(aberration, 0.0)).b;
  fragColor = vec4(r, g, b, 1.0);
}`;

// 编译、链接、设置四边形几何体、上传纹理...
// （参见 registry/blocks/vfx-magnetic/vfx-magnetic.html 获取完整实现）

// 从 GSAP 驱动光标位置
var proxy = { cx: 0.2, cy: 0.5, strength: 0.0 };
tl.to(
  proxy,
  {
    cx: 0.8,
    cy: 0.4,
    strength: 1.0,
    duration: BEAT_DURATION,
    ease: "power2.inOut",
    onUpdate: function () {
      captureContent();
      // 上传纹理，设置 uniforms，绘制
      gl.uniform2f(cursorLoc, proxy.cx, proxy.cy);
      gl.uniform1f(strengthLoc, proxy.strength);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    },
  },
  0,
);
```

---

### 3. 破碎 / 碎片爆炸（Three.js）

**效果描述：** 内容碎裂成几何碎片飞散开来，露出背后的内容。

**使用时机：** 戏剧性过渡、"挣脱"时刻、紧张释放。

**关键技术：** 使用 BufferGeometry 将源纹理细分为三角网格碎片，然后使用 GSAP 动画化每个碎片的位置/旋转。

研究 `registry/blocks/vfx-shatter/vfx-shatter.html` 以获取完整的 1156 行实现。核心思想：

```js
// 1. 将内容捕获到纹理（相同模板）
// 用于确定性的种子化 PRNG —— Math.random() 被禁用
function mulberry32(seed) {
  return function () {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
var rng = mulberry32(42);

// 2. 从纹理创建 N 个三角形碎片
var fragments = [];
for (var i = 0; i < NUM_FRAGMENTS; i++) {
  var geom = new THREE.BufferGeometry();
  var mesh = new THREE.Mesh(geom, new THREE.MeshBasicMaterial({ map: texture }));
  scene3d.add(mesh);
  fragments.push({ mesh: mesh, targetPos: randomExplosionVector(rng), delay: rng() * 0.5 });
}

// 3. 动画：先保持静止，然后爆炸
tl.to({}, { duration: holdTime }, 0);
fragments.forEach(function (frag) {
  tl.to(
    frag.mesh.position,
    {
      x: frag.targetPos.x,
      y: frag.targetPos.y,
      z: frag.targetPos.z,
      duration: 0.8,
      ease: "power3.in",
    },
    holdTime + frag.delay,
  );
  tl.to(
    frag.mesh.rotation,
    { x: rng() * 4, y: rng() * 4, duration: 0.8, ease: "power2.in" },
    holdTime + frag.delay,
  );
});
```

---

### 4. 液体 / 流体表面（Three.js）

**效果描述：** 内容漂浮在波纹流动的液体表面上，具有实时波动动力学。或者内容本身就是表面，像水一样起伏。

**使用时机：** 有机/高级感、环境背景、"有生命"的产品展示。

**关键技术：** 细分 PlaneGeometry，在顶点着色器中通过噪声函数驱动顶点位移。

研究 `registry/blocks/vfx-liquid-background/vfx-liquid-background.html` 以获取 1244 行的实现。核心思想：

```js
// 自定义顶点着色器，带波动偏移
var vertexShader = `
  varying vec2 vUv;
  uniform float u_time;
  void main() {
    vUv = uv;
    vec3 pos = position;
    // 正弦波位移
    pos.z += sin(pos.x * 3.0 + u_time * 2.0) * 0.15;
    pos.z += cos(pos.y * 2.5 + u_time * 1.5) * 0.1;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  }
`;

var mesh = new THREE.Mesh(
  new THREE.PlaneGeometry(4, 3, 64, 64), // 高度细分以实现平滑波动
  new THREE.ShaderMaterial({
    vertexShader: vertexShader,
    fragmentShader: `varying vec2 vUv; uniform sampler2D u_tex;
      void main() { gl_FragColor = texture2D(u_tex, vUv); }`,
    uniforms: {
      u_tex: { value: texture },
      u_time: { value: 0 },
    },
  }),
);
```

---

### 5. 传送门 / 维度揭示（Three.js）

**效果描述：** 一个发光的圆形传送门打开，内容从另一个维度通过它出现。

**使用时机：** 产品亮相、"进入应用"时刻、主角功能引入。

研究 `registry/blocks/vfx-portal/vfx-portal.html` 以获取完整的 863 行实现。

---

## 何时使用 HTML-in-Canvas vs 标准 GSAP

| 场景                           | 使用方式                            | 原因                                   |
| ------------------------------ | ----------------------------------- | -------------------------------------- |
| 主角产品截图展示               | HTML-in-Canvas（3D 旋转 + 辉光）    | 让平面 UI 具有电影感                   |
| 功能列表 / 统计数据            | 标准 GSAP                           | 内容导向，不需要 3D                    |
| CTA / 品牌揭示                 | HTML-in-Canvas（传送门或磁性扭曲）  | 让瞬间令人印象深刻                     |
| 社交证明 / Logo                | 标准 GSAP                           | 有序级联，信任感稳定                    |
| 幕间过渡                       | HTML-in-Canvas（破碎）              | 戏剧性的幕间切换                       |
| 背景氛围                       | HTML-in-Canvas（液体表面）          | 高级环境感                             |
| 快速功能卡片                   | 标准 GSAP                           | 速度优先，3D 会拖慢                    |

---

## 更多你可构建的特效

这些不在 VFX 块中——从核心模板 + 自定义片段着色器自行构建。每个特效是对捕获纹理应用单一 GLSL 函数。

### 6. 噪声溶解

内容溶解为噪点粒子，露出背后的内容。非常适合过渡。

```glsl
// 片段着色器 —— 基于噪声的溶解
uniform float u_progress; // 0.0 = 完全可见，1.0 = 完全溶解
uniform sampler2D u_tex;

float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

void main() {
  vec2 uv = v_uv;
  float noise = hash(uv * 50.0);
  float threshold = u_progress;
  if (noise < threshold) {
    // 溶解边界的边缘辉光
    float edge = smoothstep(threshold - 0.05, threshold, noise);
    fragColor = vec4(1.0, 0.6, 0.2, 1.0) * (1.0 - edge); // 橙色边缘辉光
  } else {
    fragColor = texture(u_tex, uv);
  }
}
```

### 7. 全息 / 彩虹色

内容带有随时间移动的彩虹色全息光泽。未来感、高级感。

```glsl
uniform float u_time;
uniform sampler2D u_tex;

void main() {
  vec4 color = texture(u_tex, v_uv);
  // 基于位置 + 时间的彩虹色调偏移
  float angle = v_uv.x * 6.28 + v_uv.y * 3.14 + u_time * 0.5;
  vec3 holo = vec3(
    sin(angle) * 0.5 + 0.5,
    sin(angle + 2.094) * 0.5 + 0.5,
    sin(angle + 4.189) * 0.5 + 0.5
  );
  // 将全息效果混合到内容上（微妙的叠加）
  fragColor = vec4(mix(color.rgb, holo, 0.15 + 0.1 * sin(u_time)), color.a);
}
```

### 8. 扫描线 + CRT

复古 CRT 显示器外观——扫描线、轻微曲率、荧光粉辉光。适合"代码"或"终端"节拍。

```glsl
uniform sampler2D u_tex;
uniform float u_time;

void main() {
  vec2 uv = v_uv;
  // 桶形畸变（CRT 曲率）
  vec2 centered = uv - 0.5;
  float dist = dot(centered, centered);
  uv = uv + centered * dist * 0.15;

  vec4 color = texture(u_tex, uv);
  // 扫描线
  float scanline = sin(uv.y * 800.0) * 0.04;
  color.rgb -= scanline;
  // 轻微 RGB 偏移（荧光粉）
  color.r = texture(u_tex, uv + vec2(0.001, 0.0)).r;
  color.b = texture(u_tex, uv - vec2(0.001, 0.0)).b;
  // 暗角
  float vignette = 1.0 - dist * 2.0;
  fragColor = vec4(color.rgb * vignette, 1.0);
}
```

### 9. 磨砂玻璃模糊

磨砂玻璃背后的内容——可见但柔和，带有微妙的光折射。适合"幕后"或"即将推出"时刻。

```glsl
uniform sampler2D u_tex;
uniform float u_blur; // 0.0 = 清晰，1.0 = 完全磨砂

void main() {
  vec2 uv = v_uv;
  vec4 color = vec4(0.0);
  // 带偏移的方框模糊
  float radius = u_blur * 0.015;
  for (float x = -2.0; x <= 2.0; x += 1.0) {
    for (float y = -2.0; y <= 2.0; y += 1.0) {
      color += texture(u_tex, uv + vec2(x, y) * radius);
    }
  }
  color /= 25.0;
  // 添加磨砂噪声纹理
  float frost = fract(sin(dot(uv * 200.0, vec2(12.9898, 78.233))) * 43758.5453);
  color.rgb += frost * 0.03 * u_blur;
  fragColor = color;
}
```

### 10. 像素排序 / 故障艺术

像素在垂直或水平条中重新排列——数字艺术美学。适合科技/创意品牌。

```glsl
uniform sampler2D u_tex;
uniform float u_intensity; // 0-1

void main() {
  vec2 uv = v_uv;
  // 每行的随机水平位移
  float row = floor(uv.y * 80.0);
  float noise = fract(sin(row * 127.1) * 43758.5);
  float displace = step(0.7, noise) * u_intensity * 0.1;
  // 带 RGB 分裂的 UV 偏移
  float r = texture(u_tex, uv + vec2(displace, 0.0)).r;
  float g = texture(u_tex, uv).g;
  float b = texture(u_tex, uv - vec2(displace * 0.5, 0.0)).b;
  fragColor = vec4(r, g, b, 1.0);
}
```

---

## 创建**任何**自定义特效

上述片段着色器是模板。模式始终是：

1. 使用 `drawElementImage` **捕获你的 HTML 内容**（顶部的模板）
2. **将捕获的 canvas 上传为 WebGL 纹理**
3. **编写一个片段着色器**，从纹理读取并输出修改后的颜色
4. **通过 `onUpdate` 从 GSAP 驱动着色器 uniforms**

任何来自 ShaderToy、The Book of Shaders、CodePen 或任何地方的 GLSL 特效都可以适配：

1. 找到你喜欢的特效（搜索 "GLSL [特效名称]" 或浏览 shadertoy.com）
2. 复制片段着色器
3. 将 `iResolution` 替换为 `vec2(1920.0, 1080.0)`，将 `iTime` 替换为你的 `u_time` uniform
4. 为捕获的内容纹理添加 `uniform sampler2D u_tex;`
5. 将 uniforms 连接到 GSAP proxy 值

**超越平面几何体的创意：**

- `SphereGeometry` — 内容映射到球体上（世界地图、全球覆盖）
- `CylinderGeometry` — 内容在旋转圆柱体上（轮播/滚动感）
- `TorusGeometry` — 内容环绕在环上（无限、循环）
- `BoxGeometry` — 内容在 3D 盒子上（产品包装、骰子）
- GLTF 模型 — 内容作为屏幕纹理映射到手机、笔记本电脑、显示器上（参见 `vfx-iphone-device`）

**后处理堆叠**（Three.js EffectComposer）：

- 辉光 + 胶片颗粒 = 电影感
- 辉光 + 色差 = 镜头效果
- 景深 + 暗角 = 聚焦注意力
- 胶片颗粒 + 扫描线 = 复古
- 多个通道叠加——你想要的任意数目

**你不限于这里列出的特效。** 如果你能想象一种视觉处理方式，你就能构建它。HTML-in-Canvas API 为你提供素材（任何 HTML 渲染为纹理），WebGL/Three.js 为你提供对该素材呈现方式的无限创作控制。
