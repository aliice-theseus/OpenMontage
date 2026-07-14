---
name: threejs-fundamentals
description: Three.js 场景设置、摄像机、渲染器、Object3D 层级、坐标系统。在设置 3D 场景、创建摄像机、配置渲染器、管理对象层级或处理变换时使用。
---

# Three.js 基础

## 快速开始

```javascript
import * as THREE from "three";

// 创建场景、摄像机、渲染器
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000,
);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

// 添加网格
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// 添加灯光
scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 5, 5);
scene.add(dirLight);

camera.position.z = 5;

// 动画循环
function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();

// 处理窗口大小变化
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

## 核心类

### Scene（场景）

所有 3D 对象、灯光和摄像机的容器。

```javascript
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000); // 纯色背景
scene.background = texture; // 天空盒纹理
scene.background = cubeTexture; // 立方体贴图
scene.environment = envMap; // PBR 环境贴图
scene.fog = new THREE.Fog(0xffffff, 1, 100); // 线性雾
scene.fog = new THREE.FogExp2(0xffffff, 0.02); // 指数雾
```

### Cameras（摄像机）

**PerspectiveCamera（透视摄像机）** — 最常见，模拟人眼。

```javascript
// PerspectiveCamera(fov, aspect, near, far)
const camera = new THREE.PerspectiveCamera(
  75, // 视野（度）
  window.innerWidth / window.innerHeight, // 宽高比
  0.1, // 近裁剪面
  1000, // 远裁剪面
);

camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);
camera.updateProjectionMatrix(); // 在更改 fov、aspect、near、far 后调用
```

**OrthographicCamera（正交摄像机）** — 无透视失真，适合 2D/等距视图。

```javascript
// OrthographicCamera(left, right, top, bottom, near, far)
const aspect = window.innerWidth / window.innerHeight;
const frustumSize = 10;
const camera = new THREE.OrthographicCamera(
  (frustumSize * aspect) / -2,
  (frustumSize * aspect) / 2,
  frustumSize / 2,
  frustumSize / -2,
  0.1,
  1000,
);
```

**ArrayCamera（阵列摄像机）** — 使用子摄像机的多个视口。

```javascript
const cameras = [];
for (let i = 0; i < 4; i++) {
  const subcamera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
  subcamera.viewport = new THREE.Vector4(
    Math.floor(i % 2) * 0.5,
    Math.floor(i / 2) * 0.5,
    0.5,
    0.5,
  );
  cameras.push(subcamera);
}
const arrayCamera = new THREE.ArrayCamera(cameras);
```

**CubeCamera（立方体摄像机）** — 为反射渲染环境贴图。

```javascript
const cubeRenderTarget = new THREE.WebGLCubeRenderTarget(256);
const cubeCamera = new THREE.CubeCamera(0.1, 1000, cubeRenderTarget);
scene.add(cubeCamera);

// 用于反射
material.envMap = cubeRenderTarget.texture;

// 每帧更新（开销大！）
cubeCamera.position.copy(reflectiveMesh.position);
cubeCamera.update(renderer, scene);
```

### WebGLRenderer（WebGL 渲染器）

```javascript
const renderer = new THREE.WebGLRenderer({
  canvas: document.querySelector("#canvas"), // 可选现有 canvas
  antialias: true, // 平滑边缘
  alpha: true, // 透明背景
  powerPreference: "high-performance", // GPU 提示
  preserveDrawingBuffer: true, // 用于截图
});

renderer.setSize(width, height);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

// 色调映射
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

// 色彩空间（Three.js r152+）
renderer.outputColorSpace = THREE.SRGBColorSpace;

// 阴影
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// 清除颜色
renderer.setClearColor(0x000000, 1);

// 渲染
renderer.render(scene, camera);
```

### Object3D

所有 3D 对象的基类。Mesh、Group、Light、Camera 都继承自 Object3D。

```javascript
const obj = new THREE.Object3D();

// 变换
obj.position.set(x, y, z);
obj.rotation.set(x, y, z); // 欧拉角（弧度）
obj.quaternion.set(x, y, z, w); // 四元数旋转
obj.scale.set(x, y, z);

// 局部 vs 世界变换
obj.getWorldPosition(targetVector);
obj.getWorldQuaternion(targetQuaternion);
obj.getWorldDirection(targetVector);

// 层级
obj.add(child);
obj.remove(child);
obj.parent;
obj.children;

// 可见性
obj.visible = false;

// 图层（用于选择性渲染/光线投射）
obj.layers.set(1);
obj.layers.enable(2);
obj.layers.disable(0);

// 遍历层级
obj.traverse((child) => {
  if (child.isMesh) child.material.color.set(0xff0000);
});

// 矩阵更新
obj.matrixAutoUpdate = true; // 默认：自动更新矩阵
obj.updateMatrix(); // 手动矩阵更新
obj.updateMatrixWorld(true); // 递归更新世界矩阵
```

### Group（组）

用于组织对象的空容器。

```javascript
const group = new THREE.Group();
group.add(mesh1);
group.add(mesh2);
scene.add(group);

// 变换整个组
group.position.x = 5;
group.rotation.y = Math.PI / 4;
```

### Mesh（网格）

结合几何体和材质。

```javascript
const mesh = new THREE.Mesh(geometry, material);

// 多种材质（每个几何体组一个）
const mesh = new THREE.Mesh(geometry, [material1, material2]);

// 常用属性
mesh.geometry;
mesh.material;
mesh.castShadow = true;
mesh.receiveShadow = true;

// 视锥体裁剪
mesh.frustumCulled = true; // 默认：在摄像机视图外时跳过

