---
name: tailwind
description: 在 Remotion 中使用 TailwindCSS
metadata:
---

如果项目中安装了 TailwindCSS，你可以且应该使用它。

不要使用 `transition-*` 或 `animate-*` 类——始终使用 `useCurrentFrame()` 钩子驱动动画。

在 Remotion 项目中需要先安装并启用 Tailwind——使用 WebFetch 获取 https://www.remotion.dev/docs/tailwind 的安装说明。
