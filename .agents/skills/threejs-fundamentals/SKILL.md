---
name: threejs-fundamentals
description: Three.js 场景设置、摄像机、渲染器、Object3D 层次结构、坐标系。在设置 3D 场景、创建摄像机、配置渲染器、管理对象层次结构或处理变换时使用。
---

# Three.js 基础

## 快速开始

```javascript
import * as THREE from "three";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 5, 5);
scene.add(dirLight);

camera.position.z = 5;

function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

## 核心类

### Scene

所有 3D 对象、灯光和摄像机的容器。

```javascript
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000); // 纯色
scene.background = texture; // 天空盒纹理
scene.background = cubeTexture; // 立方体贴图
scene.environment = envMap; // PBR 环境贴图
scene.fog = new THREE.Fog(0xffffff, 1, 100); // 线性雾
scene.fog = new THREE.FogExp2(0xffffff, 0.02); // 指数雾
```

### 摄像机

**PerspectiveCamera** - 最常用，模拟人眼。

```javascript
// PerspectiveCamera(fov, aspect, near, far)
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);
camera.updateProjectionMatrix();
```

**OrthographicCamera** - 无透视失真，适合 2D/等距。

**ArrayCamera** - 带子摄像机的多视口。

**CubeCamera** - 为反射渲染环境贴图。

### WebGLRenderer

（完整配置选项已保留）

### Object3D

所有 3D 对象的基类。Mesh、Group、Light、Camera 都扩展自 Object3D。

（变换、层次结构、可见性、图层、遍历等完整 API 已保留）

## 坐标系

Three.js 使用**右手坐标系**：

- **+X** 指向右
- **+Y** 指向上
- **+Z** 指向观察者（屏幕外）

```javascript
const axesHelper = new THREE.AxesHelper(5);
scene.add(axesHelper); // Red=X, Green=Y, Blue=Z
```

## 数学工具

（Vector3、Matrix4、Quaternion、Euler、Color、MathUtils 的完整 API 已保留）

## 常见模式

### 正确清理

```javascript
function dispose() {
  mesh.geometry.dispose();
  if (Array.isArray(mesh.material)) mesh.material.forEach((m) => m.dispose());
  else mesh.material.dispose();
  texture.dispose();
  scene.remove(mesh);
  renderer.dispose();
}
```

### 动画时钟

```javascript
const clock = new THREE.Clock();
function animate() {
  const delta = clock.getDelta();
  const elapsed = clock.getElapsedTime();
  mesh.rotation.y += delta * 0.5;
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
```

### 响应式画布

```javascript
function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
}
window.addEventListener("resize", onWindowResize);
```

### 加载管理器

```javascript
const manager = new THREE.LoadingManager();
manager.onStart = (url, loaded, total) => console.log("开始加载");
manager.onLoad = () => console.log("全部加载完成");
manager.onProgress = (url, loaded, total) => console.log(`${loaded}/${total}`);
manager.onError = (url) => console.error(`加载错误 ${url}`);
```

## 性能提示

1. **限制绘制调用**：合并几何体、使用实例化、纹理图集
2. **视锥体裁剪**：默认启用，确保包围盒正确
3. **LOD（细节级别）**：使用 `THREE.LOD` 实现基于距离的网格切换
4. **对象池化**：复用对象而不是创建/销毁
5. **避免在循环中使用 `getWorldPosition`**：缓存结果

## 另见

- `threejs-geometry` - 几何体创建和操作
- `threejs-materials` - 材质类型和属性
- `threejs-lighting` - 灯光类型和阴影
