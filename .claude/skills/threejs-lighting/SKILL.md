---
name: threejs-lighting
description: Three.js 灯光 — 灯光类型、阴影、环境光照。在添加灯光、配置阴影、设置 IBL 或优化灯光性能时使用。
---

# Three.js 灯光

## 快速开始

```javascript
import * as THREE from "three";

// 基础灯光设置
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5);
scene.add(directionalLight);
```

## 灯光类型概览

| 灯光 | 描述 | 阴影支持 | 性能消耗 |
| ---------------- | ---------------------- | -------------- | -------- |
| AmbientLight | 均匀照亮所有方向 | 否 | 极低 |
| HemisphereLight | 天空/地面渐变 | 否 | 极低 |
| DirectionalLight | 平行光线（太阳） | 是 | 低 |
| PointLight | 全向发光（灯泡） | 是 | 中 |
| SpotLight | 锥形光束 | 是 | 中 |
| RectAreaLight | 面光源（窗户） | 否* | 高 |

\*RectAreaLight 阴影需要自定义解决方案

## AmbientLight（环境光）

均匀照亮所有对象。无方向，无阴影。

```javascript
// AmbientLight(color, intensity)
const ambient = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambient);

// 运行时修改
ambient.color.set(0xffffcc);
ambient.intensity = 0.3;
```

## HemisphereLight（半球光）

从天空到地面的颜色渐变。适合室外场景。

```javascript
// HemisphereLight(skyColor, groundColor, intensity)
const hemi = new THREE.HemisphereLight(0x87ceeb, 0x8b4513, 0.6);
hemi.position.set(0, 50, 0);
scene.add(hemi);

// 属性
hemi.color; // 天空颜色
hemi.groundColor; // 地面颜色
hemi.intensity;
```

## DirectionalLight（方向光）

平行光线。模拟远距离光源（太阳）。

```javascript
// DirectionalLight(color, intensity)
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 10, 5);

// 光源指向目标（默认：0, 0, 0）
dirLight.target.position.set(0, 0, 0);
scene.add(dirLight.target);

scene.add(dirLight);
```

### DirectionalLight 阴影

```javascript
dirLight.castShadow = true;

// 阴影贴图大小（越大越清晰，越耗性能）
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;

// 阴影摄像机（正交投影）
dirLight.shadow.camera.near = 0.5;
dirLight.shadow.camera.far = 50;
dirLight.shadow.camera.left = -10;
dirLight.shadow.camera.right = 10;
dirLight.shadow.camera.top = 10;
dirLight.shadow.camera.bottom = -10;

// 阴影柔化
dirLight.shadow.radius = 4; // 模糊半径（仅限 PCFSoftShadowMap）

// 阴影偏移（修复阴影痤疮）
dirLight.shadow.bias = -0.0001;
dirLight.shadow.normalBias = 0.02;

// 可视化阴影摄像机的辅助器
const helper = new THREE.CameraHelper(dirLight.shadow.camera);
scene.add(helper);
```

## PointLight（点光源）

从一点向所有方向发射光线。类似灯泡。

```javascript
// PointLight(color, intensity, distance, decay)
const pointLight = new THREE.PointLight(0xffffff, 1, 100, 2);
pointLight.position.set(0, 5, 0);
scene.add(pointLight);

// 属性
pointLight.distance; // 最大范围（0 = 无限）
pointLight.decay; // 光衰减（物理正确 = 2）
```

### PointLight 阴影

```javascript
pointLight.castShadow = true;
pointLight.shadow.mapSize.width = 1024;
pointLight.shadow.mapSize.height = 1024;

// 阴影摄像机（透视 — 6 个方向的立方体贴图）
pointLight.shadow.camera.near = 0.5;
pointLight.shadow.camera.far = 50;

pointLight.shadow.bias = -0.005;
```

## SpotLight（聚光灯）

锥形光束。类似手电筒或舞台灯光。

```javascript
// SpotLight(color, intensity, distance, angle, penumbra, decay)
const spotLight = new THREE.SpotLight(0xffffff, 1, 100, Math.PI / 6, 0.5, 2);
spotLight.position.set(0, 10, 0);

// 目标（灯光指向此点）
spotLight.target.position.set(0, 0, 0);
scene.add(spotLight.target);

scene.add(spotLight);

// 属性
spotLight.angle; // 锥角（弧度，最大 Math.PI/2）
spotLight.penumbra; // 柔化边缘（0-1）
spotLight.distance; // 范围
spotLight.decay; // 衰减
```

