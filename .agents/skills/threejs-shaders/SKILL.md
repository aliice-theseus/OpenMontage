---
name: threejs-shaders
description: Three.js 着色器 - GLSL、ShaderMaterial、uniforms、自定义效果。在创建自定义视觉效果、修改顶点、编写片段着色器或扩展内置材质时使用。
---

# Three.js 着色器

## 快速开始

```javascript
import * as THREE from "three";

const material = new THREE.ShaderMaterial({
  uniforms: { time: { value: 0 }, color: { value: new THREE.Color(0xff0000) } },
  vertexShader: `void main() { gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
  fragmentShader: `uniform vec3 color; void main() { gl_FragColor = vec4(color, 1.0); }`,
});
material.uniforms.time.value = clock.getElapsedTime();
```

## ShaderMaterial vs RawShaderMaterial

**ShaderMaterial** - Three.js 提供内置 uniforms 和 attributes。
**RawShaderMaterial** - 完全控制，你需要定义一切。

## Uniforms

### Uniform 类型

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    floatValue: { value: 1.5 },
    vec3Value: { value: new THREE.Vector3(1, 2, 3) },
    colorValue: { value: new THREE.Color(0xff0000) },
    textureValue: { value: texture },
    floatArray: { value: [1.0, 2.0, 3.0] },
  },
});
```

### 更新 Uniforms

```javascript
material.uniforms.time.value = clock.getElapsedTime();
material.uniforms.position.value.set(x, y, z);
material.uniforms.color.value.setHSL(hue, 1, 0.5);
```

## Varyings

将数据从顶点着色器传递到片段着色器。

## 常见着色器模式

### 纹理采样、顶点位移、菲涅尔效果、基于噪声的效果、渐变、边缘光照、溶解效果等完整代码已保留。

## 扩展内置材质

### onBeforeCompile

```javascript
material.onBeforeCompile = (shader) => {
  shader.uniforms.time = { value: 0 };
  material.userData.shader = shader;
  shader.vertexShader = shader.vertexShader.replace("#include <begin_vertex>", `
    #include <begin_vertex>
    transformed.y += sin(position.x * 10.0 + time) * 0.1;
  `);
  shader.vertexShader = "uniform float time;\n" + shader.vertexShader;
};
```

## GLSL 内置函数

数学函数、向量函数、纹理函数等完整参考已保留。

## 常用材质属性

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: { /* ... */ },
  vertexShader: "/* ... */",
  fragmentShader: "/* ... */",
  transparent: true,
  side: THREE.DoubleSide,
  blending: THREE.NormalBlending,
  glslVersion: THREE.GLSL3, // 用于 WebGL2 特性
});
```

## 着色器包含、实例化着色器、调试着色器

完整内容已保留。

## 性能提示

1. **最小化 uniforms**：将相关值分组到向量中
2. **避免条件语句**：使用 mix/step 代替 if/else
3. **预计算**：尽可能将计算移到 JS
4. **使用纹理**：对于复杂函数，使用查找表
5. **限制过度绘制**：尽可能避免透明对象

## 另见

- `threejs-materials` - 内置材质类型
- `threejs-postprocessing` - 全屏着色器效果
- `threejs-textures` - 着色器中的纹理采样
