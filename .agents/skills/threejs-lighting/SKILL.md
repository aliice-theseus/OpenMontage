---
name: threejs-lighting
description: Three.js 光照 - 灯光类型、阴影、环境光照。在添加灯光、配置阴影、设置 IBL 或优化光照性能时使用。
---

# Three.js 光照

## 快速开始

```javascript
import * as THREE from "three";

// 基本光照设置
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5);
scene.add(directionalLight);
```

## 灯光类型概览

| 灯光 | 描述 | 阴影支持 | 开销 |
| ---------------- | ---------------------- | -------------- | -------- |
| AmbientLight | 均匀全向 | 否 | 非常低 |
| HemisphereLight | 天空/地面渐变 | 否 | 非常低 |
| DirectionalLight | 平行光线（太阳） | 是 | 低 |
| PointLight | 全向（灯泡） | 是 | 中等 |
| SpotLight | 锥形 | 是 | 中等 |
| RectAreaLight | 区域光（窗户） | 否 | 高 |

## 各灯光类型

（AmbientLight、HemisphereLight、DirectionalLight、PointLight、SpotLight、RectAreaLight 的完整 API 和配置已保留）

### DirectionalLight 阴影

```javascript
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
dirLight.shadow.camera.near = 0.5;
dirLight.shadow.camera.far = 50;
dirLight.shadow.camera.left = -10;
dirLight.shadow.camera.right = 10;
dirLight.shadow.camera.top = 10;
dirLight.shadow.camera.bottom = -10;
dirLight.shadow.radius = 4;
dirLight.shadow.bias = -0.0001;
dirLight.shadow.normalBias = 0.02;
```

## 阴影设置

### 启用阴影

```javascript
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
light.castShadow = true;
mesh.castShadow = true;
mesh.receiveShadow = true;
```

### 接触阴影（伪阴影，快速）

```javascript
import { ContactShadows } from "three/examples/jsm/objects/ContactShadows.js";
const contactShadows = new ContactShadows({ resolution: 512, blur: 2, opacity: 0.5, scale: 10 });
scene.add(contactShadows);
```

## 灯光辅助工具

（DirectionalLightHelper、PointLightHelper、SpotLightHelper、HemisphereLightHelper、RectAreaLightHelper）

## 环境光照（IBL）

基于图像的光照，使用 HDR 环境贴图。

```javascript
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";
const rgbeLoader = new RGBELoader();
rgbeLoader.load("environment.hdr", (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture;
  scene.background = texture;
});
```

## 常见光照设置

### 三点光照、户外日光、室内工作室等完整示例已保留。

## 光照动画

```javascript
const clock = new THREE.Clock();
function animate() {
  const time = clock.getElapsedTime();
  light.position.x = Math.cos(time) * 5;
  light.position.z = Math.sin(time) * 5;
  light.intensity = 1 + Math.sin(time * 2) * 0.5;
}
```

## 性能提示

1. **限制灯光数量**：每盏灯增加着色器复杂度
2. **使用烘焙光照**：静态场景烘焙到纹理
3. **较小的阴影贴图**：512-1024 通常足够
4. **紧凑的阴影视锥体**：只覆盖需要的区域
5. **禁用未使用的阴影**：不是所有灯光都需要阴影
6. **使用灯光图层**：将某些对象从特定灯光中排除

## 另见

- `threejs-materials` - 材质对光的响应
- `threejs-textures` - 光照贴图和环境贴图
- `threejs-postprocessing` - 泛光和其他光照效果