### SpotLight 阴影

```javascript
spotLight.castShadow = true;
spotLight.shadow.mapSize.width = 1024;
spotLight.shadow.mapSize.height = 1024;

// 阴影摄像机（透视）
spotLight.shadow.camera.near = 0.5;
spotLight.shadow.camera.far = 50;
spotLight.shadow.camera.fov = 30;

spotLight.shadow.bias = -0.0001;

// 焦点（影响阴影投影）
spotLight.shadow.focus = 1;
```

## RectAreaLight（矩形区域光）

矩形面光源。适合柔和、逼真的照明。

```javascript
import { RectAreaLightHelper } from "three/examples/jsm/helpers/RectAreaLightHelper.js";
import { RectAreaLightUniformsLib } from "three/examples/jsm/lights/RectAreaLightUniformsLib.js";

// 必须先初始化 uniforms
RectAreaLightUniformsLib.init();

// RectAreaLight(color, intensity, width, height)
const rectLight = new THREE.RectAreaLight(0xffffff, 5, 4, 2);
rectLight.position.set(0, 5, 0);
rectLight.lookAt(0, 0, 0);
scene.add(rectLight);

// 辅助器
const helper = new RectAreaLightHelper(rectLight);
rectLight.add(helper);

// 注意：仅适用于 MeshStandardMaterial 和 MeshPhysicalMaterial
// 原生不支持投射阴影
```

## 阴影设置

### 启用阴影

```javascript
// 1. 在渲染器上启用
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// 阴影贴图类型：
// THREE.BasicShadowMap - 最快，低质量
// THREE.PCFShadowMap - 默认，过滤
// THREE.PCFSoftShadowMap - 更柔和的边缘
// THREE.VSMShadowMap - 方差阴影贴图

// 2. 在灯光上启用
light.castShadow = true;

// 3. 在对象上启用
mesh.castShadow = true;
mesh.receiveShadow = true;

// 地面
floor.receiveShadow = true;
floor.castShadow = false; // 地面通常为 false
```

### 优化阴影

```javascript
// 紧缩阴影摄像机视锥体
const d = 10;
dirLight.shadow.camera.left = -d;
dirLight.shadow.camera.right = d;
dirLight.shadow.camera.top = d;
dirLight.shadow.camera.bottom = -d;
dirLight.shadow.camera.near = 0.5;
dirLight.shadow.camera.far = 30;

// 修复阴影痤疮
dirLight.shadow.bias = -0.0001; // 深度偏移
dirLight.shadow.normalBias = 0.02; // 沿法线偏移

// 阴影贴图大小（平衡质量与性能）
// 512 - 低质量
// 1024 - 中等质量
// 2048 - 高质量
// 4096 - 极高（昂贵）
```

### 接触阴影（伪阴影，快速）

```javascript
import { ContactShadows } from "three/examples/jsm/objects/ContactShadows.js";

const contactShadows = new ContactShadows({
  resolution: 512,
  blur: 2,
  opacity: 0.5,
  scale: 10,
  position: [0, 0, 0],
});
scene.add(contactShadows);
```

## 灯光辅助器

```javascript
import { RectAreaLightHelper } from "three/examples/jsm/helpers/RectAreaLightHelper.js";

// DirectionalLight 辅助器
const dirHelper = new THREE.DirectionalLightHelper(dirLight, 5);
scene.add(dirHelper);

// PointLight 辅助器
const pointHelper = new THREE.PointLightHelper(pointLight, 1);
scene.add(pointHelper);

// SpotLight 辅助器
const spotHelper = new THREE.SpotLightHelper(spotLight);
scene.add(spotHelper);

// Hemisphere 辅助器
const hemiHelper = new THREE.HemisphereLightHelper(hemiLight, 5);
scene.add(hemiHelper);

// RectAreaLight 辅助器
const rectHelper = new RectAreaLightHelper(rectLight);
rectLight.add(rectHelper);

// 灯光变化时更新辅助器
dirHelper.update();
spotHelper.update();
```

## 环境照明（IBL）

使用 HDR 环境贴图的基于图像的照明。

```javascript
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";

const rgbeLoader = new RGBELoader();
rgbeLoader.load("environment.hdr", (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;

  // 设置为场景环境（影响所有 PBR 材质）
  scene.environment = texture;

  // 可选：也用作背景
  scene.background = texture;
  scene.backgroundBlurriness = 0; // 0-1，模糊背景
  scene.backgroundIntensity = 1;
});

// PMREMGenerator 用于更好的反射
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();

rgbeLoader.load("environment.hdr", (texture) => {
  const envMap = pmremGenerator.fromEquirectangular(texture).texture;
  scene.environment = envMap;
  texture.dispose();
  pmremGenerator.dispose();
});
```

