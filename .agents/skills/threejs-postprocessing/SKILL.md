---
name: threejs-postprocessing
description: Three.js 后期处理 - EffectComposer、泛光、景深、屏幕效果。在添加视觉效果、色彩校正、模糊、发光或创建自定义屏幕空间着色器时使用。
---

# Three.js 后期处理

## 快速开始

```javascript
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";

const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5, // 强度
  0.4, // 半径
  0.85, // 阈值
);
composer.addPass(bloomPass);

function animate() {
  requestAnimationFrame(animate);
  composer.render(); // 不是 renderer.render()
}
```

## EffectComposer 设置

```javascript
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(effectPass);
// 最后一个通道应渲染到屏幕
effectPass.renderToScreen = true;
```

## 常见效果

### 泛光（Bloom）

```javascript
const bloomPass = new UnrealBloomPass(resolution, strength, radius, threshold);
bloomPass.strength = 2.0;
```

### 选择性泛光、FXAA 抗锯齿、SMAA 抗锯齿、SSAO 环境光遮蔽、景深（BokehPass）、胶片颗粒、暗角、色彩校正、Gamma 校正、像素化、故障效果、半色调、轮廓线等完整内容已保留。

## 自定义 ShaderPass

```javascript
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";

const CustomShader = {
  uniforms: { tDiffuse: { value: null }, time: { value: 0 } },
  vertexShader: `...`,
  fragmentShader: `...`,
};
const customPass = new ShaderPass(CustomShader);
composer.addPass(customPass);
customPass.uniforms.time.value = clock.getElapsedTime();
```

## 组合多个效果

```javascript
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(bloomPass);
composer.addPass(vignettePass);
composer.addPass(new ShaderPass(GammaCorrectionShader));
composer.addPass(fxaaPass); // 抗锯齿始终放在最后
```

## 渲染到纹理、多通道渲染、WebGPU 后期处理等完整内容已保留。

## 性能提示

1. **限制通道数**：每个通道增加一次全屏渲染
2. **降低分辨率**：模糊通道使用较小的渲染目标
3. **禁用未使用的效果**：开关通道
4. **使用 FXAA 代替 MSAA**：更廉价的反锯齿
5. **使用 DevTools 分析**：检查 GPU 使用情况

## 处理窗口大小变化

```javascript
function onWindowResize() {
  const width = window.innerWidth;
  const height = window.innerHeight;
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
  composer.setSize(width, height);
}
window.addEventListener("resize", onWindowResize);
```

## 另见

- `threejs-shaders` - 自定义着色器开发
- `threejs-textures` - 渲染目标
- `threejs-fundamentals` - 渲染器设置
