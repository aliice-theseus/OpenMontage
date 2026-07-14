---
name: playwright-recording
description: 使用 Playwright 将浏览器交互录制为视频。适用于为 Remotion 视频捕获演示视频、应用导览和 UI 流程。触发场景包括录制演示、捕获浏览器视频、屏幕录制网站或创建导览素材。
---

# Playwright 视频录制

Playwright 可以将浏览器交互录制为视频 — 非常适合 Remotion 合成中的演示素材。

## 快速开始

### 安装

```bash
# 在您的视频项目中
npm init -y
npm install -D playwright @playwright/test
npx playwright install chromium
```

### 基础录制脚本

```typescript
// scripts/record-demo.ts
import { chromium } from 'playwright';

async function recordDemo() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: {
      dir: './recordings',
      size: { width: 1920, height: 1080 }
    }
  });

  const page = await context.newPage();

  // 您的录制操作
  await page.goto('https://example.com');
  await page.waitForTimeout(2000);
  await page.click('button.demo');
  await page.waitForTimeout(3000);

  // 关闭以保存视频
  await context.close();
  await browser.close();

  console.log('Recording saved to ./recordings/');
}

recordDemo();
```

运行方式：
```bash
npx ts-node scripts/record-demo.ts
# 或
npx tsx scripts/record-demo.ts
```

## 录制配置

### 视口尺寸

```typescript
// 标准 1080p（推荐用于 Remotion）
viewport: { width: 1920, height: 1080 }

// 720p（较小文件）
viewport: { width: 1280, height: 720 }

// 正方形（社交媒体）
viewport: { width: 1080, height: 1080 }

// 移动端
viewport: { width: 390, height: 844 } // iPhone 14
```

### 视频质量设置

```typescript
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  recordVideo: {
    dir: './recordings',
    size: { width: 1920, height: 1080 } // 与视口匹配以获得清晰输出
  },
  // 降低速度以提高可见性
  // 注意：slowMo 是在浏览器启动时设置，而非 context
});

// 对于慢动作，使用 slowMo 启动浏览器
const browser = await chromium.launch({
  slowMo: 100 // 操作间延迟 100ms
});
```

## 录制模式

### 表单提交演示

```typescript
import { chromium } from 'playwright';

async function recordFormDemo() {
  const browser = await chromium.launch({ slowMo: 50 });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: './recordings', size: { width: 1920, height: 1080 } }
  });
  const page = await context.newPage();

  await page.goto('https://myapp.com/form');
  await page.waitForTimeout(1000);

  // 以真实速度输入
  await page.fill('#name', 'John Smith', { timeout: 5000 });
  await page.waitForTimeout(500);

  await page.fill('#email', 'john@example.com');
  await page.waitForTimeout(500);

  // 点击提交
  await page.click('button[type="submit"]');

  // 等待结果
  await page.waitForSelector('.success-message');
  await page.waitForTimeout(2000);

  await context.close();
  await browser.close();
}
```

### 多页面导航

```typescript
async function recordNavDemo() {
  const browser = await chromium.launch({ slowMo: 100 });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: './recordings', size: { width: 1920, height: 1080 } }
  });
  const page = await context.newPage();

  // 页面 1
  await page.goto('https://myapp.com');
  await page.waitForTimeout(2000);

  // 导航到页面 2
  await page.click('nav a[href="/features"]');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);

  // 导航到页面 3
  await page.click('nav a[href="/pricing"]');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);

  await context.close();
  await browser.close();
}
```

### 滚动演示

```typescript
async function recordScrollDemo() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: './recordings', size: { width: 1920, height: 1080 } }
  });
  const page = await context.newPage();

  await page.goto('https://myapp.com/long-page');
  await page.waitForTimeout(1000);

  // 平滑滚动
  await page.evaluate(async () => {
    const delay = (ms: number) => new Promise(r => setTimeout(r, ms));
    for (let i = 0; i < 10; i++) {
      window.scrollBy({ top: 200, behavior: 'smooth' });
      await delay(300);
    }
  });

  await page.waitForTimeout(1000);
  await context.close();
  await browser.close();
}
```

