# 视差星空 - 参考指南

**示例文件：** `examples/parallax_starfield.py`

## 用户查询场景

此示例可回答如下问题：
- "展示视差如何与星星一起工作"
- "创建演示深度感知的3D场景"
- "制作观察者穿越星空的动画"
- "直观解释恒星视差"
- "展示为什么移动时近处物体比远处物体移动更多"

## 场景思考过程（3b1b风格）

### 1. 确定核心概念
**视差**：当观察者移动时，近处物体相对于背景的移动比远处物体更大。这就是天文学家测量附近恒星距离的方法。

### 2. 视觉设计决策

**为什么用星星/点而不是复杂对象？**
- 星星天然存在于不同距离
- 点计算效率高（GlowDots轻松处理200+）
- 效果清晰，不受物体形状干扰

**为什么用参考立方体？**
- 提供3D空间上下文
- 帮助观众理解星星存在的体积范围
- 线框不会遮挡星星

**为什么用Pi生物作为观察者？**
- 使场景更具代入感——你在看着某人观察
- 他们的移动直观易懂
- 可以用`observer.change("pondering")`展示反应

### 3. 技术实现

#### GlowDots用于高效星体渲染
```python
# 随机3D位置
star_positions = np.random.uniform(-1, 1, (n_stars, 3))
stars = GlowDots(star_positions)
stars.set_glow_factor(2)  # 柔和发光效果
stars.set_radii(np.random.uniform(0, 0.075, n_stars))  # 不同大小
```

**关键洞察**：`GlowDots`比创建单个`Dot`对象高效得多。对于200+个点，这是必要的。

#### 3D相机控制
```python
frame = self.frame
self.set_floor_plane("xz")  # Z轴现在垂直

# 平滑相机重定向
self.play(frame.animate.reorient(-40, -26, 0), run_time=2)
```

**为什么用`set_floor_plane("xz")`？**在天文可视化中，我们通常希望Z轴作为垂直轴。此调用重新配置坐标系。

#### 观察者移动模式
```python
for dy in [1.5, -3, 3, -3, 1.5]:
    self.play(observer.animate.shift(dy * IN), run_time=3)
```

**为什么是这个特定模式？**
- `[1.5, -3, 3, -3, 1.5]` 创建：上 → 下 → 上 → 下 → 中心
- 观众看到视差偏移的完整范围
- 回到起始位置以便需要时干净地循环

### 4. 场景变体

示例包含三个变体，展示逐步递进的复杂性：

| 场景 | 用途 | 何时使用 |
|-------|---------|-------------|
| `ParallaxStarfield` | 基本效果，第三人称视角 | 一般解释 |
| `ParallaxFromObserverPOV` | 第一人称视角 | "你会看到什么？" |
| `LayeredParallax` | 明确的分层距离 | 清晰教授概念 |

## 演示的关键模式

### 模式：帧跟随对象
```python
frame.always.match_z(observer)
```
相机的Z位置持续匹配观察者，创造第一人称视角。

### 模式：分层深度以增强清晰度
```python
colors = [RED, YELLOW, BLUE]
distances = [2, 5, 10]
```
在特定距离使用不同颜色使视差效果对教学目的而言无可辩驳地清晰。

### 模式：平滑横向移动
```python
self.play(
    observer.animate.shift(dx * RIGHT),
    run_time=3,
    rate_func=smooth
)
```
缓慢平滑的运动让观众追踪单个星星并观察效果。

## 常见修改

### 添加更多星星
```python
n_stars = 500  # 增加数量
stars.set_radii(np.random.uniform(0, 0.05, n_stars))  # 更小的半径以适应密度
```

### 不同星色
```python
# 基于温度的星色
colors = [RED, ORANGE, YELLOW, WHITE, BLUE_A]
for i, star in enumerate(stars):
    star.set_color(random.choice(colors))
```

### 添加背景星系
```python
background = ImageMobject("milky_way.png")
background.set_height(20)
background.shift(50 * OUT)  # 远在星星后方
self.add(background)
```

## 输出

渲染后将产生：
- 蓝色线框立方体内的3D星空
- 上下移动的观察者（Randolph）
- 星星根据距离不同而表现出的不同偏移
- 对视差原理的清晰演示

## 运行命令

```bash
# 完整渲染
manimgl parallax_starfield.py ParallaxStarfield -w

# 预览（不输出文件）
manimgl parallax_starfield.py ParallaxStarfield -p

# 所有三个场景
manimgl parallax_starfield.py ParallaxStarfield ParallaxFromObserverPOV LayeredParallax -w
```