// 渲染顺序
mesh.renderOrder = 10; // 越大越晚渲染
```

## 坐标系统

Three.js 使用**右手坐标系**：

- **+X** 指向右
- **+Y** 指向上
- **+Z** 指向观察者（屏幕外）

```javascript
// 坐标轴辅助
const axesHelper = new THREE.AxesHelper(5);
scene.add(axesHelper); // 红=X, 绿=Y, 蓝=Z
```

## 数学工具

### Vector3

```javascript
const v = new THREE.Vector3(x, y, z);
v.set(x, y, z);
v.copy(otherVector);
v.clone();

// 运算（原地修改）
v.add(v2);
v.sub(v2);
v.multiply(v2);
v.multiplyScalar(2);
v.divideScalar(2);
v.normalize();
v.negate();
v.clamp(min, max);
v.lerp(target, alpha);

// 计算（返回新值）
v.length();
v.lengthSq(); // 比 length() 更快
v.distanceTo(v2);
v.dot(v2);
v.cross(v2); // 修改 v
v.angleTo(v2);

// 变换
v.applyMatrix4(matrix);
v.applyQuaternion(q);
v.project(camera); // 世界坐标到 NDC
v.unproject(camera); // NDC 到世界坐标
```

### Matrix4

```javascript
const m = new THREE.Matrix4();
m.identity();
m.copy(other);
m.clone();

// 构建变换
m.makeTranslation(x, y, z);
m.makeRotationX(theta);
m.makeRotationY(theta);
m.makeRotationZ(theta);
m.makeRotationFromQuaternion(q);
m.makeScale(x, y, z);

// 组合/分解
m.compose(position, quaternion, scale);
m.decompose(position, quaternion, scale);

// 运算
m.multiply(m2); // m = m * m2
m.premultiply(m2); // m = m2 * m
m.invert();
m.transpose();

// 摄像机矩阵
m.makePerspective(left, right, top, bottom, near, far);
m.makeOrthographic(left, right, top, bottom, near, far);
m.lookAt(eye, target, up);
```

### Quaternion（四元数）

```javascript
const q = new THREE.Quaternion();
q.setFromEuler(euler);
q.setFromAxisAngle(axis, angle);
q.setFromRotationMatrix(matrix);

q.multiply(q2);
q.slerp(target, t); // 球面插值
q.normalize();
q.invert();
```

### Euler（欧拉角）

```javascript
const euler = new THREE.Euler(x, y, z, "XYZ"); // 顺序很重要！
euler.setFromQuaternion(q);
euler.setFromRotationMatrix(m);

// 旋转顺序：'XYZ', 'YXZ', 'ZXY', 'XZY', 'YZX', 'ZYX'
```

### Color（颜色）

```javascript
const color = new THREE.Color(0xff0000);
const color = new THREE.Color("red");
const color = new THREE.Color("rgb(255, 0, 0)");
const color = new THREE.Color("#ff0000");

color.setHex(0x00ff00);
color.setRGB(r, g, b); // 0-1 范围
color.setHSL(h, s, l); // 0-1 范围

color.lerp(otherColor, alpha);
color.multiply(otherColor);
color.multiplyScalar(2);
```

### MathUtils（数学工具）

```javascript
THREE.MathUtils.clamp(value, min, max);
THREE.MathUtils.lerp(start, end, alpha);
THREE.MathUtils.mapLinear(value, inMin, inMax, outMin, outMax);
THREE.MathUtils.degToRad(degrees);
THREE.MathUtils.radToDeg(radians);
THREE.MathUtils.randFloat(min, max);
THREE.MathUtils.randInt(min, max);
THREE.MathUtils.smoothstep(x, min, max);
THREE.MathUtils.smootherstep(x, min, max);
```

## 常用模式

### 正确清理

```javascript
function dispose() {
  // 释放几何体
  mesh.geometry.dispose();

  // 释放材质
  if (Array.isArray(mesh.material)) {
    mesh.material.forEach((m) => m.dispose());
  } else {
    mesh.material.dispose();
  }

  // 释放纹理
  texture.dispose();

  // 从场景中移除
  scene.remove(mesh);

  // 释放渲染器
  renderer.dispose();
}
```

### 动画时钟

```javascript
const clock = new THREE.Clock();

function animate() {
  const delta = clock.getDelta(); // 距离上一帧的时间（秒）
  const elapsed = clock.getElapsedTime(); // 总时间（秒）

  mesh.rotation.y += delta * 0.5; // 不论帧率如何，速度一致

  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
```

### 响应式 Canvas

```javascript
function onWindowResize() {
  const width = window.innerWidth;
  const height = window.innerHeight;

  camera.aspect = width / height;
  camera.updateProjectionMatrix();

  renderer.setSize(width, height);
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
manager.onError = (url) => console.error(`加载 ${url} 出错`);

const textureLoader = new THREE.TextureLoader(manager);
const gltfLoader = new GLTFLoader(manager);
```

## 性能提示

1. **限制绘制调用**：合并几何体、使用实例化、纹理图集
2. **视锥体裁剪**：默认启用，确保包围盒正确
3. **LOD（细节级别）**：使用 `THREE.LOD` 实现基于距离的网格切换
4. **对象池化**：重用对象而非创建/销毁
5. **避免在循环中调用 `getWorldPosition`**：缓存结果

```javascript
// 合并静态几何体
import { mergeGeometries } from "three/examples/jsm/utils/BufferGeometryUtils.js";
const merged = mergeGeometries([geo1, geo2, geo3]);

// LOD
const lod = new THREE.LOD();
lod.addLevel(highDetailMesh, 0);
lod.addLevel(medDetailMesh, 50);
lod.addLevel(lowDetailMesh, 100);
scene.add(lod);
```

## 另请参阅

- `threejs-geometry` — 几何体创建和操作
- `threejs-materials` — 材质类型和属性
- `threejs-lighting` — 灯光类型和阴影