### 登录流程

```typescript
async function recordLoginDemo() {
  const browser = await chromium.launch({ slowMo: 75 });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: './recordings', size: { width: 1920, height: 1080 } }
  });
  const page = await context.newPage();

  await page.goto('https://myapp.com/login');
  await page.waitForTimeout(1000);

  await page.fill('#email', 'demo@example.com');
  await page.waitForTimeout(300);

  await page.fill('#password', '••••••••');
  await page.waitForTimeout(500);

  await page.click('button[type="submit"]');

  // 等待仪表板
  await page.waitForURL('**/dashboard');
  await page.waitForTimeout(3000);

  await context.close();
  await browser.close();
}
```

## 光标高亮

Playwright 默认不显示光标。添加视觉指示器：

### CSS 光标高亮

```typescript
// 注入光标可视化
await page.addStyleTag({
  content: `
    * { cursor: none !important; }
    .playwright-cursor {
      position: fixed;
      width: 24px;
      height: 24px;
      background: rgba(255, 100, 100, 0.5);
      border: 2px solid rgba(255, 50, 50, 0.8);
      border-radius: 50%;
      pointer-events: none;
      z-index: 999999;
      transform: translate(-50%, -50%);
      transition: transform 0.1s ease;
    }
    .playwright-cursor.clicking {
      transform: translate(-50%, -50%) scale(0.8);
      background: rgba(255, 50, 50, 0.8);
    }
  `
});

// 添加光标元素
await page.evaluate(() => {
  const cursor = document.createElement('div');
  cursor.className = 'playwright-cursor';
  document.body.appendChild(cursor);

  document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
  });

  document.addEventListener('mousedown', () => cursor.classList.add('clicking'));
  document.addEventListener('mouseup', () => cursor.classList.remove('clicking'));
});
```

### 点击波纹效果

```typescript
// 添加点击波纹可视化
await page.addStyleTag({
  content: `
    .click-ripple {
      position: fixed;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: rgba(234, 88, 12, 0.4);
      pointer-events: none;
      z-index: 999998;
      transform: translate(-50%, -50%) scale(0);
      animation: ripple 0.4s ease-out forwards;
    }
    @keyframes ripple {
      to {
        transform: translate(-50%, -50%) scale(2);
        opacity: 0;
      }
    }
  `
});

// 带波纹的自定义点击函数
async function clickWithRipple(page, selector) {
  const element = await page.locator(selector);
  const box = await element.boundingBox();

  await page.evaluate(({ x, y }) => {
    const ripple = document.createElement('div');
    ripple.className = 'click-ripple';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    document.body.appendChild(ripple);
    setTimeout(() => ripple.remove(), 400);
  }, { x: box.x + box.width / 2, y: box.y + box.height / 2 });

  await element.click();
}
```

## 输出到 Remotion

### 将录制文件移动到 public/demos/

```typescript
import { chromium } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

async function recordForRemotion(outputName: string) {
  const browser = await chromium.launch({ slowMo: 50 });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: './temp-recordings', size: { width: 1920, height: 1080 } }
  });
  const page = await context.newPage();

  // ... 录制操作 ...

  await context.close();

  // 获取视频路径
  const video = page.video();
  const videoPath = await video?.path();

  if (videoPath) {
    const destPath = `./public/demos/${outputName}.webm`;
    fs.mkdirSync(path.dirname(destPath), { recursive: true });
    fs.renameSync(videoPath, destPath);
    console.log(`Recording saved to: ${destPath}`);

    // 获取时长用于配置
    // 使用 ffprobe：ffprobe -v error -show_entries format=duration -of csv=p=0 file.webm
  }

  await browser.close();
}
```

