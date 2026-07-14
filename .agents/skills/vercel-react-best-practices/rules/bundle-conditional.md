---
title: 条件模块加载
impact: HIGH
impactDescription: 仅在需要时加载大数据
tags: bundle, conditional-loading, lazy-loading
---

## 条件模块加载

仅在功能激活时加载大数据或模块。

**示例（延迟加载动画帧）：**

```tsx
function AnimationPlayer({ enabled, setEnabled }: { enabled: boolean; setEnabled: React.Dispatch<React.SetStateAction<boolean>> }) {
  const [frames, setFrames] = useState<Frame[] | null>(null)

  useEffect(() => {
    if (enabled && !frames && typeof window !== 'undefined') {
      import('./animation-frames.js')
        .then(mod => setFrames(mod.frames))
        .catch(() => setEnabled(false))
    }
  }, [enabled, frames, setEnabled])

  if (!frames) return <Skeleton />
  return <Canvas frames={frames} />
}
```

`typeof window !== 'undefined'` 检查防止将此模块打包用于 SSR，优化了服务端包大小和构建速度。
