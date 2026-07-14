---
name: threejs-geometry
description: Three.js 几何体创建 — 内置形状、BufferGeometry、自定义几何体、实例化。在创建 3D 形状、处理顶点、构建自定义网格或使用实例化渲染进行优化时使用。
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
// Box — 宽、高、深、宽度分段、高度分段、深度分段
new THREE.BoxGeometry(1, 1, 1, 1, 1, 1);

// Sphere — 半径、宽度分段、高度分段、phi 起始、phi 长度、theta 起始、theta 长度
new THREE.SphereGeometry(1, 32, 32);
new THREE.SphereGeometry(1, 32, 32, 0, Math.PI * 2, 0, Math.PI); // 完整球体
new THREE.SphereGeometry(1, 32, 32, 0, Math.PI); // 半球体

// Plane — 宽度、高度、宽度分段、高度分段
new THREE.PlaneGeometry(10, 10, 1, 1);

// Circle — 半径、分段数、theta 起始、theta 长度
new THREE.CircleGeometry(1, 32);
new THREE.CircleGeometry(1, 32, 0, Math.PI); // 半圆

// Cylinder — 顶半径、底半径、高度、径向分段、高度分段、是否开口
new THREE.CylinderGeometry(1, 1, 2, 32, 1, false);
new THREE.CylinderGeometry(0, 1, 2, 32); // 圆锥
new THREE.CylinderGeometry(1, 1, 2, 6); // 六棱柱

// Cone — 半径、高度、径向分段、高度分段、是否开口
new THREE.ConeGeometry(1, 2, 32, 1, false);

// Torus（圆环）— 半径、管径、径向分段、管状分段、弧长
new THREE.TorusGeometry(1, 0.4, 16, 100);

// TorusKnot（环形结）— 半径、管径、管状分段、径向分段、p、q
new THREE.TorusKnotGeometry(1, 0.4, 100, 16, 2, 3);

// Ring（圆环面）— 内半径、外半径、theta 分段、phi 分段
new THREE.RingGeometry(0.5, 1, 32, 1);
```

### 高级形状

```javascript
// Capsule（胶囊体）— 半径、长度、端盖分段、径向分段
new THREE.CapsuleGeometry(0.5, 1, 4, 8);

// Dodecahedron（十二面体）— 半径、细节
new THREE.DodecahedronGeometry(1, 0);

// Icosahedron（二十面体）— 半径、细节（0 = 20 面，越大越平滑）
new THREE.IcosahedronGeometry(1, 0);

// Octahedron（八面体）— 半径、细节
new THREE.OctahedronGeometry(1, 0);

// Tetrahedron（四面体）— 半径、细节
new THREE.TetrahedronGeometry(1, 0);

// Polyhedron（多面体）— 顶点、索引、半径、细节
const vertices = [1, 1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1];
const indices = [2, 1, 0, 0, 3, 2, 1, 3, 0, 2, 3, 1];
new THREE.PolyhedronGeometry(vertices, indices, 1, 0);
```

### 基于路径的形状

```javascript
// Lathe（车削几何体）— 点数组、分段数、phi 起始、phi 长度
const points = [
  new THREE.Vector2(0, 0),
  new THREE.Vector2(0.5, 0),
  new THREE.Vector2(0.5, 1),
  new THREE.Vector2(0, 1),
];
new THREE.LatheGeometry(points, 32);

// Extrude（挤压几何体）— 形状、选项
const shape = new THREE.Shape();
shape.moveTo(0, 0);
shape.lineTo(1, 0);
shape.lineTo(1, 1);
shape.lineTo(0, 1);
shape.lineTo(0, 0);

const extrudeSettings = {
  steps: 2,
  depth: 1,
  bevelEnabled: true,
  bevelThickness: 0.1,
  bevelSize: 0.1,
  bevelSegments: 3,
};
new THREE.ExtrudeGeometry(shape, extrudeSettings);

