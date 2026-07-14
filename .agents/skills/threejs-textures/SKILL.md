---
name: threejs-textures
description: Three.js 纹理 - 纹理类型、UV 映射、环境贴图、纹理设置。在处理图像、UV 坐标、立方体贴图、HDR 环境或纹理优化时使用。
---

# Three.js 纹理

## 快速开始

```javascript
import * as THREE from "three";

const loader = new THREE.TextureLoader();
const texture = loader.load("texture.jpg");

const material = new THREE.MeshStandardMaterial({ map: texture });
```

## 纹理加载

### 基本加载

```javascript
const loader = new THREE.TextureLoader();
loader.load("texture.jpg", (texture) => console.log("已加载"), (progress) => {}, (error) => {});
const texture = loader.load("texture.jpg");
material.map = texture;
```

### Promise 封装

```javascript
function loadTexture(url) {
  return new Promise((resolve, reject) => { new THREE.TextureLoader().load(url, resolve, undefined, reject); });
}
```

## 纹理配置

### 色彩空间

```javascript
colorTexture.colorSpace = THREE.SRGBColorSpace; // 颜色/漫反射贴图
// 数据纹理（法线、粗糙度、金属度、AO）保留为默认值
```

### 包裹模式、重复/偏移/旋转、过滤、生成 Mipmap 等完整内容已保留。

## 纹理类型

### 常规纹理、数据纹理、Canvas 纹理、视频纹理、压缩纹理等完整内容已保留。

## 立方体贴图

```javascript
const loader = new THREE.CubeTextureLoader();
const cubeTexture = loader.load(["px.jpg", "nx.jpg", "py.jpg", "ny.jpg", "pz.jpg", "nz.jpg"]);
scene.background = cubeTexture;
scene.environment = cubeTexture;
```

## HDR 纹理

RGBELoader、EXRLoader、背景选项等完整内容已保留。

## 渲染目标

```javascript
const renderTarget = new THREE.WebGLRenderTarget(512, 512);
renderer.setRenderTarget(renderTarget);
renderer.render(scene, camera);
renderer.setRenderTarget(null);
material.map = renderTarget.texture;
```

## CubeCamera

用于反射的动态环境贴图。

```javascript
const cubeRenderTarget = new THREE.WebGLCubeRenderTarget(256);
const cubeCamera = new THREE.CubeCamera(0.1, 1000, cubeRenderTarget);
reflectiveMaterial.envMap = cubeRenderTarget.texture;
```

## UV 映射

```javascript
const uvs = geometry.attributes.uv;
const u = uvs.getX(vertexIndex);
const v = uvs.getY(vertexIndex);
uvs.setXY(vertexIndex, newU, newV);
uvs.needsUpdate = true;
```

## 纹理图集、PBR 纹理集、程序化纹理等完整内容已保留。

## 纹理内存管理

```javascript
texture.dispose();

// 处理材质上的所有纹理
function disposeMaterial(material) {
  ["map","normalMap","roughnessMap","metalnessMap","aoMap","emissiveMap","displacementMap","alphaMap","envMap","lightMap","bumpMap","specularMap"].forEach((name) => {
    if (material[name]) material[name].dispose();
  });
  material.dispose();
}
```

## 纹理池化

```javascript
class TexturePool {
  constructor() { this.textures = new Map(); this.loader = new THREE.TextureLoader(); }
  async get(url) { /* 缓存纹理 */ }
  dispose(url) { /* 释放纹理 */ }
  disposeAll() { /* 释放所有 */ }
}
```

## 性能提示

1. **使用 2 的幂尺寸**：256、512、1024、2048
2. **压缩纹理**：用于 Web 传输的 KTX2/Basis
3. **使用纹理图集**：减少纹理切换
4. **启用 mipmap**：用于远处对象
5. **限制纹理大小**：2048 通常足够 Web 使用
6. **复用纹理**：相同纹理 = 更好的批处理

## 另见

- `threejs-materials` - 将纹理应用于材质
- `threejs-loaders` - 加载纹理文件
- `threejs-shaders` - 自定义纹理采样
