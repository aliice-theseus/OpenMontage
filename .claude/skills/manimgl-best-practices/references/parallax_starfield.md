# 视差星场 - 参考指南

**示例文件**：`examples/parallax_starfield.py`

## 用户查询场景

本示例解决如下查询：
- "展示视差如何与星体一起工作"
- "创建演示深度感知的 3D 场景"
- "动画化观察者穿过星场"
- "直观解释恒星视差"
- "展示为什么移动时近处物体比远处物体移动更多"

## 场景思考过程（3b1b 风格）

### 1. 识别核心概念
**视差**：当观察者移动时，近处物体相对于背景似乎比远处物体移动更多。这就是天文学家如何测量附近恒星的距离。

### 2. 视觉设计决策

**为什么使用星星/圆点而不是复杂对象？**
- 星星天然存在于不同距离
- 圆点在计算上高效（GlowDots 轻松处理 200+）
- 没有对象形状的干扰，效果清晰

**为什么使用参考立方体？**
- 在 3D 中提供空间上下文
- 帮助观众理解星星存在的体积
- 线框不会遮挡星星

**为什么使用 Pi 角色作为观察者？**
- 使场景有代入感 — 观众看到有人在观察
- 他们的移动直观易懂
- 可以用 `observer.change("pondering")` 展示反应

### 3. 技术实现

#### 用于高效星星渲染的 GlowDots
```python
# 随机 3D 位置
star_positions = np.random.uniform(-1, 1, (n_stars, 3))
stars = GlowDots(star_positions)
stars.set_glow_factor(2)  # 柔和辉光效果
stars.set_radii(np.random.uniform(0, 0.075, n_stars))  # 不同大小
```

**关键理解**：`GlowDots` 比创建单个 `Dot` 对象高效得多。对于 200+ 个点，这至关重要。

#### 3D 相机控制
```python
frame = self.frame
self.set_floor_plane("xz")  # Z 现在为垂直轴

# 平滑相机重新定向
self.play(frame.animate.reorient(-40, -26, 0), run_time=2)
```

**为什么使用 `set_floor_plane("xz")`？** 在天文可视化中，我们通常希望 Z 作为垂直轴。这个调用重新配置了坐标系。

#### 观察者移动模式
```python
for dy in [1.5, -3, 3, -3, 1.5]:
    self.play(observer.animate.shift(dy * IN), run_time=3)
```

**为什么是这个特定模式？**
- `[1.5, -3, 3, -3, 1.5]` 产生：向上 → 向下 → 向上 → 向下 → 中间
- 观众看到完整的视差位移范围
- 返回起始位置，如需可干净循环

### 4. 场景变体

示例包含三个变体，展示渐进复杂性：

| 场景 | 用途 | 何时使用 |
|-------|---------|-------------|
| `ParallaxStarfield` | 基本效果，第三人称视角 | 一般性解释 |
| `ParallaxFromObserverPOV` | 第一人称视角 | "你会看到什么？" |
| `LayeredParallax` | 显式距离分层 | 清晰教授概念 |

## 展示的关键模式

### 模式：框架跟随对象
```python
frame.always.match_z(observer)
```
相机的 Z 位置持续匹配观察者，创建第一人称视角。

### 模式：分层深度以求清晰
```python
colors = [RED, YELLOW, BLUE]
distances = [2, 5, 10]
```
在特定距离使用不同的颜色，使教育目的的视差效果清晰无误。

### 模式：平滑横向移动
```python
self.play(
    observer.animate.shift(dx * RIGHT),
    run_time=3,
    rate_func=smooth
)
```
缓慢平滑的移动让观众追踪单个星星并观察效果。

## 常见修改

### 添加更多星星
```python
n_stars = 500  # 增加数量
stars.set_radii(np.random.uniform(0, 0.05, n_stars))  # 密度大时半径小
```

### 不同的星星颜色
```python
# 基于温度的星星颜色
colors = [RED, ORANGE, YELLOW, WHITE, BLUE_A]
for i, star in enumerate(stars):
    star.set_color(random.choice(colors))
```

### 添加背景星系
```python
background = ImageMobject("milky_way.png")
background.set_height(20)
background.shift(50 * OUT)  # 远在星星之后
self.add(background)
```

## 输出

渲染后，将产生：
- 蓝色线框立方体内的 3D 星场
- 上下移动的观察者（Randolph）
- 基于距离不同位移量的星星
- 视差原理的清晰演示

## 运行命令

```bash
# 完整渲染
manimgl parallax_starfield.py ParallaxStarfield -w

# 预览（无文件输出）
manimgl parallax_starfield.py ParallaxStarfield -p

# 所有三个场景
manimgl parallax_starfield.py ParallaxStarfield ParallaxFromObserverPOV LayeredParallax -w
```