// Tube（管状几何体）— 路径、管状分段、半径、径向分段、是否闭合
const curve = new THREE.CatmullRomCurve3([
  new THREE.Vector3(-1, 0, 0),
  new THREE.Vector3(0, 1, 0),
  new THREE.Vector3(1, 0, 0),
]);
new THREE.TubeGeometry(curve, 64, 0.2, 8, false);
```

### 文本几何体

```javascript
import { FontLoader } from "three/examples/jsm/loaders/FontLoader.js";
import { TextGeometry } from "three/examples/jsm/geometries/TextGeometry.js";

const loader = new FontLoader();
loader.load("fonts/helvetiker_regular.typeface.json", (font) => {
  const geometry = new TextGeometry("Hello", {
    font: font,
    size: 1,
    depth: 0.2, // 旧版本中为 'height'
    curveSegments: 12,
    bevelEnabled: true,
    bevelThickness: 0.03,
    bevelSize: 0.02,
    bevelSegments: 5,
  });

  // 居中文本
  geometry.computeBoundingBox();
  geometry.center();

  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);
});
```

## BufferGeometry

所有几何体的基类。将数据存储为类型化数组以实现 GPU 效率。

### 自定义 BufferGeometry

```javascript
const geometry = new THREE.BufferGeometry();

// 顶点（每个顶点 3 个浮点数：x, y, z）
const vertices = new Float32Array([
  -1, -1, 0, // 顶点 0
  1, -1, 0, // 顶点 1
  1, 1, 0, // 顶点 2
  -1, 1, 0, // 顶点 3
]);
geometry.setAttribute("position", new THREE.BufferAttribute(vertices, 3));

// 索引（用于索引几何体 — 重用顶点）
const indices = new Uint16Array([
  0, 1, 2, // 三角形 1
  0, 2, 3, // 三角形 2
]);
geometry.setIndex(new THREE.BufferAttribute(indices, 1));

// 法线（光照需要）
const normals = new Float32Array([0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]);
geometry.setAttribute("normal", new THREE.BufferAttribute(normals, 3));

// UV（用于纹理）
const uvs = new Float32Array([0, 0, 1, 0, 1, 1, 0, 1]);
geometry.setAttribute("uv", new THREE.BufferAttribute(uvs, 2));

// 颜色（逐顶点颜色）
const colors = new Float32Array([
  1, 0, 0, // 红色
  0, 1, 0, // 绿色
  0, 0, 1, // 蓝色
  1, 1, 0, // 黄色
]);
geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
// 配合使用：material.vertexColors = true
```

### BufferAttribute 类型

```javascript
// 常用属性类型
new THREE.BufferAttribute(array, itemSize);

// 类型化数组选项
new Float32Array(count * itemSize); // 位置、法线、UV
new Uint16Array(count); // 索引（最多 65535 个顶点）
new Uint32Array(count); // 索引（较大网格）
new Uint8Array(count * itemSize); // 颜色（0-255 范围）

// 项目大小
// Position（位置）：3（x, y, z）
// Normal（法线）：3（x, y, z）
// UV：2（u, v）
// Color（颜色）：3（r, g, b）或 4（r, g, b, a）
// Index（索引）：1
```

### 修改 BufferGeometry

```javascript
const positions = geometry.attributes.position;

// 修改顶点
positions.setXYZ(index, x, y, z);

// 访问顶点
const x = positions.getX(index);
const y = positions.getY(index);
const z = positions.getZ(index);

// 标记需要 GPU 更新
positions.needsUpdate = true;

// 在位置变化后重新计算法线
geometry.computeVertexNormals();

// 在变化后重新计算包围盒/包围球
geometry.computeBoundingBox();
geometry.computeBoundingSphere();
```

### 交错缓冲（高级）

```javascript
// 更大网格的更高效内存布局
const interleavedBuffer = new THREE.InterleavedBuffer(
  new Float32Array([
    // pos.x, pos.y, pos.z, uv.u, uv.v（每个顶点重复）
    -1, -1, 0, 0, 0, 1, -1, 0, 1, 0, 1, 1, 0, 1, 1, -1, 1, 0, 0, 1,
  ]),
  5, // 步长（每个顶点的浮点数）
);

