# 3D曲面 - 参考指南

**示例文件：** `examples/three_d_surfaces.py`

## 用户查询场景

此示例可回答如下问题：
- "创建3D曲面可视化"
- "展示参数曲面"
- "制作相机绕物体旋转的动画"
- "创建环面/球体/圆锥"
- "展示马鞍面"

## 场景思考过程（3b1b风格）

### 1. 核心概念
**参数曲面**：将曲面定义为函数 (u,v) → (x,y,z)。相机运动可揭示3D结构。

### 2. 技术实现

#### 基本参数曲面
```python
surface = ParametricSurface(
    lambda u, v: [u, v, np.sin(u) * np.cos(v)],
    u_range=(-3, 3),
    v_range=(-3, 3),
    resolution=(30, 30),
)
surface.set_color(BLUE)
surface.set_opacity(0.8)
```

#### 相机设置与运动
```python
frame = self.frame
frame.reorient(-30, 70, 0)  # phi, theta, gamma
frame.set_height(10)

# 动画化相机
self.play(frame.animate.reorient(30, 60, 0), run_time=3)
```

#### 带经纬线的球体
```python
# 纬线
for phi in np.linspace(-PI/2 + 0.3, PI/2 - 0.3, 6):
    line = ParametricCurve(
        lambda t: radius * np.array([
            np.cos(t) * np.cos(phi),
            np.sin(t) * np.cos(phi),
            np.sin(phi)
        ]),
        t_range=(0, TAU),
    )
```

#### 环面参数化
```python
R, r = 2, 0.7  # 主半径和副半径
torus = ParametricSurface(
    lambda u, v: [
        (R + r * np.cos(v)) * np.cos(u),
        (R + r * np.cos(v)) * np.sin(u),
        r * np.sin(v)
    ],
    u_range=(0, TAU),
    v_range=(0, TAU),
)
```

### 3. 场景变体

| 场景 | 用途 |
|-------|---------|
| `ParametricSurface3D` | z = sin(x)cos(y) 带相机轨道 |
| `SphereSurface` | 带网格线的旋转球体 |
| `ConeUnfolding` | 3D圆锥可视化 |
| `SaddleSurface` | z = x² - y² 带截面 |
| `TorusSurface` | 带旋转的甜甜圈形状 |

## 关键模式

### 模式：ThreeDAxes
```python
axes = ThreeDAxes(
    x_range=(-3, 3, 1),
    y_range=(-3, 3, 1),
    z_range=(-2, 2, 1),
)
```

### 模式：旋转对象
```python
self.play(
    Rotate(surface, TAU, axis=UP, run_time=6, rate_func=linear),
)
```

### 模式：帧重定向
```python
# reorient(phi, theta, gamma, center, height)
frame.reorient(-30, 70, 0)  # 仅角度
frame.animate.reorient(60, 60, 0)  # 动画化
```

## 运行命令

```bash
manimgl three_d_surfaces.py ParametricSurface3D -w
manimgl three_d_surfaces.py SphereSurface -w
manimgl three_d_surfaces.py TorusSurface -w
manimgl three_d_surfaces.py SaddleSurface -w
```
