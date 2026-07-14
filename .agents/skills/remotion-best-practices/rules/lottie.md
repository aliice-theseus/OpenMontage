---
name: lottie
description: 在 Remotion 中嵌入 Lottie 动画
metadata:
  category: Animation
---

# 在 Remotion 中使用 Lottie 动画

## 前置条件

首先，需要安装 @remotion/lottie 包。  
如果尚未安装，请使用以下命令：

```bash
npx remotion add @remotion/lottie # 如果项目使用 npm
bunx remotion add @remotion/lottie # 如果项目使用 bun
yarn remotion add @remotion/lottie # 如果项目使用 yarn
pnpm exec remotion add @remotion/lottie # 如果项目使用 pnpm
```

## 显示 Lottie 文件

要导入 Lottie 动画：

- 获取 Lottie 资源
- 将加载过程包裹在 `delayRender()` 和 `continueRender()` 中
- 将动画数据保存在状态中
- 使用 `@remotion/lottie` 包的 `Lottie` 组件渲染 Lottie 动画

```tsx
import { Lottie, LottieAnimationData } from "@remotion/lottie";
import { useEffect, useState } from "react";
import { cancelRender, continueRender, delayRender } from "remotion";

export const MyAnimation = () => {
  const [handle] = useState(() => delayRender("正在加载 Lottie 动画"));

  const [animationData, setAnimationData] =
    useState<LottieAnimationData | null>(null);

  useEffect(() => {
    fetch("https://assets4.lottiefiles.com/packages/lf20_zyquagfl.json")
      .then((data) => data.json())
      .then((json) => {
        setAnimationData(json);
        continueRender(handle);
      })
      .catch((err) => {
        cancelRender(err);
      });
  }, [handle]);

  if (!animationData) {
    return null;
  }

  return <Lottie animationData={animationData} />;
};
```

## 样式和动画

Lottie 支持 `style` 属性来应用样式和动画：

```tsx
return (
  <Lottie animationData={animationData} style={{ width: 400, height: 400 }} />
);
```
