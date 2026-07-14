# 过渡动画翻译：@remotion/transitions → HF 交叉淡入淡出 / 着色器过渡

`@remotion/transitions` 包是 Remotion 的预建场景间过渡库。HF 有两种翻译路径：

1. **手动 GSAP 交叉淡入淡出** — 适用于简单的透明度/变换过渡。免费，无需额外包。
2. **HF 着色器过渡包** — 适用于视觉丰富的过渡，匹配 @remotion/transitions 预设。

## 模式：`<TransitionSeries>` 就是带重叠的 `<Series>`

```tsx
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

翻译为按过渡时长重叠的场景：

- SceneA：[0, 60] = `data-start="0" data-duration="2"`
- SceneB：[60-15, 60-15+60] = `data-start="1.5" data-duration="2"`（过渡窗口重叠了 A 的结尾和 B 的开头）

然后使用 GSAP 驱动过渡：

```js
// 手动淡入淡出 (presentation={fade()})
tl.to(sceneA, { opacity: 0, duration: 0.5, ease: "none" }, 1.5);
tl.fromTo(sceneB, { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "none" }, 1.5);
```

## 过渡效果对照表

| Remotion `presentation`            | HF 翻译                                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| `fade()`                           | 手动 `gsap.to(opacity)` 交叉淡入淡出                                                         |
| `slide({direction: "from-right"})` | `gsap.fromTo(translateX: "100%" → 0)` 进入 + `to(translateX: "-100%")` 退出                  |
| `wipe({direction: "from-left"})`   | `gsap.fromTo(clip-path: inset(0 100% 0 0) → inset(0 0 0 0))` 进入                            |
| `clockWipe()`                      | 使用 HF 的 `sdf-iris` 着色器过渡（`npx hyperframes add sdf-iris`）                           |
| `flip()`                           | `gsap.to(rotateY)` 在场景之间 180° 分割                                                      |
| `cube()`                           | 使用 HF 的 `cinematic-zoom` 或使用 `rotateY` + `transform-origin` 手动构建                   |
| `iris()`                           | 使用 HF 的 `sdf-iris` 着色器过渡                                                              |
| `none()`                           | 无过渡；边界处硬切换                                                                         |

## 时间翻译

```tsx
linearTiming({durationInFrames: 15})              → ease: "none"
linearTiming({durationInFrames: 15, easing: ...}) → 按 timing.md 中的缓动表对应缓动函数
springTiming({config: {damping: 12}})             → ease: "back.out(1.4)" (~0.7 s)
```

将 `durationInFrames` 转换为秒（`/fps`）。

## 何时使用 HF 着色器过渡

对于 Remotion 预设中具有视觉丰富的 GLSL 等效效果的过渡（iris、ripple、zoom、glitch），使用 HF 的 [shader-transitions](https://hyperframes.heygen.com/catalog/blocks) 包。它们产生比手动 GSAP 变换更丰富的输出。

```bash
npx hyperframes add sdf-iris
```

然后在合成中：

```html
<div id="iris-transition" class="hf-shader-transition" data-start="1.5" data-duration="0.5">
  <!-- 通过着色器过渡的 data-from / data-to 绑定场景 -->
</div>
```

每个着色器过渡有其自己的 data 属性；查看目录页了解具体块。

## 当源码使用自定义 Presentation

Remotion 支持自定义 `presentation` 实现：

```tsx
const customPresentation: PresentationComponent = ({
  children,
  presentationProgress,
  presentationDirection,
}) => {
  return (
    <div
      style={
        {
          /* 从进度计算变换 */
        }
      }
    >
      {children}
    </div>
  );
};
```

翻译：从 `style={...}` 块中提取数学计算并生成等价的 GSAP 补间动画。具体来说，变换公式直接映射到由 `progress` 参数化的 `gsap.to(target, { transform: ... })`。

如果自定义 presentation 在内部使用 `useCurrentFrame()` 来动画化 _超出_ 简单进度曲线的内容，则将源码视为不可翻译，并退出到运行时互操作模式（参见 [escape-hatch.md](escape-hatch.md)）。