geometry.setAttribute(
  "position",
  new THREE.InterleavedBufferAttribute(interleavedBuffer, 3, 0),
); // 大小 3，偏移 0
geometry.setAttribute(
  "uv",
  new THREE.InterleavedBufferAttribute(interleavedBuffer, 2, 3),
); // 大小 2，偏移 3
```

## EdgesGeometry 与 WireframeGeometry

```javascript
// 边缘线（仅硬边）
const edges = new THREE.EdgesGeometry(boxGeometry, 15); // 15 = 阈值角度
const edgeMesh = new THREE.LineSegments(
  edges,
  new THREE.LineBasicMaterial({ color: 0xffffff }),
);

// 线框（所有三角形）
const wireframe = new THREE.WireframeGeometry(boxGeometry);
const wireMesh = new THREE.LineSegments(
  wireframe,
  new THREE.LineBasicMaterial({ color: 0xffffff }),
);
```

## 点云

```javascript
// 创建点云
const geometry = new THREE.BufferGeometry();
const positions = new Float32Array(1000 * 3);

for (let i = 0; i < 1000; i++) {
  positions[i * 3] = (Math.random() - 0.5) * 10;
  positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
  positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
}

geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

const material = new THREE.PointsMaterial({
  size: 0.1,
  sizeAttenuation: true, // 大小随距离减小
  color: 0xffffff,
});

const points = new THREE.Points(geometry, material);
scene.add(points);
```

## 线条

```javascript
// Line（连接的线段）
const points = [
  new THREE.Vector3(-1, 0, 0),
  new THREE.Vector3(0, 1, 0),
  new THREE.Vector3(1, 0, 0),
];
const geometry = new THREE.BufferGeometry().setFromPoints(points);
const line = new THREE.Line(
  geometry,
  new THREE.LineBasicMaterial({ color: 0xff0000 }),
);

// LineLoop（闭合环）
const loop = new THREE.LineLoop(geometry, material);

// LineSegments（线段对）
const segmentsGeometry = new THREE.BufferGeometry();
segmentsGeometry.setAttribute(
  "position",
  new THREE.BufferAttribute(
    new Float32Array([
      -1, 0, 0, 0, 1, 0, // 线段 1
      0, 1, 0, 1, 0, 0, // 线段 2
    ]),
    3,
  ),
);
const segments = new THREE.LineSegments(segmentsGeometry, material);
```

## InstancedMesh（实例化网格）

高效渲染同一几何体的多个副本。

```javascript
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const count = 1000;

const instancedMesh = new THREE.InstancedMesh(geometry, material, count);

// 设置每个实例的变换
const dummy = new THREE.Object3D();
const matrix = new THREE.Matrix4();

for (let i = 0; i < count; i++) {
  dummy.position.set(
    (Math.random() - 0.5) * 20,
    (Math.random() - 0.5) * 20,
    (Math.random() - 0.5) * 20,
  );
  dummy.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
  dummy.scale.setScalar(0.5 + Math.random());
  dummy.updateMatrix();

  instancedMesh.setMatrixAt(i, dummy.matrix);
}

// 标记需要 GPU 更新
instancedMesh.instanceMatrix.needsUpdate = true;

// 可选：逐实例颜色
instancedMesh.instanceColor = new THREE.InstancedBufferAttribute(
  new Float32Array(count * 3),
  3,
);
for (let i = 0; i < count; i++) {
  instancedMesh.setColorAt(
    i,
    new THREE.Color(Math.random(), Math.random(), Math.random()),
  );
}
instancedMesh.instanceColor.needsUpdate = true;