### 立方体贴图环境

```javascript
const cubeLoader = new THREE.CubeTextureLoader();
const envMap = cubeLoader.load([
  "px.jpg", "nx.jpg",
  "py.jpg", "ny.jpg",
  "pz.jpg", "nz.jpg",
]);

scene.environment = envMap;
scene.background = envMap;
```

## 光照探针（高级）

从空间中某一点捕捉光照信息，用于环境照明。

```javascript
import { LightProbeGenerator } from "three/examples/jsm/lights/LightProbeGenerator.js";

// 从立方体贴图生成
const lightProbe = new THREE.LightProbe();
scene.add(lightProbe);

lightProbe.copy(LightProbeGenerator.fromCubeTexture(cubeTexture));

// 或从渲染目标生成
const cubeCamera = new THREE.CubeCamera(
  0.1, 100,
  new THREE.WebGLCubeRenderTarget(256),
);
cubeCamera.update(renderer, scene);
lightProbe.copy(
  LightProbeGenerator.fromCubeRenderTarget(renderer, cubeCamera.renderTarget),
);
```

## 常用灯光设置

### 三点照明

```javascript
// 主光
const keyLight = new THREE.DirectionalLight(0xffffff, 1);
keyLight.position.set(5, 5, 5);
scene.add(keyLight);

// 补光（更柔和，在另一侧）
const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
fillLight.position.set(-5, 3, 5);
scene.add(fillLight);

// 背光（轮廓光）
const backLight = new THREE.DirectionalLight(0xffffff, 0.3);
backLight.position.set(0, 5, -5);
scene.add(backLight);

// 环境补光
const ambient = new THREE.AmbientLight(0x404040, 0.3);
scene.add(ambient);
```

### 室外日光

```javascript
// 太阳
const sun = new THREE.DirectionalLight(0xffffcc, 1.5);
sun.position.set(50, 100, 50);
sun.castShadow = true;
scene.add(sun);

// 天空环境
const hemi = new THREE.HemisphereLight(0x87ceeb, 0x8b4513, 0.6);
scene.add(hemi);
```

### 室内工作室

```javascript
// 多个面光源
RectAreaLightUniformsLib.init();

const light1 = new THREE.RectAreaLight(0xffffff, 5, 2, 2);
light1.position.set(3, 3, 3);
light1.lookAt(0, 0, 0);
scene.add(light1);

const light2 = new THREE.RectAreaLight(0xffffff, 3, 2, 2);
light2.position.set(-3, 3, 3);
light2.lookAt(0, 0, 0);
scene.add(light2);

// 环境补光
const ambient = new THREE.AmbientLight(0x404040, 0.2);
scene.add(ambient);
```

## 灯光动画

```javascript
const clock = new THREE.Clock();

function animate() {
  const time = clock.getElapsedTime();

  // 灯光围绕场景旋转
  light.position.x = Math.cos(time) * 5;
  light.position.z = Math.sin(time) * 5;

  // 脉动强度
  light.intensity = 1 + Math.sin(time * 2) * 0.5;

  // 颜色循环
  light.color.setHSL((time * 0.1) % 1, 1, 0.5);

  // 如果使用辅助器则更新
  lightHelper.update();
}
```

## 性能提示

1. **限制灯光数量**：每个灯光增加着色器复杂度
2. **使用烘焙光照**：对于静态场景，烘焙到纹理中
3. **较小的阴影贴图**：512-1024 通常足够
4. **紧缩阴影视锥体**：仅覆盖需要的区域
5. **禁用未使用的阴影**：并非所有灯光都需要阴影
6. **使用灯光图层**：将对象排除在特定灯光之外

```javascript
// 灯光图层
light.layers.set(1); // 灯光仅影响图层 1
mesh.layers.enable(1); // 网格在图层 1 上
otherMesh.layers.disable(1); // 其他网格不受影响

// 选择性阴影
mesh.castShadow = true;
mesh.receiveShadow = true;
decorMesh.castShadow = false; // 小对象通常不需要投射阴影
```

## 另请参阅

- `threejs-materials` — 材质对光的响应
- `threejs-textures` — 光照贴图和环境贴图
- `threejs-postprocessing` — 泛光和其他灯光效果
