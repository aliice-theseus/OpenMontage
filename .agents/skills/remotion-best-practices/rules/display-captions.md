---
name: display-captions
description: 在 Remotion 中显示字幕，支持 TikTok 风格页面和单词高亮
metadata:
  tags: captions, subtitles, display, tiktok, highlight
---

# 在 Remotion 中显示字幕

本指南说明如何在 Remotion 中显示字幕，假设你已经拥有 [`Caption`](https://www.remotion.dev/docs/captions/caption) 格式的字幕。

## 前置条件

阅读[音频转写](transcribe-captions.md)了解如何生成字幕。

首先，需要安装 [`@remotion/captions`](https://www.remotion.dev/docs/captions) 包。
如果尚未安装，请使用以下命令：

```bash
npx remotion add @remotion/captions
```

## 获取字幕

首先，获取你的字幕 JSON 文件。使用 [`useDelayRender()`](https://www.remotion.dev/docs/use-delay-render) 延迟渲染直至字幕加载完成：

```tsx
import { useState, useEffect, useCallback } from "react";
import { AbsoluteFill, staticFile, useDelayRender } from "remotion";
import type { Caption } from "@remotion/captions";

export const MyComponent: React.FC = () => {
  const [captions, setCaptions] = useState<Caption[] | null>(null);
  const { delayRender, continueRender, cancelRender } = useDelayRender();
  const [handle] = useState(() => delayRender());

  const fetchCaptions = useCallback(async () => {
    try {
      // 假设 captions.json 位于 public/ 文件夹中
      const response = await fetch(staticFile("captions123.json"));
      const data = await response.json();
      setCaptions(data);
      continueRender(handle);
    } catch (e) {
      cancelRender(e);
    }
  }, [continueRender, cancelRender, handle]);

  useEffect(() => {
    fetchCaptions();
  }, [fetchCaptions]);

  if (!captions) {
    return null;
  }

  return <AbsoluteFill>{/* 在此处渲染字幕 */}</AbsoluteFill>;
};
```

## 创建页面

使用 `createTikTokStyleCaptions()` 将字幕分组到页面中。`combineTokensWithinMilliseconds` 选项控制每次显示的单词数量：

```tsx
import { useMemo } from "react";
import { createTikTokStyleCaptions } from "@remotion/captions";
import type { Caption } from "@remotion/captions";

// 字幕切换频率（毫秒）
// 值越高 = 每页显示更多单词
// 值越低 = 显示更少单词（逐字显示）
const SWITCH_CAPTIONS_EVERY_MS = 1200;

const { pages } = useMemo(() => {
  return createTikTokStyleCaptions({
    captions,
    combineTokensWithinMilliseconds: SWITCH_CAPTIONS_EVERY_MS,
  });
}, [captions]);
```

## 使用序列渲染

遍历页面并在 `<Sequence>` 中渲染每个页面。根据页面时间计算起始帧和时长：

```tsx
import { Sequence, useVideoConfig, AbsoluteFill } from "remotion";
import type { TikTokPage } from "@remotion/captions";

const CaptionedContent: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill>
      {pages.map((page, index) => {
        const nextPage = pages[index + 1] ?? null;
        const startFrame = (page.startMs / 1000) * fps;
        const endFrame = Math.min(
          nextPage ? (nextPage.startMs / 1000) * fps : Infinity,
          startFrame + (SWITCH_CAPTIONS_EVERY_MS / 1000) * fps,
        );
        const durationInFrames = endFrame - startFrame;

        if (durationInFrames <= 0) {
          return null;
        }

        return (
          <Sequence
            key={index}
            from={startFrame}
            durationInFrames={durationInFrames}
          >
            <CaptionPage page={page} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

## 保留空白字符

字幕对空白字符敏感。你应在每个单词前的 `text` 字段中包含空格。使用 `whiteSpace: "pre"` 来保留字幕中的空白字符。

## 为字幕创建独立组件

将字幕逻辑放在单独的组件中。  
为其创建一个新文件。

## 单词高亮

字幕页面包含 `tokens`，你可以使用它们来高亮当前正在朗读的单词：

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { TikTokPage } from "@remotion/captions";

const HIGHLIGHT_COLOR = "#39E508";

const CaptionPage: React.FC<{ page: TikTokPage }> = ({ page }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 当前时间相对于序列开始
  const currentTimeMs = (frame / fps) * 1000;
  // 通过添加页面开始时间转换为绝对时间
  const absoluteTimeMs = page.startMs + currentTimeMs;

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{ fontSize: 80, fontWeight: "bold", whiteSpace: "pre" }}>
        {page.tokens.map((token) => {
          const isActive =
            token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs;

          return (
            <span
              key={token.fromMs}
              style={{ color: isActive ? HIGHLIGHT_COLOR : "white" }}
            >
              {token.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

## 在视频内容旁边显示字幕

默认情况下，将字幕与视频内容放在一起，使字幕保持同步。  
为每个视频创建一个新的字幕 JSON 文件。

```tsx
<AbsoluteFill>
  <Video src={staticFile("video.mp4")} />
  <CaptionPage page={page} />
</AbsoluteFill>
```
