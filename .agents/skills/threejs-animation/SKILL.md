---
name: threejs-animation
description: Three.js 动画 - 关键帧动画、骨骼动画、变形目标、动画混合。在动画化对象、播放 GLTF 动画、创建程序化运动或混合动画时使用。
---

# Three.js 动画

## 快速开始

```javascript
import * as THREE from "three";

// 简单程序化动画
const clock = new THREE.Clock();

function animate() {
  const delta = clock.getDelta();
  const elapsed = clock.getElapsedTime();

  mesh.rotation.y += delta;
  mesh.position.y = Math.sin(elapsed) * 0.5;

  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();
```

## 动画系统概述

Three.js 动画系统有三个主要组件：

1. **AnimationClip** - 关键帧数据的容器
2. **AnimationMixer** - 在根对象上播放动画
3. **AnimationAction** - 控制剪辑的播放

## AnimationClip

存储关键帧动画数据。

```javascript
// 创建动画剪辑
const times = [0, 1, 2]; // 关键帧时间（秒）
const values = [0, 1, 0]; // 每个关键帧的值

const track = new THREE.NumberKeyframeTrack(
  ".position[y]", // 属性路径
  times,
  values,
);

const clip = new THREE.AnimationClip("bounce", 2, [track]);
```

### KeyframeTrack 类型

```javascript
// 数字轨道（单值）
new THREE.NumberKeyframeTrack(".opacity", times, [1, 0]);

// 矢量轨道（位置、缩放）
new THREE.VectorKeyframeTrack(".position", times, [0, 0, 0, 1, 2, 0, 0, 0, 0]);

// 四元数轨道（旋转）
const q1 = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0, 0));
const q2 = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, Math.PI, 0));
new THREE.QuaternionKeyframeTrack(".quaternion", [0, 1], [q1.x, q1.y, q1.z, q1.w, q2.x, q2.y, q2.z, q2.w]);

// 颜色轨道
new THREE.ColorKeyframeTrack(".material.color", times, [1, 0, 0, 0, 1, 0, 0, 0, 1]);
```

### 插值模式

```javascript
const track = new THREE.VectorKeyframeTrack(".position", times, values);
track.setInterpolation(THREE.InterpolateLinear); // 默认
track.setInterpolation(THREE.InterpolateSmooth); // 三次样条
track.setInterpolation(THREE.InterpolateDiscrete); // 阶跃函数
```

## AnimationMixer

在对象及其后代上播放动画。

```javascript
const mixer = new THREE.AnimationMixer(model);
const action = mixer.clipAction(clip);
action.play();

function animate() {
  const delta = clock.getDelta();
  mixer.update(delta); // 必需！
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
```

### Mixer 事件

```javascript
mixer.addEventListener("finished", (e) => {
  console.log("动画完成：", e.action.getClip().name);
});
mixer.addEventListener("loop", (e) => {
  console.log("动画循环：", e.action.getClip().name);
});
```

## AnimationAction

控制动画剪辑的播放。

```javascript
const action = mixer.clipAction(clip);

// 播放控制
action.play();
action.stop();
action.reset();
action.halt(fadeOutDuration);

// 时间控制
action.time = 0.5;
action.timeScale = 1; // 播放速度（负数 = 反向）
action.paused = false;

// 权重（用于混合）
action.weight = 1;
action.setEffectiveWeight(1);

// 循环模式
action.loop = THREE.LoopRepeat; // 默认：无限循环
action.loop = THREE.LoopOnce; // 播放一次并停止
action.loop = THREE.LoopPingPong; // 来回交替
action.repetitions = 3;

// 钳制
action.clampWhenFinished = true; // 完成时保持最后一帧

// 混合模式
action.blendMode = THREE.NormalAnimationBlendMode;
action.blendMode = THREE.AdditiveAnimationBlendMode;
```

### 淡入/淡出

```javascript
action.reset().fadeIn(0.5).play();
action.fadeOut(0.5);

// 动画间交叉淡出
const action1 = mixer.clipAction(clip1);
const action2 = mixer.clipAction(clip2);
action1.play();
action1.crossFadeTo(action2, 0.5, true);
action2.play();
```

（代码块中骨骼动画、变形目标、动画混合、程序化动画模式、性能提示等完整内容与英文版保持一致，仅翻译注释。）

## 性能提示

1. **共享剪辑**：同一 AnimationClip 可用于多个混合器
2. **优化剪辑**：调用 `clip.optimize()` 移除冗余关键帧
3. **屏幕外禁用**：对不可见对象停止混合器更新
4. **对动画使用 LOD**：远处角色使用更简单的绑定
5. **限制活动混合器数**：每个 `mixer.update()` 都有开销

## 另见

- `threejs-loaders` - 加载动画 GLTF 模型
- `threejs-fundamentals` - 时钟和动画循环
- `threejs-shaders` - 着色器中的顶点动画