scene.add(instancedMesh);
```

### 运行时更新实例

```javascript
// 更新单个实例
const matrix = new THREE.Matrix4();
instancedMesh.getMatrixAt(index, matrix);
// 修改矩阵...
instancedMesh.setMatrixAt(index, matrix);
instancedMesh.instanceMatrix.needsUpdate = true;

// 对实例化网格进行光线投射
const intersects = raycaster.intersectObject(instancedMesh);
if (intersects.length > 0) {
  const instanceId = intersects[0].instanceId;
}
```

## InstancedBufferGeometry（高级）

用于自定义超越变换/颜色的逐实例属性。

```javascript
const geometry = new THREE.InstancedBufferGeometry();
geometry.copy(new THREE.BoxGeometry(1, 1, 1));

// 添加逐实例属性
const offsets = new Float32Array(count * 3);
for (let i = 0; i < count; i++) {
  offsets[i * 3] = Math.random() * 10;
  offsets[i * 3 + 1] = Math.random() * 10;
  offsets[i * 3 + 2] = Math.random() * 10;
}
geometry.setAttribute("offset", new THREE.InstancedBufferAttribute(offsets, 3));

// 在着色器中使用
// attribute vec3 offset;
// vec3 transformed = position + offset;
```

## 几何体工具

```javascript
import * as BufferGeometryUtils from "three/examples/jsm/utils/BufferGeometryUtils.js";

// 合并几何体（必须具有相同属性）
const merged = BufferGeometryUtils.mergeGeometries([geo1, geo2, geo3]);

// 带组的合并（用于多材质）
const merged = BufferGeometryUtils.mergeGeometries([geo1, geo2], true);

// 计算切线（法线贴图需要）
BufferGeometryUtils.computeTangents(geometry);

// 交错属性以获得更好性能
const interleaved = BufferGeometryUtils.interleaveAttributes([
  geometry.attributes.position,
  geometry.attributes.normal,
  geometry.attributes.uv,
]);
```

## 常用模式

### 居中几何体

```javascript
geometry.computeBoundingBox();
geometry.center(); // 移动顶点使中心在原点
```

### 缩放适配

```javascript
geometry.computeBoundingBox();
const size = new THREE.Vector3();
geometry.boundingBox.getSize(size);
const maxDim = Math.max(size.x, size.y, size.z);
geometry.scale(1 / maxDim, 1 / maxDim, 1 / maxDim);
```

### 克隆和变换

```javascript
const clone = geometry.clone();
clone.rotateX(Math.PI / 2);
clone.translate(0, 1, 0);
clone.scale(2, 2, 2);
```

### 形态目标

```javascript
// 基础几何体
const geometry = new THREE.BoxGeometry(1, 1, 1, 4, 4, 4);

// 创建形态目标
const morphPositions = geometry.attributes.position.array.slice();
for (let i = 0; i < morphPositions.length; i += 3) {
  morphPositions[i] *= 2; // 缩放 X
  morphPositions[i + 1] *= 0.5; // 挤压 Y
}

geometry.morphAttributes.position = [
  new THREE.BufferAttribute(new Float32Array(morphPositions), 3),
];

const mesh = new THREE.Mesh(geometry, material);
mesh.morphTargetInfluences[0] = 0.5; // 50% 混合
```

## 性能提示

1. **使用索引几何体**：通过索引重用顶点
2. **合并静态网格**：使用 `mergeGeometries` 减少绘制调用
3. **使用 InstancedMesh**：适用于许多相同对象
4. **选择合适的分段数**：更多分段 = 更平滑但更慢
5. **释放未使用的几何体**：`geometry.dispose()`

```javascript
// 常用分段数参考
new THREE.SphereGeometry(1, 32, 32); // 良好质量
new THREE.SphereGeometry(1, 64, 64); // 高质量
new THREE.SphereGeometry(1, 16, 16); // 性能模式

// 使用完毕后释放
geometry.dispose();
```

## 另请参阅

- `threejs-fundamentals` — 场景设置和 Object3D
- `threejs-materials` — 网格的材质类型
- `threejs-shaders` — 自定义顶点操作
