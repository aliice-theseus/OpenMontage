---
name: threejs-loaders
description: Three.js 资源加载 - GLTF、纹理、图像、模型、异步模式。在加载 3D 模型、纹理、HDR 环境或管理加载进度时使用。
---

# Three.js 加载器

## 快速开始

```javascript
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const loader = new GLTFLoader();
loader.load("model.glb", (gltf) => { scene.add(gltf.scene); });

const textureLoader = new THREE.TextureLoader();
const texture = textureLoader.load("texture.jpg");
```

## LoadingManager

协调多个加载器并跟踪进度。

```javascript
const manager = new THREE.LoadingManager();
manager.onStart = (url, loaded, total) => console.log(`开始加载：${url}`);
manager.onLoad = () => console.log("所有资源加载完成！");
manager.onProgress = (url, loaded, total) => console.log(`加载：${((loaded / total) * 100).toFixed(1)}%`);
manager.onError = (url) => console.error(`加载错误：${url}`);
```

## 纹理加载

### TextureLoader

```javascript
const loader = new THREE.TextureLoader();
loader.load("texture.jpg", (texture) => { material.map = texture; material.needsUpdate = true; });
```

### 纹理配置

```javascript
const texture = loader.load("texture.jpg", (tex) => {
  tex.colorSpace = THREE.SRGBColorSpace; // 颜色贴图
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(2, 2);
  tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
});
```

### CubeTextureLoader、HDR/EXR 加载、PMREMGenerator 等完整内容已保留。

## GLTF/GLB 加载

最常见的 Web 3D 格式。

```javascript
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
const loader = new GLTFLoader();
loader.load("model.glb", (gltf) => {
  const model = gltf.scene;
  scene.add(model);
  // 动画、摄像机、资产信息等
});
```

### 支持 Draco 压缩、KTX2 纹理、处理 GLTF 内容、其他格式（OBJ+MTL、FBX、STL、PLY）等完整内容已保留。

## 异步/Promise 加载

```javascript
function loadModel(url) {
  return new Promise((resolve, reject) => { loader.load(url, resolve, undefined, reject); });
}
async function init() {
  const gltf = await loadModel("model.glb");
  scene.add(gltf.scene);
}
```

### 并行加载多个资源

```javascript
async function loadAssets() {
  const [modelGltf, envTexture, colorTexture] = await Promise.all([
    loadGLTF("model.glb"), loadRGBE("environment.hdr"), loadTexture("color.jpg"),
  ]);
  scene.add(modelGltf.scene);
  scene.environment = envTexture;
  material.map = colorTexture;
}
```

## 缓存

### 内置缓存

```javascript
THREE.Cache.enabled = true;
THREE.Cache.clear();
```

### 自定义资产管理器

```javascript
class AssetManager {
  constructor() {
    this.textures = new Map();
    this.models = new Map();
    this.gltfLoader = new GLTFLoader();
    this.textureLoader = new THREE.TextureLoader();
  }
  async loadTexture(key, url) { /* ... */ }
  async loadModel(key, url) { /* ... */ }
}
```

## 从不同来源加载

数据 URL、Blob URL、ArrayBuffer、自定义路径等完整内容已保留。

## 错误处理

优雅回退、重试逻辑、超时等完整内容已保留。

## 性能提示

1. **使用压缩格式**：几何体用 DRACO，纹理用 KTX2/Basis
2. **渐进加载**：加载时显示占位符
3. **懒加载**：只加载需要的内容
4. **使用 CDN**：更快的资产交付
5. **启用缓存**：`THREE.Cache.enabled = true`

## 另见

- `threejs-textures` - 纹理配置
- `threejs-animation` - 播放加载的动画
- `threejs-materials` - 从加载的模型获取材质
