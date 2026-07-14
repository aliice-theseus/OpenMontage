---
name: threejs-geometry
description: Three.js 几何体创建 - 内置形状、BufferGeometry、自定义几何体、实例化。在创建 3D 形状、处理顶点、构建自定义网格或使用实例化渲染优化时使用。
---

# Three.js 几何体

## 快速开始

```javascript
import * as THREE from "three";

// 内置几何体
const box = new THREE.BoxGeometry(1, 1, 1);
const sphere = new THREE.SphereGeometry(0.5, 32, 32);
const plane = new THREE.PlaneGeometry(10, 10);

// 创建网格
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const mesh = new THREE.Mesh(box, material);
scene.add(mesh);
```

## 内置几何体

### 基本形状

```javascript
// Box - width, height, depth, widthSegments, heightSegments, depthSegments
new THREE.BoxGeometry(1, 1, 1, 1, 1, 1);

// Sphere - radius, widthSegments, heightSegments, phiStart, phiLength, thetaStart, thetaLength
new THREE.SphereGeometry(1, 32, 32);
new THREE.SphereGeometry(1, 32, 32, 0, Math.PI * 2, 0, Math.PI); // 完整球体
new THREE.SphereGeometry(1, 32, 32, 0, Math.PI); // 半球

// Cylinder - radiusTop, radiusBottom, height, radialSegments, heightSegments, openEnded
new THREE.CylinderGeometry(1, 1, 2, 32, 1, false);
new THREE.CylinderGeometry(0, 1, 2, 32); // 圆锥
```

（所有内置几何体：Box、Sphere、Plane、Circle、Cylinder、Cone、Torus、TorusKnot、Ring 等完整列表已保留）

### 高级形状

```javascript
// Capsule - radius, length, capSegments, radialSegments
// Dodecahedron, Icosahedron, Octahedron, Tetrahedron, Polyhedron
```

### 基于路径的形状

```javascript
// LatheGeometry - 通过旋转点云生成
// ExtrudeGeometry - 挤压形状
// TubeGeometry - 沿曲线生成管道
```

### 文本几何体

```javascript
import { FontLoader } from "three/examples/jsm/loaders/FontLoader.js";
import { TextGeometry } from "three/examples/jsm/geometries/TextGeometry.js";
```

## BufferGeometry

所有几何体的基类。数据以类型化数组存储，实现 GPU 高效处理。

### 自定义 BufferGeometry

```javascript
const geometry = new THREE.BufferGeometry();
// 设置顶点位置、索引、法线、UV、颜色等
```

### BufferAttribute 类型

```javascript
new THREE.BufferAttribute(array, itemSize);
// itemSize: Position=3, Normal=3, UV=2, Color=3/4, Index=1
```

### 修改 BufferGeometry

```javascript
const positions = geometry.attributes.position;
positions.setXYZ(index, x, y, z);
positions.needsUpdate = true;
geometry.computeVertexNormals();
```

## EdgesGeometry & WireframeGeometry

```javascript
const edges = new THREE.EdgesGeometry(boxGeometry, 15);
const wireframe = new THREE.WireframeGeometry(boxGeometry);
```

## Points（点云）

```javascript
const geometry = new THREE.BufferGeometry();
const positions = new Float32Array(1000 * 3);
// 填充位置数据...
const material = new THREE.PointsMaterial({ size: 0.1, color: 0xffffff });
const points = new THREE.Points(geometry, material);
scene.add(points);
```

## Lines（线条）

```javascript
const points = [new THREE.Vector3(-1, 0, 0), new THREE.Vector3(0, 1, 0), new THREE.Vector3(1, 0, 0)];
const geometry = new THREE.BufferGeometry().setFromPoints(points);
const line = new THREE.Line(geometry, new THREE.LineBasicMaterial({ color: 0xff0000 }));
```

## InstancedMesh（实例化网格）

高效渲染同一几何体的多个副本。

```javascript
const count = 1000;
const instancedMesh = new THREE.InstancedMesh(geometry, material, count);
// 设置每个实例的变换
```

## 几何体工具

```javascript
// 合并几何体
const merged = BufferGeometryUtils.mergeGeometries([geo1, geo2, geo3]);
// 计算切线（法线贴图需要）
BufferGeometryUtils.computeTangents(geometry);
```

## 常见模式

- 居中几何体：`geometry.center()`
- 缩放到适配：计算包围盒并按最大维度缩放
- 克隆和变换：`geometry.clone().rotateX(Math.PI / 2)`
- 变形目标：创建 morphPositions 并设置 `geometry.morphAttributes`

## 性能提示

1. **使用索引几何体**：通过索引复用顶点
2. **合并静态网格**：使用 `mergeGeometries` 减少绘制调用
3. **使用 InstancedMesh**：用于许多相同对象
4. **选择合适的分段数**：更多分段 = 更平滑但更慢
5. **处理未使用的几何体**：`geometry.dispose()`

## 另见

- `threejs-fundamentals` - 场景设置和 Object3D
- `threejs-materials` - 网格材质类型
- `threejs-shaders` - 自定义顶点操作
