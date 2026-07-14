# 向量场 - 参考指南

**示例文件：** `examples/vector_fields.py`

## 用户查询场景

此示例可回答如下问题：
- "创建向量场可视化"
- "展示粒子在场中流动"
- "可视化电荷产生的电场"
- "制作梯度下降动画"
- "展示流体流动"

## 场景思考过程（3b1b风格）

### 1. 核心概念
**向量场**：空间中每个点都有一个向量指示方向和大小。粒子跟随场，揭示流动模式。

### 2. 技术实现

#### 手动箭头场（可移植方法）
```python
arrows = VGroup()
for x in np.arange(-3.5, 4, 0.7):
    for y in np.arange(-2.5, 3, 0.7):
        vx, vy = -y * 0.15, x * 0.15  # 旋转场
        arrow = Arrow(
            start=[x, y, 0],
            end=[x + vx, y + vy, 0],
            buff=0,
            stroke_width=2,
        )
        # 按大小着色
        mag = np.sqrt(vx**2 + vy**2)
        arrow.set_color(interpolate_color(BLUE, YELLOW, mag / 0.5))
        arrows.add(arrow)
```

#### 粒子跟随场
```python
def follow_field(mob, dt):
    x, y = mob.get_center()[:2]
    vx, vy = field_func(x, y)
    mob.shift(np.array([vx, vy, 0]) * dt)

dot.add_updater(follow_field)
trail = TracedPath(dot.get_center, stroke_color=RED)
```

#### 电偶极子场
```python
def E_field(pos):
    r1, r2 = pos - q1_pos, pos - q2_pos
    d1, d2 = np.linalg.norm(r1), np.linalg.norm(r2)
    E1 = r1 / d1**3   # 来自+电荷
    E2 = -r2 / d2**3  # 来自-电荷
    return E1 + E2
```

### 3. 场景变体

| 场景 | 用途 |
|-------|---------|
| `SimpleVectorField` | 带粒子的旋转场 |
| `GradientFieldDemo` | 标量场 + 梯度箭头 |
| `ParticleFlow` | 涡旋中的多个粒子 |
| `ElectricDipole` | 正/负电荷的场 |

## 关键模式

### 模式：按大小着色
```python
mag = np.linalg.norm([vx, vy])
color = interpolate_color(BLUE, YELLOW, min(mag * scale, 1))
arrow.set_color(color)
```

### 模式：对多个箭头使用LaggedStartMap
```python
self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.02, run_time=2))
```

### 模式：循环中Updater的闭包
```python
for i in range(n):
    dot = Dot(...)
    def make_updater():  # 闭包捕获当前状态
        def update(mob, dt):
            # 使用mob，而不是dot
            ...
        return update
    dot.add_updater(make_updater())
```

## 运行命令

```bash
manimgl vector_fields.py SimpleVectorField -w
manimgl vector_fields.py GradientFieldDemo -w
manimgl vector_fields.py ParticleFlow -w
manimgl vector_fields.py ElectricDipole -w
```
