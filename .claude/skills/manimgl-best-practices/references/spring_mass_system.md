# 弹簧-质量系统 - 参考指南

**示例文件**：`examples/spring_mass_system.py`

## 用户查询场景

本示例解决如下查询：
- "创建弹簧振荡动画"
- "展示阻尼简谐运动"
- "可视化带弹簧上质量的物理模拟"
- "动画化带实时图表的弹簧-质量系统"
- "比较不同阻尼系数"

## 场景思考过程（3b1b 风格）

### 1. 识别核心概念
**阻尼简谐运动**：附着在弹簧上的质量块振荡，由于摩擦/阻尼，振幅随时间减小。方程为：`x'' = -kx - μv`

### 2. 视觉设计决策

**为什么弹簧使用参数螺旋？**
- 3D 线圈看起来更逼真
- 质量块移动时自然拉伸
- 使用 `ParametricCurve` 实现平滑渲染

**为什么在数轴上追踪位置？**
- 提供定量反馈
- 显示精确的位移值
- 容易理解运动方向

### 3. 技术实现

#### 创建自包含的物理组件
```python
class SpringMassSystem(VGroup):
    def __init__(self, x0=0, v0=0, k=3, mu=0.1, ...):
        # 存储物理状态
        self.k = k
        self.mu = mu
        self.velocity = v0

        # 添加物理更新器
        self.add_updater(lambda m, dt: m.time_step(dt))
```

**关键理解**：将物理和视觉效果封装在一个 VGroup 子类中。这使得它可复用，并保持动画代码整洁。

#### 物理积分（欧拉方法）
```python
def time_step(self, delta_t, dt_size=0.01):
    state = [self.get_x(), self.velocity]
    for _ in range(sub_steps):
        x, v = state
        acceleration = -self.k * x - self.mu * v
        state[0] += v * true_dt
        state[1] += acceleration * true_dt
```

#### 动态速度/力向量
```python
def get_velocity_vector(self, scale_factor=0.5, color=GREEN):
    vector = Vector(RIGHT, fill_color=color)
    vector.add_updater(lambda m: m.put_start_and_end_on(
        self.mass.get_center(),
        self.mass.get_center() + scale_factor * self.velocity * RIGHT
    ))
    return vector
```

### 4. 场景变体

| 场景 | 用途 |
|-------|---------|
| `SpringMassDemo` | 带速度/力向量的基本振荡 |
| `SpringWithGraph` | 使用 TracedPath 的实时 x(t) 图表 |
| `MultipleSprings` | 比较不同阻尼值 |

## 展示的关键模式

### 模式：可暂停的物理
```python
def pause(self):
    self._is_running = False

def unpause(self):
    self._is_running = True
```

### 模式：用于图表的 TracedPath
```python
tracking_point = Point()
tracking_point.add_updater(lambda p: p.move_to(
    axes.c2p(time_tracker.get_value(), spring.get_x())
))
position_graph = TracedPath(tracking_point.get_center, stroke_color=BLUE)
```

## 运行命令

```bash
# 基本演示
manimgl spring_mass_system.py SpringMassDemo -w

# 带实时图表
manimgl spring_mass_system.py SpringWithGraph -w

# 比较阻尼
manimgl spring_mass_system.py MultipleSprings -w
```
