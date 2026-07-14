# 旋转指数 - 参考指南

**示例文件**：`examples/rotating_exponentials.py`

## 用户查询场景

本示例解决如下查询：
- "在复平面上可视化 e^(it)"
- "展示欧拉公式动画"
- "演示余弦如何从旋转指数产生"
- "创建带旋转向量的复平面"
- "直观展示 e^(iπ) = -1"

## 场景思考过程（3b1b 风格）

### 1. 核心概念
**欧拉公式**：`e^(it) = cos(t) + i·sin(t)` — 复平面上的旋转单位向量。两个反向旋转的指数之和等于实数余弦。

### 2. 视觉设计决策

**为什么使用 ComplexPlane？**
- 复数的自然坐标系
- 内置网格和标签
- `n2p()` 方法将复数转换为点

**为什么展示追踪路径？**
- 揭示单位圆自然产生
- 显示角度和位置之间的关系

### 3. 技术实现

#### 带 TracedPath 的旋转向量
```python
time_tracker = ValueTracker(0)

vector = Vector(RIGHT, color=YELLOW)
vector.add_updater(lambda v: v.put_start_and_end_on(
    ORIGIN,
    plane.n2p(np.exp(1j * time_tracker.get_value()))
))

tip_dot = Dot(color=YELLOW)
tip_dot.add_updater(lambda d: d.move_to(vector.get_end()))

traced = TracedPath(tip_dot.get_center, stroke_color=BLUE)
```

#### 余弦的反向旋转
```python
# e^(it) 逆时针旋转
v1.add_updater(lambda v: v.put_start_and_end_on(
    ORIGIN, plane.n2p(np.exp(1j * t))
))
# e^(-it) 顺时针旋转
v2.add_updater(lambda v: v.put_start_and_end_on(
    ORIGIN, plane.n2p(np.exp(-1j * t))
))
# 和始终为实数：2cos(t)
```

### 4. 场景变体

| 场景 | 用途 |
|-------|---------|
| `RotatingExponential` | 基本 e^(it) 可视化 |
| `CounterRotatingExponentials` | 展示 e^(it) + e^(-it) = 2cos(t) |
| `EulersFormula` | 著名的 e^(iπ) = -1 |
| `ComplexExponentialSpiral` | 衰减螺旋 e^((a+bi)t) |

## 关键模式

### 模式：用于弧线的 always_redraw
```python
angle_arc = always_redraw(lambda: Arc(
    start_angle=0,
    angle=time_tracker.get_value() % TAU,
    radius=0.3,
    color=GREEN
))
```

### 模式：复数到点的转换
```python
# 使用 ComplexPlane.n2p()（数字到点）
point = plane.n2p(1 + 2j)  # 复数
point = plane.n2p(np.exp(1j * theta))  # 欧拉形式
```

## 运行命令

```bash
manimgl rotating_exponentials.py RotatingExponential -w
manimgl rotating_exponentials.py CounterRotatingExponentials -w
manimgl rotating_exponentials.py EulersFormula -w
manimgl rotating_exponentials.py ComplexExponentialSpiral -w
```
