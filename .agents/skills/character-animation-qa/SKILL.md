---
name: character-animation-qa
description: 通过 schema 检查、Playwright 浏览器预览、帧采样和 FFmpeg/ffprobe 最终输出检查来审查本地角色动画。
license: MIT
---

# 角色动画 QA

在展示角色动画预览或最终渲染之前使用此技能。

## 审查层次

1. Schema 验证：角色设计、绑定计划、姿态库、动作时间线。
2. 静态资源检查：引用的部件和背景存在。
3. 浏览器预览：加载预览、截取屏幕截图、收集控制台错误。
4. 运动检查：比较采样帧是否存在非微小差异。
5. 最终 MP4 检查：ffprobe 元数据、时长、分辨率、音频、帧样本。
6. 代理视觉审查：检查采样帧是否存在肢体分离、图层错误、角色出框、表情模糊、文字断裂。

## Playwright 模式

```ts
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
await page.goto(previewUrl, { waitUntil: "networkidle" });
await page.screenshot({ path: "preview.png" });
```

## 通过/修改/失败

- `pass`：技术检查通过，表演可读。
- `revise`：可修复的绑定/时间线问题。
- `fail`：缺少资源、渲染空白、运行失败或运行时错误。

## 参考资料

- Playwright 屏幕截图：
  https://playwright.dev/docs/screenshots
- Playwright 页面导航：
  https://playwright.dev/docs/api/class-page#page-goto
- FFmpeg/ffprobe 应用于最终媒体探测：
  https://ffmpeg.org/ffprobe.html
