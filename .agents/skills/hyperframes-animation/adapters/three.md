---
name: hyperframes-three
description: Three.js 和 WebGL 适配器模式，用于 HyperFrames。在编写确定性 Three.js 场景、WebGL canvas 图层、AnimationMixer 时间线、摄像机运动、着色器驱动的视觉效果或响应 HyperFrames hf-seek 事件的 canvas 渲染时使用。
---

# Three.js 用于 HyperFrames

HyperFrames 通过其 `three` 运行时适配器支持 Three.js。适配器不管理你的场景。它发布 HyperFrames 时间并派发 seek 事件，让你的组合能够渲染确切的帧。

## 约定

- 尽可能**同步**创建场景、摄像机、渲染器、材质和资源。
- 从 HyperFrames 时间渲染，而非挂钟时间。
- 监听 `hf-seek` 事件并在确切时间渲染。
- 在渲染关键定位之前加载模型、纹理和 HDRIs。不要在定位时获取它们。
- 避免将 `requestAnimationFrame` 或 `renderer.setAnimationLoop` 作为渲染关键运动的真相源。

适配器设置 `window.__hfThreeTime` 并在每次 seek 时派发 `new CustomEvent("hf-seek", { detail: { time } })`。

## 基本模式

```html
<canvas id="three-layer"></canvas>
<script type="module">
  import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.181.2/+esm";

  const canvas = document.getElementById("three-layer");
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  // 匹配组合的帧尺寸。
  renderer.setSize(1920, 1080, false);
  renderer.setPixelRatio(1);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1920 / 1080, 0.1, 100);
  camera.position.set(0, 0, 6);

  const mesh = new THREE.Mesh(
    new THREE.IcosahedronGeometry(1.4, 4),
    new THREE.MeshStandardMaterial({ color: 0x64d2ff, roughness: 0.38 }),
  );
  scene.add(mesh);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 2));

  function renderAt(time) {
    mesh.rotation.y = time * 0.7;
    mesh.rotation.x = Math.sin(time * 0.6) * 0.16;
    renderer.render(scene, camera);
  }

  window.addEventListener("hf-seek", (event) => {
    renderAt(event.detail.time);
  });

  renderAt(window.__hfThreeTime || 0);
</script>
```

```css
#three-layer {
  width: 100%;
  height: 100%;
  display: block;
}
```

## 加载扩展（`GLTFLoader`、`OrbitControls` 等）

对于 `three/addons/` 下的任何内容，使用 importmap 使裸说明符能够解析。HyperFrames lint 能同时识别此形式和上述内联 `+esm` 导入——根据你的组合需要选择。

```html
<script type="importmap">
  {
    "imports": {
      "three": "https://cdn.jsdelivr.net/npm/three@0.181.2/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.181.2/examples/jsm/"
    }
  }
</script>
<script type="module">
  import * as THREE from "three";
  import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
  import { OrbitControls } from "three/addons/controls/OrbitControls.js";
  // ...
</script>
```

在两个条目中将 `three` 版本锁定为相同值。在地图和裸导入之间混用版本会导致静默故障。

## AnimationMixer 模式

对于 GLTF 或创作的剪辑动画，直接定位 mixer：

```js
function renderAt(time) {
  mixer.setTime(time);
  renderer.render(scene, camera);
}
```

如果有多个 mixer，从同一个 `time` 定位所有 mixer。

## 适用场景

- 确定性 3D 对象、产品旋转、使用种子数据的粒子以及着色器平板。
- 从 `time` 导出的摄像机运动。
- 当资产是本地的且在验证完成前已加载的 GLTF 动画剪辑。

## 避免

- 使用 `Date.now()`、`performance.now()` 或时钟增量来更新场景状态。
- 将渲染关键工作留在自由运行的动画循环中。
- 在渲染时加载远程模型或纹理。
- 依赖设备像素比率的输出。固定渲染器尺寸和像素比率以进行视频渲染。
- 依赖前一帧历史的后处理通道，除非你能从时间重建状态。

## 验证

编辑 Three.js 组合后：

```bash
npx hyperframes lint
npx hyperframes validate
```

## 参考与致谢

- HyperFrames 适配器源码：`packages/core/src/runtime/adapters/three.ts`。
- Three.js `WebGLRenderer` 文档：https://threejs.org/docs/pages/WebGLRenderer.html
- Three.js `AnimationMixer.setTime()` 文档：https://threejs.org/docs/pages/AnimationMixer.html
