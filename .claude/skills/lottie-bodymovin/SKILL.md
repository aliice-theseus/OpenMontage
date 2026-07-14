---
name: lottie-bodymovin
description: 使用从 After Effects 导出的 Lottie 动画实现迪士尼 12 项动画原则时使用
---

# Lottie 动画原则

使用 Lottie（Bodymovin）为矢量动画实现所有 12 项迪士尼动画原则。

## 1. 挤压与拉伸（Squash and Stretch）

在导出前的 After Effects 中：
- 反向动画缩放 X 和 Y
- 使用表达式：`s = transform.scale[1]; [100 + (100-s), s]`

```javascript
// 运行时控制
lottie.setSpeed(1.5); // 影响挤压时序
```

## 2. 预备动作（Anticipation）

在 AE 中构建你的合成：
1. **帧 0-10**：蓄力姿势
2. **帧 10-40**：主要动作
3. **帧 40-50**：稳定

```javascript
// 播放预备段落
anim.playSegments([0, 10], true);
setTimeout(() => anim.playSegments([10, 50], true), 200);
```

## 3. 演出布局（Staging）

```javascript
// 分层多个 Lottie 动画
<div className="scene">
  <Lottie animationData={background} style={{ opacity: 0.6 }} />
  <Lottie animationData={hero} style={{ zIndex: 10 }} />
</div>
```

## 4. 连续动作与关键姿势（Straight Ahead / Pose to Pose）

AE 中的关键姿势：
- 在关键姿势处设置关键帧
- 让 AE 在关键帧之间插值
- 使用 Easy Ease 使运动平滑

```javascript
// 跳转到特定姿势
anim.goToAndStop(25, true); // 第 25 帧
```

## 5. 跟随与重叠动作（Follow Through and Overlapping Action）

在 After Effects 中：
- 将子图层关键帧偏移 2-4 帧
- 使用带延迟表达的父子关系
- `thisComp.layer("Parent").transform.position.valueAtTime(time - 0.05)`

## 6. 慢入慢出（Slow In and Slow Out）

AE 关键帧设置：
- 选择关键帧 > Easy Ease（F9）
- 使用图表编辑器调整曲线
- 贝塞尔手柄控制加速

```javascript
// 动态调整播放速度
anim.setSpeed(0.5); // 更慢
anim.setSpeed(2); // 更快
```

## 7. 弧线运动（Arc）

在 After Effects 中：
- 使用运动路径（位置属性）
- 将关键帧转换为贝塞尔曲线
- 拉动手柄创建弧线
- 或使用"自动定向到路径"

## 8. 次要动作（Secondary Action）

```javascript
// 触发次要动画
mainAnim.addEventListener('complete', () => {
  secondaryAnim.play();
});

// 或与帧同步
mainAnim.addEventListener('enterFrame', (e) => {
  if (e.currentTime > 15) particleAnim.play();
});
```

## 9. 时间节奏（Timing）

```javascript
anim.setSpeed(0.5);  // 半速 - 戏剧化
anim.setSpeed(1);    // 正常
anim.setSpeed(2);    // 双倍速度 - 干脆

// 或在 AE 导出中控制帧率
// 24fps = 电影感，30fps = 流畅，60fps = 丝滑
```

## 10. 夸张表现（Exaggeration）

在 After Effects 中：
- 将缩放推到 100% 以上（120-150%）
- 过度旋转
- 使用超调表达式
- `amp = 15; freq = 3; decay = 5; n = 0; time_start = key(1).time; if (time > time_start) { n = (time - time_start) / thisComp.frameDuration; amp * Math.sin(freq*n) / Math.exp(decay*n/100); } else { 0; }`

## 11. 扎实绘画（Solid Drawing）

在 After Effects 中：
- 使用 3D 图层
- 应用透视摄像机
- 动画 Z 轴位置和旋转
- 使用景深

## 12. 吸引力（Appeal）

AE 中的设计原则：
- 流畅曲线优于尖锐角度
- 一致的时间模式
- 令人愉悦的调色板
- 清晰的矢量形状

```javascript
// 带悬停效果的 React Lottie
<Lottie
  animationData={data}
  onMouseEnter={() => anim.setDirection(1)}
  onMouseLeave={() => anim.setDirection(-1)}
/>
```

## Lottie 实现

```javascript
import Lottie from 'lottie-react';
import animationData from './animation.json';

<Lottie
  animationData={animationData}
  loop={true}
  autoplay={true}
  style={{ width: 200, height: 200 }}
/>
```

## 关键 Lottie 功能

- `playSegments([start, end])` - 播放帧范围
- `setSpeed(n)` - 控制时间
- `setDirection(1/-1)` - 正向/反向
- `goToAndStop(frame)` - 姿势控制
- `addEventListener` - 帧事件
- 通过 `lottie-interactivity` 实现交互性
