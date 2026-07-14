# 第 3 层 — stargazed 数据驱动

## 测试内容

一个专门构建的数据驱动测试用例，用于模拟生产环境 Remotion 合成的真实形态，而不使用来自 PR #214 的运行时适配器。如果翻译通过 T3，说明技能正确处理了以下内容：

- 带有 `z.object` schema 和类型化 `defaultProps` 的 `<Composition>`
- 跨场景使用不同属性重用的自定义 React 子组件
- 物化为重复 HTML 并带有实例属性的嵌套数据结构（`stats[]`）
- 基于帧驱动的计数动画（`AnimatedNumber` → GSAP `onUpdate`）
- 两个不同的 `spring` 配置翻译为两个不同的 `back.out` 过冲
- 通过组件属性实现的实例延迟（`delayInFrames` → GSAP 时间线偏移）

## 合成结构

```
Stargazed（10 秒 @ 30 fps, 1280×720）
├── Sequence 0–3 秒   TitleScene
│                    ├── title  ← spring 缩放
│                    └── subtitle ← 线性淡入
├── Sequence 3–7 秒   StatsScene
│                    ├── StatCard "Stars" 1247 #fbbf24（延迟 0 帧）
│                    ├── StatCard "Forks" 312 #60a5fa（延迟 12 帧）
│                    └── StatCard "Issues" 48 #f87171（延迟 24 帧）
└── Sequence 7–10 秒  OutroScene
                     └── UnderlinedText "thanks for watching" ← 缩放进入下划线
```

每个 `StatCard` 是一个自定义子组件，内部使用 `AnimatedNumber` 从 0 计数到目标值。`AnimatedNumber` 本身通过 `useCurrentFrame()` + 手动 `1 - (1 - t)^3` 缓动来推导显示值。

## 有损部分（以及为什么阈值 = 0.90）

1. **`spring → back.out(N)`**：此合成中有两个不同的 spring 配置。
   - `{ damping: 12, stiffness: 100, mass: 1 }`（标题）→ `back.out(1.4)`
   - `{ damping: 14, stiffness: 90, mass: 1 }`（统计卡片）→ `back.out(1.2)`

   过冲比（1.4 vs 1.2）近似于阻尼差异。GSAP 的 back 缓动和 Remotion 的 spring 的尾部曲线不完全匹配 — 每个 spring 实例损失约 ~0.03 的平均 SSIM。

2. **计数缓动**：`AnimatedNumber` 使用 `1 - (1 - t)^3`（三次缓出）在组件中手动计算。GSAP 的 `power3.out` 是相同的曲线形状 — 应该密切匹配。两个渲染器中显示的整数每帧四舍五入；当四舍五入的值在子帧时间差上在两个数字之间切换时，会出现轻微不匹配。

3. **字体渲染**：与 T1/T2 相同的注意事项。系统 Helvetica/Arial 回退在不同渲染器之间会产生微小的抗锯齿差异。对统计卡片数字（大字重 800）影响最大。

T3 中低于 0.90 的平均 SSIM 表示_结构性_不匹配（错误的场景时长、错误的交错时间、缺少属性连接），而非近似漂移。这是我们关心的失败信号。针对 Remotion @ 4.0 使用 PNG/BT.709 输出校准的平均值为 0.953。

## 翻译演练（技能速查表）

| Remotion                                                                    | HyperFrames                                                                                |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `<Composition schema={z.object({...})} defaultProps={...} />`               | 根 `#stage` div 上的 data-\* 属性                                                          |
| 嵌套数组属性（`stats[]`）                                                   | 带每个实例 `data-*` 属性的重复 HTML 标记                                                   |
| 自定义 React 子组件                                                         | 使用组件的 prop 接口作为模板的内联重复 HTML                                                 |
| `<AnimatedNumber from={0} to={value} dur={45} />`（三次缓出计数）            | 对 `{ v: 0 }` 对象进行补间，使用 `onUpdate` 重写 `textContent`，缓动 `power3.out`          |
| `spring({damping:12, stiffness:100})`                                       | `back.out(1.4)` 约 ~0.7 秒                                                                |
| `spring({damping:14, stiffness:90})`                                        | `back.out(1.2)` 约 ~0.7 秒                                                                |
| `delayInFrames={i * 12}`（每实例）                                           | GSAP 时间线偏移 `(i * 0.4)` 秒                                                             |
| `useVideoConfig()` 获取 `fps`                                               | 丢弃 — 合成 fps 在 `#stage` 的 `data-fps` 中                                              |

## 如何渲染和评估

```bash
# 渲染 Remotion 基线（no setup.sh — 此测试用例中没有二进制资源）
cd remotion-src && npm install && npm run render

# 渲染 HyperFrames 翻译
cd ../hf-src && npx hyperframes render --output ../hf.mp4

# 比较
../../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```
