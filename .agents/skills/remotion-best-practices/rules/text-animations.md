---
name: text-animations
description: Remotion 的排版和文本动画模式
metadata:
  tags: typography, text, typewriter, highlighter ken
---

## 文本动画

基于 `useCurrentFrame()`，逐字符减少字符串以创建打字机效果。

## 打字机效果

查看[打字机](assets/text-animations-typewriter.tsx)了解带有闪烁光标和首句后暂停的高级示例。

始终使用字符串切片来实现打字机效果。切勿使用逐字符透明度。

## 单词高亮

查看[单词高亮](assets/text-animations-word-highlight.tsx)了解如何动画化单词高亮（如使用荧光笔）的示例。