### 将 WebM 转换为 MP4

Playwright 输出 WebM。转换为更好的 Remotion 兼容性：

```bash
ffmpeg -i recording.webm -c:v libx264 -crf 20 -preset medium -movflags faststart public/demos/demo.mp4
```

## 交互式录制

用于用户手动操作的录制：

```typescript
// 注入 ESC 键监听器以停止录制
async function injectStopListener(page: Page): Promise<void> {
  await page.evaluate(() => {
    if ((window as any).__escListenerAdded) return;
    (window as any).__escListenerAdded = true;
    (window as any).__stopRecording = false;
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        (window as any).__stopRecording = true;
      }
    });
  });
}

// 轮询停止信号 - 优雅处理导航错误
while (!stopped) {
  try {
    const shouldStop = await page.evaluate(() => (window as any).__stopRecording === true);
    if (shouldStop) break;
  } catch {
    // 页面导航中 - 继续录制
  }
  await new Promise(r => setTimeout(r, 200));
}
```

**关键要点：** `page.evaluate()` 在导航期间会抛出异常。使用 try/catch 并继续 — 不要将错误视为停止信号。

## 笔记本电脑窗口缩放

以全 1080p 录制同时显示较小窗口：

```typescript
const scale = 0.75; // 75% 窗口大小
const context = await browser.newContext({
  viewport: { width: 1920 * scale, height: 1080 * scale },
  deviceScaleFactor: 1 / scale,
  recordVideo: { dir: './recordings', size: { width: 1920, height: 1080 } },
});
```

## Cookie 横幅关闭

常见同意平台的全面选择器列表：

```typescript
const COOKIE_SELECTORS = [
  '#onetrust-accept-btn-handler',           // OneTrust
  '#CybotCookiebotDialogBodyButtonAccept',  // Cookiebot
  '.cc-btn.cc-dismiss',                      // Cookie Consent by Insites
  '[class*="cookie"] button[class*="accept"]',
  '[class*="consent"] button[class*="accept"]',
  'button:has-text("Accept all")',
  'button:has-text("Accept cookies")',
  'button:has-text("Got it")',
];

async function dismissCookieBanners(page: Page): Promise<void> {
  await page.waitForTimeout(500);
  for (const selector of COOKIE_SELECTORS) {
    try {
      const btn = page.locator(selector).first();
      if (await btn.isVisible({ timeout: 100 })) {
        await btn.click({ timeout: 500 });
        return;
      }
    } catch { /* try next */ }
  }
}
```

在 `page.goto()` 之后和导航的 `page.on('load')` 时调用。

## 重要提示：注入元素会出现在视频中

**警告：** 您注入的任何 DOM 元素（光标、控制面板、覆盖层）都会被录制。对于无 UI 的录制，仅使用基于终端的控制（Ctrl+C、最大时长计时器）。

## 良好演示录制的技巧

1. **使用 slowMo** - 50-100ms 使操作可见
2. **添加 waitForTimeout** - 在操作之间暂停以便理解
3. **等待动画完成** - 使用 `waitForLoadState('networkidle')`
4. **匹配 Remotion 尺寸** - 通常 1920x1080 30fps
5. **先不录制测试** - 在最终捕获前调试
6. **清除浏览器状态** - 使用新 context 以获得干净的演示
7. **关闭 Cookie 横幅** - 使用上面的全面选择器列表
8. **导航后重新注入** - 光标/监听器在页面加载时重置

---

## 反馈与贡献

如果此技能缺少信息或可以改进：

- **缺少某个模式？** 描述您需要的内容
- **发现错误？** 请告知问题所在
- **想要贡献？** 我可以帮助您：
  1. 用改进更新此技能
  2. 向 github.com/digitalsamba/claude-code-video-toolkit 创建 PR

只需说"improve this skill"，我将引导您更新 `.claude/skills/playwright-recording/SKILL.md`。
