---
name: gif
description: 在 Remotion 中显示 GIF、APNG、AVIF 和 WebP
metadata:
  tags: gif, animation, images, animated, apng, avif, webp
---

# 在 Remotion 中使用动画图片

## 基本用法

使用 `<AnimatedImage>` 显示与 Remotion 时间线同步的 GIF、APNG、AVIF 或 WebP 图片：

```tsx
import { AnimatedImage, staticFile } from "remotion";

export const MyComposition = () => {
  return (
    <AnimatedImage src={staticFile("animation.gif")} width={500} height={500} />
  );
};
```

也支持远程 URL（必须启用 CORS）：

```tsx
<AnimatedImage
  src="https://example.com/animation.gif"
  width={500}
  height={500}
/>
```

## 尺寸和适配

使用 `fit` 属性控制图片如何填充容器：

```tsx
// 拉伸填充（默认）
<AnimatedImage src={staticFile("animation.gif")} width={500} height={300} fit="fill" />

// 保持宽高比，适配容器内部
<AnimatedImage src={staticFile("animation.gif")} width={500} height={300} fit="contain" />

// 填充容器，必要时裁剪
<AnimatedImage src={staticFile("animation.gif")} width={500} height={300} fit="cover" />
```

## 播放速度

使用 `playbackRate` 控制动画速度：

```tsx
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} playbackRate={2} /> {/* 2 倍速 */}
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} playbackRate={0.5} /> {/* 半速 */}
```

## 循环行为

控制动画完成时的行为：

```tsx
// 无限循环（默认）
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} loopBehavior="loop" />

// 播放一次，显示最后一帧
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} loopBehavior="pause-after-finish" />

// 播放一次，然后清除画布
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} loopBehavior="clear-after-finish" />
```

## 样式

使用 `style` 属性添加额外的 CSS（使用 `width` 和 `height` 属性控制尺寸）：

```tsx
<AnimatedImage
  src={staticFile("animation.gif")}
  width={500}
  height={500}
  style={{
    borderRadius: 20,
    position: "absolute",
    top: 100,
    left: 50,
  }}
/>
```

## 获取 GIF 时长

使用 `@remotion/gif` 的 `getGifDurationInSeconds()` 获取 GIF 的时长。

```bash
npx remotion add @remotion/gif
```

```tsx
import { getGifDurationInSeconds } from "@remotion/gif";
import { staticFile } from "remotion";

const duration = await getGifDurationInSeconds(staticFile("animation.gif"));
console.log(duration); // 例如 2.5
```

这对于设置合成长度以匹配 GIF 很有用：

```tsx
import { getGifDurationInSeconds } from "@remotion/gif";
import { staticFile, CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction = async () => {
  const duration = await getGifDurationInSeconds(staticFile("animation.gif"));
  return {
    durationInFrames: Math.ceil(duration * 30),
  };
};
```

## 备选方案

如果 `<AnimatedImage>` 无法工作（仅 Chrome 和 Firefox 支持），可以使用 `@remotion/gif` 中的 `<Gif>` 替代。

```bash
npx remotion add @remotion/gif # 如果项目使用 npm
bunx remotion add @remotion/gif # 如果项目使用 bun
yarn remotion add @remotion/gif # 如果项目使用 yarn
pnpm exec remotion add @remotion/gif # 如果项目使用 pnpm
```

```tsx
import { Gif } from "@remotion/gif";
import { staticFile } from "remotion";

export const MyComposition = () => {
  return <Gif src={staticFile("animation.gif")} width={500} height={500} />;
};
```

`<Gif>` 组件具有与 `<AnimatedImage>` 相同的属性，但仅支持 GIF 文件。
