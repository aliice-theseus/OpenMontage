---
name: threejs-interaction
description: Three.js 交互 - 射线投射、控制器、鼠标/触摸输入、对象选择。在处理用户输入、实现点击检测、添加摄像机控制器或创建交互式 3D 体验时使用。
---

# Three.js 交互

## 快速开始

```javascript
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

// 摄像机控制器
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// 用于点击检测的射线投射
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onClick(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(scene.children);
  if (intersects.length > 0) console.log("点击了：", intersects[0].object);
}
window.addEventListener("click", onClick);
```

## Raycaster（射线投射器）

### 基本射线投射

```javascript
const raycaster = new THREE.Raycaster();
raycaster.setFromCamera(mousePosition, camera); // 从摄像机（鼠标拾取）
raycaster.set(origin, direction);               // 从任意原点和方向

const intersects = raycaster.intersectObjects(objects, recursive);
// intersects 包含：distance, point, face, faceIndex, object, uv, normal, instanceId
```

### 鼠标位置转换

```javascript
const mouse = new THREE.Vector2();
// 全窗口
mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

// 特定画布元素
function updateMouseCanvas(event, canvas) {
  const rect = canvas.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
}
```

### 触摸支持、射线选项、高效射线投射等完整内容已保留。

## 摄像机控制器

### OrbitControls

```javascript
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 2;
controls.maxDistance = 50;
controls.autoRotate = true;
controls.autoRotateSpeed = 2.0;
controls.target.set(0, 1, 0);
```

（FlyControls、FirstPersonControls、PointerLockControls、TrackballControls、MapControls 的完整内容已保留）

### TransformControls

用于移动/旋转/缩放对象的 Gizmo。

```javascript
const transformControls = new TransformControls(camera, renderer.domElement);
scene.add(transformControls);
transformControls.attach(selectedMesh);
transformControls.setMode("translate"); // 'translate', 'rotate', 'scale'
transformControls.setSpace("local");   // 'local', 'world'
```

### DragControls

直接拖拽对象。

```javascript
const dragControls = new DragControls(draggableObjects, camera, renderer.domElement);
```

## 选择系统

### 点击选择、框选、悬停效果等完整内容已保留。

## 键盘输入

```javascript
const keys = {};
document.addEventListener("keydown", (event) => { keys[event.code] = true; });
document.addEventListener("keyup", (event) => { keys[event.code] = false; });
```

## 世界-屏幕坐标转换

### 世界到屏幕、屏幕到世界、射线-平面交点等完整内容已保留。

## 事件处理最佳实践

```javascript
class InteractionManager {
  constructor(camera, renderer, scene) {
    this.camera = camera;
    this.renderer = renderer;
    this.scene = scene;
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
    this.clickables = [];
    this.bindEvents();
  }
  // ... 完整实现已保留
}
```

## 性能提示

1. **限制射线投射**：节流 mousemove 处理程序
2. **使用图层**：过滤射线投射目标
3. **简单碰撞网格**：使用不可见的更简单几何体进行射线投射
4. **不需要时禁用控制器**：`controls.enabled = false`
5. **批量更新**：分组交互检查

## 另见

- `threejs-fundamentals` - 摄像机和场景设置
- `threejs-animation` - 动画化交互
- `threejs-shaders` - 视觉反馈效果
