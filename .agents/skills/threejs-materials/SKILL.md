---
name: threejs-materials
description: Three.js 材质 - PBR、基础、Phong、着色器材質、材质属性。在样式化网格、处理纹理、创建自定义着色器或优化材质性能时使用。
---

# Three.js 材质

## 快速开始

```javascript
import * as THREE from "three";

// PBR 材质（推荐用于真实渲染）
const material = new THREE.MeshStandardMaterial({
  color: 0x00ff00,
  roughness: 0.5,
  metalness: 0.5,
});
const mesh = new THREE.Mesh(geometry, material);
```

## 材质类型概览

| 材质 | 用途 | 光照 |
| -------------------- | ------------------------------------- | ------------------ |
| MeshBasicMaterial | 无光照、纯色、线框 | 否 |
| MeshLambertMaterial | 哑光表面、性能优先 | 是（仅漫反射） |
| MeshPhongMaterial | 光泽表面、高光 | 是 |
| MeshStandardMaterial | PBR、真实材质 | 是（PBR） |
| MeshPhysicalMaterial | 高级 PBR、清漆、透射 | 是（PBR+） |
| MeshToonMaterial | 赛璐珞风格、卡通效果 | 是（toon） |
| MeshNormalMaterial | 调试法线 | 否 |
| MeshDepthMaterial | 深度可视化 | 否 |
| ShaderMaterial | 自定义 GLSL 着色器 | 自定义 |
| RawShaderMaterial | 完全着色器控制 | 自定义 |

## 材质类型详解

（MeshBasicMaterial、MeshLambertMaterial、MeshPhongMaterial、MeshStandardMaterial、MeshPhysicalMaterial、MeshToonMaterial、MeshNormalMaterial、MeshDepthMaterial 的完整 API 已保留）

### MeshPhysicalMaterial（高级 PBR）

扩展 MeshStandardMaterial，增加高级功能：

```javascript
const material = new THREE.MeshPhysicalMaterial({
  clearcoat: 1.0,        // 清漆（车漆）
  transmission: 1.0,     // 透射（玻璃、水）
  ior: 1.5,              // 折射率
  sheen: 1.0,            // 光泽（织物、天鹅绒）
  iridescence: 1.0,      // 虹彩（肥皂泡）
  anisotropy: 1.0,       // 各向异性（拉丝金属）
  specularIntensity: 1,
});
```

### 玻璃材质示例、车漆示例等已保留。

## PointsMaterial、LineBasicMaterial、LineDashedMaterial 已保留。

## ShaderMaterial

自定义 GLSL 着色器，使用 Three.js 内置 uniforms。

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: { time: { value: 0 }, color: { value: new THREE.Color(0xff0000) } },
  vertexShader: `...`,
  fragmentShader: `...`,
  transparent: true,
  side: THREE.DoubleSide,
});
```

### RawShaderMaterial - 完全控制，无内置 uniforms。

## 常用材质属性

```javascript
material.visible = true;
material.transparent = false;
material.opacity = 1.0;
material.side = THREE.FrontSide;
material.blending = THREE.NormalBlending;
material.depthTest = true;
material.depthWrite = true;
```

## 多材质

```javascript
const geometry = new THREE.BoxGeometry(1, 1, 1);
const materials = [matRed, matGreen, matBlue, matYellow, matMagenta, matCyan];
const mesh = new THREE.Mesh(geometry, materials);
```

## 环境贴图

```javascript
const envMap = cubeTextureLoader.load(["px.jpg", "nx.jpg", "py.jpg", "ny.jpg", "pz.jpg", "nz.jpg"]);
material.envMap = envMap;
material.envMapIntensity = 1;
```

## 材质克隆和修改

```javascript
const clone = material.clone();
clone.color.set(0x00ff00);
material.color.set(0xff0000);
material.needsUpdate = true;
```

## 性能提示

1. **复用材质**：相同材质 = 批处理绘制调用
2. **尽可能避免透明**：透明材质需要排序
3. **使用 alphaTest 代替透明度**：适用时更快
4. **选择更简单的材质**：Basic > Lambert > Phong > Standard > Physical
5. **限制活动灯光数**：每盏灯增加着色器复杂度

## 另见

- `threejs-textures` - 纹理加载和配置
- `threejs-shaders` - 自定义着色器开发
- `threejs-lighting` - 材质与光的交互
